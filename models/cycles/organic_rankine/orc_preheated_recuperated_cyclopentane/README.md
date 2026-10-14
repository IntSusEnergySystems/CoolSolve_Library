# Preheated + recuperated ORC on cyclopentane (Zorlu geothermal site)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0134`

Organic Rankine cycle on cyclopentane for the Zorlu (Kırşehir, Turkey)
geothermal site: the evaporator and the condenser are each *sized* by an
imposed pinch point (plus superheating / subcooling) instead of by a fixed
pressure ratio, an internal heat exchanger (recuperator) and a water preheater
recover the low-grade heat of the exhaust and of the condensate, and a
constant-efficiency pump and expander complete the cycle. The two saturation
pressures are the unknowns, closed by the two pinch conditions; no pressure drop
is modelled anywhere. Translation of the LaboThapPy Zorlu ORC example
(`preheated_rec_orc`).

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | CycloPentane (working fluid), Water (three source streams) |
| **Size** | 135 equations (largest block: 61) |
| **Source** | LaboThapPy (Apache-2.0/MIT), file `labothappy/machine/examples/ORC/fpi_orc_example.py` (case `Zorlu`), with `labothappy/component/heat_exchanger/hex_cstpinch.py`, `hex_csteff.py`, `pump_csteff.py`, `expander_csteff.py`; commit `f03f7f47` |
| **Authors** | Basile Chaudoir, Elise Neven, Titouan Janod (ULiège Thermodynamics Laboratory; LaboThapPy contributors, see `AUTHORS.txt`) |
| **License** | MIT (translation with credits, roadmap decision D3) |
| **CoolSolve** | 0.3.0 — runs; verified against a re-run of the Python example (see *Verification*) |

## Problem statement

Size the Zorlu ORC of the LaboThapPy example: cyclopentane at 34.51 kg/s
between a 141 °C / 10 bar water source (10 000 kg/s, emulating a PCM store), a
113.1 °C / 2 bar preheater source (60 kg/s) and a 24 °C / 3 bar cooling water
(900 kg/s); pump and expander at constant isentropic efficiency (0.7 / 0.8),
recuperator and preheater at constant effectiveness (0.8), condenser pinch
5 K with 3 K subcooling, evaporator pinch 5 K with 3 K superheating. Find the
condensing and evaporating pressures, the zone duties, the net power and all
state points.

## Model

State points of the working fluid, numbered in the flow direction (the arrays
`P[i]`, `h[i]`, `T[i]`, `s[i]` of the end of the file):

| # | State | # | State |
|---|---|---|---|
| 1 | pump inlet = condenser outlet | 5 | evaporator outlet = expander inlet |
| 2 | pump outlet = recuperator cold inlet | 6 | expander outlet = recuperator hot inlet |
| 3 | recuperator cold outlet = preheater inlet | 7 | recuperator hot outlet = condenser inlet |
| 4 | preheater outlet = evaporator inlet | | |

**Pump and expander** (constant isentropic efficiency, as `PumpCstEff` and
`ExpanderCstEff`):

$$h_2 = h_1 + \frac{h(P_{high},\,s_1) - h_1}{\eta_{pp}},\qquad
h_6 = h_5 - \big(h_5 - h(P_{low},\,s_5)\big)\,\eta_{exp}$$

**Recuperator and preheater** (constant effectiveness, `HexCstEff`): the duty is
a fixed fraction of the smaller of the two *enthalpy-rate* limits, the ideal
enthalpies being taken at the inlet temperature of the other stream (as in the
original, not the `C_min·ΔT` form):

$$Q_{max,h} = \dot m_H\,\big|h(P_H,\,T_{su,C}) - h_{su,H}\big|,\qquad
Q_{max,c} = \dot m_C\,\big|h(P_C,\,T_{su,H}) - h_{su,C}\big|,\qquad
Q = \varepsilon\,\min(Q_{max,h},Q_{max,c})$$

**Evaporator** (`HexCstPinch`, `system_evap`), three zones in series:
subcooling from the subcooled-liquid inlet to the bubble point, evaporation
between the saturated states at $P_{high}$, superheating by `SH_ev`:

