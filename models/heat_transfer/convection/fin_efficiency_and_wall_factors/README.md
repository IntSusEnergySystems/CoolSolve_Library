# Circular-fin efficiency and wall correction factors

🟢 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0109`

Three EES `FUNCTION`s from the core module of `ht`: the **Kern-Kraus
efficiency of a circular fin** of constant thickness attached to a circular
tube (closed form with the modified Bessel functions I₀, I₁, K₀, K₁), and the
**Kays-Crawford wall correction factors** `(mu/mu_wall)^n` that multiply the
Nusselt number (`wall_factor_Nu`) or the Darcy friction factor / frictional
pressure drop (`wall_factor_fd`), with exponents by flow regime and phase.
CoolSolve has no Bessel function, so the Bessel values are evaluated inside
the fin function by their 13-term power series (the approach already used by
`CSL-0090` and `CSL-0099`).

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the functions take viscosities and fin properties as arguments) |
| **Size** | 44 equations after analysis (largest block: 1); 3 functions, all explicit |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/core.py` (MIT); inventory row `HT-023` of `sources/ht/inventory.csv` |
| **Authors** | Caleb Bell and Contributors (library); D. Q. Kern and A. D. Kraus (fin efficiency); W. M. Kays and M. E. Crawford (wall factors) |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (26 values, max deviation 4.0·10⁻¹²) |

## Problem statement

Two classical corrections of heat-exchanger design:

- **Circular fin of constant thickness** on a tube (air coolers, finned
  condensers): the fin efficiency η_f is the ratio of the actual fin heat
  rate to the heat rate of an isothermal fin at the base temperature; it
  multiplies the fin area in the area-weighted coefficient
  `h_eff = (eta_f*A_fin + A_tube_showing)/A * h` (as applied in `CSL-0099`).
- **Property variation at the wall**: a correlation fitted at constant
  properties (Nu₀, fd₀) is corrected by `(mu/mu_wall)^n`, the exponent n
  depending on the flow regime (turbulent/laminar), the phase
  (liquid/gas) and the heating/cooling direction. As in `ht`, the direction
  is detected from the viscosities themselves: heating when
  `mu > mu_wall` (the viscosity falls towards a hotter wall).

## Model

| EES `FUNCTION` | Arguments | Returns | Equation |
|---|---|---|---|
| `fin_efficiency_Kern_Kraus` | `Do`, `D_fin`, `t_fin` [m], `k_fin` [W/m-K], `h` [W/m²-K] | eta_f [−] | eta_f = 2r_o/[m(r_e²−r_o²)] · [I₁(m r_e)K₁(m r_o) − K₁(m r_e)I₁(m r_o)]/[I₀(m r_o)K₁(m r_e) + I₁(m r_e)K₀(m r_o)], m = √(2h/(k_fin·t_fin)), r_e = D_fin/2, r_o = Do/2 |
| `wall_factor_Nu` | `mu`, `mu_wall` [Pa·s], `turbulent`, `liquid` (1/0) [−] | factor [−] | factor = (mu/mu_wall)^n |
| `wall_factor_fd` | `mu`, `mu_wall` [Pa·s], `turbulent`, `liquid` (1/0) [−] | factor [−] | factor = (mu/mu_wall)^n |

Exponents `n` (Kays & Crawford, heating/cooling, as quoted in `ht`):

| Regime · phase | `wall_factor_Nu` | `wall_factor_fd` |
|---|---|---|
| Turbulent liquid | 0.11 / 0.25 | −0.25 / −0.25 |
| Turbulent gas | 0.5 / 0 | 0.1 / 0.1 |
| Laminar liquid | 0.14 / 0.14 | −0.58 / −0.5 |
| Laminar gas | 0 / 0 | −1 / −1 |

Validity: the fin solution assumes (as in `ht`) 1-D radial conduction,
steady state, no radiation, temperature-independent `k_fin`, constant `h`
over the fin, constant base temperature, no bond resistance and a fluid at
constant temperature; the wall factors were derived for internal pipe flow
but can be used elsewhere where appropriate data is missing, and `ht` flags
the turbulent-liquid and laminar-gas Nu exponents as uncertain.

Implementation notes:

