"""Frozen partitions followed by primitive-dependency embargo (test has priority)."""

import hashlib
import math
from collections import defaultdict

SPLITS = ("iid101", "isotope101", "isotone101", "neutron_edge", "proton_edge", "shell_N", "shell_Z")
MAGIC = (8, 20, 28, 50, 82, 126)


def bucket(key):
    number = (
        int(hashlib.sha256(("nuclearbench-v1:101:" + str(key)).encode()).hexdigest()[:16], 16) % 100
    )
    return "train" if number < 60 else "validation" if number < 80 else "test"


def make_split(rows, kind):
    if kind not in SPLITS:
        raise ValueError(kind)
    parts = {p: [] for p in ("train", "validation", "test", "purged")}
    assigned = {}
    if kind in ("neutron_edge", "proton_edge"):
        chain, coordinate = ("Z", "N") if kind == "neutron_edge" else ("N", "Z")
        groups = defaultdict(list)
        for row in rows:
            groups[row[chain]].append(row)
        for group in groups.values():
            ordered = sorted(group, key=lambda r: r[coordinate])
            k = max(1, math.ceil(len(group) * 0.2)) if len(group) >= 8 else 0
            for index, row in enumerate(ordered):
                assigned[row["sample_id"]] = (
                    "test"
                    if k and index >= len(group) - k
                    else ("validation" if k and index >= len(group) - 2 * k else "train")
                )
    for row in sorted(rows, key=lambda r: r["sample_id"]):
        if kind == "iid101":
            partition = bucket(row["sample_id"])
        elif kind in ("isotope101", "isotone101"):
            partition = bucket(row["Z"] if kind == "isotope101" else row["N"])
        elif kind.startswith("shell_"):
            distance = min(abs(row[kind[-1]] - m) for m in MAGIC)
            partition = "test" if distance <= 2 else "validation" if distance <= 4 else "train"
        else:
            partition = assigned[row["sample_id"]]
        parts[partition].append(row)
    embargo(parts)
    return partition_result(parts)


def embargo(parts):
    protected = {d for r in parts["test"] for d in r["dependencies"]}
    for partition in ("validation", "train"):
        kept = []
        for row in parts[partition]:
            if protected.intersection(row["dependencies"]):
                parts["purged"].append(row)
            else:
                kept.append(row)
        parts[partition] = kept
        protected.update(d for row in kept for d in row["dependencies"])


def partition_result(parts):
    counts = {p: len(values) for p, values in parts.items()}
    enabled = all(counts[p] >= 3 for p in ("train", "validation", "test"))
    return {
        "status": "enabled" if enabled else "insufficient_coverage",
        "reason": None
        if enabled
        else "Fewer than three retained rows in at least one partition; not scored",
        "counts": counts,
        "partitions": {p: sorted(r["sample_id"] for r in values) for p, values in parts.items()},
    }


def validate_split(rows, split, kind):
    if kind == "ame2016_to_2020":
        from .temporal import make_temporal_split

        expected = make_temporal_split(rows)
    else:
        expected = make_split(rows, kind)
    if split != expected:
        raise ValueError(f"Split differs from registered algorithm: {kind}")
    by_id = {r["sample_id"]: r for r in rows}
    seen = set()
    dependencies = []
    for part in ("test", "validation", "train", "purged"):
        ids = split["partitions"][part]
        if seen.intersection(ids) or len(ids) != len(set(ids)):
            raise ValueError("Duplicate/cross-partition sample ID")
        seen.update(ids)
        if part != "purged":
            deps = {d for sid in ids for d in by_id[sid]["dependencies"]}
            if any(deps.intersection(previous) for previous in dependencies):
                raise ValueError("Primitive label dependency leakage")
            dependencies.append(deps)
    if seen != set(by_id):
        raise ValueError("Incomplete partition coverage")
