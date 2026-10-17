"""Actual label-vintage holdouts, with observation IDs shared across evaluations."""

from .splits import bucket, embargo, partition_result

TEMPORAL_SPLIT = "ame2016_to_2020"
TEMPORAL_OBSERVABLES = ("B", "S2n", "S2p", "Sn", "Sp", "OES3n", "OES3p", "delta2n", "delta2p")


def neutral_dependency(value):
    parts = value.split(":")
    if len(parts) != 4 or parts[0] not in {"AME2016", "AME2020"} or parts[1] != "ME":
        raise ValueError("Temporal mass label has an unexpected primitive parent")
    return "nuclide_mass:" + ":".join(parts[-2:])


def temporal_rows(old, new):
    rows = []
    for key in sorted(set(old) | set(new)):
        n, z = key
        if n < 8 or z < 8:
            continue
        # Old measurements keep their OLD labels, even if AME2020 revised them.
        source = old[key] if key in old else new[key]
        row = dict(source)
        row["dependencies"] = [neutral_dependency(d) for d in row["dependencies"]]
        row["note"] = (
            "Historical label vintage retained; version-independent primitive embargo. "
            + row["note"]
        )
        rows.append(row)
    return rows


def make_temporal_split(rows):
    parts = {p: [] for p in ("train", "validation", "test", "purged")}
    for row in sorted(rows, key=lambda r: r["sample_id"]):
        vintage = row["source"].split("-")[0]
        if vintage == "AME2020":
            part = "test"
        elif vintage == "AME2016":
            part = "validation" if bucket(row["sample_id"]) == "validation" else "train"
        else:
            raise ValueError("Temporal panel requires explicit AME vintage labels")
        parts[part].append(row)
    embargo(parts)
    return partition_result(parts)


def validate_temporal_vintages(rows, old, new):
    expected = temporal_rows(old, new)
    if rows != sorted(expected, key=lambda r: (r["N"], r["Z"])):
        raise ValueError("Temporal labels or membership differ from original source vintages")
