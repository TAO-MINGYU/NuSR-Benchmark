import csv
import json
import math
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import numpy as np

from nuclearbench.bank import get_task, load_bank, read_rows, validate, write_rows
from nuclearbench.data import level_sigma, number, read_be2, read_levels, read_radii, record
from nuclearbench.expressions import evaluate, prove
from nuclearbench.formulas import FORMULAS
from nuclearbench.scoring import load_predictions, partition, recover, score
from nuclearbench.sources import SOURCES, digest, fetch
from nuclearbench.splits import SPLITS, make_split, validate_split

ROOT = Path(__file__).resolve().parents[1]


class PhysicsTests(unittest.TestCase):
    def test_printed_bw_and_bwm_independent_arithmetic(self):
        for n, z in ((30, 26), (31, 26), (31, 27)):
            a = n + z
            parity = 1 if n % 2 == z % 2 == 0 else -1 if n % 2 == z % 2 == 1 else 0
            expected = (
                15.78 * a
                - 18.34 * a ** (2 / 3)
                - 0.71 * z * (z - 1) / a ** (1 / 3)
                - 23.21 * (n - z) ** 2 / a
                + 12 * parity / math.sqrt(a)
            )
            self.assertAlmostEqual(
                evaluate(FORMULAS[0]["expression"], [n], [z])[0], expected, places=10
            )
            expected = (
                15.777 * a
                - 18.34 * a ** (2 / 3)
                - 0.71 * z * (z - 1) / a ** (1 / 3)
                - 23.21 * (n - z) ** 2 / (a * (1 + math.exp(-a / 17)))
                + 12 * (1 - math.exp(-a / 30)) * parity / math.sqrt(a)
            )
            self.assertAlmostEqual(
                evaluate(FORMULAS[1]["expression"], [n], [z])[0], expected, places=10
            )

    def test_radius_is_rms_and_valence_closures_are_source_specific(self):
        actual = evaluate(FORMULAS[3]["expression"], [126], [82])[0]
        self.assertAlmostEqual(actual, math.sqrt(3 / 5) * 1.2269 * 208 ** (1 / 3), places=12)
        self.assertLess(actual, 6)
        self.assertEqual(evaluate("P_s", [28], [28])[0], 0)
        self.assertNotEqual(evaluate("P_s", [20], [20])[0], evaluate("P_m", [20], [20])[0])
        self.assertEqual(evaluate("P_m", [20], [20])[0], 0)

    def test_last_digit_uncertainty(self):
        self.assertAlmostEqual(level_sigma("123.45", "12"), 0.12)
        self.assertIsNone(level_sigma("123.45", "AP"))
        self.assertIsNone(number("1.2+X"))
        self.assertEqual(number("12#"), 12)

    def test_source_qualifiers_and_preliminary_radii(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row = {
                "reference": "ADNDT_107_1_2016_2016PR01",
                "adoptedEntryType": "MODEL_INDEPENDENT",
                "nuclide": {"n": 20, "z": 20, "a": 40},
                "be2": {"value": 0.004, "error": -1, "ndsText": []},
            }
            (root / "be2-adopted.json").write_text(json.dumps([row]))
            parsed = read_be2(root)[20, 20]
            self.assertEqual(parsed["y"], 40)
            self.assertIsNone(parsed["sigma"])
            row["be2"]["isUpperLimit"] = True
            (root / "be2-adopted.json").write_text(json.dumps([row]))
            self.assertEqual(read_be2(root), {})
            (root / "radii.html").write_text(
                "<tr>"
                + "".join(
                    "<td>" + s + "</td>"
                    for s in ("20", "Ca", "40", "20", "3.47", "0.01", "3.9", "0.2")
                )
                + "</tr>"
            )
            self.assertEqual(read_radii(root)[20, 20]["y"], 3.47)

    def test_real_binding_anchor(self):
        task_id = next(
            t["id"]
            for t in load_bank(ROOT)["tasks"]
            if t["category"] == "observable_prediction" and t["observable"] == "B"
        )
        _, rows, _ = get_task(ROOT, task_id)
        iron = next(r for r in rows if r["N"] == 30 and r["Z"] == 26)
        self.assertAlmostEqual(iron["y"], 492.26, places=2)

    def test_ensdf_ambiguous_lower_level_is_not_silently_skipped(self):
        def level(energy, spin):
            return " 40CA  L " + f"{energy:<10}" + "  " + f"{spin:<18}" + " " * 41

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def archive(extra):
                text = "\n".join([" 40CA    ADOPTED LEVELS", level("0", "0+"), *extra, ""])
                with zipfile.ZipFile(root / "ensdf_260901.zip", "w") as out:
                    out.writestr("ensdf.040", text)

            archive([level("100.0", "2+"), level("300.0", "4+")])
            tables = read_levels(root)
            self.assertEqual(tables["E2plus"][20, 20]["y"], 0.1)
            self.assertAlmostEqual(tables["R42"][20, 20]["y"], 3)
            self.assertEqual(len(tables["R42"][20, 20]["dependencies"]), 2)
            archive([level("50.0", "(2+)"), level("100.0", "2+")])
            self.assertEqual(read_levels(root)["E2plus"], {})

    def test_frozen_mass_indicator_signs_and_dependencies(self):
        tasks = load_bank(ROOT)["tasks"]
        for observable in ("S2n", "OES3n", "delta2n"):
            task = next(
                t
                for t in tasks
                if t["category"] == "observable_prediction" and t["observable"] == observable
            )
            _, rows, _ = get_task(ROOT, task["id"])
            row = next(r for r in rows if r["N"] == 30 and r["Z"] == 26)
            if observable == "S2n":
                self.assertTrue(15 < row["y"] < 25)
                self.assertEqual(len(row["dependencies"]), 2)
            else:
                self.assertIsNone(row["sigma"])
                self.assertEqual(len(row["dependencies"]), 3)
            if observable == "OES3n":
                self.assertGreater(row["y"], 0)


class PartitionTests(unittest.TestCase):
    def test_frozen_small_source_fetch_does_not_need_network(self):
        small = {name: value for name, value in SOURCES.items() if not name.endswith(".zip")}
        with (
            tempfile.TemporaryDirectory() as directory,
            patch("nuclearbench.sources.SOURCES", small),
            patch(
                "nuclearbench.sources.urlopen",
                side_effect=AssertionError("Unexpected network request"),
            ),
        ):
            fetch(directory, ROOT / "source_snapshots")
            for name, (_, sha) in small.items():
                self.assertEqual(digest(Path(directory) / name), sha)

    def test_embargo_and_order_independence(self):
        rows = [
            record(
                n,
                z,
                n + z,
                None,
                "fixture",
                "fixture",
                [f"ME:{n - 1}:{z}", f"ME:{n}:{z}", f"ME:{n + 1}:{z}"],
            )
            for n in range(10, 45)
            for z in range(10, 18)
        ]
        for kind in SPLITS:
            with self.subTest(kind=kind):
                split = make_split(rows, kind)
                self.assertEqual(split, make_split(list(reversed(rows)), kind))
                validate_split(rows, split, kind)
        self.assertGreater(make_split(rows, "iid101")["counts"]["purged"], 0)

    def test_manifest_and_checksum_tampering(self):
        result = validate(ROOT)
        self.assertEqual(result["tasks"], {"expression_recovery": 98, "observable_prediction": 53})
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "bank"
            destination.mkdir()
            for path in (
                "data",
                "splits",
                "source_snapshots",
                "bank.json",
                "checksums.json",
                "coverage.json",
                "literature.json",
                "external_audit.json",
                "target_catalog_audit.json",
            ):
                if (ROOT / path).is_dir():
                    shutil.copytree(ROOT / path, destination / path)
                else:
                    shutil.copy2(ROOT / path, destination / path)
            original_bank = (destination / "bank.json").read_bytes()
            original_checksums = (destination / "checksums.json").read_bytes()
            altered = load_bank(destination)
            altered["tasks"][0]["structure_group"] = "fabricated_independent_group"
            (destination / "bank.json").write_text(json.dumps(altered))
            locked = json.loads(original_checksums)
            locked["bank.json"] = digest(destination / "bank.json")
            (destination / "checksums.json").write_text(json.dumps(locked))
            with self.assertRaisesRegex(ValueError, "metadata differs from registry"):
                validate(destination)
            (destination / "bank.json").write_bytes(original_bank)
            (destination / "checksums.json").write_bytes(original_checksums)
            # Updating the checksum must not legitimize a fabricated source label.
            external = next(t for t in load_bank(destination)["tasks"] if t["id"] == "B34_mu_gs")
            data_path = destination / external["data"]
            original_data = data_path.read_bytes()
            rows = read_rows(data_path)
            rows[0]["y"] += 1.0
            write_rows(data_path, rows)
            locked = json.loads(original_checksums)
            locked[external["data"]] = digest(data_path)
            (destination / "checksums.json").write_text(json.dumps(locked))
            with self.assertRaisesRegex(ValueError, "External labels"):
                validate(destination)
            data_path.write_bytes(original_data)
            (destination / "checksums.json").write_bytes(original_checksums)
            # A changed upstream source cannot become this same version by changing
            # both metadata and checksums, even when its parsed numeric rows match.
            raw_name = "ripl4-resonances.readme"
            raw_path = destination / "source_snapshots" / raw_name
            original_raw = raw_path.read_bytes()
            raw_path.write_bytes(original_raw + b"\nchanged source edition\n")
            altered = load_bank(destination)
            altered["sources"][raw_name]["sha256"] = digest(raw_path)
            (destination / "bank.json").write_text(json.dumps(altered))
            locked = json.loads(original_checksums)
            locked["bank.json"] = digest(destination / "bank.json")
            locked["source_snapshots/" + raw_name] = digest(raw_path)
            (destination / "checksums.json").write_text(json.dumps(locked))
            with self.assertRaisesRegex(ValueError, "Source registry"):
                validate(destination)
            raw_path.write_bytes(original_raw)
            (destination / "bank.json").write_bytes(original_bank)
            (destination / "checksums.json").write_bytes(original_checksums)
            task = load_bank(destination)["tasks"][0]
            with (destination / task["data"]).open("a") as stream:
                stream.write("tampered\n")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                validate(destination)


class ScoringTests(unittest.TestCase):
    def test_id_alignment_and_coverage_failures(self):
        task = "A01_BW"
        _, test = partition(ROOT, task, "iid101")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "predictions.csv"

            def write(rows):
                with path.open("w", newline="") as stream:
                    writer = csv.writer(stream)
                    writer.writerow(["sample_id", "prediction"])
                    writer.writerows(rows)

            rows = [(r["sample_id"], r["y"]) for r in reversed(test)]
            write(rows)
            self.assertEqual(score(ROOT, task, "iid101", path)["rmse"], 0)
            for bad in (
                rows[:-1],
                rows + [rows[0]],
                rows + [("unknown", 1)],
                [(r[0], float("nan")) for r in rows],
            ):
                write(bad)
                with self.assertRaises(ValueError):
                    load_predictions(path, [r["sample_id"] for r in test])

    def test_proof_vs_close_fit(self):
        self.assertEqual(prove("N+Z", "A"), "proved_equal")
        f = FORMULAS[3]
        result = recover(ROOT, f["id"], "iid101", f["expression"])
        self.assertEqual(result["symbolic_status"], "proved_equal")
        self.assertTrue(result["numeric_agreement"])
        result = recover(ROOT, f["id"], "iid101", f["expression"] + "+0.0001")
        self.assertEqual(result["symbolic_status"], "unproved")
        self.assertFalse(result["numeric_agreement"])
        self.assertLess(result["rmse"], 0.001)

    def test_no_code_execution_or_invalid_numbers(self):
        for expression in ("__import__('os').getcwd()", "N[0]", "(lambda: 1)()", "N.foo", "True"):
            with self.assertRaises((ValueError, SyntaxError)):
                evaluate(expression, [20], [20])
        with self.assertRaises((ValueError, FloatingPointError)):
            evaluate("1/(N-N)", [20], [20])
        np.testing.assert_allclose(evaluate("N*0+1", [20, 21], [20, 20]), [1, 1])


if __name__ == "__main__":
    unittest.main()
