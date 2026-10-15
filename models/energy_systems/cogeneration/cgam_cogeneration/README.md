# CGAM cogeneration benchmark (gas turbine + HRSG)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0146`

The CGAM cogeneration problem (Valero et al., 1994), the classic exergy-analysis
benchmark, as built in the TESPy test suite: a gas turbine (compressor with
pressure ratio 10, diabatic combustion chamber on methane, turbine with TIT
1520 K) expands its exhaust through an air preheater and an HRSG (economiser,
drum, evaporator) that delivers 14 kg/s of saturated steam at 20 bar; the net
power output is 30 MW. The fuel flow follows from the turbine-inlet
temperature, the air flow from the net power.

| | |
|---|---|
| **Category** | Energy systems › Cogeneration |
| **Fluids** | N2, O2, CO2, H2O, CH4 (ideal gases), Water |
| **Size** | 119 equations (largest block: 28) |
| **Source** | TESPy `tests/test_models/test_CGAM_model.py` (commit `19425523`), https://github.com/oemof/tespy |
| **Authors** | Francesco Witte and the TESPy contributors; original benchmark: A. Valero, M. A. Lozano, L. Serra et al. (1994) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@e635c85 — verified (see verification field) |

## Problem statement

Design-point CGAM problem (the name comes from *cogeneration + gas*): given
the net power (30 MW) and the process-steam requirement (14 kg/s saturated
steam at 20 bar), find the operating state of the whole plant. Inputs as in
the TESPy test: air at 1.013 bar / 25 °C with 1.9 mol% water; compressor
pressure ratio 10, isentropic efficiency 0.86; air preheated to 850 K
(air-side pressure ratio 0.95, gas-side 0.97); combustion chamber with 2 %
heat loss (`eta = 0.98`, thermal-input basis) and pressure ratio 0.95, fuel
CH4 at 12 bar / 25 °C; turbine inlet 1520 K, isentropic efficiency 0.86;
exhaust at 1.013 bar; evaporator and economiser gas-side pressure ratios
0.95^0.5 each; feedwater at 20 bar / 25 °C; economiser outlet 15 K below
saturation; evaporator outlet quality 0.5.

## Model

Air and flue gas are ideal-gas mixtures: the mixture enthalpy is the
mass-fraction-weighted sum of the species enthalpies (NASA-Glenn basis,
formation enthalpies included) and the mixture entropy sums the species
entropies at their Dalton partial pressures — the same Dalton rules as the
TESPy mixture functions (`tespy/tools/fluid_properties/mixtures.py`,
`h_mix_pT_ideal`, `s_mix_pT_ideal`). The water/steam side uses the `Water`
real fluid.

- Compressor and turbine: isentropic state from `s = s_in` at the outlet
  pressure, then `(h_out - h_in)*eta_s = h_out_s - h_in` (compressor) and
  `h_in - h_out = eta_s*(h_in - h_out_s)` (turbine), as in the TESPy
  components.
- Combustion chamber: complete combustion of CH4 with the excess air of the
  given air flow (species balances: C to CO2, H to H2O, leftover O2, N2
  passes through); energy balance
  `m_air*h3 + m_fuel*h10 = m_fg*h4 + (1 - eta)*m_fuel*LHV_CH4` with the LHV
  from the formation enthalpies (TESPy `CombustionChamber.calc_lhv` method,
  25 °C reference, water gaseous), equivalent to the reference-shifted
  balance of `DiabaticCombustionChamber.energy_balance_func`. This is the
  chamber physics of library model CSL-0139 applied to the CGAM case.
- Air preheater, evaporator, economiser: energy balances
  `m_hot*(h_in - h_out) = m_cold*(h_out - h_in)` with the given pressure
  ratios; drum: outlet 9 saturated vapour, outlet 11 saturated liquid,
  `m9 = m8`; the recirculation flow m11 follows from the evaporator duty
  `m11*(h11p - h11) = m8*(h9 - h8p)`.
- The exhaust pressure chain `p5 = p7/(pr_aph*pr_eva*pr_eco)` fixes the
  turbine back-pressure; the net power `W_turb - W_comp = W_net` fixes the
  air flow; the TIT fixes the fuel flow. All equations are solved
  simultaneously (largest algebraic block: 28).

Inputs: `p1, T1, pr_cmp, eta_s_cmp, T3, pr_aph_air, pr_aph_gas, pr_cc,
eta_cc, T4, eta_s_tur, p10, T10, p7, pr_eva_gas, pr_eco_gas, W_net, m8,
p_steam, T8, td_bubble, x11p` and the air composition `y_air_*`.
Outputs: mass flows (`m_air, m_fuel, m_fg, m9, m11`), all state temperatures
and enthalpies, the powers (`W_comp, W_turb`) and the flue-gas composition
(`w4_*, y4_*`).

State numbering follows the TESPy connections (1 compressor inlet, 2
compressor outlet, 3 preheated air, 10 fuel, 4 chamber outlet / turbine
inlet, 5 turbine outlet, 6 / 6p preheater and evaporator gas outlets, 7
chimney, 8 / 8p feedwater / economiser outlet, 11 / 11p drum liquid /
evaporator outlet, 9 live steam).

## How to run

```bash
coolsolve cgam_cogeneration.eescode
```

The `.initials` file provides guesses for the combustion/turbine block (28
variables; without them that block does not converge from the CoolSolve
defaults — see the conversion log).

## Results

