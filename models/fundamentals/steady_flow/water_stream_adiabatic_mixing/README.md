# Adiabatic mixing of two water streams (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0247`

Two water streams mix at one pressure. Stream 1 is at 80 °C and 0.5 kg/s.
Stream 2 is at 20 °C. The mixture leaves at 42 °C. The pressure is written
`250e3` Pa. Steady mass and energy balances give the unknown inlet flow and
the mixture flow. Teaching exercise Cengel 5-75 from the KU Leuven
`thermo_kuleuven` collection.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water |
| **Size** | 10 equations (largest block: 2) |
| **Source** | thermo_models, file `05-75.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@6c1755b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The file name and the inventory identify the problem as Cengel 5-75, the
adiabatic mixing of two water streams. The equation window itself has no
problem text.

It gives `T_1 = 80`, `M_dot_1 = 0.5`, `T_2 = 20`, `T_3 = 42` and
`p = 250e3`. Three enthalpy calls fix the stream states. The mass balance
and the energy balance then determine `M_dot_2` and `M_dot_3`. `M_dot_2` is
an unknown. The stored 0.8695263583 kg/s is a guess, not an equation.

## Model

One open mixer, three streams, one pressure, as written in the equation
window. There is no cycle. The balances, as in the original, are

\[
\dot M_3 = \dot M_1 + \dot M_2
\]

\[
\dot M_3 h_3 = \dot M_1 h_1 + \dot M_2 h_2
\]

The first call is `Enthalpy(Water,T=T_1,P=P)`. The other two are
`enthalpy(water,t=t_2,p=p)` and `enthalpy(water,t=t_3,p=p)`. EES is
case-insensitive. CoolSolve folds `P` with `p`, `t_2` with `T_2` and `t_3`
with `T_3`: the window solved as written is square (10 equations, 10
variables), so both spellings stay. The fluid token stays `Water` on the
first call and `water` on the other two. All three calls succeed.

Three stream states of one mixer do not get diagram-state arrays. The
figure placeholder is left empty. The diagram-window RTF is empty.

| Input | Value |
|---|---|
| `T_1` | 80 °C |
| `M_dot_1` | 0.5 kg/s |
| `T_2` | 20 °C |
| `T_3` | 42 °C |
| `p` | `250e3` Pa |

Those five assignments are already equations. The system is square without
any further assignment (10 equations, 10 variables).

## How to run

```bash
coolsolve ./water_stream_adiabatic_mixing.eescode
```

The only algebraic loop is the pair `M_dot_2`, `M_dot_3` (block of 2).
CoolSolve reports 2 iterations with the shipped `.initials` and 2 iterations
without them. There is no `abs()`, so the guesses do not select a root. The
`.initials` file is the EES stored solution with no value rescaled. There is
no `coolsolve.conf` and no runnable variant.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `M_dot_2` [kg/s] | 0.8648799779852 | 0.8695263583 | 5.34e-03 |
| `M_dot_3` [kg/s] | 1.364879977985 | 1.369526358 | 3.39e-03 |
| `h_1` [J/kg] | 335173.6028164 | 531683.4005 | 3.70e-01 |
| `h_3` [J/kg] | 176106.3514343 | 384537.3096 | 5.42e-01 |
| `h_2` [J/kg] | 84147.20367329 | 299924.5261 | 7.19e-01 |

`T_1`, `T_2`, `T_3`, `p` and `M_dot_1` match. The tool prints `M_dot_2` as
0.86488 against 0.869526, `M_dot_3` as 1.36488 against 1.36953, `h_1` as
335174 against 531683, `h_3` as 176106 against 384537 and `h_2` as 84147.2
against 299925.

The solved enthalpies are liquid water at 80 °C, 20 °C and 42 °C and at
`p = 250e3` Pa. They lie 196509.80, 215777.32 and 208430.96 J/kg below the
stored values. The gap is not a constant offset, so the mixing ratio moves:
`M_dot_2` is 0.00464638 kg/s below the stored 0.8695263583 kg/s, and
`M_dot_3` is 0.00464638 kg/s below the stored 1.369526358 kg/s.

Both solutions close their own balances. On the full-precision stored
values, `0.5 + 0.8695263583364214 = 1.3695263583364214` kg/s and the energy
residual is 1.16e-10 W. On the CoolSolve solution the original mass and
energy equations are satisfied (max residual 1.4552e-11).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `05-75.EES` (EES X9.920, 10 variables),
compared with `compare_solution.py` without `--ees-units`. The tool's
summary line is:

`10 common variables, 5 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The five differences are `h_2` 7.19e-01, `h_3` 5.42e-01, `h_1` 3.70e-01,
`M_dot_2` 5.34e-03 and `M_dot_3` 3.39e-03. `T_1`, `T_2`, `T_3`, `p` and
`M_dot_1` print 0.00e+00.

