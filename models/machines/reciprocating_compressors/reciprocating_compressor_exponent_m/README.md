# Best speed exponent m for a family of reciprocating compressors

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0268`

Six Grasso reciprocating compressors (RC 212E … RC 1212E) are described by
identified polynomial isentropic-efficiency curves at three rotational speeds
(1500, 1000 and 725 rev/min) over a 50-point pressure-ratio grid. The
efficiency at a lower speed is simulated by scaling the 1500 rev/min curve
with `(rpm1/rpm2)^m`; the file evaluates all identified and simulated curves
at the default exponent m = 0.18, the first step towards finding the best
exponent m of the family (the comparison/sweep is left to the user, as in the
original).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | none (efficiency curves only) |
| **Size** | 1855 equations (largest block: 1) |
| **Source** | Laborelec toolkit 2002 (F. Trebilcock, ULiège Thermodynamics Lab) — `~/Nextcloud/thermo_models/modeles/LABORELEC_2002/1_Compressors/1_1_Reciprocating Compressors/Exponent m.EES` |
| **Authors** | Felipe Trebilcock (reviewers J. Lebrun, E. Winandy, per the inventory) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (see *Verification*) |

## Problem statement

As in the original: to define the best exponent m for a family of
reciprocating compressors, first all the polynomial efficiency curves at each
speed are identified (curve fits of measurement results), then the same
rotational speeds are simulated for different values of the exponent m. The
polynomial shape is
`epsilon_s = a0 + a1*(R_P_CP-7)^2 + a2/(R_P_CP-a3)` (a0/a1/a2/a3 per machine
and speed, as in the original).

## Model

For each of the 50 pressure ratios `R_P_CP[i]` of the default lookup table:

- 15 identified curves: three speeds × six machines (`EPSILON_S_MES_*`);
- 6 reference curves at 1500 rev/min (`epsilon_s_*_1500_rpm`, same
  polynomials as the identified 1500 rev/min curves);
- 12 simulated curves at 1000 and 725 rev/min, obtained by the speed scaling
  `epsilon_s_rpm2 = epsilon_s_1500*(rpm1/rpm2)^m` and
  `epsilon_s_rpm3 = epsilon_s_1500*(rpm1/rpm3)^m`, as in the original.

Inputs: `m`, `rpm1`, `rpm2`, `rpm3`, and the pressure-ratio grid in the
lookup table. Outputs: the 33 efficiency arrays (15 identified + 18
simulated, 50 rows each). All efficiencies and pressure ratios are
dimensionless; speeds stay in rev/min, as in the original.

## How to run

```
coolsolve ./reciprocating_compressor_exponent_m.eescode
```

The `.initials` file carries the stored EES values as guesses (the system is
explicit, 1855 equations, largest block 1). To study the influence of m, sweep
`m` in the *Parametric* tab of the GUI (the original did this by hand).

## Results

At the stored default point (m = 0.18, rpm1/2/3 = 1500/1000/725 rev/min), the
pressure-ratio grid runs from 1.662 to 6.141 (step ≈ 0.0914). Example values
(EES stored solution, matched by CoolSolve):

| Quantity | R_P_CP = 1.662 | R_P_CP = 6.141 |
|---|---:|---:|
| epsilon_s_RC212E_1500_rpm | 0.5504 | 0.7478 |
| epsilon_s_RC212E_1000_rpm | 0.5921 | 0.8044 |
| epsilon_s_RC212E_725_rpm  | 0.6274 | 0.8523 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of the
     simulated efficiencies vs R_P_CP for the three speeds (Parametric tab). -->

## Verification

Compared with the EES stored solution of `Exponent m.EES`
(`tools/compare_solution.py reciprocating_compressor_exponent_m.sol
reference/ees_variables.csv`, no `--ees-units`: the window contains no
pressure and no energy, so the `KPA C KJ` unit system required no numeric
conversion):

> 1855 common variables, 0 differ (rtol=0.001); only in EES: 1; only in
> CoolSolve: 0
> Only in EES reference: `i`

With `--all`, the largest relative difference is **2.54e-10** on `R_P_CP[3]`
(it comes from the 10-digit rounding of the stored solution; the table shipped
with the model holds the full-precision binary values). The variable `i` is
the DUPLICATE index, an artifact of the EES stored solution.

**Lookup-table recovery.** The pressure-ratio grid lives in the EES default
lookup table (`LOOKUP(i,1)`), embedded in the binary `.ees` file.
`ees_extract.py` reports *0 tables* for this file (its heuristic does not find
this grid; see the conversion log), so the table was hand-decoded from the
binary at file offset 238114: one column of fifty 80-bit extended values
(column header bytes `R_P`), from 1.662 to 6.141 with step ≈ 0.091408163.
The recovered values agree with the stored-solution variables `R_P_CP[1..50]`
to ≤ 5e-10 (display rounding of the stored solution). The table is shipped as
`reciprocating_compressor_exponent_m-lookup_1.csv`; CoolSolve reads the
nameless `LOOKUP(i,1)` on the table `lookup_1` (Language Reference §11).

## Source and attribution

Laborelec toolkit 2002 (F. Trebilcock, ULiège Thermodynamics Lab, December
2002, for Laborelec; reviewers J. Lebrun and E. Winandy per the source
inventory). Source file:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/1_Compressors/1_1_Reciprocating Compressors/Exponent m.EES`
(EES X6.596, stored solution 1856/1856).

## Conversion log

- **2026-10-22 — import**: extracted with `tools/ees_extract.py` (1856
  variables, 1 warning: `$UnitSystem SI MASS DEG KPA C KJ`). `$UnitSystem`
  directive removed; **no numeric conversion needed** — every coefficient of
  the polynomials and every pressure ratio is dimensionless and the speeds
  are in rev/min, so no value carries kPa or kJ (unit strings of the stored
  solution are blank). Comments translated/normalised to English (the
  original was already in English); trailing whitespace removed; section
  comments kept as in the original; the trailing "RESULTS" comment of the
  original is kept as a brace comment at the end of the file. Default lookup
  table recovered from the binary by hand (see *Verification*) and shipped as
  the companion `<name>-lookup_1.csv`; `ees_extract.py` found 0 tables in the
  470 kB file although the grid is present (stored-solution values confirm
  it) — decoder gap, not registered (no minimal reproducer; the evidence is
  the 470 kB source file itself).
- **Level**: taxonomy §3 score = equations 1855 (>1500 → 3) + largest block 1
  (→ 0) + arrays/DUPLICATE (→ 1) + semi-empirical catalogue calibration
  (→ 1) + no curated guesses (→ 0) = 5 → level 3; moved to **level 2** (±1
  pedagogical adjustment): the 1855 equations are 34 explicit formulas
  repeated by one DUPLICATE over 50 grid points, largest block 1, an
  introductory catalogue-curve exercise.

## Limitations and CoolSolve gaps

No CoolSolve gap blocks this model. Physical limitation of the original
(kept): the file evaluates the curves at one exponent (m = 0.18); choosing
the *best* m needs a sweep of m and a comparison with the identified curves,
which the original left to the user.

## Related models

- `CSL-0245` (grasso_screw_rpm_efficiencies): same toolkit and author, same
  `(rpm1/rpm2)^m` speed scaling on Grasso *screw* compressor polynomials at
  one pressure ratio (no arrays, no lookup table).
