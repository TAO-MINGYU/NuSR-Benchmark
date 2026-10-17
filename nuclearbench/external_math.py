"""Safe native-expression conversion and train-only affine preprocessing."""

import ast
import math
import re

import numpy as np

FUNCTIONS = {
    "sqrt": np.sqrt,
    "exp": np.exp,
    "log": np.log,
    "abs": np.abs,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "asin": np.arcsin,
    "acos": np.arccos,
    "atan": np.arctan,
}


def integer_epochs(value):
    """Preserve integral epoch schedules passed through upstream Python division."""
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float, np.integer, np.floating))
        or not math.isfinite(value)
        or value <= 0
        or int(value) != value
    ):
        raise ValueError("NN epoch count must be a positive integral value")
    return int(value)


def native_expression(expression):
    """Parse native mathematical output without executing Python expressions."""
    expression = str(expression).replace("^", "**")
    expression = re.sub(r"\bAbs\b", "abs", expression)
    expression = re.sub(r"\bln\b", "log", expression)
    expression = re.sub(r"\bpi\b", repr(math.pi), expression)
    expression = re.sub(r"\bE\b", repr(math.e), expression)
    tree = ast.parse(expression, mode="eval")
    nodes = list(ast.walk(tree))
    if len(expression) > 100_000 or len(nodes) > 20_000:
        raise ValueError("Native expression exceeds declared export limit")
    for node in nodes:
        if isinstance(
            node,
            (
                ast.Expression,
                ast.Load,
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.Pow,
                ast.USub,
                ast.UAdd,
            ),
        ):
            continue
        if (
            isinstance(node, ast.Constant)
            and type(node.value) in (int, float)
            and math.isfinite(node.value)
        ):
            continue
        if isinstance(node, ast.Name) and (re.fullmatch(r"x\d+", node.id) or node.id in FUNCTIONS):
            continue
        if isinstance(node, (ast.BinOp, ast.UnaryOp)):
            continue
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in FUNCTIONS
            and len(node.args) == 1
            and not node.keywords
        ):
            continue
        raise ValueError("Unsupported native expression syntax: " + type(node).__name__)
    return tree.body


def native_evaluate(expression, x):
    node = native_expression(expression)
    operators = {
        ast.Add: np.add,
        ast.Sub: np.subtract,
        ast.Mult: np.multiply,
        ast.Div: np.divide,
        ast.Pow: np.power,
    }

    def visit(item):
        if isinstance(item, ast.Constant):
            return float(item.value)
        if isinstance(item, ast.Name) and re.fullmatch(r"x\d+", item.id):
            return x[:, int(item.id[1:])]
        if isinstance(item, ast.UnaryOp):
            value = visit(item.operand)
            return -value if isinstance(item.op, ast.USub) else value
        if isinstance(item, ast.BinOp):
            return operators[type(item.op)](visit(item.left), visit(item.right))
        if isinstance(item, ast.Call):
            return FUNCTIONS[item.func.id](visit(item.args[0]))
        raise ValueError("Invalid expression node")

    with np.errstate(over="raise", divide="raise", invalid="raise", under="ignore"):
        result = np.broadcast_to(visit(node), (len(x),)).astype(float)
    if not np.all(np.isfinite(result)):
        raise ValueError("Nonfinite native prediction")
    return result


def transform(x, y, model, feature_names=None):
    """Return training-fitted transform; AF covariance needs independent columns."""
    mean = np.zeros(x.shape[1])
    scale = np.ones(x.shape[1])
    columns = np.arange(x.shape[1])
    if model not in {"PySR", "Operon"}:
        mean = x.mean(axis=0)
        scale = x.std(axis=0)
        scale[scale < 1e-12] = 1.0
    selection = "all_available_columns"
    if model == "AI_Feynman":
        from scipy.linalg import qr

        # Derived nuclear columns live on an N/Z manifold. Off-manifold partial
        # derivatives are not identifiable from these observations. Use the
        # invertible continuous coordinates A,I for this method's native
        # nuclear representation, rather than eleven nominally independent
        # variables. The raw mode keeps N,Z. No targets select these columns.
        if feature_names is not None and "A" in feature_names and "I" in feature_names:
            columns = np.asarray([feature_names.index("A"), feature_names.index("I")])
            selection = "predeclared_independent_A_I_coordinates_then_training_rank_filter"
        else:
            selection = "raw_coordinates_then_training_rank_filter"
        z = ((x - mean) / scale)[:, columns]
        _, r, pivot = qr(z, mode="economic", pivoting=True)
        diagonal = abs(np.diag(r))
        rank = int(np.sum(diagonal > max(float(diagonal.max(initial=0)), 1.0) * 1e-10))
        if rank == 0:
            raise ValueError("AI Feynman has no nonconstant independent training coordinate")
        columns = columns[np.sort(pivot[:rank])]
    offset = 0.0 if model in {"PySR", "Operon", "AI_Feynman"} else float(y.mean())
    centered = y - offset
    yscale = float(np.sqrt(np.mean(centered * centered)))
    if yscale < 1e-12:
        yscale = 1.0
    return {
        "model": model,
        "mean": mean.tolist(),
        "scale": scale.tolist(),
        "columns": columns.tolist(),
        "y_offset": offset,
        "y_scale": yscale,
        "column_selection": selection,
    }