| Quantity | CoolSolve | Ebsilon (`cgam-ebsilon-results.csv`) | rel. diff. |
|---|---|---|---|
| air flow m1 [kg/s] | 91.063 | 90.956 | 1.2e-03 |
| fuel flow m10 [kg/s] | 1.648 | 1.644 | 2.3e-03 |
| flue-gas flow m4 [kg/s] | 92.711 | 92.600 | 1.2e-03 |
| compressor outlet T2 [K] | 611.48 | 611.00 | 7.8e-04 |
| turbine outlet T5 [K] | 1011.27 | 1010.99 | 2.7e-04 |
| chimney T7 [K] | 431.15 | 430.04 | 2.6e-03 |
| compressor power [MW] | 29.740 | 29.6597 | 2.7e-03 |
| turbine power [MW] | 59.740 | 59.6597 | 1.4e-03 |
| flue-gas N2 / O2 / CO2 / H2O [mol frac.] | 0.7505 / 0.1368 / 0.0316 / 0.0810 | 0.7506 / 0.1369 / 0.0316 / 0.0810 | ≤ 8.6e-04 |

Derived results (CoolSolve run): thermal input 82.44 MW, net power
efficiency 36.4 %, HRSG duty 37.68 MW (evaporator 27.41 + economiser 10.28),
chamber heat loss 1.65 MW, overall energy utilisation 82.1 %. The drum
produces 14 kg/s of saturated steam at 20 bar (212.38 °C); the recirculation
flow is 29.00 kg/s.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/ + one-line caption. -->

## Verification

The source test was re-run in a throw-away virtual environment
(TESPy 0.11.3.dev0, CoolProp 8.0.0, commit `19425523`) with
`work/cgam_cogeneration/run_cgam.py` (a copy of the test's network that dumps
the connection results), and the CoolSolve `.sol` was compared with it and
with the Ebsilon table `tests/test_models/cgam-ebsilon-results.csv` using
`work/cgam_cogeneration/compare_refs.py`. As in the source test
(`test_ebsilon`), enthalpies and entropies are compared as differences within
each same-composition group (air 1–3, flue gas 4–7), because the absolute
references differ (NASA-Glenn ideal gases here, CoolProp HEOS in TESPy,
Ebsilon's own references; in particular the `H2O` entropy of CoolSolve is the
third-law NASA value, ~3.5 kJ/kg-K above CoolProp's HEOS value — a constant
offset that cancels in every equation of the model, all of which use
same-composition entropy differences).

- vs the TESPy re-run: maximum relative deviation 2.0e-03 (on
  `ds[7]−ds[4]`); all temperatures, pressures, mass flows, powers,
  enthalpy/entropy differences and molar fractions below 2.1e-03.
- vs the Ebsilon table: **compressor power 29.740 vs 29.6597 MW (2.7e-03),
  turbine power 59.740 vs 59.6597 MW (1.4e-03)** — inside the 0.5 %
  tolerance of the card; maximum over all compared quantities 4.7e-03 (on
  `ds[6]−ds[4]`, the same order as TESPy's own deviation from Ebsilon,
  which the source test bounds at 5e-03).

The source test also contains an exergy analysis (`exerpy`, external
package, Ahrendts reference environment); it is out of scope of this
translation.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the CGAM test model from TESPy, file
`tests/test_models/test_CGAM_model.py`, commit `19425523`.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff /
version control history). Original model released under the MIT License.
Changes: translated from Python to CoolSolve, network/connections flattened
into simultaneous equations, Dalton ideal-gas mixture rules inlined.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in
Python", J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
Scientific basis: the CGAM problem, A. Valero, M. A. Lozano, L. Serra,
C. Torres, G. Tsatsaronis et al., "CGAM problem: Definition and conventional
solution", Energy 19(3), pp. 279-286 (1994).

Local snapshots used: `~/git/tespy` (commit `19425523`); reference table
`~/git/tespy/tests/test_models/cgam-ebsilon-results.csv` (Ebsilon results
shipped with the TESPy test suite).

## Conversion log

- **2026-10-15 — import**: physics translated by hand from
  `test_CGAM_model.py` (network of 14 connections, 11 components, power bus)
  into 119 simultaneous equations; TESPy solver plumbing (network, cycle
  closer, power connections) became direct couplings. Unit system SI-K-Pa-J
  of the source results → SI-°C-Pa-J: temperatures in °C (the reference
  table keeps K, reproduced through `T*_K` outputs), pressures Pa.
  Air composition taken from the test's molar dict and converted to mass
  fractions as the test does.
- **2026-10-15 — LHV basis fix**: the first transcription computed the LHV
  by summing species enthalpies per kg without the molar-mass factors
  (1.94 instead of 50.03 MJ/kg); corrected as above (this changed only the
  fuel flow, −1.9 %, i.e. back to the reference value).
- **2026-10-15 — initials**: the 28-variable combustion/turbine block does
  not converge from CoolSolve's default guess (1.0); a bootstrap variant
  with the fuel flow fixed to the TESPy value produced the committed
  `.initials` (standard debugging workflow).
- **Level**: equations 119 → 1; largest block 28 → 1; no
  functions/arrays → 0; 3+ coupled components (gas turbine, preheater, HRSG
  with drum) → 1; no off-design/semi-empirics → 0; curated guesses needed
  → 1. Score 4 → level 3.

## Limitations and CoolSolve gaps

- Design point only (the TESPy test is a design-point benchmark).
- Complete combustion, no dissociation (as in the source).
- No exergy analysis (the source's second test method uses the external
  `exerpy` package).
- No CoolSolve gap blocks this model (`missing_features` is empty).

## Related models

- CSL-0139 (generic combustion chamber, TESPy `CombustionChamber`): same
  species-balance and LHV formulation, translated from the same commit of
  TESPy; this model is the CGAM application of that chamber with the TIT
  given and the fuel flow free.
