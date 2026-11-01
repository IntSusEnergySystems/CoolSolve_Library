# Water electrolyser and H2/O2 fuel cell

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0323`

The two directions of the hydrogen electrochemical reaction, H₂O → H₂ + ½ O₂ (electrolyser, power in) and H₂ + ½ O₂ → H₂O (fuel cell, power out), in one
file. Each device is a black box in the sense of TESPy: species flows fixed by the stoichiometry, an energy balance written with the formation enthalpy of
liquid water, a heat flow to a cooling-water stream, and an efficiency defined on the higher heating value of hydrogen. The file solves seven cases at once
(four electrolyser cases, three fuel-cell cases, among them a power → H₂ → power round trip) and adds LHV efficiencies, an independent check of the reaction
enthalpy and warnings for efficiencies beyond the reversible limit.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water, Hydrogen, Oxygen (real fluids); H2, O2, H2O (ideal-gas species, only for the heating-value check) |
| **Size** | 207 equations, largest block 4 |
| **Source** | TESPy `WaterElectrolyzer` and `FuelCell`, https://github.com/oemof/tespy, commit 19425523 |
| **Authors** | Francesco Witte, Benjamin W. Portner, Jorrit Wronski, Karim Shawky, matbock (names of the repository history of the two files) |
| **License** | MIT (TESPy original and library) |
| **CoolSolve** | v0.4.0@9768373: runs; verified against TESPy re-runs (see *Verification*) |

## Problem statement

An electrolyser splits feed water into hydrogen and oxygen; the electric power is the reaction enthalpy of the produced hydrogen divided by the efficiency, the
rest leaves as heat in a cooling-water stream. A fuel cell does the reverse: the electric power is the efficiency times the reaction enthalpy of the
consumed hydrogen, the rest is rejected to cooling water. The cases below are the examples of the TESPy docstrings and of `tests/test_components/test_reactors.py`.

## Model

Common to both devices (reference 25 °C and 1 bar, as in the original; liquid water, so the HHV of hydrogen):

- stoichiometry: $f_{O_2} = M_{O_2}/(M_{O_2}+2M_{H_2})$ is the mass fraction of oxygen in water, $\dot m_{O_2} = f_{O_2}\dot m_{H_2O}$,
  $\dot m_{H_2} = (1-f_{O_2})\dot m_{H_2O}$;
- $e_0 = -\Delta H_f(H_2O)/M_{H_2}$ = 141.87 MJ/kg of H₂ with $\Delta H_f = -286$ kJ/mol (the constant of the original);
- one reactor pressure for the feed (or product) water, O₂ and H₂; the two gases of the electrolyser leave at the same temperature;
- cooling water (pure water) takes the heat $\dot Q = \dot m_{cw}(h_{cw,out}-h_{cw,in})$; $p_{cw,out} = pr\,p_{cw,in}$.

Electrolyser (case index *i*), power input $P$:

$$P = -\dot m_w (h_w-h_{w,ref}) + \dot Q + \dot m_{O_2}(h_{O_2}-h_{O_2,ref}) + \dot m_{H_2}(h_{H_2}-h_{H_2,ref}+e_0),\qquad \eta\,P=\dot m_{H_2}e_0 .$$

Fuel cell (case index *j*), power output $P$ (positive):

$$P = \dot m_{H_2}(h_{H_2}-h_{H_2,ref}+e_0) + \dot m_{O_2}(h_{O_2}-h_{O_2,ref}) - \dot m_w (h_w-h_{w,ref}) - \dot Q,\qquad P=\eta\,\dot m_{H_2}e_0 .$$

Off-design of the electrolyser (case 2): efficiency $\eta = \eta_{design}\,f(\dot m_{H_2}/\dot m_{H_2,design})$ with the default characteristic of TESPy
(`data/char_lines.json`, 7 points, in `h2_electrolyzer_fuel_cell-eta_char.csv`; outside the table the end value is kept, as in TESPy, and the procedure
`eta_char_el` warns); the cooling-water pressure loss follows $\Delta p = (\zeta/D^4)\,4\dot m^2(v_{in}+v_{out})/\pi^2$ with $\zeta/D^4$ fixed at the design point.

Added to the original (not in TESPy): LHV efficiencies $\eta_{LHV}$ (electrolyser $\eta\,LHV/HHV$, fuel cell $\eta\,HHV/LHV$); LHV and HHV of hydrogen
computed from the CoolSolve species (ideal-gas H₂, O₂ and H₂O vapour at 25 °C; HHV = LHV + latent heat of water), compared with the constant of the original;
the reversible limits $\eta_{max} = \Delta H/\Delta G = 1.206$ (electrolyser) and $\Delta G/\Delta H = 0.829$ (fuel cell) on the HHV basis with the literature value
$\Delta G_f(H_2O,l) = -237.13$ kJ/mol; the procedures `check_electrolyser` and `check_fuel_cell` set flags and call `CALL WARNING` when an efficiency exceeds
them, when an electrolyser needs heat from outside ($\dot Q<0$) or when the fuel-cell power is not positive.

| Case | Specification (inputs) |
|---|---|
| EL 1 | docstring: 100 l/s of H₂ at 10 bar, 50 °C; feed water 15 °C; η = 0.8; cooling water 15 → 45 °C at 5 bar, pr = 0.99 |
| EL 2 | same plant at 0.2 P of case 1, η from the characteristic, ζ/D⁴ of case 1 |
| EL 3 | test: feed water 25 °C, 1 bar; H₂ 50 °C; η = 0.8; heat to cooling water 800 kW (cooling 20 → 45 °C) |
| EL 4 | test: all streams at 25 °C, η = 1, P = 2.5 MW (heat output must be 0) |
| FC 1 | docstring: P = 200 kW, η = 0.45, pr = 0.9, cooling water 25 → 40 °C, products at 50 °C, reactants 25 °C, 1 bar |
| FC 2 | test: 0.01 kg/s H₂, η = 0.45, pr = 0.98, cooling water 20 → 40 °C |
| FC 3 | round trip: H₂ flow, pressure (10 bar) and temperature (50 °C) of EL 1, η = 0.5 |

## How to run

```bash
coolsolve ./h2_electrolyzer_fuel_cell.eescode
```

The file needs its companion table `h2_electrolyzer_fuel_cell-eta_char.csv` and two guesses in `h2_electrolyzer_fuel_cell.initials` (`M_dot_cw_el[2]`,
`P_cwo_el[2]`; the implicit block of case 2 is singular from the default start). To study another operating point, change the closure lines of a case (for
example `eta_fc[2]`).

## Results

| Case | P | Heat to coolant | η (HHV) | η (LHV) | ṁ_H₂ [kg/s] | ṁ_O₂ [kg/s] | ṁ_water [kg/s] | ṁ_cooling [kg/s] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| EL 1 | 13.232 MW | 2.579 MW | 0.800 | 0.676 | 0.07461 | 0.59217 | 0.66678 | 20.57 |
| EL 2 | 2.646 MW | 0.397 MW | 0.845 | 0.714 | 0.01576 | 0.12505 | 0.14080 | 3.165 |
| EL 3 | 4.062 MW | 0.800 MW | 0.800 | 0.676 | 0.02290 | 0.18179 | 0.20469 | 7.655 |
| EL 4 | 2.500 MW | 0 (round-off) | 1.000 | 0.846 | 0.01762 | 0.13985 | 0.15748 | 0 |
| FC 1 | 200.0 kW | 241.5 kW | 0.450 | 0.532 | 0.003133 | 0.02486 | 0.02800 | 3.853 |
| FC 2 | 638.4 kW | 771.0 kW | 0.450 | 0.532 | 0.01000 | 0.07937 | 0.08937 | 9.221 |
| FC 3 | 5292.7 kW | 5262.1 kW | 0.500 | 0.591 | 0.07461 | 0.59217 | 0.66678 | 62.94 |

The specific energy consumption of EL 1 is 49.3 kWh/kg of H₂ (177.3 MJ/kg) at η = 0.8; at 20 % load (EL 2) the characteristic raises η to 0.845
(factor 1.0558) and lowers it to 46.7 kWh/kg. The round trip EL 1 → FC 3 has a power-to-power efficiency of 0.400 = 0.8 × 0.5 (HHV basis, `eta_rt`), with 7.84 MW of
heat to the two cooling waters. No warning is raised for the seven cases. The reference check gives $-286$ kJ/mol against 285.83 kJ/mol computed from the CoolSolve species
(deviation 6.0e-4) and LHV = 241.84 MJ/kmol, LHV/HHV = 0.8456. The file has no state-point arrays: the devices are not cycles.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): sweep of the part-load efficiency of the electrolyser,
     figures/h2_electrolyzer_fuel_cell_eta_load.png -->

## Verification

**Re-run of the TESPy examples** (`work/` venv, `pip install ~/git/tespy`, TESPy 0.11.3.dev0, CoolProp 8.0.0; the 4 tests of `tests/test_components/test_reactors.py` and the 2
doctests of the two modules pass). The networks of the table above were solved with TESPy (scripts `ref_tespy.py`, `ref_tespy_fcpatch.py` of the deleted work
folder: docstring electrolyser design and 20 % off-design, the electrolyser with η = 0.8 and Q = −800 kW, with η = 1 and P = 2.5 MW, the docstring fuel cell, the
test fuel cell and a round-trip fuel cell) and the 90 values (powers, heat, η, e, mass flows of all streams, the enthalpies of the streams, the cooling outlet
pressure) written to a `name,value` file compared with the `.sol`:

```
python3 CoolSolve/tools/compare_solution.py h2_electrolyzer_fuel_cell.sol tespy_reference.csv --rtol 1e-9
90 common variables, 0 differ (rtol=1e-09); only in EES: 0; only in CoolSolve: 118
```

At `--rtol 1e-10` 11 variables differ (largest 7.5e-10 relative, `Q_dot_cw_el[2]`); a purely relative comparison of all 90 values gives a
maximum of 1.7e-9 (`M_dot_O2_el[3]`), the Newton tolerance of CoolSolve; TESPy ran with CoolProp 8.0.0 and CoolSolve with CoolProp 8.1.0dev (revision 75af7816), and the fluid equations of state of water, hydrogen and oxygen give the same enthalpies to that precision. The docstring values of the electrolyser are reproduced:
P = 13.2 MW and η_off-design = 0.84. The fuel-cell docstring values (10.2 kg/s cooling water, Q = −642 kW) are reproduced by the unmodified TESPy re-run but not by this file, because the fuel-cell balance
is corrected (next paragraph). The eta = 1 case gives a heat output of −4.7e-10 W (TESPy: 1.8e-10 W; the test asks 0 within 1e-4).

**TESPy fuel-cell heat output violates the first law.** In `FuelCell.energy_balance_func` the residual is `P - calc_P()` with `calc_P` the delivered
power, whereas `P` is declared as power *output* with `max_val=0` (negative) and the power connector uses `E = -P`. The balance therefore describes a cell that
consumes the power it should deliver. With the docstring case (η = 0.45, 200 kW) the chemical power is 444.4 kW, yet TESPy returns a heat output of 641.5 kW
(= 444.4 kW + 200 kW − 2.9 kW sensible heat of the product water) besides the 200 kW of electricity: 841.5 kW out for 444.4 kW in. This file uses the first-law balance (power
output positive, heat = 241.5 kW). To verify the rest of the model, the TESPy fuel-cell cases were re-run with **one changed line** (`FuelCell.energy_balance_func` returning
`P + calc_P()`): heat output and cooling mass flow (FC 1: 241.5 kW, 3.853 kg/s) then agree with CoolSolve (rows `Q_dot_cw_fc`, `M_dot_cw_fc` of the 90 values); the quantities that do not depend on the sign
(P, η, e, the species flows, the product-water enthalpy) agree with the unmodified TESPy. Compared with the unmodified TESPy the CoolSolve heat output of the three fuel-cell cases is
smaller by the factor 0.376, 0.376 and 0.332 (FC 1, 2, 3). Because the TESPy fuel-cell test only checks the sign of `Q`, it does not see the problem. The electrolyser balance has no such inconsistency
(P positive input).

**Analytical checks.** (1) First law of the electrolyser cases is the balance itself; the electric power minus the heat to the cooling water minus the chemical power $\dot m_{H_2}e_0$ of EL 1 is 66.9 kW,
the sensible enthalpy of the streams relative to 25 °C (feed water at 15 °C, gases at 50 °C). (2) $e_0$ against the CoolSolve species: HHV = 285.83 kJ/mol against 286.0 kJ/mol of the
original (6.0e-4). (3) `eta_rt = eta_el[1]*eta_fc[3]` (0.4 on both sides): the round-trip efficiency is the product of the two HHV efficiencies for the same hydrogen flow.

**Guards.** Run with `eta_el[3] = 1.3` and `eta_fc[2] = 0.9` (copy in the work folder, deleted): CoolSolve prints the two reversible-limit warnings and sets `flag_2nd_el[3]` and `flag_2nd_fc[2]` to 1, the solution is otherwise unchanged.

Inputs not in the TESPy examples (`DG_f_H2O` and thus the reversible limits, the LHV from the species) have no TESPy reference: they only add checks.

## Niche

Nearest library models: `CSL-0139` *combustion_chamber* (TESPy, hydrogen only as one of the fuel components, burned in a chemical-heat release with no work), `CSL-0141`
*gas_turbine_open_cycle* (the same TESPy tutorial family, H₂ as optional fuel) and `CSL-0046` *octane_combustion_400pct_air* (first-law reaction of a fuel). They all
release the reaction enthalpy as heat of a flame. The library has no electrochemical converter: this model adds power-driven and power-producing reactions with a species balance, the
efficiency definition on HHV and LHV, the heat rejected to a coolant, part-load behaviour of the electrolyser from a characteristic line, and the power-to-power round trip; it is the building block
of a power-to-gas or hydrogen storage study. A search of `library.json` for electrolysis, fuel cell, Nernst, Gibbs, Faraday and power-to-gas finds no electrochemical model (the keyword hits are compressor models, `electromechanical`).

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented) of the components `WaterElectrolyzer` and `FuelCell` from TESPy, files
`src/tespy/components/reactors/water_electrolyzer.py` and `fuel_cell.py`, commit 19425523ff7ecd67b36e7b90efe04a9480a9ebe3.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff / version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve; both devices and seven cases in one file; the connections, design/off-design switches and Newton solver of TESPy are replaced by simultaneous
equations with the specifications of the docstring examples; the sign of the power in the fuel-cell energy balance is corrected (first law); LHV efficiencies, heating-value check, reversible-limit
flags and warnings added; the compressor of the electrolyser docstring is not modelled (only the electrolyser outlet state is used).
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in Python", J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
Scientific basis: the formation enthalpy of liquid water (−286 kJ/mol), the characteristic line of `data/char_lines.json` (TESPy default; no publication given in the source) and, for the added checks,
ΔG_f(H₂O, l) = −237.13 kJ/mol (NIST/CODATA value).

Authors found in the repository history of the two files: Francesco Witte (86 and 62 commits), Benjamin W. Portner (6), Jorrit Wronski (3 and 3), Karim Shawky (1) for the electrolyser file; matbock (7, a
GitHub handle) for the fuel-cell file.

## Conversion log

- **2026-10-31 — T-TRANSLATE** (card C-443, rows TSP-024 and TSP-025 of `sources/tespy/inventory.csv`, one model for both devices): each TESPy equation (mass flows, cooling mass and fluid equality,
  energy balance, pressure equalities, gas-temperature equality, `eta`, `e`, `Q`, `pr`, `eta_char`, `zeta_d4`) becomes a plain equation; the cases are written with `DUPLICATE` over the case index (`_el[i]`, `_fc[j]`).
- TESPy `H2`, `O2`, `H2O` (CoolProp fluids `Hydrogen`, `Oxygen`, `Water`) become the EES real-fluid names `Hydrogen`, `Oxygen`, `Water`; the chemical formulas `H2`, `O2`, `H2O` (ideal-gas substances) are used only for the heating-value check.
- Sign conventions: TESPy `P` of the fuel cell is negative, here `P_fc` is positive; TESPy `Q` of both devices is negative when the coolant is heated, here `Q_dot_cw_*` is positive. TESPy `h_ref` is
  `enthalpy(fluid,T=25,P=1E5)` of each species, as in the original.
- **Correction**: the sign of `P` in the fuel-cell energy balance (first law), see *Verification*; this changes the fuel-cell heat output and cooling flow, not the species flows or the power.
- Not translated: the compressor of the docstring, the power connection (`energy_connector_balance`), the design/off-design bookkeeping (the off-design of case 2 uses the design point of case 1 through the
  two quantities it needs: `M_dot_H2_el[1]`, `eta_el[1]`, `zeta_d4_el`), the `e` and `Q` specifications of the electrolyser other than as closure of the cases, the optional `dp`/`zeta` specifications.
- The relative hydrogen flow of the characteristic is clamped to the table range and flagged (TESPy also keeps the end value); warnings use `CALL WARNING` (a procedure writes the flag), which is valid EES.
- Initial values: two guesses for the implicit block of case 2.
- **Level**: score of docs/taxonomy.md §3: equations 207 (1) + largest block 4 (0) + procedures/DUPLICATE (1) + coupled components (0) + off-design (1) + curated guesses (1) = 4 → level 3, moved to level 2 because
  all balances are explicit algebraic relations and only one block needs a guess.

## Limitations and CoolSolve gaps

No CoolSolve gap. Physical limits: efficiencies are inputs or come from a single characteristic line (no polarisation curve, no voltage, no degradation); the reaction enthalpy is the constant of the original
(25 °C, liquid water) and the other temperatures enter through the sensible enthalpies of the real-fluid properties; the water streams are liquid (feed water of the electrolyser, product water of the fuel
cell), which the file does not check against the saturation pressure at the product temperature (an EES `x` or `Phase$` check would be needed); the energy balance has no heat loss to the environment (all
heat goes to the cooling water). The fuel-cell heat is that of the corrected balance, not the one of TESPy at this commit.

## Related models

- `CSL-0139` *combustion_chamber*: combustion of CH₄ blended with H₂ in a TESPy chamber, the thermal route from the same fuel; this model is the electrochemical one.
- `CSL-0141` *gas_turbine_open_cycle*: TESPy gas-turbine tutorial that can burn H₂; with this model it brackets power-to-hydrogen-to-power routes.
