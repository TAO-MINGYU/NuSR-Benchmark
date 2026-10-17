"""Admission decisions: citations establish candidate provenance, not exhaustiveness."""

LITERATURE = [
    {
        "id": "bw_bwm",
        "source": "https://arxiv.org/pdf/nucl-th/0405080",
        "decision": "admitted",
        "locators": "Eqs. (1), (4)-(5)",
        "role": "Original BW/BWM reference cards retained",
        "caveat": "Experimental isotonic shift is excluded; exact built-in template/initializer access must be audited",
    },
    {
        "id": "sheng2015",
        "source": "https://doi.org/10.7498/aps.64.112101",
        "decision": "admitted",
        "locators": "Eqs. (2),(4)-(11), Table 1",
        "role": "Radius scaling, isospin, finite-size and valence/pairing instances",
        "caveat": "Equivalent sharp radii converted to rms; proton-scaling variants remain related instances",
    },
    {
        "id": "misr2024v3",
        "source": "https://arxiv.org/html/2404.11477v3",
        "decision": "admitted",
        "locators": "Eqs. (4)-(5)",
        "role": "Original leading-order MISR binding/radius cards retained",
        "caveat": "Version-pinned leading expressions, not the complete MISR10 model or a blind discovery challenge",
    },
    {
        "id": "ha2007",
        "source": "https://arxiv.org/pdf/nucl-th/0612003v2",
        "decision": "admitted",
        "locators": "Eq. (1), Table I",
        "role": "Two fixed-state instances of one shared-rate valence formula",
        "caveat": "Fixed even-even spin tasks; reference valence boundaries stated explicitly",
    },
    {
        "id": "yrast2010",
        "source": "https://arxiv.org/pdf/1007.3192",
        "decision": "admitted",
        "reviewed_pdf_sha256": "34e55b2995af82ebb75f67de8caabf373972764b58811e1904a1cdf7bec2304d",
        "locators": "Eq. (3), Table A p.9",
        "role": "20 fixed-state parameter instances; one structural family",
        "caveat": "No 11+ row in Table A despite caption; excluded. Sparse observed states use common AME coordinate anchors with no invented observations.",
    },
    {
        "id": "heylen2016",
        "source": "https://arxiv.org/pdf/1609.05021",
        "decision": "admitted",
        "reviewed_pdf_sha256": "3d348b10f0843d2f5d70522102c308e9385efa671d7dfab5a490e674296b1fe1",
        "locators": "Eq. (3a)-(3b), fitted parameter sets in text",
        "role": "Naive and correlated Duflo-Zuker radius forms",
        "caveat": "Restricted light-nucleus domains and explicit EI-shell occupancy convention; original r_pi notation retained as an empirical radius reference",
    },
    {
        "id": "angeli2013",
        "source": "https://doi.org/10.1016/j.adt.2011.12.006",
        "decision": "admitted",
        "locators": "Eq. (8), reference-radius discussion",
        "role": "Inverse-power rms-radius interpolation",
        "caveat": "Some evaluated radii share model-based absolute anchors; exclude Z=75,84,86,87,88,96 from primary absolute-radius prediction",
    },
    {
        "id": "pomorski2002",
        "source": "https://arxiv.org/pdf/nucl-th/0205011",
        "decision": "restricted_reference",
        "reviewed_pdf_sha256": "e421c4eeff0bfd2781606c60b28a3db7c5641c6df74e6e011f65c53111cff471",
        "locators": "Macroscopic expression, Table I",
        "role": "Three spherical analytic macroscopic components",
        "caveat": "These are not complete LDM/NLD/LSD mass predictions: no microscopic, deformation, electron or congruence corrections are invented",
    },
    {
        "id": "dz_mass",
        "source": "https://arxiv.org/abs/1407.8218",
        "decision": "deferred",
        "role": "Possible future complex shell-occupation recovery panel",
        "caveat": "Full model requires a separately audited algorithmic grammar; an opaque callable is not a short formula recovery answer",
    },
    {
        "id": "radius_ml2025",
        "source": "https://arxiv.org/html/2512.06683v1",
        "decision": "assisted_panel_only",
        "role": "Published radius SR/predictive reference candidate",
        "caveat": "Measured binding energy/pairing features exceed N/Z-only primary information; no silent primary admission",
    },
    {
        "id": "madland_nix1988",
        "source": "https://doi.org/10.1016/0375-9474(88)90370-3",
        "decision": "deferred",
        "role": "Potential pairing-gap references",
        "caveat": "Shape-dependent terms and target-estimator correspondence require further audit; no unverified coefficients included",
    },
    {
        "id": "garvey_kelson",
        "source": "https://www.iasa.gr/stathis/Nucl/Mass_Prediction_Garvey_Kelson.pdf",
        "decision": "not_NZ_only_recovery",
        "role": "Possible future mass-relation diagnostic",
        "caveat": "Neighboring measured masses are additional inputs; cannot silently count a relation as an N/Z-only expression",
    },
    {
        "id": "variable_J",
        "source": "https://arxiv.org/pdf/1007.3192",
        "decision": "not_variable_J_primary",
        "role": "Possible separate spectroscopy model study",
        "caveat": "Variable angular momentum and moment of inertia are outside N/Z input. Fixed-spin empirical yrast tasks do not add J as a fitted input.",
    },
]

