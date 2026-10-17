"""Portable frozen artifacts, deterministic source rebuilds, and integrity checks."""

import csv
import json
import math
import shutil
from pathlib import Path

import numpy as np

from .data import load_observables
from .expressions import evaluate
from .formulas import FORMULAS, MACROS, in_domain
from .sources import SOURCES, digest, verify_raw
from .splits import SPLITS, make_split, validate_split

FIELDS = (
    "sample_id",
    "N",
    "Z",
    "A",
    "y",
    "sigma",
    "observed_y",
    "observed_sigma",
    "source",
    "source_record",
    "dependencies",
    "observed_dependencies",
    "note",
)
JSON_FIELDS = {"dependencies", "observed_dependencies"}
UNITS = {
    "B": "MeV",
    "Sn": "MeV",
    "S2n": "MeV",
    "Sp": "MeV",
    "S2p": "MeV",
    "OES3n": "MeV",
    "OES3p": "MeV",
    "delta2n": "MeV",
    "delta2p": "MeV",
    "Rch": "fm",
    "E2plus": "MeV",
    "E4plus": "MeV",
    "E3minus": "MeV",
    "R42": "1",
    "BE2": "e^2 fm^4",
}
FAMILIES = {
    "B": "mass",
    "Sn": "mass_difference",
    "S2n": "mass_difference",
    "Sp": "mass_difference",
    "S2p": "mass_difference",
    "OES3n": "pairing",
    "OES3p": "pairing",
    "delta2n": "shell_gap",
    "delta2p": "shell_gap",
    "Rch": "radius",
    "E2plus": "spectroscopy",
    "E4plus": "spectroscopy",
    "E3minus": "spectroscopy",
    "R42": "collectivity",
    "BE2": "collectivity",
}


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
    )


