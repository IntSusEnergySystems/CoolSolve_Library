# Open-cycle gas turbine with combustion chamber and generator (TESPy tutorial)

🟢 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0141`

An open Brayton cycle in which a compressor feeds a **diabatic combustion
chamber** burning a CH4/H2/CO2 fuel; the flue gas expands in a turbine that
drives the compressor and a generator. Translation of the TESPy basic tutorial
*Gas Turbine*: the gases are ideal and the **flue-gas composition results from a
species balance**, so the air flow is found from the imposed turbine inlet
temperature, and the tutorial's two parametric studies (turbine inlet
temperature, compressor pressure ratio) are reproduced.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines |
| **Fluids** | Ar, N2, O2, CO2, H2O, CH4, H2 (ideal gases) |
| **Size** | 79 equations, largest block 13: 79 for the model (no diagram array: ideal-gas mixture, workflow §7) |
| **Source** | TESPy tutorial `tutorial/basics/gas_turbine.py` ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`), companion docs `docs/basic_tutorials/gas_turbine.rst` |
| **Authors** | Francesco Witte (TESPy lead developer) and the TESPy contributors |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs (with the shipped `.initials`); translation verified against TESPy (see *Verification*) |

## Problem statement

Ambient air (Ar 1.29 %, N2 75.53 %, CO2 0.04 %, O2 23.14 % by mass) is
compressed from 1 bar, 20 °C with a pressure ratio of 15 and an isentropic
efficiency of 0.85. In the combustion chamber (pressure ratio 0.97, efficiency
0.98, i.e. 2 % of the thermal input lost to the ambient) 1 kg/s of fuel
(92 % CH4, 5 % H2, 3 % CO2) is burned at 20 °C and 15.75 bar. The flue gas
leaves at 1200 °C and expands to 1 bar with an isentropic efficiency of 0.90;
the turbine drives the compressor and a generator of efficiency 0.98. Determine
the air flow, the flue-gas composition, the excess-air ratio λ, the thermal
input and the net power and efficiency of the cycle.

## Model

State labels are the TESPy connection labels: 1 = compressor inlet, 2 =
compressor outlet = chamber inlet 1, 3 = chamber outlet = turbine inlet,
4 = turbine outlet, 5 = fuel inlet 2. The chamber's thermal input and
excess-air ratio are results here; the tutorial specifies them in its earlier
sections (see *Verification*).

- Compressor (TESPy `Compressor pr`/`eta_s`): `p_2 = 15·p_1` and
  `(h_2 − h_1)·η_s = h_2s − h_1` with `h_2s = h(s_1, p_2)`.
- Combustion chamber (TESPy `DiabaticCombustionChamber`): `p_3 = pr·p_2`;
  one **species balance per fluid** (`stoichiometry_func`) from the molar
  flows of CH4, H2 and of the available oxygen,
  `λ = n_O2,air / (n_H/4 + n_C)`; complete combustion (λ > 1), the water
  gaseous; energy balance on the **lower-heating-value basis**, referred to
  25 °C: `ṁ₁(h₂ − h_ref) + ṁ₅(h₅ − h_ref) + η·ṁ_fuel·LHV = ṁ₃(h₃ − h_ref)`,
  where `LHV` is computed from the molar formation enthalpies
  (`CombustionChamber.calc_lhv`).
- Turbine (TESPy `Turbine eta_s`): `p_4 = p_1` and
  `h_3 − h_4 = η_s·(h_3 − h_4s)` with `h_4s = h(s_3, p_4)`.
- Shaft and generator (TESPy `PowerBus`, `Generator`, `PowerSink`):
  `Ẇ_tu = ṁ₃(h₃ − h₄)`, `Ẇ_cp = ṁ₁(h₂ − h₁)`,
  `P_grid = η_gen·(Ẇ_tu − Ẇ_cp)`, `η = P_grid/ti`.
- Mixture properties: mass-weighted sums of the ideal-gas species enthalpies
  and entropies (`FUNCTION h_gas`, `FUNCTION s_gas`), the TESPy *forced-gas*
  mixing rule.

