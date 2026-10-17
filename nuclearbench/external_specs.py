"""Frozen target definitions; candidates must independently pass coverage gates."""


def spec(identifier, observable, unit, panel, family, kind, meaning):
    return {
        "id": identifier,
        "observable": observable,
        "unit": unit,
        "panel": panel,
        "structure_group": family,
        "label_kind": kind,
        "target_definition": meaning,
        "input_information": "N,Z and declared deterministic nuclear knowledge only",
        "forbidden_information": "all same-target direct/derived lookup terminals; no measured moments, resonance parameters, lifetimes, branches, Q values or other-task observations as inputs",
    }


EXTERNAL_SPECS = [
    spec(
        "B34_mu_gs",
        "mu_gs",
        "mu_N",
        "evaluated_observables",
        "magnetic_moments",
        "recommended_evaluated",
        "Definite-sign ground-state magnetic dipole moment; INDC(NDS)-0915 recommended bare-nucleus convention",
    ),
    spec(
        "B35_Q_gs",
        "Q_gs",
        "e fm^2",
        "evaluated_observables",
        "quadrupole_moments",
        "recommended_evaluated",
        "Definite-sign ground-state electric quadrupole moment; INDC(NDS)-0833; source barns times100",
    ),
    spec(
        "B36_Grodzins_EB",
        "Grodzins_EB",
        "MeV e^2 fm^4",
        "evaluated_observables",
        "collectivity",
        "derived_composite",
        "E(first2+) times B(E2;0+->2+); both are labels, not inputs; joint primitive parents and unknown covariance retained",
    ),
]
for i, (key, unit, meaning) in enumerate(
    (
        (
            "GDR_E_centroid",
            "MeV",
            "Published strength-weighted centroid (E1*S1+E2*S2)/(S1+S2), using rounded experimental-fit components; one-mode E1 when unsplit",
        ),
        ("GDR_E1", "MeV", "Single-mode energy or lower-mode energy in a split SLO response"),
        ("GDR_E2", "MeV", "Upper-mode energy; only experimental two-mode responses"),
        ("GDR_W1", "MeV", "Single-mode or lower-mode SLO fitted width"),
        ("GDR_W2", "MeV", "Upper-mode SLO fitted width; two-mode responses only"),
        (
            "GDR_peak1",
            "mb",
            "Single-mode or lower-mode Lorentzian peak cross section, not total response at the peak",
        ),
        ("GDR_peak2", "mb", "Upper-mode Lorentzian peak cross section; two-mode responses only"),
    ),
    37,
):
    EXTERNAL_SPECS.append(
        spec(
            f"B{i}_{key}",
            key,
            unit,
            "structure_parameter_prediction",
            "giant_dipole_response",
            "experimental_data_fitted_parameter",
            meaning + "; RIPL4 SLO In=1 only; systematic In=0 excluded",
        )
    )
for i, (key, unit, meaning) in enumerate(
    (
        (
            "logD0_BNL",
            "decades",
            "log10(s-wave average resonance spacing / eV), fixed BNL2018 columns",
        ),
        ("Gg0_BNL", "eV", "s-wave average total radiative width, fixed BNL2018 columns"),
        (
            "S0_BNL",
            "1e-4",
            "s-wave neutron strength function in published units of1e-4, fixed BNL2018 columns",
        ),
    ),
    44,
):
    EXTERNAL_SPECS.append(
        spec(
            f"B{i}_{key}",
            key,
            unit,
            "evaluated_resonance_parameters",
            "s_wave_neutron_resonances",
            "evaluated_resonance_parameter",
            meaning
            + "; coordinates identify the incident target, not the compound nucleus; no RIPL3 fallback",
        )
    )
for i, key in enumerate(
    ("barrier_inner", "barrier_outer", "barrier_hw_inner", "barrier_hw_outer"), 47
):
    EXTERNAL_SPECS.append(
        spec(
            f"B{i}_{key}",
            key,
            "MeV",
            "structure_parameter_prediction",
            "fission_barrier_parameters",
            "empirical_model_dependent_parameter",
            key
            + " from RIPL4 2025 empirical table; source ad-hoc uncertainty spread is not treated as statistical sigma",
        )
    )
for i, key in enumerate(
    (
        "logT_alpha",
        "logT_beta_minus",
        "logT_beta_plus_EC",
        "logT_EC",
        "logT_SF",
        "logT_proton",
        "logT_two_proton",
    ),
    1,
):
    EXTERNAL_SPECS.append(
        spec(
            f"D{i:02d}_{key}",
            key,
            "decades",
            "nuclear_decay_extension",
            "ground_state_" + key.removeprefix("logT_"),
            "evaluated_partial_lifetime",
            "log10(ground-state partial half-life / s); T_partial=T_total/(branch_percent/100); exclude censored/estimated/unknown lifetimes and branches; covariance unavailable; no measured Q value input",
        )
    )
