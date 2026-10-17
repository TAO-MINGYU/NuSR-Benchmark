"""Frozen independent decisions about the supplied76-family research catalogue."""

CATALOG_AUDIT = {
    "snapshot": "user-provided Target catalogue, frozen2026-08-30; read2026-10-17",
    "evidence_scope": "Candidate/input-contract audit of76 families, not original-source coefficient "
    "certification for all76. No personal documents or secondary radius "
    "transcription redistributed.",
    "catalog_sha256": "ba6d11704b0286d48cc8894e595f2a7bf276f0bc2d6bec252c59c261287b1bf6",
    "entries": [
        {
            "id": "NF-0001",
            "name": "Bethe–Weizsäcker semi-empirical mass formula",
            "folder": "Bethe_Weizsacker_Semi_Empirical_Mass_Formula",
            "decision": "already_covered",
            "reason": "Existing BW/BWM mass recovery and measured mass panel",
            "mapped_tasks": ["A01_BW", "A02_BWM"],
            "metadata_sha256": {
                "formula.yaml": "50a4d82f616de63b4ac4775d89d8e715702426104c931405b2250a81fcef2743",
                "README.md": "8283a136b08f379399a708599a5528f16b1d0010b4cb827061fb1e5454b55d28",
                "sources.bib": "44c7f26c6b8cb46831fac1d9c7228e94367f5bc7997cd1fdbff417254c5fc408",
            },
        },
        {
            "id": "NF-0002",
            "name": "Garvey–Kelson mass relations",
            "folder": "Garvey_Kelson_Mass_Relations",
            "decision": "extra_measured_inputs",
            "reason": "Neighbor masses are extra inputs; relation recovery is not N/Z-only "
            "function recovery",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "f236a9e65c1b35c2eccd79fc4ddc77b873496a92d1aa53308982a31f248504ed",
                "README.md": "88cc897a0bf05dab200ca3ae5883465700c7ccbca32b1dbafa990c4ad79e8dc1",
                "sources.bib": "820df5655a03d63148cae8d561cc0de6c79f750b7da7efaf5647b1df8a07026a",
            },
        },
        {
            "id": "NF-0003",
            "name": "Isobaric multiplet mass equation",
            "folder": "Isobaric_Multiplet_Mass_Equation",
            "decision": "extra_state_information",
            "reason": "Multiplet identity/isospin and fitted multiplet coefficients require a "
            "separate state-aware benchmark",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "25fe0f7ba164c054e207a141c7f19b917811a2013bb0e636c7859414c7699e81",
                "README.md": "324002b11b0a5af5abb5ef84c89bad01c7ff4e73ca89cefe6794e2997d31c3a2",
                "sources.bib": "8c6d8c5fddf4e8b807b8e45d2f815bbad71be4a1226fd1a42087de221e561434",
            },
        },
        {
            "id": "NF-0004",
            "name": "Semi-empirical beta-stability line",
            "folder": "Semi_Empirical_Beta_Stability_Line",
            "decision": "different_unit_of_analysis",
            "reason": "A-only stability-line output is Z_beta(A), not the observed Z supplied as "
            "input for each nuclide",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "369b3f5c22656891c27b3c497defc58cc422ed884896b155dc32fd0503ed5cfb",
                "README.md": "9f5a54713584bb6c04c4ec5704a54d9bd8d50fb0a24888c64c201edf77ad9ace",
                "sources.bib": "4e096b6058990683fe01a928783a18ca8037f3ce605b514fe2295630d6a08669",
            },
        },
        {
            "id": "NF-0005",
            "name": "Nuclear radius A^(1/3) law",
            "folder": "Nuclear_Radius_A_One_Third_Law",
            "decision": "already_covered",
            "reason": "Sharp/rms radius convention already represented in original recovery panel",
            "mapped_tasks": ["A04_R_A"],
            "metadata_sha256": {
                "formula.yaml": "a808169043803a43a681c8df5d7df8323e00f6f743a8ac66318dccbe382a7219",
                "README.md": "ee272cd04c597303af33de6431f83475e6ff8b26eb913cf15bbcf3821cbb27d4",
                "sources.bib": "f991de52fd8e2ee1ca44c8674080301cccab02cbd40e939e601a0472003d2a7b",
            },
        },
        {
            "id": "NF-0006",
            "name": "Grodzins relation",
            "folder": "Grodzins_Relation",
            "decision": "adapted_NZ_product",
            "reason": "Source-verified Raman/Grodzins product E2*BE2 is an N/Z target; neither "
            "measured factor is an input",
            "mapped_tasks": ["A47_Grodzins_product", "B36_Grodzins_EB"],
            "metadata_sha256": {
                "formula.yaml": "79cfbec547ff6ee36af0c3e18ff19c36061df6417531903483ce9c7503b7ea4a",
                "README.md": "3e499ea99c7fd691b0df4abf197bf7ad54db7418b4d1bd276d014fee2566406c",
                "sources.bib": "d3730d45767e33d8f284ee9851008827ab031f96569781e962afadd1e8842288",
            },
        },
        {
            "id": "NF-0007",
            "name": "Holmberg–Lipas rotational formula",
            "folder": "Holmberg_Lipas_Rotational_Formula",
            "decision": "extra_spin_and_fitted_parameters",
            "reason": "Rotational state spin and nucleus-dependent fitted parameters require "
            "another input/analysis axis",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "7bc9fe292a7c16227cd88a5515ee624b634dfee388573ec7344c1327c7abce75",
                "README.md": "b946e29f78a81097479708c3e7340ea31c85301ca3b5322ecc140fb5c7a33df1",
                "sources.bib": "00cd55db2a2e406f6ed209e96ea21bdf132752f0085504352f4f99d817595b52",
            },
        },
        {
            "id": "NF-0008",
            "name": "Bethe Fermi-gas level-density formula",
            "folder": "Bethe_Fermi_Gas_Level_Density",
            "decision": "extra_excitation_or_model_inputs",
            "reason": "Density/temperature/spin-distribution formula requires excitation energy "
            "and/or fitted model parameters beyond N/Z; parameter tables are not "
            "direct density measurements",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "b66d5c8dee9983b386d6e89c67f900d43027d782f9498852d34b74719e796cb5",
                "README.md": "e4316c355214b3df96df1443b76752767e87d8ef7358164947ad5de6fc92ef06",
                "sources.bib": "19d6aa498cbe7e26631c9daded08582cc95ef9ab8535d7dd673daaab5dc83d18",
            },
        },
        {
            "id": "NF-0009",
            "name": "Constant-temperature level-density formula",
            "folder": "Constant_Temperature_Level_Density",
            "decision": "extra_excitation_or_model_inputs",
            "reason": "Density/temperature/spin-distribution formula requires excitation energy "
            "and/or fitted model parameters beyond N/Z; parameter tables are not "
            "direct density measurements",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "e56ffdb4548cd93bb481231ae7750386a14388b303985c59310daf74f6edace3",
                "README.md": "59b20501c7b41971e5c85347368b07b9e6ec904c1e0be322ae66a2d665b056be",
                "sources.bib": "e4600a87d76ca0e9879436d952ff883f73b502a2ed4a5217667955a68ed963ad",
            },
        },
        {
            "id": "NF-0010",
            "name": "Ignatyuk energy-dependent level-density parameter",
            "folder": "Ignatyuk_Energy_Dependent_Level_Density_Parameter",
            "decision": "extra_excitation_or_model_inputs",
            "reason": "Density/temperature/spin-distribution formula requires excitation energy "
            "and/or fitted model parameters beyond N/Z; parameter tables are not "
            "direct density measurements",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "6e27fa2351bfe74fca1fc25c98314c60e1e2f4ba11d23be289e9616922fabd89",
                "README.md": "2e962d15f12f579d2025206bd144fd780e0c72ded73ce520913a727fcaa702f6",
                "sources.bib": "ef1865a6664bf6e277c339ad0b1a3bd9db4f42740f975547727f6fda9e21cb81",
            },
        },
        {
            "id": "NF-0011",
            "name": "Geiger–Nuttall law",
            "folder": "Geiger_Nuttall_Law",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "bc82f76fcfe68e08c3ca06c1f2d8d225cb53305bce53326af7207eca0d5a28e8",
                "README.md": "fb3e23dec608fe9eaafa129a2bb3782521a457c92f5ada684ec88011fee356a1",
                "sources.bib": "aa0cd223b485617c5a901a5a28e7a50aaabf6110224e0559b31c83b47304e0cc",
            },
        },
        {
            "id": "NF-0012",
            "name": "Viola–Seaborg–Sobiczewski alpha-decay formula",
            "folder": "Viola_Seaborg_Sobiczewski_Formula",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "e13367501bf085a5e4b59800fcff884d448b5963988be09fedd632faffbc93ca",
                "README.md": "ea1df516d263ff38a18fe0cd39f394feb1d699d079219039b93f89f38f955eff",
                "sources.bib": "7412f4ef8f2c26bd3b38f756766e8cf51a832387148cd53784ad32fcdd97b422",
            },
        },
        {
            "id": "NF-0013",
            "name": "Royer alpha-decay formula",
            "folder": "Royer_Alpha_Decay_Formula",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "42a5089f7d1ccccb1c3d07e854b5f5c63e08cf898a5e24ecacef97481f4f6cb0",
                "README.md": "ac1a68a43a0f52e66f516d89a8c845f930f78e63d5e643790643c3f1b2c514f6",
                "sources.bib": "92ce4a9b763a82ed5b02ca1771ffccca9f9ebc1ed9c1eff7b1a16c1748430e72",
            },
        },
        {
            "id": "NF-0014",
            "name": "Universal decay law",
            "folder": "Universal_Decay_Law",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "d7841f8e5a4d0774af84f1c002d3296d41bb9209fbbe94751755dd8b3fb8d909",
                "README.md": "bc39423dbdcf487061b4c8c8860bcf1d89bef9defd42abbdd45f2840f2136338",
                "sources.bib": "48163e330e10127f025ae94d77772c13ea0a8c1449510d44195f0e86987e3b63",
            },
        },
        {
            "id": "NF-0015",
            "name": "Brown alpha-decay formula",
            "folder": "Brown_Alpha_Decay_Formula",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "53dd38ea47809d8025d4a72ffafdb1bf550390c48771999d5543157e5ec07dab",
                "README.md": "5a841cb22743c38b5c23d424604a3f4198f6478d4cf2e5a7505ca2d7793e2fa1",
                "sources.bib": "0e6a244e21975f4363b9b86da08eb08a497cd6b0b9dcbf1e4dbf69635b9170f8",
            },
        },
        {
            "id": "NF-0016",
            "name": "Fiset–Nix beta-decay half-life formula",
            "folder": "Fiset_Nix_Beta_Decay_Formula",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "8e16bcd5d13e0b50596b9c4c1f77d1009007e24559a6ec359dc413cc261b4b60",
                "README.md": "ce08c929be86203ca9a6e003cd02283707c3a96271eadfc808723462eb7270fd",
                "sources.bib": "31658c1e1c44d4376aca51e61e71db2182d5f2add4c081e961e0b567f29cf9d7",
            },
        },
        {
            "id": "NF-0017",
            "name": "Viola fission-fragment total kinetic energy systematics",
            "folder": "Viola_Fission_Fragment_TKE_Systematics",
            "decision": "eligible_deferred_source_scope",
            "reason": "N/Z expression is eligible but the original fissioning-system and TKE "
            "dataset conventions need further audit; no invented measured TKE labels",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "0bc1b5d061f3b945acab1588f3d998d7277bf6e307be011a1565784abcecf6e4",
                "README.md": "b13640515e7864be34d8dbd1d5bcf01bd58859b1102ec893dab62cb6cc976a3c",
                "sources.bib": "b70b2bfa1d99fe8483edd13898fcfb3d1acef08e403a3be2e42c1a9ce53eed8d",
            },
        },
        {
            "id": "NF-0018",
            "name": "Parkhomenko–Sobiczewski alpha-decay formula",
            "folder": "Parkhomenko_Sobiczewski_Alpha_Decay_Formula",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "ea4cda14d10ec908868865dd0f133148ff4188eea8efd0a5f839d987c6114688",
                "README.md": "1dce9b2039240b195b83a0c38d380308e4e371a927fdf9eaa5de40fb1fdf6f6e",
                "sources.bib": "4f5b5be6b2d8f7bdcfcdcf23f98bec6c2239cbc0293a4f36b628ee0df6eb57fe",
            },
        },
        {
            "id": "NF-0019",
            "name": "Ni–Ren–Dong–Xu unified decay formula",
            "folder": "Ni_Ren_Dong_Xu_Unified_Decay_Formula",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "3b99630bb656ebf122c65925c9b9833bcc288cd0d68e4dd919065b94e0553c68",
                "README.md": "4661028ddff48b23c62a1f70950cb4b13597dcd62f62174e33b368d1883cfaca",
                "sources.bib": "af1b7288b42370206cc62dcc95edb9576bd567bd825c731266076c9f5de0f9f9",
            },
        },
        {
            "id": "NF-0020",
            "name": "Horoi cluster-decay scaling law",
            "folder": "Horoi_Cluster_Decay_Scaling_Law",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "3f354cdd609669cfa33de3a6d2a48a173b0f3fd2ec6b875dc4b1afa9916c45cc",
                "README.md": "45c974e9016943e0fd6b1ec5106a65534f25c16443bfd0dd860bcd8380867ada",
                "sources.bib": "994f6099328b62dbd7a01c06b4eaeda4c6f492b3d2889a1247a11d1361e101ff",
            },
        },
        {
            "id": "NF-0021",
            "name": "Poenaru universal curve",
            "folder": "Poenaru_Universal_Curve",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "0780eea014733cee8a4b47903509b086889f39c744fec4537497cb59a3cc8ce3",
                "README.md": "5bb43365cea6938cb51bc902e54013460247640223885ad661c4076c0ffeca8d",
                "sources.bib": "c42b18e8fc1ba33d43f8c39c6fbd5d83bf7c1fb8137ad8fc8be08b250cc0f91d",
            },
        },
        {
            "id": "NF-0022",
            "name": "New Geiger–Nuttall law for proton radioactivity",
            "folder": "Proton_Radioactivity_New_Geiger_Nuttall_Law",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "d1bdb843004fd83fabfbe626b9bc1cbdef1997b6f2dda465c1e6838156dada4c",
                "README.md": "0c69ba70a4717f44b1cf81ee5dc95afee44fe3adc3ac31a5773a84ea417efcee",
                "sources.bib": "e7a31af16cdf98493bd1b7d3f50aa565917bb805d0796a4fafeb7bc90ed15f27",
            },
        },
        {
            "id": "NF-0023",
            "name": "Universal decay law for proton emission",
            "folder": "Universal_Decay_Law_for_Proton_Emission",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "f3fee2dbc82c78713992faccbf116ded23202bd27060243fbfae15b657da3b83",
                "README.md": "c13338285e07de797b7533707ad029aa064dd1d4bfd7bd00ed12caa55828ae03",
                "sources.bib": "18e1a53dfb4ab6e79684ae2180d5fbe5c26c1396589fcd0a864059a9ab51d03c",
            },
        },
        {
            "id": "NF-0024",
            "name": "Sargent beta-decay rule",
            "folder": "Sargent_Beta_Decay_Rule",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "9a4fc4d99290bb66a89429261a1c268f772b30cc4c537ed1bf8b1658a7189c57",
                "README.md": "56f0ee64ba0c4549fe7dd564091429cba42d298290c8df1297566de8f2584b47",
                "sources.bib": "d3aabcea060b8305db7b82ef989fb40bd1ea9264b58be18de0e27451e0455b79",
            },
        },
        {
            "id": "NF-0025",
            "name": "Phase-space empirical beta half-life formula",
            "folder": "Phase_Space_Empirical_Beta_Half_Life_Formula",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "475506b7e7186833090d56f049872d56a612a06947142d9f5e75df3e4ec75328",
                "README.md": "078d1382e9ae3e1c7aba5c8bf15de4e3927218cf75106b758d0374bcf20c7c8a",
                "sources.bib": "1f090ee88a58f8d51e4a5c9b13d675e86ef56e034804d7d31be2c064256577cc",
            },
        },
        {
            "id": "NF-0026",
            "name": "Unified semi-empirical beta-minus, beta-plus and EC formula",
            "folder": "Unified_Semi_Empirical_Beta_Decay_Formula",
            "decision": "extra_Q_or_decay_state_inputs",
            "reason": "Published decay expression requires measured Q, "
            "emitted-cluster/angular-momentum information or daughter state-density "
            "inputs; no measured lookup hidden as N/Z feature",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "7fa905a32b82ae157a6dc1b3d4ce2e852e445e0e9a3b9a6cf5b57870c2afa25f",
                "README.md": "635edd7fc003398ab8b96ba3f3e3d190bde515c4426208c3b06197ebc87608f2",
                "sources.bib": "77889af06de671a8df83b109e2700723f2001eec75257bbcec2015eb5e374e3f",
            },
        },
        {
            "id": "NF-0027",
            "name": "Xu–Ren–Wang spontaneous-fission formula",
            "folder": "Xu_Ren_Wang_Spontaneous_Fission_Formula",
            "decision": "observations_only_formula_deferred",
            "reason": "N/Z formula candidate has inconsistent year/source/unit attributions "
            "across later papers; ground-state partial fission lifetimes are "
            "independently admitted from NUBASE",
            "mapped_tasks": ["D05_logT_SF"],
            "metadata_sha256": {
                "formula.yaml": "534a708ef178a742dd3793b49686dede25624d9630bc3983464bb88cc167c323",
                "README.md": "afb9d7ad543c95c99dab30a089a0088ad424609e00adcd669a78184a2453f012",
                "sources.bib": "28633a4f4e993baee53a42f6693a5242d3b26a63ebc4effe1556ea7a45c7f0a1",
            },
        },
        {
            "id": "NF-0028",
            "name": "Modernized Świątecki–LSD spontaneous-fission formula",
            "folder": "Modernized_Swiatecki_LSD_Spontaneous_Fission_Formula",
            "decision": "extra_shell_mass_inputs",
            "reason": "Shell correction or mass residual is an additional measured/model table "
            "input; not a pure N/Z recovery answer",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "dd4786112aa7d51854f03b326b0146c70dacd8e8ec209c228211276028b926d6",
                "README.md": "196f36b923f6f88acdca2e47f14389f9ae9e91e73eecacc8ce45cf1603c16112",
                "sources.bib": "81c0303871ccc3e60a1a85b8f50798243590808f8963beff3a06554aa4c3a35b",
            },
        },
        {
            "id": "NF-0029",
            "name": "Bao shell-corrected spontaneous-fission formula",
            "folder": "Bao_Shell_Corrected_Spontaneous_Fission_Formula",
            "decision": "extra_shell_mass_inputs",
            "reason": "Shell correction or mass residual is an additional measured/model table "
            "input; not a pure N/Z recovery answer",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "f5aa6d15d5d8200a846d87a9bfa9eeeb115072c8faf91e814e20d31f0db5f35b",
                "README.md": "47dbbc64531875fdbdb412adeffe5e6238b4112d634b368a6922315afd230540",
                "sources.bib": "20cdbe81c58084c5c4999520f3ef00e731e40cc701467a761671a9708833dbe4",
            },
        },
        {
            "id": "NF-0030",
            "name": "KPS generalized Świątecki formula",
            "folder": "KPS_Generalized_Swiatecki_Formula",
            "decision": "extra_shell_mass_inputs",
            "reason": "Shell correction or mass residual is an additional measured/model table "
            "input; not a pure N/Z recovery answer",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "9152c6152aeedbf5d67065181bafc66489a0d08a7fbbb836c3590c5b793e2522",
                "README.md": "d805f6960d092fbf6b3118acb5cc9b58120eb82e1313d2b48a20bac0590d76de",
                "sources.bib": "4fd3ec62a0afd28585f3761886d29524f17729e639c4139d5d9e3dd88d710a29",
            },
        },
        {
            "id": "NF-0031",
            "name": "Five-Gaussian fission mass-yield representation",
            "folder": "Five_Gaussian_Fission_Mass_Yield_Representation",
            "decision": "extra_fission_system_or_energy",
            "reason": "Fission yield/spectrum requires the fissioning system, fragment "
            "coordinate and/or neutron energy; not a single ground-state N/Z scalar",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "de1e07d07b3db8a5a101d6820fb4711cbe105d4620e7bcd524ce398dbbdf94fe",
                "README.md": "dce8839ff3ee1427c4c3f2f518ffacfb2bffb1b3b9f647d6899613ba3f25676a",
                "sources.bib": "e765929f57b53d5a58bb9e646b0cc093d3fc3b72be61a9a58a066350e5d38e2f",
            },
        },
        {
            "id": "NF-0032",
            "name": "Wahl charge-distribution systematics",
            "folder": "Wahl_Charge_Distribution_Systematics",
            "decision": "extra_fission_system_or_energy",
            "reason": "Fission yield/spectrum requires the fissioning system, fragment "
            "coordinate and/or neutron energy; not a single ground-state N/Z scalar",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "e703fe00919dd6ceea3ae93111b6389715538ce3bfe0f84a44fff8d967f7c206",
                "README.md": "7c58ff135e4fe555a4dcd3be1849ce581b9b4e72513f95d4d3803074a22c9a92",
                "sources.bib": "e417a9693414fe7e2861a7f25138032cef273534eca59d576850edac750f7fd7",
            },
        },
        {
            "id": "NF-0033",
            "name": "Watt fission-neutron spectrum",
            "folder": "Watt_Fission_Neutron_Spectrum",
            "decision": "extra_fission_system_or_energy",
            "reason": "Fission yield/spectrum requires the fissioning system, fragment "
            "coordinate and/or neutron energy; not a single ground-state N/Z scalar",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "57394af8c24332c9fc2c86e0fc6a88c43a6f24d0e7023ada6640b18e333853c6",
                "README.md": "b0ea0e3626d426a96b6ff359f7ab8ad506b4ecad63ca6b2020ec386c4d582952",
                "sources.bib": "bffdf0cb4a46d73c0a9e18a7552dbb658646ce79edf23589463fbc9d31c7d864",
            },
        },
        {
            "id": "NF-0034",
            "name": "Madland–Nix prompt fission-neutron spectrum",
            "folder": "Madland_Nix_Prompt_Fission_Neutron_Spectrum",
            "decision": "extra_fission_system_or_energy",
            "reason": "Fission yield/spectrum requires the fissioning system, fragment "
            "coordinate and/or neutron energy; not a single ground-state N/Z scalar",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "5f9a1de92f04fd0b56bb07101f435a168e74cf7c17a88e72e173424ea2ab7fab",
                "README.md": "57bf776e32936d3561aa9e03b78675aa2549aa2b9426b820ca18aa12dc3aaa4a",
                "sources.bib": "09a1507c28716c7ec0cfad993ec788c366f6651f7b6c1c073f84f9deeddb6bd1",
            },
        },
        {
            "id": "NF-0035",
            "name": "Three-point odd–even mass-staggering indicator",
            "folder": "Three_Point_Odd_Even_Mass_Staggering",
            "decision": "already_covered",
            "reason": "Three-point indicators and exact primitive-mass embargo already present; "
            "catalogue sum is not a new independent dataset",
            "mapped_tasks": ["B06_OES3n", "B07_OES3p"],
            "metadata_sha256": {
                "formula.yaml": "816660b1186ca2b6e4ec1f0a423bf55064e9bb1edd5badb5f6bfd56f292e82dd",
                "README.md": "9d168aa243e025f537caec46e4f91eddd0535012d96350a6a0b53d238b44375a",
                "sources.bib": "db3359bb85afabc8d21201be92a7a40e6e900591206cfc96a1f5f65c8ca07962",
            },
        },
        {
            "id": "NF-0036",
            "name": "Classical 12/sqrt(A) pairing-gap systematics",
            "folder": "Classical_12_over_SqrtA_Pairing_Gap",
            "decision": "admitted_reference",
            "reason": "Traditional average pairing-gap reference verified against Eq16 of the "
            "primary 2003 BCS paper; not asserted to equal OES3 exactly",
            "mapped_tasks": ["A48_pairing_classical"],
            "metadata_sha256": {
                "formula.yaml": "1eb509ded741d7f0fbff0a7be856115bf310bdc2802ac7d538bd79dc52bd4ccb",
                "README.md": "7613f726f2e65e76ed0fc9877110499c10c60fe2760d75759a4a427279427926",
                "sources.bib": "7192c1f72622b7f76250f945de0b9f6cd7b77c8aa802dc743c484955fe9d3c5f",
            },
        },
        {
            "id": "NF-0037",
            "name": "Vogel isospin-dependent pairing formula",
            "folder": "Vogel_Isospin_Dependent_Pairing_Formula",
            "decision": "admitted_reference",
            "reason": "Vogel parameterization cross-checked in primary 2003 Eq16; original "
            "credit retained; conservative benchmark-domain restriction",
            "mapped_tasks": ["A49_pairing_Vogel"],
            "metadata_sha256": {
                "formula.yaml": "a3aadc89acadccb5cda661731e5f2eb6d31296378078e8b4385d44f5974f147d",
                "README.md": "3e8368d9782600e5d85ea31b9744a9cd13d28f8322c6ec922fd8872d02eef1da",
                "sources.bib": "8aa1172bb5b2aadb4a6b9ac3ba6a28908f994c50fbe6b00d6649fa2379ea1f5d",
            },
        },
        {
            "id": "NF-0038",
            "name": "Nerlo-Pomorska–Pomorski charge-radius formula",
            "folder": "Nerlo_Pomorska_Pomorski_Charge_Radius_Formula",
            "decision": "related_structure_deferred_coefficients",
            "reason": "Finite-size/isospin radius structure already covered; source-specific "
            "printed coefficients/convention not newly certified from this catalogue",
            "mapped_tasks": ["A07_R_finite"],
            "metadata_sha256": {
                "formula.yaml": "274eb03cb51eed7bb5ede035a47b9198a915ad56cb8aeba0633fd0c18e90804a",
                "README.md": "38b872132f48c6cb87f74d78506c3ba65977b1c586a4b394eb76cf7f3dfae90a",
                "sources.bib": "edb7ae09b5806f7ffb0396d0c16e684b2c2c80f77801ad6b791fa0c007267fb0",
            },
        },
        {
            "id": "NF-0039",
            "name": "Royer–Rousseau charge-radius formula",
            "folder": "Royer_Rousseau_Charge_Radius_Formula",
            "decision": "related_structure_deferred_convention",
            "reason": "Related inverse-power/isospin radius structures already represented; "
            "original sharp/rms radius convention needs source-specific check",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "baf078d67d333cfc16fd4e0e41d6bc5c7221ff2f4a1f1f5263d9c3ed105bb27e",
                "README.md": "f907e10cbac3b04442850ced08aef2a0fef5c3b9cc1f75b3203a2beca79d1c2d",
                "sources.bib": "9725a2a390153511e6788ea8f9b21f6a68f673019079e0e1ca233a0ab88d2e45",
            },
        },
        {
            "id": "NF-0040",
            "name": "Two-parameter Fermi charge-density distribution",
            "folder": "Two_Parameter_Fermi_Charge_Density",
            "decision": "extra_radial_or_momentum_coordinate",
            "reason": "Charge density/form factor/potential is a function of r or q and "
            "nucleus-dependent shape parameters, not N/Z alone",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "09e693b225667a16da44d6abfb2f48c98f5831da2b064da36d10b226bbab3fed",
                "README.md": "3b301cd96dec7b39c4a7294a7d186f7b2fc246afde6d97fd7fc6ce9f256d6dab",
                "sources.bib": "6dd8a95a30c03c60059fe25dccab1763f127ffcfe7b3532b73d9a537a531c23a",
            },
        },
        {
            "id": "NF-0041",
            "name": "Helm nuclear form factor",
            "folder": "Helm_Nuclear_Form_Factor",
            "decision": "extra_radial_or_momentum_coordinate",
            "reason": "Charge density/form factor/potential is a function of r or q and "
            "nucleus-dependent shape parameters, not N/Z alone",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "52bb5d786578289613372117997c4654c5250d02fc7daf08d00e83a8c1988e80",
                "README.md": "e35ed9fd7a339ded4b4975b51e41c3ff877a1aae99ec461c4436304dc2229468",
                "sources.bib": "4dc023b75d4b2a73eacf4718d3032a480159ec2fec28d4b055247213a9534c1b",
            },
        },
        {
            "id": "NF-0042",
            "name": "Woods–Saxon mean-field potential",
            "folder": "Woods_Saxon_Mean_Field_Potential",
            "decision": "extra_radial_or_momentum_coordinate",
            "reason": "Charge density/form factor/potential is a function of r or q and "
            "nucleus-dependent shape parameters, not N/Z alone",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "0ed3d5c50369eac2bae476344519ffdab1e7d2357ac139bcddb34e7430f74f2c",
                "README.md": "88171e2a2d2f9183d11d491e187d2ec802de38098a684c5bd8aa28ea22c75be5",
                "sources.bib": "628561a65404945484ec390862869a3c9daad9f722d7f6994599466b1750d38e",
            },
        },
        {
            "id": "NF-0043",
            "name": "Rigid-rotor energy formula",
            "folder": "Rigid_Rotor_Energy_Formula",
            "decision": "extra_spin_and_inertia",
            "reason": "Variable spin/K and nucleus-dependent moment of inertia exceed the "
            "N/Z-only input contract",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "5410b460c7404cb9fa686aa48dbe953b402aa2d3d92931b76793e085e1395565",
                "README.md": "621e299d2e57973f8f500d556215a6611eb03ba6177240f22cba56783b6aa7ab",
                "sources.bib": "c0fdad9a1ffa80c9ec67bc185ac06dcca988d9d9f28d13f345c1011c4371b08f",
            },
        },
        {
            "id": "NF-0044",
            "name": "Harmonic quadrupole-vibrator formula",
            "folder": "Harmonic_Quadrupole_Vibrator_Formula",
            "decision": "constant_not_discovery",
            "reason": "Fixed ideal vibrator R42=2 is a physical reference, not a nontrivial SR "
            "rediscovery task",
            "mapped_tasks": ["B15_R42"],
            "metadata_sha256": {
                "formula.yaml": "558a557726d76bcd2b6e7673ee4dae5aeda161cd877d1e999b1050b6dd5c8ae4",
                "README.md": "2a71a78cc1eb43e9bae0b6dd7dfe7178286cd5731bdb149bb827f13026aa50bf",
                "sources.bib": "2c37ffa937761b57a7d13f86946530a50d7fdeaf58037213f1aa720cd6c026aa",
            },
        },
        {
            "id": "NF-0045",
            "name": "R4/2 collectivity systematics",
            "folder": "R4_over_2_Collectivity_Systematics",
            "decision": "already_covered",
            "reason": "Measured R42 already included; ideal ratios are diagnostic limits, not "
            "new independent expressions",
            "mapped_tasks": ["B15_R42"],
            "metadata_sha256": {
                "formula.yaml": "b42f6a412b9360c6823ff74967ef450acddcc36506bb658742d0e9b74b8cb291",
                "README.md": "56b43612b11d3907c6384386ad97f6d00b3e75fca426b113fc9bb8567e9e32c6",
                "sources.bib": "67f70bafa05d29e858e8e655e61003a86e4ef1057d6384bea1dcacec5560c87f",
            },
        },
        {
            "id": "NF-0046",
            "name": "Weisskopf single-particle electromagnetic estimate",
            "folder": "Weisskopf_Single_Particle_Electromagnetic_Estimate",
            "decision": "deferred_convention_conflict",
            "reason": "Catalogue general expression gives E2 coefficient about0.0594, while "
            "separate downward prose quotes0.297; transition-direction/unit convention "
            "requires original-source resolution",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "730f903d34e78998d0910abf7cf06b9ae68bd6eee69602658d0d4dcff7dc92d4",
                "README.md": "04f27eced464691b5d4fec2e5e9c24a0082436ac2d985643f972c005ac6ee05b",
                "sources.bib": "e512c7ca8a0aea18853add4896235729ee48969ff45535828d757ed89ff1da51",
            },
        },
        {
            "id": "NF-0047",
            "name": "Rotational B(E2) and Alaga rule",
            "folder": "Rotational_BE2_Alaga_Rule",
            "decision": "extra_intrinsic_state_inputs",
            "reason": "Intrinsic quadrupole moment and spin/Clebsch-Gordan state information are "
            "extra inputs",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "f033451c02cb2eee3d93977bc036ce2bf6cd408783faf6dfd7134013c13ef13e",
                "README.md": "035dd4848515041381dff02bbac9b4f3601a2c93f8e1a361a2f047072780eac5",
                "sources.bib": "0211076bbb40c5123ad8a6c89914ab7332e15807ebb7596167c4e6b516e08fb0",
            },
        },
        {
            "id": "NF-0048",
            "name": "B(E2)-to-beta2 deformation relation",
            "folder": "BE2_to_Beta2_Deformation_Relation",
            "decision": "derived_not_independent",
            "reason": "A beta2 magnitude derived from the same BE2 requires a shape convention "
            "and is not an independent deformation measurement; not multiplied into "
            "another primary task",
            "mapped_tasks": ["B11_BE2"],
            "metadata_sha256": {
                "formula.yaml": "5742a03bc26807f03fb37ec7d0e6df2d1dd43c4d89f3b0f80b27ea81419a86cb",
                "README.md": "4115ff1db5097b318438fc7f877bc94cef4cb965538b9ac44a7d4edf85c85df8",
                "sources.bib": "54c451eac10cc4437218ed99e71f7e6540dc1494fecad098775471707519be68",
            },
        },
        {
            "id": "NF-0049",
            "name": "Back-shifted Fermi-gas level-density formula",
            "folder": "Back_Shifted_Fermi_Gas_Level_Density",
            "decision": "extra_excitation_or_model_inputs",
            "reason": "Density/temperature/spin-distribution formula requires excitation energy "
            "and/or fitted model parameters beyond N/Z; parameter tables are not "
            "direct density measurements",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "379165497c9f499e2ec78c3ac424efdd2cb3ec82f3d46cacdf8dc89ee1ecb1ad",
                "README.md": "b146b57a6a215e60338e9d2cef8d331950412f2212d650edd84dbce39c7bdde1",
                "sources.bib": "d1bdd140fe099deecae394111f4c46fa6450cfa3df8a1af86886fde652504684",
            },
        },
        {
            "id": "NF-0050",
            "name": "Gilbert–Cameron composite level-density formula",
            "folder": "Gilbert_Cameron_Composite_Level_Density",
            "decision": "extra_excitation_or_model_inputs",
            "reason": "Density/temperature/spin-distribution formula requires excitation energy "
            "and/or fitted model parameters beyond N/Z; parameter tables are not "
            "direct density measurements",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "9c99d123dcce8d5fdd3ff9fc3ee6da7818c97bba7177c1e5be2a6f1596ee50cf",
                "README.md": "621a5cc4092b9679ec3f8b4a2ba68e296e3db67bb831b3546994d100988340d6",
                "sources.bib": "ac200ac8d441836e7c77f7bb1f63a07931bcb04d1c72e1e1a04513823898ab67",
            },
        },
        {
            "id": "NF-0051",
            "name": "Ericson spin-cutoff distribution",
            "folder": "Ericson_Spin_Cutoff_Distribution",
            "decision": "extra_excitation_or_model_inputs",
            "reason": "Density/temperature/spin-distribution formula requires excitation energy "
            "and/or fitted model parameters beyond N/Z; parameter tables are not "
            "direct density measurements",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "cfa3c5016178dad0e73b6d40637a5c2a0590a0d5ee2b7ba1a3af1659622fdb8a",
                "README.md": "add3e0841b312197a5eb2d0f450d63039c4b16a6647ca084dfc417d87b823627",
                "sources.bib": "65c33c890803f70130469a5efb7d9e29ef3fd6299416bf612e18abf546cef84f",
            },
        },
        {
            "id": "NF-0052",
            "name": "Giant dipole resonance centroid systematics",
            "folder": "Giant_Dipole_Resonance_Centroid_Systematics",
            "decision": "admitted_reference_and_parameters",
            "reason": "2005 mass scaling and 2018 isovector GDR forms verified from primary RIPL "
            "handbook/readme; only In=1 experimental-fit recommendations admitted as "
            "parameter labels",
            "mapped_tasks": [
                "A42_GDR_centroid_2005",
                "A45_GDR_centroid_SLO2018",
                "A46_GDR_centroid_SMLO2018",
                "B37_GDR_E_centroid",
            ],
            "metadata_sha256": {
                "formula.yaml": "b0759b77c8578f7f05a31fc16cbb0071b71b15f43327635f8d8822c8622d5a50",
                "README.md": "14ccbf1589b4f429b6225f337b9836e031cb44ca9b79244b4bf7c1745b638334",
                "sources.bib": "cf73dd1bfc70dd1b1b424a1a52d8e2f0179fed7ab8898e5717d4e4d453116c75",
            },
        },
        {
            "id": "NF-0053",
            "name": "Brink–Axel standard Lorentzian gamma-strength function",
            "folder": "Brink_Axel_Standard_Lorentzian",
            "decision": "extra_photon_energy_or_temperature",
            "reason": "Strength function requires photon energy/temperature and resonance "
            "parameters; scalar GDR parameters are admitted separately",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "7ad02379c9499d60980ec30cccf94fe72f48eb503af466fc901095bbec00bfdc",
                "README.md": "5d3be07694af1b4d0819c22d201ef003899be5a2d6a6d18025a0c162fac72781",
                "sources.bib": "5a59c269d15ee0938c5f5996488f7a371ba432c151e55877f95d98f128fd6194",
            },
        },
        {
            "id": "NF-0054",
            "name": "Kopecky–Uhl generalized Lorentzian",
            "folder": "Kopecky_Uhl_Generalized_Lorentzian",
            "decision": "extra_photon_energy_or_temperature",
            "reason": "Strength function requires photon energy/temperature and resonance "
            "parameters; scalar GDR parameters are admitted separately",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "5ed0854e98b34f155b8db2ad1bd2fdd74e258fff6bd13f35e673fde2ae404d03",
                "README.md": "dedf8143a293ce66444f0cae5f63cb8f2719c6a5875f3bcd7fa1dfc54d2c2832",
                "sources.bib": "fb65884313a5b3b88bb62ba0cb5b50a86fe98eb79adae3195bb28e952196f249",
            },
        },
        {
            "id": "NF-0055",
            "name": "Thomas–Reiche–Kuhn nuclear dipole sum rule",
            "folder": "TRK_Nuclear_Dipole_Sum_Rule",
            "decision": "admitted_analytic_reference",
            "reason": "Unenhanced TRK sum rule fixed kappa=0; analytic reference without "
            "asserted experimental integrated strength",
            "mapped_tasks": ["A50_TRK_sum"],
            "metadata_sha256": {
                "formula.yaml": "6700e68b471c330859537d1f7785d6652e785ddace3e8e6094ea01cbcd0e55a6",
                "README.md": "facf4ef587e61b4b03ceeeb16806f3e612a2c007954f10af1e51e8e4404b52db",
                "sources.bib": "5ec1730f4379ab434bb0f2a83c2e7b8982fe90a5dcd2ffc3457d5593bd2cb4b8",
            },
        },
        {
            "id": "NF-0056",
            "name": "Isoscalar giant-monopole-resonance energy systematics",
            "folder": "Isoscalar_Giant_Monopole_Resonance_Systematics",
            "decision": "eligible_deferred_observable",
            "reason": "Simple N/Z scaling is eligible but source-specific monopole centroid "
            "definitions and an audited measured set are not provided here; same A "
            "power is already represented",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "f442c83f6d93bbc6382138fb9f4502ec364f6532734512d26c9433ea100f81ae",
                "README.md": "739ff8c973540fa037290f9ca49e11b78b8a8e90b3bd2e5b032b5d41374b8a9b",
                "sources.bib": "cfd9c717fcdeae38da5012b95495aeef2ccf0d360123c7fea0966723a4c980bc",
            },
        },
        {
            "id": "NF-0057",
            "name": "Isoscalar giant-quadrupole-resonance energy systematics",
            "folder": "Isoscalar_Giant_Quadrupole_Resonance_Systematics",
            "decision": "eligible_deferred_coefficient",
            "reason": "Quoted coefficient range63-65 is not one frozen standard answer; "
            "source-specific centroid definition and data require further review",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "51ba44f076e357eef07fea2ac460b4164af360ca0fed58324c531732cf4bd81d",
                "README.md": "7a088d27895110f721d689da2b8551d124b9eeffeac9bb544c9dc09c36f29fa7",
                "sources.bib": "000ae097fa1c53f99470c83dd770a3d38af96e074d82cdbe05fbd49a093f73eb",
            },
        },
        {
            "id": "NF-0058",
            "name": "Kalbach–Mann double-differential continuum systematics",
            "folder": "Kalbach_Mann_Double_Differential_Systematics",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "322bd106c6765b32051d96e17ce9e67ac2691f9d666bd23d07f6735e5f4fc8c4",
                "README.md": "186abd0ed59d63091ddb0358319e50a776debb72d8419ee820c2694192d11769",
                "sources.bib": "f15fc82c97f20ea0666225ed9abee78d3061fe359c600b97beadafcb56de3d6a",
            },
        },
        {
            "id": "NF-0059",
            "name": "Wong fusion cross-section formula",
            "folder": "Wong_Fusion_Cross_Section_Formula",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "91265121d0fc48ac59e1eecb574ebfa54cbd026b1dcf3838d6c409217a66f606",
                "README.md": "bddcec7e73864f66fceede2b4007f60cb1f83687f5acf867ae3883d739786b92",
                "sources.bib": "be43dfb530cb90c5533e9bbce8f35d82eb670e42380cebad2bd733a4793e9e5d",
            },
        },
        {
            "id": "NF-0060",
            "name": "Kox total reaction cross-section formula",
            "folder": "Kox_Total_Reaction_Cross_Section_Formula",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "b84aa4cbf6f22d01a478892b6650329c8db24a9a36286cd506fb6cdd5e5ff3e4",
                "README.md": "716d13c85c2cd11206ca674948fb6103ad41b5ecaee50da790a2855f5d7a39c8",
                "sources.bib": "38795d8a615977177d40b9214b396a9db9088e4201ce14873290466d69d15052",
            },
        },
        {
            "id": "NF-0061",
            "name": "Shen total reaction cross-section formula",
            "folder": "Shen_Total_Reaction_Cross_Section_Formula",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "edc193029c7cdea36aa3d08504b9a86eb78b9aa0c4d068284b2a900b81e4136f",
                "README.md": "4c76b161b1bef5591db968baf407bc2157d9b5760d1576dd78f51b66d8930f73",
                "sources.bib": "47e2aea312c65f9de0f71146e1ab2d74a85e598361b4a08e6b3e8b8caadece60",
            },
        },
        {
            "id": "NF-0062",
            "name": "Tripathi–NASA reaction cross-section formula",
            "folder": "Tripathi_NASA_Reaction_Cross_Section_Formula",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "f1a918e18b313852409b9357003849ebc129f4cca765f7ff8dc80c867612295c",
                "README.md": "b70d49662f522210b7d7169ebb338b7e682aca10484b54b94d07420f8b2fb8e2",
                "sources.bib": "2bc26a1b853b251811a5ce39fc89e704b370d4aee34d37a0a062b3dc988e0d48",
            },
        },
        {
            "id": "NF-0063",
            "name": "Koning–Delaroche global nucleon optical model",
            "folder": "Koning_Delaroche_Global_Optical_Model",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "9cff02f6957b842416aa4854b877244ac1171452469a36a34607e4e965d5bbcc",
                "README.md": "dff90a03722d4ac92677755c54382e299cabee19c189be32638fcc14f62e465e",
                "sources.bib": "992ea5d53e140bb25e3f1bc6bd2834097052c06cb6ff71de3bbd9b09b87fa43d",
            },
        },
        {
            "id": "NF-0064",
            "name": "Chapel Hill 1989 global nucleon optical model",
            "folder": "Chapel_Hill_1989_Global_Optical_Model",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "e55b61ebbac112e9e0a9e4b65e284e051a055dafd1ff6f0ff479d50d66c76e6b",
                "README.md": "093390ed043b0cf46a24dbd0eda8c6c029671109dc281985d5c104705917a64c",
                "sources.bib": "deadc4e08d4e337ea508daa86d87992474a24d170a51c29e2193be194e7fa8fc",
            },
        },
        {
            "id": "NF-0065",
            "name": "McFadden–Satchler alpha optical potential",
            "folder": "McFadden_Satchler_Alpha_Optical_Potential",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "66c99ce817223356873465e7791087aa55d5d60cd2ec751e65919246561f122f",
                "README.md": "eb7837c0405184a26688a00e2fe36bd2dbffa4e532fc6b80435d4d4a3f56889d",
                "sources.bib": "21944a7eafb116dfd1177cd712261f61aa41c959774d53c67a3cbf47a26d8d4b",
            },
        },
        {
            "id": "NF-0066",
            "name": "JLM semi-microscopic folding optical potential",
            "folder": "JLM_Semi_Microscopic_Folding_Optical_Potential",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "e878d0e3d50f25fb6dda00908135bb631929cc38c3ad2cf14d1ee9e20e63ce41",
                "README.md": "752a3a8ec9178f7b802dd7ffd8de1010cf4891d9339161e98a062ce8b720ee9a",
                "sources.bib": "c145cdc9280cfe7d05ea95c7fa660580a5fa8b33da66b958a75249742f3e7c24",
            },
        },
        {
            "id": "NF-0067",
            "name": "JINA REACLIB seven-parameter reaction-rate formula",
            "folder": "JINA_REACLIB_Seven_Parameter_Rate",
            "decision": "reaction_or_temperature_inputs_outside_core",
            "reason": "Cross section/optical potential/rate needs incoming energy, "
            "projectile/target, radial coordinate or plasma temperature; current NuSR "
            "has only N/Z",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "e71ad5112546054b5b7886f35e4db1c5056b599bb3199c2a27292e3cd06c18ab",
                "README.md": "1cc96277b58876ab05794615c75433b36db593ea7f85dff207df17f28d98600c",
                "sources.bib": "814c0652d007a0ecb0a1b43f21fcb7859352cba81455ce9402c882d2aff6c15b",
            },
        },
        {
            "id": "NF-0068",
            "name": "Goldhaber fragmentation momentum-width formula",
            "folder": "Goldhaber_Fragment_Momentum_Width",
            "decision": "reaction_kinematics_outside_core",
            "reason": "Projectile/source, fragment momentum, yield ratios or thermal parameters "
            "are independent information; no artificial fixation to inflate task "
            "counts",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "e7b25cc04aca025cb44666dab09e9403286d9fa2bc745921f5feeaf197ff2e7a",
                "README.md": "3cbd7b9c4f807f1ba5b7b77edfd2ec913ef894c8f31573caa86af8db98ed4202",
                "sources.bib": "158fb75821f3245aeeafd32b239ddae93ebf8dbe5c558b2223ae25560728c0ec",
            },
        },
        {
            "id": "NF-0069",
            "name": "Morrissey projectile-fragment momentum-width systematics",
            "folder": "Morrissey_Fragment_Momentum_Width_Systematics",
            "decision": "reaction_kinematics_outside_core",
            "reason": "Projectile/source, fragment momentum, yield ratios or thermal parameters "
            "are independent information; no artificial fixation to inflate task "
            "counts",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "8b3211fd6c0952d306e1e892f270cfb7bfa71305059ef5ad750754450c5334f8",
                "README.md": "6911d4d4f417bae4b071a80531a3b20b707755996ccbb823f548a050ef754bd9",
                "sources.bib": "944dde78bd6861ff4d309bb6f2dc27b3ac805ca1b983300d32837a1cc577675d",
            },
        },
        {
            "id": "NF-0070",
            "name": "EPAX projectile-fragmentation parameterization",
            "folder": "EPAX_Projectile_Fragmentation_Parameterization",
            "decision": "reaction_kinematics_outside_core",
            "reason": "Projectile/source, fragment momentum, yield ratios or thermal parameters "
            "are independent information; no artificial fixation to inflate task "
            "counts",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "bb0b93123b084911ecac1d5047bf912397e126e7852b27f6aee78bf0b2617509",
                "README.md": "2e424a0eeb6b8d444d085235075de0a6c430717a15df8ce2a38e71d998ed6883",
                "sources.bib": "d794247a7fd356fa2eeed805e1116a907b6af168f5e6df2e25f491455aba7416",
            },
        },
        {
            "id": "NF-0071",
            "name": "Isoscaling yield-ratio formula",
            "folder": "Isoscaling_Yield_Ratio_Formula",
            "decision": "reaction_context_outside_core",
            "reason": "Fixed-source isoscaling can be a function of fragment N/Z, but "
            "reaction-source pair and yield data define another product scope; no "
            "silently fixed experimental context",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "1f99d49da9a249ff2d330776611f94ddd3bc46fa3d9216aafde2657dabaeaa53",
                "README.md": "dd9e82be5756e862de5f953b1531e322137f4bf1b553441ff223d4afeb1c4077",
                "sources.bib": "44d92e4f4529d475318666430d648261609d6390c8906be439b0045e44416cb3",
            },
        },
        {
            "id": "NF-0072",
            "name": "Albergo double-isotope thermometer",
            "folder": "Albergo_Double_Isotope_Thermometer",
            "decision": "reaction_kinematics_outside_core",
            "reason": "Projectile/source, fragment momentum, yield ratios or thermal parameters "
            "are independent information; no artificial fixation to inflate task "
            "counts",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "74b3ad8ca12f27cc824795ed4ec62b0c4053d5d18c496757a492f7262f7c932e",
                "README.md": "8d4b589a4ff521d1ca17b6eb8b6f5c863694609f6b9938ee72ecc401989c62eb",
                "sources.bib": "5bb1103a195c8ca8050d1c475acf83d5837885011e02ae7082e371b3f1e57964",
            },
        },
        {
            "id": "NF-0073",
            "name": "Light-nucleus coalescence formula",
            "folder": "Light_Nucleus_Coalescence_Formula",
            "decision": "reaction_kinematics_outside_core",
            "reason": "Projectile/source, fragment momentum, yield ratios or thermal parameters "
            "are independent information; no artificial fixation to inflate task "
            "counts",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "56670dae88baed549681a67c1643c11369e62afcef10f11f5a1896d4e2555606",
                "README.md": "2711478cf62580e63181a15aabc15f33ccffd3396538b72994bfcac4919a75a6",
                "sources.bib": "231ee1f9f4bc16ba0ea4487b8bcf3062165bf6db4954d9f7c52cdbd28744a83b",
            },
        },
        {
            "id": "NF-0074",
            "name": "Blast-wave transverse-momentum spectrum",
            "folder": "Blast_Wave_Transverse_Momentum_Spectrum",
            "decision": "reaction_kinematics_outside_core",
            "reason": "Projectile/source, fragment momentum, yield ratios or thermal parameters "
            "are independent information; no artificial fixation to inflate task "
            "counts",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "63f4d7eadb42519c7aa0987a8b601c16a865d22224a151f564268a5be0b692b6",
                "README.md": "fcb07dfe08bc77d023138e6fac3877bbe6d7aac1de97423db4a252d7bdda583e",
                "sources.bib": "c9fbf02398d6571d24f9e13c4220c443b49151926bf31eea953b38314a4627b5",
            },
        },
        {
            "id": "NF-0075",
            "name": "Nuclear-matter EOS expansion around saturation",
            "folder": "Nuclear_Matter_EOS_Saturation_Expansion",
            "decision": "matter_density_outside_core",
            "reason": "Bulk matter density/composition is an independent variable; not a "
            "finite-nucleus N/Z task",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "52fbb13c0fb38598df4ca18a2181ac676161da221716d07efe8dd3c4c6565b59",
                "README.md": "1c2455e4692de840f54d25d7662e1aae1045d0ff875ae1e2233f25125da69392",
                "sources.bib": "c547347f06adfc643d84234dce765c441d399937882d8d3caf4b2c1f77f7972e",
            },
        },
        {
            "id": "NF-0076",
            "name": "Symmetry-energy power-law parameterization",
            "folder": "Symmetry_Energy_Power_Law_Parameterization",
            "decision": "matter_density_outside_core",
            "reason": "Bulk matter density/composition is an independent variable; not a "
            "finite-nucleus N/Z task",
            "mapped_tasks": [],
            "metadata_sha256": {
                "formula.yaml": "16cd4a33ec9acf912a13c6bb1feb3d2b57b6f4fce69cc80599ffa17688c5035b",
                "README.md": "81c0a269b20ff8f4df1e703cb7b3c9d86e31b60bd3c7f27ede82f4eeb7c18102",
                "sources.bib": "bdab6acda163d16d7d45a5ae98e27dc4ab035fdfbbddfda157d7f0c71adde779",
            },
        },
    ],
}
