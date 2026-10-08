# Heat exchangers: P-NTU temperature effectiveness (function library)

🔵 **Level 2 · Intermediate**  |  🧩 **Function library**  |  ✅ **Verified**  |  `CSL-0102`

Fifteen EES `FUNCTION`s for the **temperature effectiveness** (P-NTU) method of
a heat exchanger: the temperature effectiveness `P1` of a stream referred to
its own number of transfer units `NTU1` and heat capacity ratio `R1`, for the
basic (counterflow, parallel, crossflow) arrangements, the TEMA E, G, H and J
shell-and-tube arrangements, a finned-bundle air cooler and a multipass plate
heat exchanger, plus the inverse relations `NTU1(P1, R1)`. Every argument is
dimensionless, so the functions carry no physical unit: the caller computes
`R1` and `NTU1` from its own mass flow rates, heat capacities and `UA`
(`CSL-0090` gives `Cmin`, `Cr` and `NTU = UA/Cmin`).

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | none (the relations are fluid-independent; `R1`, `NTU1` and the flow arrangement are arguments) |
| **Size** | 127 equations after analysis (largest block: 1); 15 functions of 4–75 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/hx.py` (MIT); inventory row `HT-016` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the relations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (81 values, max deviation 8.3·10⁻⁸) |

## Problem statement

For a given flow arrangement (counterflow, parallel, crossflow, a TEMA
shell-and-tube arrangement, an air-cooled bundle, a multipass plate exchanger)
and a given geometry, compute the temperature effectiveness `P1` of a stream
from its number of transfer units `NTU1` and heat capacity ratio `R1`; or, in
the other direction, compute the `NTU1` (hence the required area) that gives a
prescribed `P1`. Fifteen relations are available, each with its own validity
range and its own literature reference.

## Model

| EES `FUNCTION` | Arguments | Content | Validity (as quoted in `ht`) |
|---|---|---|---|
| `P_NTU_Pp` | x, y | common term of the plate formulas, `P_p = (1 − exp[−x(1+y)])/(1+y)`, limit `x` at y = −1 | no limit quoted |
| `P_NTU_Pc` | x, y | common term of the plate formulas, `P_c = (1 − exp[−x(1−y)])/(1 − y·exp[−x(1−y)])`, limit `x/(1+x)` | no limit quoted |
| `temperature_effectiveness_air_cooler` | R1, NTU1, rows, passes, coerce | air cooler: N rows 1 pass (general double sum), N rows N passes (N = 2…5), 4 rows 2 passes, plus the domain reduction of the original | the factorial of the number of rows overflows a double beyond ≈ 20 rows |
| `temperature_effectiveness_basic` | R1, NTU1, subtype | basic arrangements (subtype 1 counterflow, 2 parallel, 3 crossflow approximate, 4 exact crossflow, 5 crossflow mixed stream 1, 6 mixed stream 2, 7 both mixed) | the exact crossflow case is a numerical integration, the approximate one an approximation |
| `temperature_effectiveness_TEMA_J` | R1, NTU1, Ntp | TEMA J, 1, 2 and 4 tube passes | 1, 2 or 4 tube passes |
| `temperature_effectiveness_TEMA_H` | R1, NTU1, Ntp, optimal | TEMA H, 1 tube pass and the 2-pass countercurrent-like / parallel-like arrangements | 1 or 2 tube passes |
| `temperature_effectiveness_TEMA_G` | R1, NTU1, Ntp, optimal | TEMA G, 1 tube pass and the 2-pass counterflow / parallelflow arrangements | 1 or 2 tube passes |
| `temperature_effectiveness_TEMA_E` | R1, NTU1, Ntp, optimal | TEMA E, 1, 2, 3 and any even number of tube passes | no odd number of tube passes above 3 |
| `temperature_effectiveness_plate` | R1, NTU1, Np1, Np2, counterflow, passes_counterflow | multipass plate exchanger, 14 of the 20 arrangements of the original | infinite number of plates, uniform velocity and flow distribution, constant heat transfer coefficient |
| `NTU_from_P_basic` | P1, R1, subtype | analytical inverses (subtypes 1, 2, 5, 6) | an error when `P1` exceeds the maximum of the arrangement |
| `NTU_from_P_E` | P1, R1, Ntp, optimal | analytical inverses (1 tube pass, 2 passes countercurrent-like) | idem |
| `NTU_from_P_G_residual` | NTU1, R1, P1, Ntp, optimal | equation of the inverse relation, for `NTU1` as an unknown | NTU1 in 10⁻¹¹ … 10⁴ of the original |
| `NTU_from_P_J_residual` | NTU1, R1, P1, Ntp | idem | NTU1 in 10⁻¹¹ … 10³ (1 pass) or a Padé bound (2 and 4 passes) |
| `NTU_from_P_H_residual` | NTU1, R1, P1, Ntp, optimal | idem | NTU1 in 10⁻¹¹ … 100 (monotonic cases) |
| `NTU_from_P_plate_residual` | NTU1, R1, P1, Np1, Np2, counterflow, passes_counterflow | idem | NTU1 in 10⁻¹¹ … 100 or a Padé bound |

Arguments: `R1` heat capacity ratio referred to stream 1 `[-]`, `NTU1` number of
transfer units of stream 1 `[-]`, `P1` temperature effectiveness of stream 1
`[-]`, `Ntp` number of tube passes `[-]`, `Np1`/`Np2` number of passes of sides
1 and 2 of a plate exchanger `[-]`, `rows`/`passes` number of rows and passes
of an air cooler `[-]`, `counterflow`, `passes_counterflow`, `optimal` and
`coerce` flow-arrangement and option flags (1 = true, 0 = false) `[-]`,
`subtype` integer code of the basic arrangement `[-]`.

Every function carries in its comment block (i) the formula, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. The scientific basis
is Shah & Sekulic (2002), Thulukkanam (2013), Rohsenow, Hartnett & Cho (1998),
Kandlikar & Shah (1989), Triboix (2009) for the crossflow relations, and
Schedwill (1968), Schlunder (1983) and Nicole (1972) for the air cooler.

Two members of the `ht` family are **not** translated: `P_NTU_method` and
`effectiveness_NTU_method` are dispatchers that map a method name to a
relation; an EES caller calls the chosen `FUNCTION` directly. The private
helpers of `ht` (`_NTU_from_P_solver`, `_NTU_from_P_objective`,
`_NTU_from_P_erf`, `_NTU_max_for_P_solver`) are not translated either: in EES
`NTU1` is an unknown of the calling model and the effectiveness equation is a
second simultaneous equation; the Padé approximation of
`_NTU_max_for_P_solver` is only the bracket of the `ht` iteration and is
dropped (as planned in the inventory row `HT-016`).

## How to run

Open `hx_temperature_effectiveness_pntu.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./hx_temperature_effectiveness_pntu.eescode
```

The demonstration program after the definitions calls each of the 15 functions
at least twice: once (case *A*) with the input set of the `ht` doctest of the
corresponding relation, once (case *B*) with the steam/oil crossflow rating of
the `ht` docstring (stream 1 = the process stream, `m1` = 0.725 kg/s,
`Cp1` = 1900 J/kg-K, `m2` = 5.2 kg/s, `Cp2` = 1860 J/kg-K, `U` = 275 W/m²-K,
`A` = 10.82 m², so `R1` = 0.14242 and `NTU1` = 2.16007), plus one call per
remaining branch (the seven basic arrangements for two input sets, the two and
three pass cases of every TEMA arrangement, the four- and six-pass formulas, the
five air-cooler branches and the domain reduction, the 2/2, 2/3, 2/4 and 4/2
plate arrangements). It solves in 31 Newton iterations (`Solver: SUCCESS`) and
is the regression baseline (`hx_temperature_effectiveness_pntu.sol`).

The five inverse relations of `ht` are solved numerically there; here `NTU1` is
an unknown of the program and the residual is the second equation, with the
EES idiom of the two equations for one variable (the pattern of `CSL-0090`):

```
resid_G_A = 0
resid_G_A = NTU_from_P_G_residual(NTU_from_P_G_A, R1_A, P1_G_A, Ntp_A, optimal_A)
```

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these relations copies the definitions
for now.

## Results

Values of the demonstration program (full precision in
`hx_temperature_effectiveness_pntu.sol`):

| Quantity (case A, the `ht` doctests) | P1 / NTU1 `[-]` | Quantity (case B) | P1 / NTU1 `[-]` |
|---|---:|---|---:|
| `P_NTU_Pp` (x = 5, y = 0.4) | 0.713634 | | |
| `P_NTU_Pc` (x = 5, y = 0.7) | 0.920670 | (x = 2.16, y = 0.1424) | 0.801124 |
| `temperature_effectiveness_air_cooler` (2 rows, 2 passes) | 0.752307 | (4 rows, 1 pass, R1 = 4) | 0.238511 |
| `temperature_effectiveness_basic` (counterflow) | 0.975341 | (counterflow) | 0.862411 |
| `temperature_effectiveness_TEMA_J` (1 pass) | 0.569909 | (1 pass, R1 = 2) | 0.358083 |
| `temperature_effectiveness_TEMA_H` (1 pass) | 0.573073 | (2 passes, R1 = 4) | 0.236695 |
| `temperature_effectiveness_TEMA_G` (1 pass) | 0.573015 | (1 pass, R1 = 1, NTU1 = 7) | 0.802447 |
| `temperature_effectiveness_TEMA_E` (1 pass) | 0.587050 | (2 passes) | 0.568961 |
| `temperature_effectiveness_plate` (3 passes/1 pass) | 0.574351 | (1 pass/3 passes) | 0.571873 |
| `NTU_from_P_basic` (counterflow) | 3.984770 | (counterflow) | 0.964302 |
| `NTU_from_P_E` (2 passes) | 1.038198 | (2 passes) | 0.987292 |
| `NTU_from_P_G` (1 pass) | 0.999951 | (1 pass) | 0.730000 |
| `NTU_from_P_J` (1 pass) | 1.000307 | (1 pass) | 0.731276 |
| `NTU_from_P_H` (1 pass) | 0.999763 | (1 pass) | 0.729980 |
| `NTU_from_P_plate` (1 pass/3 passes) | 1.008078 | (1 pass/2 passes) | 0.731276 |

The effectiveness of a shell-and-tube exchanger increases with the number of
transfer units and falls with the capacity-rate ratio: for `R1` = 1/3 and
`NTU1` = 1 the four TEMA arrangements give 0.587 (E), 0.573 (G), 0.573 (H) and
0.570 (J) for one tube pass, i.e. the more countercurrent the arrangement the
larger the effectiveness, as expected.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the temperature
     effectiveness P1 of the TEMA E, G, H and J one-pass arrangements and of the
     counterflow relation over NTU1 at R1 = 1/3,
     figures/hx_temperature_effectiveness_pntu_p1_ntu.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/hx.py`, commit `85e0ee6`, installed from the local clone `~/git/ht` in a
