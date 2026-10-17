"""One isolated native fit. This process is never given held-out target labels."""

import argparse
import csv
import gzip
import hashlib
import json
import os
import pickle
import resource
import sys
import time
import traceback
import warnings
from pathlib import Path


def dump(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False, default=str))
    temporary.replace(path)


def choose(candidates, x, y, xv, yv, names, state, history):
    import numpy as np

    from .expressions import complexity
    from .external_math import export_expression, native_evaluate

    best, best_key = None, None
    for candidate in candidates:
        row = {
            "name": candidate.name,
            "detail": candidate.detail,
            "native_expression": candidate.expression,
        }
        try:
            prediction = np.asarray(candidate.predict(xv), dtype=float).reshape(-1)
            if prediction.shape != yv.shape or not np.all(np.isfinite(prediction)):
                raise ValueError("Invalid validation prediction")
            error = float(np.sqrt(np.mean((prediction - yv) ** 2)))
            if not np.isfinite(error):
                raise ValueError("Nonfinite validation error")
            expression = None
            if candidate.expression is not None:
                # Verify native output translation on training/validation only.
                for values in (x, xv):
                    native = np.asarray(candidate.predict(values), dtype=float).reshape(-1)
                    replay = native_evaluate(candidate.expression, values)
                    if not np.allclose(native, replay, rtol=1e-9, atol=1e-10):
                        raise ValueError(
                            "Native expression export disagrees with backend prediction"
                        )
                expression = export_expression(candidate.expression, names, state)
                cost = complexity(expression)
            else:
                # Non-symbolic candidates have no expression complexity ranking.
                cost = 0
            key = (error, cost, expression or candidate.name)
            row.update(
                status="valid",
                validation_rmse_scaled=error,
                registered_complexity=cost,
                expression=expression,
            )
            if best_key is None or key < best_key:
                best, best_key = (candidate, expression), key
        except (
            ValueError,
            FloatingPointError,
            OverflowError,
            TypeError,
            SyntaxError,
            IndexError,
        ) as error:
            row.update(status="invalid_candidate", error=str(error))
        history.append(row)
        dump("candidate-history.json", history)
    if best is None:
        raise ValueError("No valid validation-selected candidate")
    return best, best_key


def run(request):
    import numpy as np
    from threadpoolctl import threadpool_limits

    from .external_math import apply_transform, transform
    from .external_solvers import SOLVERS

    seed = request["seed"]
    import random

    random.seed(seed)
    np.random.seed(seed)
    threadpool_limits(1)
    payload = Path(request["payload"])
    if hashlib.sha256(payload.read_bytes()).hexdigest() != request["payload_sha256"]:
        raise ValueError("Training payload hash mismatch")
    with np.load(payload, allow_pickle=False) as data:
        required = {
            "x_train",
            "y_train",
            "x_validation",
            "y_validation",
            "x_test",
            "test_ids",
            "features",
        }
        if set(data.files) != required:
            raise ValueError("Payload must contain no test labels or source/formula metadata")
        x, y = data["x_train"], data["y_train"]
        xv, yv = data["x_validation"], data["y_validation"]
        names = data["features"].tolist()
        state = transform(x, y, request["model"], names)
        tx, tv = apply_transform(x, state), apply_transform(xv, state)
        ty = (y - state["y_offset"]) / state["y_scale"]
        vy = (yv - state["y_offset"]) / state["y_scale"]
        details, history = {}, []
        dump("transform.json", state)
        caught = []
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                candidates = SOLVERS[request["model"]](
                    tx, ty, tv, vy, seed, request["profile"], details
                )
                (selected, expression), key = choose(
                    candidates, tx, ty, tv, vy, names, state, history
                )
        finally:
            dump("solver-details.json", details)
            dump(
                "warnings.json",
                [{"category": w.category.__name__, "message": str(w.message)} for w in caught],
            )
        # Selection is sealed before accessing test coordinates or predictions.
        selected_record = {
            "name": selected.name,
            "expression": expression,
            "validation_key": key,
            "state": state,
            "candidate_count": len(history),
            "details": details,
        }
        dump("selected.json", selected_record)
        if selected.model is not None:
            with gzip.open("selected-model.pkl.gz", "wb", compresslevel=1) as stream:
                pickle.dump(selected.model, stream, protocol=pickle.HIGHEST_PROTOCOL)
        test = apply_transform(data["x_test"], state)
        prediction = state["y_offset"] + state["y_scale"] * np.asarray(
            selected.predict(test)
        ).reshape(-1)
        if prediction.shape != (len(test),) or not np.all(np.isfinite(prediction)):
            raise ValueError(
                "Selected candidate has invalid held-out predictions; no reselection allowed"
            )
        with Path("predictions.csv").open("w", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(["sample_id", "prediction"])
            writer.writerows(zip(data["test_ids"].tolist(), prediction.tolist()))
        # Keep training predictions for independent replay and cost/fit auditing.
        np.savez_compressed(
            "selected-training-predictions.npz",
            train=state["y_offset"] + state["y_scale"] * selected.predict(tx),
            validation=state["y_offset"] + state["y_scale"] * selected.predict(tv),
        )
    return selected_record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text())
    start = time.monotonic()
    status = "failed"
    try:
        if request["model"] in {"NuSR", "MySR"}:
            raise ValueError("Product models are excluded from this campaign")
        result = run(request)
        status = "fitted"
        dump("worker-result.json", {"status": status, "selected": result})
    except Exception as error:  # noqa: BLE001 -- preserve native solver failures as terminal records
        traceback.print_exc()
        dump(
            "worker-result.json",
            {"status": "failed", "error_type": type(error).__name__, "error": str(error)},
        )
    finally:
        own, children = (
            resource.getrusage(resource.RUSAGE_SELF),
            resource.getrusage(resource.RUSAGE_CHILDREN),
        )
        dump(
            "worker-resources.json",
            {
                "wall_seconds": time.monotonic() - start,
                "cpu_user_seconds": own.ru_utime + children.ru_utime,
                "cpu_system_seconds": own.ru_stime + children.ru_stime,
                "largest_process_peak_rss_kib": max(own.ru_maxrss, children.ru_maxrss),
                "affinity": sorted(os.sched_getaffinity(0)),
                "pid": os.getpid(),
                "note": "CPU includes process imports and waited native children; RSS is not concurrent tree sum",
            },
        )
    sys.exit(0 if status == "fitted" else 1)


if __name__ == "__main__":
    main()
