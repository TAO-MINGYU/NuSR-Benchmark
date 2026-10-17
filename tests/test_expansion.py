import json
import math
import unittest
from collections import Counter
from pathlib import Path

from nuclearbench.aggregation import aggregate
from nuclearbench.bank import get_task, load_bank
from nuclearbench.controls import control_formulas
from nuclearbench.coverage import summary
from nuclearbench.data import read_masses, record
from nuclearbench.expanded_formulas import published_formulas
from nuclearbench.expressions import evaluate
from nuclearbench.scoring import partition
from nuclearbench.splits import validate_split
from nuclearbench.temporal import make_temporal_split, temporal_rows

ROOT = Path(__file__).resolve().parents[1]


class PublishedPhysicsTests(unittest.TestCase):
    def test_ha_and_yrast_published_anchor(self):
        fs = {f["id"]: f for f in published_formulas()}
        # 56Fe has Np=Nn=2 relative to the 28 closures.
        expected = 34.9 * 56 ** (-1.19) + math.exp(-0.36 * 2) + math.exp(-0.36 * 2)
        self.assertAlmostEqual(
            evaluate(fs["A14_Ha_E2"]["expression"], [30], [26])[0], expected, places=12
        )
        expected = 68 * 56 ** (-1.34) + 0.83 * math.exp(-0.42 * 2) + 1.17 * math.exp(-0.28 * 2)
        self.assertAlmostEqual(
            evaluate(fs["A16_yrast_E2plus"]["expression"], [30], [26])[0], expected, places=12
        )
        states = [f for f in fs.values() if "_yrast_" in f["id"]]
        self.assertEqual(len(states), 20)
        self.assertFalse(any(f["fixed_spin"] == 11 for f in states))
        self.assertEqual(len({f["structure_group"] for f in states}), 1)

    def test_ei_shell_occupancy_and_correlated_radius(self):
        expected_q = (2 * 20 / 22**2) * (12 * 2 / 14**2)
        self.assertAlmostEqual(evaluate("Q_EI", [30], [26])[0], expected_q, places=15)
        for n, z in ((28, 26), (30, 28), (50, 26)):
            self.assertEqual(evaluate("Q_EI", [n], [z])[0], 0)
        fs = {f["id"]: f for f in published_formulas()}
        expected = 56 ** (1 / 3) * (
            0.94 - 0.4 * 4 / 56 ** (4 / 3) - 0.167 * (4 / 56) ** 2
        ) * math.exp(1.14 / 56) + 5.208 * expected_q / 56 ** (1 / 3)
        self.assertAlmostEqual(
            evaluate(fs["A37_DZ_R_correlated"]["expression"], [30], [26])[0], expected, places=12
        )

    def test_spherical_macro_is_not_full_mass_prediction(self):
        fs = {f["id"]: f for f in published_formulas()}
        f = fs["A41_LSD_spherical_macro"]
        n, z = 30, 26
        a = n + z
        i = (n - z) / a
        expected = -(
            -15.4920 * (1 - 1.8601 * i * i) * a
            + 16.9707 * (1 - 2.2938 * i * i) * a ** (2 / 3)
            + 3.8602 * (1 + 2.3764 * i * i) * a ** (1 / 3)
            + 3 * 1.4399764 * z * z / (5 * 1.21725 * a ** (1 / 3))
            - 0.9181 * z * z / a
        )
        self.assertAlmostEqual(evaluate(f["expression"], [n], [z])[0], expected, places=10)
        self.assertEqual(f["recovery_kind"], "published_analytic_reference")
        _, rows, _ = get_task(ROOT, f["id"])
        self.assertTrue(all(r["observed_y"] is None for r in rows))

    def test_no_fabricated_spectroscopy_observations(self):
        task, rows, _ = get_task(ROOT, "A35_yrast_E9plus")
        self.assertGreater(len(rows), 100)
        self.assertEqual(task["observed_context_rows"], 0)
        self.assertTrue(all(r["observed_y"] is None and r["source"] == "AME2020" for r in rows))
        coverage = json.loads((ROOT / "coverage.json").read_text())
        self.assertFalse(next(c for c in coverage if c["observable"] == "E9plus")["admitted"])

    def test_model_anchored_absolute_radii_excluded(self):
        _, rows, _ = get_task(ROOT, "B10_Rch")
        self.assertEqual(len(rows), 812)
        self.assertFalse({75, 84, 86, 87, 88, 96}.intersection(r["Z"] for r in rows))


class TemporalTests(unittest.TestCase):
    def test_measured_vintage_holdout_and_old_labels(self):
        _, rows, splits = get_task(ROOT, "T01_B")
        masks = splits["ame2016_to_2020"]["partitions"]
        self.assertEqual(len(masks["test"]), 71)
        old = read_masses(ROOT / "source_snapshots", "AME2016")["B"]
        new = read_masses(ROOT / "source_snapshots", "AME2020")["B"]
        test = set(masks["test"])
        changed = 0
        for row in rows:
            key = row["N"], row["Z"]
            if row["sample_id"] in test:
                self.assertNotIn(key, old)
                self.assertEqual(row["y"], new[key]["y"])
                self.assertEqual(row["source"], "AME2020")
            else:
                self.assertEqual(row["source"], "AME2016")
                self.assertEqual(row["y"], old[key]["y"])
                if key in new and abs(old[key]["y"] - new[key]["y"]) > 0.0001:
                    changed += 1
        self.assertGreater(changed, 100)

    def test_cross_vintage_dependency_purge(self):
        old = {(10, 10): record(10, 10, 1, None, "AME2016", "old", ["AME2016:ME:10:10"])}
        new = {
            (11, 10): record(
                11, 10, 2, None, "AME2020", "new", ["AME2020:ME:10:10", "AME2020:ME:11:10"]
            )
        }
        rows = temporal_rows(old, new)
        split = make_temporal_split(rows)
        self.assertEqual(split["partitions"]["purged"], ["N010Z010"])
        self.assertEqual(split["partitions"]["test"], ["N011Z010"])
        validate_split(rows, split, "ame2016_to_2020")

    def test_all_nine_temporal_tasks_have_one_historical_split(self):
        tasks = [t for t in load_bank(ROOT)["tasks"] if t["panel"] == "historical_new_measurements"]
        self.assertEqual(len(tasks), 9)
        for task in tasks:
            self.assertEqual(task["enabled_splits"], ["ame2016_to_2020"])
            _, train = partition(ROOT, task["id"], "ame2016_to_2020", "train")
            _, test = partition(ROOT, task["id"], "ame2016_to_2020")
            self.assertTrue(all(r["source"].startswith("AME2016") for r in train))
            self.assertTrue(all(r["source"].startswith("AME2020") for r in test))
            self.assertFalse(
                {d for r in train for d in r["dependencies"]}.intersection(
                    d for r in test for d in r["dependencies"]
                )
            )


