# Transient temperature distribution in a 1-D circular fin

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0349`

The **transient temperature distribution in a straight circular fin** of
3 cm length and 3 mm diameter, discretised into 11 nodes and integrated in
time. A constant heat flow of 0.5 W enters the base of the fin, the fin
loses heat to the ambient air by convection, and the temperature of the 11
nodes is tabulated along the trajectory. The model is the EES example that
demonstrates the solving of simultaneous differential equations with the
EES `Integral` function.

| | |
|---|---|
| **Category** | Heat transfer › Conduction, fins and radiation |
| **Fluids** | none (pure conduction and convection; no property call) |
| **Size** | 62 equations (58 in the native file, 4 for the energy-balance post-processing of the variant); largest block: 1 |
| **Source** | EES example *1-d transient conduction*, [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Integral/1-d_transient_conduction.ees) (commit 5c703d0, folder `Integral/`), inventory row `EEX-448` of `sources/ees_examples/inventory.csv`; plain-text source, no `.eez` companion (no stored solution) |
| **Authors** | S. A. Klein (University of Wisconsin–Madison); F-Chart Software (EES) |
| **License** | MIT — © F-Chart Software / S. A. Klein, MIT via EES-Community/ees-examples |
| **CoolSolve** | 0.4.0 — native file **blocked** by `CS-GAP-INTEGRAL-DUPLICATE` and `CS-GAP-INDEX-VAR`; the runnable variant `circular_fin_transient_coolsolve.eescode` **runs** and is verified by the energy balance of the fin (see *Verification*) |

## Problem statement

The original EES example states: *"This example calculates the transient
temperature distribution in a 1-D circular fin. It demonstrates the solving of
simultaneous differential equations and the use of the Integral table"*.

A circular fin (length `L`, diameter `D`, conductivity `k`, density `rho`,
specific heat `c`) is initially at the ambient temperature `T_infinity`. At
`t = 0` a constant heat flow `q_dot` enters its base; the lateral surface
loses heat to the ambient air by convection (`h_bar`). The temperature of
the 11 nodes of the fin is computed at `t` = `t_sim` = 50 s and along the
trajectory.

## Model

Finite-volume discretisation of the fin along its axis (as in the original):

- the fin is cut into 10 cells of length `Dx = L/(N-1)` = 3 mm, each with a
  node at its centre; the control volume of the base node (node 1) and of
  the tip node (node 11) is half a cell, the nine interior nodes have a full
  cell;
- the axial conduction uses a one-sided difference at the base and at the
  (adiabatic) tip, and a central difference at the interior nodes;
- the convective loss of a node is `h_bar·per·(T_infinity − T[i])` over the
  lateral surface of its control volume;
- the heat `q_dot` enters the base node.

| Quantity | Relation | Unit |
|---|---|---|
| thermal diffusivity | `alpha = k/(rho·c)` | m²/s |
| cross-sectional area | `Ac = pi·D²/4` | m² |
| perimeter | `per = pi·D` | m |
| node position | `x[i] = (i-1)·L/(N-1)` | m |
| cell length | `Dx = L/(N-1)` | m |
| base node | `dTdt[1] = 2·alpha·(T[2]-T[1])/Dx² + h_bar·per·(T_infinity-T[1])/(Ac·rho·c) + 2·q_dot/(rho·c·Ac·Dx)` | K/s |
| interior node | `dTdt[i] = alpha·(T[i+1]+T[i-1]-2·T[i])/Dx² + h_bar·per·(T_infinity-T[i])/(Ac·rho·c)` | K/s |
| tip node | `dTdt[N] = 2·alpha·(T[N-1]-T[N])/Dx² + h_bar·per·(T_infinity-T[N])/(Ac·rho·c)` | K/s |
| time integration | `T[i] = T_ini[i] + Integral(dTdt[i], time, 0, t_sim)` | °C |

Inputs (as in the original): `q_dot` = 0.5 W, `T_infinity` = 20 °C,
`h_bar` = 50 W/m²-K, `rho` = 4000 kg/m³, `k` = 10 W/m-K, `c` = 400 J/kg-K,
`L` = 3 cm, `D` = 3 mm, `N` = 11 nodes, `t_sim` = 50 s. Outputs: the
temperature `T[1..11]` of the nodes, their time derivatives `dTdt[1..11]`
and the energy balance of the fin.

## How to run

The native file `circular_fin_transient.eescode` is the faithful
transcription of the original EES file; it is **blocked** in CoolSolve (see
*Limitations and CoolSolve gaps*). The parser reads it (58 equations), but the
solver refuses it: first with *"INTEGRAL() calls inside a DUPLICATE loop are
not supported: write the equations one by one"*, and, when that loop is
written out, with *"There are 70 equations and 72 unknowns. The system is not
square and cannot be solved"* (the two array elements indexed by `N`). The
runnable variant is:

```bash
coolsolve ./circular_fin_transient_coolsolve.eescode
```

`circular_fin_transient_coolsolve.eescode` keeps every variable name and
changes only what the gaps force (every change is logged in the *Conversion
log*): the 11 integral equations are written one by one instead of inside a
`DUPLICATE` loop, the indices `N` and `N-1` of the last node are written
`11` and `10` (`N` itself stays 11), the range of the `$IntegralTable`
directive is written with the literal bounds `1..11`, and a post-processing
block adds the energy balance of the fin. The node-position loop (`x[i]`) and
the loop of the initial temperatures (`T_ini[i]`) are **not** unrolled. No
CoolSolve-only syntax is used: the variant is valid EES as well.

The variant is the regression baseline (`circular_fin_transient_coolsolve.sol`,
tested as `CSL-0349:coolsolve`). The trajectory is written next to the model
in `circular_fin_transient_coolsolve-integral.csv` (1001 rows, one every
0.05 s).

## Results

Default run (`t` = `t_sim` = 50 s):

| Node `i` | 1 (base) | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 (tip) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `x[i]` [mm] | 0 | 3 | 6 | 9 | 12 | 15 | 18 | 21 | 24 | 27 | 30 |
| `T[i]` [°C] | 102.78 | 84.19 | 69.72 | 58.52 | 49.90 | 43.35 | 38.46 | 34.94 | 32.57 | 31.21 | 30.76 |
| `dTdt[i]` [K/s] | 0.1958 | 0.1952 | 0.1934 | 0.1907 | 0.1873 | 0.1835 | 0.1797 | 0.1763 | 0.1736 | 0.1718 | 0.1712 |

| Derived quantity | Value |
|---|---|
| `alpha` [m²/s] | 6.25·10⁻⁶ |
| `Ac` [m²] | 7.0686·10⁻⁶ |
| `per` [m] | 9.4248·10⁻³ |
| `Dx` [m] | 3.0·10⁻³ |
| mean temperature rise of the fin at 50 s | 30.97 K |

The heat has not reached the tip after 50 s: the thermal penetration depth
`sqrt(alpha·t)` = 17.7 mm is shorter than the fin (30 mm), and the tip is
only 10.8 K above the ambient air while the base is 82.8 K above it. The
convective loss grows from 0 W at `t` = 0 to 0.4377 W at `t` = 50 s, i.e. 88 %
of the 0.5 W injected at the base; the rest (0.0623 W) is still stored in
the fin.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): trajectory of the
     11 node temperatures, saved in figures/, e.g.
     ![Temperature of the 11 nodes of the fin along time](figures/circular_fin_transient_trajectory.png) -->

## Verification

The source file is a **plain-text EES export without a stored solution** (no
`.eez` companion), so there is no EES reference to compare with: the
verification is the **energy balance of the fin** and a **limiting case**,
both run with the runnable variant.

**1. Energy balance of the fin** (the post-processing block of the variant;
`E_in` = the heat injected at the base over the simulation, `E_stored` = the
energy stored in the fin at the end, `E_conv` = the heat convected to the
air over the simulation):

| Quantity | Value [J] |
|---|---:|
| `E_in` = `q_dot·t_sim` = 0.5 W × 50 s | 25.000000 |
| `E_stored` = `rho·c·Ac·Dx·(0.5·(T[1]-T_infinity) + sum(T[i]-T_infinity, i=2,10) + 0.5·(T[11]-T_infinity))` | 10.505827 |
| `E_conv` = `h_bar·per·Dx·∫(0.5·(T[1]-T_infinity) + sum(T[i]-T_infinity, i=2,10) + 0.5·(T[11]-T_infinity))dt` | 14.494174 |
| `E_balance` = `E_in − (E_stored + E_conv)` | −3.4·10⁻¹³ |

The balance closes to 3.4·10⁻¹³ J (1.3·10⁻¹⁴ relative), which confirms the
half-cell control volumes of the base and of the tip and the accuracy of the
time integration. The convected heat was also recomputed **independently**,
by trapezoidal integration of the tabulated trajectory
(`circular_fin_transient_coolsolve-integral.csv`, 1001 rows): 14.494169 J,
i.e. 2.9·10⁻⁷ relative to the value of the model (the difference is the
quadrature error of the trapezoidal rule).

**2. Time-step refinement.** The same run with 2000 integration steps instead
of the default 1000 gives the same temperatures to 10 significant digits
(`T[1]` = 102.7823538774 °C in both runs) and the same energy balance; the
RK4 integration is converged.

**3. Limiting case (hand calculation).** If the fin were perfectly mixed
(no conduction gradient, no convection), the mean temperature rise would be
`q_dot·t_sim/(rho·c·Ac·L)` = 25 J / 0.33929 J/K = 73.68 K. The model gives
a mean rise of 30.97 K, i.e. less than the isothermal limit (part of the
input is already convected to the air) and the base is hotter than the
average while the tip is colder, as it must be.

The native file was **not** verified: it does not run in CoolSolve (the two
gaps of *Limitations and CoolSolve gaps*).

## Source and attribution

EES example *1-d transient conduction* of the **EES-Community/ees-examples**
repository (commit 5c703d0, folder `Integral/`), MIT-licensed, © F-Chart
Software / S. A. Klein. The file is a plain-text export of the EES
equations window (the first line points to the binary original published by
F-Chart Software); **it stores no solution**, so no EES reference could be
extracted from it.

Source file: `https://github.com/EES-Community/ees-examples/blob/5c703d0/Integral/1-d_transient_conduction.ees`
(inventory row `EEX-448` of `sources/ees_examples/inventory.csv`). The file
itself names no author; the attribution to S. A. Klein (University of
Wisconsin–Madison) and F-Chart Software follows the credit of the collection
and the `authors` column of the inventory row.