The maximum relative difference over all 10 common variables, as printed by
the tool, is 7.19e-01, on `h_2`. Unrounded, that ratio is 7.1943873758e-01
(84147.20367329 J/kg against 299924.5261 J/kg).

The equations are the original ones. No input was multiplied by 1000.
`p = 250e3` stays, and the stored enthalpies were compared as stored. The
enthalpy gaps are about 1.97e5 to 2.16e5 J/kg, wider than the usual Water
residual of tens to about 1100 J/kg. The mass and energy balances stay the
original equations and are satisfied, so the model stays verified.

`Enthalpy()` prints: `Enthalpy(): t=80 looks like Fahrenheit (room temperature (~25 °C)). CoolSolve uses Celsius: T=26.67.`
The solved `h_1` is 335173.6028164 J/kg, the liquid enthalpy at 80 °C and
250 kPa. The hint did not replace the temperature. The hint "Did you mean
Water" did not print. The tokens `Water` and `water` stay.

All 10 equations are satisfied (max residual 1.4552e-11) on the run with
`.initials`.

## Source and attribution

The equation window names nobody. The EES licence tag is the J. Lebrun
laboratory licence (University of Liège) and is not the author. The inventory
authors column names S. Quoilin for this KU Leuven course file, so the
authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/05-75.EES`.

Candidate TM-0336. No duplicate group. Teaching exercise, not an exam.
EES X9.920. The diagram-window RTF is empty. The inventory `ees_units` cell
is blank, and the equation window has no `$UnitSystem` line.

## Conversion log

- **2026-10-16 — import**: `ees_extract.py` on `05-75.EES` (EES X9.920, plain text, 10 variables, no tables). The report warns that the unit-system settings were not decoded. The equation window has no `$UnitSystem` line. No number was rescaled: `T_1 = 80`, `M_dot_1 = 0.5`, `T_2 = 20`, `T_3 = 42` and `p = 250e3` stay. The stored enthalpies, about 3e5 to 5e5 J/kg, were not multiplied by 1000. The source equation text and the extraction contain no `$TABSTOPS` and no `$Export`. `$Export` is not a missing feature and not a variant. The licence tag was not copied. Solved once as written, before any spelling change: 10 equations, 10 variables, system square, largest block 2. CoolSolve treats `P` and `p` as one variable, and `t_2`/`T_2` and `t_3`/`T_3` the same way, so no name was unified. The fluid tokens stay `Water` and `water`. No diagram-state array was added. Binary mtime 2026-10-16 00:54:41 +0200, CoolSolve 0.3.0, checkout commit `6c1755b`.
- **Level**: equations 10 → 0; largest block 2 → 0; no function, procedure, array or `DUPLICATE` → 0; one mixer with three stream states, not three coupled components → 0; no calibration, off-design or dynamics → 0; 2 iterations with `.initials` and 2 without, no curated guesses required → 0. Score 0 → level 1. No ±1 shift.

## Limitations and CoolSolve gaps

The window computes the two unknown mass flows of an adiabatic mixer. It
does not compute a heat loss.

Water enthalpy in this file differs from the stored solution by 196509.80
to 215777.32 J/kg. That gap is wider than the usual residual of tens to
about 1100 J/kg, and it is not a constant reference offset, so `M_dot_2`
and `M_dot_3` move by 0.00464638 kg/s. The balances in the file are the
original equations.

`Enthalpy()` warns that `t = 80` looks like Fahrenheit. The call uses 80 °C.
The warning does not block the solve.

No CoolSolve gap. `missing_features` is empty.

## Related models

`related` is empty.
