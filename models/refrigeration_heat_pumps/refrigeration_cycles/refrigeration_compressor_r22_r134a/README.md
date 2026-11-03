# Refrigeration compressor with fixed losses, R22 and R134a (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0216`

A reciprocating refrigeration compressor with a given clearance factor and a
given loss model, evaluated at one operating point for two refrigerants.
`fluid$` is R22 and `fluid2$` is R134a. The model returns the cooling
capacity, the electrical power and the COP of each.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R22, R134a |
| **Size** | 86 equations, all explicit (largest block: 1): 54 for the model, 32 for the diagram state points |
| **Source** | ULiège, *Machines et systèmes thermiques*, répétition 1, exercice 3 (file `VL050919_1-3-1.EES`) |
| **Authors** | Vincent Lemort |
| **License** | MIT |
| **CoolSolve** | 0.3.0@62d92f0 — verified (see verification field) |

## Problem statement

A refrigeration compressor has the following characteristics:

- constant electromechanical losses: 3400 W
- loss factor: 0.30
- swept volume flow rate: 0.040 m³/s
- clearance factor: 6 %

Determine the cooling capacity, the power consumption and the COP it would
provide with R22, with R134a and with propane, under these conditions:

- evaporation temperature: 0 °C
- condensation temperature: 40 °C
- subcooling at the condenser outlet: 5 K
- superheat at the evaporator outlet: 8 K

The equation window defines `fluid$ = 'R22'` and `fluid2$ = 'R134a'` only.
Propane is named in the statement and is not an equation of this file, so it
is not added.

## Model

The two points share the compressor data and the temperatures. The second
point copies `T_cd` and `T_ev` from the first, as written. Each point is one
vapour-compression cycle with pressure drops neglected (`P_su = P_ev`,
`P_ex = P_cd`).

- saturation pressures at \(T_{ev}\) and \(T_{cd}\) (`x = 0.5`)
- supply state: \(T_{su} = T_{ev} + \Delta T_{oh}\), enthalpy, entropy and
  specific volume from \((T_{su}, P_{su})\)
- volumetric efficiency \(\varepsilon_v = 1 - C\,(r_v - 1)\) with
  \(r_v = v_{su}/v_{ex}\), where \(v_{ex}\) is the specific volume at the
  isentropic exhaust \((s_{su}, P_{ex})\)
- mass flow \(\dot m = \dot V_s\,\varepsilon_v/v_{su}\)
- isentropic specific work \(w_s = h_{ex,s} - h_{su}\), and electrical power
  \(\dot W = \dot W_{loss,0} + (1+\alpha)\,\dot m\, w_s\)
- condenser outlet at \(T_{cd} - \Delta T_{sc}\) and \(P_{cd}\); expansion is
  isenthalpic, as in the original (`h_su_ev = h_ex_cd`)
- cooling capacity \(\dot Q_{ev} = \dot m\,(h_{su} - h_{su,ev})\),
  \(COP = \dot Q_{ev}/\dot W\)

The actual compressor discharge enthalpy is not computed. Point 2 of the
diagram is the isentropic exhaust.

Braced lines in the source, `{Q_dot_ev_1=64E3` / `W_dot_1=16E3}` and
`{Q_dot_ev_2=70E3` / `W_dot_2=20E3}`, are not equations and are not used.

| Inputs | Value | Outputs | R22 | R134a |
|---|---|---|---|---|
| `W_dot_loss_0` | 3400 W | `Q_dot_ev` | 122.34 kW | 74.722 kW |
| `alpha` | 0.30 | `W_dot` | 31.095 kW | 20.145 kW |
| `V_dot_s` | 0.040 m³/s | `COP` | 3.934 | 3.709 |
| `C` | 0.06 | `M_dot` | 0.7287 kg/s | 0.4767 kg/s |
| `T_ev` / `T_cd` | 0 / 40 °C | `P_ev` | 4.980 bar | 2.928 bar |
| `DELTAT_oh` / `DELTAT_sc` | 8 / 5 K | `P_cd` | 15.336 bar | 10.166 bar |
| `fluid$` / `fluid2$` | R22 / R134a | `epsilon_v` | 0.8948 | 0.8598 |

## How to run

Open `refrigeration_compressor_r22_r134a.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./refrigeration_compressor_r22_r134a.eescode
```

The CLI loads the sibling `.initials`. The system is square and fully
explicit (largest block: 1). CoolSolve reports `Solver: SUCCESS (0 iterations)`
with that file and without it. No `coolsolve.conf`.