| Inputs | Base value | Outputs | Value |
|---|---|---|---|
| `p_1`, `T_1` ambient | 1 bar, 20 °C | `m_1` air flow | 50.70 kg/s |
| `pr_cp`, `eta_s_cp` | 15, 0.85 | `T_2` compressor outlet | 411.6 °C |
| `T_3` turbine inlet | 1200 °C | `T_4` turbine outlet | 575.2 °C |
| `pr_cc`, `eta_cc` | 0.97, 0.98 | `lambda` excess-air ratio | 2.885 |
| `m_5`, `T_5`, `f_p_fuel` | 1 kg/s, 20 °C, 1.05 | `ti` thermal input | 52.02 MW |
| `eta_s_tu`, `eta_gen` | 0.90, 0.98 | `P_dot_grid` net power | 19.02 MW |
| | | `eta` thermal efficiency | 36.57 % |

## How to run

Open `gas_turbine_open_cycle.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./gas_turbine_open_cycle.eescode
```

The **shipped `gas_turbine_open_cycle.initials` is needed**: the air flow and
the flue-gas composition are strongly coupled (the energy balance fixes `m_1`
for a given `T_3`, and the composition depends on `m_1`), and the cold start
does not converge (the 13-equation chamber block reaches *MaxIterations*). The
`.initials` hold the TESPy base-case values. The tutorial's parametric studies
are CoolSolve parametric studies (GUI *Parametric* tab) over `T_3` and
`pr_cp`, or single re-solves with the input edited.

## Results

Base case (TESPy tutorial sec_9–sec_11):

| Point | TESPy | p [bar] | T [°C] | ṁ [kg/s] | mass fractions |
|---|---|---:|---:|---:|---|
| 1 compressor inlet | c1 | 1.00 | 20.00 | 50.70 | Ar .0129 N2 .7553 O2 .2314 CO2 .0004 |
| 2 compressor outlet | c2 | 15.00 | 411.60 | 50.70 | idem |
| 3 turbine inlet | c3 | 14.55 | 1200.00 | 51.70 | Ar .01265 N2 .74069 O2 .14827 CO2 .04979 H2O .04861 |
| 4 turbine outlet | c4 | 1.00 | 575.20 | 51.70 | idem |
| 5 fuel inlet | c5 | 15.75 | 20.00 | 1.00 | CH4 .92 H2 .05 CO2 .03 |

`lambda = 2.885`, `ti = 52.02 MW`, `Q_loss = −1.04 MW`, `Ẇ_tu = 39.90 MW`,
`Ẇ_cp = 20.48 MW`, `P_grid = 19.02 MW`, `eta = 36.57 %`.

Parametric studies of the tutorial (sec_11), CoolSolve values in brackets:

| `T_3` [°C] | η [%] | `P_grid` [MW] | `pr_cp` | η [%] | `P_grid` [MW] |
|---:|---:|---:|---:|---:|---:|
| 900 | 33.10 (33.02) | 17.219 (17.178) | 10 | 33.21 (33.17) | 17.275 (17.254) |
| 1200 | 36.61 (36.57) | 19.047 (19.023) | 15 | 36.61 (36.57) | 19.047 (19.023) |
| 1400 | 37.40 (37.37) | 19.458 (19.441) | 30 | 40.13 (40.08) | 20.876 (20.849) |

Both trends are the expected ones for a simple open cycle: the efficiency and
the net power rise with the turbine inlet temperature and with the compressor
pressure ratio over the swept range (the compressor work grows more slowly
than the turbine work as the pressure ratio rises).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep of the thermal efficiency and of the net power vs the turbine inlet
     temperature and the compressor pressure ratio (ideal-gas model: no
     thermodynamic diagram, decision D7), figures/gas_turbine_open_cycle_sweep.png -->

## Verification

TESPy stores no numbers for this tutorial (`tests/test_basic_tutorials.py`
only executes the scripts), so the tutorial was run in a throw-away virtual
environment (Python 3.12, TESPy installed from the local snapshot at commit
`19425523`, CoolProp 8.0.0) and the script, its printed values and this model
were compared with `CoolSolve/tools/compare_solution.py`
(`work/tespy_gas_turbine/run_reference.py` re-runs the tutorial sections
`sec_1`…`sec_11` verbatim and prints the base case and the two sweeps).

1. **Base case**: 37 common variables, maximum relative deviation
   **2.1e-03** on `W_dot_cp` (20.484 MW against 20.442 MW); every other
   physical result is at or below 1.3e-03 (`m_1` 1.3e-03, `eta` and
   `P_dot_grid` 1.2e-03, `lambda` and the flue-gas mass fractions
   1.3e-03, `T_2` 8.9e-04, `T_4` 2.4e-04, `ti` exact).