$$Q_{sc} = \dot m\,(h_f - h_4),\quad Q_{tp} = \dot m\,(h_g - h_f),\quad
Q_{sh} = \dot m\,(h_5 - h_g),\quad Q_{ev} = Q_{sc}+Q_{tp}+Q_{sh}$$

**Condenser** (`HexCstPinch`, `system_cond`): no desuperheating zone (the
recuperator delivers the fluid at the dew point), condensation down to the
bubble point, subcooling by `SC_cd`; the zone duties keep the `MIN`/`MAX`
clamps of the original, so the sum is always $\dot m\,(h_7 - h_1)$.

**Pinch closure** (the scalar `brentq` root-find on the saturation pressure of
the Python components becomes an unknown closed by the design condition):

$$PPTD_{ev} = \min\big(T_{HS}-T_5,\; T_{H,x0}-T_{sat,ev},\; T_{ex,H,ev}-T_4\big) = PP_{ev}$$
$$PPTD_{cd} = \min\big(T_7-T_{ex,C,cd},\; T_{sat,cd}-T_{C,x1,cd},\; T_1-T_{CS}\big) = PP_{cd}$$

Both `PPTD` variables are written as `MIN(...)` and then re-assigned to the
imposed pinch, exactly as in `CSL-0013`/`CSL-0014`; this is valid EES.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `M_dot` | 34.51 kg/s | `P_low` condensing pressure | 56 693 Pa (0.567 bar) |
| `T_HS` / `P_HS` / `M_dot_HS` | 141 °C / 1 MPa / 10 000 kg/s | `P_high` evaporating pressure | 849 551 Pa (8.496 bar) |
| `T_pre_su` / `P_pre_su` / `M_dot_pre_su` | 113.1 °C / 0.2 MPa / 60 kg/s | `Q_dot_ev` | 13 443 kW |
| `T_CS` / `P_CS` / `M_dot_CS` | 24 °C / 0.3 MPa / 900 kg/s | `Q_dot_cd` | 13 659 kW |
| `eta_pp` / `eta_exp` / `eff_rec` | 0.7 / 0.8 / 0.8 | `Q_dot_rec` / `Q_dot_pre` | 1 911 / 3 184 kW |
| `PP_cd` / `SC_cd` / `PP_ev` / `SH_ev` | 5 K / 3 K / 5 K / 3 K | `W_dot_exp` / `W_dot_pp` / `W_dot_net` | 3 021 / 53.1 / 2 968 kW |
| | | `eta_th` | 0.2208 |

## How to run

```bash
coolsolve ./orc_preheated_recuperated_cyclopentane.eescode
```

**The shipped `.initials` is required**: the 61-equation block does not converge
from the default guesses (`LineSearchFailed` / `SingularJacobian`). The shipped
file is the converged solution of the *simplified* model in which the two
saturation pressures are fixed inputs and the two pinch conditions are dropped
(all other equations unchanged) — the bootstrap recipe of CoolSolve
`docs/debugging_models.md` §5. With it the model converges in 8 Newton
iterations with the default solver pipeline (no `coolsolve.conf` needed).

## Results

| Quantity | CoolSolve |
|---|---|
| `T_sat_cd` / `T_sat_ev` | 32.630 °C / 133.00 °C |
| `h_1` … `h_7` [J/kg] | −36 985 / −35 446 / 19 941 / 112 214 / 501 745 / 414 206 / 358 819 |
| `T_1` … `T_7` [°C] | 29.630 / 30.123 / 59.151 / 102.93 / 136.00 / 66.06 / 32.630 |
| `x_7` (condenser inlet quality) | 0.9724 |
| `Q_dot_sc_ev` / `Q_dot_tp_ev` / `Q_dot_sh_ev` | 2 420 / 10 826 / 197 kW |
| `Q_dot_sh_cd` / `Q_dot_tp_cd` / `Q_dot_sc_cd` | 0 / 13 469 / 191 kW |
| `PP_hot_ev` / `PP_int_ev` / `PP_cold_ev` [K] | 5.00 / 7.74 / 37.8 |
| `PP_hot_cd` / `PP_int_cd` / `PP_cold_cd` [K] | 5.00 / 5.00 / 5.63 |
| `bal_1` … `bal_4` (energy-balance checks) | ≤ 1e-7 W |

