# Internal laminar convection and curved ducts: Nusselt-number correlations

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0091`

Ten EES `FUNCTION`s returning the Nusselt number Nu of single-phase internal
flow at low Reynolds number or in non-circular / curved ducts: fully
developed laminar pipe flow at constant wall temperature (Nu = 3.66) and at
constant wall heat flux (Nu = 48/11 = 4.354), the laminar thermal entry
region of a circular pipe (Hausen, Sieder-Tate, Baehr-Stephan), laminar flow
in a rectangular duct (Shah-London), and turbulent flow in a spiral
(Morimoto-Hotta) and in helical coils (Mori-Nakayama, Schmidt, Xin-Ebadian).
All of them take dimensionless or geometric arguments only (Re, Pr, L, Di,
mu, mu_w, a_r, Dh, Rm, Dc); the wall heat-transfer coefficient follows from
`h = Nu*k/Dh` and is left to the caller, as in the source library. This is
the second family of the `ht` internal-convection module planned for the
library (roadmap cards C-96…C-119) and follows the layout of `CSL-0087`
(turbulent pipe flow, same module): one `FUNCTION` per correlation, a comment
block per function with the formula, the validity range and the dual
citation, and a demonstration program calling every function twice.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Re, Pr and the geometry are arguments) |
| **Size** | 83 equations after analysis (largest block: 1); 10 functions of 1–10 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_internal.py` (MIT); inventory row `HT-005` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (21 values, max deviation 3.2·10⁻¹³) |

## Problem statement

