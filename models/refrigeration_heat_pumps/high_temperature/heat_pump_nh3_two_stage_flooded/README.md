# Two-stage NH3 heat pump with flooded evaporator (TESPy benchmark vs Ebsilon)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0313`

An industrial-size ammonia heat pump that raises a pressurised-water loop from 60 °C to 105 °C (225 kW at the design point),
after the heat-pump benchmark of the TESPy test suite. The refrigerant is evaporated in a **flooded evaporator**: a drum
separates the vapour from the liquid, a circulation pump (circulation ratio 10) pushes the liquid through the evaporator, and
the saturated vapour is superheated in a small superheater before two compressor stages with an **intercooler**. Water at 12 °C
heats first the superheater, then the evaporator. The model contains the **design point** (pinch, superheat and outlet states
specified) and an **off-design point** of the same machine, solved simultaneously: the heat transfer coefficients UA of the four
exchangers come from characteristic lines, the pressure drops from zeta/D⁴ laws, the efficiencies from characteristic lines.
The off-design point is the operating point of the source test, which compares the COP with an Ebsilon model over 20 points.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | Ammonia (refrigerant), Water (source, intercooler and sink circuits) |
| **Size** | 291 equations (largest block: 69): 30 input assignments, 113 for the design case, 120 for the off-design case, 28 for the diagram state points |
| **Source** | TESPy, `tests/test_models/test_heat_pump_model.py` (commit `19425523`) |
| **Authors** | Francesco Witte (author of the test file in the TESPy repository history) and the TESPy contributors |
| **License** | MIT (TESPy and this library) |
| **CoolSolve** | 0.4.0 — verified against a re-run of the TESPy test (see *Verification*) |

## Niche

The library has several heat pumps; the nearest are:

- `CSL-0250` *cascade_heat_pump_geothermal_dh* (same TESPy origin, with an ammonia variant): two coupled loops of single-stage
  cycles, sectioned exchangers sized by a pinch, no drum, no circulation pump, no characteristic lines, design only.
- `CSL-0013` *heat_pump_basic_tespy* and `CSL-0133` *heat_pump_propane_pinch*: single-stage cycles with a dry evaporator, a
  constant isentropic efficiency and (CSL-0133) pinch-sized exchangers.
- `CSL-0145` *refrigeration_co2_transcritical_booster*: CO₂ booster with a flash-gas receiver, not an ammonia heat pump.

What this model adds: (1) the **flooded evaporator** topology, with drum, liquid circulation pump and a vapour superheater,
the usual layout of ammonia plants; (2) **two-stage compression with intercooling** on NH₃ and a heat sink at 105 °C;
(3) the full **off-design machine description** of TESPy (UA characteristic lines of four exchangers, zeta/D⁴ pressure drops,
efficiency lines of compressors and pumps) solved together with the design point, which the heat pumps of the library do not have
(the smoothed LMTD is that of `CSL-0137`, the characteristic-line pattern that of `CSL-0135`); (4) an **independent second reference**: the
20-point COP matrix of an Ebsilon model.

## Problem statement

Design point (TESPy `design` mode): condenser refrigerant side at 60 bar (1 000 Pa pressure drop), valve inlet subcooled by
5 K; heat sink water at 10 bar heated from 60 to 105 °C; drum at 5 °C (saturated vapour leaves the drum, pump flow = 10 times the
vapour flow); superheater outlet 5 K above the dew point (0.05 bar drop); heat source water 20 kg/s at 12 °C and 1 bar
(evaporator lower terminal temperature difference 5 K); compressor 1 delivers 15 bar, the intercooler (water 5 kg/s at
20 °C) brings the refrigerant to 40 °C, compressor 2 delivers 60 bar; all four turbomachines have η_s = 0.8.

Off-design: the same machine with its design-point UA values, zeta/D⁴ coefficients and efficiency, a sink outlet temperature
`T_sink_o` and a source mass flow `M_dot_11_o` (the sink inlet 60 °C / 10 bar, the drum temperature of 5 °C and the compressor
outlet pressures 15 and 60 bar stay fixed, as in the test). The source test compares the COP
`Q̇_cd / (Ẇ_cp1 + Ẇ_cp2)` with an Ebsilon model for four sink temperatures (105, 100, 90, 80 °C) and five source flows each.

