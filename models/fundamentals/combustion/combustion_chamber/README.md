# Generic combustion chamber (TESPy `CombustionChamber`)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0139`

A steady-flow combustion chamber translated from the
[TESPy](https://github.com/oemof/tespy) component `CombustionChamber`
(commit `19425523`): fuel (methane, optionally diluted with CO₂ and blended
with hydrogen) and air enter, the flue gas leaves. The model applies the
mandatory equations of the source — mass balance, pressure equality, **one
stoichiometry equation per fluid** and the energy balance on the lower
heating value — and returns the fuel flow, the flue-gas composition and the
flue-gas temperature for a given air flow and **excess-air ratio λ**
(available oxygen / stoichiometric oxygen). The pressure ratio `pr` and the
heat dissipation ratio `eta` of TESPy's `DiabaticCombustionChamber` are
inputs as well (`eta = 1`, `pr = 1`: the adiabatic chamber). This is the
building block of the gas-turbine, CHP and burner models of the library.

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | CH4, CO2, H2O, O2, N2, Ar, H2 (ideal gases) |
| **Size** | 81 equations, all explicit (largest block: 1) |
| **Source** | TESPy `src/tespy/components/combustion/base.py` (+ `diabatic.py`), commit `19425523`, companion tests `tests/test_components/test_combustion.py` and `tests/test_models/test_CGAM_model.py` |
| **Authors** | Francesco Witte (TESPy lead developer) and the TESPy contributors |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; verified against TESPy (5 cases, max. deviation 2.0E-04) |

## Problem statement

Methane (or a methane/hydrogen/CO₂ blend) is burned in a chamber at ambient
temperature with a given air flow. Given the excess-air ratio λ, determine the
fuel mass flow, the flue-gas mass (and molar) fractions and the flue-gas
temperature. Conversely, given a thermal input and the flue-gas temperature,
determine the air flow and λ (the *thermal-input specification* of TESPy).

## Model

Assumptions, all those of the source: steady state, one pressure in the
adiabatic chamber (the ideal-gas enthalpies do not depend on it), complete
combustion (no CO, no unburned fuel), no dissociation, water vapour in the
flue gas (lower heating value basis), ideal-gas species with the
**formation enthalpy included** in their enthalpy (as in EES and in CoolSolve),
reference state 25 °C / 1 bar for the energy balance, no heat loss
(`eta = 1`) and no pressure drop (`pr = 1`) unless stated otherwise.

State points and equations (TESPy connection labels in brackets):

- **Molar masses and formation enthalpies** `MM_i = MolarMass(i)` for the
  seven species; `LHV_fuel(n_C, n_H, n_O, hf_fuel, hf_CO2, hf_H2O, hf_O2, MM_fuel)`
  is a `FUNCTION` of this file (the lower heating value of a C/H/O fuel,
  `LHV = -(Σ_i ΔHf_i - Σ_j ΔHf_j)/M_fuel`, as TESPy's
  `CombustionChamber.calc_lhv`), called for CH₄ and H₂ with the formation
  enthalpies of the source (CODATA 1989: CO₂ −393.51, H₂O(g) −241.826,
  O₂ 0 kJ/mol; CH₄ −74.6 kJ/mol from TESPy's `COMBUSTION_FLUIDS`).
- **Stoichiometry** [TESPy `stoichiometry_func`]: molar flows of the fuel
  species, `n_dot_O2_stoich = ν_O2·m_dot_fuel` with the oxygen demand per kg
  of fuel `ν_O2 = x_CH4·(n_C + n_H/4 − n_O/2)/MM_CH4 + x_H2·0.5/MM_H2`, and
  the specification
  `m_dot_fuel = n_dot_O2_air/(λ·ν_O2)` with
  `n_dot_O2_air = m_dot_air·x_air_O2/MM_O2`.
  `lambda_calc` recomputes λ from the flows (equal to `lambda` in this mode).
- **Species balances** (complete combustion): N₂ and Ar pass through, the
  CO₂ of the air and of the fuel diluent passes through, the C atoms of the
  fuel go to CO₂ (`n_dot_C·MM_CO2`), the H atoms to H₂O
  (`n_dot_H/2·MM_H2O`), the oxygen left over is the excess air
  (`m_dot_air·x_air_O2 − n_dot_O2_stoich·MM_O2`); `m_dot_CH4_fg = 0`,
  `m_dot_H2_fg = 0`; mass balance `m_dot_fg = m_dot_air + m_dot_fuel`.
  (TESPy writes the oxygen balance as `n_O2,out = n_O2,in − n_O2,in/λ`;
  with `λ = n_O2,in/n_O2,stoich` this is the same relation.)
- **Pressure** `p_fg = pr·p_air`, `p_fuel = p_air` (the pressure-equality
  constraints `p_in1 = p_in2 = p_out` of the adiabatic chamber; with `pr = 1`
  all three are equal).
- **Energy balance** (TESPy `energy_balance_func`, LHV basis):
  `Σ_in ṁ(h − h_ref) − ṁ_fg(h_fg − h_fg,ref) + η·ṁ_fuel·LHV = 0`, written as
  `Q_dot_reactants = Q_dot_flue` (the mixture enthalpies `h`, `h_ref` are the
  mass-weighted sums of the ideal-gas species enthalpies — TESPy's
  `mixing_rule="forced-gas"`). `T_fg` is the unknown of that equation;
  `Q_loss = −(1 − η)·ti` is TESPy's `Qloss`.

Outputs: `m_dot_fuel`, `ti`, `Q_loss`, `T_fg` (°C) and `T_fg_K` (K), `p_fg`,
the flue-gas mass fractions `x_fg_*` and molar fractions `y_fg_*`
(N₂, O₂, Ar, CO₂, H₂O, H₂, CH₄), `n_dot_fg`, `MM_fg`.

| Inputs | Base value | Outputs (base case) | Value |
|---|---|---|---|
| `m_dot_air` air flow | 1 kg/s | `T_fg` flue-gas temperature | 1836.8 °C (2109.97 K) |
| `lambda` excess-air ratio | 1 | `m_dot_fuel` fuel flow | 0.050136 kg/s |
| `T_air` / `T_fuel` inlet temperatures | 30 / 30 °C | `ti` thermal input | 2.508 MW |
| `p_air` chamber pressure | 100 kPa | `x_fg_CO2` / `x_fg_H2O` | 0.1310 / 0.1072 |
| air composition (N₂/O₂ mass fractions) | 0.8 / 0.2 | `x_fg_O2` (λ = 1) | ≈ 0 |
| `pr`, `eta` | 1, 1 | `MM_fg` mean molar mass | 27.68 kg/kmol |

Base case = TESPy `test_CombustionChamberHighTemperature` (CH₄ in air
N₂/O₂ = 0.8/0.2, 1 kg/s of air, 30 °C, 1 bar, λ = 1).

## How to run

```bash
coolsolve ./combustion_chamber.eescode
```

No `.initials` or `coolsolve.conf` needed: all 81 equations are explicit and
the system solves directly from the default guesses. The other cases of the
source are obtained by changing the input block (air composition, λ, `pr`,
`eta`, …).

### Thermal-input specification (`ti` mode)

The source also allows the thermal input to be specified (with the flue-gas
temperature or the air flow). The same physics is obtained with **five line
edits**, without touching any other equation (`lambda_calc` then reports λ):

1. delete the input line of `m_dot_air` — the air flow becomes an unknown,
   determined by the energy balance;
2. delete the input line of `lambda` — λ becomes the output `lambda_calc`;
3. replace `m_dot_fuel = n_dot_O2_air/(lambda*nu_O2)` by
   `m_dot_fuel = ti/LHV_fuel`;
4. replace `ti = m_dot_fuel*LHV_fuel` by the value of `ti`;
5. replace `T_fg_K = T_fg + 273.15` by the value of `T_fg`.

The system stays square (79 equations, 79 unknowns with steps 1–5 and the base
inputs, `coolsolve -d`). This mode is what the source uses when `ti` and the flue-gas
temperature are given (cases D and E of *Verification*).

## Results

Base case (`combustion_chamber.sol`, 81 equations, all explicit):

| Variable | Value |
|---|---|
| `m_dot_fuel` | 5.0135630E-02 kg/s |
| `ti` | 2.5081003E+06 W |
| `T_fg` / `T_fg_K` | 1836.815 °C / 2109.965 K |
| `m_dot_fg` | 1.0501356 kg/s |
| `x_fg_N2`, `x_fg_O2`, `x_fg_Ar` | 0.761806, 1.1E-15, 0 |
| `x_fg_CO2`, `x_fg_H2O`, `x_fg_CH4` | 0.130970, 0.107224, 0 |
| `LHV_CH4`, `LHV_H2` | 5.0026305E+07, 1.1996051E+08 J/kg |
| `MM_fg` | 27.684 kg/kmol |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep of the flue-gas temperature against lambda, or composition plot -->

## Verification

Reference: the **TESPy model itself** (local snapshot `~/git/tespy`, commit
`19425523`, installed in a throw-away virtual environment under `work/` with
its own dependencies — Python 3.12, CoolProp 8.0.0, TESPy 0.11.3.dev0). Two
scripts were used: `run_tespy.py` (the five chamber cases, written as the
component doctests and tests of `tests/test_components/test_combustion.py`)
and `run_cgam.py` (the full CGAM gas-turbine model of
`tests/test_models/test_CGAM_model.py`, whose combustion chamber is compared
to `tests/test_models/cgam-ebsilon-results.csv`). Their printed results were
written to `tespy_results.csv` / `cgam_tespy.json`; the script
`verify.py` then writes one parameter variant of `combustion_chamber.eescode`
per case, runs `coolsolve` on it and compares the outputs.

The base case was also compared with the CoolSolve tool
`tools/compare_solution.py` (reference `tespy_case_A.csv`, the TESPy values
renamed to the variable names of the model):

```text
15 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 66
```

**Maximum relative deviation over the 15 common variables: 9.74E-06**
(`T_fg_K`, 2109.965 K against 2109.986 K); every other variable is below
1.6E-13, except `x_fg_O2`, where the absolute value is 1.1E-15 (λ = 1 → no
excess oxygen, as TESPy's `test_CombustionChamber` asserts).

| Case | Specification (TESPy) | Variable | CoolSolve | TESPy | rel. dev. |
|---|---|---|---|---|---|
| **A** `test_CombustionChamberHighTemperature` | λ = 1, 1 kg/s air, air N₂/O₂ 0.8/0.2, 30 °C | `T_fg_K` | 2109.965 K | 2109.986 K | 9.7E-06 |
| | | `m_dot_fuel`, `m_dot_fg`, `ti` | 0.0501356, 1.0501356, 2.5081003E6 | same to 13 digits | 1.6E-13 |
| | | `x_fg_N2`, `x_fg_CO2`, `x_fg_H2O` | 0.761806, 0.130970, 0.107224 | same to 13 digits | 8.0E-14 |
| **B** `test_CombustionChamber` step 2 | λ = 1, air N₂/O₂/Ar 0.7556/0.2315/0.0129, fuel 4 % CO₂ | `T_fg_K` | 2328.555 K | 2328.579 K | 1.0E-05 |
| | | `x_fg_O2` | 3.3E-15 | 0 (asserted `== 0`) | – |
| | | composition, flows | – | – | ≤ 3.1E-13 |
| **C** CGAM chamber (`cgam-ebsilon-results.csv` state 4) | `pr = 0.95`, `eta = 0.98`, air 850 K / 9.6235 bar (humid), λ = 3.18388 | `T_fg_K` | 1520.306 K | 1520.000 K | 2.0E-04 |
| | | `m_dot_fuel` | 1.6466230 kg/s | 1.6466230 kg/s | 2.8E-08 |
| | | `m_dot_fg`, `p_fg` | 92.586079 kg/s, 9.142325 bar | 92.586079, 9.142325 | 5.0E-10 |
| | | `y_fg_N2`, `y_fg_O2`, `y_fg_CO2`, `y_fg_H2O` | 0.7505317, 0.1368069, 0.03161261, 0.08104876 | 0.7505317, 0.1368069, 0.03161256, 0.08104880 | 1.7E-06 |
| **D** `test_CombustionChamber` step 1 (`ti` mode) | `ti` = 1 MW, `T_fg` = 1200 °C, fuel 4 % CO₂ | `lambda_calc` | 2.022364 | 2.022487 | 6.1E-05 |
| | | `m_dot_air`, `m_dot_fg` | 0.6966159, 0.7174382 | 0.6966583, 0.7174807 | 6.1E-05 |
| **E** `CombustionChamber` docstring (`ti` mode) | `ti` = 500 kW, `T_fg` = 1200 °C, fuel 3 % CO₂ / 1 % H₂ / 96 % CH₄, humid air | `lambda_calc` | 2.013446 (**2.013**, the documented 2.014) | 2.013572 | 6.3E-05 |
| | | `m_dot_air`, composition | 0.3454820 | 0.3455037 | 6.3E-05 |

Maximum relative deviation over the five cases: **2.0E-04** (case C,
`T_fg_K`), and 6.4E-05 for the four component cases.

Deviations above 1E-13 have a single cause: the two tools do not use exactly
the same ideal-gas enthalpy data (CoolSolve uses the NASA-Glenn polynomials
of its ideal-gas species, see `src/fluids.cpp`, TESPy the CoolProp
`HEOS`/ideal-gas fits of CoolProp 8.0.0); the temperature that follows from
the energy balance is the only output that shows it, at the 1E-05 … 1E-04
level. The absolute formation enthalpies of the species agree: the
`LHV_CH4` of the model (5.002630463510E+07 J/kg) is identical to the LHV
TESPy computes from the same `COMBUSTION_FLUIDS` data, and the composition,
the fuel flow and the thermal input (which do not depend on the enthalpy
functions) agree with TESPy to 1E-13.

Against the **Ebsilon** reference table of the CGAM benchmark
(`cgam-ebsilon-results.csv`, state 4 — the composition columns of that file
are **molar** fractions, as the TESPy test converts them), the maximum
relative deviation is 1.4E-03 (`m_dot_fuel` 1.6466230 against 1.6443204 kg/s,
i.e. 0.14 %; TESPy's own full-model run deviates from the same table by
0.13 %, the accepted tolerance of `test_CGAM_model.py::test_ebsilon` being
0.5 %).

Case C prescribes the air flow and λ of the TESPy run of the full CGAM model
(the upstream compressor and turbine power balance fixes them); the five
checked outputs (flue-gas temperature, fuel flow, flue-gas flow, flue-gas
pressure and the four molar fractions) are free results of this model. Its
0.3 K on `T_fg` is the same enthalpy-data effect as in cases A and B, larger
because the air enters the chamber at 850 K instead of near the reference
temperature: the enthalpy rise of the reactants then carries 39 % of the
energy balance (`m_dot_air·(h_air − h_air,ref)` = 52 MW of the 134 MW of
`Q_dot_reactants`), so a 1E-05 relative difference in the ideal-gas
enthalpies moves the flue-gas temperature by 0.3 K.

## Source and attribution

```text
This CoolSolve model is a translation (EES-compatible language, equation-oriented) of
CombustionChamber and DiabaticCombustionChamber from TESPy, file
src/tespy/components/combustion/base.py and src/tespy/components/combustion/diabatic.py,
commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff / version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve, the fuel is restricted to CH4/CO2/H2, the
stoichiometry is written out species by species, the NO formation (f_nox) is left out.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in Python",
J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
Scientific basis: the molar formation enthalpies are the CODATA 1989 values of the source
(CombustionGases / calc_lhv in src/tespy/tools/global_vars.py and combustion/base.py).
```

Reference values used for the verification: the doctests of the component and
of `tests/test_components/test_combustion.py` (TESPy), and the Ebsilon
result table `tests/test_models/cgam-ebsilon-results.csv` (CGAM benchmark).

## Conversion log

- **2026-10-13 — translation (T-TRANSLATE, card C-184, inventory row TSP-022)**:
  the Python solver plumbing (network, connections, `Connection.m/p/h`, the
  `design`/`offdesign` switches, the `combustion_pressure_structure_matrix`)
  becomes plain simultaneous equations; the variable names of the source are
  kept (`ti`, `lamb` → `lambda`, `lamb`-based `pr`, `eta`, `Qloss`, `m`, `p`,
  `T`, `x`, the species names). The species balances, written once per fluid
  in the source, are written out as one line per species of the flue gas.
  `n_dot_O2_stoich`, `n_dot_O2_air`, `lambda_calc`, `x_fg_*`, `y_fg_*`,
  `MM_fg`, `LHV_*`, `Q_dot_reactants`, `Q_dot_flue`, `T_fg_K` are named
  outputs of the translation. The network objects and the specification
  switches do not exist in EES: the λ specification of the shipped file is the
  default one, the `ti` one is the documented five-line edit above (Cases D
  and E of *Verification* use it).
- **2026-10-13 — `lambda`**: TESPy computes λ when it is not set and imposes
  `m_O2/fuel·(n_C + n_H/4) = λ` when it is; in EES a variable has exactly one
  equation, so λ is an input and the fuel flow follows from
  `m_dot_fuel = n_dot_O2_air/(λ·ν_O2)`; `lambda_calc` reports the ratio
  recomputed from the flows (`λ` in the source's `calc` parameters).
- **2026-10-13 — energy balance**: written as `Q_dot_reactants = Q_dot_flue`
  (the pattern of `CSL-0046`): an unknown that only appears inside property
  calls (`T_fg`) is closed by that equation; a residual written as
  `expression = 0` would be a check equation in CoolSolve. `T_fg_K` carries
  the equation of `T_fg` (it is the temperature unit TESPy prints).
- **2026-10-13 — fuel**: the source is generic (any C/H/O mixture of
  `COMBUSTION_FLUIDS`). This translation fixes the combustible to CH₄ (with
  H₂ as a blend and CO₂ as a diluent), which is the fuel of the CGAM
  benchmark and of the two chamber tests; `n_C_fuel`, `n_H_fuel`, `n_O_fuel`
  are the atom counts of CH₄ used by the LHV function and by the oxygen
  demand. No gas turbine or burner in the library needs another fuel today
  (`CSL-0152` builds the composition from the elemental analysis).
- **2026-10-13 — not modelled** (out of scope of the card, documented in
  *Limitations*): NO formation (`f_nox`, needs the Pyromat back end and the
  `NO` species, `CS-GAP-FLUIDS-NASA-SPECIES`), air deficiency (λ < 1, the
  branch that returns the unburned fuel of the source), the convective
  `convergence_check` of TESPy (a solver aid, no equation).
- **Level**: taxonomy §3 score 2 → level 2: 81 equations (1), largest block 1
  (0), one `FUNCTION` (1), no multi-zone (0), no off-design (0), solves
  without curated guesses (0) = 2 → level 2. One level above the teaching
  models because the model is a reusable building block with seven species
  and two specification modes rather than a single numerical exercise.

## Limitations and CoolSolve gaps

- Complete combustion only: no CO, no soot, no unburned fuel, no
  dissociation (the source returns unburned fuel and products below λ = 1 and
  the library model `CSL-0150` covers dissociation).
- No NO formation (`f_nox`): the species `NO` is not a CoolSolve fluid
  (`CS-GAP-FLUIDS-NASA-SPECIES`), and the source needs the Pyromat back end
  for it.
- Ideal-gas species only (as the source); a real-fluid pressure effect on the
  flue-gas enthalpy (`CSL-0046` shows it at 3.9 % on H₂O) is not modelled, so
  the pressure of the chamber only appears through `pr`.
- No gap blocks the file: `missing_features` is empty, and nothing had to be
  rewritten around a CoolSolve limitation (the file uses EES syntax only).

## Related models

- `CSL-0046` *octane_combustion_400pct_air*: the same first-law reaction
  written with constant `Cp` chemistry for a single fuel and λ = 4; this
  model is the species-resolved, general version.
- `CSL-0150` *adiabatic_flame_dissociation*: adiabatic flame temperature of
  CH₄ or fuel oil with chemical equilibrium (14 species, blocked by
  `CS-GAP-CHEM-EQUIL`); the dissociation this model ignores.
- `CSL-0005` *cpbar_combustion_products*: mean specific heat of the products
  of a CmHn fuel (`f`-based, simplified air), the other route to combustion
  properties.
- `CSL-0058` *diesel_engine_excess_air_exhaust_analysis*: the same
  fuel/air stoichiometry read backwards, from an exhaust-gas analysis.
- `CSL-0013` *heat_pump_basic_tespy*: the other translated TESPy model (the
  pilot of this kind of card).