# Heat pump heating a room: power from COP (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0246`

A heat pump with a given coefficient of performance heats 800 kg of air.
The temperature rise is written as 32 - 20. The heat uses `c_v`, the heating
rate divides that heat by 15 minutes, and the power follows from the COP.
Teaching exercise Cengel 6-44 from the KU Leuven `thermo_kuleuven` collection.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | none |
| **Size** | 8 equations (largest block: 1) |
| **Source** | thermo_models, file `06-44.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@6c1755b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The file name and the inventory identify the problem as Cengel 6-44. The
equation window itself has no problem text. It gives a COP of 2.5, a mass
of 800 kg, specific heats `c_v = 720` and `c_p = 1000`, and a temperature
rise written as `32 - 20`. The heat is the mass times `c_v` times that
rise. The heating rate divides the heat by 15 minutes, written as
`15 * 60`. The power follows from `COP = Q_dot/W_dot`.

`c_p` is not used in another equation. It stays.

No stored unknown was added.

## Model

One explicit heat-pump calculation, as written in the equation window.
There is no fluid call and no cycle, so no diagram-state array is added.
The figure placeholder is left empty.

\[
\mathrm{COP} = 2.5, \quad m = 800, \quad c_v = 720, \quad c_p = 1000
\]

\[
\Delta T = 32 - 20, \quad \Delta Q = m\, c_v\, \Delta T
\]

\[
\dot{Q} = \Delta Q / (15 \times 60), \quad \mathrm{COP} = \dot{Q}/\dot{W}
\]

| Input | Value |
|---|---|
| `COP` | 2.5 |
| `m` | 800 kg |
| `c_v` | 720 J/kg-K |
| `c_p` | 1000 J/kg-K |
| temperatures in `DELTAT` | 32 and 20 |
| duration | 15 minutes, written as `15 * 60` |

Those assignments are already equations. The system is square without any
further assignment (8 equations, 8 variables). The diagram-window RTF is
empty. No stored unknown was added.

`DELTAT = 32 - 20` stays. It is not replaced by 12. `c_p = 1000` stays.

## How to run

```bash
coolsolve ./heat_pump_room_cop.eescode
```

CoolSolve reports 1 iteration with the shipped `.initials` and 18 iterations
without them. Seven blocks are direct assignments. `COP = Q_dot/W_dot` is
solved for `W_dot` by Newton1D: 1 iteration from the stored guess, 18 from
the default guess. Both runs converge. There is no `abs()`, so the guesses
do not select a root. The `.initials` file is the EES stored solution with
no value rescaled. There is no `coolsolve.conf` and no runnable variant.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `Q_dot` [W] | 7680 | 7680 | 0.00e+00 |
| `W_dot` [W] | 3072 | 3072 | 0.00e+00 |
| `DELTAQ` [J] | 6912000 | 6912000 | 0.00e+00 |
| `DELTAT` [K] | 12 | 12 | 0.00e+00 |

`Q_dot` is 7680 W in CoolSolve and 7680 W in the stored solution.
`W_dot` is 3072 W in both.

The closed form is `Q_dot = 800*720*12/(15*60) = 7680` W and
`W_dot = 7680/2.5 = 3072` W. Both match the stored values. `COP`, `m`,
`c_v` and `c_p` match as written.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `06-44.EES` (EES X9.920, 8 variables),
compared with `compare_solution.py` without `--ees-units`. The tool's
summary line is:

`8 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The maximum relative difference over all common variables, as printed by the
tool with every common variable listed, is **0.00e+00**, tied on all eight
(`c_p`, `c_v`, `COP`, `DELTAQ`, `DELTAT`, `m`, `Q_dot`, `W_dot`). Nothing
is above rtol 0.001.

No stored temperature is in kelvin. The comparison did not use
`--ees-units`, so no stored value was rewritten.

## Source and attribution

The equation window names nobody. The EES licence tag is the J. Lebrun
laboratory licence (University of Liège) and is not the author. The inventory
authors column names S. Quoilin for this KU Leuven course file, so the
authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/06-44.EES`.

Candidate TM-0338. No duplicate group. Teaching exercise, not an exam.
EES X9.920. The equation window has no comments. The diagram-window RTF is
empty.

## Conversion log

- **2026-10-16 — import**: `ees_extract.py` on `06-44.EES` (EES X9.920, plain text, 8 variables, no tables). Unit system `$UnitSystem SI MASS DEG KPA C J` (the extractor writes the directive from the binary unit system; it is not text in the source window). The window has no pressure variable. Every stored unit string is blank. No number was multiplied by 1000: `DELTAQ` stays 6912000 J, `Q_dot` stays 7680 W and `W_dot` stays 3072 W. `c_v = 720` and `c_p = 1000` stay in J/kg-K. `$UnitSystem` was deleted. The file contains no `$TABSTOPS` and no `$Export`. `$Export` is not a missing feature and not a variant. The licence tag was not copied. With `$UnitSystem` removed, the window is square: 8 equations, 8 variables, largest block 1. No diagram input and no stored unknown was turned into an equation. The diagram-window RTF is empty. No diagram-state array was added.
- **Decimal comma**: the inventory notes a decimal comma. The source window stores `COP = 2,5` and no other comma. `ees_extract.py` wrote `COP = 2.5`. The value is unchanged. No other number was rewritten.
- **DELTAT**: `DELTAT = 32 - 20` stays. It is not replaced by 12.
- **c_p**: `c_p = 1000` stays. It is not used in another equation. It is still an equation.
- **Level**: equations 8 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one heat pump with an explicit COP, not three coupled components and not discretised → 0; no calibration, off-design or dynamics → 0; converges from the default guess (18 iterations without `.initials`, 1 with the stored solution) and needs no `coolsolve.conf` → 0. Score 0 → level 1. No ±1 shift.

## Limitations and CoolSolve gaps

The COP, the mass, the specific heats and the two temperatures are the
numbers written in the window. The heat uses `c_v`. `c_p` is unused.
There is no fluid call and no cycle.

No CoolSolve gap is listed. There is no variant.

## Related models

None.