## Conversion log

- **2026-11-15 — import** (card C-519 of `roadmap.md` §6): the source is a
  plain-text EES file (`tools/ees_extract.py` cannot read it: it expects the
  binary format, and this file is the text export of the equations window),
  so the equations were transcribed by hand from the source; the header,
  the section titles and the comments were added, the comments paraphrased.
- **Unit system**: the original is `SI, K, Pa, Mass, Radian`; the model was
  converted by hand to the CoolSolve system (SI, °C, Pa, J). The ambient
  temperature `T_infinity = ConvertTemp(C,K,20 [C])` becomes `20 [C]` (the
  model uses the temperatures in differences only, which are unchanged);
  `L = 3 [cm]*Convert(cm,m)` becomes `0.03 [m]` and `D = 3 [mm]*Convert(mm,m)`
  becomes `0.003 [m]`, the original values being kept in the comments. No
  pressure, energy or angle appears in the model; the `Radian` setting is
  irrelevant. The `$UnitSystem` and `$TabStops` directives are deleted.
- **Dead code removed**: the commented-out block of the original
  (`{duplicate i=1,N / T[i]=T_ini[i] / end / time=0}`, the "arbitrary state
  variables used to check equations before integration") and the EES GUI tag
  `{$WD$ C:!EES_DEV}`.
- **`N = 11 [-]`** becomes `N = 11` (the dimensionless node count keeps the
  unit `[-]` out of the unit column, as required by the style guide).
- **Runnable variant** `circular_fin_transient_coolsolve.eescode` (the native
  file stays in valid EES and is not rewritten around the gaps):
  - `CS-GAP-INTEGRAL-DUPLICATE`: the 11 integral equations, written inside a
    `DUPLICATE i=1,N` loop in the original, are written one by one;
  - `CS-GAP-INDEX-VAR`: the last node is written `T[11]` and `T[10]` instead
    of `T[N]` and `T[N-1]`; `N` itself stays 11;
  - the range of the `$IntegralTable` directive is written with the literal
    bounds `T[1..11]`: CoolSolve does not expand a range whose bound is a
    variable (it warns *"'$IntegralTable: T[1..N]' is not a variable of the
    model; its column stays empty"* and the trajectory loses its temperature
    columns);
  - a **post-processing block** adds the energy balance of the fin
    (`E_in`, `E_stored`, `E_conv`, `E_balance`); it does not change the
    physics of the model: the tabulated trajectory is byte-identical with and
    without it (checked).
  - the node-position loop and the initial-temperature loop are **not**
    unrolled; no variable is renamed; no CoolSolve-only syntax is used.
- **Level**: equations 62 → 1 point (50–300); largest block 1 → 0 points
  (≤ 5); arrays / `DUPLICATE` → 1 point; discretised → 1 point; dynamics
  (transient problem) → 1 point; numerics → 0 points (the model solves with
  the default settings, no `.initials` and no `coolsolve.conf` needed).
  Score 4 → level 3, moved to **level 2** (pedagogical intent: a single
  textbook example of the EES `Integral` function, one algebraic block and
  explicit equations, in the neighbouring conduction category).

## Limitations and CoolSolve gaps

- **`CS-GAP-INTEGRAL-DUPLICATE`** (already registered): an `INTEGRAL` call
  inside a `DUPLICATE` loop is not supported — *"INTEGRAL() calls inside a
  DUPLICATE loop are not supported: write the equations one by one"*. The
  11 integral equations of the native file are inside such a loop, so the
  native file stops there. This gap blocks the native file
  (`missing_features`); the runnable variant writes the equations one by one.
- **`CS-GAP-INDEX-VAR`** (already registered): an array element indexed by a
  main-program variable that an equation sets to a constant is not resolved;
  `T[N]` and `T[N-1]` (with `N = 11`) become unmatched variables and the
  system is not square (*"There are 70 equations and 72 unknowns"* when the
  integral loop of the native file is written out). This gap blocks the
  native file (`missing_features`); the runnable variant writes `T[11]` and
  `T[10]`.
- The `$IntegralTable` range with a variable bound (`T[1..N]`) is not
  expanded by CoolSolve (warning, empty column): it is not registered as a
  gap, it is worked around in the variant (literal bounds).
- The model is a finite-volume discretisation with 11 nodes: the tip node
  is adiabatic (the tip face is not convected) and the base node has no
  temperature gradient inside its half cell.
- `CS-DOC-SQUARE-INTEGRAL`: the `-d` analysis of a model with `INTEGRAL` calls
  reports *"System square: No"* and no block (the states are counted as
  unknowns); the solve itself succeeds and is verified. The statistics of
  `model.json` are therefore given by hand.

## Related models

This is the transient temperature field of a circular fin heated at its
base, integrated with the EES `Integral` function, plus the energy balance
of the discretised fin.
