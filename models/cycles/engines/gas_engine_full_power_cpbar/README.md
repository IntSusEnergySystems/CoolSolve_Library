# Full-power operating point of a 4-stroke gas engine (combustion products with cpbar)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0034`

Steady-state model of a 5 L four-stroke natural-gas engine at its nominal
(full-power) operating point, as an exercise of the ULiège *machines et systèmes
thermiques* course. The combustion products are not described by real-fluid
properties but by their **mean specific heat** returned by the `cpbar` routine of
the ULiège combustion library (copied from **CSL-0005**), which is the reason
this model needs the library: it computes the flame temperature and the
temperature drops in the expansion and in the cooling jacket from enthalpy
differences of ideal-gas species. Useful as a template for engine energy
balances written with `cpbar` instead of a real-gas combustion model, and as a
second, independent use of `cpbar` next to the boiler of **CSL-0006**.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air, CH4 (fuel); CO2, CO, H2O, N2, O2 (combustion products, ideal gases) |
| **Size** | 85 equations (largest block: 13) — 69 of them are the exercise itself, 16 belong to the copied `cpbar` routine |
| **Source** | ULiège MSTh repetition, TP 08, exercise 4 of 2005-11-14 (`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 08/MSTH051114 EXERCICE 4.EES`, EES X7.458); imported from the CoolSolve example `examples/internal_combustion_engine_cpbar.eescode` (CSX-026) |
| **Authors** | ULiège MSTh course (J. Lebrun, V. Lemort, S. Bertagnolio); the CoolSolve example is by S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@536d427 — verified against the stored EES solution of the original (69 variables, 3 above rtol = 0.001) |

## Problem statement

*Translated from the original file (French comments kept in the .eescode where
they document the exercise).*

A 4-stroke gas engine (5 L) runs at 500 rpm with a fuel-air ratio of 0.055 and
produces no shaft power (`W_dot_sh = 0`); its actual indicated efficiency is
0.3277, its friction torque 39.79 N·m and the cooling water (0.9 kg/s, 60 °C)
rejects the combustion heat to the environment through the jacket
(`AU_gw`) and the water circuit (`AU_wa`).

The original introduces an intake pressure loss (throttle of the carburettor):
its parametric table shows that the shaft power is cancelled by reducing the
intake pressure `p_2` to about 1.8·10⁴ Pa; `W_dot_sh = 0` can then be imposed.
Determine the operating point: air and fuel flow rates, flame temperature,
temperature of the exhaust and of the cooling water, and the power terms.

## Model

All the equations of the original are kept; nothing was added or removed.

* **States 1 to 5 (intake pressure loss).** The charge flow rate is given twice:
  by the displaced volume, `V_dot_4 = i·N_rot·ncVs`, and through the area `A_3`
  at the velocity `C_3`, `V_dot_3 = A_3·C_3`. The pressure after the throttle is
  therefore not an input: it is the pressure `P_2` that closes the isentropic path
  `s_2 = ENTROPY(Air, T_2, P_2)`, `v_3 = VOLUME(Air, s_2, P_3)`,
  `T_3 = TEMPERATURE(Air, s_2, P_3)` together with the kinetic-energy balance
  `c_p_2·(t_2 − t_3) = C_3²/2`. In the original this pressure comes from a
  parametric table; here it is solved for (it comes out at 17 945.5 Pa, i.e.
  17 945.38 Pa in the stored solution). At this point `P_3` is only ≈ 10 Pa
  below `P_2` and `t_3` 0.05 K below `t_2`: state 3 is an acceleration of the
  charge (`C_3` = 10 m/s), not a compression.
* **Combustion.** Energy balance of the reactants (air and methane brought to the
  25 °C reference) and of the products, `Q_dot_1 + … + Q_dot_5 = 0`, with
  `Q_dot_5 = M_dot_g·c_p_g_6·(t_6 − 25)`: the mean specific heat of the products
  between 25 °C and the flame temperature `t_6` is returned by
  `cpbar(m, n, f, 25, t_6)`. `Q_dot_4 = 0` (no unburned-CO loss, air excess).
