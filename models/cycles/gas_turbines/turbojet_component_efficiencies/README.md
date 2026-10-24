# Turbojet with component efficiencies (exercise)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0226`

Ideal-gas turbojet at one flight point. Cold-side and hot-side specific heats
and ratios of specific heats are constant. The compressor and the turbine have
given isentropic efficiencies, and the turbine work balances the compressor
work through `eta_m`. The model returns the specific thrust, the fuel-air
ratio and the specific fuel consumption.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air (ideal gas, `fluid$ = 'Air'`) |
| **Size** | 39 equations (largest block: 2) |
| **Source** | `~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R6/autres exo/THD10_R07_E5.EES` (EES X8.423) |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see Verification) |

## Problem statement

Teaching exercise, ULiège course MECA0002. The equation window walks an
ideal-gas turbojet from inlet station 1 to exit station 6 (the nozzle
equations themselves use index 7). Each component is an open system in steady
flow. Kinetic and potential energy changes are neglected except where the
window says otherwise. The flight speed is kept, so the cycle is written with
total temperatures and total pressures.

Data, as converted:

- ambient air: `p_amb = 22e3` Pa (22 kPa), `T_amb = -40+273` K, flight speed `c_0 = 800/3.6` m/s (800 km/h)
- turbine inlet total temperature `T0[4] = 1200+273` K
- compressor pressure ratio `pi_c = 20` (the window comments `pi_c = 12`; the stored solution is 20)
- combustor pressure ratio `pi_b = 0.97`
- `eta_c = 0.85`, `eta_t = 0.88`, `eta_m = 0.99`
- `C_p_c = 1005` J/kg-K, `gamma_c = 1.4` on the cold side
- `C_p_t = 1140` J/kg-K, `gamma_t = 1.333` on the hot side
- kerosene lower heating value `PCI = 43.1e6` J/kg
- `R = 287` J/kg-K is assigned and is not used in another equation
- `fluid$ = 'Air'`

There is no air mass-flow unknown, so the thrust result is the specific thrust.

## Model

Cold-side and hot-side perfect gases, constant `C_p` and `gamma`. No property
call. `c_p_c` and `C_p_c` are the same variable, as are `c_p_t` and `C_p_t`
(EES and CoolSolve match names without regard to case). The spellings of the
window are kept.

Ram inlet, station 1:

\[
T_0[1] = T[1] + \frac{c_0^2}{2\,C_{p,c}},
\qquad
p_0[1] = p[1]\left(\frac{T_0[1]}{T[1]}\right)^{\gamma_c/(\gamma_c-1)}
\]

The original writes `c_0^2/2000/C_p_c` because `C_p_c` was in kJ/kg-K.

Diffuser: `T0[2] = T0[1]` and `p0[2] = p0[1]`. Compressor:

\[
p_0[3] = p_0[2]\,\pi_c,
\qquad
\eta_c\left(\frac{T_0[3]}{T_0[2]}-1\right) = \pi_c^{(\gamma_c-1)/\gamma_c}-1,
\qquad
w_c = c_{p,c}\,(T_0[3]-T_0[2])
\]

Combustor, per unit mass of air, with fuel-air ratio `f`:

\[
p_0[4] = \pi_b\,p_0[3],
\qquad
(1+f)\,c_{p,t}\,T_0[4] = c_{p,c}\,T_0[3] + q_b,
\qquad
q_b = \mathrm{PCI}\,f
\]

Turbine and shaft:

\[
w_t\,\eta_m + w_c = 0,
\qquad
w_t = c_{p,t}\,(T_0[5]-T_0[4]),
\qquad
\eta_t\left(\pi_t^{(\gamma_t-1)/\gamma_t}-1\right) = \frac{T_0[5]}{T_0[4]}-1
\]

Nozzle, station 7, expanded to ambient pressure. The energy balance is
quadratic in the exit speed `c_7`:

