# Task inventory

Frozen release 1.0.0. Counts are task rows, not independent measurements. All data and split links below are relative to this repository.

## A. Published expression recovery

| ID | Observable | Rows | Family | Data / partitions |
| --- | --- | ---: | --- | --- |
| A01_BW | B (MeV) | 2020 | liquid_drop | [CSV](data/A01_BW.csv) / [IDs](splits/A01_BW.json) |
| A02_BWM | B (MeV) | 2020 | liquid_drop | [CSV](data/A02_BWM.csv) / [IDs](splits/A02_BWM.json) |
| A03_MISR1_B | B (MeV) | 939 | misr | [CSV](data/A03_MISR1_B.csv) / [IDs](splits/A03_MISR1_B.json) |
| A04_R_A | Rch (fm) | 880 | radius_scaling | [CSV](data/A04_R_A.csv) / [IDs](splits/A04_R_A.json) |
| A05_R_Z | Rch (fm) | 880 | radius_scaling | [CSV](data/A05_R_Z.csv) / [IDs](splits/A05_R_Z.json) |
| A06_R_I | Rch (fm) | 880 | radius_isospin | [CSV](data/A06_R_I.csv) / [IDs](splits/A06_R_I.json) |
| A07_R_finite | Rch (fm) | 880 | radius_isospin | [CSV](data/A07_R_finite.csv) / [IDs](splits/A07_R_finite.json) |
| A08_R_collective | Rch (fm) | 880 | radius_valence | [CSV](data/A08_R_collective.csv) / [IDs](splits/A08_R_collective.json) |
| A09_R_pairing | Rch (fm) | 880 | radius_valence | [CSV](data/A09_R_pairing.csv) / [IDs](splits/A09_R_pairing.json) |
| A10_MISR1_R | Rch (fm) | 315 | misr | [CSV](data/A10_MISR1_R.csv) / [IDs](splits/A10_MISR1_R.json) |

Expressions use fixed published coefficients. The fitting target is formula-generated `y`; `observed_y` is experimental context only. See [FORMULAS.md](FORMULAS.md) for all conventions.

## B. Evaluated observable prediction

| ID | Observable | Rows | Unit | Data / partitions |
| --- | --- | ---: | --- | --- |
| B01_B | B | 2457 | MeV | [CSV](data/B01_B.csv) / [IDs](splits/B01_B.json) |
| B02_S2n | S2n | 2232 | MeV | [CSV](data/B02_S2n.csv) / [IDs](splits/B02_S2n.json) |
| B03_S2p | S2p | 2151 | MeV | [CSV](data/B03_S2p.csv) / [IDs](splits/B03_S2p.json) |
| B04_Sn | Sn | 2314 | MeV | [CSV](data/B04_Sn.csv) / [IDs](splits/B04_Sn.json) |
| B05_Sp | Sp | 2268 | MeV | [CSV](data/B05_Sp.csv) / [IDs](splits/B05_Sp.json) |
| B06_OES3n | OES3n | 2192 | MeV | [CSV](data/B06_OES3n.csv) / [IDs](splits/B06_OES3n.json) |
| B07_OES3p | OES3p | 2105 | MeV | [CSV](data/B07_OES3p.csv) / [IDs](splits/B07_OES3p.json) |
| B08_delta2n | delta2n | 2031 | MeV | [CSV](data/B08_delta2n.csv) / [IDs](splits/B08_delta2n.json) |
| B09_delta2p | delta2p | 1846 | MeV | [CSV](data/B09_delta2p.csv) / [IDs](splits/B09_delta2p.json) |
| B10_Rch | Rch | 884 | fm | [CSV](data/B10_Rch.csv) / [IDs](splits/B10_Rch.json) |
| B11_BE2 | BE2 | 417 | e^2 fm^4 | [CSV](data/B11_BE2.csv) / [IDs](splits/B11_BE2.json) |
| B12_E2plus | E2plus | 509 | MeV | [CSV](data/B12_E2plus.csv) / [IDs](splits/B12_E2plus.json) |
| B13_E4plus | E4plus | 368 | MeV | [CSV](data/B13_E4plus.csv) / [IDs](splits/B13_E4plus.json) |
| B14_E3minus | E3minus | 99 | MeV | [CSV](data/B14_E3minus.csv) / [IDs](splits/B14_E3minus.json) |
| B15_R42 | R42 | 368 | 1 | [CSV](data/B15_R42.csv) / [IDs](splits/B15_R42.json) |

