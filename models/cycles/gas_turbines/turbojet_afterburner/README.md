# Turbojet with afterburner (exercise)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0295`

Station-by-station ideal-gas turbojet (ULiège MECA0002, exercise 6) with an
afterburner (post-combustion) section added behind the turbine. The component
efficiencies are polytropic, the combustor and the afterburner have given
efficiencies and pressure ratios, and the afterburner exit total temperature
`T_pc` is the parameter of the original study. The model returns the specific
thrust, the two fuel-air ratios and the specific fuel consumption, and
reproduces the study of `T_pc` on thrust and consumption.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air (ideal gas, `fluid$ = 'Air'`) |
| **Size** | 47 equations (largest block: 2) |
| **Source** | `~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R6/autres exo/THD10_R07_E6.EES` (EES X8.423) |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (see Verification) |

## Problem statement

Teaching exercise, ULiège course MECA0002. An afterburner section is proposed
behind the turbine of the turbojet of exercise 5 (`CSL-0226`). The gases leave
the afterburner at 1600 °C, the pressure losses of the section are 5 % of the
inlet pressure and its efficiency is 0.97. What do the specific thrust and the
specific fuel consumption become? Discuss also the influence of the afterburner
exit temperature on both quantities (the original file answers it with a
parametric table and a plot).

## Model

Cold-side and hot-side perfect gases with constant `C_p` and `gamma`; no
property call. The window walks the engine from the ram-inlet station 1 to the
nozzle exit station 7 with total temperatures and total pressures (the flight
speed is kept). Compressor and turbine use **polytropic** efficiencies written
with logarithms; the combustor and the afterburner have an efficiency `eta_b`,
`eta_pc` multiplying their heat input.

- Ram inlet, station 1: `T0[1] = T[1] + c_0^2/(2*C_p_c)`,
  `p0[1] = p[1]*(T0[1]/T[1])^(gamma_c/(gamma_c-1))`.
- Diffuser: `T0[2] = T0[1]`, `p0[2] = p0[1]`.
- Compressor: `p0[3] = p0[2]*pi_c`,
  `eta_c*ln(T0[3]/T0[2]) = (gamma_c-1)/gamma_c*ln(pi_c)`,
  `w_c = C_p_c*(T0[3]-T0[2])`.
- Combustor, per unit air mass flow, fuel-air ratio `f`:
  `p0[4] = p0[3]*pi_b`,
  `(1+f)*C_p_t*T0[4] = C_p_c*T0[3] + eta_b*q_b`, `q_b = PCI*f`.
- Turbine and shaft: `eta_m*w_t + w_c = 0`, `w_t = C_p_t*(T0[5]-T0[4])`,
  `eta_t*ln(p0[5]/p0[4]) = gamma_t/(gamma_t-1)*ln(T0[5]/T0[4])`.
- **Afterburner, station 6**: `T0[6] = T_pc` (imposed), `p0[6] = p0[5]*pi_pc`,
  `(1+f_pc)*C_p_t*T0[6] = C_p_t*T0[5] + eta_pc*q_pc`, `q_pc = PCI*f_pc`.
- Nozzle, station 7, complete expansion to `p[7] = p_amb`:
  `T[7]/T0[7] = (p[7]/p0[7])^((gamma_t-1)/gamma_t)`,
  `T0[7] = T[7] + c_7^2/(2*C_p_t)`.
- Specific thrust and specific fuel consumption with the total fuel-air ratio
  `f_tot = f + f_pc`: `Fs = (1+f_tot)*c_7 - c_0`, `Cs = f_tot/Fs`.

Data, as converted: `p_amb = 23e3` Pa, `T_amb = -40+273` K,
`c_0 = 800/3.6` m/s, `T0[4] = 1200+273` K, `pi_c = 12`, `pi_b = pi_pc = 0.95`
(`pi_pc`) and `0.97` (`pi_b`), `eta_c = eta_t = eta_b = eta_pc = 0.85`
(polytropic) and `0.97` (combustion), `eta_m = 0.99`,
`C_p_c = 1005` J/kg-K, `gamma_c = 1.4`, `C_p_t = 1140` J/kg-K,
`gamma_t = 1.333`, `PCI = 43.1e6` J/kg, `T_pc = 1600+273` K at the default
point. `R = 287` J/kg-K is assigned and not used in another equation. There is
no air mass-flow unknown, so the thrust result is the specific thrust.

