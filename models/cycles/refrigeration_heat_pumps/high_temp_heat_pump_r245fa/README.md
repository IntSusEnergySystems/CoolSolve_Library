# Simple R245fa high-temperature heat pump (T_ev 80 °C / T_cd 145 °C)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0251`

Subcritical vapour-compression high-temperature heat pump on R245fa that lifts water
from 95 °C to 120 °C: the cycle conditions are imposed (evaporation at 80 °C,
condensation at 145 °C, 5 K superheating, 5 K subcooling, compressor isentropic
efficiency 0.6) and the water-side temperature profiles of both exchangers are
recomputed from the refrigerant states on 10 nodes; the local temperature
differences give the two pinch points (10.31 K and 10.00 K in the reference run).

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R245fa (working fluid), water (secondary fluid, constant cp) |
| **Size** | 163 equations (largest block: 1) |
| **Source** | [squoilin/NextGenerationHeatPumps](https://github.com/squoilin/NextGenerationHeatPumps) `nghp/simple HTHP model.py` @ `6db23af` |
| **Authors** | Sylvain Quoilin (MIT) |
| **License** | MIT (repository LICENSE, © 2020 Sylvain Quoilin) |
| **CoolSolve** | 0.4.0@9768373 — verified (source re-run, max rel diff 2.3e-09) |

## Problem statement

High-temperature heat pumps deliver process heat above 100 °C. The source script
studies the simplest configuration: a subcritical cycle on a single fluid with
imposed saturation temperatures, a compressor with a constant isentropic efficiency,
and secondary-fluid (water) profiles recomputed from the refrigerant enthalpy
changes — no imposed water outlet temperatures, only the water inlets and a
temperature approach at each exchanger end.

## Model

Eight refrigerant state points (numbered 0–7 as in the original; state 7 repeats
state 0):

| state | description |
|---|---|
| 0 | evaporator outlet, saturated vapour at `P_low` = `PRESSURE(R245fa, T=80 °C, x=0.5)` |
| 1 | compressor inlet, superheated vapour (`T[1] = T[0] + 5 K`) |
| 2 | compressor outlet, `h[2] = h[1] - (h[1]-h_ex_cp_s)/epsilon_s` with `epsilon_s = 0.6` |
| 3 | saturated vapour at the condenser inlet (`P_high` = `PRESSURE(R245fa, T=145 °C, x=0.5)`) |
| 4 | saturated liquid in the condenser |
| 5 | subcooled condenser outlet (`T[5] = T[4] - 5 K`) |
| 6 | evaporator inlet after isenthalpic expansion (`h[6] = h[5]`) |

Mass flow: the condenser duty is imposed (`Q_dot_cd = 10 kW`) and
`M_dot = Q_dot_cd/(h[2]-h[5])`. The sink water enters at 120 °C; its mass flow
follows from the temperature approach `DELTAT_cd = 10 K` imposed at the condensing
temperature (`T_hw[3] = T[3] - DELTAT_cd`). The source water enters at 95 °C and
its mass flow from the approach `DELTAT_ev = 10 K` at the evaporator refrigerant
inlet (`T_cw[6] = T[6] + DELTAT_ev`). Both water streams have a constant
`cp_w = 4800 J/kg-K` (as in the original).

Each exchanger is discretised on 10 equal-enthalpy nodes (`DUPLICATE i=1,10`): the
refrigerant temperature from `(h, P_high)`/`(h, P_low)` property calls, the water
temperature linearly between the two end values (the water profiles are linear in
enthalpy, so the node values are exact). The pinch of each exchanger is
`MIN(dT[1..10])` over the signed local differences (refrigerant − water in the
condenser, water − refrigerant in the evaporator — the branch that the original's
`if/else` sign convention selects for these two exchangers).

Post-processing outputs (not in the original script, derived from its equations):
`Q_dot_ev`, `W_dot`, `COP_cd = Q_dot_cd/W_dot`, `COP_ev = Q_dot_ev/W_dot`.

Inputs: `fluid$`, `T_ev`, `T_cd`, `DELTAT_sh`, `DELTAT_sc`, `epsilon_s`,
`T_w_su_cd`, `DELTAT_cd`, `Q_dot_cd`, `T_w_su_ev`, `DELTAT_ev`, `cp_w`.
Outputs: `M_dot`, `M_dot_hw`, `M_dot_cw`, `pinch_cd`, `pinch_ev`, the profiles
`T_prof_cd[i]`/`T_hf[i]`, `T_prof_ev[i]`/`T_cf[i]` and the post-processed powers.

## How to run

```
coolsolve models/cycles/refrigeration_heat_pumps/high_temp_heat_pump_r245fa/high_temp_heat_pump_r245fa.eescode
```

Fully explicit system (163 equations, 163 blocks of size 1): no guesses needed,
solves in 0 iterations. No variants, no `coolsolve.conf`.

## Results

| quantity | value |
|---|---|
| `P_low` / `P_high` | 789 008 Pa / 3 109 867 Pa |
| `T[0..7]` (°C) | 80, 85, 153.18, 145, 145, 140, 80, 80 |
| `M_dot` (refrigerant) | 0.10211 kg/s |
| `M_dot_hw` (sink water) | 0.11028 kg/s |
| `M_dot_cw` (source water) | 0.25528 kg/s |
| `pinch_cd` / `pinch_ev` | 10.306 K / 10.000 K |
| `Q_dot_ev` / `W_dot` | 6 126.8 W / 3 873.2 W |
| `COP_cd` / `COP_ev` | 2.582 / 1.582 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the
     cycle with the two water profiles, saved in figures/, e.g.
     ![T-s diagram of the heat pump](figures/high_temp_heat_pump_r245fa_ts.png) -->

## Verification

**Source re-run** (`source-rerun`): `nghp/simple HTHP model.py` (plus its
`components.heat_exchangers.hx`) was re-run in a throw-away venv (Python 3.12,
CoolProp 8.0.0, `MPLBACKEND=Agg`; the IPython `reset` line removed from a copy,
imports fixed by `PYTHONPATH`) and its results compared value by value with the
`.sol` of this model — 127 values: the 8 state temperatures (°C), pressures,
enthalpies and entropies; the three mass flows; both pinches; the four end
temperatures of the water (`T_hw[2..5]`, `T_cw[0,1,6]`); the two duties/power;
and the four 10-node profiles (`T_prof_cd`, `T_hf`, `T_prof_ev`, `T_cf`, plus
`h_cd`, `h_ev`, `s_cd`, `s_ev`).

| group | max relative deviation |
|---|---|
| state `T[0..7]`, `p`, `h`, `s` | ≤ 2.4e-11 |
| `M_dot`, `M_dot_hw`, `M_dot_cw` | ≤ 7.7e-11 |
| `pinch_cd` = 10.30619430 K, `pinch_ev` = 10 K | ≤ 3.2e-10 |
| water end temperatures `T_hw`/`T_cw` | ≤ 1.4e-11 |
| `Q_dot_ev`, `W_dot` (post-processed) | ≤ 4.0e-11 |
| 10-node profiles (40 temperatures, 40 enthalpies, 20 entropies) | ≤ 2.3e-09 |
| **all 127 values** | **2.3e-09** |

The printed lines of the script agree as well (rounded there): `M_dot` 0.10 kg/s,
`M_dot_hw` 0.11 kg/s, condenser pinch 10.31 K, evaporator pinch 10.00 K, and the
printed state tables (T in K, p in Pa, h in J/kg, s in J/kg-K) match the `.sol`
values above. The residual deviations (≤ 2.3e-09) are the CoolProp back-end
difference (pip CoolProp 8.0.0 in the venv vs the pinned CoolProp 8.1.0dev of the
CoolSolve build), far below the expected < 0.1 %. No variable was excluded from
the comparison.

## Source and attribution

- Sylvain Quoilin (MIT), *Simple heat pump model with CoolProp (high-level
  interface)*, `nghp/simple HTHP model.py` of
  [github.com/squoilin/NextGenerationHeatPumps](https://github.com/squoilin/NextGenerationHeatPumps),
  commit `6db23af4dbad2098043a74d1871dbcc6f8eee468` (shallow clone of 2026-10-21).
- Licence: MIT (repository `LICENSE`, © 2020 Sylvain Quoilin).
- The companion `hx` discretised-exchanger function lives in the same repository
  (`nghp/components/heat_exchangers.py`, same author and licence); its equations
  are inlined twice in the model (see conversion log).
- Inventory row: `sources/ext_leads/inventory.csv` LDS-009.

## Conversion log

- **2026-10-21 — translation**: from the Python script (units K, Pa, J/kg) to
  EES equations in the CoolSolve unit system (SI, temperatures in °C): every
  temperature input and state temperature converted K→°C (`T_ev = 80` for
  353.15 K etc.; temperature *differences* keep their value). The forward script
  (property calls in sequence) becomes a simultaneous, fully explicit square
  system (163 equations, largest block 1).
- The `hx()` function of `nghp/components/heat_exchangers.py` is inlined twice
  (condenser and evaporator) as `DUPLICATE i=1,10` blocks, as in the original
  call sites; its Python `if/else` sign convention for the pinch
  (`min(T_sf − Ti)` or `min(Ti − T_sf)`) is written as the signed difference
  appropriate to each exchanger (`dT_cd = T_prof_cd − T_hf`,
  `dT_ev = T_cf − T_prof_ev`); both branch conditions of the original were
  checked to hold for these exchangers, so the values are the same. The pinch
  itself uses the aggregate `MIN(dT[1..10])` (EES/CoolSolve array aggregate).
- Name collision resolved: the original rebinds the Python name `T_cd`/`T_ev`
  (first the scalar condensation/evaporation temperature, later the 10-node
  refrigerant profile returned by `hx`); EES has one variable per name, so the
  profile arrays are `T_prof_cd[i]`/`T_prof_ev[i]` (documented in the model).
  All other source names (`T`, `p`, `h`, `s`, `T_hw`, `T_cw`, `M_dot`,
  `M_dot_hw`, `M_dot_cw`, `h_cd`, `h_ev`, `s_cd`, `s_ev`, `T_hf`, `T_cf`,
  `pinch_cd`, `pinch_ev`, `cp_w`, `p_low`/`P_low`, `p_high`/`P_high`) are kept.
- State numbering 0–7 (including the duplicated state 7 of the original) kept;
  the arrays `T[i]`, `h[i]`, `s[i]`, `P[i]` double as the diagram overlay arrays.
- Dead code dropped: the `v` array (allocated, never filled in the original) and
  the commented-out critical-point lines. The plot block (CoolProp
  `PropertyPlot`/`StateContainer`, IPython) is Python plumbing and disappears.
- Comment corrections: the original's comment on `Q_dot_cd`
  ("heat capacity flowrates of cooling water kW/K") contradicts its use as the
  condenser duty in W (10 kW); the model says so. The original's comments on
  `DELTAT_cd`/`DELTAT_ev` ("pinch point temperature of cooling water") are
  kept as "temperature approach", the quantity actually computed.
- Post-processing block added (marked as not in the original): `Q_dot_ev`,
  `W_dot`, `COP_cd`, `COP_ev`, derived from the original's own equations; it
  cannot change the results.
- No (T, H) or other unsupported property input pair occurs in the source (all
  calls are (T, x), (T, P), (s, P), (h, P)); no REFPROP call; no MODULE/
  SUBPROGRAM: no decision D11/D12/D10 rewrite was needed. The secondary fluid is
  water only through the constant `cp_w` — no water property call, as in the
  original.
- **Level**: score of taxonomy §3: equations 163 → 1; largest block 1 → 0;
  arrays/`DUPLICATE` present → 1; discretised exchangers (multi-zone) → 1;
  no semi-empirical/off-design physics → 0; no curated guesses → 0. Total 3 →
  level 2 (matches the `level_guess` of the inventory row).

## Limitations and CoolSolve gaps

Physical: subcritical cycle on a pure fluid only (the companion *advanced* script
of the repository covers zeotropic/transcritical cycles, translated separately);
no pressure drops; constant water `cp`; the pinch is evaluated on the 10 discrete
nodes, not continuously; the isentropic-efficiency compressor model has no
mechanical losses. No CoolSolve gap blocks this model (`missing_features` empty).

## Related models

- `CSL-0133` (propane heat pump with pinch-sized exchangers): same pinch-check
  philosophy on a low-temperature propane cycle; this model instead *imposes* the
  cycle temperatures and recomputes the water profiles of a high-temperature
  (80/145 °C) R245fa cycle.
- `CSL-0039` (high-temperature heat pump with PCM storage, Zorlu case study):
  another high-temperature heat pump, different fluid (cyclopentane), topology
  and storage.
- `CSL-0014` (hx_constant_pinch): the imposed-pinch exchanger component; here the
  pinch is an *output* of imposed end approaches on discretised profiles.
- `CSL-0138` (moving-boundary heat exchanger): higher-fidelity exchanger model
  for the same kind of evaporation/condensation problems.
