# Air-cooled heat exchanger, air side: finned-bundle HTC, pressure drop and fan noise

🔵 **Level 2 · Intermediate**  &nbsp;|&nbsp; 🧩 **Function library**  &nbsp;|&nbsp; ✅ **Verified**  &nbsp;|&nbsp; `CSL-0099`

Eight EES `FUNCTION`s for the air side of an air cooler (a finned tube bundle
crossed by air): the air-side heat-transfer coefficient on a bare-tube basis
(Briggs & Young, ESDU high-fin, ESDU low-fin, Ganguli/VDI), the air-side
pressure drop across the bundle (ESDU high-fin and low-fin) and the sound
pressure level of a one-fan bay (GPSA, Mukherjee). Three helper functions
complete the family: the Kern & Kraus circular-fin efficiency and the two
modified Bessel functions it needs, evaluated by their power series because
CoolSolve has no Bessel function. All arguments are the geometry of the bundle
and the air properties, as in the source library — no property function is
called inside the functions. This is family `HT-013` of the `ht` triage
(roadmap card C-108); it follows the layout set by `CSL-0087`.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the air properties `rho`, `Cp`, `mu`, `k`, `k_fin` are arguments; the model calls no property function) |
| **Size** | 117 equations after analysis (largest block: 1); 11 functions of 2–60 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/air_cooler.py` (+ `ht/core.py`, `ht/conv_tube_bank.py`) (MIT); inventory row `HT-013` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (Briggs & Young, Ganguli/Tung/Taborek, Mukherjee & Hewitt, GPSA, ESDU, VDI — see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (32 values, max deviation 3.8·10⁻¹⁰) |

## Problem statement

Given the geometry of a finned tube bundle (tube diameter, fin diameter, fin
thickness and pitch, tube pitches, number of rows, total surface area, minimum
free-flow area), the mass flow rate of air across it and the air properties,
compute the air-side heat-transfer coefficient (referred to the bare-tube area,
as the correlations do), the air-side pressure drop, and — for the fan of the
bay — the sound pressure level at 1 m from it. The caller does the sizing of
the bundle; these functions only close the heat-transfer and hydraulic (and
acoustic) relations of an air cooler, each with its own validity range.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in the original) |
|---|---|---|---|
| `h_Briggs_Young` | m, A, A_min, A_increase, A_fin, A_tube_showing, tube_diameter, fin_diameter, fin_thickness, bare_length, rho, Cp, mu, k, k_fin | Nu = 0.134·Re^0.681·Pr^(1/3)·(S/h_f)^0.2·(S/t_f)^0.1134, then h = k/D·Nu·(η_f·A_fin + A_tube_showing)/A·A_increase | 1000 < Re < 8000; 11.13 < D_o < 40.89 mm; 1.42 < h_f < 16.57 mm; 0.33 < t_f < 2.02 mm; 1.30 < fin pitch < 4.06 mm; 24.49 < normal pitch < 111 mm |
| `h_ESDU_high_fin` | as above + pitch_parallel, pitch_normal, tube_rows, Pr_wall | Nu = 0.242·Re^0.658·(S/h_f)^0.297·(p₁/p₂)^-0.091·Pr^(1/3)·F₂·F₁, F₂ = 0.76 / 0.84 / 0.92 / 1 for 1 / 2 / 3 / ≥4 rows, F₁ = (Pr/Pr_wall)^0.26 | none quoted; the ESDU data cover 4–11 fins/in, D_o 3/8–2 in, h_f 1/3–5/8 in, D_tip/D_root 1.2–2.4, 5000 < Re < 50 000 |
| `h_ESDU_low_fin` | as `h_ESDU_high_fin` | Nu = 0.183·Re^0.7·(S/h_f)^0.36·(p₁/D_fin)^0.06·(h_f/D_fin)^0.11·Pr^0.36·F₂·F₁, F₂ = the ESDU 73031 row-count factor (in-line / staggered table) | none quoted; the ESDU data cover 11–32 fins/in, D_o 0.5–1.25 in, h_f 0.03–0.1 in, 1000 < Re < 80 000 |
| `h_Ganguli_VDI` | as `h_Briggs_Young` + pitch_parallel, pitch_normal, tube_rows | Nu = c·Re^0.6·Pr^(1/3)·A_increase^-0.15, c = 0.2 / 0.22 in-line (≤3 / ≥4 rows), 0.2 / 0.33 / 0.36 / 0.38 staggered (1 / 2 / 3 / ≥4 rows) | none quoted |
| `dP_ESDU_high_fin` | m, A_min, A_increase, flow_area_contraction_ratio, tube_diameter, pitch_parallel, pitch_normal, tube_rows, rho, mu | K_f = 4.567·Re^-0.242·A_increase^0.504·(p₁/D)^-0.376·(p₂/D)^-0.546, K_acc = 1 + φ², dP = (K_acc + n·K_f)·ρ·V_max²/2 | the ESDU data: 4–11 fins/in, D_o 3/8–2 in, h_f 1/3–5/8 in, 5000 < Re < 50 000 (72 % of its points within 10 %) |
| `dP_ESDU_low_fin` | as above + fin_height, bare_length | K_f = 4.72·Re^-0.286·(h_f/S)^0.51·((p₁−D)/(p₂−D))^0.536·(D/(p₁−D))^0.36, K_acc = 1 + φ², dP = (K_acc + n·K_f)·ρ·V_max²/2 | the ESDU data: 11–32 fins/in, D_o 0.5–1.25 in, h_f 0.03–0.1 in, 1000 < Re < 80 000 (standard deviation 7.7 % on 81 points) |
| `air_cooler_noise_GPSA` | tip_speed, power | PWL = 56 + 30·log₁₀(v_tip/304.8) + 10·log₁₀(P) in dB(A), with v_tip in m/min and P in hp | none quoted |
| `air_cooler_noise_Mukherjee` | tip_speed, power, fan_diameter, induced | SPL = 46 + 30·log₁₀(v_tip) + 10·log₁₀(P) − 20·log₁₀(D_fan), less 3 dB when induced | none quoted |
| `eta_fin_Kern_Kraus_aircooler` | tube_diameter, fin_diameter, fin_thickness, k_fin, h | η_f = 2r_o/[m(r_e²−r_o²)]·[I₁(mr_e)K₁(mr_o) − K₁(mr_e)I₁(mr_o)]/[I₀(mr_o)K₁(mr_e) + I₁(mr_e)K₀(mr_o)], m = √(2h/(k_fin·t_fin)) | none quoted |
| `bessel_mod_I_series` | n_order, z | I_n(z) = (z/2)^n·Σ_k (z²/4)^k/[k!(k+n)!], 13 terms | exact to machine precision for z ≤ 2 (checked to z = 2.5) |
| `bessel_mod_K_series` | n_order, z | K₀(z) = −[ln(z/2)+γ]·I₀(z) + Σ_{k≥1} H_k·(z²/4)^k/(k!)², K₁(z) = I₀/z + [ln(z/2)+γ]·I₁ − (2/z)·Σ_{k≥1} k·H_k·a_k | idem |

Arguments: `m` mass flow rate of air `[kg/s]`; `A` combined finned and bare
surface area exposed `[m^2]`; `A_min` minimum free-flow area `[m^2]`;
`A_increase` ratio of the actual surface area to the bare-tube surface area
`[-]`; `A_fin` area of all fins `[m^2]`; `A_tube_showing` area of bare tube
showing `[m^2]`; `tube_diameter` bare-tube diameter `[m]`; `fin_diameter`
tube diameter including its fins `[m]`; `fin_thickness` fin thickness `[m]`;
`fin_height` height of the fins above the bare tube `[m]`; `bare_length` length
of bare tube between two fins `[m]`; `pitch_parallel` / `pitch_normal` tube
pitches `[m]`; `tube_rows` rows per bundle `[-]`; `flow_area_contraction_ratio`
ratio of `A_min` to the bundle face area `[-]`; `rho`, `Cp`, `mu`, `k`, `k_fin`
`[kg/m^3]`, `[J/kg-K]`, `[Pa-s]`, `[W/m-K]`, `[W/m-K]`; `Pr_wall` Prandtl
number at the wall `[-]`; `tip_speed` `[m/s]`; `power` shaft power of the fan
motor `[W]`; `fan_diameter` `[m]`; `induced` 0 forced / 1 induced draft `[-]`;
`n_order` 0 or 1 `[-]`; `z` argument of the Bessel function `[-]`.

The four heat-transfer functions all return the **bare-tube-basis**
coefficient, obtained by multiplying the coefficient on the fin surface by
`(η_f·A_fin + A_tube_showing)/A` and then by `A_increase`; the fin efficiency
`η_f` is the Kern & Kraus solution for a circular fin of constant thickness.

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by the original**, (iii) the original paper or book and
(iv) the `ht` module, function, version and commit it was taken from.

## How to run

Open `air_cooler_air_side.eescode` in the CoolSolve GUI and press *Solve*, or
from a terminal:

```bash
coolsolve ./air_cooler_air_side.eescode
```

The demonstration program after the definitions calls each function: case *A*
uses the input sets of the `ht` doctests (three bundles and one fan), case *B*
a second, uniform set (a two-row in-line low-fin bundle of 10 tubes per row and
a 42 m/s / 45 kW / 3 m fan). It solves without any iteration
(`Solver: SUCCESS (0 iterations)`, every equation explicit) and is the
regression baseline (`air_cooler_air_side.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0099 ---}` and
lists `CSL-0099` in its `related` field.

## Results

Values of the demonstration program (full precision in
`air_cooler_air_side.sol`):

| Quantity | case A | case B |
|---|---:|---:|
| `bessel_mod_I_series(0, 1.5)` = I₀(1.5) `[-]` | 1.64672 | 1.64672 |
| `bessel_mod_I_series(1, 1.5)` = I₁(1.5) `[-]` | 0.981666 | 0.981666 |
| `bessel_mod_K_series(0, 1.5)` = K₀(1.5) `[-]` | 0.213806 | 0.213806 |
| `bessel_mod_K_series(1, 1.5)` = K₁(1.5) `[-]` | 0.277388 | 0.277388 |
| `eta_fin` (case A: 1 in tube, 57.15 mm fin, 58 W/m²K) `[-]` | 0.841259 | 0.946962 |
| `h_Briggs_Young` `[W/m^2-K]` | 1422.87 | 289.074 |
| `h_ESDU_high_fin` (Pr_wall = Pr) `[W/m^2-K]` | 1390.89 | 305.244 |
| `h_ESDU_high_fin` (Pr_wall given) `[W/m^2-K]` | 1390.18 | 309.073 |
| `h_ESDU_low_fin` (Pr_wall = Pr) `[W/m^2-K]` | 553.854 | 276.390 |
| `h_ESDU_low_fin` (Pr_wall given) `[W/m^2-K]` | 553.204 | 273.271 |
| `h_Ganguli_VDI` `[W/m^2-K]` | 969.285 | 156.792 |
| `dP_ESDU_high_fin` `[Pa]` | 485.631 | 90.043 |
| `dP_ESDU_low_fin` `[Pa]` | 464.543 | 82.268 |
| `air_cooler_noise_GPSA` `[dB(A)]` | 100.537 | 101.328 |
| `air_cooler_noise_Mukherjee`, forced draft `[dB(A)]` | 99.110 | 102.962 |
| `air_cooler_noise_Mukherjee`, induced draft `[dB(A)]` | 96.110 | 99.962 |

Case A bundles: A1 high-fin (4 rows × 20 tubes of 3 m, 1 in OD, 0.4 mm fins at
2.309 mm pitch, 15.9 mm high, 21.56 kg/s of air — the Briggs & Young and ESDU
high-fin doctests), A2 low-fin (4 rows × 8 tubes of 0.5 m, 16.4 mm OD, 1 mm
fins at 3 mm pitch, 4.1 mm high, 0.914 kg/s — the ESDU low-fin and both
pressure-drop doctests), A3 staggered 4 rows × 56 tubes of 36 ft, 1 in OD,
0.33 mm fins at 10/inch, 130.7 kg/s (the Ganguli/VDI worked example). Case A4
fan: 52.95 m/s tip speed, 18 717 W (25.1 hp), 4.267 m diameter. Case B: a
two-row in-line bundle (10 tubes of 1.2 m per row, 19.05 mm OD, 0.8 mm fins at
3.5 mm pitch, 3 mm high, 40 mm square pitches, 2.35 kg/s) and a 42 m/s,
45 kW, 3 m fan.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): a parametric
     sweep of the case-B bundle, e.g. h_Briggs_Young, h_ESDU_low_fin and
     dP_ESDU_low_fin against the air mass flow rate (Parametric tab of the GUI),
     figures/air_cooler_air_side_parametric.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/air_cooler.py`, commit `85e0ee6`, installed from the local clone in a
throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for case *B*; the modified Bessel functions were
compared with `scipy.special.iv` / `kv` and the fin efficiency with the `ht`
doctest of `fin_efficiency_Kern_Kraus`. The 32 output values of the
demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
32 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 85
```

(the 85 “only in CoolSolve” variables are the 85 inputs of the demonstration
program — the geometry and air properties of the three bundles of case A and of
the bundle of case B, and the fan data; the reference table holds only the 32
outputs). The largest relative deviation over the 32 values is **3.8·10⁻¹⁰**
(`dP_ESDU_high_fin_B`), which is the rounding of the printed input values of the
demonstration program (the areas and the flow-area contraction ratios are given
with ten significant digits).

Per-function values, `ht` (or SciPy) / CoolSolve:

| Function | case A: `ht` | case A: CoolSolve | rel. dev. | case B: `ht` | case B: CoolSolve | rel. dev. |
|---|---:|---:|---:|---:|---:|---:|
| `bessel_mod_I_series (n = 0, z = 1.5)` | 1.6467231898 | 1.6467231898 | 6.6e-14 | 1.6467231898 | 1.6467231898 | 6.6e-14 |
| `bessel_mod_I_series (n = 1, z = 1.5)` | 0.9816664286 | 0.9816664286 | 7.9e-15 | 0.9816664286 | 0.9816664286 | 7.9e-15 |
| `bessel_mod_K_series (n = 0, z = 1.5)` | 0.2138055626 | 0.2138055626 | 1.2e-13 | 0.2138055626 | 0.2138055626 | 1.2e-13 |
| `bessel_mod_K_series (n = 1, z = 1.5)` | 0.2773878005 | 0.2773878005 | 1.6e-13 | 0.2773878005 | 0.2773878005 | 1.6e-13 |
| `eta_fin_Kern_Kraus_aircooler` | 0.8412588620 | 0.8412588620 | 1.8e-14 | 0.9469619290 | 0.9469619290 | 3.4e-14 |
| `h_Briggs_Young` | 1422.8722403238 | 1422.8722403490 | 1.8e-11 | 289.0741391808 | 289.0741392505 | 2.4e-10 |
| `h_ESDU_high_fin (Pr_wall = Pr)` | 1390.8889180498 | 1390.8889180690 | 1.4e-11 | 305.2442316801 | 305.2442317523 | 2.4e-10 |
| `h_ESDU_high_fin (Pr_wall given)` | 1390.1825849909 | 1390.1825850110 | 1.4e-11 | 309.0729280830 | 309.0729281561 | 2.4e-10 |
| `h_ESDU_low_fin (Pr_wall = Pr)` | 553.8538364709 | 553.8538363922 | 1.4e-10 | 276.3898196601 | 276.3898197277 | 2.4e-10 |
| `h_ESDU_low_fin (Pr_wall given)` | 553.2037755901 | 553.2037755112 | 1.4e-10 | 273.2711582434 | 273.2711583102 | 2.4e-10 |
| `h_Ganguli_VDI` | 969.2850818579 | 969.2850818778 | 2.1e-11 | 156.7916262526 | 156.7916262857 | 2.1e-10 |
| `dP_ESDU_high_fin` | 485.6307687792 | 485.6307687040 | 1.5e-10 | 90.0429343379 | 90.0429343720 | 3.8e-10 |
| `dP_ESDU_low_fin` | 464.5433141866 | 464.5433141266 | 1.3e-10 | 82.2676294840 | 82.2676295131 | 3.5e-10 |
| `air_cooler_noise_GPSA` | 100.5368047796 | 100.5368047796 | 2.1e-14 | 101.3280517982 | 101.3280517982 | 3.0e-13 |
| `air_cooler_noise_Mukherjee (forced)` | 99.1102632909 | 99.1102632909 | 7.6e-15 | 102.9615380723 | 102.9615380723 | 6.3e-14 |
| `air_cooler_noise_Mukherjee (induced)` | 96.1102632909 | 96.1102632909 | 7.8e-15 | 99.9615380723 | 99.9615380723 | 3.5e-14 |

Case A is the doctest of each correlation (`h_Briggs_Young` 1422.872240323,
`h_ESDU_high_fin` 1390.88891804, `h_ESDU_low_fin` 553.85383647, `h_Ganguli_VDI`
969.285081857, `dP_ESDU_high_fin` 485.630768779, `dP_ESDU_low_fin`
464.5433141865, `air_cooler_noise_GPSA` 100.5368047795,
`air_cooler_noise_Mukherjee` 99.1102632909): the values of case A and of case
B in the table above are reproduced.

The demonstration program also exercises the other branches of the non-smooth
regime switches: case A is a four-row staggered bundle (row factor F₂ = 1 for
the ESDU high-fin formula, 0.8984 for the ESDU low-fin one, coefficient 0.38
for Ganguli/VDI), case B a two-row in-line bundle (F₂ = 0.84, F₂ = 0.8479 and
coefficient 0.2). The wall property correction F₁ is exercised by giving
`Pr_wall` a value different from `Pr`.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the air-cooler correlations of `ht`, the heat-transfer
component of ChEDL, file `ht/air_cooler.py`, functions `h_Briggs_Young`,
`h_ESDU_high_fin`, `h_ESDU_low_fin`, `h_Ganguli_VDI`, `dP_ESDU_high_fin`,
`dP_ESDU_low_fin`, `air_cooler_noise_GPSA` and `air_cooler_noise_Mukherjee`,
version 1.2.0, commit 85e0ee6 (2025-12-07). The helper functions come from
`ht/core.py` (`fin_efficiency_Kern_Kraus`, which calls the modified Bessel
functions of SciPy), and the tube-row correction factor of the ESDU low-fin
formula is the table of `ht/conv_tube_bank.py`
(`ESDU_tube_row_correction`), already translated as a function of `CSL-0095`.

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; each correlation became one EES
`FUNCTION` named after the `ht` function, with the formula, the validity range,
the original reference and the `ht` module/function/version/commit in its
comment block. The Python `math.log10` became the EES `log10`, the Python
constants `minute` (60) and `hp` (745.6998715822701) became literal
conversion factors inside the two noise functions, and the two
SciPy Bessel functions were replaced by their power series (see below). The
optional `Pr_wall` argument of the two ESDU heat-transfer relations became a
mandatory argument: passing `Pr_wall = Pr` gives the correction factor 1 and
reproduces exactly what the original does when its `Pr_wall` argument is
absent. No equation was changed. Scientific basis per function: the original
paper or book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block
of each function and in `model.json` (`origin.authors`). Published under the
library license with full credit (decision D3 of the `ht` triage).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-108, family `HT-013`).** One EES
  `FUNCTION` per `ht` correlation (8 functions) plus three helper functions,
  named after the `ht` functions (`eta_fin_Kern_Kraus_aircooler` is renamed to
  leave the generic `fin_efficiency_Kern_Kraus` of inventory row `HT-023` /
  model `CSL-0109` free), the arguments of the Python functions, all in SI.
  No property function is called inside a function (rule 5 of
  `sources/ht/README.md` §7): the caller passes `rho`, `Cp`, `mu`, `k` and
  `k_fin`.
- **Modified Bessel functions.** CoolSolve has no Bessel function (the EES
  intrinsics `BESSELI`, `BESSELK`, … are listed as *not implemented* in
  `docs/ees_vs_coolsolve.csv`), so I₀, I₁, K₀ and K₁ are evaluated by their
  power series (13 terms), the same approach as `CSL-0090`. K₁ is written as
  the negative derivative of K₀, term by term (dI₀/dz = I₁,
  da_k/dz = 2k·a_k/z), because that is the form in which the derivative of the
  K₀ series can be summed with the same terms. The combined expression of
  `eta_fin_Kern_Kraus_aircooler` is unchanged. The series reproduce the SciPy
  values to 1.6·10⁻¹³ at z = 1.5 and stay exact to machine precision up to
  z = 2.5 (checked with SciPy); the demonstration program never exceeds
  z = 1.7.
- **Tube-row correction factor.** `h_ESDU_low_fin` calls
  `ESDU_tube_row_correction` in `ht`. That function is already a function of
  `CSL-0095` (*tube_bank_nusselt*); its table is written **inline** in
  `h_ESDU_low_fin` (the ladder of the `IF` branches, exactly the form of
  `CSL-0095`) so that no function name of another model is duplicated in the
  library. No equation was changed. (When `CS-FEAT-IMPORT` provides
  `$INCLUDE library:…`, the call can be restored.)
- **Staggered / in-line test.** `ht` computes `staggered =
  abs(1 - pitch_normal/pitch_parallel) > 0.05`; the same test is written in
  `h_ESDU_low_fin`, and the `h_Ganguli_VDI` branch uses `< 0.05` (in-line), as
  in the original.
- **`Pr_wall` (optional in `ht`).** Mandatory in EES: pass `Pr_wall = Pr` for
  no property correction (the correction factor is then
  (Pr/Pr_wall)^0.26 = 1 exactly, which is what omitting the argument does in
  `ht`). Both calls are exercised in the demonstration program. The wall factor
  of `ht` (`wall_factor` with the Prandtl option) chooses its exponent from
  the sign of `Pr - Pr_wall`; both exponents are 0.26 here, so the single
  expression `(Pr/Pr_wall)^0.26` is the original formula for both branches.
- **`dP_ESDU_low_fin` coefficient.** The docstring of the `ht` function prints
  `K_f = 4.71 Re^-0.286 …` but its **code** uses **4.72**; 4.72 is what
  reproduces its doctest value (464.5433141865). The EES function follows the
  code, as for `turbulent_Sandall` in `CSL-0087`.
- **Non-smooth regime switches** (tube-row factor F₂, in-line/staggered
  coefficient of `h_Ganguli_VDI`, the `induced` flag) are written with EES
  `IF/THEN/ELSE` blocks inside the functions, not with function dispatch: a
  caller selects the correlation directly.
- **Selectors not translated**: none — the eight functions of `ht/air_cooler.py`
  are all correlations. `Ft_aircooler` (the temperature-effectiveness factor
  of an air cooler) belongs to family `HT-019` (model `CSL-0105`), not to this
  card.
- **Units**: `ht` is already SI, so no unit conversion was needed. The two
  noise functions convert their inputs internally (m/s → m/min, W → hp with
  the constants of `ht`, 60 and 745.6998715822701) because the formulas of
  GPSA and Mukherjee are written in those units; the EES argument list stays SI.
- **Level**: equations 117 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The demonstration input sets are the ones of the original library, kept as
  they are: `h_Briggs_Young` is used outside its quoted Re range in case B
  (Re = 10 029 > 8000) and `h_ESDU_high_fin` / `h_ESDU_low_fin` are used on a
  low-fin, two-row bundle, which is not the high-fin geometry of ESDU 86022.
  `ht` does not check the ranges either, so its values are reproduced as they
  are: the numbers of the *Results* and *Verification* tables check the
  **equations**, not recommended design values. The validity column of the
  table above is the one to use when choosing an input.
- The 13-term Bessel series is exact for the argument range of a finned bundle
  (m·r_e ≤ 2, i.e. z ≤ 2); for a larger argument (very thin fin or very large
  `h`) the series must be extended — the number of terms is the `DUPLICATE`
  count of `bessel_mod_I_series` and `bessel_mod_K_series`.
- No air property is evaluated: the caller must supply `rho`, `Cp`, `mu`, `k`
  and `k_fin` at the bulk air temperature (and `k_fin` for the fin material).
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES (`FUNCTION`,
  `IF/THEN/ELSE`, `DUPLICATE`, `LN`, `log10`, `SQRT`, `ABS`) and runs in
  CoolSolve v0.3.0.

## Related models

- `CSL-0095` *tube_bank_nusselt*: the tube-bank Nusselt numbers of the same
  `ht` triage; its `ESDU_tube_row_correction` function is the table written
  inline in `h_ESDU_low_fin` here.
- `CSL-0090` *hx_effectiveness_ntu*: another `ht` family that evaluates a
  modified Bessel function by its power series because CoolSolve has none; the
  same approach is used here for the fin efficiency.
- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` function library of
  the batch; same layout, comment blocks and demonstration program.
- `CSL-0105` *lmtd_and_f_correction* (roadmap card C-114): the
  `Ft_aircooler` temperature-effectiveness factor of the same `ht` module,
  translated there.
- `CSL-0008`, `CSL-0077`: air-cooled condenser models that would use the
  air-side functions of this library.
- `sources/labothappy` LTP-039 (finned-tube air-side heat-transfer
  coefficient) and LTP-032 (finned-tube air-side pressure drop): the
  correlations these models need.
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.
- `CSL-0109` *fin_efficiency_and_wall_factors*: the standalone function library
  of the same `ht` core module (`HT-023`), with the same Kern-Kraus fin
  efficiency as a reusable `FUNCTION` (this model keeps its inlined helper
  `eta_fin_Kern_Kraus_aircooler` and the `bessel_mod_*_series` evaluators).
