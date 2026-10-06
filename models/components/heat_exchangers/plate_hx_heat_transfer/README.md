# Plate heat exchangers: single-phase Nusselt numbers and two-phase boiling heat-transfer coefficients

🔵 **Level 2 · Intermediate**  |  🧩 **Function library**  |  ✅ **Verified**  |  `CSL-0096`

Nine EES `FUNCTION`s for the corrugated channel of a chevron-style
plate-and-frame heat exchanger — four of them return the Nusselt number of the
single-phase channel (Kumar, Martin, Muley-Manglik, Khan-Khan), five return the
flow-boiling heat-transfer coefficient of the channel for a given heat flux
(Amalfi, Lee-Kang-Kim, Han-Lee-Kim, Huang-Sheer, Yan-Lin) — plus the two
friction-factor correlations of Martin that the Nusselt correlation calls
inside `ht`. All fluid properties are arguments: the calling model evaluates
them, as the `ht` translation rules require. Family `HT-010` of the `ht`
triage, same layout as `CSL-0087`.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | none (the correlations are fluid-independent; the properties are arguments) |
| **Size** | 68 equations after analysis (largest block: 1); 11 functions of 8–60 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), files `ht/conv_plate.py` and `ht/boiling_plate.py` (MIT), plus two friction-factor functions of the companion library [`fluids`](https://github.com/CalebBell/fluids); inventory row `HT-010` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (24 values, max deviation 3.6·10⁻¹²) |

## Problem statement

For a given flow regime (Re, Pr) and plate geometry (chevron angle, corrugation
wavelength, enlargement factor), compute the Nusselt number of the channel of a
plate heat exchanger; multiply it by `k/Dh` for the wall heat-transfer
coefficient. For flow boiling inside the channel, given the quality and a heat
flux, compute the boiling heat-transfer coefficient from the fluid properties.
Nine historical correlations are available for each case, each with its own
validity range; the choice between them is left to the user, who knows the
fluid and the geometry.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_Kumar` | Re, Pr, chevron_angle, mu, mu_wall | Nu = C1·Reᵐ·Pr^0.33·(mu/mu_wall)^0.17, C1 and m read from five chevron-angle rows of three Reynolds-number columns | Re from 0.1 to 10 000, chevron angle 30–65°; "applicable only to well designed Chevron PHEs" |
| `Nu_Martin` | Re, Pr, chevron_angle, variant | Nu = 0.122·Pr^(1/3)·[fd·Re²·SIN(2·β)]^0.374, fd from `fd_Martin_1999` (variant = 0) or `fd_Martin_VDI` (variant = 1) | Re = 200–10 000, chevron angle 0–80° |
| `Nu_Muley_Manglik` | Re, Pr, chevron_angle, plate_enlargement_factor | Nu = (0.2668 − 0.006967·β + 7.244·10⁻⁵·β²)·(20.7803 − 50.9372·φ + 41.1585·φ² − 10.1507·φ³)·Re^[0.728 + 0.0543·SIN(2πβ/90 + 3.7)]·Pr^(1/3) | Re above 1000, chevron angle 30–60°, enlargement factor 1–1.5 |
| `Nu_Khan_Khan` | Re, Pr, chevron_angle | Nu = (0.0161·β/β_max + 0.1298)·Re^(0.198·β/β_max + 0.6398)·Pr^0.35, β_max = 60° | Re = 500–2500, chevron angle 30–60°, Pr = 3.5–6 |
| `fd_Martin_1999` | Re, chevron_angle | 1/SQRT(f_f) = COS β/SQRT(0.045·TAN β + 0.09·SIN β + f0/COS β) + (1 − COS β)/SQRT(3.8·f1), fd = 4·f_f, f0 = 16/Re or (1.56·LN Re − 3)⁻², f1 = 149/Re + 0.9625 or 9.75·Re^−0.289 at Re = 2000 | Re = 200–10 000, chevron angle 0–80° |
| `fd_Martin_VDI` | Re, chevron_angle | same form with 0.18·TAN β + 0.36·SIN β, f0 = 64/Re or (1.8·LOG10 Re − 1.5)⁻², f1 = 597/Re + 3.85 or 39·Re^−0.289 | Re = 200–10 000, chevron angle 0–80° |
| `h_Amalfi` | m, x, Dh, rhol, rhog, mul, mug, kl, Hvap, sigma, q, A_channel_flow, chevron_angle | h = (kl/Dh)·{982·(β/β_max)^1.101·We_m^0.315·Bo^0.320·(ρ_l/ρ_g)^−0.224 for Bd < 4; 18.495·(β/β_max)^0.135·Re_g^0.135·Re_lo^0.351·Bd^0.235·Bo^0.198·(ρ_l/ρ_g)^−0.223 for Bd ≥ 4} | 1903-point database, refrigerants R134a, R410A, R507A, R1234yf, hydrocarbons, ammonia/water, air/water |
| `h_Lee_Kang_Kim` | m, x, D_eq, rhol, rhog, mul, mug, kl, Hvap, q, A_channel_flow | h = (kl/D_eq)·{98.7·(Re_g/Re_l)^−0.0848·Bo^−0.0597·Xtt^0.0973 for Re_g/Re_l < 9; 234.9·(Re_g/Re_l)^−0.576·Bo^−0.275·Xtt^0.66 above} | G = 14.5–33.6 kg/m²/s, q = 15–30 kW/m², x = 0.09–0.6, 200 < Re < 600, mean deviation 4.4 % |
| `h_Han_Lee_Kim` | m, x, Dh, rhol, rhog, mul, kl, Hvap, Cpl, q, A_channel_flow, wavelength, chevron_angle | h = Ge_1·(kl/Dh)·Re_eq^Ge_2·Pr^0.4·Bo_eq^0.3, Ge_1 = 2.81·(λ/Dh)^−0.041·β^−2.83, Ge_2 = 0.746·(λ/Dh)^−0.082·β^0.61 | three exchangers of 45°, 35° and 20°, G = 13–34 kg/m²/s, T = 5–15 °C, x = 0.15–0.9, q = 2.5–8.5 kW/m² |
| `h_Huang_Sheer` | rhol, rhog, mul, kl, Hvap, sigma, Cpl, q, Tsat, angle | h = 1.87·10⁻³·(kl/d_o)·(q·d_o/(kl·Tsat))^0.56·(Hvap·d_o²/α_l²)^0.31·Pr_l^0.33, d_o = 0.0146·θ·[2σ/(g(ρ_l−ρ_g))]^0.5 | 222 points for R134a and R507A, chevron angle 28–60°, q = 1.85–10.75 kW/m², G = 5.6–52.25 kg/m²/s, x = 0.21–0.95, T_sat = 1.9–13.04 °C |
| `h_Yan_Lin` | m, x, Dh, rhol, rhog, mul, kl, Hvap, Cpl, q, A_channel_flow | h = 1.926·(kl/Dh)·Re_eq·Pr_l^(1/3)·Bo_eq^0.3·Re^−0.5 | R134a, 2 channels, chevron angle 60°, x = 0.1–0.8, q = 11–15 kW/m², G = 55 and 70 kg/m²/s; 2000 < Re_eq < 10 000 |

Arguments: Re (Reynolds number on the hydraulic diameter of the channel, `[-]`),
Pr (bulk Prandtl number, `[-]`), chevron_angle (angle of the corrugations with
the vertical axis, `[degrees]`), plate_enlargement_factor (extra surface area
with respect to a flat plate, `[-]`), m (mass flow rate of one channel,
`[kg/s]`), x (quality, `[-]`), Dh (hydraulic diameter of the channel, `= 4λ/φ`,
`[m]`), D_eq (equivalent diameter of the channel, `= 4a`, `[m]`),
A_channel_flow (flow area of the fluid, `= 2·width·amplitude`, `[m²]`),
wavelength (pitch of the corrugations, `[m]`), rhol / rhog (`[kg/m³]`), mul / mug
(`[Pa·s]`), kl (`[W/m/K]`), Hvap (`[J/kg]`), sigma (`[N/m]`), Cpl (`[J/kg/K]`),
q (heat flux, `[W/m²]`), Tsat (saturation temperature, `[K]`), angle (contact
angle of the bubbles with the wall, `[degrees]`), variant (0 = friction factor
of 1999, 1 = VDI Heat Atlas), mu / mu_wall (bulk and wall viscosity, `[Pa·s]`).

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. The friction factors of
Martin come from the companion library `fluids`, which `ht` imports; they are
cited with their own module and version.

No dispatcher of the family had to be dropped: `ht/conv_plate.py` and
`ht/boiling_plate.py` export exactly nine functions, all of which are
translated here (plus the two `fluids` helpers).

## How to run

Open `plate_hx_heat_transfer.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./plate_hx_heat_transfer.eescode
```

The demonstration program after the definitions calls each of the eleven
functions: case *A* uses the input set of the `ht` doctest of the corresponding
correlation (published values), case *B* a single uniform input set describing a
60° brazed-plate R134a evaporator at 10 °C (`Re = 6000`, `Pr = 4.5`,
`m = 8·10⁻³ kg/s` per channel, `A_ch = 4·10⁻⁴ m²`, `Dh = 3·10⁻³ m`,
`D_eq = 7.4·10⁻³ m`, `λ = 3.7·10⁻³ m`, `x = 0.35`, `q = 5·10⁴ W/m²`,
`rhol = 1206 kg/m³`, `rhog = 41.9 kg/m³`, `mul = 2.6·10⁻⁴ Pa·s`,
`mug = 1.35·10⁻⁵ Pa·s`, `kl = 0.0835 W/m/K`, `Hvap = 201 300 J/kg`,
`sigma = 0.0143 N/m`, `Cpl = 1420 J/kg/K`, `T_sat = 283.15 K`). Case *B*
exercises the branches that the doctests do not reach (Amalfi with
`Bd ≥ 4`, Lee-Kang-Kim with `Re_g/Re_l ≥ 9`) and the second friction factor.
The file solves without any iteration (`Solver: SUCCESS (0 iterations)`, every
equation is explicit) and is the regression baseline
(`plate_hx_heat_transfer.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0096 ---}` and
lists `CSL-0096` in its `related` field.

## Results

Values of the demonstration program (full precision in
`plate_hx_heat_transfer.sol`):

| Quantity (case A) | value | Quantity (case B) | value |
|---|---:|---|---:|
| `fd_Martin_1999` | 0.78189 | | 1.80618 |
| `Nu_Kumar` (no viscosity correction) | 47.758 | (with the correction) | 84.022 |
| `Nu_Kumar_visc` (mu/mu_wall = 1.25) | 49.604 | | |
| `Nu_Martin` (variant = 0, Re = 2000) | 30.428 | (Re = 6000) | 159.52 |
| `Nu_Martin_VDI` (variant = 1, Re = 2000) | 30.419 | (Re = 6000) | 159.49 |
| `Nu_Muley_Manglik` | 36.491 | | 260.16 |
| `Nu_Khan_Khan` | 38.409 | | 361.42 |
| `h_Amalfi` | 776.08 | | 3071.63 |
| `h_Lee_Kang_Kim` | 1229.63 | | 1387.05 |
| `h_Han_Lee_Kim` | 675.73 | | 3051.76 |
| `h_Huang_Sheer` | 4401.06 | | 7757.65 |
| `h_Yan_Lin` | 318.72 | | 685.71 |

Units: Nu and fd are dimensionless, `h_*` in `W/m²/K`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the nine
     correlations over a Reynolds-number sweep, e.g. Nu vs Re at Pr = 1 and
     Pr = 100 for the four single-phase correlations, and h vs quality at
     q = 50 kW/m^2 for the five boiling correlations,
     figures/plate_hx_heat_transfer_nu_re.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_plate.py` and `ht/boiling_plate.py`, commit `85e0ee6`, installed from
