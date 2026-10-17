"""Equal-group summaries with explicit completeness and failed-run accounting."""

import math
from collections import defaultdict
from statistics import mean


def aggregate(bank, runs, panel, split, models, noise=0, expected_digest=None):
    tasks = [
        t
        for t in bank["tasks"]
        if t["panel"] == panel
        and split in t["enabled_splits"]
        and t["evidence_role"] != "development"
    ]
    if not tasks or not models or len(set(models)) != len(models):
        raise ValueError("Choose a nonempty panel/split and unique model list")
    if noise not in bank["noise_levels"] or (
        noise and tasks[0]["category"] != "expression_recovery"
    ):
        raise ValueError("Invalid noise condition")
    expected = {(t["id"], seed) for t in tasks for seed in bank["model_seeds"]}
    selected = {model: {} for model in models}
    all_tasks = {t["id"]: t for t in bank["tasks"]}
    for run in runs:
        if (
            run.get("model") not in selected
            or run.get("split") != split
            or run.get("noise", 0) != noise
        ):
            continue
        key = (run.get("task"), run.get("seed"))
        if run.get("task") in all_tasks:
            spec = all_tasks[run["task"]]
            if (
                spec["panel"] != panel
                or spec["evidence_role"] == "development"
                or split not in spec["enabled_splits"]
            ):
                continue
        if expected_digest is not None and run.get("bank_checksums_sha256") != expected_digest:
            raise ValueError("Run belongs to a different or unspecified frozen bank")
        if key not in expected:
            raise ValueError("Unexpected task/seed in requested aggregation panel")
        if key in selected[run["model"]]:
            raise ValueError("Duplicate run; best-retry selection is forbidden")
        if run.get("status") not in {"scored", "failed", "timeout", "unsupported"}:
            raise ValueError("Unknown terminal status")
        if run["status"] == "scored":
            error = run.get("nrmse_train_std")
            if (
                error is None
                or not isinstance(error, (int, float))
                or not math.isfinite(error)
                or error < 0
            ):
                raise ValueError("A scored run needs finite nonnegative normalized error")
            if tasks[0]["category"] == "expression_recovery" and (
                run.get("symbolic_status")
                not in {"proved_equal", "unproved", "unproved_timeout", "unproved_error"}
                or type(run.get("numeric_agreement")) is not bool
            ):
                raise ValueError(
                    "Recovery summaries require both proof status and numerical agreement"
                )
        selected[run["model"]][key] = run
    result = {}
    for model, available in selected.items():
        missing = sorted(expected - set(available))
        groups = defaultdict(list)
        for task in tasks:
            rows = [available.get((task["id"], seed)) for seed in bank["model_seeds"]]
            complete = all(r is not None for r in rows)
            all_scored = complete and all(r["status"] == "scored" for r in rows)
            item = {
                "task": task["id"],
                "complete": complete,
                "normalized_error": mean(r["nrmse_train_std"] for r in rows)
                if all_scored
                else None,
                # Failed terminal runs remain in the denominator. Missing runs prevent a final summary.
                "symbolic_recovery": mean(
                    bool(
                        r and r["status"] == "scored" and r.get("symbolic_status") == "proved_equal"
                    )
                    for r in rows
                )
                if complete
                else None,
                "numerical_agreement": mean(
                    bool(r and r["status"] == "scored" and r.get("numeric_agreement")) for r in rows
                )
                if complete
                else None,
            }
            groups[task["structure_group"]].append(item)
        summaries = {}
        for name, items in sorted(groups.items()):
            summaries[name] = {"task_instances": len(items), "tasks": items}
            for metric in ("normalized_error", "symbolic_recovery", "numerical_agreement"):
                values = [t[metric] for t in items]
                summaries[name][metric] = (
                    mean(values) if all(v is not None for v in values) else None
                )
        totals = {}
        for metric in ("normalized_error", "symbolic_recovery", "numerical_agreement"):
            values = [s[metric] for s in summaries.values()]
            totals[metric] = mean(values) if all(v is not None for v in values) else None
        if tasks[0]["category"] != "expression_recovery":
            for container in [totals, *summaries.values()]:
                container.pop("symbolic_recovery", None)
                container.pop("numerical_agreement", None)
            for items in groups.values():
                for item in items:
                    item.pop("symbolic_recovery", None)
                    item.pop("numerical_agreement", None)
        result[model] = {
            "expected_runs": len(expected),
            "observed_runs": len(available),
            "missing_runs": [{"task": t, "seed": s} for t, s in missing],
            "terminal_failures": sum(r["status"] != "scored" for r in available.values()),
            "complete": not missing,
            "groups": summaries,
            "equal_group_summary": totals,
        }
    return {
        "panel": panel,
        "split": split,
        "noise": noise,
        "models": result,
        "weighting": "equal seeds within task, equal tasks within declared group, equal groups within panel; no raw mixed-unit RMSE average",
        "interpretation": "Incomplete groups have no final aggregate; normalized error is unavailable when any terminal run lacks a valid prediction",
    }