## Model

States follow the TESPy connections (table below). Subscript `_d` = design case, `_o` = off-design case, same equations
with the specified quantities of the design case replaced by the characteristic laws.

| State | TESPy connection | State | TESPy connection |
|---|---|---|---|
| 1 | superheater → compressor 1 | 10 | drum → superheater (saturated vapour) |
| 2 | compressor 1 → intercooler | 11 | source → superheater (water) |
| 3 | intercooler → compressor 2 | 12 | superheater → evaporator (water) |
| 4 | compressor 2 → condenser | 13 | evaporator → sink (water) |
| 5 | condenser → valve | 14 | intercooler water inlet |
| 6 | valve → drum | 15 | intercooler water outlet |
| 7 | drum → circulation pump (saturated liquid) | 16 | consumer → recirculation pump |
| 8 | circulation pump → evaporator | 17 | recirculation pump → condenser (water) |
| 9 | evaporator → drum (two-phase) | 18 | condenser → consumer (water) |

- **Drum** (TESPy `Drum`): one pressure `p_dr` = saturation pressure at `T_10`; energy balance
  `m·h_6 + m_cir·h_9 = m_cir·h_7 + m·h_10`; `m_cir = 10·m` (the `Ref(dr_su, 10, 0)` of the test).
- **Heat exchangers** (`HeatExchanger`): energy balance, smoothed LMTD (`LMTD_smoothed`, `CSL-0137`); design: `UA = Q/LMTD`
  with the specified terminal difference or outlet state; off-design: `Q = UA_d · f_UA · LMTD`, `f_UA = 2/(1/f₁ + 1/f₂)`,
  `f_i` = characteristic line of the relative mass flow `m/m_d` of the inlet of side i (`UA_char`).
- **Pressure drops**: design: specified (`Ref`/`pr`); off-design: `Δp = (ζ/D⁴)·8·m²·(v_in+v_out)/2/π²` with ζ/D⁴ from the design
  point (`zeta1_d4`, `zeta2_d4`); the evaporator and the condenser refrigerant side keep their fixed ratios, as in the test.
- **Compressors and pumps**: `(h_out − h_in)·η_s,d·f(m/m_d) = h_out,s − h_in` (`eta_s_char`); design `f = 1`.
- **Superheater water side**: flat UA line (`UA_char1` = 1), refrigerant side line D.
- **Characteristic lines** (`-char.csv`, table `char`): evaluated by `INTERPOLATE` (linear, as TESPy `CharLine`). TESPy holds
  the end value outside the table, CoolSolve extrapolates linearly: the argument is limited with `MIN(·, x_max)` (it is
  active for the condenser water flow and the recirculation pump, whose flow ratio reaches 2.7 in the matrix for tables ending
  at 2.5 and 1.25: e.g. `f_rp_o` = 0.7614 at the baseline point, ratio 1.63).
- Water loop (consumer, recirculation pump): the consumer has no pressure drop and closes the loop; the pump equation fixes the
  consumer outlet enthalpy; the recirculation pump work (0.30 W design, 1.70 W baseline) does not enter the COP.

| Main inputs | Value |
|---|---|
| `p_4`, `p_2`, `T_10`, `circ`, `dTsc_d`, `dTsh_d` | 60 bar, 15 bar, 5 °C, 10, 5 K, 5 K |
| `T_sink_d`, `M_dot_11_d` | 105 °C, 20 kg/s |
| `T_sink_o`, `M_dot_11_o` (off-design point) | 90 °C, 25 kg/s (baseline `.sol`) |

## How to run

```bash
coolsolve ./heat_pump_nh3_two_stage_flooded.eescode
```

The `.initials` (the design solution used as guess for both cases) is needed: without it the large off-design block
(69 unknowns) fails with a singular Jacobian. To compute another off-design point change `T_sink_o` and `M_dot_11_o`; all 20 points
of the Ebsilon matrix converge from the shipped `.initials`. The COP matrix below was produced by running the file once per
point (script of the verification, not shipped). The state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1…7) give the refrigerant main loop
of the design case for the CoolSolve diagrams.

## Results

Design (case d) and off-design baseline (90 °C, 25 kg/s, case o):