- **Bessel functions.** CoolSolve has no Bessel function (flagged by the
  `ht` triage, `sources/ht/README.md` §9). The six Bessel values of the fin
  formula are evaluated in the function body by their 13-term power series
  (Abramowitz & Stegun 9.6.2 and 9.6.11), checked in Python against scipy
  (the library `ht` itself calls): exact to machine precision (≤ 2.2·10⁻¹⁵)
  for z ≤ 2, 1.4·10⁻¹⁴ at z = 2.5 and 6.6·10⁻¹³ at z = 3, degrading beyond —
  so the function is exact while **m·r_e ≤ 2** and the caller should check
  m·r_e for larger fins. The series is the same as the one shipped by
  `CSL-0099` (`bessel_mod_I_series`/`bessel_mod_K_series`); it is inlined
  here because library function names must be unique and this file must be
  self-contained.
- The unit of `h` printed in the `ht` docstring (`[W/K]`) is inconsistent
  with `m = SQRT(2h/(k_fin*t_fin))` [1/m]: `h` is a heat-transfer
  coefficient in W/m²-K (the fin function of `CSL-0099` uses the same unit).
- The Python keyword defaults (`turbulent=True`, `liquid=False`) became
  mandatory 1/0 arguments, as in the other `ht` translations.
- **Selector not translated**: `wall_factor` (the `ht` utility that
  dispatches to the coefficients by property option) only routes to the two
  functions above; an EES caller selects `wall_factor_Nu` or
  `wall_factor_fd` directly. The three input-consistency checks of
  `core.py` (`countercurrent_hx_temperature_check`, `is_heating_temperature`,
  `is_heating_property`) and `LMTD` (already translated in `CSL-0105`)
  are not part of this family.

## How to run

Open `fin_efficiency_and_wall_factors.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./fin_efficiency_and_wall_factors.eescode
```

The demonstration program after the definitions calls the fin function once
per case and each wall factor for the four regime/phase combinations
(case *A*: the `ht` doctest input set, heating direction; case *B*: a second
input set with the eight combinations in both directions, the cooling call
swapping `mu` and `mu_wall`). It solves without any iteration
(`Solver: SUCCESS (0 iterations)`, every equation is explicit) and is the
regression baseline (`fin_efficiency_and_wall_factors.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these functions copies their
definitions in a block `{--- Library functions copied from CSL-0109 ---}`
and lists `CSL-0109` in its `related` field.

## Results

Values of the demonstration program (full precision in
`fin_efficiency_and_wall_factors.sol`):

| Quantity | Case A | Case B |
|---|---:|---:|
| `eta_fin_Kern_Kraus` [−] | 0.84126 | 0.72075 |
| `wall_factor_Nu` turbulent liquid | 1.11393 | 1.05306 (heat) / 0.88914 (cool) |
| `wall_factor_Nu` laminar liquid | 1.14719 | 1.06801 (heat) / 0.93632 (cool) |
| `wall_factor_Nu` turbulent gas | 1.07417 | 1.09545 (heat) / 1.0 (cool) |
| `wall_factor_Nu` laminar gas | 1.0 | 1.0 (both) |
| `wall_factor_fd` turbulent liquid | 0.78254 | 0.88914 (heat) / 1.12468 (cool) |
| `wall_factor_fd` laminar liquid | 0.56616 | 0.76140 (heat) / 1.26491 (cool) |
| `wall_factor_fd` turbulent gas | 1.01441 | 1.01840 (heat) / 0.98193 (cool) |
| `wall_factor_fd` laminar gas | 0.86667 | 0.83333 (heat) / 1.2 (cool) |

Case A: a 3.8·10⁻⁴ m thick stainless fin (k = 200 W/m-K) of 57.15 mm outer
diameter on a 25.4 mm tube with h = 58 W/m²-K → η_f = 0.841 (the `ht`
doctest); a liquid heated from 3·10⁻⁴ Pa·s at the wall to 8·10⁻⁴ Pa·s in
the bulk, and a gas from 1.3·10⁻⁵ to 1.5·10⁻⁵ Pa·s. Case B: a copper fin
(k = 385 W/m-K, h = 250 W/m²-K) → η_f = 0.72; liquid 8·10⁻⁴/5·10⁻⁴ Pa·s
and gas 2.4·10⁻⁵/2.0·10⁻⁵ Pa·s.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. eta_f
     vs h for the two fins of the demonstration program,
     figures/fin_efficiency_and_wall_factors_eta_h.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/core.py`, commit `85e0ee6`; the installed copy is byte-identical to the
local clone at that commit) for case *A*, plus values computed with the same
Python functions for case *B*. The 26 output values of the demonstration
program were compared with `CoolSolve/tools/compare_solution.py`
(tolerance `rtol = 0.001`):

