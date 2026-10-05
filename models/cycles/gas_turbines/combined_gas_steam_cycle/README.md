# Combined gas-steam cycle (Brayton topping cycle, Rankine bottoming cycle)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0052`

A **combined gas-steam cycle**: a gas turbine (Brayton) topping cycle runs on
air assumed to be a perfect gas, and its exhaust gases heat the steam of a
simple **Rankine** bottoming cycle in a heat exchanger. The statement gives no
flow rate and no power, so the model obtains the **steam-to-gas flow ratio**
from the energy balance of the heat exchanger and the **thermal efficiency of
the combined cycle** from the sum of the four machine powers over the heat
released by the topping cycle.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air (ideal gas, working fluid of the topping cycle), Water (bottoming cycle) |
| **Size** | 44 equations, all explicit (largest block: 1): 36 for the model, 8 for the diagram state points |
| **Source** | ULiège — course *Thermodynamique appliquée*, 2022-2023, repetition 7, exercise 5 (EES file `R07_E05_2022.EES`) |
| **Authors** | `TBD` (ULiège Thermodynamics Laboratory) — the file names no author; the EES licence stamp and the companion Word metadata do not identify one either |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against EES (see *Verification*) |

## Problem statement

> *Consider the combined gas-steam cycle of the figure. The upper cycle is that
> of a gas turbine with a compressor pressure ratio of 8. The air enters the
> compressor at 300 K and enters the turbine at 1300 K. The isentropic
> efficiencies of the compressor and of the turbine are 80 % and 85 %. The
> lower cycle is a simple Rankine cycle operating between pressure limits of
> 7 MPa and 5 kPa; the pump and the turbine are taken as isentropic. The steam
> is heated in a heat exchanger by the exhaust gases up to a temperature of
> 500 °C, and the exhaust gases leave the heat exchanger at 450 K. Determine
> the ratio between the steam flow rate and the gas flow rate, and the thermal
> efficiency of the combined cycle.*

The Brayton cycle takes in and rejects its air at ambient pressure, which the
original takes as 1 bar.

## Model

Two cycles, each walked through station by station from the state where the
statement gives the most information; all components are isobaric heat
exchangers or isentropic machines with a constant isentropic efficiency, no
pressure loss and no combustion chemistry. Station 1 of the gas cycle is the
compressor inlet and station 5 the outlet of the heat exchanger; station 1 of
the steam cycle is the pump inlet and station 4 the turbine outlet.

| Station | Component | State |
|---|---|---|
| TGV 1 → 2 | compressor | isentropic efficiency `eta_is_cp`, `P_TGV[2]/P_TGV[1] = 8` |
| TGV 2 → 3 | boiler | isobaric |
| TGV 3 → 4 | gas turbine | isentropic efficiency `eta_is_turb`, `P_TGV[4] = P_TGV[5] = P_TGV[1]` |
| TGV 4 → 5 | heat exchanger (gas side) | isobaric, exhaust leaves at `T_TGV[5] = 450 K` |
| steam 1 → 2 | pump | isentropic, saturated liquid assumed at the inlet (`x[1] = 0`) |
| steam 2 → 3 | heat exchanger (steam side) | isobaric, `P[2] = P[3] = 7 MPa`, steam heated to 500 °C |
| steam 3 → 4 | turbine | isentropic, `P[4] = P[1] = 5 kPa` |

- **Steam-to-gas flow ratio**: the statement gives no flow rate, but the
  enthalpies give it from the energy balance of the heat exchanger,
  $\dot m_{TGV}(h_{TGV,5}-h_{TGV,4}) = \dot m_{steam}(h_3-h_2)$:
  $Ratio_{ORC,TGV} = |(h_{TGV,5}-h_{TGV,4})/(h_3-h_2)|$.
