# SEGS solar thermal power plant (TESPy validation model)

🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0147`

Steady-state design-point model of the SEGS VI-type parabolic-trough solar
thermal power plant (Kramer Junction, California), the large validation model
of the TESPy–Ebsilon comparison study of Witte et al. (2022). A Therminol VP-1
oil loop (solar field, HTF pump, HTF splitter at 12.84 % to the reheater)
feeds the steam generator (superheater, evaporator with drum, economiser) of a
regenerative Rankine cycle: 7 turbine stages with individual isentropic
efficiencies (0.64–0.94), 5 feedwater preheaters whose drains cascade through
subcoolers and letdown valves into a 3-inlet feedwater tank (deaerator), a
surface condenser coupled to a wet cooling tower with fan-driven air flow, and
the full generator/motor power chain (7 generators, 5 motors, distribution
bus) ending at the grid as power sink. The model returns all 79 fluid states,
25 power flows, the solar heat input and the net power.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water/steam, Therminol VP-1 (HTF), dry air (cooling tower) |
| **Size** | 397 equations (largest block: 59), plus 2 property `FUNCTION`s |
| **Source** | TESPy `tests/test_models/test_solar_energy_generating_system.py`, [github.com/oemof/tespy](https://github.com/oemof/tespy), commit `19425523`; model originally from [github.com/fwitte/SEGS_exergy](https://github.com/fwitte/SEGS_exergy) (Witte et al., *Energies* 2022) |
| **Authors** | Francesco Witte, Ilka Tuschy and TESPy contributors (see the commit history of the source file) |
| **License** | MIT (TESPy); this translation MIT |
| **CoolSolve** | 0.3.0 — verified against the re-run of the source and the Ebsilon reference values (see *Verification*) |

## Problem statement

Reproduce the design point of the Ebsilon SEGS model used as benchmark in the
TESPy test suite: HTF at 390 °C / 23.304 bar at the solar field outlet,
100 bar / 371 °C live steam at 38.969 kg/s, reheat to 371 °C at 17.1 bar,
condenser at 0.08 bar with a cooling tower cooling 30 °C water by ambient air
at 25 °C. The TESPy test asserts the net electrical power against Ebsilon
(31.769 MW, relative tolerance 5·10⁻⁴) and the HTF temperature at the solar
field inlet (connection 79: 296.254 °C, absolute tolerance 0.05 K).

## Model

The translation keeps the TESPy component equations and the connection labels
as state names (`m_1, p_1, h_1, T_1` = connection "1", `Q_sol` = heat
connection `h_solar`, `e_1…e_25` = power connections). Python solver plumbing
(network objects, cycle closers, design/off-design machinery,Ref references)
becomes plain simultaneous equations; each TESPy component maps to:

- **Turbine**: `eta_s*(h_in − h_out,s) = h_in − h_out` with
  `h_out,s = h(p_out, s_in)`, `P = m*(h_in − h_out)`;
- **Pumps and fan** (work-absorbing): `h_out,s − h_in = eta_s*(h_out − h_in)`;
- **Heat exchangers**: two mass balances, energy balance `m_hot*Δh_hot =
  m_cold*Δh_cold`, optional pressure ratios `pr`, upper terminal temperature
  difference `ttd_u = T_hot,in − T_cold,out` (for the TESPy `Condenser`
  components `T_hot,in` is the dew point at the hot inlet pressure);
- **Subcoolers**: `ttd_l = T_hot,out − T_cold,in` (drain leaves 10 K above
  the incoming feedwater);
- **TESPy `Condenser` components** (main condenser and the 5 preheaters):
  the hot outlet is **saturated liquid** (`subcooling = False` default),
  `h_out,hot = h'(p_out,hot)`;
- **Drum**: all four ports at one pressure, outlets on the saturation lines
  (`x = 0` and `x = 1`), mass and energy balances; the evaporator outlet is at
  `x = 0.5`, the economiser outlet 2 K subcooled (`td_bubble`);
- **Splitter**: mass split free, all outlets at inlet `h` and `p` (HTF
  splitter 7: `m_76 = 0.1284*m_70`);
- **Merge** (incl. the 3-inlet feedwater tank): mass balance, enthalpy
  weighted by mass flow, all ports at one pressure;
- **Valve**: isenthalpic;
- **CycleCloser**: pressure and enthalpy equality only (TESPy imposes no mass
  equation; the mass continuity comes from the component chain);
- **Generator/motor**: `P_out = 0.97/0.95*P_in`; **PowerBus**: sum in = sum
  out; the grid power `e_25 = P_net` is the remaining unknown.

