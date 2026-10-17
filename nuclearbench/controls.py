"""Designed nuclear-mechanism controls, explicitly not published empirical laws."""

import hashlib

from .formulas import entry

# Each template has three preregistered numeric instantiations, not three new families.
# Ranges and structure never depend on observed target values or NuSR performance.
TEMPLATES = [
    ("isospin_quadratic", "smooth_isospin", "a*(N-Z)**2/A", {"a": (15, 30)}, ["symmetry"]),
    (
        "surface_symmetry",
        "smooth_isospin",
        "(a*A**(2/3)+b*A**(1/3))*I**2",
        {"a": (10, 25), "b": (2, 8)},
        ["surface", "symmetry"],
    ),
    ("wigner_cusp", "wigner_congruence", "a*abs(N-Z)/A", {"a": (8, 24)}, ["isospin_cusp"]),
    (
        "congruence_exp",
        "wigner_congruence",
        "a*exp(-b*abs(I))",
        {"a": (5, 15), "b": (3, 7)},
        ["isospin_cusp", "exponential"],
    ),
    (
        "pairing_power",
        "discrete_pairing",
        "a*d/A**p",
        {"a": (9, 15), "p": (0.35, 0.65)},
        ["parity", "inverse_power"],
    ),
    (
        "pairing_isospin",
        "discrete_pairing",
        "a*d*(1-b*I**2)/sqrt(A)",
        {"a": (9, 15), "b": (0.5, 2)},
        ["parity", "symmetry"],
    ),
    (
        "shell_gaussian_sum",
        "shell_localization",
        "a*exp(-((N-n0)/w)**2)+b*exp(-((Z-z0)/w)**2)",
        {"a": (1, 4), "b": (1, 4), "w": (4, 9)},
        ["neutron_shell", "proton_shell"],
    ),
    (
        "shell_gaussian_joint",
        "shell_localization",
        "a*exp(-((N-n0)/w)**2-((Z-z0)/w)**2)",
        {"a": (2, 7), "w": (5, 10)},
        ["localized_shell_interaction"],
    ),
    (
        "shell_absolute_exp",
        "shell_localization",
        "a*exp(-abs(N-n0)/w)",
        {"a": (2, 7), "w": (4, 10)},
        ["shell_cusp"],
    ),
    (
        "valence_product",
        "valence_collectivity",
        "a*Np*Nn/A",
        {"a": (0.1, 0.8)},
        ["valence_product"],
    ),
    (
        "valence_saturation",
        "valence_collectivity",
        "a*P/(b+P)",
        {"a": (1, 5), "b": (1, 6)},
        ["valence", "saturation"],
    ),
    (
        "valence_isospin",
        "valence_collectivity",
        "a*Np*Nn*(1-b*I**2)/A",
        {"a": (0.1, 0.6), "b": (0.5, 2)},
        ["valence", "symmetry"],
    ),
    (
        "shell_isospin",
        "mixed_shell",
        "a*I*exp(-((N-n0)/w)**2)",
        {"a": (2, 7), "w": (5, 10)},
        ["shell", "symmetry"],
    ),
    (
        "shell_pairing",
        "mixed_shell",
        "a*d*exp(-((N-n0)/w)**2)/sqrt(A)",
        {"a": (8, 16), "w": (5, 10)},
        ["shell", "parity"],
    ),
    (
        "bulk_pairing",
        "mixed_global",
        "a*A-b*A**(2/3)-c*(N-Z)**2/A+h*d/sqrt(A)",
        {"a": (14, 17), "b": (15, 21), "c": (18, 27), "h": (9, 15)},
        ["bulk", "surface", "symmetry", "parity"],
    ),
    (
        "bulk_shell_collective",
        "mixed_global",
        "a*A-b*A**(2/3)-c*(N-Z)**2/A+h*exp(-((N-n0)/w)**2)+k*Np*Nn/A",
        {"a": (14, 17), "b": (15, 21), "c": (18, 27), "h": (2, 6), "w": (5, 10), "k": (0.1, 0.5)},
        ["bulk", "surface", "symmetry", "shell", "valence"],
    ),
]


def control_formulas():
    import re

    result = []
    closures = ((28, 20), (50, 28), (82, 50))
    for index, (name, family, template, ranges, mechanisms) in enumerate(TEMPLATES, 1):
        for instance, role in enumerate(("development", "confirmation", "confirmation"), 1):
            if index >= 13:
                role = "confirmation"
            parameters = {}
            for key, (lo, hi) in ranges.items():
                token = f"nuclearbench-v2-control:{name}:{instance}:{key}"
                u = int(hashlib.sha256(token.encode()).hexdigest()[:12], 16) / float(16**12 - 1)
                parameters[key] = round(lo + (hi - lo) * u, 4)
            parameters.update(zip(("n0", "z0"), closures[instance - 1]))
            expression = template
            for key, value in parameters.items():
                expression = re.sub(r"\b" + key + r"\b", str(value), expression)
            f = entry(
                f"S{index:02d}_{name}_{instance:02d}",
                expression,
                "E_control",
                family,
                "https://github.com/TAO-MINGYU/NuSR-Benchmark/blob/v2.0.0/CONTROL_DESIGN.md",
                "Benchmark-designed template, not an experimentally established expression",
                "nuclear_grid",
                recovery_kind="synthetic_mechanism_control",
                structure_group=name,
                evidence_role=role,
                confirmation_axis="family_composition"
                if index >= 13
                else ("coefficient_instance" if instance > 1 else "development"),
                scope="Designed diagnostic numeric energy in MeV",
                template=template,
                parameters_instantiated=parameters,
                parameter_ranges=ranges,
                mechanisms=mechanisms,
                generator_version="sha256-uniform-v1",
            )
            f["status"] = "synthetic_control_not_an_empirical_law"
            f["parameters"] = (
                "Preregistered deterministic coefficients; never fitted to observations"
            )
            result.append(f)
    return result
