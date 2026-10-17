"""Independent primary-source readers for the 0.2.0 observational expansion.

Do not import NuSR bundles or Target's processed labels. Source locators refer
to frozen original rows; qualifications and model status remain explicit.
"""

import csv
import math
import re
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from .data import ELEMENTS, insert, number, record

MOMENT = re.compile(r"([+-]?(?:\d+(?:\.\d*)?|\.\d+))(?:\((\d+)\))?\Z")
SPIN = re.compile(r"\d+(?:/\d+)?[+-]\Z")
YEAR_SECONDS = 365.25 * 86400
TIME_UNITS = {
    "ys": 1e-24,
    "zs": 1e-21,
    "as": 1e-18,
    "fs": 1e-15,
    "ps": 1e-12,
    "ns": 1e-9,
    "us": 1e-6,
    "ms": 1e-3,
    "s": 1.0,
    "m": 60.0,
    "h": 3600.0,
    "d": 86400.0,
    "y": YEAR_SECONDS,
    "ky": YEAR_SECONDS * 1e3,
    "My": YEAR_SECONDS * 1e6,
    "Gy": YEAR_SECONDS * 1e9,
    "Ty": YEAR_SECONDS * 1e12,
    "Py": YEAR_SECONDS * 1e15,
    "Ey": YEAR_SECONDS * 1e18,
    "Zy": YEAR_SECONDS * 1e21,
    "Yy": YEAR_SECONDS * 1e24,
}
DECAY_MODES = {
    "A": "logT_alpha",
    "B-": "logT_beta_minus",
    "B+": "logT_beta_plus_EC",
    "EC": "logT_EC",
    "SF": "logT_SF",
    "p": "logT_proton",
    "2p": "logT_two_proton",
}


def moment_value(text):
    """Keep unambiguous signs and digit uncertainties; never repair malformed data."""
    text = text.strip().replace("−", "-")
    text = re.sub(r"^([+-])\s+", r"\1", text)
    match = MOMENT.fullmatch(text)
    if not match:
        return None
    value = float(match[1])
    sigma = None
    if match[2] is not None:
        sigma = float(Decimal(int(match[2])) * Decimal(10) ** Decimal(match[1]).as_tuple().exponent)
    return value, sigma


def read_moments(raw):
    result, audit = {}, {}
    for filename, target, report, scale, heading in (
        ("magn_mom_recomm.csv", "mu_gs", "indc-nds-0915", 1.0, "magnetic dipole [nm]"),
        ("elec_mom_recomm.csv", "Q_gs", "indc-nds-0833", 100.0, "electric quadrupole [b]"),
    ):
        stats, candidates = Counter(), defaultdict(list)
        with (Path(raw) / filename).open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.reader(stream)
            header = next(reader)
            if len(header) != 12 or header[6] != heading or header[1] != "n.n+n.z":
                raise ValueError("Unexpected IAEA moment CSV layout")
            for index, fields in enumerate(reader, 2):
                stats["source_rows"] += 1
                if len(fields) != 12:
                    stats["malformed_columns"] += 1
                    continue
                # Despite its unusual header, column 2 is A, NOT N (e.g. 59Fe).
                try:
                    z, a = int(fields[0]), int(fields[1])
                except ValueError:
                    stats["malformed_identity"] += 1
                    continue
                n = a - z
                if z >= len(ELEMENTS) or z <= 0 or fields[2] != ELEMENTS[z] or n < 0:
                    stats["malformed_identity"] += 1
                    continue
                if fields[3].strip() != "0" or fields[-1].strip() != report:
                    stats["wrong_state_or_report"] += 1
                    continue
                # Spins are metadata, never additional model input. Use definite states only.
                parsed = moment_value(fields[6])
                if not SPIN.fullmatch(fields[5].strip()) or parsed is None:
                    stats["qualified_spin_sign_or_value"] += 1
                    continue
                value, sigma = parsed
                candidates[n, z].append(
                    record(
                        n,
                        z,
                        value * scale,
                        None if sigma is None else sigma * scale,
                        "IAEA-" + report.upper(),
                        f"{filename}:{index}",
                        [f"IAEA:{report}:gs:{n}:{z}"],
                        f"Recommended ground-state moment; spin={fields[5]}; raw={fields[6]}; "
                        f"NSR={fields[9]}; scale={scale}; "
                        + (
                            "nm denotes nuclear magnetons, not length"
                            if target == "mu_gs"
                            else "barns multiplied by 100 for e fm^2"
                        ),
                    )
                )
        table = {}
        for key, entries in candidates.items():
            if len(entries) != 1:
                stats["duplicate_recommendation_rows_excluded"] += len(entries)
                continue
            table[key] = entries[0]
        stats["retained"] = len(table)
        result[target], audit[target] = table, dict(stats)
    return result, audit


