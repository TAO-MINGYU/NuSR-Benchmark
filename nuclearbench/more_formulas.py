"""Additional source-verified N/Z expressions, not an exhaustive formula catalogue."""

from .formulas import entry
from .sources import RIPL4_BASE

HANDBOOK = "https://www-nds.iaea.org/RIPL-3/handbook/ripl2-feb2005.pdf"
RIPL2018 = RIPL4_BASE + "gamma/gdr-parameters_exp%26systematics_slo%26smlo.readme"
PAIRING = "https://arxiv.org/pdf/nucl-th/0308046v1"
GRODZINS = "https://arxiv.org/html/2105.07164v1"


def more_formulas():
    result = []

    def add(identifier, expression, observable, group, source, locator, domain, **extra):
        result.append(
            entry(
                identifier,
                expression,
                observable,
                group,
                source,
                locator,
                domain,
                recovery_kind="published_empirical",
                structure_group=group,
                evidence_role="reference_recovery",
                **extra,
            )
        )

    centroid = "(31.2*A**(-1/3)+20.6*A**(-1/6))"
    add(
        "A42_GDR_centroid_2005",
        centroid,
        "GDR_E_single",
        "gdr_mass_scaling",
        HANDBOOK,
        "Sec.7.6, printed p129, Eq.(7.25)",
        "gdr_reference",
        scope="One-mode experimental-fit coordinates with A>=40; spherical-systematics reference, not an exact measured law",
    )
    add(
        "A43_GDR_width_2005",
        f"0.026*{centroid}**1.91",
        "GDR_W_single",
        "gdr_response_scaling",
        HANDBOOK,
        "Sec.7.6, p129, Eq.(7.25), substitute published centroid",
        "gdr_reference",
        scope="Same single-mode scope; measured energy is not supplied as an input",
    )
    add(
        "A44_GDR_peak_2005",
        f"144*N*Z/(A*3.141592653589793*0.026*{centroid}**1.91)",
        "GDR_peak_single",
        "gdr_response_scaling",
        HANDBOOK,
        "Sec.7.6, p129, Eq.(7.25), substitute published width and energy",
        "gdr_reference",
        scope="Same single-mode scope; pi fixed to3.141592653589793; no measured width input",
    )
    for i, model, e1, e2 in ((45, "SLO", 130.0, 9.0), (46, "SMLO", 128.0, 8.5)):
        add(
            f"A{i}_GDR_centroid_{model}2018",
            f"{e1}*sqrt(4*N*Z/A**2)*A**(-1/3)/sqrt(1+{e2}*A**(-1/3))",
            "GDR_E_centroid",
            "gdr_isovector_centroid",
            RIPL2018,
            "COMMENT2, centroid systematics and printed e1/e2 parameters",
            "gdr_reference",
            scope="Two coefficient instances of the same structure; SLO observations are context only, not SMLO measurements",
        )
    add(
        "A47_Grodzins_product",
        "25.7*Z**2*A**(-2/3)",
        "Grodzins_EB",
        "collectivity_product",
        GRODZINS,
        "Eq.(1), Raman coefficient2.57; keV*e^2b^2 multiplied by10 to obtain MeV*e^2fm^4",
        "grodzins_reference",
        scope="Composite target E(2+)*B(E2;0+->2+); neither measured factor is a predictor; known shell-closure limitations",
    )
    add(
        "A48_pairing_classical",
        "12/sqrt(A)",
        "Delta_pair_ref",
        "average_pairing_reference",
        PAIRING,
        "Eq.(16), traditional-model average gap",
        "pairing_reference",
        coordinate_observable="B",
        scope="Average phenomenological pairing reference, not an asserted exact three-point mass indicator",
    )
    add(
        "A49_pairing_Vogel",
        "(7.2-44*I**2)*A**(-1/3)",
        "Delta_pair_ref",
        "average_pairing_reference",
        PAIRING,
        "Eq.(16), Vogel parameterization; original credit Vogel/Jonson/Hansen1984",
        "vogel_reference",
        coordinate_observable="B",
        scope="Benchmark restricted to50<Z<82 and82<N<126; average gap, not an exact OES3 target",
    )
    result.append(
        entry(
            "A50_TRK_sum",
            "60*N*Z/A",
            "TRK_sum",
            "dipole_sum_rule",
            HANDBOOK,
            "Sec.7.6, p129, text immediately below Eq.(7.25)",
            "gdr_reference",
            recovery_kind="published_analytic_reference",
            structure_group="dipole_sum_rule",
            evidence_role="analytic_reference",
            scope="Unenhanced Thomas-Reiche-Kuhn analytic reference (kappa=0); not an experimental integrated cross section",
        )
    )
    return result
