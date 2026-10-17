"""Native solver calls. Inputs contain training and validation data only."""

import copy
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .external_math import native_evaluate


@dataclass
class Candidate:
    name: str
    predict: object
    expression: str | None = None
    model: object = None
    detail: dict | None = None


def pysr_candidates(x, y, xv, yv, seed, profile, details):
    from pysr import PySRRegressor
    from pysr.julia_import import jl

    model = PySRRegressor(
        **profile,
        random_state=seed,
        output_directory=str(Path("pysr-native").resolve()),
        run_id="search",
    )
    model.fit(x, y, variable_names=[f"x{i}" for i in range(x.shape[1])])
    details["effective_options"] = {k: repr(v) for k, v in model.get_params().items()}
    details["julia_version"] = str(jl.seval("VERSION"))
    details["core_version"] = str(jl.seval("pkgversion(SymbolicRegression)"))
    details["core_path"] = str(jl.seval("pathof(SymbolicRegression)"))
    details["work_semantics"] = (
        "native max_evals; optimizer and initialization costs measured separately by process CPU"
    )
    for index, row in model.equations_.iterrows():
        expression = str(row["sympy_format"])
        yield Candidate(
            str(index),
            lambda values, i=index: model.predict(values, index=i),
            expression,
            detail={
                "native_complexity": int(row["complexity"]),
                "training_loss": float(row["loss"]),
            },
        )


def operon_candidates(x, y, xv, yv, seed, profile, details):
    import pyoperon as op
    from pyoperon.sklearn import SymbolicRegressor

    dtype = str(np.asarray(op.Dataset(np.asfortranarray(x[:2])).Values).dtype)
    if dtype != "float64":
        raise RuntimeError("Registered Operon baseline requires the double-precision source build")
    details["native_scalar_dtype"] = dtype
    details["native_build"] = op.Version()
    model = SymbolicRegressor(**profile, random_state=seed)
    model.fit(x, y)
    details["effective_options"] = model.get_params()
    details["work_counts"] = model.stats_
    for index, row in enumerate(model.pareto_front_):
        # The sklearn wrapper's six-digit formatter is unsuitable for recovery.
        expression = op.InfixFormatter.Format(row["tree"], model.variables_, 17)
        import re

        variables = {name: f"x{i}" for i, name in enumerate(model.variables_.values())}
        expression = re.sub(
            r"\b[A-Za-z_]\w*\b", lambda m, v=variables: v.get(m[0], m[0]), expression
        )
        tree = row["tree"]
        yield Candidate(
            str(index),
            lambda values, t=tree: model.evaluate_model(t, values),
            expression,
            detail={"native_length": int(row["length"])},
        )


def aifeynman_candidates(x, y, xv, yv, seed, profile, details):
    import importlib
    import random

    import torch
    from aifeynman import run_aifeynman
    from aifeynman.get_pareto import ParetoSet

    from .external_math import integer_epochs

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    Path("input").mkdir()
    np.savetxt("input/train.txt", np.column_stack((x, y)))
    # Observe only the root Pareto set; recursive reduced problems are not
    # predictions of the original target. This hook does not alter points.
    root = [None]
    original_init, original_add = ParetoSet.__init__, ParetoSet.add
    run_module = importlib.import_module("aifeynman.S_run_aifeynman")
    original_nn = run_module.NN_train
    details["nn_invocations"] = []

    def typed_nn(pathdir, filename, epochs=1000, *args, **kwargs):
        # Upstream passes NN_epochs/2 to range() through its pretrained branch.
        # Converting an exactly integral float preserves the intended workload;
        # it does not shorten the schedule or alter numerical model code.
        count = integer_epochs(epochs)
        with open(pathdir + filename) as stream:
            rows = sum(bool(line.strip()) for line in stream)
        details["nn_invocations"].append(
            {
                "requested_epochs": epochs,
                "integral_epochs": count,
                "rows": rows,
                "small_data_multiplier": 3 if rows < 5000 else 1,
                "learning_rate_stages": kwargs.get("N_red_lr", 4),
                "pretrained": bool(kwargs.get("pretrained_path")),
            }
        )
        Path("nn-invocations.json").write_text(json.dumps(details["nn_invocations"], indent=2))
        return original_nn(pathdir, filename, count, *args, **kwargs)

    def initialize(instance):
        original_init(instance)
        if root[0] is None:
            root[0] = instance

    def add(instance, point):
        result = original_add(instance, point)
        if instance is root[0]:
            Path("native-frontier.json").write_text(
                json.dumps(
                    [
                        {
                            "expression": str(p[2]),
                            "native_complexity": float(p[0]),
                            "native_error": float(p[1]),
                        }
                        for p in instance.get_pareto_points()
                    ],
                    allow_nan=True,
                )
            )
        return result

    ParetoSet.__init__, ParetoSet.add = initialize, add
    run_module.NN_train = typed_nn
    try:
        run_aifeynman(str(Path("input").resolve()) + "/", "train.txt", **profile)
    finally:
        ParetoSet.__init__, ParetoSet.add = original_init, original_add
        run_module.NN_train = original_nn
    if root[0] is None:
        raise ValueError("AI Feynman did not construct a root Pareto set")
    details["effective_options"] = profile
    details["compatibility"] = (
        "NumPy1.23.5; exactly-integral pretrained NN epoch float converted to int"
    )
    details["work_semantics"] = (
        "BF_try_time is per native brute-force call; source has additional 600s "
        "compositionality calls and small-data NN epoch multiplier; no global fit timeout"
    )
    for index, point in enumerate(root[0].get_pareto_points()):
        expression = str(point[2])
        yield Candidate(
            str(index),
            lambda values, e=expression: native_evaluate(e, values),
            expression,
            detail={"native_complexity": float(point[0])},
        )


