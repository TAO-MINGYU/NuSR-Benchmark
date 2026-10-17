"""Independent fixed-format readers and explicit primitive label dependencies."""

import html
import json
import math
import re
import zipfile
from decimal import Decimal
from pathlib import Path

NUMBER = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?\Z")
ELEMENTS = [
    "_",
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
]
ATOMIC = {s.upper(): z for z, s in enumerate(ELEMENTS)}


def number(text):
    text = str(text).strip().replace("#", ".")
    return float(text) if NUMBER.fullmatch(text) and math.isfinite(float(text)) else None


def primitive(n, z, version="AME2020"):
    return f"{version}:ME:{n}:{z}"


def record(n, z, y, sigma, source, locator, dependencies, note=""):
    if y is None or not math.isfinite(y):
        raise ValueError("Missing or nonfinite point label")
    return {
        "sample_id": f"N{n:03d}Z{z:03d}",
        "N": n,
        "Z": z,
        "A": n + z,
        "y": y,
        "sigma": sigma,
        "source": source,
        "source_record": locator,
        "dependencies": sorted(set(dependencies)),
        "note": note,
        "observed_y": None,
        "observed_sigma": None,
        "observed_dependencies": [],
    }


def insert(table, key, value):
    if key in table:
        raise ValueError(f"Duplicate upstream coordinate: {key}")
    table[key] = value


def read_masses(raw, version="AME2020"):
    if version not in {"AME2016", "AME2020"}:
        raise ValueError("Unsupported AME vintage")
    old = version == "AME2016"
    mass_file = "mass16.txt" if old else "mass_1.mas20.txt"
    text = (Path(raw) / mass_file).read_text()
    if "BINDING ENERGY/A" not in text or ("f13.5" if old else "f14.6") not in text:
        raise ValueError("Unsupported AME mass format")
    masses, binding = {}, {}
    for index, line in enumerate(text.splitlines(), 1):
        if len(line) < 82 or not line[4:9].strip().isdigit() or not line[9:14].strip().isdigit():
            continue
        n, z, a = int(line[4:9]), int(line[9:14]), int(line[14:19])
        if a != n + z:
            raise ValueError("AME inconsistent N,Z,A")
        me_end, unc_end, ba_end, bu_start, bu_end = (
            (41, 52, 63, 63, 72) if old else (42, 54, 67, 68, 78)
        )
        me, unc = number(line[28:me_end]), number(line[me_end:unc_end])
        ba, bu = number(line[unc_end:ba_end]), number(line[bu_start:bu_end])
        locator = f"{mass_file}:{index}"
        if me is not None and "#" not in line[28:unc_end]:
            insert(
                masses,
                (n, z),
                record(
                    n,
                    z,
                    me * 0.001,
                    None if unc is None else unc * 0.001,
                    version,
                    locator,
                    [primitive(n, z, version)],
                ),
            )
        if ba is not None and "#" not in line[unc_end:bu_end] and (n, z) in masses:
            insert(
                binding,
                (n, z),
                record(
                    n,
                    z,
                    ba * a * 0.001,
                    None if bu is None else bu * a * 0.001,
                    version,
                    locator,
                    [primitive(n, z, version)],
                    "B=A*(B/A); source B/A rounded",
                ),
            )
    result = {"B": binding}
    for filename, names in (
        ("rct1.mas20.txt", (("S2n", 2, 0), ("S2p", 0, 2))),
        ("rct2_1.mas20.txt", (("Sn", 1, 0), ("Sp", 0, 1))),
    ):
        if old:
            filename = "rct1-16.txt" if filename == "rct1.mas20.txt" else "rct2-16.txt"
        text = (Path(raw) / filename).read_text()
        if ("f10.2,f8.2" if old else "f12.4,f10.4") not in text:
            raise ValueError("Unsupported AME reaction format")
        for name, _, _ in names:
            result[name] = {}
        for index, line in enumerate(text.splitlines(), 1):
            if (
                len(line) < 34
                or not line[1:4].strip().isdigit()
                or not line[8:11].strip().isdigit()
            ):
                continue
            a, z = int(line[1:4]), int(line[8:11])
            n = a - z
            for column, (name, dn, dz) in enumerate(names):
                width, stride = (10, 18) if old else (12, 22)
                lo = 12 + stride * column
                value, unc = number(line[lo : lo + width]), number(line[lo + width : lo + stride])
                neighbor = (n - dn, z - dz)
                if (
                    value is None
                    or "#" in line[lo : lo + stride]
                    or (n, z) not in masses
                    or neighbor not in masses
                ):
                    continue
                expected = (
                    masses[neighbor]["y"]
                    + dn * masses[1, 0]["y"]
                    + dz * masses[0, 1]["y"]
                    - masses[n, z]["y"]
                )
                if abs(expected - value * 0.001) > (0.00003 if old else 0.000003):
                    raise ValueError(f"Reaction/mass inconsistency: {name},{n},{z}")
                insert(
                    result[name],
                    (n, z),
                    record(
                        n,
                        z,
                        value * 0.001,
                        None if unc is None else unc * 0.001,
                        version,
                        f"{filename}:{index}",
                        [primitive(n, z, version), primitive(*neighbor, version)],
                        "Published reaction uncertainty; nucleon masses are fixed constants",
                    ),
                )
    for name, axis, step, pairing in (
        ("OES3n", 0, 1, True),
        ("OES3p", 1, 1, True),
        ("delta2n", 0, 2, False),
        ("delta2p", 1, 2, False),
    ):
        table = {}
        for (n, z), row in masses.items():
            left = (n - step, z) if axis == 0 else (n, z - step)
            right = (n + step, z) if axis == 0 else (n, z + step)
            if left not in masses or right not in masses:
                continue
            factor = ((-1) ** (n if axis == 0 else z)) / 2 if pairing else 1
            value = factor * (masses[left]["y"] - 2 * row["y"] + masses[right]["y"])
            table[n, z] = record(
                n,
                z,
                value,
                None,
                version + "-derived",
                row["source_record"],
                [primitive(*left, version), primitive(n, z, version), primitive(*right, version)],
                "Three-point atomic mass excess difference; covariance unavailable, sigma unknown",
            )
        result[name] = table
    return result


