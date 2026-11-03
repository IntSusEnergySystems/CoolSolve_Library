# Hydroelectric plant: power from flow rate, head and turbine efficiency (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0242`

Energy balance of a hydroelectric turbine. The volume flow rate, the head,
the turbine efficiency and the density are given. The model computes the
mass flow rate, the turbine power and the loss rate. Teaching exercise
Cengel 2-123 from the KU Leuven `thermo_kuleuven` collection.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | none |
| **Size** | 11 equations (largest block: 1) |
| **Source** | thermo_models, file `02-123.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7d66c3b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The file name and the inventory identify the problem as Cengel 2-123. The
equation window itself has no problem text. It gives a volume flow rate of
100 m³/s, a head of 120 m, a turbine efficiency of 0.8 and a density of
1000 kg/m³.

The mass flow rate is the volume flow rate times the density. The specific
inlet energy is the built-in gravitational acceleration times the head. The
inlet energy flow rate is the mass flow rate times that specific energy.
The outlet specific energy and the outlet energy flow rate are zero. The
turbine power is the net energy flow rate times the efficiency. The last
equation is the energy balance, which gives the loss rate.

No stored unknown was added.

## Model

One turbine energy balance, as written in the equation window. There is no
fluid call and no cycle, so no diagram-state array is added. The figure
placeholder is left empty.

\[
\dot{M} = \dot{V}\,\rho, \quad e_{\mathrm{in}} = g\#\,\Delta h, \quad
\dot{E}_{\mathrm{in}} = \dot{M}\, e_{\mathrm{in}}
\]

\[
e_{\mathrm{out}} = 0, \quad \dot{E}_{\mathrm{out}} = 0
\]

\[
\dot{W}_t = (\dot{E}_{\mathrm{in}} - \dot{E}_{\mathrm{out}})\,\eta_t
\]

\[
\dot{W}_t + \dot{Q}_{\mathrm{losses}} = \dot{E}_{\mathrm{in}} - \dot{E}_{\mathrm{out}}
\]

| Input | Value |
|---|---|
| `V_dot` | 100 m³/s |
| `DELTAh` | 120 m |
| `eta_t` | 0.8 |
| `rho` | 1000 kg/m³ |

Those four assignments are already equations. The system is square without
any further assignment (11 equations, 11 variables). The diagram-window RTF
is empty. No stored unknown was added.

`e_in = g# * DELTAh` stays. `g#` is the built-in. `DELTAh` stays the head
in metres.

## How to run

```bash
coolsolve ./hydroelectric_head_power.eescode
```

CoolSolve reports 2 iterations with the shipped `.initials` and 19 iterations
without them. The only implicit equation is the energy balance for
`Q_dot_losses`; from the default guess that block takes 19 Newton steps and
still converges. There is no `abs()`, so the guesses do not select a root.
The `.initials` file is the EES stored solution with no value rescaled. There
is no `coolsolve.conf` and no runnable variant.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `W_dot_t` [W] | 94143840 | 94147200 | 3.57e-05 |
| `Q_dot_losses` [W] | 23535960 | 23536800 | 3.57e-05 |
| `M_dot` [kg/s] | 100000 | 100000 | 0.00e+00 |
| `e_in` [J/kg] | 1176.798 | 1176.84 | 3.57e-05 |
| `E_dot_in` [W] | 117679800 | 117684000 | 3.57e-05 |

`W_dot_t` is 94143840 W in CoolSolve and 94147200 W in the stored solution.
`Q_dot_losses` is 23535960 W against 23536800 W. `M_dot` is 100000 kg/s in
both.

CoolSolve evaluates `g#` as 9.80665 m/s², so `e_in` is 1176.798 J/kg. The
stored `e_in` is 1176.84 J/kg, which is 9.807 m/s² times the head of 120 m.
`E_dot_in`, `W_dot_t` and `Q_dot_losses` scale with that constant. `V_dot`,
`DELTAh`, `eta_t`, `rho`, `e_out` and `E_dot_out` match.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `02-123.EES` (EES X9.920, 11 variables),
compared with `compare_solution.py` without `--ees-units`. The tool's
summary line is:

`11 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1`

The one name only in CoolSolve is `g#`, the built-in constant in
`e_in = g# * DELTAh`. It is written into the solution. It is not an extra
unknown: the statistics are 11 equations and 11 variables, and the system
is square.

The maximum relative difference over all common variables, as printed by the
tool with every common variable listed, is **3.57e-05**, tied on `E_dot_in`,
`W_dot_t` and `Q_dot_losses` (unrounded 3.568879371877231e-05). `e_in`
prints 3.57e-05 as well (unrounded 3.5688793718701205e-05). Nothing is
above rtol 0.001.

No stored temperature is in kelvin. The comparison did not use
`--ees-units`, so no stored temperature was rewritten to °C.

## Source and attribution

The equation window names nobody. The EES licence tag is the J. Lebrun
laboratory licence (University of Liège) and is not the author. The inventory
authors column names S. Quoilin for this KU Leuven course file, so the
authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/02-123.EES`.

Candidate TM-0330. No duplicate group. Teaching exercise, not an exam.
EES X9.920. The equation window has no comments. The diagram-window RTF is
empty.

## Conversion log

- **2026-10-16 — import**: `ees_extract.py` on `02-123.EES` (EES X9.920, plain text, 11 variables, no tables). Unit system `$UnitSystem SI MASS DEG KPA C J`. The window has no pressure variable. Every stored unit is blank. No number was multiplied by 1000: `V_dot = 100`, `DELTAh = 120`, `eta_t = 0.8` and `rho = 1000` stay. Energy is in joules in this unit system, so the power values stay in watts. `$UnitSystem` was deleted. The file contains no `$TABSTOPS` and no `$Export`. `$Export` is not a missing feature and not a variant. The licence tag was not copied. With `$UnitSystem` removed, the window is square: 11 equations, 11 variables, largest block 1. No diagram input and no stored unknown was turned into an equation. The diagram-window RTF is empty. No diagram-state array was added.
- **g#**: `e_in = g# * DELTAh` stays. `g#` is the built-in and was not replaced by 9.81. CoolSolve uses 9.80665 m/s². The stored specific energy 1176.84 J/kg is 9.807 m/s² times 120 m.
- **DELTAh**: the name stays. It is the head in metres.
- **Level**: equations 11 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one turbine balance, not discretised → 0; no calibration, off-design or dynamics → 0; converges from the default guess (19 iterations without `.initials`, 2 with the stored solution) and needs no `coolsolve.conf` → 0. Score 0 → level 1. No ±1 shift.

## Limitations and CoolSolve gaps

The head, the flow rate, the efficiency and the density are the numbers
written in the window. `g#` is the CoolSolve built-in, 9.80665 m/s², and the
stored solution follows 9.807 m/s². The turbine power and the loss rate
differ from the stored values by the relative amount 3.57e-05, inside
rtol 0.001.

No CoolSolve gap is listed. There is no variant.

## Related models

None.