* **Expansion.** `M_dot_g·c_p_g_67·(t_6 − t_7) = W_dot_sh = 0`, with `c_p_g_67`
  the mean specific heat between `t_6` and `t_7` from `cpbar`.
* **Cooling.** `cpbar` once more between `T_7` and `t_8`; the products give up
  `Q_dot_gw` to the water (ε-NTU, `AU_gw`, cross-flow formula of the original),
  which leaves the jacket at `t_w_ex_1`; the water then rejects `Q_dot_wa` to the
  environment (ε-NTU, `AU_wa`).
* **Power terms.** `W_dot_p` (throttle), `W_dot_m = 2π·N_rot·T_m` (friction),
  `W_dot_in_act = η_in_act·M_dot_f·LHV`, `eta_sh`.

| Inputs | Value | Inputs | Value |
|---|---|---|---|
| `AU_gw`, `AU_wa` | 83.8, 127.4 W/K | `A_3`, `ncVs`, `i` | 0.002072 m², 5·10⁻³ m³, 0.5 |
| `eta_in_act`, `T_m` | 0.3277, 39.79 N·m | `rpm` | 500 rpm |
| `f`, `LHV`, `m`, `n` | 0.055, 50·10⁶ J/kg, 1, 4 | `t_a`, `p` | 20 °C, 10⁵ Pa |
| `W_dot_sh` | 0 W (imposed) | `M_dot_w`, `t_w_su` | 0.9 kg/s, 60 °C |

| Outputs | CoolSolve | EES stored |
|---|---|---|
| `M_dot_a` air flow | 4.2091·10⁻³ kg/s | 4.2091·10⁻³ |
| `M_dot_f` fuel flow | 2.3150·10⁻⁴ kg/s | 2.3150·10⁻⁴ |
| `P_2` intake pressure | 17 945.5 Pa | 17 945.4 |
| `t_3` after compression | 19.9498 °C | 19.9498 |
| `t_6` flame temperature | 1961.4 °C | 1963.1 |
| `t_7` exhaust temperature | 1961.4 °C | 1963.1 |
| `t_8` products at the jacket | 60.002 °C | 60.002 |
| `t_w_ex_1` water out of the jacket | 63.019 °C | 63.019 |
| `t_w_ex` water out of the circuit | 61.589 °C | 61.589 |
| `Q_dot_gw` | 11 378.1 W | 11 378.2 |
| `Q_dot_wa` | 5389.1 W | 5389.1 |
| `W_dot_in_act` | 3793.1 W | 3793.1 |
| `W_dot_p` (throttle) | 1709.7 W | 1709.7 |
| `W_dot_m` (friction) | 2083.4 W | 2083.4 |
| `eta_sh` | 0 | ~0 |

## How to run

```bash
coolsolve ./gas_engine_full_power_cpbar.eescode      # note the ./
```

Two companion files are needed:

* `gas_engine_full_power_cpbar.initials` — guess values taken from the EES
  stored solution; the flame temperature sits inside the `cpbar` calls and the
  model does not converge from the default guesses.
* `coolsolve.conf` — `tolerance = 1E-4`. The nominal point imposes
  `W_dot_sh = 0`, so `t_7 = t_6` and `c_p_g_67` is the limit
  `hp/(T_p1 − T_p2) = (h(t_6) − h(t_7))/(t_6 − t_7)` as `t_7 → t_6`: the expansion
  equation is then satisfied identically, but the 0/0 limit cannot be resolved
  below the accuracy of the property evaluation, and the block residual stops at
  ≈ 1·10⁻⁵ W instead of 1·10⁻⁹ W. EES stores the same degenerate point
  (`t_6 = t_7 = 1963.098531 °C`).

## Results

