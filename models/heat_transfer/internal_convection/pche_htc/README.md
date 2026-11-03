# Printed-circuit heat exchanger (PCHE): channel heat-transfer coefficient correlations

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0322`

EES `FUNCTION`s returning the convective heat-transfer coefficient inside the semicircular channels
of a printed-circuit heat exchanger (the compact diffusion-bonded recuperator of supercritical-CO2
Brayton cycles): a straight channel (laminar Stephan-Preusser form and Gnielinski transition form, on
the hydraulic diameter of the semicircle) and the zigzag-channel fits of `PCHE_Lee` selected by the
bending angle (the **recommended zigzag correlation**, valid for alpha <= 40 deg when Re <= 2000). They
are a translation of the `printed_circuit_htc.py` module of LaboThapPy. The zigzag formula of `PCHE_conv`
is not physical as coded in the original: `h_PCHE_zigzag` returns the flag -1 and the source expression is
documented in *Limitations* only.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (Re, Pr, k, mu are arguments; the demonstration inputs are CO2-like numbers) |
| **Size** | 66 equations (largest block: 1); 7 `FUNCTION`s |
| **Source** | [LaboThapPy](https://github.com/PyLaboThap/LaboThapPy), commit `f03f7f47`, file `labothappy/correlations/convection/printed_circuit_htc.py`; inventory row `LTP-040` |
| **Authors** | Basile Chaudoir (ULiège, author of the file in the repository history); scientific authors of the fits: see *Source and attribution* |
| **License** | MIT (library); original LaboThapPy Apache-2.0 |
| **CoolSolve** | 0.4.0 — **verified** against a re-run of the original (27 values, max relative deviation 4.0e-13) |

## Problem statement

A PCHE is made of plates in which half-round channels (diameter `D_c`) are chemically etched; the
hot and cold plates are stacked and diffusion-bonded. The model needs the heat-transfer coefficient of
such a channel from the mass flux `G`, the fluid properties and the channel geometry. `CSL-0104`
(vertical-pipe Nu of near-supercritical flow), `CSL-0087`/`CSL-0091` (round-pipe Nu) and `CSL-0128`
(plate/pipe eps-NTU HX with Gnielinski branches) do not contain a semicircular-channel diameter
or the PCHE-specific fits of this file.

## Model

All functions use the hydraulic diameter of the semicircle, `Dh = pi*D_c/(2 + pi)`, and
`Re = G*Dh/mu`, `h = Nu*k/Dh`.

| `FUNCTION` | Arguments | Equation | Original |
|---|---|---|---|
| `Dh_PCHE` | `D_c` | `Dh = pi*D_c/(2+pi)` | `PCHE_conv`, `PCHE_Lee` |
| `Nu_StephanPreusser_PCHE` | `Re, Pr, Dh, L_c` | `Nu = 3.657 + 0.0677*Re*Pr*(Dh/L_c)^1.33/(1 + 0.1*Pr*(Re*Dh/L_c)^0.3)` | `PCHE_conv`, `Stephan_Preusser` |
| `Nu_GnielinskiTransition_PCHE` | `Re, Pr, Dh, L_c` | `f = (1.82*log10(Re) - 1.64)^-2`, `Nu = (f/8)*(Re-1000)*Pr/(1 + 12.7*(f/8)^0.5*(Pr^(2/3)-1))*(1 + (Dh/L_c)^(2/3))` | `PCHE_conv`, `gnielinski_transition` |
| `h_PCHE_straight` | `D_c, G, k, L_c, mu, Pr` | `Re < 2300`: Stephan-Preusser, else Gnielinski transition | `PCHE_conv`, `"Straight"` |
| `h_PCHE_zigzag` | `alpha, D_c, G, k, L_c, mu, T` | **returns -1 (not available)**: the zigzag formula of `PCHE_conv` is not physical as coded (see *Limitations*); use `h_PCHE_Lee` | `PCHE_conv`, `"Zigzag"` |
| `Nu_PCHE_Lee` | `alpha, Re, Pr` (recommended zigzag correlation) | `Re <= 2000`: `0.0479*Re^0.7089*Pr^(1/3)*(h_z/p_z)^0.3`; `Re > 2000`: `0.0845*Re^0.721*Pr^0.33` | `PCHE_Lee` |
| `f_PCHE_Lee` | `alpha, Re` | `f = 29.1955*Re^-0.5223*(h_z/p_z)^0.864` (`Re <= 2000`) | `PCHE_Lee` (computed, not returned) |
| `h_PCHE_Lee` | `alpha, D_c, G, k, mu, Pr` | `h = Nu_PCHE_Lee*k/Dh` | `PCHE_Lee` |

Channel pitch `p_z` and amplitude `h_z` of `PCHE_Lee`, by bending angle `alpha` (degrees): `alpha <= 10`:
12.93 / 1.14 mm; `<= 20`: 12.09 / 2.2 mm; `<= 30`: 10.95 / 3.16 mm; `<= 40`: 9.53 / 4 mm.

**Recommended zigzag correlation: `h_PCHE_Lee` / `Nu_PCHE_Lee`.** Validity as coded in the original:
`alpha <= 40` deg when `Re <= 2000` (the function returns -1 for `alpha > 40` there); for `Re > 2000` the
fit does not depend on `alpha`. The friction fit `f_PCHE_Lee` exists for `Re <= 2000` only (-1 otherwise).

## Niche

Nearest library models: `CSL-0104` (`supercritical_internal_nu`, Nu of vertical-pipe near-critical flow),
`CSL-0087` / `CSL-0091` (round-pipe Nu families) and `CSL-0128` (`hx_eps_ntu_plate_pipe`). What is new in
this model: the **semicircular hydraulic diameter** of the PCHE channel and the **Lee zigzag-channel fits**
(`PCHE_Lee`, piecewise in the bending angle, with the friction-factor fit). The straight-channel branches
(Stephan-Preusser laminar and Gnielinski transition) are the equations of `CSL-0128` repeated for
convenience, under PCHE names, because `$INCLUDE library:` is not available yet (`CS-FEAT-IMPORT`).

## How to run

```bash
coolsolve ./pche_htc.eescode
```

The demonstration program calls the functions: three straight-channel cases (Re = 1222, 9165 and 2300.06),
one call of `h_PCHE_zigzag` (`h_Z1`, which shows the flag -1), and ten `PCHE_Lee` cases (a `DUPLICATE` array) covering the four
angle classes, their boundary values (10, 20, 30, 40 deg) and the two Reynolds ranges. Inputs: D_c = 2 mm,
k = 0.04 W/m-K, mu = 2e-5 Pa-s, Pr = 1.5, L_c = 0.5 m (CO2-like values chosen for the demonstration, not a
state point of a cycle). The file is explicit (`Solver: SUCCESS (0 iterations)`, 66 equations)
and `pche_htc.sol` is the regression baseline. Until `$INCLUDE library:` exists (`CS-FEAT-IMPORT`), a model
using these functions copies them in a block `{--- Library functions copied from CSL-0322 ---}`.

## Results

| Case | Re [-] | h [W/m²-K] |
|---|---:|---:|
| Straight, `h_S1` (laminar branch) | 1222.03 | 120.83 |
| Straight, `h_S2` (transition branch) | 9165.23 | 1314.96 |
| Straight, `h_S3` (just above Re = 2300) | 2300.06 | 308.92 |
| Zigzag `PCHE_conv`, `h_Z1` (alpha = 15 deg, G = 100) | 6110.15 | -1 (not available) |
| `PCHE_Lee` (recommended), `h_L[1]` (alpha = 5, G = 20) | 1222.03 | 133.67 |
| `PCHE_Lee`, `h_L[2]` (alpha = 15) | 1222.03 | 166.13 |
| `PCHE_Lee`, `h_L[3]` (alpha = 25) | 1222.03 | 190.78 |
| `PCHE_Lee`, `h_L[4]` (alpha = 35) | 1222.03 | 213.47 |
| `PCHE_Lee`, `h_L[5]` (alpha = 25, G = 40) | 2444.06 | 876.54 |
| `PCHE_Lee`, `h_L[8]` (alpha = 15, G = 50) | 3055.08 | 1029.55 |

`h_L[6]`, `h_L[7]`, `h_L[9]`, `h_L[10]` (alpha = 10, 40, 20, 30) fall in the class of the lower bound
(133.67, 213.47, 166.13 and 190.78 W/m²-K). The friction-factor fit `f_L[1..4]` = 0.0874, 0.1635, 0.2436,
0.3366 for alpha = 5, 15, 25, 35 deg (Re = 1222). The `-1` returned for `f_L[5]` and `f_L[8]` flags the range
not defined by the original (Re > 2000).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. h versus alpha for PCHE_Lee, figures/pche_htc_lee.png -->

## Verification

Reference: the original `PCHE_conv` and `PCHE_Lee` re-run in a throw-away virtual environment
(`python3 -m venv --system-site-packages`, `pip install ~/git/LaboThapPy`, i.e. LaboThapPy 0.1.0 from the local
clone at commit `f03f7f47`, with CoolProp 8.0.0 and numpy as installed by pip/system), calling
`labothappy.correlations.convection.printed_circuit_htc` (`PCHE_conv` with `"Straight"`, `PCHE_Lee`) with the
same inputs as the demonstration program (script in a work folder deleted at the end; 27 reference values:
Dh, the Reynolds numbers and the `h` values). `compare_solution.py` against those values:
**27 common variables, 0 differ (rtol=0.001)**; the largest relative deviation, computed
with a short script on the same files, is **4.0e-13** (`h_L[8]`), i.e. round-off of the 13 digits
written to the `.sol`. The friction-factor fit `f_L` is not returned by the original (it is a local
variable): its values for alpha = 5, 15 and 35 deg (0.087433, 0.163520, 0.336648) were recomputed with the
same formula in a separate Python line and agree with the `.sol` to the digits printed
(0.08743343670005, 0.1635195772011, 0.3366483185174). The paper values of the Lee and Jiang correlations
were **not** checked against the publications (not available offline); the file claims fidelity to the code
of the original only.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented) of the PCHE
heat-transfer correlations of LaboThapPy, file `labothappy/correlations/convection/printed_circuit_htc.py`
(functions `PCHE_conv`, `PCHE_Lee`), commit `f03f7f47`.

> LaboThapPy - https://github.com/PyLaboThap/LaboThapPy
> Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université de Liège (ULiège),
> Université de Mons (UMONS). Original author of the file (repository history): Basile Chaudoir
> (two commits, 2025-10-22 and 2025-11-03); contributors of the library: see `AUTHORS.txt`.
> Apache License 2.0 (`LICENSE.txt`, `NOTICE.txt`; `pyproject.toml` declares MIT).

Changes: translated from Python to CoolSolve; the type switch of `PCHE_conv` was split into one function
per channel type; the nested Python functions `Stephan_Preusser` and `gnielinski_transition` became
`FUNCTION`s; the nested `if/elif` of `PCHE_Lee` became nested block `IF`s; no equation of the shipped functions was changed.

Scientific basis, as quoted in the docstrings of the original (not independently checked):
S. W. Lee, S. M. Shin, S. Chung, H. Jo, *Evaluation of thermal-hydraulic performance and economics of
Printed Circuit Heat Exchanger (PCHE) for recuperators of Sodium cooled Fast Reactors (SFRs) using CO2 and N2
as working fluids* (2022), for `PCHE_conv`; Y. Jiang, E. Liese, S. E. Zitney, D. Bhattacharyya, *Design and
Dynamic Modeling of Printed Circuit Heat Exchangers for Supercritical Carbon Dioxide Brayton Power Cycles*
(2018), and Y. Lee, S. Lee, H. B. Park, K. W. Seo, D. Lee, *Thermal-hydraulic performance analysis of zigzag
channel PCHE according to bending angle* (2024), for `PCHE_Lee`. The Gnielinski and Stephan-Preusser forms
are as in the same LaboThapPy module family (`pipe_htc.py`, see `CSL-0128`).
Source path: `~/git/LaboThapPy/labothappy/correlations/convection/printed_circuit_htc.py`.

## Conversion log

- **2026-10-31 — orchestrator correction (card C-442).** `h_PCHE_zigzag` (zigzag branch of `PCHE_conv`) no
  longer returns the source formula: it returns -1 (error flag) because the source expression is not
  physical (see *Limitations*); its two demonstration cases and the mass flow per channel were removed
  (file 73 -> 66 equations; verification 31 -> 27 values). `PCHE_Lee` is the recommended zigzag correlation.
- **2026-10-31 — translation (T-FUNC card C-442, inventory row `LTP-040`).** One `FUNCTION` per correlation;
  arguments in SI; no property call inside a function (the caller passes `Re`, `Pr`, `k`, `mu`). Unused
  arguments of the original (`mu_w`, `Pr_w`, `rho`, `L_c` in `PCHE_Lee`, `alpha` in the straight case) were
  dropped from the function signatures, and the unused Python function `sieder_tate` (the Re > 10000 branch
  is commented out in the original) and the commented-out pressure-drop line were not translated.
- `Nu_PCHE_Lee` with alpha > 40 deg and Re <= 2000 returns -1 (the original fails with an unbound variable);
  `f_PCHE_Lee` returns -1 for Re > 2000 (undefined there). Both are decisions of this translation.
- `pi` is used inside the function bodies: it works in CoolSolve 0.4.0 (the earlier `CS-BUG-PI-FUNCTION` is fixed
  in the build used; the check is the agreement of `Dh` with Python, 2.6e-13).
- **Level**: 66 equations (1) + largest block 1 (0) + functions and `DUPLICATE` (1) + no multi-zone (0) +
  no calibration (0) + no curated guesses (0) = score 2 → level 2.

## Limitations and CoolSolve gaps

- **Wavy and airfoil channels are not in the original**: `PCHE_conv` documents `type_channel` as
  "Straight / Zigzag / Wavy / Airfoil" but only `"Straight"` and `"Zigzag"` have equations; with the
  other two the original fails with `UnboundLocalError` (`Nu` unbound, run in the throw-away venv). The
  library therefore has no wavy/airfoil function; the inventory description of LTP-040 mentions them.
- **The zigzag branch of `PCHE_conv` is not physical as written, and is not shipped.** `h_PCHE_zigzag` returns -1.
  Source expression (with `Dh = pi*D_c/(2+pi)`, `Re = G*Dh/mu`, `m_dot = G*pi*D_c^2/8`, `T` the temperature in K as
  in the original, `T_C = T - 273.15`), shown for the record only (Python syntax):

  ```text
  Nu = 2.2631e6 * Re**(1.0515**1e-3) * m_dot**6.5405e-1 * alpha**(-2.0665e-4) * (L_c/D_c)**8.0885e-5
       * 2.2967e6 * m_dot**6.5429e-1 * (T-273.15)**(-1.3319e-3)     h = Nu*k/Dh
  ```

  It multiplies two prefactors (2.2631e6 and 2.2967e6) and raises `Re` to `1.0515**1e-3 = 1.00005` (a power;
  with the product 1.0515e-3 apparently intended, `Re` would be nearly absent). Evaluated by the original
  code in the throw-away venv: h = 1.0900e13 W/m²-K (alpha = 15 deg, G = 100 kg/m²-s, T = 400 K, same
  inputs as `h_Z1`) and 2.2016e12 W/m²-K (alpha = 30 deg, G = 50, T = 350 K); the CoolSolve translation
  of that expression reproduced both to 2.1e-13 before it was withdrawn. Re-evaluating the formula in Python
  with the exponent 1.0515e-3 (own check, not the original code) still gives 1.8e9 W/m²-K. Use `PCHE_Lee`.
- **Straight channel**: the power 1.33 of the Stephan-Preusser term applies to `Dh/L_c` only as written
  (`0.0677*Re*Pr*(Dh/L_c)^1.33`); with the power on the whole product `Re*Pr*Dh/L_c` the demonstration case
  `h_S1` would give 133.2 instead of 120.8 W/m²-K (own recomputation; the literature form was not checked).
  The branch switch at Re = 2300 is discontinuous: Nu = 3.72 just below and 9.44 just above (same inputs);
  Gnielinski is also used for Re > 10000 (Sieder-Tate branch commented out in the original).
- `PCHE_Lee` has no `alpha`-dependence for Re > 2000, and the Re <= 2000 fit changes by steps at the class
  boundaries 10, 20, 30, 40 deg.
- No CoolSolve gap: the file solves natively (no `missing_features`). `$INCLUDE library:` of the functions is
  the open feature `CS-FEAT-IMPORT`.

## Related models

- `CSL-0104` (supercritical_internal_nu): near-supercritical vertical-pipe Nu correlations, round pipe.
- `CSL-0087`, `CSL-0091` (internal_turbulent_nusselt, internal_laminar_and_curved_nu): round-pipe Nu families.
- `CSL-0128` (hx_eps_ntu_plate_pipe): same Stephan-Preusser and Gnielinski-transition equations.
- `CSL-0127` (hx_constant_effectiveness_discretised): sCO2 recuperator model that could use these
  coefficients.
