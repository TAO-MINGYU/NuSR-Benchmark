"""Preregistered external-baseline recipes; no task answers enter this module."""

SEEDS = (7, 17, 37, 73, 101)
SR_MODELS = ("PySR", "Operon", "AI_Feynman")
PREDICTORS = ("GPR", "LightGBM", "MLP_ensemble", "Ridge")
MODES = ("raw", "nuclear")
FEATURES = ("N", "Z", "A", "I", "d", "P_s", "P_m", "Np", "Nn", "P", "Q_EI")
# The CLI exports eleven columns in nuclear mode (including N/Z).
UNARY = ("sqrt", "exp", "log", "abs", "sin", "cos", "tan", "asin", "acos", "atan")

PROFILES = {
    "PySR": {
        "niterations": 1_000_000,
        "max_evals": 5_000_000,
        "populations": 8,
        "population_size": 100,
        "ncycles_per_iteration": 380,
        "maxsize": 128,
        "maxdepth": 32,
        "optimizer_iterations": 25,
        "optimizer_nrestarts": 2,
        "binary_operators": ["+", "-", "*", "/", "^"],
        "constraints": {"^": [-1, 1]},
        "unary_operators": list(UNARY),
        "precision": 64,
        "parallelism": "serial",
        "deterministic": True,
        "batching": False,
        "model_selection": "accuracy",
        "progress": False,
        "verbosity": 0,
        "warm_start": False,
    },
    "Operon": {
        "population_size": 1000,
        "pool_size": 1000,
        "generations": 1_000_000,
        "max_evaluations": 5_000_000,
        "objectives": ["mse", "length"],
        "optimizer": "lm",
        "optimizer_iterations": 25,
        "local_search_probability": 1.0,
        "lamarckian_probability": 1.0,
        "max_length": 128,
        "max_depth": 32,
        "initialization_max_length": 12,
        "allowed_symbols": "add,sub,mul,div,pow,constant,variable," + ",".join(UNARY),
        "model_selection_criterion": "mean_squared_error",
        "n_threads": 1,
        "max_time": None,
        "epsilon": 0.0,
        "warm_start": False,
    },
    "AI_Feynman": {
        "BF_try_time": 60,
        "BF_ops_file_type": "14ops.txt",
        "polyfit_deg": 4,
        "NN_epochs": 4000,
        "vars_name": [],
        "test_percentage": 0,
    },
    "GPR": {
        "kernels": [
            "rbf",
            "matern15",
            "matern25",
            "linear_rbf",
            "linear_matern15",
            "linear_matern25",
        ],
        "n_restarts_optimizer": 3,
        "alpha": 1e-8,
        "amplitude_bounds": [1e-4, 1e4],
        "length_scale_bounds": [1e-2, 1e3],
        "noise_bounds": [1e-8, 10.0],
    },
    "LightGBM": {
        "num_leaves": [7, 15, 31, 63],
        "min_child_samples": [5, 20, 50],
        "n_estimators": 4000,
        "learning_rate": 0.03,
        "reg_lambda": 1.0,
        "early_stopping_rounds": 100,
        "n_jobs": 1,
        "deterministic": True,
        "force_col_wise": True,
        "verbosity": -1,
    },
    "MLP_ensemble": {
        "hidden_layers": [[64, 64], [128, 128], [128, 64, 32]],
        "alpha": [1e-4, 1e-2],
        "members": 5,
        "max_epochs": 2000,
        "validation_every": 10,
        "patience_checks": 20,
        "learning_rate_init": 1e-3,
        "batch_size": 64,
        "activation": "tanh",
    },
    "Ridge": {"alpha": [0.0, 1e-6, 1e-3, 0.1, 1.0, 10.0, 100.0]},
}

DEPENDENCIES = {
    "numpy": "2.4.6",
    "scipy": "1.17.1",
    "scikit-learn": "1.9.1",
    "sympy": "1.14.0",
    "lightgbm": "4.7.0",
    "pyoperon": "0.6.2",
    "pysr": "2.7.0",
    "psutil": "7.2.2",
}


def requests(bank):
    """Every admitted task/split; keep development tasks explicitly labeled."""
    for task in bank["tasks"]:
        models = SR_MODELS if task["category"] == "expression_recovery" else SR_MODELS + PREDICTORS
        noises = (0.0, 0.01, 0.05) if task["category"] == "expression_recovery" else (0.0,)
        for split in task["enabled_splits"]:
            for mode in MODES:
                for noise in noises:
                    for seed in SEEDS:
                        for model in models:
                            yield {
                                "task": task["id"],
                                "split": split,
                                "mode": mode,
                                "noise": noise,
                                "seed": seed,
                                "model": model,
                                "panel": task["panel"],
                                "evidence_role": task["evidence_role"],
                                "category": task["category"],
                            }
