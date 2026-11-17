# Lumped-capacitance cooling of a sphere in a fluid

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0343`

A solid sphere initially at 400 °C is cooled by convection to a fluid medium
at 20 °C. The energy balance of the lump (a single thermal capacitance) is
integrated in time with the EES `INTEGRAL` function, and the closed-form
solution of the same equation is computed beside it. The native file keeps the
EES *table-based* two-argument `INTEGRAL` and is therefore **blocked**
(`CS-GAP-INTEGRAL-2ARG`); a runnable variant, `lumped_capacitance_cooling_coolsolve.eescode`,
uses the equation-based `INTEGRAL` with explicit limits and is verified against
the solution stored by EES.

| | |
|---|---|
| **Category** | Fundamentals › Tanks and vessels |
| **Fluids** | – (no property call: the medium is only characterised by its temperature) |
| **Size** | 12 equations (the `-d` analysis of the native file reports 11 blocks, largest block 2; the block statistics of a model with `INTEGRAL` calls are not usable, `CS-DOC-SQUARE-INTEGRAL`) |
| **Source** | EES example library of F-Chart Software — `~/Nextcloud/thermo_models/EES_library/Difeqn1.ees` (EES X8.806); plain-text mirror: [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/difeqn1.ees) (MIT); inventory row `EEL-049` |
| **Authors** | S. A. Klein — the examples are © F-Chart Software |
| **License** | MIT (via the EES-Community mirror) |
| **CoolSolve** | 0.4.0@cc582a6 — native file blocked by `CS-GAP-INTEGRAL-2ARG`; the runnable variant is verified against the EES stored solution (see *Verification*) |

## Problem statement

The original file (F-Chart's EES example "Difeqn1") states: *"The problem is
to solve for the temperature of a single lump which has an initial temperature
of 400 °C and it is transferring energy to a fluid medium at 20 °C."* The file
demonstrates the `Integral` function used with a Parametric table (the *Table-based
Integral function*) and states that the same problem *"could have been solved
more simply with the Equation-based Integral function which offers the
advantages of having automatic step size adjustment"*.

The lump is a sphere of radius 5 mm, density 3000 kg/m³ and specific heat
1000 J/kg·K, cooled by convection to a fluid at 20 °C with a heat-transfer
coefficient of 10 W/m²·K.

**Niche.** This is the textbook *lumped-capacitance* cooling of a body in a
fluid, integrated in time — a single thermal capacitance and a single
convective boundary. It is not the **building RC network** of `CSL-0042`
(a discretised wall/zone network with weather files), not the **dynamic storage
tank** of `CSL-0009` (a charged/discharged hot-water tank with a stratified
node) and not the **phase-change tank** of `CSL-0041` (ice melting in a tank);
it is also not the **steady** vessel energy balance of `CSL-0230`. Its
interest is didactic: it is the shortest possible `INTEGRAL` model (one state,
one algebraic derivative), it shows the table-based and the equation-based
forms of the EES `Integral` function, and it comes with its own closed-form
solution, which makes it a check of the integrator itself.

## Model

The lump is isothermal (lumped capacitance) and exchanges heat with the
surrounding fluid by convection only:

- the energy balance of the lump, with `A = 4πr²` and `V = 4/3 πr³`:

  `ρ·V·c·dTdt = −h·A·(T − T_∞)` ;

- the temperature is the integral of that derivative,
  `T = T_i + ∫ dTdt dt` (EES: `integral(dTdt, Time)`);

- the closed-form solution of the same linear ODE, which the original computes
  beside the numerical one:

  `(T_exact − T_∞)/(T_i − T_∞) = exp(−h·A/(ρ·c·V)·Time)` .

The time constant of the lump is `τ = ρ·c·V/(h·A) = 500 s`: with the data of
the file, `h·A/(ρ·c·V) = 2·10⁻³ s⁻¹`, so the lump cools by a factor `e` every
500 s and is at 71.43 °C after 1000 s.

| Input | Value | Meaning (as in the original) |
|---|---|---|
| `r` | 0.005 m | radius of the sphere |
| `rho` | 3000 kg/m³ | density of the lump |
| `c` | 1000 J/kg·K | specific heat of the lump |
| `T_i` | 400 °C | initial temperature of the lump |
| `T_infinity` | 20 °C | temperature of the fluid medium |
| `h` | 10 W/m²·K | heat-transfer coefficient |

| Output | Meaning |
|---|---|
| `T` | temperature of the lump at the end of the integration (variant) or at `Time` (native file) |
| `T_exact` | closed-form solution at the same time |
| `dTdt` | time derivative of the temperature of the lump [K/s] |

## How to run

The native file `lumped_capacitance_cooling.eescode` is the faithful
transcription of the EES equations and **does not run** in CoolSolve: the
two-argument table-based `integral(dTdt, Time)` is not supported
(`CS-GAP-INTEGRAL-2ARG`):

```
=== Solver Error ===
Status: EvaluationError
Message: INTEGRAL() expects 4 or 5 arguments (integrand, var, lo, hi[, step]); got 2 (line 42).
```

The runnable variant `lumped_capacitance_cooling_coolsolve.eescode` solves in
one second:

```bash
/sylvain/git/csl-lanes/minimax/CoolSolve/build/coolsolve \
    ./models/fundamentals/tanks_vessels/lumped_capacitance_cooling/lumped_capacitance_cooling_coolsolve.eescode