```
26 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 18
```

(the 18 "only in CoolSolve" variables are the 18 inputs of the demonstration
program — the reference table holds only the 26 outputs). The largest
relative deviation over the 26 values is **4.0·10⁻¹²**
(`wall_factor_fd_A_LG`), i.e. the 13-digit print precision of the `.sol`
baseline.

Per-value table, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `eta_fin_Kern_Kraus` | 0.8412588620231153 | 0.8412588620231 | 1.8e-14 |
| `wall_factor_Nu` TL | 1.1139265634480144 | 1.113926563448 | 1.3e-14 |
| `wall_factor_Nu` LL | 1.147190712947014 | 1.147190712947 | 1.2e-14 |
| `wall_factor_Nu` TG | 1.0741723110591495 | 1.074172311057 | 2.0e-12 |
| `wall_factor_Nu` LG | 1.0 | 1.0 | 0 |
| `wall_factor_fd` TL | 0.7825422900366437 | 0.7825422900366 | 5.6e-14 |
| `wall_factor_fd` LL | 0.5661586346885796 | 0.5661586346885 | 1.4e-13 |
| `wall_factor_fd` TG | 1.0144129637732298 | 1.014412963773 | 2.3e-13 |
| `wall_factor_fd` LG | 0.8666666666666666 | 0.8666666666701 | 4.0e-12 |

| Function (case B) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `eta_fin_Kern_Kraus` | 0.7207477935126819 | 0.7207477935127 | 2.5e-14 |
| `wall_factor_Nu` TL heat | 1.0530601975872609 | 1.053060197587 | 2.5e-13 |
| `wall_factor_Nu` LL heat | 1.0680136358372831 | 1.068013635837 | 2.7e-13 |
| `wall_factor_Nu` TG heat | 1.0954451150103321 | 1.09544511501 | 3.0e-13 |
| `wall_factor_Nu` LG heat | 1.0 | 1.0 | 0 |
| `wall_factor_Nu` TL cool | 0.8891397050194614 | 0.8891397050194 | 6.9e-14 |
| `wall_factor_Nu` LL cool | 0.9363176334504728 | 0.9363176334505 | 2.9e-14 |
| `wall_factor_Nu` TG cool | 1.0 | 1.0 | 0 |
| `wall_factor_Nu` LG cool | 1.0 | 1.0 | 0 |
| `wall_factor_fd` TL heat | 0.8891397050194614 | 0.8891397050194 | 6.9e-14 |
| `wall_factor_fd` LL heat | 0.7613956829284607 | 0.7613956829284 | 8.0e-14 |
| `wall_factor_fd` TG heat | 1.0183993761470242 | 1.018399376147 | 2.4e-14 |
| `wall_factor_fd` LG heat | 0.8333333333333334 | 0.8333333333333 | 4.0e-14 |
| `wall_factor_fd` TL cool | 1.1246826503806981 | 1.124682650381 | 2.7e-13 |
| `wall_factor_fd` LL cool | 1.2649110640673518 | 1.264911064067 | 2.8e-13 |
| `wall_factor_fd` TG cool | 0.9819330445619127 | 0.9819330445619 | 1.3e-14 |
| `wall_factor_fd` LG cool | 1.2 | 1.2 | 0 |