\[
\frac{T[7]}{T_0[7]} = \left(\frac{p[7]}{p_0[7]}\right)^{(\gamma_t-1)/\gamma_t},
\qquad
T_0[7] = T[7] + \frac{c_7^2}{2\,C_{p,t}}
\]

Specific thrust and specific fuel consumption. The original comment writes the
momentum balance with `c_6`; the equation uses `c_7`:

\[
F_s = (1+f)\,c_7 - c_0,
\qquad
C_s = f/F_s
\]

| Quantity | Role | Value |
|---|---|---|
| `p_amb`, `T_amb`, `c_0` | flight condition | 22 kPa, 233 K, 800/3.6 m/s |
| `T0[4]` | turbine inlet total temperature | 1473 K |
| `pi_c` | compressor pressure ratio | 20 |
| `pi_b`, `eta_c`, `eta_t`, `eta_m` | component data | 0.97, 0.85, 0.88, 0.99 |
| `Fs` | specific thrust | solved [m/s] |
| `f` | fuel-air mass ratio | solved [-] |
| `Cs` | specific fuel consumption | solved [kg/(N·s)] |
| `c_7` | nozzle-exit speed | solved [m/s] |
| `w_c`, `w_t` | specific compressor and turbine work | solved [J/kg] |

The system is square: 39 equations and 39 variables, including the string
assignment `fluid$ = 'Air'`. Thirty-seven equations are explicit. The largest
block has size 2 (`q_b` and `f`). CoolSolve evaluates `c_7` in an explicit
block and returns the positive root.

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./turbojet_component_efficiencies.eescode
```

`turbojet_component_efficiencies.initials` is the EES stored solution converted
to Pa, J and kelvin, including the positive exit speed `c_7`. With those
initials the solver reports 11 iterations. Without them it reports 45
iterations and the same solution. A guess `c_7 = -994.9` still returns the
positive root (39 iterations): the explicit block does not keep the negative
square root. No `coolsolve.conf` and no variant.

## Results

Temperatures below are kelvin. Specific thrust is in m/s, which is N per
(kg/s) of air. Compressor work is positive, turbine work is negative, the
compressor pressure ratio raises `p0`, and the nozzle exit is faster than the
flight speed.

| Quantity | CoolSolve | EES stored (Pa, J, K) |
|---|---:|---:|
| `Fs` [m/s] | 796.9212817 | 796.9212856 |
| `f` [-] | 0.02433944214 | 0.02433944214 |
| `Cs` [kg/(N·s)] | 3.054183982e-05 | 3.054183968e-05 (from stored `f/Fs`; not stored itself) |
| `c_7` [m/s] | 994.9275230 | 994.9275268 |
| `w_c` [J/kg] | 412204.9639 | 412204.9639 |
| `w_t` [J/kg] | −416368.6504 | −416368.6504 |
| `q_b` [J/kg] | 1.049029956e+06 | 1.049029956e+06 |
| `pi_t` [-] | 0.2658480735 | 0.2658480735 |
| `T0[3]` [K] | 667.7227084 | 667.7227084 |
| `T[7]` [K] | 673.6061066 | 673.6061066 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `THD10_R07_E5.EES`, compared with
`compare_solution.py --ees-units`. Summary line, quoted as printed:

`37 common variables, 9 differ (rtol=0.001); only in EES: 18; only in CoolSolve: 2`

`--ees-units` scales a unit of kPa or kJ (including kJ/kg and kJ/kg-K) and also
subtracts 273.15 from a unit of K when the variable name starts with `T`. It
does not scale a blank unit or a unit such as m/s. Those unscaled common
variables agree (`c_0`, `c_7`, `Fs`, `f`, the efficiencies, the gammas, `pi_c`,
`pi_b`, `pi_t`). The nine printed differences are the temperatures kept in
kelvin. The maximum relative difference over all common variables is 1.172318
on `T[1]` and on `T_amb` (`273.15/233`). On the other common variables the
largest relative difference is 4.90e-09, on `Fs`.

There is no `enthalpy` call, so there is no ideal-gas enthalpy offset. All 39
equations are satisfied (max relative residual 3.52e-10 with the initials).

Eighteen stored names are absent from the equation window and were not added:
`c_6`, `m`, `n`, `p0[6]`, `p[2]`, `p[3]`, `p[4]`, `p[6]`, `q_m_e`, `s[1]`,
`s[2]`, `s[3]`, `s[4]`, `T0[6]`, `T[2]`, `T[3]`, `T[4]`, `T[6]`. CoolSolve
also reports `Cs`, which the window computes and the EES variable list does
not store, and `fluid$`.

## Source and attribution

The equation window names no author. The author recorded for this ULiège
MECA0002 exercise is S. Quoilin. Language of the source: French. License: MIT.

Source file: `~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R6/autres exo/THD10_R07_E5.EES`
(candidate TM-0436, EES X8.423). The source file is not in the library.

## Conversion log

- **2026-10-15 — import**: Extracted with `tools/ees_extract.py` (EES X8.423, decimal commas already converted to dots). Deleted `$UnitSystem SI MASS DEG KPA C KJ`. The window has no `$TABSTOPS` and no `$Export`. Comments translated to English.
- **2026-10-15 — units**: `p_amb = 22` kPa → `22e3` Pa. `C_p_c = 1.005` kJ/kg-K → `1005` J/kg-K. `C_p_t = 1.140` kJ/kg-K → `1140` J/kg-K. `R = 0.287` kJ/kg-K → `287` J/kg-K. `PCI = 43.1e3` kJ/kg → `43.1e6` J/kg. The two kinetic terms `c^2/2000/C_p` became `c^2/(2*C_p)` so that the temperature rise is unchanged once `C_p` is in J/kg-K. `c_0 = 800/3.6` is unchanged. `T_amb = -40+273` and `T0[4] = 1200+273` are unchanged; temperatures were not rewritten in °C. `gamma_c = 1.4` and `gamma_t = 1.333` are unchanged. `fluid$ = 'Air'` is unchanged.
- **2026-10-15 — square system**: The converted window, before any stored unknown was added, had 38 equations and 39 unknowns (System square: No). The extra unknown is `pi_c`, which the window uses and only mentions in the comment `pi_c = 12`. Added `pi_c = 20` from the stored solution. No other comment was restored. The system is then square (39 equations, largest block 2).
- **2026-10-15 — tables**: The extract reports two parametric tables, `table1` (2364 rows of `v`, `pi_c`) and `Table 1` (17 rows of `Fs`, `Cs`). The equation window does not call `INTERPOLATE` or `LOOKUP`. Those tables were not shipped and were not turned into equations.
- **2026-10-15 — not added**: No `P[i]`/`h[i]`/`T[i]`/`s[i]` diagram arrays. The window's own `T0[i]` (and `T[i]`, `p[i]`, `p0[i]`) stay. No `LowerHeatingValue` call; `PCI` stays a numeric constant. The parametric tables and the source file were not copied into the library.
- **Level**: equations 39 → 0; largest block 2 → 0; arrays `T0[i]`, `T[i]`, `p[i]`, `p0[i]` → 1; five coupled components (diffuser, compressor, combustor, turbine, nozzle) → 1; no off-design, part-load, dynamics or calibration → 0; converges with no curated-guess requirement and no `coolsolve.conf` → 0. Score 2 → level 2.

## Limitations and CoolSolve gaps

Constant specific heats and a single flight point. `R` is unused. The window
has no air mass flow, so thrust and fuel flow are specific (`Fs`, `f`, `Cs`).
The original comment numbers the nozzle as station 6; the equations use index
7. No CoolSolve gap blocks the file.

## Related models

- `CSL-0295` *turbojet_afterburner*: exercise 6 of the same ULiège series —
  this cycle with an afterburner section behind the turbine, polytropic
  component efficiencies and the study of the afterburner exit temperature.