```

No guess file is needed (the integration is explicit); the baseline is
`lumped_capacitance_cooling_coolsolve.sol`, which is tested as
`CSL-0343:coolsolve`. The trajectory is written to
`lumped_capacitance_cooling_coolsolve-integral.csv` (11 rows, every 100 s) and
is stored in the `.sol` baseline.

## Results

Trajectory of the lump (runnable variant, RK4 integration, 1 s steps) against
the EES parametric table stored in the original file:

| Time [s] | `T` (CoolSolve) [°C] | `T` (EES table-based) [°C] | `T_exact` (CoolSolve) [°C] | `T_exact` (EES) [°C] |
|---:|---:|---:|---:|---:|
| 0 | 400.000 | 400.000 | 400.000 | 400.000 |
| 100 | 331.118 | 330.909 | 331.118 | 331.118 |
| 200 | 274.722 | 274.380 | 274.722 | 274.722 |
| 300 | 228.548 | 228.129 | 228.548 | 228.548 |
| 400 | 190.745 | 190.288 | 190.745 | 190.745 |
| 500 | 159.794 | 159.326 | 159.794 | 159.794 |
| 600 | 134.454 | 133.994 | 134.454 | 134.454 |
| 700 | 113.707 | 113.268 | 113.707 | 113.707 |
| 800 | 96.721 | 96.310 | 96.721 | 96.721 |
| 900 | 82.814 | 82.436 | 82.814 | 82.814 |
| 1000 | 71.427 | 71.084 | 71.427 | 71.427 |

At the end of the integration (1000 s) the variant gives
`T` = 71.42740764 °C, `T_exact` = 71.42740763 °C and
`dTdt` = −0.1028548 K/s.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): trajectory plot of T and T_exact
     against time (CoolSolve, Integral tab), saved in figures/, e.g.
     ![Trajectory of the lump temperature](figures/lumped_capacitance_cooling_trajectory.png) -->

## Verification

**Reference.** The solution stored by EES in
`~/Nextcloud/thermo_models/EES_library/Difeqn1.ees` (12 variables) and the
Parametric table stored in the same file (11 rows × 3 columns: `T`, `T_exact`,
`Time`). Both were extracted with `tools/ees_extract.py`.

**Comparison with the stored solution** (`compare_solution.py`, runnable
variant against `reference/ees_variables.csv`):

```
12 common variables, 2 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 2
```

The two deviations are `T` (4.81e-03) and `dTdt` (6.68e-03); all the other
variables agree exactly, and the closed-form solution `T_exact` agrees to
1.26e-12 (EES 71.42740763 °C against CoolSolve 71.42740762991 °C). The two
deviations are **the integration error of EES, not of CoolSolve**:

- the EES value of `T` is the one of the *table-based* integral function, whose
  table is marched with a 100 s step; the trapezoidal rule with that step
  reproduces the 11 values of the EES parametric table to a relative difference
  of at most 1.2e-09, i.e. the stored EES trajectory is
  `T(t) = T_∞ + (T_i − T_∞)·(9/11)^(t/100 s)`, which lies below the closed
  form by 0.063 % at 100 s and 0.48 % at 1000 s;
- the runnable variant integrates with RK4 and a 1 s step, so it follows the
  closed form to a relative difference of 1.6e-10 at 1000 s.

**Analytical check.** With the data of the file, `h·A/(ρ·c·V)` =
`10·4π·0.005²/(3000·1000·4/3·π·0.005³)` = 2.0e-03 s⁻¹, hence
`T_exact(1000 s) = 20 + 380·exp(−0.002·1000)` = **71.42740763 °C**, the value
stored by EES; the variant gives 71.42740763 °C.

**Comparison with the parametric table.** The trajectory of the variant
(`$IntegralTable Time:100 T T_exact`, 11 rows) against the 11 rows of the EES
parametric table: `T_exact` agrees to at most 1.9e-06 (the `.sol` prints the
trajectory with six significant digits) and `T` differs by at most 4.84e-03 —
the EES integration error described above, which grows with time exactly as the
trapezoidal error of a 100 s step does.

## Source and attribution

S. A. Klein, F-Chart Software — EES example "Difeqn1" of the example library
of EES (© F-Chart Software). The plain-text mirror published under the MIT
licence by [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples)
(commit 5c703d0, 2026-03-01), file `Case_Study/difeqn1.ees`, is the source of
the licence. The binary file of the collection is
`~/Nextcloud/thermo_models/EES_library/Difeqn1.ees` (EES X8.806, inventory row
`EEL-049`); its `{$ID$ #0001: For use only by Professor S.A. Klein University of
Wisconsin - Madison klein}` stamp identifies the EES licence holder, not the
author of the model.

## Conversion log

- **2026-11-14 — import**: `tools/ees_extract.py` on
  `~/Nextcloud/thermo_models/EES_library/Difeqn1.ees` (EES X8.806, 12 variables,
  1 parametric table of 11 rows × 3 columns, no lookup table). The extracted
  report gives the unit system `SI MASS DEG KPA C KJ`; **the model needs no
  unit conversion**: it uses no pressure, its energies are already in J/kg·K
  and its temperatures in °C (`rho` in kg/m³, `c` in J/kg·K, `h` in W/m²·K,
  `r`, `A`, `V` in m, m², m³, the times in s). The `$UnitSystem` directive was
  deleted, as the style guide requires. The EES editor directives `$TabStops`
  and `$ShowWindow Solution` were removed (display settings of the EES
  editor); the comments were kept in English, as in the original.
- **2026-11-14 — inputs restored**: `Time`, the independent variable swept by
  the EES Parametric table (0 to 1000 s, step 100 s), is given in the native
  file the value of the last row of that table (1000 s), which is the state the
  solution stored by EES holds; the whole table is reproduced by the runnable
  variant (workaround of `CS-GAP-PARAMETRIC`: *default run in the equations,
  table documented in the README*). The equations, the variable names and the
  order of the original are otherwise unchanged.
- **2026-11-14 — runnable variant** `lumped_capacitance_cooling_coolsolve.eescode`:
  the gap `CS-GAP-INTEGRAL-2ARG` forces the two-argument table-based
  `integral(dTdt, Time)` to be written as the equation-based
  `INTEGRAL(dTdt, Time, 0, Time_final)`; the end of the integration is given by
  the input `Time_final` = 1000 s (last row of the parametric table) and the
  trajectory is tabulated every 100 s. Nothing else is changed: the equations,
  the variable names and the units are those of the native file.
- **Level**: taxonomy §3 score — equations 12 (< 50 → 0), largest algebraic
  block 2 (≤ 5 → 0; the blocks of a model with `INTEGRAL` calls are not
  reliable, `CS-DOC-SQUARE-INTEGRAL`), no function/procedure/array (0), no
  multi-zone structure (0), dynamics (1), no curated guess needed (0) — total
  1 → **level 1** (as the inventory row `EEL-049` announces).

## Limitations and CoolSolve gaps

- `CS-GAP-INTEGRAL-2ARG` — the EES *Table-based Integral function*
  (`integral(f, t)`, the two-argument form) is not supported: CoolSolve only
  parses the equation-based four/five-argument form `INTEGRAL(f, t, lo, hi[, step])`.
  This blocks the **native file**; the runnable variant uses the equation-based
  form with the limits of the parametric table. Reported in the CoolSolve gap
  register with a minimal reproducer.
- The physical limits of the model are those of the lumped-capacitance
  approximation itself (a single temperature for the lump, a constant `h`,
  a constant ambient temperature) — the original makes the same assumptions.

## Related models

- `CSL-0042` (*3R2C building thermal network with weather lookup*): dynamic
  thermal model solved with `INTEGRAL`, but a discretised building network with
  weather files, not a single lump.