The engine burns 4.21 g/s of air-fuel charge at 500 rpm, produces no shaft power
at this operating point (all the indicated power — 3.79 kW — leaves through the
throttle, 1.71 kW, and the friction torque, 2.08 kW), reaches a flame
temperature of ≈ 1961 °C and rejects 11.4 kW to the cooling water, of which
5.4 kW leaves to the environment (the water is 0.6 K below the jacket outlet
temperature at the entry of the water-to-environment exchanger).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the model runs on
     ideal-gas Air, so there is no thermodynamic diagram to overlay (CS-FEAT-DIAGRAM-IDEAL):
     a parametric sweep plot is expected, e.g. ![flame and exhaust temperature vs engine
     speed](figures/<name>_rpm.png) -->

## Verification

Reference: the stored solution of the EES original (`reference/ees_variables.csv`
produced by `tools/ees_extract.py` in the temporary work folder, not shipped; 69 variables, run with `W_dot_sh = 0` and
`P_2 = 17 945.38 Pa`), compared with

```bash
python3 ../CoolSolve/tools/compare_solution.py gas_engine_full_power_cpbar.sol reference/ees_variables.csv
```

which reports

```
69 common variables, 3 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 17
```

* 66 of the 69 variables agree within rtol = 0.001. The results of the exercise
  agree to ≤ 8.7·10⁻⁴ relative (`P_2`, `p_3`, `p_4`, `p_5`, `v_3`, `v_4`,
  `V_dot_3`, `t_3`, `t_8`, `Q_dot_gw`, `Q_dot_wa`, `t_w_ex_1`, `t_w_ex`,
  `W_dot_in_act`, `W_dot_p`, `W_dot_m`, `C_3`, `M_dot_a`, `Q_dot_3`, `Q_dot_5` and
  the jacket ε-NTU terms are at ≤ 6.2·10⁻⁶, checked at C-38; `Q_dot_1`, `c_p_a`
  and `c_p_2` at 4.4–4.9·10⁻⁴); the worst of them is `c_p_g_78` and the cooling
  quantities derived from it at 8.7·10⁻⁴, and `t_6 = t_7` at 8.4·10⁻⁴ (1.7 K below the EES value at 1963.1 °C): it
  follows `c_p_g_6`, the mean specific heat of the products between 25 °C and
  `t_6` (+8.6·10⁻⁴, EES vs CoolSolve ideal-gas enthalpies of the species), since
  `c_p_g_6·(t_6 − 25)` is fixed by the combustor energy balance — not an effect of
  the degenerate point `t_7 = t_6`, which only concerns `c_p_g_67`.
* The three deviations:
  * `c_f` = `CP(CH4, 20 °C)`: 2220.6 vs 2241.7 J/kg·K (0.94 %) — EES treats CH4
    as an ideal gas, CoolSolve uses the CoolProp (real-gas) heat capacity;
  * `Q_dot_2` = `M_dot_f·c_f·(25 − t_5)` = 2.570 vs 2.595 W — a 0.025 W term,
    it follows `c_f`;
  * `s_2` = 4360.94 vs 6175.19 J/kg·K — a constant offset of 1814 J/kg·K between
    the entropy reference states of the EES Air table and of CoolProp Air; every
    entropy-*difference* result (`t_3`, `v_3`, `C_3`) agrees within 1.2·10⁻⁶.
* Sanity checks: the charge mass balance `M_dot_g = M_dot_a + M_dot_f` is closed,
  the energy balance of the combustor is satisfied (residual of the model ≤
  1·10⁻⁵ W with `coolsolve.conf`), `eta_in_act` and `W_dot_in_act` are imposed and
  recovered, `t_7 ≤ t_6` and `t_8 ≈ t_w_su` as expected for a zero-power point.

## Source and attribution