## How to run

From this folder:

```bash
coolsolve ./turbojet_afterburner.eescode
```

`turbojet_afterburner.initials` is the EES stored solution converted to Pa and
J (temperatures kept in kelvin). With those initials the solver reports 16
iterations; without them 61 iterations and the same solution. No
`coolsolve.conf`, no variant. To sweep `T_pc` (the original parametric study),
edit `T_pc` and re-solve.

## Results

Temperatures are kelvin; specific thrust is in m/s, i.e. N per (kg/s) of air.

| Quantity | CoolSolve | EES stored (Pa, J, K) |
|---|---:|---:|
| `Fs` [m/s] | 1045.727660 | 1045.727656 |
| `Cs` [kg/(N·s)] | 4.5015e-05 | (from stored `f_tot/Fs`; not stored itself) |
| `f` [-] | 0.026975 | 0.026975 |
| `f_pc` [-] | 0.020098 | 0.020098 |
| `c_7` [m/s] | 1210.946782 | 1210.946778 |
| `T0[3]` [K] | 593.803528 | 593.803526 |
| `T0[5]` [K] | 1173.588173 | 1173.588175 |
| `p0[5]` [Pa] | 130407.218 | 130407.219 |
| `w_c` [J/kg] | 337916.19 | 337916.19 |
| `w_t` [J/kg] | −341329.48 | −341329.48 |

At the default point the afterburner fuel-air ratio `f_pc = 0.0201` is 75 % of
the main-combustor ratio `f = 0.0270`: the afterburner burns about as much
fuel again to reheat the gases from 1174 K (turbine exit, fixed by the shaft
balance) to 1873 K and accelerate them to `c_7` = 1211 m/s.

Influence of `T_pc` (CoolSolve re-run of the original parametric study, 100 K
steps; the original table sweeps 1450–1900 K in 50 K steps):

| `T_pc` [K] | 1450 | 1550 | 1650 | 1750 | 1850 | 1900 |
|---|---:|---:|---:|---:|---:|---:|
| `Fs` [m/s] | 880.3 | 920.9 | 960.5 | 999.2 | 1037.1 | 1055.8 |
| `Cs` [10⁻⁵ kg/(N·s)] | 3.956 | 4.093 | 4.225 | 4.352 | 4.474 | 4.534 |

Both grow with `T_pc`: from 1450 K to 1900 K the specific thrust gains 19.9 %
and the specific consumption 14.6 % — more thrust per unit air flow, but the
extra fuel is only partly paid back by the extra momentum.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of the T_pc sweep,
     figures/turbojet_afterburner_tpc.png  + one-line caption -->

## Verification

Reference: the solution stored in `THD10_R07_E6.EES`, compared with
`compare_solution.py --ees-units` after the hand conversion of kPa and kJ.
Summary line, quoted as printed:

`45 common variables, 11 differ (rtol=0.001); only in EES: 15; only in CoolSolve: 2`

`--ees-units` scales kPa and kJ and also subtracts 273.15 from a unit of K when
the variable name starts with `T`. The model keeps temperatures in kelvin, so
the 11 printed differences (`T0[1]`, `T0[2]`, `T0[3]`, `T0[4]`, `T0[5]`,
`T0[6]`, `T0[7]`, `T[1]`, `T[7]`, `T_amb`, `T_pc`) are exactly that shift:
comparing them in kelvin they agree within 3.8e-09 (`T0[3]`). The maximum
relative difference over all common variables is 1.172318 on `T[1]` and
`T_amb` (`273.15/233`); on the other common variables the largest relative
difference is 7.607708e-09, on `p0[5]`.

Fifteen stored names are absent from the equation window and were not added:
`m`, `n`, `p[2]`, `p[3]`, `p[4]`, `p[6]`, `q_m_e`, `s[1]`, `s[2]`, `s[3]`,
`s[4]`, `T[2]`, `T[3]`, `T[4]`, `T[6]` (variable-window entries of earlier
sessions). CoolSolve also reports `Cs`, which the window computes and EES did
not store, and `fluid$`. All 47 equations are satisfied (max relative error
2.0e-16 with the initials). The stored EES values are not a `T_pc` sweep: the
parametric table stores only the `T_pc` inputs, so the sweep above is a
CoolSolve re-run, not a table comparison.

## Niche