For a given flow regime (Re, Pr), wall state (constant temperature or
constant heat flux) and geometry (circular pipe, rectangular duct, spiral or
helical coil), compute the Nusselt number Nu of the flow; multiply it by
`k/Dh` to obtain the wall heat-transfer coefficient. Ten correlations are
available for the laminar and curved-duct cases, each with its own validity
range; the choice between them is left to the user, who knows the fluid and
the geometry.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_laminar_T_const` | dummy | Nu = 3.66 | fully developed laminar flow, constant wall temperature |
| `Nu_laminar_Q_const` | dummy | Nu = 48/11 = 4.354 | fully developed laminar flow, constant wall heat flux |
| `Nu_laminar_entry_thermal_Hausen` | Re, Pr, L, Di | Nu = 3.66 + 0.0668·Gz/(1 + 0.04·Gz^(2/3)), Gz = Di/L·Re·Pr | as in `ht` (no explicit range); Pr ≫ 1: also developing velocity profile |
| `Nu_laminar_entry_Seider_Tate` | Re, Pr, L, Di, mu, mu_w | Nu = 1.86·(Di/L·Re·Pr)^(1/3)·(mu/mu_w)^0.14 | Re < 10⁴, 0.7 < Pr < 16700 |
| `Nu_laminar_entry_Baehr_Stephan` | Re, Pr, L, Di | Nu = (3.657/tanh(2.264·Gz^(−1/3) + 1.7·Gz^(−2/3)) + 0.0499·Gz·tanh(Gz^(−1)))/tanh(2.432·Pr^(1/6)·Gz^(−1/6)) | as in `ht` (no explicit range) |
| `Nu_laminar_rectangular_Shan_London` | a_r | Nu = 8.235·(1 − 2.0421·a_r + 3.0853·a_r² − 2.4765·a_r³ + 1.0578·a_r⁴ − 0.1861·a_r⁵) | constant wall heat flux; a_r ∈ [0, 1] |
| `Nu_Morimoto_Hotta` | Re, Pr, Dh, Rm | Nu = 0.0239·(1 + 5.54·Dh/Rm)·Re^0.806·Pr^0.268 | as in `ht` (no explicit range) |
| `Nu_helical_Mori_Nakayama` | Re, Pr, Di, Dc | Pr < 1: Nu = Pr/(26.2·(Pr^(2/3) − 0.074))·Re^0.8·(Di/Dc)^0.1·(1 + 0.098/(Re·(Di/Dc)²)^0.2); Pr ≥ 1: Nu = Pr^0.4/41·Re^(5/6)·(Di/Dc)^(1/12)·(1 + 0.061/(Re·(Di/Dc)^2.5)^(1/6)) | Re·(Di/Dc)² > 0.1 |
| `Nu_helical_Schmidt` | Re, Pr, Di, Dc | Re < 2.2·10⁴: Nu = 0.023·(1 + 14.8·(1 + Di/Dc)·(Di/Dc)^(1/3))·Re^(0.8 − 0.22·(Di/Dc)^0.1)·Pr^(1/3); Re > 2.2·10⁴: Nu = 0.023·(1 + 3.6·(1 − Di/Dc)·(Di/Dc)^0.8)·Re^0.8·Pr^(1/3) | the two Re ranges |
| `Nu_helical_Xin_Ebadian` | Re, Pr, Di, Dc | Nu = 0.00619·Re^0.92·Pr^0.4·(1 + 3.455·Di/Dc) | 0.7 < Pr < 5, 0.0267 < Di/Dc < 0.0884 (data range) |

Arguments: Re (Reynolds number on Di or Dh, `[-]`), Pr (bulk Prandtl number,
`[-]`), L (pipe length, `[m]`), Di (inside diameter, `[m]`), mu and mu_w
(bulk and wall viscosity, `[Pa·s]`), a_r (duct aspect ratio, `[-]`), Dh
(hydraulic diameter, `[m]`), Rm (average spiral radius, `[m]`), Dc (helix
diameter, tube-center to tube-center, `[m]`), dummy (unused dummy argument
of the two constant functions, `[-]`).

Every function carries in its comment block (i) the equation, (ii) the
validity range **as quoted by `ht`**, (iii) the original paper or book and
(iv) the `ht` module, function, version and commit it was taken from. The
scientific basis is, for most correlations, the presentation in Bergman,
Lavine, Incropera & DeWitt, *Introduction to Heat Transfer*, 6E, Wiley,
2011, Rohsenow, Hartnett & Cho, *Handbook of Heat Transfer*, 3E,
McGraw-Hill, 1998, Baehr & Stephan, *Heat and Mass Transfer*, Springer 2013,
or Shah & London, *Supplement 1: Laminar Flow Forced Convection in Ducts*,
Academic Press, 1978; the original papers are named individually (Hausen
1943, Sieder-Tate 1936, Mori-Nakayama 1967, Schmidt 1967, Xin-Ebadian 1997,
Morimoto-Hotta 1986).

Two members of the `ht` family are **not** translated: `Nu_conv_internal`
and `Nu_conv_internal_methods` are dispatchers that map a method name to a
correlation; an EES caller calls the chosen `FUNCTION` directly.

## How to run

Open `internal_laminar_and_curved_nu.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./internal_laminar_and_curved_nu.eescode
```

The demonstration program after the definitions calls each of the 10
functions twice: once (case *A*) with the input set of the `ht` doctest of the
corresponding correlation, once (case *B*) with a second input set that
exercises the other branch of the two-branch correlations (Mori-Nakayama
Pr ≥ 1, Schmidt Re ≤ 2.2·10⁴). The Sieder-Tate function is called a third
time in case *A* with a viscosity ratio mu/mu_w = 0.8 to exercise the
correction. It solves without any iteration (`Solver: SUCCESS (0 iterations)`,
every equation is explicit) and is the regression baseline
(`internal_laminar_and_curved_nu.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0091 ---}` and
lists `CSL-0091` in its `related` field.

## Results

Values of the demonstration program (full precision in
`internal_laminar_and_curved_nu.sol`):

| Quantity (case A) | Nu [−] | Quantity (case B) | Nu [−] |
|---|---:|---|---:|
| `Nu_laminar_T_const` | 3.66 | | 3.66 |
| `Nu_laminar_Q_const` | 4.3636 | | 4.3636 |
| `Nu_laminar_entry_thermal_Hausen` (Re = 10⁵, L/Di = 10) | 39.014 | (Re = 5000, L/Di = 100) | 11.488 |
| `Nu_laminar_entry_Seider_Tate` (mu = mu_w) | 41.366 | (mu/mu_w = 2/3) | 12.385 |
| `Nu_laminar_entry_Seider_Tate_visc` (mu/mu_w = 0.8) | 40.094 | | |
| `Nu_laminar_entry_Baehr_Stephan` | 72.654 | | 12.622 |
| `Nu_laminar_rectangular_Shan_London` (a_r = 0.7) | 3.7518 | (a_r = 0.5) | 4.1258 |
| `Nu_Morimoto_Hotta` (Dh/Rm = 0.1) | 634.49 | (Dh/Rm = 0.1) | 305.55 |
| `Nu_helical_Mori_Nakayama` (Pr = 0.7 < 1) | 496.25 | (Pr = 5 ≥ 1) | 606.40 |
| `Nu_helical_Schmidt` (Re = 2·10⁵ > 2.2·10⁴) | 466.26 | (Re = 10⁴ ≤ 2.2·10⁴) | 106.65 |
| `Nu_helical_Xin_Ebadian` | 474.11 | | 341.77 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the 10
      correlations over a Reynolds-number sweep, e.g. Nu vs Re at Pr = 0.7
      and Pr = 5, figures/internal_laminar_and_curved_nu_nu_re.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_internal.py`, commit `85e0ee6`, installed from the local clone in a
throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for case *B*. The 21 output values of the demonstration
program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
21 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 62
```

(the 62 “only in CoolSolve” variables are the 62 inputs of the demonstration
program — `Re_Hausen_A`, `Pr_Hausen_A`, `L_Hausen_A`, `Di_Hausen_A`,
`Re_ST_A`, `Pr_ST_A`, `L_ST_A`, `Di_ST_A`, `mu_ST_A`, `mu_w_ST_A`,
`Re_BS_A`, `Pr_BS_A`, `L_BS_A`, `Di_BS_A`, `a_r_A`, `Re_MH_A`, `Pr_MH_A`,
`Dh_MH_A`, `Rm_MH_A`, `Re_MN_A`, `Pr_MN_A`, `Di_MN_A`, `Dc_MN_A`,
`Re_Sch_A`, `Pr_Sch_A`, `Di_Sch_A`, `Dc_Sch_A`, `Re_XE_A`, `Pr_XE_A`,
`Di_XE_A`, `Dc_XE_A` and their `_B` counterparts —; the reference
table holds only the 21 outputs). The largest relative deviation over the 21
values is **3.2·10⁻¹³** (`Nu_helical_Schmidt_B`), i.e. round-off in the
double-precision evaluation.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_laminar_T_const_A` | 3.66 | 3.66 | 0.0 |
| `Nu_laminar_Q_const_A` | 4.363636363636 | 4.363636363636 | 0.0 |
| `Nu_laminar_entry_thermal_Hausen_A` | 39.013523589885 | 39.01352358989 | 1.1e-13 |
| `Nu_laminar_entry_Seider_Tate_A` | 41.366029684589 | 41.36602968459 | 1.1e-13 |
| `Nu_laminar_entry_Seider_Tate_visc_A` | 40.093727787482 | 40.09372778748 | 1.1e-13 |
| `Nu_laminar_entry_Baehr_Stephan_A` | 72.654020465510 | 72.65402046551 | 1.1e-13 |
| `Nu_laminar_rectangular_Shan_London_A` | 3.751762675455 | 3.751762675455 | 0.0 |
| `Nu_Morimoto_Hotta_A` | 634.487947386986 | 634.4879473870 | 1.6e-13 |
| `Nu_helical_Mori_Nakayama_A` | 496.252248066333 | 496.2522480663 | 1.3e-13 |
| `Nu_helical_Schmidt_A` | 466.256999683208 | 466.2569996832 | 1.3e-13 |
| `Nu_helical_Xin_Ebadian_A` | 474.114134243448 | 474.1141342434 | 1.3e-13 |

Case *B* (second input set, computed with the same Python functions):