throw-away virtual environment under `work/`) for case *A*, plus values computed
with the same Python functions for case *B* and for every remaining branch. The
81 output values of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
81 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 46
```

The 46 “only in CoolSolve” variables are the 46 inputs of the demonstration
program (`R1_A`, `NTU1_A`, `R1_B`, `NTU1_B`, `rows_A`, `passes_A`, `Ntp_A`,
`Np1_A`, `Np2_A`, `counterflow_A`, `optimal_A`, `coerce_A`, the requested
effectivenesses `P1_*`, …) and the five residual variables `resid_*` (zero to
machine precision); the reference table holds only the 81 outputs. The largest
relative deviation over the 81 values is **8.3·10⁻⁸**
(`temperature_effectiveness_basic_extra4`), i.e. the composite Simpson
quadrature (80 intervals) of the exact crossflow integral, which CoolSolve
cannot evaluate inside a function body — the same quadrature in the main
program of `CSL-0090` gives 1.4·10⁻⁸. Over the other 80 values the largest
deviation is 1.2·10⁻⁹ (`NTU_from_P_G_A`, convergence tolerance of the implicit
inversion) and the remaining 79 agree to 6.6·10⁻¹⁰, i.e. round-off.

Per-value comparison, `ht` / CoolSolve (81 values):

| Variable | `ht` 1.2.0 | CoolSolve 0.3.0 | rel. dev. |
|---|---:|---:|---:|
| `P_NTU_Pp_A` | 0.713634370025 | 0.713634370025 | 0.0e+00 |
| `P_NTU_Pc_A` | 0.920670368605 | 0.920670368605 | 0.0e+00 |
| `temperature_effectiveness_air_cooler_A` | 0.752307285582 | 0.752307285582 | 0.0e+00 |
| `temperature_effectiveness_basic_A` | 0.975341272976 | 0.975341272976 | 0.0e+00 |
| `temperature_effectiveness_TEMA_J_A` | 0.569908519365 | 0.569908519365 | 0.0e+00 |
| `temperature_effectiveness_TEMA_H_A` | 0.573072828491 | 0.573072828491 | 0.0e+00 |
| `temperature_effectiveness_TEMA_G_A` | 0.573014935087 | 0.573014935087 | 0.0e+00 |
| `temperature_effectiveness_TEMA_E_A` | 0.587050065403 | 0.587050065403 | 0.0e+00 |
| `temperature_effectiveness_plate_A` | 0.574351435272 | 0.574351435272 | 0.0e+00 |
| `NTU_from_P_basic_A` | 3.984769850376 | 3.984769850376 | 0.0e+00 |
| `NTU_from_P_E_A` | 1.038197924082 | 1.038197924082 | 0.0e+00 |
| `NTU_from_P_G_A` | 0.999951370776 | 0.999951369548 | 1.2e-09 |
| `NTU_from_P_J_A` | 1.000307013888 | 1.000307013888 | 0.0e+00 |
| `NTU_from_P_H_A` | 0.999762869689 | 0.999762869689 | 0.0e+00 |
| `NTU_from_P_plate_A` | 1.008078071885 | 1.008078071182 | 7.0e-10 |
| `P1_TEMA_G_check_A` | 0.573000000000 | 0.572999999623 | 6.6e-10 |
| `P1_TEMA_J_check_A` | 0.570000000000 | 0.570000000000 | 0.0e+00 |
| `P1_TEMA_H_check_A` | 0.573000000000 | 0.573000000000 | 0.0e+00 |
| `P1_plate_check_A` | 0.574300000000 | 0.574299999790 | 3.7e-10 |
| `R1_B` | 0.142421422663 | 0.142421422700 | 2.6e-10 |
| `NTU1_B` | 2.160072595281 | 2.160072595300 | 8.8e-12 |
| `P_NTU_Pp_B` | 0.801124237935 | 0.801124237917 | 2.3e-11 |
| `P_NTU_Pc_B` | 0.862410628614 | 0.862410628610 | 4.5e-12 |
| `temperature_effectiveness_air_cooler_B` | 0.238511024422 | 0.238511024422 | 0.0e+00 |
| `temperature_effectiveness_air_cooler_extra_4x4` | 0.812194036319 | 0.812194036319 | 1.2e-13 |
| `temperature_effectiveness_air_cooler_extra_4x2` | 0.856349711210 | 0.856349711205 | 6.4e-12 |
| `temperature_effectiveness_air_cooler_extra_6x1` | 0.845784327165 | 0.845784327157 | 9.3e-12 |
| `temperature_effectiveness_air_cooler_coerced` | 0.859156596062 | 0.859156596057 | 5.5e-12 |
| `temperature_effectiveness_basic_B` | 0.862410628614 | 0.862410628610 | 4.5e-12 |
| `temperature_effectiveness_basic_extra2` | 0.801124237935 | 0.801124237917 | 2.3e-11 |
| `temperature_effectiveness_basic_extra3` | 0.850786342341 | 0.850786342334 | 8.0e-12 |
| `temperature_effectiveness_basic_extra4` | 0.846162913084 | 0.846162842451 | 8.3e-08 |
| `temperature_effectiveness_basic_extra5` | 0.844236258328 | 0.844236258319 | 1.0e-11 |
| `temperature_effectiveness_basic_extra6` | 0.831218036143 | 0.831218036131 | 1.4e-11 |
| `temperature_effectiveness_basic_extra7` | 0.829734878910 | 0.829734878898 | 1.5e-11 |
| `temperature_effectiveness_basic_test1` | 0.173382601503 | 0.173382601503 | 0.0e+00 |
| `temperature_effectiveness_basic_test2` | 0.163852912050 | 0.163852912050 | 0.0e+00 |
| `temperature_effectiveness_basic_test3` | 0.149974594007 | 0.149974594007 | 0.0e+00 |
| `temperature_effectiveness_basic_test4` | 0.169870212187 | 0.169870212196 | 4.9e-11 |
| `temperature_effectiveness_basic_test5` | 0.168678230894 | 0.168678230894 | 0.0e+00 |
| `temperature_effectiveness_basic_test6` | 0.169537907740 | 0.169537907740 | 0.0e+00 |
| `temperature_effectiveness_basic_test7` | 0.168411216829 | 0.168411216829 | 0.0e+00 |
| `temperature_effectiveness_TEMA_J_B` | 0.358083089595 | 0.358083089595 | 0.0e+00 |
| `temperature_effectiveness_TEMA_J_extra_2p` | 0.568887823232 | 0.568887823232 | 0.0e+00 |
| `temperature_effectiveness_TEMA_J_extra_4p` | 0.568871184657 | 0.568871184657 | 0.0e+00 |
| `temperature_effectiveness_TEMA_H_B` | 0.236695335246 | 0.236695335246 | 0.0e+00 |
| `temperature_effectiveness_TEMA_H_extra_1p_R2` | 0.364025704995 | 0.364025704995 | 0.0e+00 |
| `temperature_effectiveness_TEMA_H_extra_2p_unopt` | 0.556005707231 | 0.556005707231 | 0.0e+00 |
| `temperature_effectiveness_TEMA_H_extra_2p_unopt_R4` | 0.192234814128 | 0.192234814128 | 0.0e+00 |
| `temperature_effectiveness_TEMA_G_B` | 0.802446620198 | 0.802446620198 | 0.0e+00 |
| `temperature_effectiveness_TEMA_G_extra_2p` | 0.582423877814 | 0.582423877814 | 0.0e+00 |
| `temperature_effectiveness_TEMA_G_extra_2p_R2` | 0.483842488914 | 0.483842488914 | 0.0e+00 |
| `temperature_effectiveness_TEMA_G_extra_2p_unopt` | 0.555988302857 | 0.555988302857 | 0.0e+00 |
| `temperature_effectiveness_TEMA_G_extra_2p_unopt_R2` | 0.318296079640 | 0.318296079640 | 0.0e+00 |
| `temperature_effectiveness_TEMA_E_B` | 0.568961321767 | 0.568961321767 | 0.0e+00 |
| `temperature_effectiveness_TEMA_E_extra_2p_unopt` | 0.569908519365 | 0.569908519365 | 0.0e+00 |
| `temperature_effectiveness_TEMA_E_extra_2p_unopt_R2` | 0.358083089595 | 0.358083089595 | 0.0e+00 |
| `temperature_effectiveness_TEMA_E_extra_3p` | 0.570862488899 | 0.570862488899 | 0.0e+00 |
| `temperature_effectiveness_TEMA_E_extra_3p_unopt` | 0.276815590660 | 0.276815590660 | 0.0e+00 |
| `temperature_effectiveness_TEMA_E_extra_4p` | 0.568889338658 | 0.568889338658 | 0.0e+00 |
| `temperature_effectiveness_TEMA_E_extra_6p` | 0.829772049252 | 0.829772049240 | 1.4e-11 |
| `temperature_effectiveness_plate_B` | 0.571872675766 | 0.571872675766 | 0.0e+00 |
| `temperature_effectiveness_plate_extra_2x2_par` | 0.801124237935 | 0.801124237917 | 2.3e-11 |
| `temperature_effectiveness_plate_extra_2x2_cf_par` | 0.847597093066 | 0.847597093058 | 9.1e-12 |
| `temperature_effectiveness_plate_extra_2x4_cf` | 0.855123819389 | 0.855123819383 | 6.7e-12 |
| `temperature_effectiveness_plate_extra_4x2_cf` | 0.856397731580 | 0.856397731575 | 6.3e-12 |
| `temperature_effectiveness_plate_extra_2x3_par` | 0.810690214487 | 0.810690214471 | 2.0e-11 |
| `NTU_from_P_basic_B` | 0.964301692629 | 0.964301692642 | 1.4e-11 |
| `NTU_from_P_basic_extra_par` | 0.741223538463 | 0.741223538476 | 1.8e-11 |
| `NTU_from_P_basic_extra_mix1` | 0.981848703457 | 0.981848703476 | 1.9e-11 |
| `NTU_from_P_basic_extra_mix2` | 0.366144750001 | 0.366144750004 | 6.8e-12 |
| `NTU_from_P_E_B` | 0.987291530683 | 0.987291530703 | 2.1e-11 |
| `NTU_from_P_E_extra_1p` | 0.964301692629 | 0.964301692642 | 1.4e-11 |
| `NTU_from_P_G_B` | 0.729999583607 | 0.729999583617 | 1.4e-11 |
| `P1_TEMA_G_check_B` | 0.500000000000 | 0.500000000000 | 0.0e+00 |
| `NTU_from_P_J_B` | 0.731275769178 | 0.731275769188 | 1.4e-11 |
| `P1_TEMA_J_check_B` | 0.500000000000 | 0.500000000000 | 2.0e-13 |
| `NTU_from_P_H_B` | 0.729980438763 | 0.729980438773 | 1.4e-11 |
| `P1_TEMA_H_check_B` | 0.500000000000 | 0.500000000000 | 0.0e+00 |
| `NTU_from_P_plate_B` | 0.731275769178 | 0.731275769188 | 1.4e-11 |
| `P1_plate_check_B` | 0.500000000000 | 0.500000000000 | 2.0e-13 |

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the P-NTU temperature-effectiveness relations of `ht`, the
heat-transfer component of ChEDL, file `ht/hx.py`, functions `P_NTU_Pp`,
`P_NTU_Pc`, `temperature_effectiveness_air_cooler`,
`temperature_effectiveness_basic`, `temperature_effectiveness_TEMA_E`,
`temperature_effectiveness_TEMA_G`, `temperature_effectiveness_TEMA_H`,
`temperature_effectiveness_TEMA_J`, `temperature_effectiveness_plate`,
`NTU_from_P_basic`, `NTU_from_P_E`, `NTU_from_P_G`, `NTU_from_P_H`,
`NTU_from_P_J` and `NTU_from_P_plate`, version 1.2.0, commit 85e0ee6
(2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; each `ht` relation became one EES
`FUNCTION` named after it (the four relations that `ht` solves numerically
became the `*_residual` functions carrying their equation), the Python string
`subtype` became an integer code, the Python booleans `optimal`,
`counterflow`, `passes_counterflow` and `coerce` became 1/0 flags, and the
Python `log` became the EES `LN`. No equation was changed. Scientific basis per
function: the original paper or book quoted in its comment block.

The scientific authors of the relations are credited in the comment block of
each function and in `model.json` (`origin.authors`); the books `ht` takes them
from are Shah & Sekulic, *Fundamentals of Heat Exchanger Design* (2002),
Thulukkanam, *Heat Exchanger Design Handbook* (2013) and Rohsenow, Hartnett &
Cho, *Handbook of Heat Transfer*, 3E (1998).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-111, family `HT-016`).** One EES
  `FUNCTION` per `ht` relation (15 functions), named after the `ht` function,
  with the formula, the validity range as quoted by `ht`, the original
  reference and the `ht` module/function/version/commit in the comment block.
  Arguments are the Python arguments, all dimensionless; no property function is
  used inside a function, so the calling model passes `R1`, `NTU1`, `P1` and
  the flow arrangement itself.
- **`ELSEIF` is not used**: in CoolSolve 0.3.0 the condition of an `ELSEIF` is
  ignored and the value of the **last** branch of the chain is returned (see
  *Limitations*); all 36 `ELSEIF` of the first draft were therefore rewritten as
  nested `IF`/`ELSE` blocks, which is the same construct and valid EES.
- **Selectors not translated**: `P_NTU_method` and `effectiveness_NTU_method`
  only map a method name to a relation; the caller chooses the `FUNCTION`
  directly.
- **Iteration helpers not translated**: `NTU_from_P_G`, `NTU_from_P_J`,
  `NTU_from_P_H` and `NTU_from_P_plate` solve their equation numerically in
  `ht`; here the equation is the body of the corresponding `*_residual`
  function and `NTU1` is an unknown of the calling model (the demonstration
  program shows the two-equation EES idiom). The Padé approximation of
  `_NTU_max_for_P_solver` (a bracket of the `ht` iteration) is dropped.
  `NTU_from_P_basic` and `NTU_from_P_E` keep the analytical inverses that `ht`
  returns directly (four arrangements and two cases respectively); their other
  cases are inverted with `temperature_effectiveness_basic` or
  `temperature_effectiveness_TEMA_E` as the second equation.
- **`temperature_effectiveness_plate`**: the 6 asymmetric arrangements of the
  20 supported by `ht` (2/1, 3/1, 3/2, 4/1, 4/2 and 4/3) are obtained in `ht`
  by a **recursive** call that exchanges the two sides
  (`R1 → 1/R1`, `NTU1 → NTU1*R1`, passes exchanged, result multiplied by
  `1/R1`). A self-recursive EES `FUNCTION` crashes CoolSolve 0.3.0 (segmentation
  fault) or is mis-evaluated silently (see *Limitations*), so the exchange is
  done explicitly by the caller; the relation is written in the comment block
  of the function and used by the demonstration program for its cases *A* and
  `extra_4x2_cf`. The 14 direct arrangements are unchanged.
- **`temperature_effectiveness_air_cooler`**: the domain reduction of `coerce`
  is applied to the rows and passes *before* the branch selection, exactly as
  the original applies it in its `else` branch followed by a recursive call
  (the reduced pair is always a supported case). The general `N rows 1 pass`
  double sum is evaluated with nested `DUPLICATE` loops; the powers of `K`, the
  cumulative sums `(NKR)^k/k!`, the binomial coefficients and the factorials are
  advanced along the loops, which avoids both the arrays and the recursion of
  the original.
- **`temperature_effectiveness_basic`, subtype 4** (exact crossflow): the
  integral of the original (`scipy.integrate.quad`) is replaced by a composite
  Simpson rule with 80 intervals evaluated inside the function, and the
  modified Bessel function `I0(v)` by its power series (25 terms); both are
  needed because CoolSolve cannot integrate and has no Bessel function (as
  already done in `CSL-0090`). This is the only value of the verification table
  that is not a round-off match (8.3·10⁻⁸).
- **Limit values**: the singular closed forms (`R1` = 1, 2, 4, `R1` = 0.25,
  `R2` = 0.5, `y` = ±1) are handled by the explicit limit expressions of the
  original, in an `IF`, as in the original. Where the original raises an error
  (unsupported number of tube passes, unsupported pass combination, `P1` above
  the maximum of the arrangement) the output is left undefined here; the valid
  arguments are listed above and in the comment block of each function.
- **Level**: equations 127 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- **`ELSEIF` is mis-evaluated by CoolSolve 0.3.0**: the condition of an
  `ELSEIF` is ignored and the value of the **last** branch of the chain is
  returned, without any warning. Minimal reproducer (two branches, the call
  selects the first, the answer is the value of the second):

  ```
  FUNCTION f(a)
  {test}
    IF a = 1 THEN
      f = 11
    ELSEIF a = 3 THEN
      f = 33
    ENDIF
  END
  q = f(1)
  ```

  CoolSolve 0.3.0 returns `q = 33` (EES returns 11). The file therefore uses
  nested `IF`/`ELSE` blocks, which are equivalent and valid EES; a model written
  with `ELSEIF` and copied into CoolSolve would silently get the wrong branch.
  This is reported as an *unverified suggestion* (no reference to the EES
  `ELSEIF` syntax was available, so nothing is registered in
  `CoolSolve/docs/model_library_support.md`, where `CS-GAP-ELSEIF-CHAIN`
  describes another, different `ELSE`+`IF` ladder problem).
- **A self-recursive EES `FUNCTION` cannot be used in CoolSolve 0.3.0**: a
  minimal function `f(a)` that calls itself under a condition gives a wrong
  value (1.0) instead of the value of the taken branch, or ends in a
  segmentation fault (stack overflow) — even when the recursion terminates after
  one level, as in the plate function of this card. This is why the asymmetric
  plate arrangements are computed by an explicit side exchange. Evidence and
  reproducer: the *Limitations* and *Suggestion* sections of the final message
  of this card; no gap is registered (no EES reference available).
- **`temperature_effectiveness_plate` is unreliable when its arguments are
  variables** in CoolSolve 0.3.0: with literal arguments it reproduces `ht`,
  with variables taken from equations of the calling program it can return a
  value that is wrong by a large amount (e.g. 0.0811 instead of 0.1915 for
  `R1` = 3, `NTU1` = 1/3, 1 pass/3 passes — the argument `R1/3` then reaches
  the singular limit branch of `P_NTU_Pc`). The two demonstration calls that
  need the side exchange therefore pass the exchanged values as literals of the
  `ht` doctest input set, with the relation written in the comment; a model
  using this function should check its results against the reference. This is an
  *unverified suggestion*, not a registered gap.
- The demonstration input sets are chosen to exercise the branches, not to stay
  inside every quoted validity range; the values of the *Results* and
  *Verification* tables check the **equations**, not recommended design values.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  relations copies the definitions for now.

## Related models

- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU (ε-NTU) relations
  of the same method, from the same `ht` triage and with the same layout; the
  shell-and-tube and multipass branches left out of that file are here.
- `CSL-0096` *plate_hx_heat_transfer*: the plate-channel heat-transfer
  correlations (`ht` family `HT-010`) that a plate exchanger model combines with
  `temperature_effectiveness_plate`.
- `CSL-0002` *counterflow_hx_oil_water* and `CSL-0026*
  crossflow_hx_hot_gas_water*: two rated heat exchangers that use the ε-NTU
  relations of `CSL-0090`.
- `CSL-0032` *wet_air_cooled_condenser*: an air-cooled condenser, whose
  rating would use `temperature_effectiveness_air_cooler` and the TEMA branches.
- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` family of the library
  (same layout: one `FUNCTION` per correlation, per-function comment block,
  demonstration program, verification table).
- `CSL-0105` *lmtd_and_f_correction*: the LMTD relations of the same `ht`
  triage (`LMTD`, `F_LMTD_Fakheri`, `Ft_aircooler`, same layout), the other
  way of rating a shell-and-tube or air-cooler exchanger.
