"""Render the full inventory and coverage tables directly from frozen artifacts."""

import json
from pathlib import Path

from .bank import load_bank
from .coverage import summary


def render(root):
    root = Path(root)
    bank = load_bank(root)
    counts = summary(bank)
    lines = [
        "# Task inventory — v2.0.0",
        "",
        "Two evaluation categories: expression recovery and observable prediction. Published formulas, restricted analytic references and designed controls are separate panels within recovery. Counts below are task instances, not independent physical laws.",
        "",
        f"Total: **{counts['task_instances']} task instances**, {counts['task_rows']:,} task rows, {counts['enabled_task_split_pairs']} enabled task/split pairs.",
        "",
        "Recovery labels are generated values. `observed_y` is optional experimental context and is never a fitting input. Common-coordinate spectroscopy cards do not fabricate missing level measurements. Restricted macroscopic components and synthetic controls assert no experimental value for their generated target.",
        "",
    ]
    for panel in counts["panels"]:
        tasks = [t for t in bank["tasks"] if t["panel"] == panel]
        lines += [
            f"## {panel}",
            "",
            "| ID | Target / unit | Rows | Observed context | Structure group | Role | Enabled splits | Files |",
            "| --- | --- | ---: | ---: | --- | --- | ---: | --- |",
        ]
        for t in tasks:
            lines.append(
                f"| {t['id']} | {t['observable']} / {t['unit']} | {t['rows']} | {t['observed_context_rows']} | {t['structure_group']} | {t['evidence_role']} | {len(t['enabled_splits'])} | [CSV]({t['data']}) / [IDs]({t['splits']}) |"
            )
        lines += [""]
    lines += [
        "Full expressions, domains, printed coefficients, sources and scope restrictions are in each task's `formula` entry in [bank.json](bank.json). See [FORMULAS.md](FORMULAS.md), [CONTROL_DESIGN.md](CONTROL_DESIGN.md), [TEMPORAL_PROTOCOL.md](TEMPORAL_PROTOCOL.md) and [SPLIT_COUNTS.md](SPLIT_COUNTS.md).",
        "",
        "B identifiers retain candidate ordinals: gaps reflect rejected sparse states, not missing files. All rejections and their coverage are listed in [COVERAGE.md](COVERAGE.md). v1.0.0 remains available at its immutable Git tag.",
    ]
    files = {"TASKS.md": "\n".join(lines).rstrip() + "\n"}
    lines = [
        "# Coverage audit — v2.0.0",
        "",
        "## Instance counts and declared grouping",
        "",
        "Declared groups organize reports; they do not certify statistical independence. Different coefficients, spin states, splits, noise levels or random seeds must not be counted as new structure families.",
        "",
    ]
    for panel, p in counts["panels"].items():
        lines += [
            f"### {panel}: {p['task_instances']} instances",
            "",
            "| Declared group | Instances |",
            "| --- | ---: |",
        ]
        lines += [
            f"| {group} | {number} |" for group, number in p["declared_structure_groups"].items()
        ]
        lines += [""]
    lines += [
        "## Evaluated-observable admission",
        "",
        "Original 15 core targets are retained with the radius-anchor correction. New observed targets require at least 30 conservative N/Z-domain rows and two enabled split families. The rule was fixed before any model campaign; sparse/ambiguous states are not rescued by relaxing their label definition.",
        "",
        "| Target | Parsed source rows | Domain rows after exclusions | Admitted | Enabled splits | Reason |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ]
    for c in json.loads((root / "coverage.json").read_text()):
        lines.append(
            f"| {c['observable']} | {c['upstream_parsed']} | {c['domain_rows']} | {c['admitted']} | {len(c['enabled_splits'])} | {c['reason']} |"
        )
    lines += [
        "",
        "The absolute-radius panel excludes 72 domain rows with Z=75,84,86,87,88,96 because of model-based reference anchors identified in the source discussion. Remaining radii are evaluated quantities with shared calibration/correlation, not independent raw measurements.",
        "",
        "## Literature decisions",
        "",
        "| Source ID | Decision | Locator / role | Caveat |",
        "| --- | --- | --- | --- |",
    ]
    for item in json.loads((root / "literature.json").read_text()):
        lines.append(
            f"| [{item['id']}]({item['source']}) | {item['decision']} | {item.get('locators', '')} {item['role']} | {item['caveat']} |"
        )
    lines += [
        "",
        "This is an audited selection, not an exhaustive literature review or a guarantee of manuscript acceptance. Source PDF hashes, where recorded, identify reviewed originals; complete articles are not redistributed.",
    ]
    files["COVERAGE.md"] = "\n".join(lines).rstrip() + "\n"
    kinds = [
        "iid101",
        "isotope101",
        "isotone101",
        "neutron_edge",
        "proton_edge",
        "shell_N",
        "shell_Z",
        "ame2016_to_2020",
    ]
    lines = [
        "# Retained partition counts",
        "",
        "Each cell is train/validation/test after primitive embargo. `*` means insufficient coverage and disabled scoring; `—` means a split is not part of the task. Every purge list and count is preserved in its JSON. Small nonzero partitions are not a guarantee of strong statistical power.",
        "",
        "| Task | " + " | ".join(kinds) + " |",
        "| --- | " + " | ".join("---" for _ in kinds) + " |",
    ]
    for t in bank["tasks"]:
        masks = json.loads((root / t["splits"]).read_text())
        cells = []
        for kind in kinds:
            if kind not in masks:
                cells.append("—")
                continue
            s = masks[kind]
            cells.append(
                "/".join(str(s["counts"][part]) for part in ("train", "validation", "test"))
                + ("*" if s["status"] != "enabled" else "")
            )
        lines.append("| " + t["id"] + " | " + " | ".join(cells) + " |")
    files["SPLIT_COUNTS.md"] = "\n".join(lines).rstrip() + "\n"
    return files


def write_docs(root):
    for name, text in render(root).items():
        (Path(root) / name).write_text(text)