2. **Excluded from the comparison**: the absolute mixture enthalpies `h_1`,
   `h_2`, `h_3`, `h_4`, `h_5`. TESPy evaluates the mixtures with CoolProp's
   real-gas (HEOS) species and their reference states (flue gas: 1.798 MJ/kg
   at 1200 °C), this model with CoolSolve's ideal-gas (NASA) species
   (0.279 MJ/kg): a constant offset of 1.52 MJ/kg on the flue gas. The
   **enthalpy differences**, which drive the results, are compared instead:

   | | TESPy [J/kg] | CoolSolve [J/kg] | rel. diff |
   |---|---:|---:|---:|
   | `h_2 − h_1` compressor rise | 403 683 | 403 999 | 7.8e-04 |
   | `h_3 − h_4` turbine drop | 772 244 | 771 621 | 8.1e-04 |

   The 0.08 % is the gas model itself: TESPy's `CoolPropWrapper` uses the
   HEOS back end for the species, this model the ideal-gas one (the model
   assumption, also visible in the mixture entropies: `s_1` = 6846 J/kg·K in
   TESPy against 6684 J/kg·K here — a constant mixing/reference offset that
   cancels in every isentropic relation).
3. **Parametric studies** (sec_11 sweeps, 11 points each, re-solved
   point-wise): the three points above agree to 1.3e-03 (efficiency) and
   2.4e-03 (net power), the same gas-model deviation as the base case.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the TESPy basic tutorial *Gas Turbine*, file
`tutorial/basics/gas_turbine.py`, commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff / version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve; the network solver and the
component/connection objects replaced by simultaneous equations; the
diabatic-chamber equations (species balances, λ, lower-heating-value energy
balance referred to 25 °C) written out; units normalised to SI-°C-Pa-J (TESPy
displays bar/°C/MW); the base case of sec_9–sec_11 shipped, the composition
variants and sweeps of sec_12–sec_13 documented but not shipped.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in Python",
J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
Scientific basis: the tutorial itself; the lower heating value uses the molar
formation enthalpies of CODATA 1989 (CO2 −393.51, H2O(g) −241.826 kJ/mol) and
of TESPy's `COMBUSTION_FLUIDS` (CH4 −74.6 kJ/mol), as in the source.

Source file (Python, comments in English), local snapshot of S. Quoilin:
`~/git/tespy/tutorial/basics/gas_turbine.py`
(companion: `docs/basic_tutorials/gas_turbine.rst`; component sources:
`src/tespy/components/combustion/{base,diabatic}.py`,
`src/tespy/components/turbomachinery/{compressor,turbine}.py`;
test: `tests/test_basic_tutorials.py`) — inventory candidate `TSP-036`.

## Conversion log

- **2026-10-14 — translation** (workflow `T-TRANSLATE`, card C-186): the
  TESPy network (`Source`, `Compressor`, `DiabaticCombustionChamber`,
  `Turbine`, `Generator`, `PowerBus`, `PowerSink`, 5 material connections and
  4 power connections) rewritten as 79 simultaneous EES equations. Mapping:
  - `PowerBus`/`Generator`/`PowerSink` → `W_dot_tu`, `W_dot_cp`,
    `W_dot_gen = W_dot_tu - W_dot_cp`, `P_dot_grid = eta_gen·W_dot_gen`
    (the shaft power balance is an identity);
  - `c5.p = Ref(c2, 1.05, 0)` → `p_5 = f_p_fuel·p_2` (input `f_p_fuel`);
  - `cc.lamb`/`cc.ti` are *results* here (the tutorial's base case fixes the
    fuel flow `m_5` and the turbine inlet temperature `T_3`), so the chamber
    block closes on the energy balance and gives `m_1` and `lambda`;
  - the flue-gas **mass fractions** `x_*_3` are the state variables (the
    `fluid` dict of TESPy); the seven species balances are written
    explicitly; the mixture property calls of TESPy's `forced-gas` mixing
    rule become the `FUNCTION h_gas` and `FUNCTION s_gas`;
  - `LHV_fuel` (TESPy `CombustionChamber.calc_lhv`) **copied from `CSL-0139`**,
    which translated the same function (`CS-FEAT-IMPORT`: CoolSolve cannot yet
    import it with `$INCLUDE library:`), with the constants in the calling
    code;
  - the unit system was already SI-like: only the display units change
    (bar → Pa, °C unchanged, MW → W, kJ/kg → J/kg).