def read_gdr(raw):
    """Only In=1 recommendations; 8,845 systematic rows are not observations."""
    names = (
        "GDR_E1",
        "GDR_W1",
        "GDR_S1",
        "GDR_E2",
        "GDR_W2",
        "GDR_S2",
        "GDR_Ssum",
        "GDR_peak1",
        "GDR_peak2",
    )
    result = {key: {} for key in names}
    result["GDR_E_single"], result["GDR_W_single"], result["GDR_peak_single"] = {}, {}, {}
    result["GDR_E_centroid"] = {}
    stats = Counter()
    for index, line in enumerate((Path(raw) / "ripl4-gdr-slo.dat").read_text().splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        z, a = int(line[:4]), int(line[4:8])
        n = a - z
        flag = line[89:94].strip()
        stats["source_rows"] += 1
        if flag not in {"0", "1"}:
            raise ValueError("Unknown RIPL GDR experimental/systematics flag")
        if flag == "0":
            stats["systematics_excluded"] += 1
            continue
        values = [number(line[8 + 9 * i : 17 + 9 * i]) for i in range(9)]
        if n < 0 or not all(values[i] is not None and values[i] > 0 for i in (0, 1, 2, 6, 7)):
            raise ValueError("Invalid experimental GDR record")
        double = values[3] is not None
        if double and not all(values[i] is not None and values[i] > 0 for i in (3, 4, 5, 8)):
            raise ValueError("Incomplete two-mode GDR record")
        if double and values[3] <= values[0]:
            raise ValueError("GDR low/high mode ordering is inconsistent")
        deps = [f"RIPL4:GDR:SLO:{n}:{z}"]
        note = (
            "Experimental-data fitted SLO parameter, not a direct cross-section measurement; "
            f"In=1; {'two modes' if double else 'one mode'}; uncertainties not supplied"
        )

        def add(target, value, n=n, z=z, index=index, deps=deps, note=note):
            insert(
                result[target],
                (n, z),
                record(
                    n,
                    z,
                    value,
                    None,
                    "RIPL4-GDR-SLO-2018",
                    f"ripl4-gdr-slo.dat:{index}:{target}",
                    deps,
                    note,
                ),
            )

        for target, value in zip(names, values):
            if value is not None:
                add(target, value)
        # Same published 2018 strength-weighted convention for single and double modes.
        centroid = (
            (values[0] * values[2] + values[3] * values[5]) / (values[2] + values[5])
            if double
            else values[0]
        )
        add("GDR_E_centroid", centroid)
        if not double:
            for target, i in (("GDR_E_single", 0), ("GDR_W_single", 1), ("GDR_peak_single", 7)):
                add(target, values[i])
        stats["experimental_two_mode" if double else "experimental_single_mode"] += 1
    return result, dict(stats)


def read_resonances(raw):
    """BNL-2018 recommendations at the incident target N/Z, fixed s-wave L=0."""
    result = {key: {} for key in ("logD0_BNL", "Gg0_BNL", "S0_BNL")}
    stats = Counter()
    for index, line in enumerate(
        (Path(raw) / "ripl4-resonances-L0.dat").read_text().splitlines(), 1
    ):
        if not line.strip() or line.startswith("#"):
            continue
        stats["source_rows"] += 1
        z, n, a = int(line[:4]), int(line[4:8]), int(line[8:12])
        if a != n + z or int(line[18:20]) != 0:
            raise ValueError("Unexpected resonance target identity or partial wave")
        vals = [number(line[37 + 12 * i : 49 + 12 * i]) for i in range(12)]
        for target, i in (("logD0_BNL", 2), ("Gg0_BNL", 6), ("S0_BNL", 10)):
            value, sigma = vals[i], vals[i + 1]
            if value is None or value <= 0:
                stats[target + ":missing"] += 1
                continue
            if sigma is not None and sigma < 0:
                raise ValueError("Negative resonance uncertainty")
            if target == "logD0_BNL":
                sigma = None if sigma is None else sigma / (value * math.log(10))
                value = math.log10(value)
            # Published strength values are in units 1e-4, not the unscaled fraction.
            insert(
                result[target],
                (n, z),
                record(
                    n,
                    z,
                    value,
                    sigma,
                    "RIPL4-BNL2018-L0",
                    f"ripl4-resonances-L0.dat:{index}:{target}",
                    [f"RIPL4:BNL2018:L0:{n}:{z}"],
                    "Target nuclide N/Z, not compound (N+1,Z); fixed s-wave; "
                    "BNL columns only, no fallback to RIPL3; logD uncertainty is first-order propagation",
                ),
            )
    return result, dict(stats)


def read_barriers(raw):
    result = {
        key: {}
        for key in ("barrier_inner", "barrier_outer", "barrier_hw_inner", "barrier_hw_outer")
    }
    stats = Counter()
    for index, line in enumerate((Path(raw) / "ripl4-fission.dat").read_text().splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        z, a = int(fields[0]), int(fields[1])
        n = a - z
        stats["source_rows"] += 1
        # The source has a mistyped 84/207/Bi row. Do not silently repair it.
        if fields[2].capitalize() != ELEMENTS[z]:
            stats["inconsistent_element_excluded"] += 1
            continue
        for target, i in (
            ("barrier_inner", 4),
            ("barrier_hw_inner", 6),
            ("barrier_outer", 9),
            ("barrier_hw_outer", 11),
        ):
            value = number(fields[i]) if len(fields) > i else None
            if value is None or value <= 0:
                continue
            insert(
                result[target],
                (n, z),
                record(
                    n,
                    z,
                    value,
                    None,
                    "RIPL4-fission-2025",
                    f"ripl4-fission.dat:{index}:{target}",
                    [f"RIPL4:fission:{n}:{z}"],
                    "Empirical/model-dependent barrier; source uncertainties are ad-hoc spreads, "
                    f"not statistical sigma; source record={line.strip()}",
                ),
            )
    return result, dict(stats)


def read_decay(raw):
    result = {target: {} for target in DECAY_MODES.values()}
    stats = Counter()
    for index, line in enumerate((Path(raw) / "nubase_4.mas20.txt").read_text().splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        stats["source_rows"] += 1
        a, zstate = int(line[:3]), int(line[4:8])
        z, state = divmod(zstate, 10)
        if state or line[67:69].strip():
            stats["excited_or_ambiguous_state"] += 1
            continue
        n = a - z
        raw_t, unit = line[69:78].strip(), line[78:80].strip()
        t = number(raw_t) if "#" not in raw_t else None
        if t is None or t <= 0 or unit not in TIME_UNITS:
            stats["stable_estimated_censored_or_unknown_lifetime"] += 1
            continue
        for token in line[119:209].split(";"):
            token = token.strip()
            match = re.fullmatch(
                r"(A|B-|B\+|EC|SF|2p|p)=([0-9]+(?:\.[0-9]*)?(?:[Ee][+-]?\d+)?)(?:\s+\d+(?:\.\d*)?)?",
                token,
            )
            if not match:
                stats["unselected_qualified_or_unknown_branch"] += 1
                continue
            mode, fraction = match[1], float(match[2]) / 100
            if not 0 < fraction <= 1:
                stats["nonpositive_or_invalid_branch"] += 1
                continue
            target = DECAY_MODES[mode]
            # Log before dividing avoids overflow across the very wide lifetime range.
            y = math.log10(t) + math.log10(TIME_UNITS[unit]) - math.log10(fraction)
            insert(
                result[target],
                (n, z),
                record(
                    n,
                    z,
                    y,
                    None,
                    "NUBASE2020",
                    f"nubase_4.mas20.txt:{index}:{mode}",
                    [f"NUBASE2020:gs:{n}:{z}:lifetime", f"NUBASE2020:gs:{n}:{z}:branch:{mode}"],
                    f"log10(T_partial / s); T_partial=T_total/(branch_percent/100); "
                    f"raw T={raw_t} {unit}; dT={line[81:88].strip()}; branch={token}; "
                    "branch/half-life covariance unknown, sigma unavailable; B+ includes electron capture convention",
                ),
            )
    return result, dict(stats)


def grodzins_product(tables):
    result = {}
    for key in sorted(set(tables["BE2"]) & set(tables["E2plus"])):
        b, e = tables["BE2"][key], tables["E2plus"][key]
        n, z = key
        result[key] = record(
            n,
            z,
            b["y"] * e["y"],
            None,
            "BE2-ENSDF-derived",
            b["source_record"] + " * " + e["source_record"],
            b["dependencies"] + e["dependencies"],
            "E(2+) in MeV times B(E2;0+->2+) in e^2 fm^4; composite target, not measured E2 as input; covariance unknown",
        )
    return result


def read_external(raw, tables):
    result, audit = {}, {}
    for name, reader in (
        ("moments", read_moments),
        ("gdr", read_gdr),
        ("resonances", read_resonances),
        ("barriers", read_barriers),
        ("decay", read_decay),
    ):
        values, counts = reader(raw)
        result.update(values)
        audit[name] = counts
    result["Grodzins_EB"] = grodzins_product(tables)
    return result, audit