class MechanismTests(unittest.TestCase):
    def test_templates_instances_and_confirmation_roles(self):
        controls = control_formulas()
        self.assertEqual(len(controls), 48)
        self.assertEqual(len({f["structure_group"] for f in controls}), 16)
        self.assertEqual(
            Counter(f["evidence_role"] for f in controls), {"development": 12, "confirmation": 36}
        )
        self.assertEqual(sum(f["confirmation_axis"] == "family_composition" for f in controls), 12)
        self.assertEqual(controls, control_formulas())
        self.assertTrue(
            all(f["status"] == "synthetic_control_not_an_empirical_law" for f in controls)
        )

    def test_discrete_pairing_and_underflow_are_physically_defined(self):
        f = next(f for f in control_formulas() if f["id"] == "S05_pairing_power_01")
        y = evaluate(f["expression"], [30, 31, 31], [26, 27, 26])
        self.assertGreater(y[0], 0)
        self.assertLess(y[1], 0)
        self.assertEqual(y[2], 0)
        self.assertEqual(evaluate("exp(-100000)", [30], [26])[0], 0)
        _, rows, _ = get_task(ROOT, f["id"])
        self.assertTrue(
            all(
                r["observed_y"] is None and r["source"] == "NuclearBench-designed-control"
                for r in rows
            )
        )

    def test_inventory_exposes_related_instances(self):
        report = summary(load_bank(ROOT))
        self.assertEqual(report["task_instances"], 151)
        self.assertEqual(report["panels"]["published_empirical"]["task_instances"], 46)
        self.assertEqual(
            report["panels"]["published_empirical"]["declared_structure_groups"][
                "valence_spectroscopy"
            ],
            22,
        )
        self.assertEqual(
            len(report["panels"]["synthetic_mechanism_control"]["declared_structure_groups"]), 16
        )


class DocumentationTests(unittest.TestCase):
    def test_inventory_documents_match_frozen_artifacts(self):
        from nuclearbench.documentation import render

        for name, text in render(ROOT).items():
            self.assertEqual((ROOT / name).read_text(), text)


class AggregationTests(unittest.TestCase):
    def fixture(self):
        tasks = [
            {
                "id": t,
                "panel": "p",
                "enabled_splits": ["s"],
                "evidence_role": "evaluation",
                "category": "expression_recovery",
                "structure_group": g,
            }
            for t, g in (("a", "g1"), ("b", "g1"), ("c", "g2"))
        ]
        bank = {"tasks": tasks, "model_seeds": [7], "noise_levels": [0]}
        runs = [
            {
                "model": "m",
                "task": t,
                "seed": 7,
                "split": "s",
                "status": "scored",
                "nrmse_train_std": e,
                "symbolic_status": "proved_equal" if t == "c" else "unproved",
                "numeric_agreement": t == "c",
                "bank_checksums_sha256": "fixture",
            }
            for t, e in (("a", 2), ("b", 2), ("c", 10))
        ]
        return bank, runs

    def test_equal_groups_not_equal_instance_count(self):
        bank, runs = self.fixture()
        bank["tasks"].append(
            dict(bank["tasks"][0], id="development_only", evidence_role="development")
        )
        runs.append(dict(runs[0], task="development_only", nrmse_train_std=999))
        result = aggregate(bank, runs, "p", "s", ["m"], expected_digest="fixture")["models"]["m"]
        self.assertEqual(result["equal_group_summary"]["normalized_error"], 6)
        self.assertEqual(result["equal_group_summary"]["symbolic_recovery"], 0.5)
        self.assertTrue(result["complete"])

    def test_missing_failed_and_duplicate_runs_remain_visible(self):
        bank, runs = self.fixture()
        result = aggregate(bank, runs[:-1], "p", "s", ["m"])["models"]["m"]
        self.assertFalse(result["complete"])
        self.assertIsNone(result["equal_group_summary"]["normalized_error"])
        # A terminal failure must not inherit success flags from an earlier candidate.
        runs[-1]["status"] = "failed"
        result = aggregate(bank, runs, "p", "s", ["m"])["models"]["m"]
        self.assertEqual(result["terminal_failures"], 1)
        self.assertIsNone(result["equal_group_summary"]["normalized_error"])
        self.assertEqual(result["equal_group_summary"]["symbolic_recovery"], 0)
        self.assertEqual(result["equal_group_summary"]["numerical_agreement"], 0)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            aggregate(bank, runs + [runs[0]], "p", "s", ["m"])
        with self.assertRaisesRegex(ValueError, "different"):
            aggregate(bank, runs, "p", "s", ["m"], expected_digest="other")


if __name__ == "__main__":
    unittest.main()