CoolSolve prints a hint that `T = 35` looks like Fahrenheit, because 35 is
close to 32 °F. The condenser outlet stays 35 °C. The hint does not change
the value.

## Results

CoolSolve values. The comparison with the stored EES solution is in
*Verification*.

| | R22 (`fluid$`) | R134a (`fluid2$`) |
|---|---:|---:|
| Evaporation / condensation pressure | 4.980 / 15.336 bar | 2.928 / 10.166 bar |
| Mass flow rate | 0.7287 kg/s | 0.4767 kg/s |
| Volumetric efficiency | 0.8948 | 0.8598 |
| Cooling capacity | 122.34 kW | 74.722 kW |
| Electrical power | 31.095 kW | 20.145 kW |
| COP | 3.934 | 3.709 |

`P[i]`, `h[i]`, `T[i]`, `s[i]` are the R22 states (1 evaporator outlet,
2 isentropic compressor exhaust, 3 condenser outlet, 4 evaporator inlet).
`P2[i]`, `h2[i]`, `T2[i]`, `s2[i]` are the same four states for R134a.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/refrigeration_compressor_r22_r134a_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` without `--ees-units`, against
`reference/ees_variables.csv` extracted from `VL050919_1-3-1.EES`
(EES X7.403, 52 stored variables). The stored units are already SI
(blank, `W`, `m^3/s`, or `-` on the COPs). No value was rescaled.

> 52 common variables, 5 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 34

The maximum relative difference over all common variables, as printed, is
**5.95e-01** on `h_su_ev_2`. `h_ex_cd_2` is the same number: the expansion is
isenthalpic.

The five variables above `rtol` are absolute R134a enthalpies and the supply
entropy:

| Variable | EES | CoolSolve | CoolSolve − EES | rel. diff |
|---|---:|---:|---:|---:|
| `h_su_2` | 257609.3253 J/kg | 405738.3220 J/kg | +148128.997 J/kg | 3.65e-01 |
| `h_ex_2_s` | 284629.2575 J/kg | 432758.5001 J/kg | +148129.243 J/kg | 3.42e-01 |
| `h_ex_cd_2` | 100865.8864 J/kg | 248993.4289 J/kg | +148127.543 J/kg | 5.95e-01 |
| `h_su_ev_2` | 100865.8864 J/kg | 248993.4289 J/kg | +148127.543 J/kg | 5.95e-01 |
| `s_su_2` | 957.2873545 J/kg·K | 1752.831862 J/kg·K | +795.5445 J/kg·K | 4.54e-01 |

Saturated liquid R134a at −40 °C in this binary is \(h = 148144.046\) J/kg and
\(s = 795.610\) J/kg·K. EES sets \(h = 0\) and \(s = 0\) at that state, so a
difference of this size is the reference offset. At the three stored
enthalpies the offset sits 14.8 to 16.5 J/kg below 148144.046 J/kg, and the
entropy offset sits 0.066 J/kg·K below 795.610 J/kg·K. Those small gaps are a
property difference on top of the reference. The three enthalpy offsets agree
with each other within 1.7 J/kg, so the reference cancels in a difference of
enthalpies.

R22 is not that offset. CoolSolve’s saturated liquid at −40 °C is
\(h = 154887.0\) J/kg and \(s = 822.735\) J/kg·K, and the stored solution has
no state at −40 °C to subtract. Measured on the stored states, CoolSolve − EES
is not constant:

| Variable | EES | CoolSolve | CoolSolve − EES |
|---|---:|---:|---:|
| `h_su_1` | 410899.7706 J/kg | 410917.4077 J/kg | +17.637 J/kg |
| `h_ex_1_s` | 440110.1871 J/kg | 440151.6827 J/kg | +41.496 J/kg |
| `h_ex_cd_1` | 243186.2095 J/kg | 243041.5741 J/kg | −144.635 J/kg |
| `s_su_1` | 1771.792190 J/kg·K | 1771.858969 J/kg·K | +0.0668 J/kg·K |

The enthalpy residual changes sign. It is a property difference between
EES X7.403 and CoolProp, not a second copy of the R134a reference, and not
the 154887 J/kg value at −40 °C.

COP, cooling capacity and power, reported separately from the absolute
enthalpies:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `COP_1` | 3.9334968 | 3.9342665 | 1.96e-04 |
| `Q_dot_ev_1` | 122268.3141 W | 122337.0901 W | 5.62e-04 |
| `W_dot_1` | 31083.87279 W | 31095.27261 W | 3.67e-04 |
| `COP_2` | 3.709192589 | 3.709197327 | 1.28e-06 |
| `Q_dot_ev_2` | 74721.46429 W | 74721.96510 W | 6.70e-06 |
| `W_dot_2` | 20144.94057 W | 20145.04986 W | 5.43e-06 |

On R134a the reference offset cancels: `Q_dot_ev_2`, `W_dot_2` and `COP_2`
differ only in the sixth digit. On R22 there is no constant offset to cancel.
The residuals that remain on `Q_dot_ev_1`, `W_dot_1` and `COP_1` are the
property difference above. All six are under `rtol = 0.001`.

The largest relative difference that is not an R134a absolute enthalpy or
entropy is `w_s_1` at 8.16e-04 (29210.41647 J/kg in EES, 29234.27501 J/kg in
CoolSolve), still under `rtol`. It is the same R22 enthalpy residual seen on
\(h_{ex,s} - h_{su}\).

The 34 names only in the CoolSolve solution are the diagram arrays
`P[i]`, `h[i]`, `T[i]`, `s[i]`, `P2[i]`, `h2[i]`, `T2[i]`, `s2[i]`
(i = 1…4) and the string variables `fluid$` and `fluid2$`. The equations are
satisfied (`System square: Yes`, `Solver: SUCCESS`).

## Source and attribution

The file name `VL050919` is Vincent Lemort, 2005-09-19. The equation window
names no other author. The `{$ID$}` tag is the licence of Jean Lebrun,
Laboratoire de Thermodynamique, University of Liège, not an author. Course:
*Machines et systèmes thermiques*, répétition 1, exercice 3. The comments in
the source are French. Source file:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 01/MSTH_EX1_VL050919/VL050919_1-3-1.EES`
(EES X7.403, inventory row TM-0012).

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X7.403, unit
  system `SI MASS DEG PA C J`, 52 variables, no tables, no warnings).
  `$UnitSystem` was deleted. The equation window has no `$TABSTOPS` and no
  `$Export`. Comments were translated into English. Variable names are
  unchanged. `fluid$` and `fluid2$` are kept as string variables.