- **Logarithmic/iterative content**: none left — TESPy's Newton network
  solver, the `Ref` pressure, the successive `solve()` calls of the tutorial
  and the `lamb`/`ti` specification switches become simultaneous equations
  and input lines; the sec_11 sweeps become parametric studies.
- **Decision — tutorial content not shipped**: the earlier sections of the
  tutorial (sec_3–sec_7: chamber alone with `ti`, `m` or `T_3` specification,
  the `lamb` specification, the fuel-composition variants) demonstrate
  TESPy's specification flexibility on the chamber component, not a different
  cycle. They are described here and were checked during the task: the
  chamber block of this model reproduces the tutorial's **sec_3** state
  (chamber alone, `pr_cc` = 1, `eta_cc` = 1, λ = 1.5, `ti` = 10 MW, air at
  1 bar/20 °C straight into the chamber, fuel 96 % CH4 / 4 % CO2) when
  `T_3` is left free, `pr_cp` is set to 1 and `m_5` is replaced by the
  λ-relation of `CSL-0139` (`m_5 = n_dot_O2_air/(λ·ν_O2)`): fuel flow
  0.208224 kg/s (TESPy 0.208224), air flow 5.169077 kg/s (5.169077), flue-gas
  temperature 1510.25 °C (1510.31 °C, 3.4e-05) and the seven mass fractions
  equal to 8 digits. The sec_12/13 sweeps (O2 mass fraction in the flue gas,
  fuel composition from a thermal input) need the specification switches and
  are out of scope of a cycle model.
- **Level**: taxonomy §3 score 5 (79 equations → 1, block of 13 → 1,
  functions → 1, four coupled components → 1, no semi-empirical/off-design →
  0, curated guesses → 1) = level 3, moved down by one to **level 2**: the
  13-equation block is one physical combustion chamber, not a discretisation,
  and the pedagogical intent (basic tutorial) matches `CSL-0050` and
  `CSL-0060` of the same category.
- **No diagram arrays**: the working fluid is an ideal-gas *mixture*, which
  the CoolSolve diagrams cannot represent (`CS-FEAT-DIAGRAM-IDEAL`, decision
  D7): the figure is a parametric sweep plot, workflow §7.

## Limitations and CoolSolve gaps

- No CoolSolve gap met: the model uses property calls on ideal-gas species,
  arithmetic and three `FUNCTION`s; it solves with the shipped `.initials`.
- Ideal gases: no dissociation, no real-gas effects, no NOx formation (the
  TESPy `f_nox` parameter, not used by the tutorial); the water of the flue
  gas is vapour at 25 °C, as in the source.
- TESPy sign convention: the turbine and the compressor powers are negative in
  the `PowerConnection` results table (energy flows into the component); this
  model reports them as positive `W_dot_tu` and `W_dot_cp`.
- The mixture entropy misses the constant mixing term `-R·Σx·ln x`; it
  cancels in every isentropic relation of the model (compressor and turbine,
  constant composition), so the isentropic reference states are unchanged.
- The cold start does not converge (see *How to run*); `.initials` ship with
  the model.

## Related models

- `CSL-0139` *combustion_chamber*: the `CombustionChamber` /
  `DiabaticCombustionChamber` component class of the same TESPy snapshot,
  translated as a standalone chamber (fixed air flow, λ as an input, flue-gas
  temperature as a result) and verified against the CGAM reference; its
  `LHV_fuel` function is the one copied here.
- `CSL-0135` *turbine_stodola_offdesign*: the `Turbine` class of the same
  snapshot (η_s relation and Stodola cone law); this model uses only its
  design-point η_s relation.
- `CSL-0013` *heat_pump_basic_tespy*: the basic heat-pump tutorial of the
  same TESPy snapshot.
- `CSL-0050` *gas_turbine_two_shaft_intercooled_regenerative* and
  `CSL-0060` *gas_turbine_reheat*: gas turbines of the same category on air as
  a perfect gas, with the combustion chemistry neglected — this model keeps
  the species balances and the mixture properties of the tutorial.