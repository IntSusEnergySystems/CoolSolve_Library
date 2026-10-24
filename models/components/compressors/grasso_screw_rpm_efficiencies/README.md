# Example: Grasso screw isentropic efficiencies at two speeds

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0245`

Example from the Laborelec 2002 toolkit. Four Grasso screw compressors
(C-52, H-5, N-5 and S-51) are given by polynomial isentropic efficiencies.
The polynomials are evaluated at one pressure ratio, and each result is
scaled from 2940 rpm to 1500 rpm.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | none |
| **Size** | 12 equations (largest block: 1) |
| **Source** | Laborelec toolkit 2002, file `Example-Grasso Screw RPM General Simulation.EES` |
| **Authors** | Felipe Trebilcock |
| **License** | MIT |
| **CoolSolve** | 0.3.0@6c1755b — verified against the EES stored solution (see *Verification*) |

## Problem statement

This file is an example, not an examination problem. The name of the source
is `Example-Grasso Screw RPM General Simulation.EES`.

The equation window evaluates four polynomial isentropic efficiencies and
scales each of them with a power of the speed ratio. The diagram labels the
four machines `Compressor: Grasso C-52`, `Compressor: Grasso H-5`,
`Compressor: Grasso N-5` and `Compressor: Grasso S-51`.

The section title above the polynomials is the original sentence
"Isentropic efficiencies at 1500 rpm (polynomial expressions)". The
left-hand names are `epsilon_s_*_2940rpm`. Both wordings are kept. The
second section is the original sentence "Simulated efficiencies (rpm
analysis)": each 1500 rpm efficiency is the 2940 rpm value times
`(rpm1/rpm2)^m`.

`{R_P=1}` is a comment. The guess stored for `R_P` is 1. The stored
solution is `R_P = 5.4`.

## Model

The four polynomials stay as written. With \(R_P\) the pressure ratio,

\[
\varepsilon_{s,2940} = a + b(R_P-7)^2 - \frac{c}{R_P-d},
\qquad
\varepsilon_{s,1500} = \varepsilon_{s,2940}\left(\frac{\mathrm{rpm}_1}{\mathrm{rpm}_2}\right)^m
\]

| Machine | \(a\) | \(b\) | \(c\) | \(d\) |
|---|---:|---:|---:|---:|
| C-52 | 0.77 | 0.006 | 0.204 | 1.139 |
| H-5 | 0.82 | 0.00634 | 0.192 | 1.216 |
| N-5 | 0.83 | 0.00486 | 0.17 | 1.265 |
| S-51 | 0.83 | 0.00485 | 0.17 | 1.122 |

`rpm1 = 2940`, `rpm2 = 1500` and `m = -0.18` stay as written. There is no
fluid call. The four formulas do not call each other: each machine is one
polynomial and one speed scaling.

Before `R_P` is assigned, CoolSolve reports 11 equations and 12 variables
(`System square: No`). Every name except `R_P` is the left-hand side of one
equation. The closing assignment is the stored solution, `R_P = 5.4`, not
the comment value 1. With that assignment the system is square: 12 equations,
12 variables, 12 blocks of one explicit equation.

| Inputs | Value | Outputs | At 2940 rpm | At 1500 rpm |
|---|---:|---|---:|---:|
| `R_P` | 5.4 | C-52 `epsilon_s` | 0.737484 | 0.653351 |
| `rpm1` | 2940 rev/min | H-5 `epsilon_s` | 0.790341 | 0.700178 |
| `rpm2` | 1500 rev/min | N-5 `epsilon_s` | 0.801329 | 0.709913 |
| `m` | −0.18 | S-51 `epsilon_s` | 0.802678 | 0.711107 |

## How to run

Open `grasso_screw_rpm_efficiencies.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./grasso_screw_rpm_efficiencies.eescode
```

CoolSolve reports 0 iterations with the `.initials` file and 0 iterations
without it. Every block is an explicit evaluation, so the stored guesses are
not required. No `coolsolve.conf` is used. The `.initials` file is the EES
stored solution.

## Results

Pressure ratio `R_P = 5.4`, speeds 2940 rpm and 1500 rpm, exponent
`m = -0.18`. Efficiencies are dimensionless.

| Quantity | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `epsilon_s_C_52_1500rpm` | 0.6533508484 | 0.6533508484476 | 7.29e-11 |
| `epsilon_s_H_5_1500rpm` | 0.7001781976 | 0.7001781975705 | 4.21e-11 |
| `epsilon_s_N_5_1500rpm` | 0.7099125373 | 0.7099125372776 | 3.16e-11 |
| `epsilon_s_S_51_1500rpm` | 0.7111073398 | 0.7111073398208 | 2.93e-11 |
| `epsilon_s_C_52_2940rpm` | 0.7374839146 | 0.7374839145740 | 3.53e-11 |
| `epsilon_s_H_5_2940rpm` | 0.7903412987 | 0.7903412986616 | 4.86e-11 |
| `epsilon_s_N_5_2940rpm` | 0.8013291453 | 0.8013291453446 | 5.57e-11 |
| `epsilon_s_S_51_2940rpm` | 0.8026778046 | 0.8026778045816 | 2.29e-11 |
| `R_P` | 5.4 | 5.4 | 0 |
| `rpm1` [rev/min] | 2940 | 2940 | 0 |
| `rpm2` [rev/min] | 1500 | 1500 | 0 |
| `m` | −0.18 | −0.18 | 0 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Compared with the solution stored by EES X6.596 in
`Example-Grasso Screw RPM General Simulation.EES`
(`tools/compare_solution.py`, `rtol=0.001`, without `--ees-units`):
*"12 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0"*.

The largest relative difference over the 12 common variables is **7.29e-11**
(`epsilon_s_C_52_1500rpm`). Unrounded, that difference is 7.285524e-11. The
EES value is stored to ten digits (0.6533508484); CoolSolve gives
0.6533508484476. The same rounding accounts for the other efficiencies. No
common variable exceeds `rtol=0.001`.

A second comparison with `--ees-units` converted no reference value. Every
stored unit string is blank. The quoted summary above is the run without
`--ees-units`.

With the `.initials` file, CoolSolve reports all 12 equations satisfied
(max relative residual 0).

## Source and attribution

Example from the Laborelec toolkit 2002, written by Felipe Trebilcock. The
equation window is in English.

Source file (EES X6.596), collection of S. Quoilin:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/1_Compressors/1_2_Screw Compressors/Example-Grasso Screw RPM General Simulation.EES`
(inventory candidate `TM-0287`).

