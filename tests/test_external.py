import csv
import json
import math
import tempfile
import unittest
from pathlib import Path

from nuclearbench.data import record
from nuclearbench.expressions import evaluate
from nuclearbench.external_data import (
    YEAR_SECONDS,
    grodzins_product,
    moment_value,
    read_barriers,
    read_decay,
    read_gdr,
    read_moments,
    read_resonances,
)
from nuclearbench.more_formulas import more_formulas

ROOT = Path(__file__).resolve().parents[1]


class ExternalPhysicsTests(unittest.TestCase):
    def test_supplied_catalog_audit_is_complete_and_maps_to_actual_tasks(self):
        audit = json.loads((ROOT / "target_catalog_audit.json").read_text())
        entries = audit["entries"]
        self.assertEqual({r["id"] for r in entries}, {f"NF-{i:04d}" for i in range(1, 77)})
        tasks = {t["id"] for t in json.loads((ROOT / "bank.json").read_text())["tasks"]}
        for row in entries:
            self.assertTrue(row["decision"] and row["reason"] and row["metadata_sha256"])
            self.assertFalse(set(row["mapped_tasks"]) - tasks)

    def test_published_gdr_nested_reference_and_units(self):
        fs = {f["id"]: f for f in more_formulas()}
        n, z = 126, 82
        a = n + z
        energy = 31.2 / a ** (1 / 3) + 20.6 / a ** (1 / 6)
        width = 0.026 * energy**1.91
        peak = 144 * n * z / (a * math.pi * width)
        for key, expected in [
            ("A42_GDR_centroid_2005", energy),
            ("A43_GDR_width_2005", width),
            ("A44_GDR_peak_2005", peak),
        ]:
            self.assertAlmostEqual(
                evaluate(fs[key]["expression"], [n], [z])[0], expected, places=11
            )
        energy2018 = (
            130.0 * math.sqrt(4 * n * z / a**2) / (a ** (1 / 3) * math.sqrt(1 + 9.0 / a ** (1 / 3)))
        )
        self.assertAlmostEqual(
            evaluate(fs["A45_GDR_centroid_SLO2018"]["expression"], [n], [z])[0],
            energy2018,
            places=12,
        )
        # Conversion is 1keV * 1barn^2 = 10MeV*fm^4; no measured excitation input.
        product = 2.57 * z * z / a ** (2 / 3) * 10
        self.assertAlmostEqual(
            evaluate(fs["A47_Grodzins_product"]["expression"], [n], [z])[0], product, places=10
        )

    def test_moment_sign_qualifiers_and_last_digits(self):
        self.assertEqual(moment_value("-0.3358(4)"), (-0.3358, 0.0004))
        self.assertEqual(moment_value("+ 0.7547(3)"), (0.7547, 0.0003))
        for value in [
            "(-)0.8652(3)",
            "+0.55(4) or +0.60(4)",
            "+0.70)15)",
            "[1.2(3)]",
            "<0.1",
            "1.0#",
        ]:
            self.assertIsNone(moment_value(value))

    def test_moment_mass_column_and_ground_state_only(self):
        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory)
            for filename, heading, report, value in [
                ("magn_mom_recomm.csv", "magnetic dipole [nm]", "indc-nds-0915", "-0.3358(4)"),
                ("elec_mom_recomm.csv", "electric quadrupole [b]", "indc-nds-0833", "+0.104(1)"),
            ]:
                with (raw / filename).open("w", newline="") as stream:
                    out = csv.writer(stream)
                    out.writerow(
                        [
                            "z",
                            "n.n+n.z",
                            "symbol",
                            "energy [keV]",
                            "halflife",
                            "spin",
                            heading,
                            "method",
                            "description",
                            "nsr",
                            "journal",
                            "indc",
                        ]
                    )
                    out.writerow(
                        [
                            26,
                            59,
                            "Fe",
                            0,
                            "44.5d",
                            "3/2-",
                            value,
                            "NMR",
                            "",
                            "",
                            "",
                            "indc-nds-0915" if "magn" in filename else report,
                        ]
                    )
                    out.writerow([26, 59, "Fe", 10, "1s", "3/2-", value, "NMR", "", "", "", report])
            tables, _ = read_moments(raw)
            self.assertEqual(set(tables["mu_gs"]), {(33, 26)})
            self.assertEqual(tables["mu_gs"][33, 26]["y"], -0.3358)
            self.assertEqual(tables["Q_gs"][33, 26]["y"], 10.4)
            self.assertAlmostEqual(tables["Q_gs"][33, 26]["sigma"], 0.1)

    def test_official_gdr_systematics_exclusion_and_centroid(self):
        tables, audit = read_gdr(ROOT / "source_snapshots")
        self.assertEqual(audit["systematics_excluded"], 8845)
        self.assertEqual(len(tables["GDR_E1"]), 135)
        self.assertEqual(len(tables["GDR_E_single"]), 74)
        self.assertEqual(tables["GDR_E_single"][126, 82]["y"], 13.370)
        expected = (12.300 * 0.432 + 16.030 * 0.821) / (0.432 + 0.821)
        self.assertAlmostEqual(tables["GDR_E_centroid"][90, 60]["y"], expected, places=12)
        self.assertIsNone(tables["GDR_E_centroid"][90, 60]["sigma"])
        self.assertNotIn((11, 8), tables["GDR_E1"])  # 19O is In=0.

    def test_resonance_target_identity_and_bnl_columns(self):
        tables, _ = read_resonances(ROOT / "source_snapshots")
        row = tables["logD0_BNL"][12, 11]  # 23Na target, compound is 24Na.
        self.assertAlmostEqual(row["y"], math.log10(122000.0), places=12)
        self.assertAlmostEqual(row["sigma"], 30000 / (122000 * math.log(10)), places=12)
        self.assertEqual(tables["Gg0_BNL"][14, 13]["y"], 1.61)  # 27Al.
        self.assertEqual(tables["S0_BNL"][14, 13]["y"], 2.8)  # published1e-4 units.

    def test_barrier_model_status_and_source_identity_error(self):
        tables, audit = read_barriers(ROOT / "source_snapshots")
        self.assertEqual(audit["inconsistent_element_excluded"], 1)
        self.assertNotIn((123, 84), tables["barrier_inner"])
        self.assertEqual(tables["barrier_inner"][146, 94]["y"], 6.05)
        self.assertIsNone(tables["barrier_inner"][146, 94]["sigma"])

    def test_partial_lifetime_units_and_branch_factor(self):
        tables, _ = read_decay(ROOT / "source_snapshots")
        self.assertAlmostEqual(
            tables["logT_beta_minus"][33, 27]["y"], math.log10(5.2714 * YEAR_SECONDS), places=12
        )
        self.assertAlmostEqual(
            tables["logT_SF"][154, 98]["y"],
            math.log10(2.645 * YEAR_SECONDS / (3.1028 / 100)),
            places=12,
        )
        self.assertIsNone(tables["logT_SF"][154, 98]["sigma"])
        self.assertNotEqual(tables["logT_SF"][154, 98]["y"], math.log10(2.645 * YEAR_SECONDS))

    def test_decay_limits_estimates_isomers_and_unknown_branches_rejected(self):
        def line(state=0, t="2.0", branch="A=50"):
            chars = list(" " * 209)

            def put(start, end, value):
                chars[start:end] = list(str(value).ljust(end - start))

            put(0, 3, "060")
            put(4, 8, f"027{state}")
            put(69, 78, t)
            put(78, 80, "s")
            put(119, 209, branch)
            return "".join(chars)

        with tempfile.TemporaryDirectory() as directory:
            raw = Path(directory)
            for text in [
                line(state=1),
                line(t="2.0#"),
                line(t="<2.0"),
                line(t="~2.0"),
                line(branch="A~50"),
                line(branch="A<50"),
                line(branch="A=?"),
                line(branch="A=0"),
            ]:
                (raw / "nubase_4.mas20.txt").write_text(text + "\n")
                tables, _ = read_decay(raw)
                self.assertFalse(any(tables.values()))
            (raw / "nubase_4.mas20.txt").write_text(line() + "\n")
            tables, _ = read_decay(raw)
            self.assertEqual(tables["logT_alpha"][33, 27]["y"], math.log10(4.0))

    def test_composite_preserves_both_primitive_parents(self):
        b = record(30, 26, 1000, 10, "BE2", "b", ["strength"])
        e = record(30, 26, 0.8, 0.01, "ENSDF", "e", ["level"])
        row = grodzins_product({"BE2": {(30, 26): b}, "E2plus": {(30, 26): e}})[30, 26]
        self.assertEqual(row["y"], 800)
        self.assertEqual(row["dependencies"], ["level", "strength"])
        self.assertIsNone(row["sigma"])


if __name__ == "__main__":
    unittest.main()
