import contextlib
import csv
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from nuclearbench.bank import get_task, load_bank
from nuclearbench.cli import export
from nuclearbench.expressions import evaluate
from nuclearbench.external_math import (
    apply_transform,
    export_expression,
    integer_epochs,
    native_evaluate,
    native_expression,
    transform,
)
from nuclearbench.external_prepare import payload
from nuclearbench.external_profiles import requests
from nuclearbench.external_solvers import Candidate
from nuclearbench.external_worker import choose, run
from nuclearbench.scoring import recover
from nuclearbench.sources import digest

ROOT = Path(__file__).resolve().parents[1]


@contextlib.contextmanager
def inside(path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class ExternalCampaignTests(unittest.TestCase):
    def test_integral_upstream_epoch_schedule_preserves_counts(self):
        for value in (4000, 2000.0, np.int64(60), np.float64(30)):
            self.assertEqual(integer_epochs(value), value)
            self.assertIsInstance(integer_epochs(value), int)
        for value in (True, 0, -1, 1.5, float("nan"), float("inf"), "4000"):
            with self.assertRaises(ValueError):
                integer_epochs(value)

    def test_compact_affine_quartic_preserves_native_predictions(self):
        n = np.asarray([12.0, 21.0, 40.0, 45.0, 60.0])
        z = np.asarray([8.0, 12.0, 10.0, 25.0, 40.0])
        x = np.column_stack((n, z))
        state = transform(x, n + 2 * z, "AI_Feynman", ["N", "Z"])
        native = "0.3*x0**4 + 0.07*x0*x1**3 + x1**2 + 1.2"
        expression = export_expression(native, ["N", "Z"], state)
        target = state["y_scale"] * native_evaluate(native, apply_transform(x, state))
        np.testing.assert_allclose(evaluate(expression, n, z), target, rtol=1e-10, atol=1e-9)

    def test_complete_requested_matrix_and_product_exclusion(self):
        bank = load_bank(ROOT)
        matrix = list(requests(bank))
        expected = sum(
            len(t["enabled_splits"])
            * 2
            * 5
            * (3 * 3 if t["category"] == "expression_recovery" else 7)
            for t in bank["tasks"]
        )
        self.assertEqual(len(matrix), expected)
        self.assertEqual(len(matrix), 79630)
        self.assertEqual({r["task"] for r in matrix}, {t["id"] for t in bank["tasks"]})
        self.assertFalse({"MySR", "NuSR"} & {r["model"] for r in matrix})
        self.assertEqual({r["seed"] for r in matrix}, {7, 17, 37, 73, 101})
        self.assertTrue(any(r["evidence_role"] == "development" for r in matrix))
        self.assertTrue(
            all(r["noise"] == 0 for r in matrix if r["category"] != "expression_recovery")
        )

    def test_payload_has_no_test_labels_and_noise_matches_original_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.npz"
            payload(ROOT, "A04_R_A", "iid101", "raw", 0.05, path)
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                export(
                    SimpleNamespace(
                        root=ROOT,
                        task="A04_R_A",
                        split="iid101",
                        partition="train",
                        features="raw",
                        noise=0.05,
                        include_target=False,
                    )
                )
            expected = {
                r["sample_id"]: float(r["y"])
                for r in csv.DictReader(io.StringIO(stream.getvalue()))
            }
            _, _, splits = get_task(ROOT, "A04_R_A")
            ids = splits["iid101"]["partitions"]["train"]
            with np.load(path) as data:
                self.assertEqual(
                    set(data.files),
                    {
                        "features",
                        "x_train",
                        "y_train",
                        "x_validation",
                        "y_validation",
                        "x_test",
                        "test_ids",
                    },
                )
                np.testing.assert_array_equal(data["y_train"], [expected[i] for i in ids])
                self.assertEqual(len(data["x_test"]), len(data["test_ids"]))
                self.assertFalse(set(ids) & set(data["test_ids"].tolist()))

    def test_ai_rank_filter_and_inverse_expression_are_training_fitted(self):
        n, z = np.asarray([12.0, 21.0, 40.0, 45.0, 60.0]), np.asarray([8.0, 12.0, 10.0, 25.0, 40.0])
        x = np.column_stack((n, z, n + z))
        state = transform(x, n + 2 * z, "AI_Feynman")
        self.assertEqual(len(state["columns"]), 2)
        expression = "1.7*x0 + 2.5*x1"
        transformed = native_evaluate(expression, apply_transform(x, state)) * state["y_scale"]
        exported = export_expression(expression, ["N", "Z", "A"], state)
        np.testing.assert_allclose(evaluate(exported, n, z), transformed, rtol=1e-12, atol=1e-12)

    def test_native_math_is_safe_and_trigonometry_is_replayable(self):
        for expression in (
            "__import__('os').system('id')",
            "x0.__class__",
            "[x0][0]",
            "sqrt(x0,x1)",
        ):
            with self.assertRaises(ValueError):
                native_expression(expression)
        x = np.asarray([[1.0, 2.0], [3.0, 4.0]])
        np.testing.assert_allclose(
            native_evaluate("Abs(x0)+sin(x1)+pi", x), x[:, 0] + np.sin(x[:, 1]) + np.pi
        )
        np.testing.assert_allclose(
            evaluate("cos(3.141592653589793*N)", [8, 9, 10], [8, 8, 8]), [1, -1, 1]
        )

    def test_ai_nuclear_coordinates_are_predeclared_and_invertible(self):
        n = np.asarray([12.0, 20.0, 40.0, 80.0, 100.0])
        z = np.asarray([8.0, 13.0, 20.0, 25.0, 50.0])
        names = ["N", "Z", "A", "I", "d"]
        x = np.column_stack([evaluate(f, n, z) for f in names])
        state = transform(x, n, "AI_Feynman", names)
        self.assertEqual(state["columns"], [2, 3])
        self.assertIn("predeclared_independent_A_I", state["column_selection"])
        np.testing.assert_allclose((x[:, 2] + x[:, 2] * x[:, 3]) / 2, n)
        np.testing.assert_allclose((x[:, 2] - x[:, 2] * x[:, 3]) / 2, z)

    def test_selection_uses_validation_and_keeps_invalid_candidates(self):
        with tempfile.TemporaryDirectory() as directory, inside(directory):
            x = np.asarray([[1.0], [2.0], [3.0]])
            state = {"mean": [0.0], "scale": [1.0], "columns": [0], "y_offset": 0.0, "y_scale": 1.0}
            candidates = [
                Candidate("train-perfect", lambda v: np.zeros(len(v))),
                Candidate("invalid", lambda v: np.full(len(v), np.nan)),
                Candidate("validation-best", lambda v: np.full(len(v), 5.0)),
            ]
            history = []
            (best, _), _ = choose(
                candidates, x, np.zeros(3), x, np.full(3, 5.0), ["N"], state, history
            )
            self.assertEqual(best.name, "validation-best")
            self.assertEqual(history[1]["status"], "invalid_candidate")
            self.assertEqual(len(history), 3)

    def test_no_reselection_after_test_domain_failure(self):
        with tempfile.TemporaryDirectory() as directory, inside(directory):
            p = Path("fit.npz").resolve()
            x = np.asarray([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]])
            np.savez_compressed(
                p,
                x_train=x,
                y_train=np.zeros(3),
                x_validation=x + 3,
                y_validation=np.zeros(3),
                x_test=np.asarray([[-100.0, -100.0]]),
                test_ids=np.asarray(["fixture"]),
                features=np.asarray(["N", "Z"]),
            )

            def solver(*args):
                yield Candidate(
                    "validation-best", lambda values: np.where(values[:, 0] < -10, np.nan, 0)
                )
                yield Candidate("alternative", lambda values: np.ones(len(values)))

            request = {
                "model": "Ridge",
                "seed": 7,
                "payload": str(p),
                "payload_sha256": digest(p),
                "profile": {},
            }
            with (
                patch.dict("nuclearbench.external_solvers.SOLVERS", {"Ridge": solver}),
                self.assertRaisesRegex(ValueError, "no reselection"),
            ):
                run(request)
            self.assertEqual(
                json.loads(Path("selected.json").read_text())["name"], "validation-best"
            )
            self.assertFalse(Path("predictions.csv").exists())

    def test_witness_domain_failure_is_not_lost_predictive_score(self):
        task, _, _ = get_task(ROOT, "A48_pairing_classical")
        rows = [
            {"sample_id": "first", "N": 20, "Z": 20, "y": 1.0},
            {"sample_id": "second", "N": 40, "Z": 30, "y": 2.0},
        ]
        with patch("nuclearbench.scoring.partition", return_value=(task, rows)):
            result = recover(ROOT, task["id"], "iid101", "log(N-16)")
        self.assertEqual(result["status"], "scored")
        self.assertTrue(np.isfinite(result["rmse"]))
        self.assertFalse(result["numeric_agreement"])
        self.assertEqual(
            result["numeric_witness_status"], "candidate_undefined_on_reference_domain"
        )


if __name__ == "__main__":
    unittest.main()