LITERATURE += [
    {
        "id": "ripl2005_gdr_trk",
        "source": "https://www-nds.iaea.org/RIPL-3/handbook/ripl2-feb2005.pdf",
        "decision": "admitted",
        "locators": "Sec7.6 printedp129 Eq7.25 and TRK text",
        "role": "Three published nested GDR recovery references and one unenhanced analytic sum rule",
        "caveat": "Near-stability spherical systematics; no measured energy/width inserted; sum rule is "
        "not experimental truth",
        "reviewed_pdf_sha256": "04e83714f6d212963a0a87760ba1c9ca7e253fe3a9638bb153b25a593a13554c",
    },
    {
        "id": "ripl2018_gdr",
        "source": "https://raw.githubusercontent.com/IAEA-NDS/RIPL-4/54afc19a4f7c861d28237c1da812d4cf385b528d/gamma/gdr-parameters_exp%26systematics_slo%26smlo.readme",
        "decision": "admitted",
        "locators": "COMMENT2 and fixed e1/e2 sets; In flag format",
        "role": "SLO/SMLO centroid reference variants; SLO experimental-fit parameter prediction",
        "caveat": "Only135 In=1 recommendations are observational;8845 systematic rows excluded; fit "
        "parameters are model-dependent",
    },
    {
        "id": "pairing2003",
        "source": "https://arxiv.org/pdf/nucl-th/0308046v1",
        "decision": "admitted",
        "locators": "Eq16; original Vogel1984 credit in references",
        "role": "Traditional and isospin-dependent averaged pairing reference expressions",
        "caveat": "Average gaps are not exact OES3 values; Vogel benchmark coordinate domain is "
        "restricted",
        "reviewed_pdf_sha256": "37554efc5af2232ef8b07239982de4cdca24e1266278be30c35767245c94c1ac",
    },
    {
        "id": "grodzins2021",
        "source": "https://arxiv.org/html/2105.07164v1",
        "decision": "admitted_as_NZ_product",
        "locators": "Eq1;keV and e2barn2 units",
        "role": "Raman/Grodzins E2*BE2 reference and real composite prediction",
        "caveat": "Neither measured factor is an input; coefficient2.57 becomes25.7 in MeV*e2fm4; "
        "shell-closure limitations retained",
        "reviewed_pdf_sha256": "350dd2db7f8b67d5c8c3953bca9bbe4d8b44c404cb51a0b0d16f5db7983d172b",
    },
    {
        "id": "moments0915",
        "source": "https://www-nds.iaea.org/nuclearmoments/magn_mom_recomm.csv",
        "decision": "admitted",
        "locators": "Recommended report0915; definite ground-state sign/spin",
        "role": "Ground-state magnetic moments",
        "caveat": "CSV second column is A; excited states, unknown signs, malformed fields and other "
        "report versions excluded",
    },
    {
        "id": "moments0833",
        "source": "https://www-nds.iaea.org/nuclearmoments/elec_mom_recomm.csv",
        "decision": "admitted",
        "locators": "Recommended report0833; ground state",
        "role": "Electric quadrupole moments",
        "caveat": "Barns times100; no tentative sign or silent repair of malformed values",
    },
    {
        "id": "ripl4_resonances2025",
        "source": "https://raw.githubusercontent.com/IAEA-NDS/RIPL-4/54afc19a4f7c861d28237c1da812d4cf385b528d/resonances/resonances.readme",
        "decision": "admitted",
        "locators": "L0 fixed-format BNL2018 columns",
        "role": "s-wave spacing, radiative width and neutron strength",
        "caveat": "Target N/Z is not compound N+1/Z; missing BNL values do not fall back to older RIPL3 "
        "values",
    },
    {
        "id": "ripl4_fission2025",
        "source": "https://raw.githubusercontent.com/IAEA-NDS/RIPL-4/54afc19a4f7c861d28237c1da812d4cf385b528d/fission/empirical-barriers-ripl4.readme",
        "decision": "admitted_separate_parameter_panel",
        "locators": "2025 empirical barrier table and uncertainty notice",
        "role": "Barrier heights and curvatures",
        "caveat": "Model-dependent parameters; ad-hoc spreads are not statistical sigma; "
        "inconsistent84/207/Bi row excluded",
    },
    {
        "id": "nubase2020",
        "source": "https://www-nds.iaea.org/amdc/ame2020/nubase_4.mas20.txt",
        "decision": "admitted_optional_decay_panel",
        "locators": "Ground-state half-life and direct branch fields",
        "role": "N/Z-only prediction of log partial lifetimes",
        "caveat": "No Q input; censoring/estimates/unknown branching excluded; proton/two-proton "
        "candidates must still pass coverage",
    },
    {
        "id": "nudat_source_identity",
        "source": "https://www.nndc.bnl.gov/nudat3/guide/",
        "decision": "ENSDF_view_not_new_independent_source",
        "role": "NuDat source-identity audit",
        "caveat": "Levels/gammas/decay are ENSDF-derived; changing web frontend does not create "
        "independent measurements",
    },
    {
        "id": "weisskopf_catalog_conflict",
        "source": "https://doi.org/10.1103/PhysRev.83.1073",
        "decision": "deferred",
        "role": "Possible single-particle reference",
        "caveat": "Supplied catalogue generalE2 expression gives about0.0594A^(4/3), but separate "
        "downward prose quotes0.297; original direction/convention unresolved, not copied "
        "blindly",
    },
]
