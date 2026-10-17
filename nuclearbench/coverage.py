"""Counts reveal parameter/state repetition instead of treating it as novelty."""

from collections import Counter, defaultdict


def summary(bank):
    panels = defaultdict(list)
    for task in bank["tasks"]:
        panels[task["panel"]].append(task)
    return {
        "version": bank["version"],
        "task_instances": len(bank["tasks"]),
        "task_rows": sum(t["rows"] for t in bank["tasks"]),
        "enabled_task_split_pairs": sum(len(t["enabled_splits"]) for t in bank["tasks"]),
        "panels": {
            panel: {
                "task_instances": len(tasks),
                "declared_structure_groups": dict(
                    sorted(Counter(t["structure_group"] for t in tasks).items())
                ),
                "evidence_roles": dict(Counter(t["evidence_role"] for t in tasks)),
            }
            for panel, tasks in sorted(panels.items())
        },
        "interpretation": "Instances and declared groups are not a statistical proof of independent mechanisms; never count splits/seeds as new questions",
    }