`OES3n/p` are three-point odd-even mass staggering, `delta2n/p` are two-nucleon shell gaps, `E2plus/E4plus/E3minus` are the first definite states of those spins, and `R42=E4plus/E2plus`. None asserts an exact unknown physical expression.

## Retained train / validation / test counts

Each cell is train/validation/test after dependency purging. Purged IDs and counts are retained in the JSON. An asterisk means insufficient coverage and disabled scoring; no substitute split is selected.

| Task | iid101 | isotope101 | isotone101 | neutron_edge | proton_edge | shell_N | shell_Z |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A01_BW | 1210/394/416 | 1310/302/408 | 1333/358/329 | 1152/434/434 | 1158/431/431 | 1304/310/406 | 1074/380/566 |
| A02_BWM | 1210/394/416 | 1310/302/408 | 1333/358/329 | 1152/434/434 | 1158/431/431 | 1304/310/406 | 1074/380/566 |
| A03_MISR1_B | 561/188/190 | 635/145/159 | 612/137/190 | 535/202/202 | 555/192/192 | 495/186/258 | 397/226/316 |
| A04_R_A | 520/186/174 | 536/175/169 | 549/186/145 | 558/161/161 | 656/112/112 | 587/120/173 | 493/128/259 |
| A05_R_Z | 520/186/174 | 536/175/169 | 549/186/145 | 558/161/161 | 656/112/112 | 587/120/173 | 493/128/259 |
| A06_R_I | 520/186/174 | 536/175/169 | 549/186/145 | 558/161/161 | 656/112/112 | 587/120/173 | 493/128/259 |
| A07_R_finite | 520/186/174 | 536/175/169 | 549/186/145 | 558/161/161 | 656/112/112 | 587/120/173 | 493/128/259 |
| A08_R_collective | 520/186/174 | 536/175/169 | 549/186/145 | 558/161/161 | 656/112/112 | 587/120/173 | 493/128/259 |
| A09_R_pairing | 520/186/174 | 536/175/169 | 549/186/145 | 558/161/161 | 656/112/112 | 587/120/173 | 493/128/259 |
| A10_MISR1_R | 190/63/62 | 202/59/54 | 198/50/67 | 221/47/47 | 269/23/23 | 179/54/82 | 145/39/131 |
| B01_B | 1463/490/504 | 1583/447/427 | 1572/438/447 | 1419/519/519 | 1369/544/544 | 1659/347/451 | 1403/451/603 |
| B02_S2n | 588/301/448 | 1433/407/392 | 611/299/401 | 1114/297/476 | 1099/325/484 | 1494/22/411 | 1254/418/560 |
| B03_S2p | 567/296/440 | 606/288/381 | 1381/386/384 | 1065/204/458 | 1037/200/466 | 1440/310/401 | 1198/56/508 |
| B04_Sn | 602/297/468 | 1488/421/405 | 668/296/413 | 1229/406/497 | 1186/419/509 | 1436/162/426 | 1304/433/577 |
| B05_Sp | 572/302/466 | 653/284/400 | 1456/407/405 | 1174/344/479 | 1147/355/492 | 1521/325/422 | 1133/213/547 |
| B06_OES3n | 265/185/442 | 1405/401/386 | 266/210/383 | 1082/288/468 | 1050/317/478 | 1452/22/406 | 1227/414/551 |
| B07_OES3p | 279/202/421 | 213/208/374 | 1353/379/373 | 988/192/450 | 967/186/454 | 1407/304/394 | 1150/38/513 |
| B08_delta2n | 298/185/407 | 1294/376/361 | 357/214/357 | 954/102/438 | 916/153/446 | 1128/17/382 | 1133/384/514 |
| B09_delta2p | 302/198/361 | 326/183/342 | 1188/333/325 | 795/64/402 | 935/9/394 | 1233/268/345 | 772/53/447 |
| B10_Rch | 524/186/174 | 540/175/169 | 553/186/145 | 562/161/161 | 660/112/112 | 587/120/177 | 493/128/263 |
| B11_BE2 | 239/92/86 | 287/86/44 | 264/101/52 | 257/80/80 | 337/40/40 | 275/53/89 | 218/77/122 |
| B12_E2plus | 280/114/115 | 341/119/49 | 324/118/67 | 291/109/109 | 387/61/61 | 322/71/116 | 272/93/144 |
| B13_E4plus | 213/77/78 | 234/94/40 | 226/94/48 | 248/60/60 | 314/27/27 | 254/46/68 | 218/60/90 |
| B14_E3minus | 57/23/19 | 64/26/9 | 59/28/12 | 99/0/0* | 99/0/0* | 57/9/33 | 67/8/24 |
| B15_R42 | 213/77/78 | 234/94/40 | 226/94/48 | 248/60/60 | 314/27/27 | 254/46/68 | 218/60/90 |

