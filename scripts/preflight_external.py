"""Real native API and export smoke checks on a separate synthetic fixture.

Reduced budgets are explicitly preflight-only and never enter formal results.
"""

import argparse
import copy
import hashlib
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from nuclearbench.expressions import evaluate
from nuclearbench.external_campaign import environment
from nuclearbench.external_profiles import FEATURES, PROFILES


def run_case(args, model, mode):
    work = args.output / (model + "-" + mode)
    work.mkdir(exist_ok=False, parents=True)
    rng = np.random.default_rng(117)
    n = rng.integers(8, 100, 64)
    z = rng.integers(8, 80, 64)
    names = ["N", "Z"] if mode == "raw" else list(FEATURES)
    x = np.column_stack([evaluate(f, n, z) for f in names])
    y = 1.7 * n + 2.5 * z
    data = work / "fixture.npz"
    np.savez_compressed(
        data,
        x_train=x[:40],
        y_train=y[:40],
        x_validation=x[40:52],
        y_validation=y[40:52],
        x_test=x[52:],
        features=np.asarray(names),
        test_ids=np.asarray(["fixture" + str(i) for i in range(12)]),
    )
    profile = copy.deepcopy(PROFILES[model])
    if not args.production_budget:
        if model == "PySR":
            profile.update(
                populations=2,
                population_size=30,
                max_evals=3000,
                niterations=5,
                ncycles_per_iteration=10,
                optimizer_iterations=3,
            )
        elif model == "Operon":
            profile.update(
                population_size=30,
                pool_size=30,
                max_evaluations=1000,
                generations=5,
                optimizer_iterations=3,
            )
        elif model == "AI_Feynman":
            profile.update(BF_try_time=1, NN_epochs=10, polyfit_deg=2)
        elif model == "GPR":
            profile.update(n_restarts_optimizer=0)
        elif model == "LightGBM":
            profile.update(
                num_leaves=[7, 15], min_child_samples=[5], n_estimators=60, early_stopping_rounds=10
            )
        elif model == "MLP_ensemble":
            profile.update(
                hidden_layers=[[16, 16]],
                alpha=[1e-4],
                members=2,
                max_epochs=30,
                validation_every=5,
                patience_checks=3,
            )
    request = {
        "model": model,
        "seed": 7,
        "payload": str(data.resolve()),
        "payload_sha256": hashlib.sha256(data.read_bytes()).hexdigest(),
        "profile": profile,
        "purpose": "synthetic_contract_preflight",
    }
    path = work / "request.json"
    path.write_text(json.dumps(request, indent=2))
    source = str(Path(__file__).resolve().parents[1])
    python, env = environment(
        {"runtime": json.loads(args.runtime.read_text()), "source_root": source}, model, work
    )
    # No global fit wall-time cap; native smoke budgets are explicit above.
    with (work / "stdout.log").open("w") as out, (work / "stderr.log").open("w") as err:
        result = subprocess.run(
            [python, "-m", "nuclearbench.external_worker", "--request", str(path)],
            cwd=work,
            env=env,
            stdout=out,
            stderr=err,
            check=False,
        )
    if result.returncode:
        return {"model": model, "mode": mode, "status": "failed", "exit": result.returncode}
    import csv

    with (work / "predictions.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 12 and all(np.isfinite(float(r["prediction"])) for r in rows)
    selected = json.loads((work / "selected.json").read_text())
    assert selected["candidate_count"] > 0
    return {
        "model": model,
        "mode": mode,
        "status": "passed",
        "candidate_count": selected["candidate_count"],
        "production_budget": args.production_budget,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--modes", nargs="+", default=["raw", "nuclear"])
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--production-budget", action="store_true")
    args = parser.parse_args()
    args.runtime, args.output = args.runtime.resolve(), args.output.resolve()
    os.environ.update(OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
    cases = [(model, mode) for model in args.models for mode in args.modes]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_case, args, *case) for case in cases]
        results = []
        for future in futures:
            result = future.result()
            print(json.dumps(result), flush=True)
            results.append(result)
    args.output.mkdir(exist_ok=True, parents=True)
    (args.output / "summary.json").write_text(json.dumps(results, indent=2))
    raise SystemExit(0 if all(r["status"] == "passed" for r in results) else 1)
