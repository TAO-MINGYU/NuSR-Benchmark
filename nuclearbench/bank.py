"""Portable frozen artifacts, deterministic source rebuilds, and integrity checks."""

import csv
import json
import math
import shutil
from pathlib import Path

import numpy as np

from .controls import control_formulas
from .data import STATES, load_observables, read_masses, state_name
from .expanded_formulas import published_formulas
from .expressions import evaluate
from .formulas import MACROS, in_domain
from .literature import LITERATURE
from .sources import SOURCES, digest, verify_raw
from .splits import SPLITS, make_split, validate_split
from .temporal import (
    TEMPORAL_OBSERVABLES,
    TEMPORAL_SPLIT,
    make_temporal_split,
    temporal_rows,
    validate_temporal_vintages,
)

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
    "E_control": "MeV",
    "B_macro": "MeV",
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
for _j, _p in STATES:
    UNITS[state_name(_j, _p)] = "MeV"
    FAMILIES[state_name(_j, _p)] = "shape_coexistence" if _j == 0 else "spectroscopy"

MODEL_ANCHORED_RADIUS_Z = {75, 84, 86, 87, 88, 96}
MIN_NEW_OBSERVATIONS = 30


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
    coverage = []

    def add(task_id, category, observable, rows, family, formula=None, temporal=False):
        if not rows:
            raise ValueError(f"Empty dataset: {task_id}")
        data = f"data/{task_id}.csv"
        splits = f"splits/{task_id}.json"
        write_rows(output / data, rows)
        partition = (
            {TEMPORAL_SPLIT: make_temporal_split(rows)}
            if temporal
            else {kind: make_split(rows, kind) for kind in SPLITS}
        )
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
                "source_population": len(tables.get(observable, tables["B"])),
                "observed_context_rows": sum(r["observed_y"] is not None for r in rows),
                "panel": formula["recovery_kind"]
                if formula
                else ("historical_new_measurements" if temporal else "evaluated_observables"),
                "structure_group": formula["structure_group"] if formula else family,
                "evidence_role": formula["evidence_role"] if formula else "evaluation",
                "split_families": list(partition),
                "enabled_splits": [k for k in partition if partition[k]["status"] == "enabled"],
            }
        )

    for formula in [*published_formulas(), *control_formulas()]:
        rows = []
        synthetic = formula["recovery_kind"] == "synthetic_mechanism_control"
        coordinate_table = (
            tables["B"]
            if synthetic
            or formula["domain"] == "spectroscopy"
            or formula["recovery_kind"] == "published_analytic_reference"
            else tables[formula["observable"]]
        )
        for (n, z), coordinate in sorted(coordinate_table.items()):
            if not in_domain(formula["domain"], n, z):
                continue
            observed = (
                None
                if synthetic or formula["recovery_kind"] == "published_analytic_reference"
                else tables[formula["observable"]].get((n, z))
            )
            row = dict(observed or coordinate)
            row.update(
                observed_y=None if observed is None else observed["y"],
                observed_sigma=None if observed is None else observed["sigma"],
                observed_dependencies=[] if observed is None else observed["dependencies"],
                sigma=None,
                dependencies=[f"formula:{formula['id']}:{n}:{z}"],
            )
            row["note"] = (
                "Formula-generated label; missing observed context is not fabricated. Coordinate/observation locator follows. "
                + row["note"]
            )
            if synthetic:
                row["source"] = "NuclearBench-designed-control"
                row["source_record"] = formula["id"] + ":sha256-uniform-v1"
                row["note"] = "Synthetic diagnostic, not an empirical observation."
            elif formula["recovery_kind"] == "published_analytic_reference":
                row["observed_y"] = None
                row["observed_sigma"] = None
                row["observed_dependencies"] = []
                row["note"] = (
                    "Restricted analytic component; no experimental value for this component is asserted."
                )
            rows.append(row)
        values = evaluate(formula["expression"], [r["N"] for r in rows], [r["Z"] for r in rows])
        for row, value in zip(rows, values):
            row["y"] = float(value)
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
        excluded_anchors = 0
        if observable == "Rch":
            excluded_anchors = sum(r["Z"] in MODEL_ANCHORED_RADIUS_Z for r in rows)
            rows = [r for r in rows if r["Z"] not in MODEL_ANCHORED_RADIUS_Z]
        eligible_splits = [k for k in SPLITS if make_split(rows, k)["status"] == "enabled"]
        admitted = index <= 15 or (len(rows) >= MIN_NEW_OBSERVATIONS and len(eligible_splits) >= 2)
        coverage.append(
            {
                "observable": observable,
                "upstream_parsed": len(table),
                "domain_rows": len(rows),
                "model_anchored_radius_rows_excluded": excluded_anchors,
                "admitted": admitted,
                "reason": "legacy core retained"
                if index <= 15
                else (
                    "meets >=30 observations and >=2 usable splits"
                    if admitted
                    else "insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits"
                ),
                "enabled_splits": eligible_splits,
            }
        )
        if not admitted:
            continue
        add(
            f"B{index:02d}_{observable}",
            "observable_prediction",
            observable,
            rows,
            FAMILIES[observable],
        )
    old = read_masses(raw, "AME2016")
    for index, observable in enumerate(TEMPORAL_OBSERVABLES, 1):
        rows = temporal_rows(old[observable], tables[observable])
        validate_temporal_vintages(rows, old[observable], tables[observable])
        add(
            f"T{index:02d}_{observable}",
            "observable_prediction",
            observable,
            rows,
            FAMILIES[observable],
            temporal=True,
        )
    bank = {
        "schema_version": 2,
        "version": "2.0.0",
        "release_date": "2026-10-17",
        "tasks": tasks,
        "macros": MACROS,
        "model_seeds": [7, 17, 37, 73, 101],
        "noise_levels": [0, 0.01, 0.05],
        "split_seed": 101,
        "experimental_status": "retrospective_release_validation_not_blind",
        "source_policy": "Pinned evaluated values, no estimated mass parents, preliminary radii or censored point labels",
        "sources": {
            name: {
                "url": url,
                "sha256": sha,
                "snapshot_retrieved": "2026-10-17"
                if name in {"mass16.txt", "rct1-16.txt", "rct2-16.txt"}
                else "2026-10-01",
            }
            for name, (url, sha) in SOURCES.items()
        },
        "source_counts": {k: len(v) for k, v in tables.items()},
        "bundled_sources": bundled,
        "counting_policy": "Task instances, split conditions and seeds are not independent physics/structure families",
        "radius_primary_excluded_Z": sorted(MODEL_ANCHORED_RADIUS_Z),
    }
    write_json(output / "coverage.json", coverage)
    write_json(output / "literature.json", LITERATURE)
    write_json(output / "bank.json", bank)
    paths = [
        output / "bank.json",
        output / "coverage.json",
        output / "literature.json",
        *sorted((output / "data").glob("*.csv")),
        *sorted((output / "splits").glob("*.json")),
        *sorted((output / "source_snapshots").iterdir()),
    ]
    write_json(output / "checksums.json", {str(p.relative_to(output)): digest(p) for p in paths})
    return validate(output)


