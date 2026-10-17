"""Small arithmetic AST interpreter: expression files are never passed to eval."""

import ast
import json
import operator
import subprocess
import sys

import numpy as np

from .formulas import MACROS

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
NAMES = {"N", "Z", "A", "I", "d", "P_s", "P_m"}
EXTRA_FEATURES = ("Np", "Nn", "P", "Q_EI")
NAMES.update(EXTRA_FEATURES)
FUNCS = {"sqrt": np.sqrt, "exp": np.exp, "log": np.log, "abs": np.abs}


def parse(expression):
    if len(expression) > 4000:
        raise ValueError("Expression exceeds 4000 characters")
    tree = ast.parse(expression, mode="eval")
    nodes = list(ast.walk(tree))
    if len(nodes) > 512:
        raise ValueError("Expression exceeds 512 AST nodes")

    def check(node, depth=0):
        if depth > 64:
            raise ValueError("Expression exceeds depth limit")
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if not np.isfinite(node.value) or abs(node.value) > 1e8:
                raise ValueError("Invalid numeric constant")
        elif isinstance(node, ast.Name) and node.id in NAMES:
            pass
        elif isinstance(node, ast.BinOp) and type(node.op) in OPS:
            check(node.left, depth + 1)
            check(node.right, depth + 1)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            check(node.operand, depth + 1)
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in FUNCS
            and len(node.args) == 1
            and not node.keywords
        ):
            check(node.args[0], depth + 1)
        else:
            raise ValueError(
                "Only whitelisted arithmetic, nuclear macros and unary functions are accepted"
            )

    check(tree.body)
    return tree.body


def valence(n, z, macro):
    sets = MACROS[macro]
    vn = np.min(abs(n[:, None] - np.asarray(sets["neutron_magic"])), axis=1)
    vp = np.min(abs(z[:, None] - np.asarray(sets["proton_magic"])), axis=1)
    return np.divide(vn * vp, vn + vp, out=np.zeros_like(n, dtype=float), where=vn + vp != 0)


def valence_counts(n, z):
    sets = MACROS["standard_valence"]
    return (
        np.min(abs(z[:, None] - np.asarray(sets["proton_magic"])), axis=1),
        np.min(abs(n[:, None] - np.asarray(sets["neutron_magic"])), axis=1),
    )


def ei_fraction(count):
    boundaries = np.asarray(MACROS["Q_EI"]["boundaries"])
    index = np.clip(np.searchsorted(boundaries, count, side="right") - 1, 0, len(boundaries) - 2)
    lower, upper = boundaries[index], boundaries[index + 1]
    value = (count - lower) * (upper - count) / (upper - lower) ** 2
    return np.where((count >= boundaries[0]) & (count <= boundaries[-1]), value, 0.0)


def evaluate(expression, n, z):
    n, z = np.broadcast_arrays(np.asarray(n, dtype=float), np.asarray(z, dtype=float))
    if n.ndim != 1:
        raise ValueError("N and Z must be one-dimensional")
    values = {
        "N": n,
        "Z": z,
        "A": n + z,
        "I": (n - z) / (n + z),
        "d": (((-1.0) ** n) + ((-1.0) ** z)) / 2,
        "P_s": valence(n, z, "P_s"),
        "P_m": valence(n, z, "P_m"),
    }
    vp, vn = valence_counts(n, z)
    values.update(
        Np=vp,
        Nn=vn,
        P=np.divide(vp * vn, vp + vn, out=np.zeros_like(n), where=vp + vn != 0),
        Q_EI=ei_fraction(n) * ei_fraction(z),
    )

    def run(node):
        if isinstance(node, ast.Constant):
            return float(node.value)
        if isinstance(node, ast.Name):
            return values[node.id]
        if isinstance(node, ast.BinOp):
            return OPS[type(node.op)](run(node.left), run(node.right))
        if isinstance(node, ast.UnaryOp):
            return -run(node.operand) if isinstance(node.op, ast.USub) else run(node.operand)
        return FUNCS[node.func.id](run(node.args[0]))

    with np.errstate(over="raise", divide="raise", invalid="raise", under="ignore"):
        value = np.broadcast_to(run(parse(expression)), n.shape).astype(float)
    if not np.all(np.isfinite(value)):
        raise ValueError("Nonfinite expression output")
    return value


def complexity(expression):
    """Registered syntax cost; macro costs are protocol weights, not expanded tree sizes."""
    costs = {
        "N": 1,
        "Z": 1,
        "A": 3,
        "I": 9,
        "d": 9,
        "P_s": 67,
        "P_m": 43,
        "Np": 55,
        "Nn": 63,
        "P": 131,
        "Q_EI": 95,
    }

    def count(node):
        if isinstance(node, ast.Constant):
            return 1
        if isinstance(node, ast.Name):
            return costs[node.id]
        if isinstance(node, ast.BinOp):
            return 1 + count(node.left) + count(node.right)
        if isinstance(node, ast.UnaryOp):
            return 1 + count(node.operand)
        return 1 + count(node.args[0])

    return count(parse(expression))


def prove(left, right, timeout=5):
    parse(left)
    parse(right)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "nuclearbench.expressions", "--prove"],
            input=json.dumps([left, right]),
            text=True,
            capture_output=True,
            timeout=timeout,
            check=True,
        )
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return "unproved_timeout"
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return "unproved_error"


def _symbolic(expression):
    import sympy as sp

    n, z = sp.symbols("N Z", positive=True, integer=True)
    values = {
        "N": n,
        "Z": z,
        "A": n + z,
        "I": (n - z) / (n + z),
        "d": ((-1) ** n + (-1) ** z) / 2,
        "P_s": sp.Symbol("P_s", nonnegative=True),
        "P_m": sp.Symbol("P_m", nonnegative=True),
        **{name: sp.Symbol(name, nonnegative=True) for name in EXTRA_FEATURES},
    }
    functions = {"sqrt": sp.sqrt, "exp": sp.exp, "log": sp.log, "abs": sp.Abs}

    def run(node):
        if isinstance(node, ast.Constant):
            return sp.Rational(ast.get_source_segment(expression, node))
        if isinstance(node, ast.Name):
            return values[node.id]
        if isinstance(node, ast.BinOp):
            return OPS[type(node.op)](run(node.left), run(node.right))
        if isinstance(node, ast.UnaryOp):
            return -run(node.operand) if isinstance(node.op, ast.USub) else run(node.operand)
        return functions[node.func.id](run(node.args[0]))

    return run(parse(expression))


if __name__ == "__main__":
    import sympy as sp

    left, right = json.load(sys.stdin)
    difference = _symbolic(left) - _symbolic(right)
    print(
        json.dumps(
            "proved_equal" if difference == 0 or sp.simplify(difference) == 0 else "unproved"
        )
    )