- **Thermal efficiency of the combined cycle**: useful effect over costly
  effect, the costly effect being the heat released by the topping cycle
  ($Q_{TGV,2\to3} = \dot m_{TGV}(h_{TGV,3}-h_{TGV,2})$) and the useful effect
  the two turbine powers minus the compressor and pump powers. With
  $\dot m_{steam} = Ratio_{ORC,TGV}\,\dot m_{TGV}$, the common mass flow is
  simplified away, so the efficiency needs no flow rate either.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `P_TGV[2]/P_TGV[1]` compressor pressure ratio | 8 | `Ratio_ORC_TGV` steam-to-gas flow ratio | 0.1313 kg/kg |
| `T_TGV[1]` / `T_TGV[3]` compressor and turbine inlet temperature | 300 / 1300 K | `n_th` **thermal efficiency of the combined cycle** | 48.7 % |
| `T_TGV[5]` exhaust gas outlet temperature | 450 K | `T_TGV[4]` gas turbine outlet temperature | 853 K |
| `eta_is_cp` / `eta_is_turb` | 0.8 / 0.85 | `h[3]` / `h[4]` steam turbine inlet / outlet enthalpy | 3411 / 2073 kJ/kg |
| `P_TGV[1]` ambient pressure | 1 bar | `x[4]` steam quality at the turbine outlet | 0.799 |
| `P[2]` / `P[4]` steam cycle pressure limits | 7 MPa / 5 kPa | `h[1]` / `h[2]` pump inlet / outlet enthalpy | 137.7 / 144.8 kJ/kg |
| `T[3]` steam turbine inlet temperature | 500 °C | `x[1]` pump inlet quality (assumption) | 0 |

## How to run

Open `combined_gas_steam_cycle.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./combined_gas_steam_cycle.eescode
```

Every equation is explicit (largest block: 1), so no `.initials` file is
needed. `P_TGV[2]/P_TGV[1]`, `T[3]` and `T_TGV[5]` are the inputs a
parametric sweep is most useful on.

## Results

Per kilogram of gas (states read from the `.sol` baseline):

| State | T [°C] | p [bar] | h [kJ/kg] |
|---|---:|---:|---:|
| TGV 1 compressor inlet | 26.85 (300 K) | 1.000 | 426.3 † |
| TGV 2 compressor outlet | 325.3 | 8.000 | 731.7 † |
| TGV 3 turbine inlet | 1026.85 (1300 K) | 8.000 | 1522.9 † |
| TGV 4 turbine outlet | 579.8 | 1.000 | 1006.9 † |
| TGV 5 exhaust gas at the heat-exchanger outlet | 176.85 (450 K) | 1.000 | 578.1 † |
| steam 1 pump inlet | 32.87 | 0.050 | 137.7 |
| steam 2 pump outlet | 33.04 | 70.00 | 144.8 |
| steam 3 turbine inlet | 500.0 | 70.00 | 3411.4 |
| steam 4 turbine outlet | 32.87 | 0.050 | 2073.0 |

† air enthalpies carry the reference-state offset of the CoolProp `Air`
model (+126.06 kJ/kg with respect to EES); the **differences** agree with the
EES values (see *Verification*).

| Result | Value |
|---|---:|
| `Ratio_ORC_TGV` steam flow rate / gas flow rate | 0.1313 kg steam per kg gas |
| `n_th` thermal efficiency of the combined cycle | 48.7 % |
| heat given to the steam, per kg of gas (`h_TGV[5]-h_TGV[4]`) | 428.8 kJ/kg |
| thermal efficiency of the topping cycle alone (compressor + turbine) | 26.6 % |
| thermal efficiency of the bottoming cycle alone (pump + turbine) | 40.8 % |

The numbers are consistent with each other: per kilogram of gas the topping
cycle produces 210.5 kJ/kg of net work from 791.2 kJ/kg of heat, and the
0.1313 kg of steam that receives the 428.8 kJ/kg of exhaust energy produces
0.1313 × 1331.4 = 174.8 kJ/kg more; the sum, 385.3 kJ/kg over 791.2 kJ/kg,
is the 48.7 % of `n_th`.

