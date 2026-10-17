"""Source-audited additions; spin/parameter variants keep one structural group."""

from .data import state_name
from .formulas import FORMULAS, SHENG, entry
from .more_formulas import more_formulas

HA = "https://arxiv.org/pdf/nucl-th/0612003v2"
YRAST = "https://arxiv.org/pdf/1007.3192v1"
DZ = "https://arxiv.org/pdf/1609.05021v1"
ANGELI = "https://doi.org/10.1016/j.adt.2011.12.006"
LSD = "https://arxiv.org/pdf/nucl-th/0205011v1"

# Table A, p.9. Tuple: fixed spin, parity, alpha,gamma,beta_p,beta_n,lambda_p,lambda_n.
# The caption mentions 11+ but supplies no coefficient row for it: it is not admitted.
YRAST_PARAMETERS = [
    (2, "+", 68, 1.34, 0.83, 1.17, 0.42, 0.28),
    (4, "+", 268, 1.38, 1.21, 1.68, 0.33, 0.23),
    (6, "+", 598, 1.38, 1.40, 1.64, 0.31, 0.18),
    (8, "+", 1439, 1.45, 1.34, 1.50, 0.26, 0.15),
    (10, "+", 2317, 1.47, 1.36, 1.65, 0.21, 0.14),
    (1, "-", 75, 0.83, 2.18, 2.33, 0.57, 0.44),
    (3, "-", 77, 0.83, 1.07, 0.90, 0.40, 0.47),
    (5, "-", 144, 0.92, 0.84, 1.09, 0.32, 0.45),
    (7, "-", 283, 1.01, 0.66, 1.08, 0.37, 0.56),
    (9, "-", 442, 1.06, 0.77, 1.33, 0.32, 0.37),
    (2, "-", 48, 0.73, 1.09, 1.59, 0.19, 0.31),
    (4, "-", 75, 0.81, 1.00, 1.27, 0.17, 0.24),
    (6, "-", 108, 0.83, 0.77, 1.40, 0.19, 0.28),
    (8, "-", 277, 1.00, 0.90, 1.49, 0.15, 0.20),
    (10, "-", 238, 0.90, 1.24, 1.76, 0.44, 0.25),
    (1, "+", 47, 0.67, 0.54, 0.99, 0.76, 0.50),
    (3, "+", 49, 0.76, 1.17, 1.49, 0.58, 0.32),
    (5, "+", 87, 0.82, 1.05, 1.26, 0.40, 0.24),
    (7, "+", 139, 0.88, 1.19, 1.48, 0.28, 0.24),
    (9, "+", 173, 0.86, 1.09, 1.61, 0.34, 0.46),
]