def read_radii(raw):
    text = (Path(raw) / "radii.html").read_text()
    result = {}
    z = None
    for index, row in enumerate(
        re.findall(r"<tr\b[^>]*>(.*?)</tr>", text, re.IGNORECASE | re.DOTALL)
    ):
        cells = [
            html.unescape(re.sub(r"<[^>]*>", "", c)).strip()
            for c in re.findall(r"<td\b[^>]*>(.*?)</td>", row, re.IGNORECASE | re.DOTALL)
        ]
        if len(cells) != 8:
            continue
        if cells[0]:
            z = int(cells[0])
        if not z:
            continue
        a, n = int(cells[2]), int(cells[3])
        if a != n + z:
            raise ValueError("Radii inconsistent N,Z,A")
        value, unc = number(cells[4]), number(cells[5])
        if value is None:
            continue
        if value <= 0:
            raise ValueError("Not a charge rms radius")
        insert(
            result,
            (n, z),
            record(
                n,
                z,
                value,
                unc,
                "Angeli2013",
                f"radii.html:table-row-{index}",
                [f"Angeli2013:R:{n}:{z}"],
                "Published column only; preliminary column excluded",
            ),
        )
    return result


def read_be2(raw):
    result = {}
    for index, row in enumerate(json.loads((Path(raw) / "be2-adopted.json").read_text())):
        if (
            row.get("reference") != "ADNDT_107_1_2016_2016PR01"
            or row.get("adoptedEntryType") != "MODEL_INDEPENDENT"
        ):
            continue
        nuc = row["nuclide"]
        n, z = nuc["n"], nuc["z"]
        if n % 2 or z % 2 or nuc["a"] != n + z:
            raise ValueError("Unexpected B(E2) ground state transition")
        field = row.get("be2") or {}
        qualifiers = field.get("ndsText", [])
        if (
            field.get("isUpperLimit")
            or field.get("isLowerLimit")
            or any(re.search(r"\b(LT|GT|LE|GE|AP|CA|SY)\b", str(q)) for q in qualifiers)
        ):
            continue
        value, unc = field.get("value"), field.get("error")
        if not isinstance(value, (float, int)):
            continue
        sigma = unc * 10000 if isinstance(unc, (float, int)) and unc >= 0 else None
        insert(
            result,
            (n, z),
            record(
                n,
                z,
                value * 10000,
                sigma,
                "BE2-2016",
                f"be2-adopted.json:{index}:be2",
                [f"BE2-2016:{n}:{z}"],
                "0+ -> 2+; e^2 b^2 * 10000; source error="
                + str(unc)
                + "; qualifiers="
                + json.dumps(qualifiers),
            ),
        )
    return result


def level_sigma(value, unc):
    return (
        float(Decimal(int(unc)) * Decimal(10) ** Decimal(value).as_tuple().exponent)
        if unc.isdigit()
        else None
    )