**Therminol VP-1**: the source uses the CoolProp incompressible fluid
`INCOMP::TVP1`, which CoolSolve cannot evaluate (unknown fluid; EES's own
incompressible-substance libraries are likewise unavailable, gap
`CS-GAP-INCOMPRESSIBLE` in the CoolSolve register). The model therefore
evaluates the HTF with the empirical correlations of library model **CSL-0121**
(fit of the HEDH heat-transfer-fluid data sheet HTF-VP1): the two `FUNCTION`s
`h_htf(T)` (specific enthalpy, cp polynomial integrated from 0 °C) and
`rho_htf(T)`. Only enthalpy *differences* enter the balances, so the arbitrary
reference cancels. The HTF pump isentropic state uses the incompressible
relation `h_out,s = h_in + (p_out − p_in)/rho(T_in)`. Dry air (cooling tower)
is the EES ideal-gas substance `Air` (the source's CoolProp pseudo-pure `air`);
only enthalpy differences are used.

Inputs are the fixed data block of the source test (pressures, temperatures,
efficiencies, `ttd` values, split ratio, converted bar → Pa, kJ/kg → J/kg,
MW → W).

## How to run

```bash
coolsolve ./segs_solar_power_plant.eescode
```

The system is square (397 equations / 397 variables, largest block 59) and
converges from the committed `.initials` (the states of the source run,
unit-converted). The level-4 rating follows taxonomy.md §3: equations 2
(397), largest block 2 (59), functions/arrays 1, ≥ 3 coupled components 1,
off-design/semi-empirical 0, curated guesses 1 → score 7.

## Results

| Quantity | CoolSolve | TESPy (re-run) | Ebsilon (test target) |
|---|---:|---:|---:|
| Net power `P_net` (e25) | 31.782 MW | 31.7688 MW | 31.769 MW |
| HTF temperature at field inlet `T_79` | 296.410 °C | 296.2539 °C | 296.254 °C |
| Solar heat `Q_sol` | 91.883 MW | 91.8697 MW | – |
| HTF mass flow `m_70` | 402.67 kg/s | 405.39 kg/s | – |
| Main steam flow `m_3` | 38.969 kg/s | 38.969 kg/s | – |
| HP turbine 1 power | 7.6995 MW | 7.6995 MW | – |
| Solar-to-net efficiency | 34.6 % | 34.6 % | – |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1…13: live steam, turbine
exhausts, reheat, condenser, condensate, deaerator, economiser inlet) give
the steam cycle on the T-s or P-h diagram (CoolSolve *Diagram* tab, *Overlay
array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the
     steam cycle (arrays P[i], h[i], T[i], s[i]), figures/segs_solar_power_plant_ts.png -->

## Verification

**Reference: re-run of the source test** (TESPy 0.11.3.dev0 built from the
local clone at commit `19425523`, throw-away virtual environment under
`work/segs/`; script `run_segs.py`, a 1:1 replica of
`tests/test_models/test_solar_energy_generating_system.py::setup_method`
without the exerpy import). The re-run reproduces the test assertions
(`T_c79 = 296.2539 °C`, `power_e25 = 31.7688 MW` against the Ebsilon values).
The dumped connection states (`tespy_reference.json`, 79 fluid states with
m, p, h, T and fluid, 25 power flows) were compared with the CoolSolve `.sol`
by a short Python script; every deviation quoted below comes from that run.

| Quantity group | Max deviation vs TESPy re-run |
|---|---|
| Water/steam temperatures (46 states) | 0.0000 K (identical CoolProp backend) |
| Water/steam pressures | < 4·10⁻¹³ (relative) |
| Water/steam mass flows (except CW loop) | < 2·10⁻⁵ (relative) |
| Turbine/generator/motor powers e1–e18, e21, e22 | < 10⁻⁵ (relative) |
| Cooling-water loop (TESPy fluid `INCOMP::Water`) | `m_cw` −0.19 %; absolute enthalpies offset by the `INCOMP::Water` reference state (≈ +84 kJ/kg at 36 °C), differences agree to 0.2 % |
| Air side (fan, cooling tower) | enthalpies < 1.4·10⁻⁷, mass flow 1.9·10⁻⁵ |
| HTF loop (Therminol VP-1) | mass flow −0.67 %, temperatures within 0.31 K, absolute enthalpies +5.6 % (correlation offset, differences ≈ 1 %) |
| Net power vs Ebsilon target 31.769 MW | +4.2·10⁻⁴ (tolerance 5·10⁻⁴) |
| HTF pump power | −0.8 % |

**All remaining deviations come from the Therminol VP-1 property data**: this
model uses the CSL-0121 HEDH correlations where the source uses CoolProp
`INCOMP::TVP1`. They propagate into the HTF mass flow (the steam-generator
duties are fixed by the water side), hence into the HTF pump power and, through
the merge at the field inlet, into `T_79` (+0.156 K against the Ebsilon value —
outside the ±0.05 K of the TESPy test, whose comment notes that its tolerances
"account for differences in the fluid property data of the heat transfer fluid
between CoolProp versions"). Everything on water/steam and air agrees to
solver precision because CoolSolve and TESPy share the CoolProp backends
(HEOS water, ideal-gas/pseudo-pure air).

**Energy balance** (checked on the solution): the distribution bus closes
exactly (Σ generator outputs − Σ motor inputs = `P_net`); `Q_sol` equals the
sum of the four HTF duties by construction, and the overall solar-to-net
efficiency of 34.6 % matches the source.

## Source and attribution

Translated from the TESPy test suite (MIT): `tests/test_models/
test_solar_energy_generating_system.py` at commit `19425523` of
[github.com/oemof/tespy](https://github.com/oemof/tespy) (local clone
`~/git/tespy`), by **Francesco Witte** and contributors (Ilka Tuschy et al.).
The original SEGS exergy model lives at
[github.com/fwitte/SEGS_exergy](https://github.com/fwitte/SEGS_exergy) and is
described in F. Witte, I. Tuschy et al., *Energies* (2022) — cited as the
scientific reference of the model. Reference values of the Ebsilon benchmark
model are quoted from the test file. Therminol VP-1 correlations: library
model `CSL-0121` (fit of the HEDH data sheet HTF-VP1, ULiège collection).
Decision taken without asking: the TESPy *exerpy* exergy-analysis part of the
test (`test_exergy_analysis`) is out of scope — only the thermodynamic model
(`test_model`) is translated.

## Conversion log

- **2026-10-14 — translation** (`T-TRANSLATE`, card C-192, batch B-12).
  Physics translated from the TESPy network to simultaneous EES equations;
  component equations as listed under *Model*. Units converted by hand:
  bar → Pa, kJ/kg → J/kg, MW → W, ttd in K. Python plumbing (Network,
  CycleCloser, Ref, PowerConnection) became plain equations; the grid power
  `e_25` remains the single degree of freedom of the power chain.
- TESPy `Condenser` semantics applied to the main condenser **and** the 5
  preheaters: `ttd_u` to the dew point at the hot inlet and saturated-liquid
  hot outlet (`subcooling = False`), verified digit-by-digit against the
  re-run (`h_18`, `h_37`, `h_42`, `h_47`, `h_52`, `h_57` = `h'(p)` to 0.000).
- Cycle closers impose pressure and enthalpy equality only (no mass equation);
  adding the mass equations made the system over-determined — removed.
- Two sign conventions were initially transcribed wrongly and fixed against
  the re-run: the subcooler/evaporator `ttd_l` (hot outlet is *above* the
  cold inlet, +10 K / +5 K) and the reheater steam side (steam is heated,
  `h_7 > h_6`); pump/fan efficiency `eta = Δh_s/Δh` (not the turbine form).
  All logged here for transparency; the committed file was verified after the
  fixes.
- `INCOMP::TVP1` replaced by the CSL-0121 correlations (see *Model*);
  `INCOMP::Water` (cooling water) and pseudo-pure `air` replaced by the EES
  real `Water` and ideal-gas `Air` substances; HTF pump isentropic state by
  the incompressible relation. Deviations listed under *Verification*.
- Dependencies of the card: the Stodola cone law (C-180/`CSL-0135`) is not
  needed (all turbines are design-point with fixed exhaust pressures) and
  there is no combustion in the solar plant, so C-184/C-191 do not apply.

## Limitations

- Design point only (the source test solves `mode="design"`; the off-design
  machinery of TESPy is not part of the model).
- The exergy analysis of the source repository (exerpy) is not translated.
- `T_79` is reproduced within 0.16 K, not within the 0.05 K of the TESPy
  test, because of the VP-1 property data (see *Verification*).

## Related models

- `CSL-0121` *heat_transfer_fluid_properties*: the Therminol VP-1 correlations
  used by this model (`h_htf`, `rho_htf` are copied from it).
- `CSL-0029` *rankine_cycle_regenerative_extraction*: smaller regenerative
  extraction Rankine cycle (one reheater, extraction turbines, deaerator) —
  the teaching-level counterpart of the water/steam part of this plant.
- `CSL-0135` *turbine_stodola_offdesign*: off-design turbine model (Stodola
  cone law) for part-load studies of such plants; not used here (design point
  with fixed stage efficiencies and exhaust pressures).
