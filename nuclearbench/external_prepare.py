"""Prepare answer-free fit payloads and a complete deterministic request matrix."""

import argparse
import hashlib
import json
import math
import time
from collections import Counter
from pathlib import Path

import numpy as np

from .bank import get_task, load_bank, validate
from .expressions import evaluate
from .external_profiles import FEATURES, PROFILES, requests
from .sources import digest


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def identity(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def training_noise(task_id, sample_id, scale, level):
    if not level:
        return 0.0
    seed = int(
        hashlib.sha256((task_id + ":" + sample_id + ":noise101").encode()).hexdigest()[:16], 16
    )
    u = (seed + 1) / (2**64 + 1)
    v = (int(hashlib.sha256(str(seed).encode()).hexdigest()[:16], 16) + 1) / (2**64 + 1)
    return level * scale * math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)


def payload(root, task_id, split, mode, noise, destination):
    _task, rows, parts = get_task(root, task_id)
    selected = parts[split]
    if selected["status"] != "enabled":
        raise ValueError("Cannot replace an unsupported split")
    by_id = {r["sample_id"]: r for r in rows}
    # Partition IDs are retained exactly; only ordering is canonicalized.
    sets = {
        name: [by_id[i] for i in selected["partitions"][name]]
        for name in ("train", "validation", "test")
    }
    features = ("N", "Z") if mode == "raw" else FEATURES
    data = {"features": np.asarray(features)}
    for name, values in sets.items():
        n = np.asarray([r["N"] for r in values], dtype=float)
        z = np.asarray([r["Z"] for r in values], dtype=float)
        data["x_" + name] = np.column_stack([evaluate(f, n, z) for f in features])
        if name != "test":
            data["y_" + name] = np.asarray([r["y"] for r in values], dtype=float)
        else:
            data["test_ids"] = np.asarray([r["sample_id"] for r in values])
    sigma = float(np.std(data["y_train"]))
    data["y_train"] += np.asarray(
        [training_noise(task_id, r["sample_id"], sigma, noise) for r in sets["train"]]
    )
    np.savez_compressed(destination, **data)
    return {
        "path": str(destination.resolve()),
        "sha256": digest(destination),
        "counts": {k: len(v) for k, v in sets.items()},
        "features": list(features),
        "noise_training_std": sigma,
        "has_test_labels": False,
    }


def prepare(bank_root, output):
    start = time.monotonic()
    validate(bank_root)
    output.mkdir(exist_ok=False, parents=True)
    (output / "payloads").mkdir()
    bank = load_bank(bank_root)
    fingerprint = digest(Path(bank_root) / "checksums.json")
    payloads, matrix = {}, []
    for spec in requests(bank):
        key = (spec["task"], spec["split"], spec["mode"], spec["noise"])
        if key not in payloads:
            name = identity(list(key))
            payloads[key] = payload(bank_root, *key, output / "payloads" / (name + ".npz"))
        item = {
            **spec,
            "profile": PROFILES[spec["model"]],
            "bank_checksums_sha256": fingerprint,
            "payload": payloads[key]["path"],
            "payload_sha256": payloads[key]["sha256"],
        }
        item["request_id"] = identity(item)
        matrix.append(item)
    # Deterministic mixing prevents thousands of slow first-task fits from
    # starving other models/tasks. It is independent of observed outcomes.
    matrix.sort(key=lambda item: item["request_id"])
    with (output / "requests.jsonl").open("w") as stream:
        for item in matrix:
            stream.write(canonical(item) + "\n")
    (output / "payload-inventory.json").write_text(json.dumps(list(payloads.values()), indent=2))
    summary = {
        "bank_version": bank["version"],
        "bank_checksums_sha256": fingerprint,
        "request_count": len(matrix),
        "task_count": len({r["task"] for r in matrix}),
        "models": dict(Counter(r["model"] for r in matrix)),
        "modes": dict(Counter(r["mode"] for r in matrix)),
        "noise": dict(Counter(str(r["noise"]) for r in matrix)),
        "development_runs": sum(r["evidence_role"] == "development" for r in matrix),
        "payload_count": len(payloads),
        "matrix_sha256": digest(output / "requests.jsonl"),
        "preparation_wall_seconds": time.monotonic() - start,
        "preparation_cpu_seconds": time.process_time(),
        "model_results_observed": False,
        "product_models_included": False,
    }
    (output / "matrix-summary.json").write_text(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.bank, args.output), indent=2))