def apply_transform(x, state):
    return ((x - np.asarray(state["mean"])) / np.asarray(state["scale"]))[:, state["columns"]]


def export_expression(expression, feature_names, state):
    node = native_expression(expression)
    mapping = {}
    for index, col in enumerate(state["columns"]):
        feature = feature_names[col]
        mean, scale = state["mean"][col], state["scale"][col]
        text = feature
        if mean != 0:
            text = f"({text}-{mean!r})"
        if scale != 1:
            text = f"({text}/{scale!r})"
        mapping["x" + str(index)] = ast.parse(text, mode="eval").body

    if state.get("model") == "AI_Feynman" and len(state["columns"]) <= 2:
        return _compact_affine_polynomials(node, feature_names, state)

    class Substitute(ast.NodeTransformer):
        def visit_Name(self, item):
            return mapping.get(item.id, item)

    body = ast.unparse(Substitute().visit(node))
    if state["y_scale"] != 1:
        body = f"({state['y_scale']!r}*({body}))"
    if state["y_offset"] != 0:
        body = f"({state['y_offset']!r}+({body}))"
    return body


def _compact_affine_polynomials(node, feature_names, state):
    """Algebraic export, with expansion bounded to two variables and degree four."""
    import operator

    import sympy as sp

    symbols = {name: sp.Symbol(name, real=True) for name in feature_names}
    active = [symbols[feature_names[c]] for c in state["columns"]]
    functions = {name: getattr(sp, name) for name in FUNCTIONS if name != "abs"}
    functions["abs"] = sp.Abs
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def number(value):
        return sp.Float(repr(float(value)), 17)

    def visit(item):
        if isinstance(item, ast.Constant):
            return (sp.Integer(item.value) if type(item.value) is int else number(item.value)), 0
        if isinstance(item, ast.Name):
            col = state["columns"][int(item.id[1:])]
            return (symbols[feature_names[col]] - number(state["mean"][col])) / number(
                state["scale"][col]
            ), 1
        if isinstance(item, ast.UnaryOp):
            value, degree = visit(item.operand)
            return (-value if isinstance(item.op, ast.USub) else value), degree
        if isinstance(item, ast.Call):
            value, _ = visit(item.args[0])
            return functions[item.func.id](value), None
        left, dl = visit(item.left)
        right, dr = visit(item.right)
        degree = None
        if dl is not None and dr is not None:
            if isinstance(item.op, (ast.Add, ast.Sub)):
                degree = max(dl, dr)
            elif isinstance(item.op, ast.Mult):
                degree = dl + dr
            elif isinstance(item.op, ast.Div) and dr == 0:
                degree = dl
            elif (
                isinstance(item.op, ast.Pow)
                and isinstance(item.right, ast.Constant)
                and 0 <= item.right.value <= 4
                and int(item.right.value) == item.right.value
            ):
                degree = dl * int(item.right.value)
                right = sp.Integer(int(item.right.value))
        value = operations[type(item.op)](left, right)
        if degree is not None and degree <= 4:
            value = sp.Poly(value, *active).as_expr()
        return value, degree

    result, degree = visit(node)
    result = number(state["y_offset"]) + number(state["y_scale"]) * result
    if degree is not None and degree <= 4:
        result = sp.Poly(result, *active).as_expr()
    if result.has(sp.I, sp.zoo, sp.oo, sp.nan):
        raise ValueError("Nonreal or nonfinite symbolic export")
    result = result.xreplace({sp.pi: number(math.pi), sp.E: number(math.e)})
    return str(result).replace("Abs(", "abs(")