Both pinch conditions are exactly satisfied (`PPTD_cd` = `PPTD_ev` = 5.000 K); in
the evaporator the active pinch is at the hot end (the superheating of 3 K
against the 141 °C source) and in the condenser at the hot end / dew-point
interface, which coincide because there is no desuperheating zone.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of
      the cycle with the recuperator, figures/orc_preheated_recuperated_cyclopentane_ph.png -->

## Verification

1. **The source's own example was re-run** in a throw-away virtual environment
   (`work/`, `pip install ~/git/LaboThapPy`, LaboThapPy commit `f03f7f47`,
   CoolProp 8.0.0, SciPy 1.18.1): `run_zorlu.py` (a copy of the `preheated_rec_orc`
   function and of the `Zorlu` main block of `fpi_orc_example.py`, without the
   plotting call) converges in 6 Wegstein iterations, `PPTD_cond` = 5.000000 and
   `PPTD_evap` = 5.000003.
2. **The preheater-source bug of the original main block was corrected and both
   cases compared** (the same script, argument `bug` / `fix`):

   | | as shipped (`bug`) | corrected (`fix`) | CoolSolve |
   |---|---:|---:|---:|
   | preheater source | 24 °C, 3 bar, 900 kg/s | 113.1 °C, 2 bar, 60 kg/s | 113.1 °C, 2 bar, 60 kg/s |
   | `Q_dot_pre` | 1 778.5 kW | 3 242.4 kW | 3 184.3 kW |
   | `Q_dot_ev` | 14 883.2 kW | 13 419.3 kW | 13 442.7 kW |
   | evaporator inlet `T_4` | 83.2 °C | 102.7 °C | 102.9 °C |
   | `P_low` / `P_high` | 56 698.8 / 849 551.1 Pa | 56 698.8 / 849 551.1 Pa | 56 693.5 / 849 551.1 Pa |
   | `W_dot_net` | 2 954.9 kW | 2 954.9 kW | 2 967.9 kW |

   In the shipped version the preheater *heats* the working fluid from 58 °C to
   83 °C while its "source" is the 24 °C cooling water, which then **cools**:
   the enthalpy-rate limit of `HexCstEff` is computed with the hot side at the
   cold inlet temperature, so the fictitious limit is large and the exchanger
   duty is unphysical (the same happens with `T_PRE`, `p_PRE`, `m_dot_PRE`
   defined in the main block but never used). Correcting it leaves the cycle
   pressures, the recuperator duty and the net power untouched (they do not
   depend on the preheater duty) and changes only the evaporator duty (−9.8 %).
3. **Model vs the corrected Python run**, `tools/compare_solution.py`
   (the reference CSV and the run scripts were written in the throw-away `work/`
   folder, deleted at the end of the card; 38 variables mapped by hand onto the
   names of the model): *"38 common variables, 17 differ (rtol=0.001); only in EES: 0; only
   in CoolSolve: 97"* — largest relative deviation **1.93e-01** on
   `Q_dot_sh_ev` (0.197 vs 0.159 MW, i.e. 0.29 % of `Q_dot_ev`). The bulk of
   the state points agrees far better: `P_low` 9.5e-05, `P_high` 1.1e-12,
   `T_sat_cd` 7.8e-05, `T_sat_ev` 1.7e-09, `W_dot_pp` 2.3e-06, `Q_dot_cd` 7.0e-04,
   `Q_dot_tp_cd` 7.1e-04, `Q_dot_tp_ev` 9.1e-09, `Q_dot_sc_cd` 6.9e-06,
   `T_ex_H_ev` 4.2e-06, `x_7` 7.1e-04, `h_1`/`h_2` 1.3e-04.

   **The deviations above 0.1 % have one cause**: the Python circuit is
   sequential-modular and its two iteration variables are pressures, so the
   states it prints are not exactly the states its own pinch residual was solved
   for. Its evaporator outlet is `h_5` = 500 644.24 J/kg at 408.5715 K, while
   its own last root evaluation used `T_C_ex` = `T_ev_x1 + SH_ev` = 409.15 K;
   the two differ by 0.5785 K. Recomputed with the same CoolProp as the Python
   run, `enthalpy(Cyclopentane, P=849551 Pa, T=409.15 K)` = **501 745.38 J/kg**,
   which is exactly the `h_5` of the model, and
   `enthalpy(Cyclopentane, P=849551 Pa, T=408.5715 K)` = **500 644.16 J/kg**,
   exactly the value stored by the Python circuit. The translation therefore
   closes the pinch *exactly* and inherits a 0.58 K (0.22 % in `h_5`)
   difference at the expander inlet, from which follow `s_5` (0.21 %),
   `h_6`/`T_6` (0.44 % / 2.0 %), `W_dot_exp`/`W_dot_net` (0.43 %), `h_3`/`T_3`
   (10.6 % / 1.06 K, the recuperator outlet), `Q_dot_rec` (3.8 %) and
   `Q_dot_pre` (−1.8 %) — all six are read from a single stale state. A run with
   `SH_ev` = 2.42 K (which moves the evaporating pressure to 8.59 bar and lowers
   the expander inlet temperature) reduces `Q_dot_rec` to 1 888 kW (+2.7 %) and
   `Q_dot_pre` to 3 202 kW (−1.2 %). The two pinch-point differences of the
   cycle (the active candidate of each exchanger) agree exactly.
