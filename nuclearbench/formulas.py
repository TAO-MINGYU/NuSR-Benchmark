"""Published numeric formula conventions; no fitted coefficients are estimated here."""

BW = "https://arxiv.org/pdf/nucl-th/0405080"
SHENG = "https://doi.org/10.7498/aps.64.112101"
MISR = "https://arxiv.org/html/2404.11477v3"


def entry(name, expression, observable, family, source, locator, domain, **extra):
    return dict(
        id=name,
        expression=expression,
        observable=observable,
        family=family,
        source=source,
        locator=locator,
        domain=domain,
        label="formula_generated",
        status="empirical_model_not_unique_physical_truth",
        parameters="Fixed printed coefficients; never refit using test labels",
        **extra,
    )


FORMULAS = [
    entry(
        "A01_BW",
        "15.78*A-18.34*A**(2/3)-0.71*Z*(Z-1)/A**(1/3)-23.21*(N-Z)**2/A+12*d/sqrt(A)",
        "B",
        "liquid_drop",
        BW,
        "Eq. (1), coefficients in text",
        "mass_bw",
    ),
    entry(
        "A02_BWM",
        "15.777*A-18.34*A**(2/3)-0.71*Z*(Z-1)/A**(1/3)-23.21*(N-Z)**2/(A*(1+exp(-A/17)))+12*(1-exp(-A/30))*d/sqrt(A)",
        "B",
        "liquid_drop",
        BW,
        "Eqs. (4)-(5); no isotonic experimental shift",
        "mass_bw",
    ),
    entry(
        "A03_MISR1_B",
        "Z*(1+1/N+1.10*N/Z**2)*(I*(32.43-A**(1/3)*N/Z)+16.70)",
        "B",
        "misr",
        MISR,
        "Version 3, Eq. (4), eta0=1 MeV",
        "misr",
    ),
    entry(
        "A04_R_A",
        "sqrt(3/5)*1.2269*A**(1/3)",
        "Rch",
        "radius_scaling",
        SHENG,
        "Eq. (2), Table 1",
        "sheng",
    ),
    entry(
        "A05_R_Z",
        "sqrt(3/5)*1.6394*Z**(1/3)",
        "Rch",
        "radius_scaling",
        SHENG,
        "Eq. (6), Table 1",
        "sheng",
    ),
    entry(
        "A06_R_I",
        "sqrt(3/5)*1.2828*(1-0.2704*I)*A**(1/3)",
        "Rch",
        "radius_isospin",
        SHENG,
        "Eq. (4), Table 1",
        "sheng",
    ),
    entry(
        "A07_R_finite",
        "sqrt(3/5)*1.2331*(1-0.1461*I+2.3310/A)*A**(1/3)",
        "Rch",
        "radius_isospin",
        SHENG,
        "Eq. (5), Table 1",
        "sheng",
    ),
    entry(
        "A08_R_collective",
        "sqrt(3/5)*1.2262*(1-0.1473*I+1.9876/A+0.3993*P_s/A)*A**(1/3)",
        "Rch",
        "radius_valence",
        SHENG,
        "Eq. (10), Table 1",
        "sheng",
    ),
    entry(
        "A09_R_pairing",
        "sqrt(3/5)*1.2262*(1-0.1472*I+1.9552/A+0.4030*P_s/A+0.1093*d/A)*A**(1/3)",
        "Rch",
        "radius_valence",
        SHENG,
        "Eq. (11), Table 1",
        "sheng",
    ),
    entry(
        "A10_MISR1_R",
        "A**(1/3)*(0.95+1.48/Z)+0.017*(P_m-Z/N)*exp(I)-I",
        "Rch",
        "misr",
        MISR,
        "Version 3, Eq. (5); numeric radii in fm",
        "misr",
    ),
]


def in_domain(domain, n, z):
    if domain == "mass_bw":
        return n >= 8 and 8 <= z <= 83
    if domain == "sheng":
        return n > 8 and z > 8
    if domain == "misr":
        return n >= 8 and 12 <= z <= 50
    raise ValueError(domain)


MACROS = {
    "A": "N+Z",
    "I": "(N-Z)/(N+Z)",
    "d": "((-1)**N+(-1)**Z)/2",
    "P_s": {
        "formula": "vp*vn/(vp+vn), 0 when vp+vn=0; valence=min absolute distance",
        "proton_magic": [2, 6, 14, 28, 50, 82, 114],
        "neutron_magic": [2, 8, 14, 28, 50, 82, 126, 184],
        "note": "Source-specific effective closures, not a claim all are universal magic numbers",
    },
    "P_m": {
        "formula": "vp*vn/(vp+vn), 0 when vp+vn=0; valence=min absolute distance",
        "proton_magic": [8, 20, 28, 50, 82],
        "neutron_magic": [8, 20, 28, 50, 82],
    },
    "radius_conversion": "Sheng reports equivalent sharp R_C=sqrt(5/3)*r_rms; every Sheng expression here includes sqrt(3/5).",
}