STATES = [
    (2, "+"),
    (4, "+"),
    (3, "-"),
    (6, "+"),
    (8, "+"),
    (10, "+"),
    (1, "-"),
    (5, "-"),
    (7, "-"),
    (9, "-"),
    (2, "-"),
    (4, "-"),
    (6, "-"),
    (8, "-"),
    (10, "-"),
    (1, "+"),
    (3, "+"),
    (5, "+"),
    (7, "+"),
    (9, "+"),
    (0, "+"),
]


def state_name(spin, parity):
    return f"E{spin}" + ("plus" if parity == "+" else "minus")


def read_levels(raw):
    result = {state_name(j, p): {} for j, p in STATES}

    def process(lines, filename, start):
        if not lines or not lines[0][9:39].strip().startswith("ADOPTED LEVELS"):
            return
        match = re.fullmatch(r"\s*(\d+)([A-Z]{1,2}|\d{2})\s*", lines[0][:5])
        if not match:
            return
        a, symbol = match.groups()
        z = ATOMIC.get(symbol, 100 + int(symbol) if symbol.isdigit() else -1)
        n = int(a) - z
        if z < 0 or n < 0 or n % 2 or z % 2:
            return
        levels = []
        censored = []
        unresolved = False
        for offset, line in enumerate(lines):
            if line[5:8] != "  L":
                continue
            energy, unc, spin = line[9:19].strip(), line[19:21].strip(), line[21:39].strip()
            value = number(energy)
            if (
                value is None
                or unc in {"LT", "LE", "GT", "GE", "AP", "CA", "SY"}
                or line[79:80] in {"?", "S"}
            ):
                if value is not None and value > 0:
                    censored.append(value)
                if not any(x[0] > 0 for x in levels):
                    unresolved = True
                continue
            if value >= 0:
                levels.append(
                    (value, level_sigma(energy, unc), spin, f"{filename}:{start + offset}")
                )
        if not any(x[0] == 0 and x[2] == "0+" for x in levels) or unresolved:
            return
        for j, parity in STATES:
            name, spin = state_name(j, parity), f"{j}{parity}"
            eligible = sorted(x for x in levels if x[0] > 0 and x[2] == spin)
            if not eligible:
                continue
            value, unc, _, locator = eligible[0]
            if any(e < value for e in censored) or any(
                0 < x[0] < value and not re.fullmatch(r"\d+(?:/\d+)?[+-]", x[2]) for x in levels
            ):
                continue
            insert(
                result[name],
                (n, z),
                record(
                    n,
                    z,
                    value * 0.001,
                    None if unc is None else unc * 0.001,
                    "ENSDF-2026-09-01",
                    locator,
                    [f"ENSDF:{locator}"],
                    "First definite " + spin + "; even-even 0+ ground state; " + lines[0].strip(),
                ),
            )

    with zipfile.ZipFile(Path(raw) / "ensdf_260901.zip") as archive:
        for filename in sorted(archive.namelist()):
            if not re.fullmatch(r"ensdf\.\d{3}", filename):
                continue
            current = []
            start = 0
            for index, line in enumerate(
                archive.read(filename).decode("ascii", errors="replace").splitlines(), 1
            ):
                if not line.strip() or (len(line) > 9 and line[5:9] == "    "):
                    process(current, filename, start)
                    current = (
                        [line]
                        if line.strip() and line[9:39].strip().startswith("ADOPTED LEVELS")
                        else []
                    )
                    start = index
                elif current:
                    current.append(line)
            process(current, filename, start)
    result["R42"] = {}
    for (n, z), e4 in result["E4plus"].items():
        if (n, z) not in result["E2plus"]:
            continue
        e2 = result["E2plus"][n, z]
        result["R42"][n, z] = record(
            n,
            z,
            e4["y"] / e2["y"],
            None,
            "ENSDF-derived",
            e4["source_record"] + " / " + e2["source_record"],
            e4["dependencies"] + e2["dependencies"],
            "E4/E2; covariance unavailable, sigma unknown",
        )
    # Keep original public B01-B15 identifiers stable; append new spin states.
    return {
        name: result[name]
        for name in (
            "E2plus",
            "E4plus",
            "E3minus",
            "R42",
            *(state_name(j, p) for j, p in STATES[3:]),
        )
    }


def load_observables(raw):
    tables = read_masses(raw)
    tables["Rch"] = read_radii(raw)
    tables["BE2"] = read_be2(raw)
    tables.update(read_levels(raw))
    return tables