4. **Cross-check with `CSL-0039`** (the Zorlu heat pump of the same site, on the
   same fluid): the site data are the same — hot water 141 °C / 10 000 kg/s
   (`T_HS`, `M_dot_HS`; `T_sf_su_cd` = 141 °C, `m_dot_sf_su_cd` = 10 000 kg/s in
   `CSL-0039`) and the geothermal brine at 113.1 °C (`T_pre_su`; `T_sf_su_pp` =
   113.1 °C in `CSL-0039`) — and the saturation properties of `CycloPentane` are
   the same CoolProp backend, so the two models can be compared state by state
   when the topology is changed.
5. **Sanity checks**: the four balance residuals `bal_1`…`bal_4` (cycle energy
   balance, condenser duty vs heat gained by the cooling water, preheater duty vs
   heat lost by its source, evaporator duty vs heat gained by the hot source) are
   ≤ 1e-7 W; the condenser's cooling water leaves 3.6 K above its inlet
   (24 → 27.6 °C) and the preheater source 12.6 K colder (113.1 → 100.5 °C), both
   below the imposed pinch.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the Zorlu ORC example of LaboThapPy, file
`labothappy/machine/examples/ORC/fpi_orc_example.py` (function
`preheated_rec_orc`, main block `study_case = "Zorlu"`), and of the components it
instantiates — `labothappy/component/heat_exchanger/hex_cstpinch.py`
(`HexCstPinch`), `hex_csteff.py` (`HexCstEff`),
`labothappy/component/pump/pump_csteff.py` (`PumpCstEff`) and
`labothappy/component/expander/expander_csteff.py` (`ExpanderCstEff`) — all at
commit `f03f7f47`. LaboThapPy — https://github.com/PyLaboThap/LaboThapPy —
Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université
de Liège (ULiège), Université de Mons (UMONS). Original authors: B. Chaudoir,
E. Neven, T. Janod (see `AUTHORS.txt`).

Changes: translated from Python to CoolSolve; the sequential-modular
`CircuitFPI` and its two pressure iteration variables replaced by simultaneous
equations closed by the pinch conditions; the scalar `brentq`/`fsolve` root
finds of `HexCstPinch` replaced by the unknown saturation pressure; the
`max(0,·)`/`min(·)` clamps of the condenser zone duties kept (they are inactive
here), the two-phase zone starts written with `MIN`/`MAX` clamps on the
qualities instead of two-phase property calls at a moving quality; the
preheater source corrected (see *Verification* 2); `T_PRE`, `p_PRE`, `m_dot_PRE`
renamed `T_pre_su`, `P_pre_su`, `M_dot_pre_su` because CoolSolve does not create
a variable whose name ends in an unquoted property-input prefix (`Q_dot_PRE` was
silently swallowed and made the system one equation short); temperatures
converted from K to °C; 28 post-processing state-array equations added for the
diagrams (results unchanged). Scientific basis: the pinch-design method of the
source itself; no paper or standard is cited in the file.