| Quantity | Design | Off-design 90 °C / 25 kg/s |
|---|---:|---:|
| Condenser duty `Q_dot_cd` | 224.98 kW | 243.70 kW |
| Compressor 1 / 2 power | 40.65 / 54.35 kW | 40.86 / 54.66 kW |
| COP | 2.3683 | 2.5512 |
| Evaporator / superheater / intercooler duty | 164.95 / 2.79 / 37.75 kW | 183.21 / 2.80 / 37.84 kW |
| NH₃ mass flow (vapour) / pump flow | 0.2082 / 2.082 kg/s | 0.2103 / 2.103 kg/s |
| Quality after the valve / evaporator outlet | 0.363 / 0.0637 | 0.300 / 0.0700 |
| Sink water flow | 1.191 kg/s | 1.938 kg/s |
| UA condenser / evaporator / superheater / intercooler | 4 697 / 27 820 / 665 / 864 W/K | design values, factor f_UA 1.193 / 1.087 / 1.002 / 1.003 |

| State | m [kg/s] | p [bar] | T [°C] | h [kJ/kg] | State | m [kg/s] | p [bar] | T [°C] | h [kJ/kg] |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.2082 | 5.1056 | 9.73 | 1626.01 | 10 | 0.2082 | 5.1556 | 5.00 | 1612.63 |
| 2 | 0.2082 | 15.0000 | 103.13 | 1821.26 | 11 | 20 | 1.0000 | 12.00 | 50.50 |
| 3 | 0.2082 | 14.9900 | 40.00 | 1639.92 | 12 | 20 | 0.9990 | 11.97 | 50.37 |
| 4 | 0.2082 | 60.0000 | 171.92 | 1900.96 | 13 | 20 | 0.9990 | 10.00 | 42.12 |
| 5 | 0.2082 | 59.9900 | 92.88 | 820.33 | 14 | 5 | 1.0000 | 20.00 | 84.01 |
| 6 | 0.2082 | 5.1556 | 5.00 | 820.33 | 15 | 5 | 0.9980 | 21.80 | 91.56 |
| 7 | 2.0819 | 5.1556 | 5.00 | 368.85 | 16 | 1.191 | 9.9980 | 60.00 | 252.00 |
| 8 | 2.0819 | 5.1608 | 5.00 | 368.85 | 17 | 1.191 | 10.0000 | 60.00 | 252.00 |
| 9 | 2.0819 | 5.1556 | 5.00 | 448.08 | 18 | 1.191 | 9.9980 | 105.00 | 440.92 |

(design case; the off-design states are in the `.sol`, suffix `_o`). Compressor 1 raises the pressure by a factor 2.94
(5.11 → 15.0 bar), compressor 2 by 4.00 (14.99 → 60.0 bar); the refrigerant leaves compressor 2 at 172 °C and is desuperheated,
condensed and subcooled by 5 K (92.9 °C) in the condenser.

**COP matrix** (CoolSolve = TESPy to ≤ 2.0e-9 relative; Ebsilon: reference values of the test):

| T_sink [°C] | m_source [kg/s] | COP CoolSolve | COP TESPy | COP Ebsilon | CoolSolve vs Ebsilon |
|---:|---:|---:|---:|---:|---:|
| 105 | 23 | 2.4160 | 2.4160 | 2.436 | −0.82 % |
| 105 | 22 | 2.4009 | 2.4009 | 2.414 | −0.54 % |
| 105 | 20 | 2.3683 | 2.3683 | 2.368 | +0.01 % |
| 105 | 18 | 2.3598 | 2.3598 | 2.338 | +0.93 % |
| 105 | 16 | 2.3430 | 2.3430 | 2.287 | +2.45 % |
| 100 | 27 | 2.5147 | 2.5147 | 2.591 | −2.94 % |
| 100 | 24 | 2.4724 | 2.4724 | 2.523 | −2.00 % |
| 100 | 20 | 2.4271 | 2.4271 | 2.448 | −0.85 % |
| 100 | 16 | 2.3946 | 2.3946 | 2.355 | +1.68 % |
| 100 | 12 | 2.3359 | 2.3359 | 2.216 | +5.41 % |
| 90 | 31 | 2.6352 | 2.6352 | 2.777 | −5.11 % |
| 90 | 25 | 2.5512 | 2.5512 | 2.635 | −3.18 % |
| 90 | 20 | 2.5201 | 2.5201 | 2.557 | −1.44 % |
| 90 | 15 | 2.4700 | 2.4700 | 2.442 | +1.14 % |
| 90 | 10 | 2.3832 | 2.3832 | 2.243 | +6.25 % |
| 80 | 33 | 2.7059 | 2.7059 | 2.866 | −5.59 % |
| 80 | 26 | 2.6249 | 2.6249 | 2.711 | −3.18 % |
| 80 | 20 | 2.5888 | 2.5888 | 2.629 | −1.53 % |
| 80 | 15 | 2.5389 | 2.5389 | 2.528 | +0.43 % |
| 80 | 10 | 2.4558 | 2.4558 | 2.351 | +4.46 % |

