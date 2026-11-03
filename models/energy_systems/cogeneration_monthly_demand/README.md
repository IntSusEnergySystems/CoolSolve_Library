# Cogeneration monthly balance and annual demand (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0233`

Teaching exercise of the ULiège course MSTh (*Machines et systèmes thermiques*),
repetition TP 12, exercise 2, file dated 2005-12-13. The equation window
computes a monthly balance for November and December: the water capacity rate,
the slope, the heat demand, the captured heat and the backup energy, then the
annual demand in kWh. November and December temperatures are assigned and no
other equation uses them.

| | |
|---|---|
| **Category** | Energy systems › Cogeneration |
| **Fluids** | none |
| **Size** | 17 equations (largest block: 1) |
| **Source** | thermo_models, file `MSTH051213 EXERCICE 2.EES` |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

The equation window is titled `MSTH051213 exercice 2`. It contains no longer
statement. As written, it sets a mass flow, a specific heat and a parameter
`A`, forms the capacity rate and the slope, then a monthly balance.

November and December each have a temperature and an intersection note. The
monthly balance subtracts the captured heat rate from the demand and turns
the backup heat rate into energy over 30 days. A ratio of captured heat to
demand is formed for each month. The last equation is the annual demand in
kWh over 365 days.

## Model

The assignments `M_dot = 150/(24*3600)`, `c_w = 4187`, `A = 5` and
`Q_dot_demande = C_dot*(55-10)` are equations. `c_w` is in J/kg-K, so
`C_dot = M_dot*c_w` is in W/K and the demand is in W. The slope is

\[
\mathrm{pente} = C_\mathrm{dot}\times 24/A
\]

with `24` and `A` as written, so `pente` has the unit of `C_dot` (W/K). The
source notes that one finds `pente = 34.89`. That note is a comment.

The intersection notes `350` and `200` are comments. The same numbers already
stand in the captured-heat equations:

\[
\dot Q_\mathrm{capté,nov} = 350\,(A/24), \qquad
\dot Q_\mathrm{capté,dec} = 200\,(A/24)
\]

Backup heat rate is demand minus captured heat rate. Backup energy uses 30
days in both months, including December:

\[
Q_\mathrm{appoint,kWh} = \dot Q_\mathrm{appoint}\times 30\times 24/1000
\]

The annual demand uses 365 days:

\[
Q_\mathrm{demande,kWh,an} = \dot Q_\mathrm{demande}\times 365\times 24/1000
\]

`t_nov = 5.5` °C and `t_dec = 3.5` °C stay. No other equation uses them.
There is no fluid and no property call, so no diagram-state array is added.

| Input | Value |
|---|---|
| `M_dot` | `150/(24*3600)` kg/s |
| `c_w` | 4187 J/kg-K |
| `A` | 5, as written (the window states no unit) |
| `t_nov` | 5.5 °C |
| `t_dec` | 3.5 °C |
| demand | `C_dot*(55-10)` W |
| November capture | `350*(A/24)` W |
| December capture | `200*(A/24)` W |

The window is square: 17 equations and 17 variables. No stored value was
turned into an extra equation.

## How to run

```bash
coolsolve ./cogeneration_monthly_demand.eescode
```

Every block is explicit (17 blocks of size 1). CoolSolve reports 0 iterations
with the shipped `.initials` and 0 iterations without them. The `.initials`
file is the EES stored solution (15 names). `Q_dot_capté_nov` and
`Q_dot_capté_dec` are absent from that stored solution.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `Q_dot_appoint_kWh_mois_nov` [kWh] | 183.01875 | 183.01875 | 0.00e+00 |
| `Q_dot_appoint_kWh_dec` [kWh] | 205.51875 | 205.51875 | 0.00e+00 |
| `Q_demande_kWh_an` [kWh] | 2865.478125 | 2865.478125 | 0.00e+00 |
| `Q_dot_demande` [W] | 327.109375 | 327.109375 | 0.00e+00 |
| `eta_nov` [-] | 0.22291218852 | 0.2229121885 | 8.97e-11 |
| `eta_dec` [-] | 0.12737839344 | 0.1273783934 | 3.14e-10 |
| `pente` [W/K] | 34.8916666667 | 34.89166667 | 9.54e-11 |

`Q_dot_capté_nov` is 72.91666666667 W and `Q_dot_capté_dec` is
41.66666666667 W. Those two names are only in CoolSolve.

Closed form of the same equations: `Q_dot_demande = 327.109375` W,
November backup `183.01875` kWh, December backup `205.51875` kWh, annual
demand `2865.478125` kWh.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `MSTH051213 EXERCICE 2.EES` (EES X7.458,
15 variables), compared with `compare_solution.py` without `--ees-units`.
The tool's summary line is:

`15 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 2`

The maximum relative difference over all 15 common variables is `3.14e-10`,
on `eta_dec`. The stored value is `0.1273783934` and the solved value is
`0.12737839344` (the last stored digit). Every other common variable is
smaller: `Q_dot_appoint_nov` `1.31e-10`, `Q_dot_appoint_dec` `1.17e-10`,
`pente` `9.54e-11`, `eta_nov` `8.97e-11`, `M_dot` `6.39e-11`, `C_dot`
`3.05e-11`. `A`, `c_w`, `t_nov`, `t_dec`, `Q_dot_demande`,
`Q_dot_appoint_kWh_mois_nov`, `Q_dot_appoint_kWh_dec` and
`Q_demande_kWh_an` print `0.00e+00`.

Names only in CoolSolve: `Q_dot_capté_nov`, `Q_dot_capté_dec`. Nothing is
only in the EES reference. All 17 equations are satisfied (max residual 0).

## Source and attribution

The equation window names no person. The EES licence tag is
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege}`,
the licence holder, so the authors field stays `TBD (ULiège MSTh)`.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 12/MSTH051213 EXERCICE 2.EES`.

Candidate TM-0174. No duplicate group. Teaching exercise, MSTh repetition
TP 12, exercise 2, file date 2005-12-13 (`MSTH051213`). EES X7.458. Language
of the window: French.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `MSTH051213 EXERCICE 2.EES` (EES X7.458, plain text, 15 stored variables, no tables, no warnings). The equation window has no `$UnitSystem` line; the extractor prepended `$UnitSystem SI MASS DEG PA C J` from the stored unit settings, and that line was deleted. The window has no `$TABSTOPS` and no `$Export`. Units were already pascal, Celsius and joule, so no number was scaled. With the directive removed, CoolSolve reports the window square: 17 equations, 17 variables, largest block 1. No stored unknown was added. Comments were translated to English. `Q_dot_capté_nov` and `Q_dot_capté_dec` keep the accent. The notes `on trouve: pente=34.89`, `intersection: 350` and `intersection: 200` stay comments; 350 and 200 are not written a second time. December backup energy keeps 30 days. `t_nov` and `t_dec` stay. No diagram-state array.
- **Level**: equations 17 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one balance, not a multi-zone or discretised model → 0; no calibration, off-design, part-load or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

`t_nov` and `t_dec` do not enter the balance. The window states no unit for
`A`, for `350` or for `200`. December backup energy uses 30 days, as written.
The stored solution lists 15 names; the captured-heat rates exist only as
equations.

No CoolSolve gap. `missing_features` is empty.

## Related models

`related` is empty.