Nearest library models: `CSL-0226` *turbojet_component_efficiencies* (exercise
5 of the same series: same station-by-station ideal-gas walk, but isentropic
efficiencies, no afterburner, `pi_c = 20`, `p_amb = 22` kPa) and `CSL-0051`
*turbojet_ideal_260ms* (ideal turbojet, no efficiencies, other flight point).
No library model has an afterburner/reheat section behind the turbine. This
model adds that topology (second combustion with its own fuel ratio entering
thrust and consumption through `f_tot`), polytropic instead of isentropic
component efficiencies, a combustion efficiency in the energy balances, and
the `T_pc` parametric study of thrust and consumption.

## Source and attribution

The equation window names no author. The author recorded for this ULiège
MECA0002 exercise series is S. Quoilin. Language of the source: French.
License: MIT.

Source file: `~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R6/autres exo/THD10_R07_E6.EES`
(candidate TM-0437, EES X8.423). The source file is not in the library.

## Conversion log

- **2026-10-24 — import**: Extracted with `tools/ees_extract.py` (EES X8.423,
  decimal commas converted to dots by the tool). Deleted
  `$UnitSystem SI MASS DEG KPA C KJ`; removed the `{$ID$}` licence tag.
  Comments translated to English.
- **2026-10-24 — units**: `p_amb = 23` kPa → `23e3` Pa. `C_p_c = 1.005`
  kJ/kg-K → `1005` J/kg-K. `C_p_t = 1.140` kJ/kg-K → `1140` J/kg-K.
  `R = 0.287` kJ/kg-K → `287` J/kg-K. `PCI = 43.1e3` kJ/kg → `43.1e6` J/kg.
  The two kinetic terms `c^2/2000/C_p` became `c^2/(2*C_p)` so that the
  temperature rise is unchanged once `C_p` is in J/kg-K. `T_amb = -40+273`,
  `T0[4] = 1200+273` and `T_pc = 1600+273` are unchanged: temperatures were
  not rewritten in °C. `c_0 = 800/3.6`, the gammas and the efficiencies are
  unchanged. `fluid$ = 'Air'` is unchanged.
- **2026-10-24 — square system**: The converted window is square as extracted
  (47 equations, 47 variables, largest block 2); `pi_c = 12` is given in the
  window (in exercise 5 it was only a comment). `.initials` holds the stored
  values of the unknowns converted to Pa and J.
- **2026-10-24 — tables**: The extract reports `table1` (2303×2, columns `v`,
  `T_pc`). Only 12 rows carry a `T_pc` value (1450:50:1900 K): that is the
  original study; the `v` column is mis-decoded garbage (`inf`, `1`, `-inf`,
  `3.2e51`) and no result column is stored. The table was not shipped and was
  not turned into equations; the sweep is re-run from the README.
- **2026-10-24 — not added**: No `P[i]`/`h[i]`/`T[i]`/`s[i]` diagram arrays:
  air-standard model without property calls (as `CSL-0226`; CoolSolve has no
  ideal-gas diagram, `CS-FEAT-DIAGRAM-IDEAL`). The window's own `T0[i]`,
  `T[i]`, `p[i]`, `p0[i]` stay. The parametric table and the source file were
  not copied into the library.
- **Level**: equations 47 → 0; largest block 2 → 0; arrays `T0[i]`, `T[i]`,
  `p[i]`, `p0[i]` → 1; six coupled components (diffuser, compressor,
  combustor, turbine, afterburner, nozzle) → 1; no off-design, part-load,
  dynamics or calibration (the `T_pc` sweep is a parameter study, the solved
  point is design) → 0; converges with no curated-guess requirement (61
  iterations without initials, no `coolsolve.conf`) → 0. Score 2 → level 2.

## Limitations and CoolSolve gaps

Constant specific heats and a single flight point; `R` is unused. The window
has no air mass flow, so thrust and fuel flow are specific. The turbine exit
state follows from the shaft balance, so `T0[5]` does not depend on `T_pc`
(only the afterburner does). No CoolSolve gap blocks the file.

## Related models

- `CSL-0226` *turbojet_component_efficiencies*: exercise 5 of the same ULiège
  series, the same cycle without the afterburner and with isentropic component
  efficiencies.
- `CSL-0051` *turbojet_ideal_260ms*: ideal (no efficiency) turbojet of the
  same course, with propulsion efficiency.