- **2026-10-15 — statement versus window**: the statement asks for R22, R134a
  and propane. The window only assigns `fluid$ = 'R22'` and
  `fluid2$ = 'R134a'`. Propane was not added. The braced targets
  `Q_dot_ev_1 = 64E3`, `W_dot_1 = 16E3`, `Q_dot_ev_2 = 70E3` and
  `W_dot_2 = 20E3` stay comments.
- **2026-10-15 — units**: already SI (Pa, °C, J). No input, equation or guess
  was rescaled. `compare_solution.py` was run without `--ees-units`.
- **2026-10-15 — square system**: 54 equations before the diagram block
  (52 numeric equations and the two string assignments), 54 variables.
  CoolSolve reports the full file as 86 equations, 86 variables,
  `System square: Yes`. No Diagram-window input was restored.
- **2026-10-15 — guesses**: the extractor wrote `T_ev_1 = 1` and `T_ev_2 = 1`
  because the stored value is 0. The shipped `.initials` uses the stored
  solution, including `T_ev_1 = 0` and `T_ev_2 = 0`.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  R22 and `P2[i]`, `h2[i]`, `T2[i]`, `s2[i]` for R134a (i = 1…4). They are
  post-processing. The 52 stored variables are the comparison above.
- **Level**: equations 86 → 1; largest block 1 → 0; diagram arrays → 1; two
  parallel fluid points are not three coupled components → 0; the clearance
  and the losses are given at one point → 0; explicit, 0 iterations with and
  without guesses, no `coolsolve.conf` → 0. Score 2, shifted by −1 to level 1
  because the file is two copies of an explicit introductory exercise plus
  diagram post-processing.

## Limitations and CoolSolve gaps

The loss factor, the clearance and the swept flow are imposed. The model does
not compute the real compressor discharge state, only the isentropic exhaust
used for \(w_s\) and \(\varepsilon_v\). Pressure drops are neglected, as in
the original. Propane is not evaluated. No CoolSolve gap blocks the file.
`$Export` is absent; it is not a missing feature.

## Related models

None. `related` is empty. TM-0010, already published as CSL-0022, is a similar
compressor exercise (Jaccard 0.46) and is not grouped with this file.
TM-0013 has the same equations as TM-0012 and is not imported here.
