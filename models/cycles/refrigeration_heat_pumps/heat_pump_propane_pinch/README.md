# Propane heat pump with pinch-sized evaporator and condenser

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0133`

Vapour-compression heat pump on propane whose condenser and evaporator are sized
by an **imposed pinch point** instead of by a fixed condensing/evaporating
temperature: each exchanger is split into a superheated, a two-phase and a
subcooled zone, and its saturation pressure is the unknown closed by the
condition that the smallest temperature difference between the two streams
equals the imposed pinch. The refrigerant mass flow rate is imposed, so the two
saturation pressures `P_low` and `P_high` are the only unknowns of the cycle.
Translation of the `basic_HP` heat-pump example of the LaboThapPy library
(ULiège Thermodynamics Laboratory).

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R290 (propane), Water |
| **Size** | 83 equations (largest block: 38), incl. 16 diagram equations |
| **Source** | LaboThapPy (Apache-2.0), `labothappy/machine/examples/Heat_Pumps/fpi_HeatPump_example.py` (`basic_HP`) and `labothappy/component/heat_exchanger/hex_cstpinch.py`, commit `f03f7f47` |
| **Authors** | Basile Chaudoir, Elise Neven, Titouan Janod (ULiège Thermodynamics Laboratory; LaboThapPy contributors, see `AUTHORS.txt`) |
| **License** | MIT (translation with credits, roadmap decision D3) |
| **CoolSolve** | 0.3.0@4c80b25 — runs; verified against a re-run of the LaboThapPy example (max. rel. difference 3.0·10⁻⁵, see *Verification*) |

## Problem statement

Size and compute a heat pump that heats water entering at 60 °C (2 kg/s, 3 bar)
with the condenser and cools water entering at 20 °C (10 kg/s, 3 bar) with the
evaporator. The refrigerant is propane at a fixed mass flow rate of 0.1 kg/s;
the compressor has a constant isentropic efficiency of 0.7. Design data:
condenser pinch 3 K and subcooling 3 K, evaporator pinch 3 K and superheating
3 K, no pressure drop on either exchanger. Find the evaporating and condensing
pressures, the zone duties, the discharge state and the COP.

## Model

Four components, as in the original circuit (states numbered as in the state
arrays, §*Results*):

| Component | Original LaboThapPy class | Equations |
|---|---|---|
| Compressor | `CompressorCstEff` | $s_1 = s(P_{low}, h_1)$, $h_{2s} = h(P_{high}, s_1)$, $h_2 = h_1 + (h_{2s} − h_1)/\eta_{cp}$, $\dot W = \dot m(h_2 − h_1)$ |
| Condenser | `HexCstPinch` (`system_cond`, `DP_h = DP_c = 0`) | desuperheating $\dot Q_{sh} = \dot m(h_2 − h_g)$, condensation $\dot Q_{tp} = \dot m(h_g − h_f)$, subcooling to $T_3 = T_{sat} − \Delta T_{sc}$; the water is heated zone by zone from $(T,P)$ |
| Valve | `ValveIsenthalpic` | $h_4 = h_3$, then $(P_{low}, h_4)$ |
| Evaporator | `HexCstPinch` (`system_evap`, `DP = 0`) | evaporation $\dot Q_{tp} = \dot m(h_g − h_4)$, superheating to $T_1 = T_{sat} + \Delta T_{sh}$; the water is cooled zone by zone from $(T,P)$ |

Pinch closure — the three candidate temperature differences of each exchanger,
evaluated as in the original `PP_array`, and their minimum, which is set equal
to the imposed pinch (in the Python source this is a scalar root-find
`brentq` on the saturation pressure, here a simultaneous equation):

- condenser: $PP_{hot} = T_2 − T_{ex,C}$, $PP_{int} = T_{sat} − T_{C,x1}$
  (dew-point interface), $PP_{cold} = T_3 − T_{HS}$;
- evaporator: $PP_{cold} = T_{H,ex} − T_4$, $PP_{int} = T_{H,x0} − T_{sat}$
  (bubble-point interface), $PP_{hot} = T_{CS} − T_1$;
- $PPTD = \min(PP_{hot}, \min(PP_{int}, PP_{cold})) = Pinch$.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `fluid$` / `M_dot` | R290 / 0.1 kg/s | `P_low` evaporating pressure | 7.1175 bar (`T_sat_ev` = 14.00 °C) |
| `T_HS` / `M_dot_HS` / `P_HS` | 60 °C / 2 kg/s / 3 bar | `P_high` condensing pressure | 23.908 bar (`T_sat_cd` = 66.01 °C) |
| `T_CS` / `M_dot_CS` / `P_CS` | 20 °C / 10 kg/s / 3 bar | `Q_dot_cd` / `Q_dot_ev` | 29.91 kW / 21.79 kW |
| `eta_cp` | 0.7 | `W_dot` / `COP` | 8.12 kW / 3.683 |
| `PP_cd` / `SC_cd` | 3 K / 3 K | water 60 → 63.57 °C, 20 → 19.48 °C | |
| `PP_ev` / `SH_ev` | 3 K / 3 K | `x_4` evaporator inlet quality | 0.400 |

## How to run

```bash
coolsolve ./heat_pump_propane_pinch.eescode
```

**The shipped `.initials` file is required**: the 38-equation block does not
converge from default guesses (`LineSearchFailed`). The two entries are exactly
the pressure guesses of the original script — the saturation pressure of the
refrigerant at 15 °C and at 60 °C (731 512 Pa and 2 116 753 Pa) — and the model
then converges in 9 Newton iterations. There is no variant and no `coolsolve.conf`.

## Results

| Quantity | CoolSolve |
|---|---:|
| `P_low` [bar] | 7.117 47 |
| `P_high` [bar] | 23.907 7 |
| `T_sat_ev` / `T_sat_cd` [°C] | 14.000 / 66.011 |
| `T_1` / `T_2` / `T_3` / `T_4` [°C] | 17.000 / 82.898 / 63.011 / 14.000 |
| `h_1` / `h_2s` / `h_2` [J/kg] | 595 487 / 652 334 / 676 698 |
| `h_3` = `h_4` [J/kg] | 377 588 |
| `Q_dot_sh_cd` / `Q_dot_tp_cd` / `Q_dot_sc_cd` [W] | 4 711 / 24 157 / 1 042 |
| `Q_dot_tp_ev` / `Q_dot_sh_ev` / `Q_dot_sc_ev` [W] | 21 227 / 563 / 0 |
| `Q_dot_cd` / `Q_dot_ev` [W] | 29 911 / 21 790 |
| `W_dot` [W] / `COP` | 8 121 / 3.683 |
| condenser `PP_hot` / `PP_int` / `PP_cold` [K] | 19.324 / **3.000** / 3.011 |
| evaporator `PP_cold` / `PP_int` / `PP_hot` [K] | 5.479 / 5.479 / **3.000** |

Physical checks (all satisfied): the discharge state is superheated
(`T_2` = 82.9 °C > `T_sat_cd` = 66.0 °C, pressure rise 7.12 → 23.9 bar), the
condenser outlet is subcooled (`T_3` = 63.0 °C < `T_sat_cd`) and the evaporator
outlet superheated (`T_1` = 17.0 °C > `T_sat_ev` = 14.0 °C); the valve outlet is
two-phase at the evaporating pressure (`x_4` = 0.400); the imposed pinch is met
**exactly** at the dew-point interface of the condenser and at the hot end of the
evaporator, the other candidate differences being larger (3.011 K and 5.479 K);
the two energy balances close exactly — `Q_dot_cd` = `Q_dot_water_cd`,
`Q_dot_ev` = `Q_dot_water_ev` and `Q_dot_cd` = `Q_dot_ev` + `W_dot`
(21 789.88 + 8 121.10 = 29 910.98 W).

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (1 evaporator outlet = compressor
suction, 2 compressor discharge = condenser inlet, 3 condenser outlet,
4 evaporator inlet after the valve) give the cycle on the P-h or T-s diagram
(CoolSolve *Diagram* tab, *Overlay array path*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the
      propane cycle, figures/heat_pump_propane_pinch_ph.png -->

## Verification

1. **The source's own example was re-run.** `fpi_HeatPump_example.py`
   (`basic_HP`, default `study_case = "Example"`) of the LaboThapPy snapshot
   `~/git/LaboThapPy`, commit `f03f7f47`, was installed in a throw-away virtual
   environment (`pip install ~/git/LaboThapPy`, CoolProp 8.0.0, SciPy 1.18.1,
   Python 3.12). The script's `plot_cycle_Ts()` call is replaced by a dump of the
   converged component states, which prints the same line as the original:

   ```
   Converged at P_HP = 2390774.3915738715, P_LP = 711746.7848062697
   ```

   The circuit converges in 2 Wegstein iterations with a 1·10⁻³ tolerance on the
   residual variables (`P_high`, `P_low`, `h`).
2. **Comparison.** The 54 state, duty, pinch and performance variables of the
   converged circuit (written as a `name,value,units` CSV) were compared with the
   CoolSolve solution by
   `python3 ~/git/CoolSolve/tools/compare_solution.py heat_pump_propane_pinch.sol reference_python.csv --ees-units`
   (the `units` column carries K for the temperatures, converted with
   `--ees-units`): **54 common variables, 0 differ (rtol = 1e-3)**. Run with
   `--rtol 1e-9` to list them, the **maximum relative difference is 2.97·10⁻⁵**,
   on `T_1` (16.9995 °C in the reference against exactly 17.0000 °C here).

   | Quantity | LaboThapPy | CoolSolve | rel. diff |
   |---|---:|---:|---:|
   | `P_low` [Pa] | 711 746.785 | 711 746.749 | 5.0·10⁻⁸ |
   | `P_high` [Pa] | 2 390 774.392 | 2 390 774.305 | 3.6·10⁻⁸ |
   | `T_sat_ev` [°C] | 14.0000 | 14.0000 | 1.3·10⁻⁷ |
   | `T_sat_cd` [°C] | 66.0106 | 66.0106 | 2.7·10⁻⁸ |
   | `Q_dot_cd` [W] | 29 910.86 | 29 910.98 | 3.9·10⁻⁶ |
   | `Q_dot_ev` [W] | 21 789.89 | 21 789.88 | 4.4·10⁻⁷ |
   | `W_dot` [W] | 8 121.07 | 8 121.10 | 3.9·10⁻⁶ |
   | `COP` | 3.683119 | 3.683119 | 2.7·10⁻⁸ |
   | `Q_dot_sh_cd` [W] | 4 711.22 | 4 711.35 | 2.7·10⁻⁵ |
   | `PPTD_cd` / `PPTD_ev` [K] | 3.000001 / 2.999998 | 3.000000 / 3.000000 | ≤ 6.1·10⁻⁷ |

   Both sides use the same property library (CoolProp, propane HEOS), so the
   residual 10⁻⁶–10⁻⁵ differences are the convergence tolerance of the original
   itself, not a model difference: the sequential-modular solver stops when the
   pressure and enthalpy residuals are below 1·10⁻³ (relative). Its largest
   effect here is `T_1` (16.9995 °C): the compressor is closed on the suction
   connector state the loop last stored, 0.5 mK below the evaporator's own
   reported outlet (17.0000 °C = `T_sat_ev` + 3 K, its saturation temperature
   1.8·10⁻⁶ K below the one solved here). In the simultaneous system these are
   the same variable, so they come out exactly equal. The other large relative
   deviations are on *inactive* pinch candidates (`PP_hot_cd`: 19.3243 vs
   19.3238 K, a difference of 0.5 mK on a quantity six times the pinch) and on
   quantities proportional to it.
3. **Exact pinch.** The imposed pinch is an exact self-check of the translation
   (both `PPTD_cd` and `PPTD_ev` solve to 3.000000000000 K, and the two other
   candidate differences are strictly larger), so the zone interfaces of the two
   exchangers are in the right place.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the heat-pump example of LaboThapPy, files
`labothappy/machine/examples/Heat_Pumps/fpi_HeatPump_example.py` (function
`basic_HP`, the `Example` branch of `__main__`) and
`labothappy/component/heat_exchanger/hex_cstpinch.py`, commit `f03f7f47`.
LaboThapPy — https://github.com/PyLaboThap/LaboThapPy —
Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université
de Liège (ULiège), Université de Mons (UMONS). Original authors: B. Chaudoir,
E. Neven, T. Janod (see `AUTHORS.txt`).
Changes: translated from Python to CoolSolve; the circuit solver
(`CircuitFPI`, Wegstein on pressure/enthalpy residuals) and the per-component
scalar root-finds (`brentq` on the saturation pressure) are replaced by
simultaneous equations, the pressure and enthalpy links by named equations;
zone names of `system_cond`/`system_evap` (`x0`/`x1`) kept. Scientific basis:
none cited in the source beyond the constant-pinch design method of the
`HexCstPinch` component; the moving-boundary generalisation of that family is
Bell et al., Appl. Therm. Eng. 79 (2015) — see `CSL-0138`.

The second case of the same script (`basic_IHX_HP`, the cyclopentane Zorlu
geothermal plant with an internal heat exchanger) is **not** translated here: it
is the plant of `CSL-0039`, which was only used as a cross-check of the
component pattern (three zones + pinch).

Source files (not copied into the library):
`~/git/LaboThapPy/labothappy/machine/examples/Heat_Pumps/fpi_HeatPump_example.py`
(257 lines), `~/git/LaboThapPy/labothappy/component/heat_exchanger/hex_cstpinch.py`
(812 lines), `~/git/LaboThapPy/labothappy/component/compressor/compressor_csteff.py`,
`~/git/LaboThapPy/labothappy/component/valve/valve_isenthalpic.py`; reference:
URL above + those paths at commit `f03f7f47`. No student names or personal data
involved.

## Conversion log

- **2026-10-12 — translation**: `basic_HP` (Example case) transcribed
  component by component; the zone structure, the pinch candidates and their
  minimum are those of `system_cond`/`system_evap`, comments paraphrased from
  the source's own comments ("as in the original"). Temperature differences and
  duties unchanged; absolute temperatures converted from K to °C (the source
  states them in K, the offsets `T_HS` = 333.15 K and `T_CS` = 293.15 K become
  60 °C and 20 °C, `SH_ev`/`SC_cd`/`PP_*` are differences and are unchanged).
  Fluid name: the CoolProp `'Propane'` of the source becomes the EES real-fluid
  name `R290` (bare `Propane`/`R744` convention, workflow §9). The secondary
  fluid is `Water` in both exchangers, as in the example (`fluid_HS` and
  `fluid_CS` are both `'Water'`), and is written directly in the property calls
  instead of being carried as a second string variable. `DP_c`/`DP_h` = 0 (the
  example's defaults, no `DP_*` parameter is set). 16 post-processing state-array
  equations added for the diagrams (results unchanged: the solution is identical
  with and without that block).
- **2026-10-12 — inactive guards of the original dropped**: the source writes
  each zone duty as `m_dot*max(...)` or `m_dot*min(...)` to protect the wrong
  phase regimes (`Q_dot_sh = m*max(h_su − h_g, 0)`, `Q_dot_tp = m*max(min(…), 0)`,
  the `x_start = max(0, x_in)` clamp, and the subcooled-outlet fallback to
  `PropsSI`). Every one of these clamps is *inactive* at the shipped operating
  point (compressor discharge superheated: `T_2` = 82.9 °C > 66.0 °C; valve exit
  two-phase at 40 % quality, so the evaporator inlet enthalpy equals the
  two-phase start `h_4` and the subcooling zone is empty: `Q_dot_sc_ev` = 0;
  condenser outlet subcooled: `T_3` = 63.0 °C < 66.0 °C), so the plain equations
  above are exact here. They are the same simplifications as in `CSL-0014`; out
  of these regimes add the clamp explicitly.
- **2026-10-12 — curated initials**: the shipped `.initials` holds the two
  pressure guesses of the original script (`PropsSI('P','T',T_CS−5,'Q',0.5)` and
  `PropsSI('P','T',T_HS,'Q',0.5)`); the block fails from default guesses.
- **Level**: rubric score 6 (83 equations = 1, largest block 38 = 2, arrays = 1,
  multi-component cycle = 1, curated guesses = 1, no semi-empirical/off-design
  physics = 0) → level 3, lowered by one: the cycle adds only a compressor and a
  valve to the exchanger model of `CSL-0014`, the whole system is one smooth
  block that converges in 9 Newton iterations from two physical guesses, and
  there is no discretisation and no off-design case.

## Limitations and CoolSolve gaps

- **Design point only.** Constant efficiencies and imposed pinches: no
  off-design, part-load or pressure-drop case (the original has none either).
- **Pinch location near-degenerate in the condenser**: the interface pinch
  (3.000 K) and the cold-end pinch (3.0106 K) differ by 11 mK, so a perturbed
  set of inputs can switch the active branch of the `MIN` between them. The
  solution is the correct one (all other candidates are larger), but a study
  that varies the subcooling should check which candidate is active.
- **CoolProp warning during the Newton iterations**: `ENTHALPY(): t=357.441 is
  interpreted as 357.441 °C` — a transient of the first iterations (the trial
  discharge temperature); the converged states are unaffected.
- No CoolSolve gap is met by this model: `missing_features` is empty, the
  native file is valid EES and runs as it stands.

## Related models

- CSL-0134 *orc_preheated_recuperated_cyclopentane*: the same pinch design in
  an ORC on cyclopentane (adds a constant-effectiveness recuperator and
  preheater, drops the compressor and the valve).
- `CSL-0014` (*hx_constant_pinch*): the condenser branch of the same
  `HexCstPinch` component, standalone; this model is the cycle that closes both
  exchangers with the pinch condition.
- `CSL-0253` (*high_temp_heat_pump_zeotropic_transcritical*): same
  imposed-pinch heat-pump structure on imposed pressures (transcritical
  R1336mzz(Z), water capacity flow rates closed by the pinches).
- `CSL-0013` (*heat_pump_basic_tespy*): the same cycle topology (constant-η
  compressor, isenthalpic valve) on R134a from the TESPy tutorial, with fixed
  evaporating/condensing temperatures instead of imposed pinches.
- `CSL-0001` (*refrigeration_cycle_simple_compressor*): a propane refrigeration
  cycle with a semi-empirical compressor and fixed evaporation/condensation
  temperatures — the counterpart of this design model.
- `CSL-0039` (*high_temp_heat_pump_pcm_storage*): the Zorlu cyclopentane plant
  for which the same LaboThapPy script also contains a case (`basic_IHX_HP`,
  with an internal heat exchanger); not translated here, used as cross-check.
- `CSL-0250` *cascade_heat_pump_geothermal_dh*: cascade heat pump sized by imposed pinches in sectioned exchangers; uses the same MIN-of-zone-boundary-differences pinch pattern, split into an imposed boundary plus a check (see its conversion log).
- `CSL-0252` *orc_double_stage_kirchstockach*: double-stage ORC with the same pinch-designed condensers; its pinch condition is written at the binding dew-point boundary instead of a `MIN` over the zone candidates.
- `CSL-0254` *recuperated_brayton_hthp*: another 1 MW-class high-temperature heat pump design model of the same category, on an air Brayton cycle with molten-salt heat sink instead of a vapour-compression cycle on propane.