The COP rises when the sink temperature drops and when the source flow rises (at 80 °C: 2.456 at 10 kg/s, 2.706 at 33 kg/s;
at 105 °C: 2.343 at 16 kg/s, 2.416 at 23 kg/s).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the NH3 main loop (design case, arrays P[i], h[i]),
     figures/heat_pump_nh3_two_stage_flooded_ph.png -->

## Verification

1. **Re-run of the TESPy test.** `tests/test_models/test_heat_pump_model.py` (commit `19425523`) was run in a throw-away virtual
   environment (`pip install` of the local clone, Python 3.12.3, TESPy 0.11.3.dev0, CoolProp 8.0.0): the test passes (1 passed),
   and a script built on the test's own `setup_method` saved every connection and component result for the design point and
   for the 20 off-design points. CoolSolve embeds CoolProp 8.1.0dev (`coolsolve --version`).
2. **Design and baseline point, `tools/compare_solution.py`** (`--rtol 1e-6`, reference CSV written from the TESPy results with
   the names of this model: 18 states × (p, h, T), mass flows, powers, duties, UA, ζ/D⁴, LMTD, COP): *157 common variables, 0 differ
   (rtol=1e-06)*. The maximum relative difference is 4.0e-7 (`W_dot_pu_o`, the 2 W circulation-pump work, a difference
   of nearly equal enthalpies; the other pump powers 2.3e-7 to 3.0e-7); all other variables agree to 2.7e-9 or better (the absolute
   enthalpies of CoolProp's default reference state are identical on both sides). COP design: 2.368309474521 (CoolSolve)
   vs 2.368309474486 (TESPy).
3. **All 20 off-design points** (same script, CoolSolve run per point from the shipped `.initials`): COP agrees with TESPy to ≤ 2.0e-9
   relative; the maximum relative difference of any state p, h, T, m (18 states) is 2.6e-9 (h) / 2.2e-9 (m) / 9.5e-10 (T) /
   6.6e-11 (p) over the 20 points. The characteristic-line clamps are exercised (`f_rp_o` = 0.7614).
4. **Second reference, Ebsilon** (COP matrix of the test, 4 × 5 points): CoolSolve deviates from the Ebsilon COP by −5.59 % to
   +6.25 % (maximum 6.25 % at 90 °C / 10 kg/s; 0.01 % at the design point of the matrix, 105 °C / 20 kg/s); the TESPy deviations are
   the same figures, because CoolSolve = TESPy. The test accepts 7 % and notes that "not all ebsilon characteristics are available,
   thus perfect matching is not possible". The deviation pattern (negative at high source flow, positive at low flow) is that of
   the source test, not a feature of the translation.

## Source and attribution

Francesco Witte, **TESPy** — *Thermal Engineering Systems in Python* (Witte, F. and Tuschy, I., *TESPy: Thermal Engineering
Systems in Python*, Journal of Open Source Software 5 (49), 2178, 2020, doi 10.21105/joss.02178), <https://github.com/oemof/tespy>,
commit `19425523ff7ecd67b36e7b90efe04a9480a9ebe3`, MIT licence. Translated file:
[`tests/test_models/test_heat_pump_model.py`](https://github.com/oemof/tespy/blob/19425523ff7ecd67b36e7b90efe04a9480a9ebe3/tests/test_models/test_heat_pump_model.py)
("Test the operating points of the heat pump against a different model", file added in February 2019 by Francesco Witte, the
only author in the history of the file). The component equations (`HeatExchanger.UA_func/UA_char_func`, `zeta_d4_func`,
`Compressor/Pump.eta_s_char_func`, `smoothed_lmtd`) are those of TESPy `src/tespy/components` and `tools/characteristics.py`
at that commit. The characteristic-line values (compressor, pump, four UA sets) and the Ebsilon COP values are the arrays of
the test file, shipped as `heat_pump_nh3_two_stage_flooded-char.csv` and quoted in the table above; the Ebsilon model itself is
not available. Smoothed LMTD: S. Quoilin, PhD thesis, University of Liège, 2011 (see `CSL-0137`). Source path:
`~/git/tespy/tests/test_models/test_heat_pump_model.py` (inventory `TSP-052`; the TESPy tutorial `TSP-038`, same NH₃ two-stage
heat pump built step by step without reference results, is not translated separately). Translated and published under the
CoolSolve_Library MIT licence (decision D3), with credit to the authors of the original model.

## Conversion log

- **2026-10-31 — translation** (T-TRANSLATE, card C-361): TESPy network of 20 fluid connections (18 distinct states, two of them closed by cycle closers), 3 power connections and a power bus
  rewritten as simultaneous equations of two cases (design `_d`, off-design `_o`) in one file, solved together; the TESPy
  `design_path` becomes the shared design-point variables (`UA_*_d`, `zeta*_d`, `m_*_d`, `eta_s_d`). Pressure specified with
  `Ref(..., -x)` becomes `p − Δp`; `td_bubble`/`td_dew` become `T_sat ∓ ΔT`; `ttd_l` becomes `T_13 = T_8 + 5`.
- Units SI-°C-Pa-J; fluids `NH3` → `Ammonia`, `water` → `Water` (CoolProp HEOS, as TESPy). The power network (grid, bus, power
  connections) is the sum `W_dot_el = W_dot_cp1 + W_dot_cp2`.
- Equality of the drum pressure at the four connections is the single variable `p_dr`; the drum outlet quality constraints are `x = 0`
  (`h_7`) and `x = 1` (`h_10`, with `T_10` = 5 °C fixing the pressure, in both cases).
- The off-design water mass flow ratio of the intercooler is 1 (the flow is imposed); `f_ic2_o` is the table value at 1.
- Upper clamp of the characteristic line arguments with `MIN` (TESPy `CharLine` holds the end value; CoolSolve's `INTERPOLATE`
  extrapolates linearly). The lower end is not clamped: no ratio below 0.5 occurs in the matrix.
- `LMTD_smoothed` copied from `CSL-0137` (`$INCLUDE library:` not used, as in other models of the library).
- **Level**: equations 291 → 1, largest block 69 → 2, `FUNCTION` → 1, ≥ 3 coupled components → 1, off-design → 1, curated
  initials needed → 1: score 7 → level 4, lowered to 3: the size comes from solving the same machine twice (design + one operating
  point), nothing is calibrated and no discretisation is involved.

## Limitations and CoolSolve gaps

- One off-design operating point per run (the matrix is a series of runs); no `DUPLICATE` array over the 20 points.
- The off-design case needs the shipped `.initials`; the flat superheater UA line and the clamped lines are taken as in the test.
- No CoolSolve gap or bug was found; no `missing_features`.

## Related models

- `CSL-0250` *cascade_heat_pump_geothermal_dh*: TESPy cascade of two single-stage loops (ammonia variant), sectioned pinch-sized
  exchangers, design only; no drum, no circulation pump, no off-design.
- `CSL-0013` *heat_pump_basic_tespy*: the single-stage TESPy tutorial heat pump on R134a.
- `CSL-0133` *heat_pump_propane_pinch*: single-stage propane heat pump with pinch-sized exchangers.
- `CSL-0145` *refrigeration_co2_transcritical_booster*: CO₂ booster system with a receiver, from the TESPy model library.
- `CSL-0137` *hx_lmtd_ua*: the TESPy `HeatExchanger` UA/characteristic-line component, source of `LMTD_smoothed`.
- `CSL-0135` *turbine_stodola_offdesign*: the TESPy efficiency characteristic line pattern for a turbine.
- See also `CSL-0125` *pump_curve_similarity* and `CSL-0157` *reciprocating_catalogue_r717* (pump curves; NH₃ compressor catalogue
  model) as single-component models.