* **Original model (EES, X7.458)**:
  `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 08/MSTH051114 EXERCICE 4.EES`
  (candidate **TM-0127**), MSTh repetition TP 08, exercise 4 of 2005-11-14;
  ULiège MSTh course (J. Lebrun, V. Lemort, S. Bertagnolio). The `{$ID$}` tag of
  the file names Jean Lebrun (Laboratoire de Thermodynamique, Université de
  Liège) as the licence holder. `MSTH051114EXERCICE4.EES` (TM-0131) is a
  byte-identical copy of the same exercise.
* **CoolSolve example**: `~/git/CoolSolve/examples/internal_combustion_engine_cpbar.eescode`
  (CSX-026), by S. Quoilin (ULiège Thermodynamics Laboratory) — it stays in the
  CoolSolve repository; this library model is its curated version.
* **`cpbar`**: `P. Ngendakumana`, *CombCmHn_SI_PNG2003_V2.LIB* (ULiège
  Thermodynamics Laboratory, 2003), shipped as **CSL-0005** and copied into this
  model as in CSL-0006 (`CS-FEAT-IMPORT`, `$INCLUDE library:…`, is not
  available yet).
* Both sources are published under the library license (MIT).

## Conversion log

* **2026-10-05 — import** (`tools/ees_extract.py`, EES X7.458): the unit system
  of the original is already `SI MASS DEG PA C J`, i.e. the CoolSolve unit
  system: **no unit conversion was needed**. 69 variables, no lookup or
  parametric table decoded; the report flags `cpbar` as an external routine that
  the file does not define.
* **2026-10-05 — `cpbar`**: the original calls the library routine in *function
  position* (`c_p_a = cpbar(m,n,0,25,T_5)`) and does not contain its code. The
  library ships it as a **five-output `PROCEDURE`** (CSL-0005), which EES calls
  with `CALL`, so the four call sites were transcribed as
  `CALL cpbar(m,n,f,T_p1,T_p2:c_p, Q_4, x, e_min, e)` — the same transcription as
  CSL-0006. Only `c_p` is used by the exercise; the other four outputs were named
  `Q_4_a`, `x_a`, `e_min_a`, `e_a` (and `…_6`, `…_67`, `…_78`) to avoid clashing
  with the exercise variables (`Q_4_67` is therefore *not* the exercise's
  `Q_dot_4`). The body of the routine is copied verbatim from CSL-0005, including
  its `UNITSYSTEM` guard and its `{…}` comments.
  *Diff with the CoolSolve example:* the example inlines a **one-output**
  `PROCEDURE cpbar` (its body still computes `Q_4`, `x`, `e_min`, `e` as unused
  local variables) and calls it in function position (CoolSolve accepts that
  form, `coolsolve -d` on the example maps `c_p_g_6 = cpbar(...)` to `t_6`).
  This library model follows CSL-0005 (multi-output, `CALL`), i.e. the version of
  the routine that actually exists in the ULiège combustion library; the
  arithmetic is identical, so the four mean specific heats (`c_p_a`,
  `c_p_g_6`, `c_p_g_67`, `c_p_g_78`) match the EES stored solution within
  0.1 %.
* **2026-10-05 — inputs**: `W_dot_sh = 0` is imposed by the original and kept.
  `P_2` is *not* added as an input: in the original, `p_2 = p_1` is a display
  string in the equation window, so `P_2` came from the parametric table, and
  the model closes the equation set by itself (`s_2` and `P_2` are the two
  unknowns of the isentropic chain). It is solved at 17 945.5 Pa against
  17 945.38 Pa in the stored solution.
* **2026-10-05 — curation**: French comments translated to English and given
  their SI unit; section titles as display strings; the other operating points of
  the original (`W_dot_sh = 90E3`, `M_dot_f = 22/3600`, `Q_dot_gw = 90E3`,
  `W_dot_m = 10E3`, `Q_dot_wa = 8E3`, `p_2 = 1.8E4`) are no longer commented-out
  equations of dead code, they are quoted once in a comment block, because the
  exercise is a single operating point (removing them changes nothing: they were
  already inactive as string literals or comments). No equation was added,
  removed or modified; `Q_dot_4 = 0` and the display string `p_2 = p_1` are kept
  as they are in the original.