The arrays `P[i]`, `T[i]`, `h[i]`, `s[i]`, `x[i]` (i = 1 pump inlet, 2 pump
outlet, 3 turbine inlet, 4 turbine outlet) and `P_TGV[i]`, `T_TGV[i]`,
`h_TGV[i]`, `s_TGV[i]` (i = 1 … 5) give both cycles on a diagram (CoolSolve
*Diagram* tab, *Overlay array path*, *Close cycle*); only the steam cycle can
actually be drawn, since the working fluid of the gas cycle is an ideal gas
(`CS-FEAT-DIAGRAM-IDEAL`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. combined-cycle thermal efficiency n_th and steam-to-gas flow ratio Ratio_ORC_TGV
     vs the compressor pressure ratio P_TGV[2]/P_TGV[1] or vs the steam temperature T[3]
     (1D/2D plot of the Parametric tab; the gas cycle is on an ideal gas, which has no
     diagram in CoolSolve) -->

## Verification

**Import vs. the EES stored solution** (`tools/compare_solution.py
combined_gas_steam_cycle.sol … --ees-units`, 36 common variables; the
reference is the solution stored by EES 10.836 in the source file).

| Variable | EES | CoolSolve | rel. deviation |
|---|---:|---:|---:|
| `n_th` combined-cycle thermal efficiency [–] | 0.4870167 | 0.4870167 | 1.7e-07 |
| `Ratio_ORC_TGV` steam-to-gas flow ratio [–] | 0.1312640 | 0.1312646 | 4.6e-06 |
| `h[3]` steam turbine inlet enthalpy [J/kg] | 3.41139e+06 | 3.41139e+06 | 2.9e-10 |
| `h[4]` steam turbine outlet enthalpy [J/kg] | 2.07297e+06 | 2.07297e+06 | 3.6e-10 |
| `h[1]` pump inlet enthalpy [J/kg] | 1.37750e+05 | 1.37750e+05 | 7.4e-06 |
| `T_TGV[4]` gas turbine outlet temperature [°C] | 579.816 | 579.816 | 2.9e-08 |

- **27 of the 36 common variables agree within 7.4e-06** relative (worst case
  `h[1]`, the saturated-liquid enthalpy at 5 kPa); every other one is at or
  below 4.6e-06, the pressures and temperatures being reproduced exactly.
  `compare_solution.py` prints *"36 common variables, 9 differ (rtol=0.001)"*.
- The **9 variables left out** of that figure are the absolute enthalpy and
  entropy of air: `h_TGV[1]`, `h_TGV[2]`, `h_TGV[3]`, `h_TGV[4]`, `h_TGV[5]`,
  `h_TGV_2_is`, `h_TGV_4_is`, `s_TGV[1]`, `s_TGV[3]`. They differ by the
  reference-state offset between the two air models (**+126.06 kJ/kg** on `h`
  and **−2.978 kJ/kg·K** on `s`, nearly constant over the ten states).
  Compared through their **differences**, the air agrees: `h_TGV[3]-h_TGV[4]`
  515 977.9 (EES) against 515 980.4 J/kg, `h_TGV[2]-h_TGV[1]` 305 435.1
  against 305 436.6 J/kg and `s_TGV[3]-s_TGV[1]` 975.28 against 975.29 J/kg·K,
  i.e. 4.9e-06 — the two ideal-gas models of air are practically the same.
- **Only in EES** (8): `m_dot_TGV`, `m_dot_ORC`, `W_dot_turb_TGV`,
  `W_dot_cp_TGV`, `W_dot_turb_ORC`, `W_dot_pump_ORC`, `effet_utile`,
  `effet_couteux`. They appear in the EES variable list because EES tokenizes
  the commented-out equations of the original, but no equation uses them (see
  *Conversion log*).
- **Only in CoolSolve** (8): `T_TGV[2]`, `s_TGV[2]`, `s_TGV[4]`, `s_TGV[5]`,
  `T[1]`, `T[2]`, `T[4]`, `x[4]` — the state points added for the diagrams
  (they do not change any result of the model).

## Source and attribution

Exercise solution of the ULiège course *Thermodynamique appliquée* (MECA0002),
2022-2023, repetition 7, exercise 5. **No author is named in the file**: its
header is the statement, its comments are unsigned, and the EES `$ID$` stamp
(`For use only by students and staff at the Laboratoire de Thermodynamique,
University of Liege PoloUHB`) only identifies the laboratory's student/staff
licence. The companion Word document of the repetition
(`ThAp22_R07.docx`) has `Windows User` as its creator. Written in French;
`model.json` therefore lists `TBD (ULiège Thermodynamics Laboratory, course
Thermodynamique appliquée)`.

Source file (EES 10.836), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R7/R07_E05_2022.EES`
(inventory candidate `TM-0446`).

**No other solution of this exercise in the collection.** The same repetition
of the 2020-2021 edition (`…/R7/V-1/`) holds the slides and the Python/CoolProp
solutions of exercises 1 to 3 only (`ThAp20_R07E01.py` to `E03.py`), so the
model was verified against the EES stored solution alone.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): EES
  10.836 file, unit system `SI MASS DEG KPA K KJ` (pressures in kPa,
  temperatures in K, energies in kJ), decimal comma converted to the dot
  convention by the tool, EES licence/display tags removed, 44 stored
  variables, no lookup and no parametric table. Comments translated to English
  (paraphrasing the original ones), standard header added, no equation changed
  except the two below.
- **Unit conversion by hand** (`docs/ees_import.md` §6): `T_TGV[1] = 26.85 [C]`
  (300 K), `T_TGV[3] = 1026.85 [C]` (1300 K), `T_TGV[5] = 176.85 [C]` (450 K),
  `P_TGV[1] = 1E5 [Pa]`, `P[2] = 7E6 [Pa]`, `P[4] = 5E3 [Pa]`, and
  `T[3] = 500 [C]`, which the original wrote as `500[K]+273.15[K]` (an
  annotation on a sub-expression, already registered as
  `CS-GAP-UNIT-SUBEXPR`, so the line is rewritten by the conversion anyway).
  The original values are kept in the comments of every converted input. No
  other equation contains a unit factor, an absolute temperature or an
  empirical correlation, so nothing else was changed. No `.initials` file is
  shipped: every equation is explicit, and the model converges from its
  solution without any guess (the stored values would have needed a different
  reference state for the air, see *Verification*).
- **Fluid name** (the one physics-relevant change): the original evaluates the
  gas cycle with the EES humid-air pseudo-fluid `'Air_ha'` **without any
  humidity ratio**, i.e. as dry air; it is written `Air`, the ideal-gas dry-air
  substance, for two reasons: CoolSolve's humid-air backend returns a silently
  wrong value (10 000 J/kg) above 623.15 K, i.e. exactly the turbine inlet
  temperature of this model (bug reported, `CS-BUG-HUMIDAIR-HIGHT`), and the
  two substances are the same dry air — verified by the enthalpy difference
  between the compressor and turbine inlets, which agrees with EES to 4.9e-06.
  `'water'` is written `Water`. Both names are valid EES.
- **Dead code removed**: the original keeps the successive forms of `n_th` and
  the definitions of `m_dot_TGV`, `m_dot_ORC`, `W_dot_turb_TGV`,
  `W_dot_cp_TGV`, `W_dot_turb_ORC`, `W_dot_pump_ORC`, `effet_utile` and
  `effet_couteux` **in comments** (they were written and commented out while
  the derivation was built up). They are part of the explanation, so the
  derivation is paraphrased in the comments of the two result blocks, and the
  final form of `n_th` is kept byte for byte. Those eight names remain in the
  EES variable list but in no equation of the model.
- **Diagram support**: 8 post-processing equations added at the end of the
  model (the gas-cycle states `T_TGV[2]`, `s_TGV[2]`, `s_TGV[4]`, `s_TGV[5]`
  and the steam states `T[1]`, `T[2]`, `T[4]`, `x[4]`), so that the five
  stations of the gas cycle and the four of the steam cycle are complete in
  the state arrays; the results of the model are unchanged.
- The extraction was checked **unmodified** first (`coolsolve -d`, only the
  `$UnitSystem` line and the `CS-GAP-UNIT-SUBEXPR` line of `T[3]` removed):
  *"36 equations, 36 variables, System square: Yes"* — the original is neither
  over- nor under-determined, so nothing had to be replaced by a stored value.
- **Level**: taxonomy score 1 (44 equations → 0; largest block 1 → 0; arrays →
  1; fewer than three coupled components → 0; no off-design, part-load or
  dynamics → 0; converges without curated guesses → 0), which gives level 1;
  raised by one to **level 2** because the exercise is a complete combined
  cycle (two cycles, four machines and a heat exchanger) walked through
  component by component, the same level as the other gas-turbine models of
  the course.
- No figure of a thermodynamic diagram is expected for the gas cycle (ideal
  gas): the figure of this model is a parametric sweep (workflow §7, decision
  D7).

## Limitations and CoolSolve gaps

- **Bug reported, not blocking**: `enthalpy`/`entropy` on the humid-air fluid
  `AirH2O` return **10 000 J/kg** (respectively J/kg·K) for temperatures above
  623.15 K, with no warning and a *SUCCESS* solver status, while EES evaluates
  the same state normally (registered as `CS-BUG-HUMIDAIR-HIGHT`; the original
  file stores 1396.83 kJ/kg for the 1300 K, 800 kPa state of this model). The
  gas cycle is therefore written with the ideal-gas substance `Air`, which is
  the same dry air (see *Conversion log*); the gap is not in
  `missing_features`, since the native file runs.
- **Gap reported, not blocking**: a unit annotation on a sub-expression
  (`T[3] = 500[K]+273.15[K]`, valid EES) is a parse error in CoolSolve —
  already registered as `CS-GAP-UNIT-SUBEXPR`. The hand unit conversion
  rewrites that line, so the converted file runs.
- The steam cycle is *named* "ORC" in the variables of the original
  (`Ratio_ORC_TGV`, `m_dot_ORC`), although it is a plain Rankine cycle on
  water with no working-fluid change and no superheat beyond the statement;
  the names were kept, with this note.
- No pressure loss is modelled in the heat exchanger or in the pipes, no
  combustion chemistry (the heat released by the topping cycle is
  characterised only by its inlet and outlet temperature), no mechanical or
  generator efficiency, and the pump is assumed to be isentropic with a
  saturated liquid at its inlet — as in the original, whose comment adds that
  a slight subcooling of 2 to 3 K at the pump inlet could be considered
  (a pump cannot take two-phase or gas flow without cavitation and damage,
  and subcooling would lower the efficiency).
- The gas cycle absorbs and rejects its air at ambient pressure, which is an
  input of the model (`P_TGV[1]`), not a result.
- The quality `x[4] = 0.799` and the saturation temperature `T[4] = 32.87 °C`
  are computed at 5 kPa; CoolSolve needs no upper/lower bounds here since the
  isentropic expansion from 7 MPa and 500 °C stays inside the two-phase dome.

## Related models

- `CSL-0050` *gas_turbine_two_shaft_intercooled_regenerative*: the other gas
  cycle of the same course and repetition series (open-circuit two-shaft gas
  turbine on ideal-gas air), with intercooling, regeneration and reheat.
- `CSL-0004` *rankine_cycle_60mw*: the Rankine cycle of the same repetition,
  as a standalone plant with flows, efficiency and cooling-water balance.
- `CSL-0029` *rankine_cycle_regenerative_extraction*: the other steam cycle of
  the same repetition (extraction to a deaerator).
- `CSL-0011` *two_shaft_gas_turbine_compressor_map*: the same machine concept
  (two mechanically independent shafts, HP turbine driving the compressor) but
  with a compressor performance map instead of a constant pressure ratio, and
  with the mean specific heats of the combustion-library function `cpbar`
  (model *blocked* by `CS-GAP-INTERP-EES`).