the local clone in a throw-away virtual environment) for case *A*, plus values
computed with the same Python functions for case *B*. The 24 output values of
the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
24 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 44
```

(the 44 “only in CoolSolve” variables are the 44 input equations of the
demonstration program; the reference table holds only the 24 outputs). The
largest relative deviation over the 24 values is **3.6·10⁻¹²**
(`h_Lee_Kang_Kim_B`), i.e. round-off in the double-precision evaluation.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. | Function (case B) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|---|---:|---:|---:|
| `fd_Martin_1999` | 0.781891630837 | 0.781891630837 | 6.4e-13 | `fd_Martin_1999` | 1.806180001315 | 1.806180001315 | 2.8e-12 |
| `Nu_Kumar` | 47.7578188929 | 47.7578188929 | 1.1e-12 | `fd_Martin_VDI` | 1.805329781498 | 1.805329781498 | 1.1e-12 |
| `Nu_Kumar_visc` | 49.6042841351 | 49.6042841351 | 0.0e+00 | `Nu_Kumar` | 84.0223035481 | 84.0223035481 | 2.4e-13 |
| `Nu_Martin` | 30.4276010538 | 30.4276010538 | 1.3e-12 | `Nu_Martin` | 159.521620132 | 159.521620132 | 3.1e-12 |
| `Nu_Martin_VDI` | 30.4186720101 | 30.4186720101 | 1.3e-12 | `Nu_Martin_VDI` | 159.493531838 | 159.493531838 | 3.1e-12 |
| `Nu_Muley_Manglik` | 36.4908710060 | 36.4908710060 | 5.5e-13 | `Nu_Muley_Manglik` | 260.163013796 | 260.163013796 | 3.8e-13 |
| `Nu_Khan_Khan` | 38.4088363910 | 38.4088363910 | 1.0e-12 | `Nu_Khan_Khan` | 361.422170152 | 361.422170152 | 1.4e-12 |
| `h_Amalfi` | 776.078117910 | 776.078117910 | 7.7e-13 | `h_Amalfi` | 3071.62861698 | 3071.62861698 | 9.8e-13 |
| `h_Lee_Kang_Kim` | 1229.62712951 | 1229.62712951 | 1.6e-12 | `h_Lee_Kang_Kim` | 1387.04566543 | 1387.04566543 | 3.6e-12 |
| `h_Han_Lee_Kim` | 675.732225542 | 675.732225542 | 4.4e-13 | `h_Han_Lee_Kim` | 3051.75975493 | 3051.75975493 | 1.3e-12 |
| `h_Huang_Sheer` | 4401.05563508 | 4401.05563508 | 4.5e-13 | `h_Huang_Sheer` | 7757.64998218 | 7757.64998218 | 3.9e-13 |
| `h_Yan_Lin` | 318.722856596 | 318.722856596 | 3.1e-13 | `h_Yan_Lin` | 685.714516584 | 685.714516584 | 4.4e-13 |

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the plate-heat-exchanger correlations of `ht`, the
heat-transfer component of ChEDL, files `ht/conv_plate.py` (functions
`Nu_plate_Kumar`, `Nu_plate_Martin`, `Nu_plate_Muley_Manglik`,
`Nu_plate_Khan_Khan`) and `ht/boiling_plate.py` (functions
`h_boiling_Amalfi`, `h_boiling_Lee_Kang_Kim`, `h_boiling_Han_Lee_Kim`,
`h_boiling_Huang_Sheer`, `h_boiling_Yan_Lin`), version 1.2.0, commit `85e0ee6`
(2025-12-07). `Nu_plate_Martin` calls two friction-factor correlations of the
companion library `fluids` inside `ht`; they are translated here as
`fd_Martin_1999` and `fd_Martin_VDI`.

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.
> fluids - https://github.com/CalebBell/fluids - "Copyright (C) 2016,
> Caleb Bell", MIT License.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` named after the `ht` function (with the `Nu_` / `h_` prefix of the
library convention), the optional viscosity arguments of `Nu_plate_Kumar` became
mandatory (pass `mu = mu_wall` for the form without the correction), the Python
default values (`chevron_angle = 45` in `h_boiling_Amalfi`, `angle = 35` in
`h_boiling_Huang_Sheer`, `variant = '1999'` in `Nu_plate_Martin`) became
explicit arguments or 1/0 flags, and the Python trigonometric functions, which
take radians, were converted to the EES `SIN`/`COS`/`TAN`, which take degrees.
The `fluids` helpers (`Bond`, `Prandtl`, `thermal_diffusivity`,
`Lockhart_Martinelli_Xtt`, the two Martin friction factors) are written out as
their defining equations. No correlation equation was changed.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`); the reference of each
function is the original paper quoted in the `ht` docstring.

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-105, family `HT-010`).** Nine EES
  `FUNCTION`s of the nine correlations of the family, named after the `ht`
  function, with the formula, the validity range as quoted by `ht`, the
  original reference and the `ht` module/function/version/commit in the comment
  block. Arguments are the Python arguments, dimensionless or in SI; no
  property function is used inside the functions, so the calling model passes
  the fluid properties itself (rule 5 of `sources/ht/README.md` §7).
- **Two additional functions**, `fd_Martin_1999` and `fd_Martin_VDI` (the file
  therefore holds 11 functions for the 9 correlations of the card): they are the
  two friction-factor correlations of `fluids` that `Nu_plate_Martin` calls
  inside `ht`, and the Nusselt correlation cannot be evaluated without them.
  This is a documented addition, not a deviation from the card.
- **Non-smooth switches** use multi-line `IF/THEN/ENDIF` blocks: the two
  Reynolds-number branches of both friction factors (Re = 2000), the
  chevron-angle-row and Reynolds-number-column selection of the Kumar
  coefficient tables, the two branches of `Nu_Martin` (the `variant` flag) and
  the two branches of `h_Amalfi` (Bd = 4) and of `h_Lee_Kang_Kim` (Re_g/Re_l = 9).
  `ELSE IF`/`ELSEIF` ladders are avoided: `CS-GAP-ELSEIF-CHAIN` (the grouped
  `ENDIF;ENDIF` form does not parse) and, in CoolSolve v0.3.0, the single-line
  `IF … THEN … ENDIF` and `ELSEIF` forms inside a function body are silently
  ignored (see *Limitations*), so mutually exclusive conditions are written as
  sequential single-condition blocks.
- `Nu_Kumar`: the three coefficient tables of the original (5 chevron-angle rows
  of 3 columns, the column selected by the Reynolds number) are written as
  constant assignments in an explicit ladder — the row is selected by
  `i_angle`, then the three Reynolds-number limits of that row are compared with
  scalar `IF`s. An array table with a computed index was avoided because a
  comparison against an array element inside a function body does not work in
  CoolSolve v0.3.0 (see *Limitations*); the coefficients themselves are the
  exact values of the tables.
- `Nu_plate_Martin`: the Python `variant` string ('1999' / 'VDI') became the
  1/0 flag `variant`; `SIN(2*chevron_angle)` replaces `sin(2*radians(...))` and
  `SIN(4*chevron_angle + 3.7*180/pi())` the `sin(2*pi*beta/90 + 3.7)` of
  Muley-Manglik (the EES trigonometric functions take degrees; `pi()` is used
  because `pi` is not resolved inside a function body, `CS-BUG-PI-FUNCTION`).
- `h_boiling_Amalfi`: the exponent of `(beta/beta_max)` in the `Bd >= 4` branch
  is **0.135**, the value of the code of `ht`, while the formula printed in its
  docstring gives 0.248; the EES function follows the code, like `Nu_Sandall` in
  `CSL-0087`. The difference is not detectable on the doctest, whose input set
  stays in the `Bd < 4` branch (Bd = 0.796); case *B*, which reaches
  `Bd >= 4`, was therefore computed with the same `ht` function and reproduces
  the code exactly.
- `h_boiling_Han_Lee_Kim`: the exponents −2.83 and 0.61 are applied to the
  chevron angle β in radians, as in the code of `ht`, while the formula printed
  in its docstring applies them to (π/2 − β). The two forms coincide at
  β = 45° (the value of the doctest) and differ at 60°, which is why case *B
  (60°)* discriminates: the function follows the code and reproduces the `ht`
  value 3051.76 W/m²/K.
- `h_boiling_Huang_Sheer`: the contact angle is used in degrees, as in the code
  of `ht` (its doctest, 4401.06 W/m²/K, discriminates: the radian reading would
  give 2123.71 W/m²/K). The EES constant `g` is not resolved inside a function
  body either (`CS-BUG-PI-FUNCTION`), so the gravitational acceleration is
  written `9.80665 m/s²` in `h_Amalfi` and `h_Huang_Sheer`.
- **Selectors not translated**: none — the two modules of the family export nine
  functions and all nine are correlations.
- **Level**: equations 68 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 2 → **level 2**, the rating of the other `ht` families.

## Limitations and CoolSolve gaps

- **The single-line `IF … THEN … ENDIF` form and `ELSEIF` inside a
  `FUNCTION`/`PROCEDURE` body are silently ignored** in CoolSolve v0.3.0
  (build `0.3.0@536d427`): the condition never becomes true, the branch does not
  execute and the model solves with a wrong value and a `SUCCESS` status. The
  multi-line `IF … THEN ⏎ … ⏎ ENDIF` block works. This is the same parser
  defect as the registered bug `CS-BUG-IF-IGNORED` ("The parser never built
  `IfThenElse` nodes"), whose fix (`c8ce07c`, branch `fix/library-gaps`) is not
  in this build; no new row was added, the ID is referenced instead. Every
  conditional of this file is written as a multi-line block with a single
  condition.
- The constant `g` is not resolved inside a function body either (it evaluates
  as 1), like the constant `pi` of `CS-BUG-PI-FUNCTION`; `pi()` does work and is
  used. The two occurrences of `g` of this file (`h_Amalfi`, `h_Huang_Sheer`)
  write the constant `9.80665 m/s²` instead.
- A comparison against an **array element** inside a function body
  (`IF Re > Re_ub[1] THEN …`) also never becomes true in v0.3.0, which is why
  the coefficient tables of `Nu_Kumar` are written as scalar assignments in a
  ladder. (Part of the same defect; not registered separately.)
- The two demonstration input sets are chosen to be realistic, not to stay inside
  every quoted validity range: some calls fall outside it (case A:
  `Nu_Martin` at Re = 2000 is exactly at the boundary of the laminar branch of
  the friction factor, `h_Lee_Kang_Kim` with q = 100 kW/m² is far above the
  15–30 kW/m² of its development, `h_Han_Lee_Kim` with q = 100 kW/m² above
  8.5 kW/m²; case B: `Nu_Khan_Khan` and `Nu_Martin` outside their Reynolds
  ranges, `h_Yan_Lin` with G = 20 kg/m²/s below the 55–70 kg/m²/s of its
  development). `ht` does not check the ranges in these functions, so its values
  are reproduced as they are; the numbers of the *Results* and *Verification*
  tables check the **equations**, they are not recommended design values.
- No coolant is named: the correlations are fluid-independent and the caller
  passes the properties. A model that evaluates them itself must use the real-fluid
  EES names (`R134a`, `R410A`, `Water`, …).
- No `fluid$`, no `MODULE`/`SUBPROGRAM` and no `(T, H)` property call: nothing
  to rewrite (decisions D10 and D11 do not apply to this card).
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the pattern of this file (first `ht`
  T-FUNC card); its turbulent pipe correlations are the same physics in a
  circular duct instead of a corrugated channel.
- `CSL-0088` *nucleate_boiling_and_chf*: pool nucleate boiling and critical heat
  flux; the five `h_boiling_*` functions of this file are the flow-boiling
  counterparts for a plate channel, written for a given heat flux.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations a plate
  exchanger rating combines with the heat-transfer coefficients of this file.
- `CSL-0095` *tube_bank_nusselt*: crossflow tube banks, the other geometry of
  the same `ht` triage.
- `CSL-0027` *shell_and_tube_steam_condenser*: a condenser model that would use
  the `h_` functions of this file (or of `CSL-0089`) for its two-phase side.
- `sources/labothappy` LTP-035 (plate HTC family, quoting Martin, Han, Amalfi and
  Shah) and `sources/thermocycle` THC-011 (single-phase and plate correlations,
  Martin 2012): same physics, partly overlapping correlations; the `ht` family is
  the most complete single list and the reference for the equations.
- `CSL-0098` *flow_boiling_in_tubes*: the in-tube flow-boiling
  coefficients (Lazarek-Black, Li-Wu, Sun-Mishima, Thome, Yun-Heo-Kim, Chen,
  Liu-Winterton, Shah 1982, Gungor-Winterton 1987), same layout; a corrugated
  channel boils with both this file's plate correlations and those.