## Conversion log

- **2026-10-16 — import** (`tools/ees_extract.py`): the extract report gives
  `$UnitSystem SI MASS DEG KPA C KJ`. The window contains no pressure and no
  energy, and every stored unit string is blank, so no value was multiplied
  by 1000. The four polynomials, the four speed scalings, `rpm1 = 2940`,
  `rpm2 = 1500` and `m = -0.18` stay as written. `$UnitSystem` was deleted.
  The extracted window contains no `$TABSTOPS` and no `$Export`. A trailing
  NUL byte on the last line (`m=-0.18`) was stripped before solving. Comments
  were already in English. No diagram-state arrays were added: there is no
  fluid call.
- **2026-10-16 — square system**: with the NUL and `$UnitSystem` removed and
  `R_P` still unassigned, CoolSolve reports `System square: No` (11 equations,
  12 variables) and stops with "There are 11 equations and 12 unknowns. The
  system is not square and cannot be solved". `{R_P=1}` is only a comment;
  the guess is 1. The stored solution is `R_P = 5.4`. That assignment was
  added. The comment value 1 was not used. The system is then square
  (12 equations, largest block 1).
- **2026-10-16 — decoded table**: the extractor reported a parametric table
  "Table 1 (98×2)". The equation window does not call `LOOKUP` or
  `INTERPOLATE`, and `T_cd` is not a variable of the window. The decoded CSV
  pairs `epsilon_s_S_51_1500rpm` with `T_cd`, then runs into empty cells and
  zeros; one cell repeats the stored value 0.7111073398. The table was not
  imported. Verification uses the stored variables (12/12).
- **2026-10-16 — `.initials`**: the 12 values stored by EES. Convergence does
  not need them (0 iterations with the file, 0 without it).
- **Level 1** (taxonomy.md §3): 12 equations (0) + largest block 1 (0) + no
  function, procedure, array or `DUPLICATE` (0) + the four polynomials are
  not four coupled components (0) + coefficients, speeds and the exponent are
  given, with no calibration and no part-load balance (0) + explicit blocks,
  0 iterations with or without `.initials`, no `coolsolve.conf` (0) = 0 →
  Introductory. No ±1 shift.

## Limitations and CoolSolve gaps

- One pressure ratio and two speeds. The file does not build a performance
  map, a mass flow or a power.
- The polynomial coefficients and the exponent `m` are given. They are not
  fitted in this file.
- No fluid is called.
- No registered CoolSolve gap blocks this model (`missing_features` is empty).
  `$Export` was not in the extracted window.

## Related models

- `CSL-0268` (reciprocating_compressor_exponent_m): same toolkit and author,
  same `(rpm1/rpm2)^m` speed scaling, on six Grasso *reciprocating*
  compressor polynomial families over a 50-point pressure-ratio lookup table.
- `CSL-0269` (grasso_screw_catalogue_r717): the same toolkit's catalogue-data
  model of the Grasso C-52 screw compressor at 2940 rpm (24 manufacturer
  rows on R717).
