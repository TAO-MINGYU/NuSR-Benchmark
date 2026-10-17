"""ID-aligned scoring; incomplete predictions fail rather than shrink the test set."""

import csv
import hashlib
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

from .bank import get_task
from .expressions import complexity, evaluate, prove
from .sources import digest


def partition(root, task_id, kind, part="test"):
    task, rows, splits = get_task(root, task_id)
    if kind not in splits or splits[kind]["status"] != "enabled":
        raise ValueError(f"Unavailable split: {task_id}:{kind}")
    ids = set(splits[kind]["partitions"][part])
    return task, [r for r in rows if r["sample_id"] in ids]


def load_predictions(path, expected):
    with Path(path).open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["sample_id", "prediction"]:
            raise ValueError("Prediction CSV must contain exactly sample_id,prediction")
        result = {}
        for row in reader:
            sid = row["sample_id"]
            if sid in result:
                raise ValueError(f"Duplicate prediction ID: {sid}")
            value = float(row["prediction"])
            if not math.isfinite(value):
                raise ValueError("Nonfinite prediction")
            result[sid] = value
    if set(result) != set(expected):
        raise ValueError(
            f"Prediction coverage mismatch: missing={len(set(expected) - set(result))}, unexpected={len(set(result) - set(expected))}"
        )
    return result


def metrics(rows, predictions, train_rows):
    residual = np.asarray([predictions[r["sample_id"]] - r["y"] for r in rows])
    scale = float(np.std([r["y"] for r in train_rows]))
    groups = defaultdict(list)
    for row, error in zip(rows, residual):
        groups[row["Z"]].append(float(error))
    chains = {
        str(z): {"n": len(errors), "rmse": math.sqrt(sum(e * e for e in errors) / len(errors))}
        for z, errors in sorted(groups.items())
    }
    rmse = float(np.sqrt(np.mean(residual**2)))
    return {
        "n": len(rows),
        "rmse": rmse,
        "mae": float(np.mean(abs(residual))),
        "bias": float(np.mean(residual)),
        "max_abs_error": float(np.max(abs(residual))),
        "nrmse_train_std": None if scale == 0 else rmse / scale,
        "isotope_macro_rmse": float(np.mean([c["rmse"] for c in chains.values()])),
        "worst_isotope_rmse": max(c["rmse"] for c in chains.values()),
        "chains": chains,
    }


def score(root, task_id, kind, prediction_file):
    task, test = partition(root, task_id, kind)
    _, train = partition(root, task_id, kind, "train")
    predictions = load_predictions(prediction_file, [r["sample_id"] for r in test])
    return dict(
        task=task_id,
        split=kind,
        panel=task["panel"],
        bank_checksums_sha256=digest(Path(root) / "checksums.json"),
        structure_group=task["structure_group"],
        evidence_role=task["evidence_role"],
        status="scored",
        unit=task["unit"],
        prediction_sha256=hashlib.sha256(Path(prediction_file).read_bytes()).hexdigest(),
        **metrics(test, predictions, train),
    )


def recover(root, task_id, kind, expression):
    task, test = partition(root, task_id, kind)
    if task["category"] != "expression_recovery":
        raise ValueError("Real observables have no asserted exact expression")
    _, train = partition(root, task_id, kind, "train")
    n = [r["N"] for r in test]
    z = [r["Z"] for r in test]
    predicted = evaluate(expression, n, z)
    result = metrics(test, dict(zip((r["sample_id"] for r in test), predicted)), train)
    reference = task["formula"]["expression"]
    # Independent domain witnesses, including both parities and source-specific closures.
    from .formulas import in_domain

    ns = sorted(
        set(range(8, 161, 3)) | {m + d for m in (8, 20, 28, 50, 82, 126) for d in (-1, 0, 1)}
    )
    zs = sorted(set(range(8, 101, 3)) | {m + d for m in (8, 20, 28, 50, 82) for d in (-1, 0, 1)})
    pairs = [(n, z) for n in ns for z in zs if in_domain(task["formula"]["domain"], n, z)]
    wn, wz = zip(*pairs)
    actual = evaluate(expression, wn, wz)
    expected = evaluate(reference, wn, wz)
    scale = max(float(np.std([r["y"] for r in train])), 1e-12)
    test_equal = bool(np.allclose(predicted, [r["y"] for r in test], rtol=1e-8, atol=1e-8 * scale))
    witness_equal = bool(np.allclose(actual, expected, rtol=1e-8, atol=1e-8 * scale))
    return dict(
        task=task_id,
        split=kind,
        panel=task["panel"],
        bank_checksums_sha256=digest(Path(root) / "checksums.json"),
        structure_group=task["structure_group"],
        evidence_role=task["evidence_role"],
        status="scored",
        unit=task["unit"],
        expression=expression,
        symbolic_status=prove(expression, reference),
        numeric_agreement=test_equal and witness_equal,
        numeric_tolerance={"rtol": 1e-8, "atol": 1e-8 * scale},
        witness_count=len(pairs),
        expression_complexity=complexity(expression),
        reference_complexity=complexity(reference),
        **result,
    )