All 26 relative deviations are below 4.1·10⁻¹². The laminar-gas values are
exact by construction: n = 0 gives a factor of exactly 1 for Nu, and n = ±1
for fd only leaves the round-off of the printed digits.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the circular-fin efficiency and the wall correction
factors of `ht`, the heat-transfer component of ChEDL, file `ht/core.py`,
functions `fin_efficiency_Kern_Kraus`, `wall_factor_Nu` and `wall_factor_fd`
(the latter two dispatching through the utility `wall_factor`), version
1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; the Python keyword defaults
(`turbulent=True`, `liquid=False`) became mandatory 1/0 arguments; the
heating/cooling detection of `wall_factor` (`is_heating_property`:
heating when `mu > mu_wall`) is inlined as a block `IF`; the modified
Bessel functions of scipy are replaced by their 13-term power series
(exact for m·r_e ≤ 2), because CoolSolve has no Bessel function — the
closed form of the correlation itself is unchanged. No equation was
changed. Scientific basis per function: Kern & Kraus, *Extended Surface
Heat Transfer*, McGraw-Hill, 1972 (fin efficiency, also in Thulukkanam,
*Heat Exchanger Design Handbook*, 2E, CRC Press, 2013 and Bergman,
Lavine, Incropera & DeWitt, *Introduction to Heat Transfer*, 6E, Wiley,
2011); Kays & Crawford, *Convective Heat and Mass Transfer*, 3E,
McGraw-Hill, 1993 (wall factors).

## Conversion log

- **2026-10-08 — translation (T-FUNC card C-118, family `HT-023`).** Three
  EES `FUNCTION`s, one per `ht` function, named after it, with the formula,
  the validity notes as quoted by `ht`, the original reference and the `ht`
  module/function/version/commit in the comment block. Arguments are the
  Python arguments, in SI (`m`, `W/m-K`, `W/m²-K`, `Pa·s`) plus the two 1/0
  flags; no property functions are used inside the functions.
- **Bessel power series** (see *Model*): the 13-term series of Abramowitz &
  Stegun replaces scipy's `i0/i1/k0/k1`, verified in Python against scipy to
  ≤ 2.2·10⁻¹⁵ for z ≤ 2; the two demonstration cases have m·r_e = 1.12 and
  1.62. Same approach as `CSL-0090` (series/quadrature for the crossflow
  integral) and `CSL-0099` (`bessel_mod_*_series` helpers); inlined here so
  the function name stays unique across the library.
- **Heating/cooling detection inlined**: `wall_factor` dispatches on
  `is_heating_property(mu, mu_wall)` = `mu_wall < mu`; written as block
  `IF`s inside the two functions (non-smooth switch, EES `IF`).
- **Selector not translated**: `wall_factor` (dispatcher by property
  option); the caller chooses `wall_factor_Nu`/`wall_factor_fd` directly.
- **Level**: equations 44 → 0 points (< 50), largest block 1 → 0,
  functions present → 1, multi-zone no → 0, semi-empirical no → 0,
  curated guesses no → 0. Score 1 → level 1 by the score, kept at **level 2**
  (±1 rule) like every other `ht` function library of the batch
  (`CSL-0087`, `CSL-0105`…`CSL-0108`), all with the triage `level_guess = 2`.

## Limitations and CoolSolve gaps

- The fin function is exact while **m·r_e ≤ 2** (series truncation); beyond,
  the series needs more terms. The two demonstration cases stay below
  (m·r_e = 1.12 and 1.62). Typical air-cooler fins are in range; a deep
  validation call (`Do = 0.0254, D_fin = 0.06, t_fin = 2.5·10⁻⁴, k_fin = 15,
  h = 45`, m·r_e = 4.65) deviates by 2.5·10⁻⁹ from `ht` and stays negligible
  for design use, but the caller should check m·r_e.
- No gap registered for this card: everything is plain EES (`FUNCTION`,
  `DUPLICATE`, block `IF/THEN/ELSE`, `LN`, `SQRT`, `^`) and runs in
  CoolSolve v0.3.0. The absence of Bessel functions in CoolSolve is known
  (documented in `CSL-0090` and `CSL-0099`); registering it would need
  evidence that EES provides built-in Bessel functions, which was not
  available offline (unverified suggestion only).
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  functions copies the definitions for now.

## Related models

- `CSL-0099` *air_cooler_air_side*: the finned-bundle air-side family of the
  same `ht` triage; it contains the same Kern-Kraus fin efficiency
  (`eta_fin_Kern_Kraus_aircooler`) and the same Bessel series
  (`bessel_mod_I_series`/`bessel_mod_K_series`) as helpers of its `h`
  correlations, and applies the fin area correction exactly as described
  here.
- `CSL-0087` *internal_turbulent_nusselt*: the turbulent pipe-flow Nu
  correlations that the wall factors correct (e.g. Sieder-Tate is the
  fixed-exponent 1/6.14 form); the `fd` factors apply to the pipe friction
  factors of `CSL-0018` (`pipe_pressure_drop_colebrook`).