Source files (not copied into the library):
`~/git/LaboThapPy/labothappy/machine/examples/ORC/fpi_orc_example.py` and the
four component modules above; reference: the URL above + those paths + commit
`f03f7f47`. No student names or personal data involved.

## Conversion log

- **2026-10-13 — translation**: the six components (pump, recuperator,
  preheater, evaporator, expander, condenser) transcribed as simultaneous
  equations, comments paraphrased from the original's own comments or marked
  "as in the original"; the source's connector names (`su_C`, `ex_H`,
  `Q_dot_max`, `PPTD`, `x_start`, …) are kept for the exchanger quantities and
  the working-fluid states are numbered 1…7 in the flow direction (the mapping
  is in the comment block above the state definitions).
- **2026-10-13 — preheater source corrected**: the main block of the original
  builds `PREsource` from `fluid_CS, T_CS, p_CS, m_dot_CS` although
  `T_PRE`, `p_PRE`, `m_dot_PRE` are defined; the model uses the values actually
  defined for the preheater source. Impact quantified in *Verification* 2.
- **2026-10-13 — naming**: `Q_dot_PRE` → `Q_dot_pre_su`, `T_PRE` → `T_pre_su`,
  `P_PRE` → `P_pre_su`, `M_dot_PRE` → `M_dot_pre_su` (CoolSolve swallows
  unknown variables whose name ends in a property-input prefix, which made the
  system one equation short; no physics change).
- **2026-10-13 — zone starts without two-phase property calls**: the state where
  the condensation zone starts is written with the clamps of the original on the
  qualities (`x_7`, `x_4` as `QUALITY` outputs) instead of
  `ENTHALPY(fluid, P, x=x_start)`; the calls with a moving quality made the
  block fail at iteration 0 (`LineSearchFailed`), the clamp form is
  mathematically identical in the two-phase range and always defined.
- **2026-10-13 — curated initials**: the shipped `.initials` is the solution of
  the same equations with the two pressures fixed (see *How to run*); required,
  the block does not converge from the default guesses.
- **Level**: rubric of `docs/taxonomy.md` §3 → 1 (135 equations) + 2 (largest
  block 61) + 1 (arrays) + 1 (six coupled components, multi-zone) + 0 (no
  calibration/off-design) + 1 (curated guesses needed) = 6 → **level 3**.

## Limitations and CoolSolve gaps

- **No pressure drops** (`DP_c = DP_h = 0`, the defaults of the original) and no
  heat loss to the ambient, as in the source.
- **Fixed regime**: the evaporator supply is subcooled liquid (all three zones
  active) and the condenser supply is at the dew point (no desuperheating zone),
  which is what the shipped site data produce. Out of these regimes the clamps
  keep the model well defined but the zone duties need to be re-checked.
- The recuperator and the preheater are rated with the **enthalpy-rate** limit of
  `HexCstEff`, not with `C_min·ΔT`; with a two-phase working fluid on one side
  this overestimates `Q_max` (the ideal enthalpy is taken at a temperature inside
  the dome). This is the behaviour of the source and is kept.
- CoolSolve warns `t=… looks like Fahrenheit` on the water property calls around
  30 °C and `201.97 is interpreted as °C` on the preheater ideal-enthalpy call —
  spurious heuristics (checked against CoolProp, exact agreement).
- No CoolSolve gap blocks this model (`missing_features` is empty).

## Related models

- `CSL-0013` *heat_pump_basic_tespy* and `CSL-0014` *hx_constant_pinch*: the
  same LaboThapPy components at their model level (`HexCstEff`, the condenser
  branch of `HexCstPinch`); this model is the cycle that assembles both branches.
- `CSL-0126` *hx_constant_effectiveness*: the `HexCstEff` component alone.
- `CSL-0133` *heat_pump_propane_pinch*: the same pinch design in a heat-pump
  cycle (condenser + evaporator + constant-efficiency compressor + valve).
- `CSL-0039` *high_temp_heat_pump_pcm_storage*: the Zorlu site on the same fluid
  (CoolSolve example `zorlu_heat_pump`), the cycle this model is the ORC
  counterpart of.
- `CSL-0019` *orc_simple_r245fa*: a screening ORC with an imposed effectiveness,
  no pinch design, no preheater.
