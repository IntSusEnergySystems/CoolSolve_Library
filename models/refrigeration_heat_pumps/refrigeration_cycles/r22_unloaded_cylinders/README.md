# R22 refrigeration machine with unloaded cylinders (exercise)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0222`

An R22 reciprocating compressor is solved twice: at full swept volume
(4 cylinders) and at half swept volume (2 cylinders). Losses reheat the
suction gas before an adiabatic compression. The evaporator and the
condenser are effectiveness-NTU exchangers on water. A weight `theta`
mixes the reduced-displacement water outlet with the idle outlet so that
the mixed evaporator exit is 14 °C. The model returns the cooling
capacity, the compressor power and the COP of each regime, and the
weighted power `W_dot_set`.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R22; water with a constant specific heat of 4187 J/kg·K |
| **Size** | 117 equations (largest block: 30): 101 for the model, 16 for the diagram state points |
| **Source** | ULiège, *Machines et systèmes thermiques*, répétition TP 10, exercice 2 (file `MSTH_041123_exercice_2.EES`) |
| **Authors** | TBD (ULiège MSTh) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified (see verification field) |

## Problem statement

The equation window is headed "MSTH041123 exercice 2" and does not contain
a separate statement. It sets up one machine at two displacements.

- Full load uses the swept volume flow `V_dot_s`. The comment on
  `V_dot_s_r = V_dot_s/2` says full load on 4 cylinders and reduced
  displacement on 2 cylinders.
- Reduced displacement uses half the swept volume and adds a given pumping
  power inside the compressor loss expression, as written.
- Both regimes use the same evaporator and condenser conductances, the same
  water flow rates, 5 K of superheat and 3 K of subcooling. The water
  specific heat is the constant 4187 J/kg·K.
- The reduced-displacement regime is mixed with an idle outlet (water
  leaves at the supply temperature) so that the mixed evaporator water
  exit is 14 °C. `W_dot_set` is that weight times the reduced-displacement
  power.

The fluid in every property call is R22. No other refrigerant is named in
the equations.

## Model

Pressure drops are not in the equations (`p_su = p_ev`, `p_ex = p_cd`, and
the same with the `_r` suffix). Saturation pressures use `x = 1`.

The evaporator and the condenser are semi-isothermal effectiveness-NTU
exchangers. The effectiveness is computed once, from the water capacity
rate, and used for both regimes:

\[
\varepsilon = 1 - \exp(-\mathrm{NTU}), \quad \mathrm{NTU} = AU/\dot C_w, \quad \dot C_w = \dot m_w\, c_w
\]

\[
\dot Q_{ev} = \varepsilon_{ev}\,\dot C_{w,ev}\,(t_{w,su,ev} - t_{ev}) = \dot C_{w,ev}\,(t_{w,su,ev} - t_{w,ex,ev})
\]

and likewise at the condenser, \(\dot Q_{cd} = \varepsilon_{cd}\,\dot C_{w,cd}\,(t_{cd} - t_{w,su,cd})\).
The reduced-displacement regime reuses `epsilon_ev` and `epsilon_cd`.

The compressor, as stated in the original hypothesis: all losses take
place before compression, and the compression itself is adiabatic.

- Volumetric efficiency \(\varepsilon_{v,1} = 1 - C\,(r_v - 1)\), with
  \(r_v = v_{su,1}/v_{ex,1}\) taken on the reheated suction state.
- Mass flow \(\dot m = \varepsilon_{v,1}\,\dot V_s/v_{su,1}\).
- Isentropic specific work from that reheated state,
  \(w_{s,1} = h_{exs,1} - h_{su,1}\).
- Full-load power \(\dot W = \dot W_{loss} + (1+\alpha)\,\dot W_s\).
- Reduced-displacement power, as written,
  \(\dot W_r = \dot W_{loss} + (1+\alpha)\,(\dot W_{s,r} + 0.5\,\dot W_{pumping})\),
  with \(\dot V_{s,r} = \dot V_s/2\).
- The suction reheat is
  \(h_{su,1} - h_{su} = (\dot W - \dot W_s)/\dot m\), and
  \(h_{ex,1} = h_{exs,1}\).

A second isentropic work, \(w_s = h_{exs} - h_{su}\), is taken from the
evaporator-outlet entropy `s_su` (before the reheat). It is used only in
`epsilon_s = w_s/w` at full load. The reduced-displacement regime does not
compute that efficiency. Expansion is isenthalpic (`h_su_ev = h_ex_cd`).

