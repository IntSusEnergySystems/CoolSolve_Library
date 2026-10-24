# Identified full-load point of a 5 L four-stroke gas engine

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0272`

Steady-state model of the 5 L four-stroke natural-gas engine of the ULiège MSTh
course at its maximum-power point (2400 rpm, about 90 kW on the shaft),
*recomputed from the engine characteristics identified in exercise 1*: total
valve area, jacket and water-to-environment conductance products, indicated
efficiency and friction torque. The fuel flow, the shaft power and all state
temperatures are outputs (second part of exercise 2). The native file is
blocked by the missing `cpbar` user-library routine (`CS-GAP-INCLUDE`); the
runnable variant uses the same equations with the `CALL` form of `cpbar`.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas, intake and products in the valve/cylinder), CH4 (ideal gas, fuel cp), constant `cp` for liquid water |
| **Size** | 89 equations (largest block: 14) |
| **Source** | `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 08/SB/MSTh - R8 - Ex 2 SB.EES` (TM-0133) |
| **Authors** | ULiège MSTh course (J. Lebrun, V. Lemort, S. Bertagnolio) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — native file blocked by `CS-GAP-INCLUDE`, variant verified |

## Problem statement

Exercise 2 of the ULiège MSTh repetition TP 08 (solution by S. Bertagnolio,
01/12/05). A 5 L four-stroke gas engine is known at its maximum-power point:
fuel/air ratio 0.055, ambient 20 °C and 1 bar, 2400 rpm, 90 kW at the shaft,
cooling water 0.9 kg/s entering at 60 °C, fuel 22 kg/h with LHV 50 MJ/kg,
90 kW carried away by the jacket water, 10 kW of mechanical losses and 8 kW of
losses to the environment. Exercise 1 identifies the engine characteristics
from these data; the file imported here (part 2) *recomputes the nominal point
from the identified characteristics* — valve area 0.002072 m², `AU_gw` 83.8 W/K,
`AU_amb` 127.4 W/K, indicated efficiency 0.3277, friction torque 39.79 N·m —
and thereby checks the identification.

## Model

Charge path: no throttling at full load (`DELTAP_throttling = 0`), air and
fuel mixed at ambient temperature, then an isentropic path to the valve throat
pressure with the total-enthalpy balance `cp_23*(T_2-T_3) = C_3^2/2` and the
geometric relation `V_dot_3 = A_f_soupapes*C_3`; the cylinder inlet pressure is
the throat pressure (isobaric exit) and the charge flow is fixed by the swept
volume flow `V_dot_s = i*N*ncV_s`.

Combustion: adiabatic chamber, reactants brought to the reference temperature
25 °C in two fictitious exchangers, complete combustion (`Q_dot_4 = 0`), the
products' mean specific heat given by the `cpbar` routine of the ULiège
combustion library (`CombCmHn_SI_PNG2003_V2.LIB`, CmHn = CH4, simplified air).
The flame temperature `T_6` follows from the chamber energy balance.

Converter and cooling: `W_dot_sh = M_dot_g*cp_g_67*(T_6-T_7)`, the shaft power
being an output; the indicated work adds the friction power `W_dot_m = 2*pi*N*T_m`
and the pumping power `V_dot_4*(P_1-P_4)`, and `eta_in = W_dot_in/(M_dot_f*LHV_f)`
is the identified indicated efficiency. The jacket is an eps-NTU gas-water
exchanger (`AU_gw`), the environment losses a semi-isothermal water-air exchanger
(`AU_amb`, constant air temperature); both water outlets are computed.

Inputs: `AU_amb`, `AU_gw`, `A_f_soupapes`, `eta_in`, `T_m` (identified),
`i`, `ncV_s`, `f`, `T_a_su`, `P_a_su`, `rpm`, `M_dot_w`, `T_w_su`, `LHV_f`.
Outputs: `W_dot_sh`, `M_dot_f`, `T_6`, `T_7`, `T_8`, `Q_dot_gw`, `Q_dot_amb`,
`eta_sh`, `T_w_ex_1`, `T_w_ex`, `C_3`, `P_3`.

## How to run

```
coolsolve ./gas_engine_identified_nominal_point_coolsolve.eescode
```

The native file `gas_engine_identified_nominal_point.eescode` keeps the
function-position `cpbar` calls of the original and stops at the
`CS-GAP-INCLUDE` error quoted below; the variant
`gas_engine_identified_nominal_point_coolsolve.eescode` differs only by the
three `CALL cpbar(...)` statements (valid EES, the routine is the same
five-output `PROCEDURE` copied from `CSL-0005`). Both files ship the
`.initials` of the EES solution (the variant needs them for a clean start) and
the variant has a `.sol` baseline, tested as `CSL-0272:coolsolve`.

## Results

Variant, default operating point (the identification recovered):

| Quantity | Value | Exercise datum |
|---|---:|---:|
| Shaft power `W_dot_sh` | 90.03 kW | 90 kW |
| Fuel flow `M_dot_f` | 0.0061131 kg/s = 22.01 kg/h | 22 kg/h |
| Fuel power `M_dot_f*LHV_f` | 305.7 kW | — |
| Indicated power `W_dot_in` | 100.2 kW | — |
| Friction power `W_dot_m` | 10.00 kW (`2*pi*N*T_m`) | 10 kW |
| Pumping power `W_dot_pumping` | 136 W | — |
| Jacket heat `Q_dot_gw` | 90.01 kW | 90 kW |
| Heat to the environment `Q_dot_amb` | 8.00 kW | 8 kW |
| Flame / exhaust / jacket-out gas `T_6`, `T_7`, `T_8` | 1961.5 / 1440.7 / 893.6 °C | — |
| Water out of the jacket / of the engine `T_w_ex_1`, `T_w_ex` | 83.88 / 81.76 °C | — |
| Valve throat: `P_3`, `C_3`, `T_3` | 98637 Pa, 48.07 m/s, 18.85 °C | — |
| Shaft efficiency `eta_sh` | 0.2945 | — |

<!-- FIGURE (maintainer): parametric sweep or diagram of the engine point, docs/model_workflow.md §7 -->

## Verification

The native file does not run (blocked by `CS-GAP-INCLUDE`); the numbers above
are those of the variant, checked against two EES stored solutions with
`tools/compare_solution.py` (tolerance as printed, `rtol=0.001`):

1. **TM-0133 (the imported file)** — `31 common variables, 0 differ (rtol=0.001);
   only in EES: 0; only in CoolSolve: 59`. The 31 stored values are the
   constants of the file (identifications, data); EES never solved this file in
   its part-2 configuration (see *Conversion log*), so no EES value of the
   outputs exists.
2. **TM-0132, `MSTh - R8 - Ex 1 SB.EES`** (exercise 1, the same engine point
   with the measured inputs imposed) — `72 common variables, 11 differ
   (rtol=0.001); only in EES: 0; only in CoolSolve: 18`. Largest `s_2`
   (3.19e-01: a constant EES-vs-CoolProp entropy reference offset of
   1814.9 J/(kg·K)), then `cp_f` 9.41e-03 and `Q_dot_2` 9.09e-03 (ideal-gas CH4
   vs CoolProp heat capacity, the same deviation as `CSL-0034` and `CSL-0149`);
   the remaining eight (2.3e-03 … 2.6e-03: `C_dot_78`, `C_dot_min_gw`,
   `epsilon_gw`, `NTU_gw`, `omega_gw`, `cp_g_67`, `cp_g_78`,
   `W_dot_pumping`) are the rounding of the identified characteristics passed
   here as inputs (e.g. `AU_gw` 83.8 vs 83.7955 W/K, `A_f_soupapes` 0.002072 vs
   0.002072256 m², `W_dot_m` = 2·pi·N·T_m = 10000.3 W vs the 10 kW imposed in
   exercise 1). Excluding `s_2`, the largest difference is 9.41e-03.

Physics checks: the charge mass balance and the chamber energy balance are
closed, and the four nominal data of the exercise statement quoted in the
results table are reproduced within 0.04 %.

## Source and attribution

Solution by S. Bertagnolio of exercise 2 of the repetition TP 08 of the course
*Machines et systèmes thermiques* (ULiège, J. Lebrun, V. Lemort,
S. Bertagnolio), file `MSTh - R8 - Ex 2 SB.EES` (EES X7.458, French,
`$UnitSystem SI MASS DEG PA C J`, EES licence stamp of the Laboratoire de
Thermodynamique, ULiège). The `cpbar` routine comes from the ULiège user
library `CombCmHn_SI_PNG2003_V2.LIB` (P. Ngendakumana, 2003), copied as in
`CSL-0005`. Published under the library MIT licence, this being the
maintainer's laboratory collection.

## Conversion log

- **2026-10-22 — import**: extracted with `tools/ees_extract.py` (EES X7.458,
  unit system already `SI MASS DEG PA C J`: no unit conversion needed);
  `$UnitSystem` line removed; the EES solution stored in the file (31
  constants, full values only as guesses) copied to the `.initials`;
  comments translated to English, French section titles kept in structure;
  the cpbar routine copied from `CSL-0005` until `CS-FEAT-IMPORT`
  (`$INCLUDE library:cpbar_combustion_products`) exists.
- **Correction of one source error**: `"T_a_su=20 [°C]"` is commented out in
  the source. With it commented, the part-2 configuration of the file has
  **74 unknowns and 73 equations** (`coolsolve -d`: `System square: No`), the
  ambient temperature being the free parameter (the file's stored solution
  confirms it never solved in this configuration: only the 31 constants carry
  values). Uncommenting the line — the ambient temperature is data of the
  exercise statement, and the sibling `P_a_su=1E5[Pa]` was kept active — gives
  89 equations / 89 unknowns with the copied cpbar (`System square: Yes`).
  Impact: the model goes from unsolvable to solvable; no other equation of the
  original was changed, and the results reproduce the nominal data of the
  statement (90 kW, 22 kg/h, 90 kW, 8 kW).
- **Variants**: the only change of `..._coolsolve.eescode` is the three
  `cpbar` calls in `CALL` form, with the four unused outputs of the procedure
  going to new variables (`Q_4_a`/`x_a`/… , `Q_4_67`/…, `Q_4_78`/…) — the
  change forced by `CS-GAP-INCLUDE`, valid EES, variable names otherwise
  unchanged.
- **Level**: equations 89 → 0; largest block 14 → 1; a procedure (`cpbar`) → 1;
  no multi-zone/discretisation, no calibration or part-load, no special
  numerics (30 iterations from the EES guesses) → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- `CS-GAP-INCLUDE` (`missing_features`): `cpbar` is an implicit user-library
  routine of the original; the native file keeps the function-position call of
  the source and CoolSolve reports
  `Procedure cpbar has 5 outputs and cannot be called as a function (inline
  syntax requires exactly 1 output)`. The variant uses the `CALL` form.
- Physics, as in the original: ideal-gas `Air` for the charge and the
  products in the valve/cylinder, ideal-gas `CH4` for `cp_f`, constant
  `cp = 4187 J/(kg·K)` for the water, complete combustion, air and fuel at
  ambient temperature, no heat transfer in the cylinder (combustion modelled
  as an adiabatic chamber with fictitious exchangers).
- The EES reference of the outputs is the sibling identification file
  TM-0132, not this file (see *Verification*).

## Related models

- `CSL-0034` (gas_engine_full_power_cpbar): same engine family, stand-by
  (throttled) operating point of the 2005-11-14 exercise 4.
- `CSL-0149` (gas_engine_complete_model): the complete exercises 1-5 of this
  TP 08 series (including the stand-by map and the recovery exchangers), same
  blocked native/verified-variant pattern; `CSL-0272` is the part-2 nominal
  point of exercise 2 only.
- `CSL-0005` (cpbar_combustion_products): the `cpbar` routine used here.