| Function | `ht` | CoolSolve | Function | `ht` | CoolSolve |
|---|---:|---:|---|---:|---:|
| `Nu_laminar_T_const_B` | 3.66 | 3.66 | `Nu_helical_Mori_Nakayama_B` | 606.402663522973 | 606.4026635230 |
| `Nu_laminar_Q_const_B` | 4.363636363636 | 4.363636363636 | `Nu_helical_Schmidt_B` | 106.650902770534 | 106.6509027705 |
| `Nu_laminar_entry_thermal_Hausen_B` | 11.488360610697 | 11.48836061070 | `Nu_helical_Xin_Ebadian_B` | 341.770963297939 | 341.7709632979 |
| `Nu_laminar_entry_Seider_Tate_B` | 12.384624671778 | 12.38462467178 | | | |
| `Nu_laminar_entry_Baehr_Stephan_B` | 12.622366375250 | 12.62236637525 | | | |
| `Nu_laminar_rectangular_Shan_London_B` | 4.125812203125 | 4.12581220312 | | | |
| `Nu_Morimoto_Hotta_B` | 305.553480588029 | 305.5534805880 | | | |

All 21 relative deviations are below 3.2·10⁻¹³.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the laminar and curved-duct internal-convection
correlations of `ht`, the heat-transfer component of ChEDL, file
`ht/conv_internal.py`, functions `laminar_T_const`, `laminar_Q_const`,
`laminar_entry_thermal_Hausen`, `laminar_entry_Seider_Tate`,
`laminar_entry_Baehr_Stephan`, `Nu_laminar_rectangular_Shan_London`,
`Morimoto_Hotta`, `helical_turbulent_Nu_Mori_Nakayama`,
`helical_turbulent_Nu_Schmidt` and `helical_turbulent_Nu_Xin_Ebadian`,
version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one
EES `FUNCTION` named after the `ht` function (with the `Nu_` prefix of the
library convention), the optional viscosity arguments of
`laminar_entry_Seider_Tate` became mandatory (pass `mu = mu_w` for the form
without the correction), the two constant functions received an unused dummy
argument (EES requires at least one argument in a `FUNCTION` statement,
`ht`'s take none), the Python `tanh` became the EES `TANH` and the regime
switches of `helical_turbulent_Nu_Mori_Nakayama` (Pr < 1) and
`helical_turbulent_Nu_Schmidt` (Re ≤ 2.2·10⁴) became EES `IF`. No equation
was changed. Scientific basis per function: the original paper or book
quoted in its comment block.

The scientific authors of the correlations are credited in the comment block
of each function and in `model.json` (`origin.authors`); the reference most
of them come from in `ht` is Bergman, Lavine, Incropera & DeWitt,
*Introduction to Heat Transfer*, 6E, Wiley, 2011.

## Conversion log

- **2026-10-07 — translation (T-FUNC card C-100, family `HT-005`).** One
  EES `FUNCTION` per `ht` correlation (10 functions), named `Nu_<method>`,
  with the formula, the validity range as quoted by `ht`, the original
  reference and the `ht` module/function/version/commit in the comment
  block. Arguments are the Python arguments, all dimensionless or in SI
  (`Pa·s`, `m`); no property functions are used inside the functions, so the
  calling model passes Re, Pr and the geometry itself (rule 5 of
  `sources/ht/README.md` §7).
- `laminar_T_const` and `laminar_Q_const` take no arguments in `ht`; EES
  requires at least one argument in a `FUNCTION` statement, so both received
  an unused `dummy` argument (documented in their comment blocks). The
  demonstration program passes 0.
- `laminar_entry_Seider_Tate`: `ht` makes `mu` and `mu_w` optional (no
  correction when they are absent); EES has no optional arguments, so they
  are mandatory and the caller passes `mu = mu_w` for the uncorrected form.
  Both calls are exercised in the demonstration program (case A: `mu = mu_w`
  and mu/mu_w = 0.8; case B: mu/mu_w = 2/3).
- `helical_turbulent_Nu_Mori_Nakayama` and `helical_turbulent_Nu_Schmidt`:
  the non-smooth regime switches (Pr < 1; Re ≤ 2.2·10⁴) are EES `IF`
  statements inside the function bodies, as in `CSL-0087`.
- **Selectors not translated**: `Nu_conv_internal` and
  `Nu_conv_internal_methods` only map a method name to a correlation; the
  caller chooses the `FUNCTION` directly.
- **Level**: equations 83 → 1 point (50–300), largest block 1 → 0,
  functions present → 1, multi-zone no → 0, semi-empirical/off-design no → 0,
  curated guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The two demonstration input sets are chosen to be realistic, not to stay
  inside every quoted validity range: case A calls the entry-region
  correlations at Re = 10⁵ although `ht` notes Re < 10⁴ for Sieder-Tate
  (the Hausen and Baehr-Stephan entry correlations have no quoted Re limit).
  `ht` does not check the ranges in these functions, so its values are
  reproduced as they are; the numbers of the *Results* and *Verification*
  tables are a check of the **equations**, not recommended design values.
  The validity column of the table above is the one to use when choosing an
  input.
- No friction-factor correlation is included: `ht` has none (the pipe
  friction factors are in the companion library `fluids`); `CSL-0018`
  provides the Colebrook-White factor for smooth and rough pipes in EES.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES (`FUNCTION`,
  `IF/THEN/ELSE`, `TANH`, `^`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the turbulent counterpart of this
  file — same `ht` module `ht/conv_internal.py`, same layout and same
  comment blocks; a pipe-flow model chooses between the two by regime.
- `CSL-0088` *nucleate_boiling_and_chf*: the pool-boiling family of the same
  `ht` triage, same layout; its arguments are boiling-fluid properties.
- `CSL-0089` *condensation_film*: the condensation family of the same `ht`
  triage, same layout; its `h_Shah` uses the Dittus-Boelter coefficient of
  `CSL-0087` for the single-phase part of the two-phase film.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations of a
  heat exchanger as EES functions; a rating model combines them with the
  heat-transfer coefficients of `CSL-0087` and of this file.
- `CSL-0092` *free_conv_cylinders*: the free-convection counterpart of
  `CSL-0087` (natural convection from vertical and horizontal cylinders),
  same layout; its functions take Pr and Gr instead of Re, Pr and the
  geometry.
- `CSL-0093` *free_conv_plates_and_sphere*: the other free-convection family
  of the same `ht` triage (vertical plate, horizontal plate and sphere),
  same layout.
- `CSL-0094` *external_crossflow_cylinder*: the **external** forced-convection
  counterpart of `CSL-0087` (single cylinder in crossflow), same layout.
- `CSL-0095` *tube_bank_nusselt*: the tube-bank forced-convection family of
  the same `ht` triage (Zukauskas, ESDU 73031, HEDH, row/angle corrections),
  same layout; a crossflow bundle combines its corrections with the
  single-cylinder Nu of `CSL-0094`.
- `CSL-0097` *two_phase_nonboiling_in_tube*: the two-phase non-boiling
  in-tube heat-transfer coefficients of the same `ht` triage, same layout; a
  tube carrying a condensing or evaporating mixture needs its single-phase Nu
  together with them.
- `CSL-0098` *flow_boiling_in_tubes*: the flow- and film-boiling
  coefficients of the same `ht` triage, same layout.
- `CSL-0099` *air_cooler_air_side*: the finned-bundle air-side HTC, pressure
  drop and fan noise of the same `ht` triage, same layout.
- `CSL-0100` *free_conv_enclosed_and_jackets*: the enclosed-plate,
  helical-coil and vessel-jacket correlations of the same `ht` triage, same
  layout; its helical-coil free-convection correlation is the natural
  counterpart of the helical forced-convection correlations of this file.
- `CSL-0101` *external_forced_conv_plates*: the other **external**
  forced-convection geometry of the same `ht` module `ht/conv_external.py`
  (isothermal flat plate), same layout.
- `CSL-0103` *tube_bank_dp_bell_delaware*: the shell-side pressure drop
  (Kern) and Bell-Delaware correction factors of the same `ht` triage, same
  layout.
- `CSL-0104` *supercritical_internal_nu*: the near-supercritical internal
  convection correlations of the same `ht` triage, same layout; they apply
  to the same pipe flow once the wall temperature crosses the pseudo-critical
  point of the fluid.
- `CSL-0005` *cpbar_combustion_products* and `CSL-0079`
  *brineprop_secondary_refrigerants*: the other two function libraries of
  the library (same layout: definitions + demonstration program).
- `sources/labothappy` LTP-034 (in-tube HTC correlations): the `ht` family is
  more complete and is the reference for the equations.