The setpoint equations are both kept:

\[
t_{w,ex,ev,set} = \theta\, t_{w,ex,ev,ON} + (1-\theta)\, t_{w,ex,ev,OFF} = 14
\]

with `t_w_ex_ev_ON = t_w_ex_ev_r` and `t_w_ex_ev_OFF = t_w_su_ev`. The
full-load water exit is a result and is not in this mixture. Commented
assignments such as `t_w_ex_ev_r = t_w_ex_ev` stay comments.

| Inputs | Value | Outputs | Full load | Half displacement |
|---|---|---|---|---|
| `V_dot_s` | 0.0233 m³/s | `Q_dot_ev` | 56.436 kW | 35.367 kW |
| `C` | 0.125 | `W_dot` | 17.062 kW | 10.212 kW |
| `alpha` | 0.228 | `COP` | 3.308 | 3.463 |
| `W_dot_loss` | 1294 W | `M_dot` | 0.3731 kg/s | 0.2240 kg/s |
| `W_dot_pumping` | 1513 W | `t_ev` / `t_cd` | 3.81 / 49.93 °C | 7.99 / 46.16 °C |
| `AU_ev` / `AU_cd` | 7000 / 15000 W/K | `p_ev` / `p_cd` | 5.626 / 19.39 bar | 6.406 / 17.77 bar |
| `M_dot_w_ev` / `M_dot_w_cd` | 2.4 / 2.2 kg/s | `t_w_ex_ev` | 9.38 °C | 11.48 °C |
| `t_w_su_ev` / `t_w_su_cd` | 15 / 40 °C | `epsilon_vol_1` | 0.7421 | 0.8106 |
| `DELTAt_oh` / `DELTAt_sc` | 5 / 3 K | `theta` | — | 0.2841 |
| `t_w_ex_ev_set` | 14 °C | `W_dot_set` | — | 2.901 kW |

`theta` and `W_dot_set` belong to the reduced-displacement mixture, not to
the full-load point. `epsilon_s` at full load is 0.6963.

## How to run

Open `r22_unloaded_cylinders.eescode` in the CoolSolve GUI, or from this
folder:

```bash
coolsolve ./r22_unloaded_cylinders.eescode
```

The shipped `.initials` are the solution stored in the EES file. With them
the solve converges in 12 iterations. Without them the block of 30
equations stops with `LineSearchFailed` at iteration 10. There is no
`coolsolve.conf`.

## Results

CoolSolve values, with the stored EES values beside them. Powers and
capacities are in W.

| | Full load, EES | Full load, CoolSolve | Half displacement, EES | Half displacement, CoolSolve |
|---|---:|---:|---:|---:|
| Cooling capacity | 56403.6 | 56435.6 | 35349.0 | 35367.4 |
| Compressor power | 17060.6 | 17062.4 | 10211.5 | 10211.6 |
| COP | 3.30608 | 3.30761 | 3.46168 | 3.46344 |
| Evaporation temperature [°C] | 3.813 | 3.806 | 7.989 | 7.985 |
| Condensation temperature [°C] | 49.923 | 49.927 | 46.154 | 46.156 |

`theta` is 0.284274 in the stored solution and 0.284126 in CoolSolve.
`W_dot_set` is 2902.87 W and 2901.39 W.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/r22_unloaded_cylinders_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `MSTH_041123_exercice_2.EES` (EES X7.210,
101 variables), compared with `compare_solution.py` without `--ees-units`.

```
101 common variables, 3 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 16
```

The maximum relative difference over the common variables is 1.66e-03 on
`t_ev`. The other two above `rtol = 0.001` are `t_su_1` (1.51e-03) and
`v_ex_1` (1.04e-03). The 16 names present only in CoolSolve are the diagram
arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1…4).

R22 does not carry the R134a reference offset (about +148144 J/kg and
+795.61 J/kg·K). On the stored enthalpies, CoolSolve minus EES is about
+8 to +50 J/kg for the vapour states and about −159 J/kg at the condenser
outlet (`h_ex_cd` −158.9 J/kg, `h_ex_cd_r` −156.8 J/kg). On the stored
entropies the difference is about +0.038 to +0.101 J/kg·K. The residual
depends on the state. It is not one constant.

