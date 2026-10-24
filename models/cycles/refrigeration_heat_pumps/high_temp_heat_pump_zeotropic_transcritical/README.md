# High-temperature heat pump: zeotropic/transcritical cycle (R1336mzz(Z))

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0253`

High-temperature heat pump (HTHP) of the maintainers's
[NextGenerationHeatPumps](https://github.com/squoilin/NextGenerationHeatPumps)
repository: the cycle pressures are imposed (default run 10.5 bar / 32 bar on
R1336mzz(Z)), the compressor has a constant isentropic efficiency, the heat
delivered is imposed, and the two secondary water loops are *recalculated*
from an imposed pinch in each exchanger — their capacity flow rates are the
unknowns of the design problem. The script is written for pure fluids or
zeotropic mixtures and for subcritical or transcritical cycles; the default
run is **transcritical** in the CoolProp property data used here (32 bar is
above the 29.04 bar critical pressure of R1336mzz(Z)), so the condensing
states collapse onto the compressor outlet and the subcooling is referred to
the critical temperature, exactly as in the original's `else` branch.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration cycles and heat pumps |
| **Fluids** | R1336mzz(Z) (native file), R365mfc (runnable variant) |
| **Size** | 66 equations (largest block: 7, the `MIN`-pinch loop of the variant) |
| **Source** | [squoilin/NextGenerationHeatPumps](https://github.com/squoilin/NextGenerationHeatPumps), `nghp/advanced HTHP model.py`, commit `6db23af4dbad2098043a74d1871dbcc6f8eee468` |
| **Authors** | Sylvain Quoilin |
| **License** | MIT (repository `LICENSE`: "MIT License, Copyright (c) 2020 Sylvain Quoilin") |
| **CoolSolve** | 0.4.0 (`0.4.0@9768373`) — native file blocked by `CS-GAP-FLUIDS-R1336MZZ`; runnable `_coolsolve` variant verified against the original script |

## Problem statement

As in the original script: impose the cycle pressures `p_low` and `p_high`,
the superheating `DELTAT_sh`, the subcooling `DELTAT_sc`, the compressor
isentropic efficiency `epsilon_s`, the heat delivered `Q_dot_cd`, the two
water inlet temperatures and the two pinch points; compute the eight cycle
states, the mass flow rate, the COP, and the water profiles that realise the
imposed pinches (the original prints the water inlet/outlet temperatures of
each exchanger and draws the T-s diagram; the plot plumbing is not
translated).

## Model

- **States 1–8** follow the original script's states 0–7 (index shifted by
  1): 1 saturated vapour at `p_low`, 2 compressor supply (`+ DELTAT_sh`),
  3 compressor outlet (from `epsilon_s` and the isentropic exhaust `h_s`
  at `(p_high, s_2)`), 4/5 the condensation states, 6 condenser outlet
  (subcooled), 7 evaporator inlet after the isenthalpic valve, 8 = 1 (loop
  closure, as the original state 7).
- **Transcritical default run**: `p_high` = 32 bar > `p_crit` = 29.04 bar,
  so states 4/5 are aliased onto state 3 and `T[5] = T_CRIT - DELTAT_sc`
  (the original's `else` branch). The subcritical branch (`T[4]`/`T[5]`
  saturated at `p_high`, `T[6] = T[5] - DELTAT_sc`) is translated in the
  `_coolsolve` variant, whose fluid (R365mfc, `p_crit` = 32.66 bar) takes it.
- **Exchangers**: the original discretises each exchanger (40/20 points,
  enthalpy-linear grid, linear water profile) and solves for the water
  capacity flow rate `C_dot` such that the *minimum* stream temperature
  difference equals the imposed pinch (`fsolve`). In the default runs the
  minimum lies at an exchanger end (condenser: hot end, `T[3] - T_hf_ex`;
  evaporator: cold end, `T_cf_ex - T[7]`), so the same `C_dot` is closed by
  `MIN` of the end (variant: also dew/bubble interface) temperature
  differences, the pattern of `CSL-0013`/`CSL-0014`. Equivalence checked
  against the original grids: the end differences are exactly the grid
  minima (7.50 K on both sides).
- **Mass flow and COP** as in the original:
  `M_dot = Q_dot_cd/(h[3] - h[5])`, `COP = (h[3] - h[5])/(h[3] - h[2])`.

## How to run

Native file (blocked, does not run in CoolSolve):

```bash
coolsolve ./high_temp_heat_pump_zeotropic_transcritical.eescode
# EvaluationError - Unknown fluid: 'R1336mzz(Z)'  (CS-GAP-FLUIDS-R1336MZZ)
```

Runnable variant (R365mfc, subcritical branch, `p_low` = 8 bar — every
change logged below), with its `.initials` and `.sol` baseline:

```bash
coolsolve ./high_temp_heat_pump_zeotropic_transcritical_coolsolve.eescode
```

Tested as `CSL-0253:coolsolve` by `tools/test_models.py`.

## Results

Variant `CSL-0253:coolsolve` (R365mfc, 8/32 bar, same waters and pinches as
the original default run):

| Quantity | Value |
|---|---|
| `T[2]` compressor supply | 120.34 °C |
| `T[3]` compressor outlet | 186.41 °C |
| `T[4]`/`T[5]` condensing | 185.68 °C |
| `T[6]` gas-cooler/condenser outlet | 153.68 °C |
| `M_dot` | 0.086322 kg/s |
| `COP` | 3.957 |
| Condenser water 130 °C → | 178.91 °C (`C_dot_hf` = 204.45 W/K) |
| Evaporator water 135 °C → | 120.84 °C (`C_dot_cf` = 527.70 W/K) |

Native default run (R1336mzz(Z), 10.5/32 bar, transcritical) reference
values from the re-run of the original script, which the native equations
reproduce as soon as the fluid is registered: `T[3]` = 181.67 °C,
`T[5]` = 139.35 °C (= `T_CRIT` − 32 K), `M_dot` = 0.089822 kg/s, `COP` =
5.514, condenser water 130 °C → 174.17 °C (`C_dot_hf` = 226.38 W/K),
evaporator water 135 °C → 120.84 °C (`C_dot_cf` ≈ 843.3 W/K, cold-end
pinch).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![T-s diagram of the cycle](figures/high_temp_heat_pump_zeotropic_transcritical_ts.png)
     + one-line caption -->

## Verification

The original script was re-run in a throw-away venv (Python 3.12,
CoolProp 8.0.0; `MPLBACKEND=Agg`; the `get_ipython().magic('reset -sf')`
line and the `misc`/`components` relative imports fixed in a **copy** under
`work/`, never in the library). Two runs were used:

1. **Native default run** (R1336mzz(Z), 10.5/32 bar) for the reference
   numbers above; with CoolProp the cycle is transcritical (see conversion
   log).
2. **Variant operating point** (R365mfc, `p_low` = 8 bar, `p_high` = 32 bar)
   compared with the variant `.sol`: all printed state points, `M_dot`,
   `COP`, both water outlet temperatures and `C_dot_hf` agree; **maximum
   relative difference 7.9e-08** (on `C_dot_hf`; the script prints 4–6
   significant digits), state points ≤ 3e-11. Same CoolProp equation of
   state on both sides (8.0.0 in the venv, 8.1.0dev in the CoolSolve
   build).

| Quantity | Script | CoolSolve variant | rel. diff. |
|---|---|---|---|
| `T[3]` [°C] | 186.41085697 | 186.41085697 | 1.1e-11 |
| `h[3]` [J/kg] | 548 142.71666946 | 548 142.7166592 | 1.9e-11 |
| `M_dot` [kg/s] | 0.0863220329 | 0.0863220329 | 8.9e-11 |
| `COP` [-] | 3.9565029631 | 3.9565029631 | 2.7e-10 |
| `T_hf_ex` [°C] | 178.91086 (174.2 printed) | 178.91085697 | 2.2e-08 |
| `C_dot_hf` [W/K] | 204.4536 | 204.4535839 | 7.9e-08 |
| `T_cf_ex` [°C] | 120.8 (120.83937984) | 120.83937984 | 3.2e-09 |

## Source and attribution

Original model: **"advanced HTHP model.py"** by **Sylvain Quoilin**,
[github.com/squoilin/NextGenerationHeatPumps](https://github.com/squoilin/NextGenerationHeatPumps)
(path `nghp/advanced HTHP model.py`, commit
`6db23af4dbad2098043a74d1871dbcc6f8eee468`), MIT licence. Properties:
CoolProp (the original selects the `REFPROP` back end, replaced by the
CoolProp `HEOS` back end per the library decision D12). Candidate
`LDS-010` of `sources/ext_leads/inventory.csv` (batch B-14, 2026-10-21).

## Conversion log

- **2026-10-21 — translation (T-TRANSLATE)**: Python plumbing removed
  (IPython reset, `NoStdStreams`, CoolProp `PropertyPlot`/`StateContainer`
  T-s plot, `draw_ts`); the state computations become simultaneous
  equations with the source's variable meanings (states renamed 1–8 =
  original 0–7); the `hx_pinch` discretised loops + `fsolve` become the
  `MIN`-of-end-differences pinch conditions closing the water capacity flow
  rates (equivalent for the default runs: the grid minima are at the ends,
  checked against the original 40/20-point profiles).
- **2026-10-21 — decision D12 (REFPROP → CoolProp)**: `library = 'REFPROP'`
  replaced by HEOS in the verification harness and by the CoolSolve/CoolProp
  fluid name in the model. Consequence, documented: CoolProp's critical
  pressure of R1336mzz(Z) is 29.037 bar (REFPROP's is higher), so the
  default run (32 bar) takes the **transcritical** branch of the original
  script instead of its subcritical branch; the verification is CoolProp to
  CoolProp, so the comparison is unaffected.
- **2026-10-21 — phase-specified isentropic exhaust**: the original calls
  `specify_phase(iphase_gas)` before the `(P, s)` flash of the isentropic
  outlet; this call **fails in CoolProp 8** for R1336mzz(Z) ("unable to
  solve 1phase PY flash"), so the plain `(P, s)` flash is used everywhere.
  For the default run the isentropic exhaust is clearly gas (it solves, and
  the plain flash returns it, quality −1); for the R365mfc variant the
  isentropic reference is marginally two-phase (quality ≈ 0.98) and the
  plain flash returns the dome-consistent value — the value a valid EES
  `enthalpy(P=…, s=…)` call returns as well.
- **2026-10-21 — input readings kept as in the original**: `Q_dot_cd =
  10000` is the total condenser duty in W (the original comment says "heat
  capacity flowrates of cooling water kW/K" but uses it as the duty);
  `T_w_ex_ev = 0` selects the imposed-pinch branch of the evaporator (the
  imposed-outlet-temperature branch is not translated); `impose_T = False`
  (the imposed-saturation-temperature branch is not translated); the
  zeotropic-mixture option of the original (`Butane&Hexane`, commented out
  in the script, `set_mole_fractions([0.5, 0.5])`) is not part of the
  default run — the equations take `fluid$` as a string, so a mixture run
  only needs the mixture string in `fluid$` (CoolSolve supports CoolProp
  mixtures, `CS-GAP-FLUIDS-MIXTURE` closed).
- **2026-10-21 — runnable variant** `…_coolsolve.eescode`: fluid
  `R365mfc` (the gap-forced substitution), `p_low` = 8 bar (10.5 bar would
  violate the imposed 7.5 K evaporator pinch: `Tsat`(10.5 bar) = 125.9 °C
  against a 135 °C source), same `p_high`, waters, pinches, efficiencies;
  subcritical branch equations (states 4/5 saturated, `T[6] = T[5] -
  DELTAT_sc`) with dew/bubble interface candidates in the condenser pinch.
  No other change; no CoolSolve-only syntax.
- **Level**: equations 66 → 1; largest block 7 → 1; arrays present → 1;
  ≥ 3 coupled components (compressor + 2 exchangers + valve) → 1;
  off-design/semi-empirical → 0; curated guesses not needed (solves without
  `.initials`) → 0. Score 4 → **level 3**.

## Limitations and CoolSolve gaps

- `CS-GAP-FLUIDS-R1336MZZ`: the working fluid of the default run,
  R1336mzz(Z), is missing from the CoolSolve fluid registry although
  CoolProp provides it; the native file stops with
  *"Unknown fluid: 'R1336mzz(Z)'"*. No workaround in the native file; the
  `_coolsolve` variant substitutes R365mfc.
- The zeotropic-mixture capability of the original is kept through the
  `fluid$` string (CoolProp mixture syntax) but is not exercised by a
  default run (the original's default is the pure fluid).

## Related models

- `CSL-0133` (heat_pump_propane_pinch): same imposed-pinch heat-pump
  structure (water/water, subcritical, pinch closes the two saturation
  pressures), from LaboThapPy.
- `CSL-0145` (refrigeration_co2_transcritical_booster): transcritical cycle
  in CoolSolve (CO2).
- `CSL-0014` (hx_constant_pinch): imposed-pinch exchanger formulation
  (`MIN` of candidate differences).