def published_formulas():
    result = [
        dict(
            f,
            recovery_kind="published_empirical",
            structure_group=f["family"],
            evidence_role="evaluation",
            scope="Full designated empirical expression",
        )
        for f in FORMULAS
    ]

    def add(name, expr, observable, family, source, locator, domain, **extra):
        result.append(
            entry(
                name,
                expr,
                observable,
                family,
                source,
                locator,
                domain,
                recovery_kind="published_empirical",
                structure_group=family,
                evidence_role="evaluation",
                scope="Full designated empirical expression",
                **extra,
            )
        )

    add(
        "A11_R_ZI",
        "sqrt(3/5)*1.6131*(1+0.1029*I)*Z**(1/3)",
        "Rch",
        "radius_isospin",
        SHENG,
        "Eq. (7), Table 1; a=-0.1029",
        "sheng",
    )
    add(
        "A12_R_Zasym",
        "sqrt(3/5)*1.6123*(1+0.0435*(N-Z)/Z)*Z**(1/3)",
        "Rch",
        "radius_isospin",
        SHENG,
        "Eq. (8), Table 1; a=-0.0435",
        "sheng",
    )
    add(
        "A13_R_Zfinite",
        "sqrt(3/5)*1.5579*(1+0.0835*(N-Z)/Z+1.0652/Z)*Z**(1/3)",
        "Rch",
        "radius_isospin",
        SHENG,
        "Eq. (9), Table 1; a=-0.0835",
        "sheng",
    )
    for task, j, p, alpha, beta, gamma, lam in (
        ("A14_Ha_E2", 2, "+", 34.9, 1, 1.19, 0.36),
        ("A15_Ha_E3", 3, "-", 62.8, 0.9, 0.79, 0.24),
    ):
        add(
            task,
            f"{alpha}*A**(-{gamma})+{beta}*(exp(-{lam}*Np)+exp(-{lam}*Nn))",
            state_name(j, p),
            "valence_spectroscopy",
            HA,
            "Eq. (1), Table I, version 2",
            "spectroscopy",
            fixed_spin=j,
            fixed_parity=p,
        )
    for index, (j, p, alpha, gamma, bp, bn, lp, ln) in enumerate(YRAST_PARAMETERS, 16):
        add(
            f"A{index:02d}_yrast_{state_name(j, p)}",
            f"{alpha}*A**(-{gamma})+{bp}*exp(-{lp}*Np)+{bn}*exp(-{ln}*Nn)",
            state_name(j, p),
            "valence_spectroscopy",
            YRAST,
            "Eq. (3), Table A, version 1",
            "spectroscopy",
            fixed_spin=j,
            fixed_parity=p,
            printed_coefficients={
                "alpha": alpha,
                "gamma": gamma,
                "beta_p": bp,
                "beta_n": bn,
                "lambda_p": lp,
                "lambda_n": ln,
            },
        )
    add(
        "A36_DZ_R_naive",
        "A**(1/3)*(0.947-0.4*(N-Z)/A**(4/3)-0.1475*I**2)*exp(1.37/A)",
        "Rch",
        "radius_isovector_exponential",
        DZ,
        "Eq. (3a), A<=60 fitted parameter set",
        "dz_naive",
    )
    add(
        "A37_DZ_R_correlated",
        "A**(1/3)*(0.94-0.4*(N-Z)/A**(4/3)-0.167*I**2)*exp(1.14/A)+5.208*Q_EI/A**(1/3)",
        "Rch",
        "radius_isovector_exponential",
        DZ,
        "Eqs. (3a)-(3b), correlated parameter set",
        "dz_correlated",
    )
    add(
        "A38_Angeli_R",
        "0.9071*A**(1/3)+1.105/A**(1/3)-0.548/A",
        "Rch",
        "radius_inverse_powers",
        ANGELI,
        "Eq. (8); rms radius reference interpolation",
        "sheng",
    )
    # Only the analytic spherical macroscopic piece is representable using N/Z.
    # Microscopic/deformation/electron/congruence terms are NOT silently supplied.
    for index, name, bv, kv, bs, ks, bc, kc, bg, kg, r0, c4 in [
        (39, "LDM", -15.8484, 1.8475, 19.3859, 1.9830, 0, 0, 0, 0, 1.18995, 1.1995),
        (40, "NLD", -15.4721, 1.6411, 17.0603, 0.7546, 0, 0, 10.3574, 13.4235, 1.21610, 0.7952),
        (41, "LSD", -15.4920, 1.8601, 16.9707, 2.2938, 3.8602, -2.3764, 0, 0, 1.21725, 0.9181),
    ]:
        expr = f"-({bv}*(1-{kv}*I**2)*A+{bs}*(1-{ks}*I**2)*A**(2/3)"
        if bc:
            expr += f"+{bc}*(1-({kc})*I**2)*A**(1/3)"
        if bg:
            expr += f"+{bg}*(1-{kg}*I**2)"
        expr += f"+3*1.4399764*Z**2/(5*{r0}*A**(1/3))-{c4}*Z**2/A)"
        f = entry(
            f"A{index}_{name}_spherical_macro",
            expr,
            "B_macro",
            "macroscopic_curvature",
            LSD,
            "Macroscopic expression and Table I; spherical shape factors equal 1",
            "macroscopic",
            recovery_kind="published_analytic_reference",
            structure_group="macroscopic_curvature",
            evidence_role="restricted_reference",
            scope="Negative spherical macroscopic energy only; not the complete mass model",
            numerical_convention="e^2=1.4399764 MeV fm; microscopic, deformation, electron and congruence corrections excluded",
        )
        result.append(f)
    return result + more_formulas()