* **2026-10-05 — numerics**: `.initials` = the guess column of the EES stored
  solution; `coolsolve.conf` = `tolerance = 1E-4` for the degenerate `t_6 = t_7`
  point (see *How to run*). Neither changes the physics; the baseline `.sol` is
  the solution of the shipped configuration.
* No `$UnitSystem` directive is kept, no EES GUI tag remains
  (`{$ID$…}` was removed by the extraction), no lookup table is involved.
* **Level 2** (card): the taxonomy score of the analysis is 4 (85 equations,
  largest block 13, procedures, curated guesses → level 3), lowered by one
  because 16 of the 85 equations belong to the copied `cpbar` routine and the
  exercise itself is a single operating point of explicit, mostly linear
  bookkeeping balances with no iteration and no off-design treatment.

## Limitations and CoolSolve gaps

* No gap blocks this model: the native file runs as it is in the EES original
  (with the `cpbar` calls transcribed to `CALL`, see the conversion log).
  `missing_features` is empty.
* **`cpbar` called with `CALL` (C-38 review).** The original calls `cpbar(...)`
  in function position; the library ships the five-output `PROCEDURE` of
  CSL-0005, which EES calls with `CALL` and which CoolSolve refuses in function
  position ("cannot be called as a function"). The transcription changes no
  equation and the `CALL` form is valid EES, so it is kept as the main file
  (not a `_coolsolve` variant): it is not a rewrite around a CoolSolve gap,
  because it is not established that EES accepts a multi-output `PROCEDURE` in
  function position — the 2005 exercise probably used an older one-output
  `cpbar`. The question stays in the maintainer's pending list (unverified
  suggestion `CS-GAP-PROC-MULTIOUT`, not registered); if EES turns out to accept
  the function form with the V2 procedure, the native file should be restored to
  it and the `CALL` form moved to a `_coolsolve` variant.
* The degenerate point `W_dot_sh = 0` (see `coolsolve.conf`) is a property of the
  exercise, not a CoolSolve limitation: EES stores `t_6 = t_7` exactly as well.
* The engine is not a cycle model: no thermodynamic diagram can be overlaid
  (`CS-FEAT-DIAGRAM-IDEAL`, all gases are ideal in EES), hence a sweep plot as
  figure.
* `Q_dot_wa = epsilon_wa·C_dot_w·(t_w_ex_1 − t_a)` and
  `Q_dot_wa = C_dot_w·(t_w_ex_1 − t_w_ex)` are two definitions of the same
  variable in the original (as in several other course models). They are not
  redundant — the first gives the power, the second the water exit temperature
  `t_w_ex`, which stays 1.4 K above the ambient temperature; both are kept.
* `P_2` is solved, not imposed: with another value of the exercise inputs
  (speed, throttle, conductance products) the point found is the one of the
  zero-power constraint `W_dot_sh = 0`, not a prescribed throttle setting. Sweep
  `W_dot_sh` (or use a parametric table) to obtain the other operating points
  quoted in the original.

## Related models

* **CSL-0005** `cpbar_combustion_products`: the `cpbar` routine (function
  library) copied into this model.
* **CSL-0006** `boiler_mean_specific_heat`: the same `cpbar` transcription in a
  boiler, at a different operating point.
* **CSL-0024** `single_cylinder_engine_weibe`: the crank-angle dynamic
  counterpart of this exercise (combustion with a Weibe law instead of `cpbar`,
  no cooling circuit).
* **CSL-0049** `otto_cycle_air_standard`: the air-standard Otto cycle of
  the same engine family, solved as a steady ideal-gas model (no cooling
  circuit, no combustion products).
* **CSL-0149** `gas_engine_complete_model`: the maximum-power counterpart of
  this stand-by point, from the same TP 08 exercise series (SB versions),
  with the throttle map lookup, the water circuit and two recovery exchangers.