def read_rows(path):
    with Path(path).open(newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError(f"Unexpected CSV schema: {path}")
        rows = list(reader)
    for row in rows:
        for name in ("N", "Z", "A"):
            row[name] = int(row[name])
        for name in ("y", "sigma", "observed_y", "observed_sigma"):
            row[name] = None if row[name] == "" else float(row[name])
        for name in JSON_FIELDS:
            row[name] = json.loads(row[name])
    return rows


def write_rows(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in sorted(rows, key=lambda r: (r["N"], r["Z"])):
            writer.writerow(
                {
                    k: json.dumps(row[k], separators=(",", ":")) if k in JSON_FIELDS else row[k]
                    for k in FIELDS
                }
            )


def load_bank(root):
    return json.loads((Path(root) / "bank.json").read_text())


def get_task(root, task_id):
    bank = load_bank(root)
    matches = [t for t in bank["tasks"] if t["id"] == task_id]
    if len(matches) != 1:
        raise ValueError(f"Unknown task: {task_id}")
    task = matches[0]
    return (
        task,
        read_rows(Path(root) / task["data"]),
        json.loads((Path(root) / task["splits"]).read_text()),
    )


def build(raw, output):
    verify_raw(raw)
    output = Path(output)
    if (output / "bank.json").exists():
        raise ValueError("Build into a fresh directory; never overwrite a frozen release")
    tables = load_observables(raw)
    bundled = [name for name in SOURCES if not name.endswith(".zip")]
    (output / "source_snapshots").mkdir(parents=True, exist_ok=True)
    for name in bundled:
        shutil.copyfile(Path(raw) / name, output / "source_snapshots" / name)
    tasks = []

    def add(task_id, category, observable, rows, family, formula=None):
        if not rows:
            raise ValueError(f"Empty dataset: {task_id}")
        data = f"data/{task_id}.csv"
        splits = f"splits/{task_id}.json"
        write_rows(output / data, rows)
        partition = {kind: make_split(rows, kind) for kind in SPLITS}
        write_json(output / splits, partition)
        tasks.append(
            {
                "id": task_id,
                "category": category,
                "observable": observable,
                "unit": UNITS[observable],
                "family": family,
                "rows": len(rows),
                "data": data,
                "splits": splits,
                "formula": formula,
                "source_population": len(tables[observable]),
                "enabled_splits": [k for k in SPLITS if partition[k]["status"] == "enabled"],
            }
        )

    for formula in FORMULAS:
        rows = []
        for (n, z), observed in sorted(tables[formula["observable"]].items()):
            if not in_domain(formula["domain"], n, z):
                continue
            row = dict(observed)
            row.update(
                observed_y=row["y"],
                observed_sigma=row["sigma"],
                observed_dependencies=row["dependencies"],
                sigma=None,
                dependencies=[f"formula:{formula['id']}:{n}:{z}"],
            )
            row["y"] = float(evaluate(formula["expression"], [n], [z])[0])
            row["note"] = (
                "Formula-generated label; observational columns are never fitting inputs. "
                + row["note"]
            )
            rows.append(row)
        add(
            formula["id"],
            "expression_recovery",
            formula["observable"],
            rows,
            formula["family"],
            formula,
        )
    for index, (observable, table) in enumerate(tables.items(), 1):
        rows = [dict(row) for (n, z), row in sorted(table.items()) if n >= 8 and z >= 8]
        add(
            f"B{index:02d}_{observable}",
            "observable_prediction",
            observable,
            rows,
            FAMILIES[observable],
        )
    bank = {
        "schema_version": 1,
        "version": "1.0.0",
        "release_date": "2026-10-17",
        "tasks": tasks,
        "macros": MACROS,
        "model_seeds": [7, 17, 37, 73, 101],
        "noise_levels": [0, 0.01, 0.05],
        "split_seed": 101,
        "experimental_status": "retrospective_release_validation_not_blind",
        "source_policy": "Pinned evaluated values, no estimated mass parents, preliminary radii or censored point labels",
        "sources": {
            name: {"url": url, "sha256": sha, "snapshot_retrieved": "2026-10-01"}
            for name, (url, sha) in SOURCES.items()
        },
        "source_counts": {k: len(v) for k, v in tables.items()},
        "bundled_sources": bundled,
    }
    write_json(output / "bank.json", bank)
    paths = [
        output / "bank.json",
        *sorted((output / "data").glob("*.csv")),
        *sorted((output / "splits").glob("*.json")),
        *sorted((output / "source_snapshots").iterdir()),
    ]
    write_json(output / "checksums.json", {str(p.relative_to(output)): digest(p) for p in paths})
    return validate(output)


def validate(root):
    root = Path(root)
    bank = load_bank(root)
    checksums = json.loads((root / "checksums.json").read_text())
    expected = {"bank.json"}
    expected.update("source_snapshots/" + name for name in bank["bundled_sources"])
    for name in bank["bundled_sources"]:
        if digest(root / "source_snapshots" / name) != bank["sources"][name]["sha256"]:
            raise ValueError(f"Source hash mismatch: {name}")
    for task in bank["tasks"]:
        expected.update((task["data"], task["splits"]))
    if set(checksums) != expected:
        raise ValueError("Incomplete checksum inventory")
    for path, sha in checksums.items():
        if not (root / path).resolve().is_relative_to(root.resolve()) or digest(root / path) != sha:
            raise ValueError(f"Artifact hash mismatch: {path}")
    if len({t["id"] for t in bank["tasks"]}) != len(bank["tasks"]):
        raise ValueError("Duplicate task ID")
    totals = {"expression_recovery": 0, "observable_prediction": 0}
    row_count = 0
    disabled = []
    for task in bank["tasks"]:
        _, rows, partitions = get_task(root, task["id"])
        if len(rows) != task["rows"] or len({r["sample_id"] for r in rows}) != len(rows):
            raise ValueError(f"Row count or unique ID mismatch: {task['id']}")
        for row in rows:
            if row["A"] != row["N"] + row["Z"] or min(row["N"], row["Z"]) < 8:
                raise ValueError("Invalid nuclear coordinates")
            if row["sample_id"] != f"N{row['N']:03d}Z{row['Z']:03d}" or not row["dependencies"]:
                raise ValueError("Invalid sample ID/dependency manifest")
            for key in ("y", "sigma", "observed_y", "observed_sigma"):
                if row[key] is not None and (
                    not math.isfinite(row[key]) or ("sigma" in key and row[key] < 0)
                ):
                    raise ValueError("Invalid label/uncertainty")
            if not row["source"] or not row["source_record"]:
                raise ValueError("Missing provenance")
        if task["category"] == "expression_recovery":
            f = task["formula"]
            values = evaluate(f["expression"], [r["N"] for r in rows], [r["Z"] for r in rows])
            # libm implementations may differ at the last bit across platforms.
            if not np.allclose(values, [r["y"] for r in rows], rtol=2e-14, atol=2e-14):
                raise ValueError("Formula/label mismatch")
            if any(
                not in_domain(f["domain"], r["N"], r["Z"])
                or r["observed_y"] is None
                or r["sigma"] is not None
                for r in rows
            ):
                raise ValueError("Recovery domain/label ambiguity")
        if set(partitions) != set(SPLITS):
            raise ValueError("Missing split family")
        for kind, split in partitions.items():
            validate_split(rows, split, kind)
            if split["status"] != "enabled":
                disabled.append(f"{task['id']}:{kind}")
        if task["enabled_splits"] != [k for k in SPLITS if partitions[k]["status"] == "enabled"]:
            raise ValueError("Inconsistent enabled split list")
        totals[task["category"]] += 1
        row_count += len(rows)
    return {"status": "valid", "tasks": totals, "rows": row_count, "disabled_splits": disabled}