## Full formula references

### A01_BW

Source: [Eq. (1), coefficients in text](https://arxiv.org/pdf/nucl-th/0405080); domain `mass_bw`.

```text
15.78*A-18.34*A**(2/3)-0.71*Z*(Z-1)/A**(1/3)-23.21*(N-Z)**2/A+12*d/sqrt(A)
```

### A02_BWM

Source: [Eqs. (4)-(5); no isotonic experimental shift](https://arxiv.org/pdf/nucl-th/0405080); domain `mass_bw`.

```text
15.777*A-18.34*A**(2/3)-0.71*Z*(Z-1)/A**(1/3)-23.21*(N-Z)**2/(A*(1+exp(-A/17)))+12*(1-exp(-A/30))*d/sqrt(A)
```

### A03_MISR1_B

Source: [Version 3, Eq. (4), eta0=1 MeV](https://arxiv.org/html/2404.11477v3); domain `misr`.

```text
Z*(1+1/N+1.10*N/Z**2)*(I*(32.43-A**(1/3)*N/Z)+16.70)
```

### A04_R_A

Source: [Eq. (2), Table 1](https://doi.org/10.7498/aps.64.112101); domain `sheng`.

```text
sqrt(3/5)*1.2269*A**(1/3)
```

### A05_R_Z

Source: [Eq. (6), Table 1](https://doi.org/10.7498/aps.64.112101); domain `sheng`.

```text
sqrt(3/5)*1.6394*Z**(1/3)
```

### A06_R_I

Source: [Eq. (4), Table 1](https://doi.org/10.7498/aps.64.112101); domain `sheng`.

```text
sqrt(3/5)*1.2828*(1-0.2704*I)*A**(1/3)
```

### A07_R_finite

Source: [Eq. (5), Table 1](https://doi.org/10.7498/aps.64.112101); domain `sheng`.

```text
sqrt(3/5)*1.2331*(1-0.1461*I+2.3310/A)*A**(1/3)
```

### A08_R_collective

Source: [Eq. (10), Table 1](https://doi.org/10.7498/aps.64.112101); domain `sheng`.

```text
sqrt(3/5)*1.2262*(1-0.1473*I+1.9876/A+0.3993*P_s/A)*A**(1/3)
```

### A09_R_pairing

Source: [Eq. (11), Table 1](https://doi.org/10.7498/aps.64.112101); domain `sheng`.

```text
sqrt(3/5)*1.2262*(1-0.1472*I+1.9552/A+0.4030*P_s/A+0.1093*d/A)*A**(1/3)
```

### A10_MISR1_R

Source: [Version 3, Eq. (5); numeric radii in fm](https://arxiv.org/html/2404.11477v3); domain `misr`.

```text
A**(1/3)*(0.95+1.48/Z)+0.017*(P_m-Z/N)*exp(I)-I
```
