"""Offline operations by default. Only fetch contacts the upstream data servers."""

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

from .bank import build, load_bank, validate
from .expressions import EXTRA_FEATURES, evaluate
from .scoring import partition, recover, score
from .sources import digest, fetch


def export(args):
    task, rows = partition(args.root, args.task, args.split, args.partition)
    _, train = partition(args.root, args.task, args.split, "train")
    if args.noise and task["category"] != "expression_recovery":
        raise ValueError("Synthetic label noise is only defined for formula recovery")
    scale = float(np.std([r["y"] for r in train]))
    columns = ["sample_id", "N", "Z"]
    if args.features == "nuclear":
        columns += ["A", "I", "d", "P_s", "P_m", *EXTRA_FEATURES]
    include = args.partition != "test" or args.include_target
    if include:
        columns += ["y", "weight"]
    writer = csv.DictWriter(sys.stdout, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    features = (
        {
            name: evaluate(name, [r["N"] for r in rows], [r["Z"] for r in rows])
            for name in ("A", "I", "d", "P_s", "P_m", *EXTRA_FEATURES)
        }
        if args.features == "nuclear"
        else {}
    )
    for index, row in enumerate(rows):
        out = {k: row[k] for k in ("sample_id", "N", "Z")}
        if args.features == "nuclear":
            for feature in ("A", "I", "d", "P_s", "P_m", *EXTRA_FEATURES):
                out[feature] = float(features[feature][index])
        if include:
            y = row["y"]
            if args.partition == "train" and args.noise:
                seed = int(
                    hashlib.sha256(
                        (args.task + ":" + row["sample_id"] + ":noise101").encode()
                    ).hexdigest()[:16],
                    16,
                )
                # Explicit Box-Muller rather than version-dependent generator internals.
                u = (seed + 1) / (2**64 + 1)
                v = (int(hashlib.sha256(str(seed).encode()).hexdigest()[:16], 16) + 1) / (2**64 + 1)
                y += args.noise * scale * math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)
            out.update(y=y, weight=1.0)
        writer.writerow(out)


def main():
    parser = argparse.ArgumentParser(description="Frozen nuclear-structure question bank")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("list", "summary", "validate", "export", "score", "recover"):
        command = commands.add_parser(name)
        command.add_argument("--root", type=Path, default=Path("."))
        if name in ("export", "score", "recover"):
            command.add_argument("--task", required=True)
            command.add_argument("--split", default="iid101")
        if name == "list":
            command.add_argument("--panel", default=None)
        if name == "export":
            command.add_argument(
                "--partition", choices=("train", "validation", "test"), default="train"
            )
            command.add_argument("--features", choices=("raw", "nuclear"), default="raw")
            command.add_argument("--include-target", action="store_true")
            command.add_argument("--noise", type=float, choices=(0, 0.01, 0.05), default=0)
        if name == "score":
            command.add_argument("--predictions", type=Path, required=True)
        if name == "recover":
            command.add_argument("--expression", required=True)
    command = commands.add_parser("fetch")
    command.add_argument("--raw", type=Path, default=Path(".cache/raw"))
    command.add_argument("--snapshots", type=Path, default=Path("source_snapshots"))
    command = commands.add_parser("build")
    command.add_argument("--raw", type=Path, required=True)
    command.add_argument("--output", type=Path, required=True)
    command = commands.add_parser("aggregate")
    command.add_argument("--root", type=Path, default=Path("."))
    command.add_argument("--results", type=Path, required=True)
    command.add_argument("--panel", required=True)
    command.add_argument("--split", required=True)
    command.add_argument("--models", nargs="+", required=True)
    command.add_argument("--noise", type=float, default=0)
    args = parser.parse_args()
    try:
        if args.command == "fetch":
            fetch(args.raw, args.snapshots)
            result = {"status": "sources_verified"}
        elif args.command == "build":
            result = build(args.raw, args.output)
        elif args.command == "validate":
            result = validate(args.root)
        elif args.command == "aggregate":
            from .aggregation import aggregate

            validate(args.root)
            result = aggregate(
                load_bank(args.root),
                json.loads(args.results.read_text()),
                args.panel,
                args.split,
                args.models,
                args.noise,
                expected_digest=digest(args.root / "checksums.json"),
            )
        elif args.command == "summary":
            from .coverage import summary

            result = summary(load_bank(args.root))
        elif args.command == "list":
            result = [
                {
                    k: t[k]
                    for k in (
                        "id",
                        "category",
                        "panel",
                        "structure_group",
                        "evidence_role",
                        "observable",
                        "unit",
                        "rows",
                        "enabled_splits",
                    )
                }
                for t in load_bank(args.root)["tasks"]
                if args.panel is None or t["panel"] == args.panel
            ]
        elif args.command == "export":
            validate(args.root)
            export(args)
            return
        elif args.command == "score":
            validate(args.root)
            result = score(args.root, args.task, args.split, args.predictions)
        else:
            validate(args.root)
            result = recover(args.root, args.task, args.split, args.expression)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        FloatingPointError,
        OverflowError,
        ZeroDivisionError,
        RecursionError,
        SyntaxError,
    ) as error:
        print(json.dumps({"status": "failed", "error": str(error)}), file=sys.stderr)
        raise SystemExit(2) from error