Those residuals largely cancel in the compressor power, which is a
difference of vapour enthalpies plus the given loss terms: relative
difference 1.03e-04 at full load (1.76 W) and 1.06e-05 at half displacement
(0.11 W). They do not cancel in the cooling capacity, which subtracts the
condenser-outlet enthalpy from the evaporator-outlet enthalpy, so the
liquid and vapour residuals add: relative difference 5.65e-04 (31.9 W) and
5.20e-04 (18.4 W). The COP follows the capacity residual: 4.62e-04 and
5.09e-04. All three stay inside `rtol = 0.001`. The property residual is
accepted: the equations are satisfied, and the diagram block does not move
the 101 stored variables (maximum absolute change 0 against the solve
without that block).

## Source and attribution

The equation window is headed "MSTH041123 exercice 2" and names no person.
The EES licence tag is `{$ID$ #202: Laboratoire de Thermodynamique, U. de Liege}`,
which is the laboratory licence, not an author. Authors: TBD (ULiège MSTh).

Source file: `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 10/MSTH_041123_exercice_2.EES`
(thermo_models candidate TM-0158). EES X7.210. The source file is not in
the library.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X7.210, unit
  system `SI MASS DEG PA C J`, 101 variables, no tables, no warnings). The
  decimal comma was already converted to a dot by the extractor; those
  numbers are the ones used. `$UnitSystem` was deleted. The equation window
  has no `$TABSTOPS` and no `$Export`. Comments were translated into
  English. The fluid stays R22.
- **2026-10-15 — units**: already SI (Pa, °C, J). No input, equation or
  guess was rescaled. `compare_solution.py` was run without `--ees-units`.
- **2026-10-15 — square system**: the extraction with only `$UnitSystem`
  removed is square: 101 equations, 101 variables, `System square: Yes`.
  CoolSolve treats `p_`/`P_` and `t_`/`T_` as the same variables, so the
  two spellings were not unified. Property calls stay in the original
  capitals (`VOLUME`, `PRESSURE`, `ENTHALPY`, `ENTROPY`, `TEMPERATURE`);
  they are accepted. The comment glued to `V_dot_s_r = V_dot_s/2` parsed,
  and the equation is unchanged.
- **2026-10-15 — comments kept**: `t_w_ex_ev_set = 14` and the mixture with
  `theta` are both equations. Quoted lines such as `t_w_ex_ev_r=t_w_ex_ev`,
  the provisional values and `!changement de donnée!` stay comments. A
  quoted paste headed "Solution:" (rounded figures, COP 3.343,
  `Q_dot_ev` 57586 W) is an earlier display, not the stored variable
  solution, and was not kept. The cylinder split and the 14 °C setpoint
  were not changed.
- **2026-10-15 — diagram states**: `P[i]`, `h[i]`, `T[i]`, `s[i]` for the
  four full-load refrigerant states the window already computes (suction at
  the evaporator outlet, compressor exhaust, condenser outlet, evaporator
  inlet). The exhaust entropy is `s_su_1` because `h_ex_1 = h_exs_1`.
  `s[3]`, `T[4]` and `s[4]` are property calls on states the window already
  fixes. No second array set for the reduced-displacement regime. The 101
  stored variables are unchanged.
- **2026-10-15 — guesses**: `.initials` is the stored EES solution. Without
  it the block of 30 fails at iteration 10 (`LineSearchFailed`); with it
  the solve takes 12 iterations.
- **Level**: equations 117 → 1; largest block 30 → 1; diagram arrays → 1;
  two regimes of one machine, not three coupled components and not
  multi-zone → 0; part-load (half displacement and the weight `theta`) → 1;
  stored initials required → 1. Score 5, which would be level 3, shifted by
  −1 to level 2: the file is an MSTh repetition exercise on a single
  machine, not a design or research model.

## Limitations and CoolSolve gaps

The water specific heat is the constant 4187 J/kg·K. Both exchangers are
semi-isothermal: one effectiveness, no zones, no pressure drop. The
clearance, the loss factor, the constant loss and the pumping power are
given. The factor 0.5 on `W_dot_pumping` is as written in the original.
The two regimes share `epsilon_ev` and `epsilon_cd`. The full-load water
exit is not part of the 14 °C mixture. No CoolSolve gap blocks the file.
`$Export` is absent; it is not a missing feature.

## Related models

None.