def validate(root):
    root = Path(root)
    bank = load_bank(root)
    if bank["schema_version"] != 2 or bank["version"] != "2.0.0":
        raise ValueError(
            "This verifier targets bank v2.0.0; use the v1.0.0 tag to validate the legacy bank"
        )
    checksums = json.loads((root / "checksums.json").read_text())
    expected = {"bank.json", "coverage.json", "literature.json"}
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
    registry = {
        f["id"]: json.loads(json.dumps(f)) for f in [*published_formulas(), *control_formulas()]
    }
    actual_recovery = {t["id"] for t in bank["tasks"] if t["category"] == "expression_recovery"}
    if actual_recovery != set(registry):
        raise ValueError("Missing or additional registered recovery tasks")
    if json.loads((root / "literature.json").read_text()) != json.loads(json.dumps(LITERATURE)):
        raise ValueError("Literature admission ledger differs from reviewed registry")
    old_mass = read_masses(root / "source_snapshots", "AME2016")
    new_mass = read_masses(root / "source_snapshots", "AME2020")
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
            if f != registry.get(task["id"]):
                raise ValueError(
                    f"Formula differs from source-audited/generator registry: {task['id']}"
                )
            if (task["panel"], task["structure_group"], task["evidence_role"]) != (
                f["recovery_kind"],
                f["structure_group"],
                f["evidence_role"],
            ):
                raise ValueError("Recovery panel/group/role metadata differs from registry")
            if task["observed_context_rows"] != sum(r["observed_y"] is not None for r in rows):
                raise ValueError("Incorrect observational context count")
            values = evaluate(f["expression"], [r["N"] for r in rows], [r["Z"] for r in rows])
            # libm implementations may differ at the last bit across platforms.
            if not np.allclose(values, [r["y"] for r in rows], rtol=2e-14, atol=2e-14):
                raise ValueError("Formula/label mismatch")
            if any(
                not in_domain(f["domain"], r["N"], r["Z"]) or r["sigma"] is not None for r in rows
            ):
                raise ValueError("Recovery domain/label ambiguity")
        temporal = task["panel"] == "historical_new_measurements"
        if temporal:
            validate_temporal_vintages(
                rows, old_mass[task["observable"]], new_mass[task["observable"]]
            )
        if task["id"] == "B10_Rch" and any(r["Z"] in MODEL_ANCHORED_RADIUS_Z for r in rows):
            raise ValueError("Model-anchored absolute radius admitted to primary prediction")
        expected_splits = [TEMPORAL_SPLIT] if temporal else list(SPLITS)
        if set(partitions) != set(expected_splits) or task["split_families"] != expected_splits:
            raise ValueError("Missing split family")
        for kind, split in partitions.items():
            validate_split(rows, split, kind)
            if split["status"] != "enabled":
                disabled.append(f"{task['id']}:{kind}")
        if task["enabled_splits"] != [
            k for k in expected_splits if partitions[k]["status"] == "enabled"
        ]:
            raise ValueError("Inconsistent enabled split list")
        totals[task["category"]] += 1
        row_count += len(rows)
    return {"status": "valid", "tasks": totals, "rows": row_count, "disabled_splits": disabled}
