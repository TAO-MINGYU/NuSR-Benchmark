"""Node-local runtime acceptance, performed before any scientific fit."""

import argparse
import json
import sys
from importlib import metadata
from pathlib import Path

import numpy as np


def probe(kind):
    if kind == "main":
        import lightgbm
        import pyoperon
        import pysr
        import sklearn
        from pysr.julia_import import jl

        dtype = str(
            np.asarray(pyoperon.Dataset(np.asfortranarray([[1.0, 2.0], [3.0, 4.0]])).Values).dtype
        )
        if dtype != "float64":
            raise RuntimeError("The registered Operon baseline requires its verified fp64 build")
        return {
            "python": sys.version,
            "numpy": np.__version__,
            "pysr": pysr.__version__,
            "pyoperon": metadata.version("pyoperon"),
            "operon_scalar": dtype,
            "operon_build": pyoperon.Version(),
            "lightgbm": lightgbm.__version__,
            "sklearn": sklearn.__version__,
            "julia": str(jl.seval("VERSION")),
            "core": str(jl.seval("pkgversion(SymbolicRegression)")),
            "core_path": str(jl.seval("pathof(SymbolicRegression)")),
        }
    import aifeynman
    import torch
    from aifeynman._symbolic_regress_mdl3 import go

    assert callable(go)
    if np.__version__ != "1.23.5" or torch.cuda.is_available():
        raise RuntimeError("AI Feynman requires its CPU/NumPy1.23.5 compatibility environment")
    return {
        "python": sys.version,
        "numpy": np.__version__,
        "torch": torch.__version__,
        "aifeynman": metadata.version("aifeynman"),
        "module": aifeynman.__file__,
        "fortran_extension": "loaded",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["main", "aifeynman"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(probe(args.kind), indent=2))