def gpr_candidates(x, y, xv, yv, seed, profile, details):
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import (
        RBF,
        ConstantKernel,
        DotProduct,
        Matern,
        WhiteKernel,
    )

    for index, name in enumerate(profile["kernels"]):
        if name.endswith("rbf"):
            base = RBF(np.ones(x.shape[1]), tuple(profile["length_scale_bounds"]))
        else:
            base = Matern(
                np.ones(x.shape[1]),
                tuple(profile["length_scale_bounds"]),
                nu=1.5 if name.endswith("15") else 2.5,
            )
        kernel = ConstantKernel(1.0, tuple(profile["amplitude_bounds"])) * base
        if name.startswith("linear"):
            kernel += DotProduct(1.0, (1e-4, 1e4))
        kernel += WhiteKernel(1e-3, tuple(profile["noise_bounds"]))
        model = GaussianProcessRegressor(
            kernel=kernel,
            alpha=profile["alpha"],
            normalize_y=False,
            random_state=seed + index,
            n_restarts_optimizer=profile["n_restarts_optimizer"],
        )
        model.fit(x, y)
        yield Candidate(
            name,
            model.predict,
            model=model,
            detail={
                "kernel": str(model.kernel_),
                "log_marginal_likelihood": float(model.log_marginal_likelihood_value_),
            },
        )


def lightgbm_candidates(x, y, xv, yv, seed, profile, details):
    import lightgbm as lgb

    options = {
        k: v
        for k, v in profile.items()
        if k not in {"num_leaves", "min_child_samples", "early_stopping_rounds"}
    }
    for leaves in profile["num_leaves"]:
        for child in profile["min_child_samples"]:
            model = lgb.LGBMRegressor(
                **options,
                objective="regression",
                random_state=seed,
                num_leaves=leaves,
                min_child_samples=child,
            )
            model.fit(
                x,
                y,
                eval_set=[(xv, yv)],
                eval_metric="l2",
                callbacks=[lgb.early_stopping(profile["early_stopping_rounds"], verbose=False)],
            )
            yield Candidate(
                f"leaves{leaves}-child{child}",
                model.predict,
                model=model,
                detail={
                    "best_iteration": int(model.best_iteration_),
                    "num_leaves": leaves,
                    "min_child_samples": child,
                },
            )


@dataclass
class Ensemble:
    members: list

    def predict(self, x):
        return np.mean([m.predict(x) for m in self.members], axis=0)


def mlp_candidates(x, y, xv, yv, seed, profile, details):
    from sklearn.neural_network import MLPRegressor

    for layers in profile["hidden_layers"]:
        for alpha in profile["alpha"]:
            members, histories = [], []
            for index in range(profile["members"]):
                model = MLPRegressor(
                    hidden_layer_sizes=tuple(layers),
                    alpha=alpha,
                    activation=profile["activation"],
                    solver="adam",
                    learning_rate_init=profile["learning_rate_init"],
                    batch_size=min(profile["batch_size"], len(y)),
                    random_state=seed + index * 1009,
                    shuffle=True,
                    early_stopping=False,
                    max_iter=1,
                )
                best, best_error, stale, history = None, float("inf"), 0, []
                for epoch in range(1, profile["max_epochs"] + 1):
                    model.partial_fit(x, y)
                    if epoch % profile["validation_every"]:
                        continue
                    error = float(np.mean((model.predict(xv) - yv) ** 2))
                    history.append({"epoch": epoch, "validation_mse": error})
                    if np.isfinite(error) and error < best_error:
                        best, best_error, stale = copy.deepcopy(model), error, 0
                    else:
                        stale += 1
                    if stale >= profile["patience_checks"]:
                        break
                if best is None:
                    raise ValueError("MLP member has no finite validation checkpoint")
                members.append(best)
                histories.append(history)
            ensemble = Ensemble(members)
            yield Candidate(
                f"layers{layers}-alpha{alpha}",
                ensemble.predict,
                model=ensemble,
                detail={"layers": layers, "alpha": alpha, "histories": histories},
            )


def ridge_candidates(x, y, xv, yv, seed, profile, details):
    from sklearn.linear_model import LinearRegression, Ridge

    for alpha in profile["alpha"]:
        model = LinearRegression() if alpha == 0 else Ridge(alpha=alpha)
        model.fit(x, y)
        yield Candidate(f"alpha{alpha}", model.predict, model=model, detail={"alpha": alpha})


SOLVERS = {
    "PySR": pysr_candidates,
    "Operon": operon_candidates,
    "AI_Feynman": aifeynman_candidates,
    "GPR": gpr_candidates,
    "LightGBM": lightgbm_candidates,
    "MLP_ensemble": mlp_candidates,
    "Ridge": ridge_candidates,
}
