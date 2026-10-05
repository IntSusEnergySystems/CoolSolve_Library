# Land-based two-shaft gas turbine with intercooling, regeneration and reheat

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0050`

An open-circuit gas turbine (Brayton cycle) on air assumed to be a perfect
gas, with **two shafts**: a low-pressure (LP) compressor, a water-cooled
intercooler, a high-pressure (HP) compressor, a regenerator, a main combustion
chamber, an HP turbine that drives the two compressors, a second (reheat)
combustion chamber and an LP turbine that drives an alternator. The model
computes the power available at the shaft of the LP turbine and the overall
efficiency of the machine.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines |
| **Fluids** | Air (ideal gas, working fluid), Water (intercooler cooling side) |
| **Size** | 93 equations, 74 blocks (largest: 20) |
| **Source** | ULiège — course *Thermodynamique appliquée*, 2022-2023, repetition 6, exercise 3 (EES file `R06_E03_2022.EES`) |
| **Authors** | `TBD` (ULiège Thermodynamics Laboratory) — the file names no author; the EES licence stamp and the course metadata do not identify one either |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against EES (see *Verification*) |

## Problem statement

> *A land-based gas turbine has the following characteristics (see the data
> below). Determine the power available at the shaft of the LP turbine and the
> overall efficiency of the machine.*

Data: air flow rate 100 kg/s; pressure ratio of **each** compressor 4;
isentropic efficiency of the compressors 0.83; turbine entry temperature
1250 K; combustion efficiency 0.98; the HP turbine serves only to drive the
compressors (mechanical transmission efficiency 0.95); isentropic efficiency
of the turbines 0.83; alternator efficiency 0.95; compressor entry at 1 bar
and 20 °C; fuel kerosene (LHV = 43.1 MJ/kg). Further data given with the
equations of the original file: intercooler cooled by 25 kg/s of water entering
at 20 °C, effectiveness 0.9; regenerator effectiveness 0.7; heat released in
the second combustion chamber = one third of that of the main chamber
(`Q_dot_b2 = Q_dot_b/3`).

## Model

The machine is walked through from station 1 to station 10; the exit state of
each component is computed from its entry state and the powers exchanged
between the components are evaluated. Every component is an open system in
steady state; kinetic and potential energy variations are neglected (as in the
original).

| Station | Component | State |
|---|---|---|
| 1 → 2 | LP compressor | isentropic efficiency, `p[2] = p[1]*pi_c` |
| 2 → 3 | intercooler (water side, 25 kg/s at 20 °C) | isobaric, effectiveness on the maximum (limiting-fluid) heat transfer |
| 3 → 4 | HP compressor | isentropic efficiency, `p[4] = p[3]*pi_c` |
| 4 → 5 / 9 → 10 | regenerator | isobaric, effectiveness on the maximum heat transfer |
| 5 → 6 | main combustion chamber | isobaric, energy balance with `eta_b` and the fuel LHV |
| 6 → 7 | HP turbine | drives the two compressors (`eta_m*W_dot_t1 + W_dot_c1 + W_dot_c2 = 0`) |
| 7 → 8 | second combustion chamber | isobaric, `Q_dot_b2 = Q_dot_b/3` |
| 8 → 9 | LP turbine | full expansion to `p[9] = p[10] = p_amb` |
| 9 → — | alternator | `W_dot_el = W_dot_alt*eta_alt` |

Effiencies of the two heat exchangers are defined on the **maximum** (limiting
fluid) heat transfer rate, computed from ideal-state enthalpies and a `min()`
over the two sides, not from `m_dot*cp`; the two diagnostic variables `a_cycle` /
`a_ref` (intercooler) and `a_4_5` / `a_9_10` (regenerator) show which side is
limiting. The fuel flow rates `m_dot_f` and `m_dot_f2` are unknowns, obtained
from the mass and energy balances of the two combustion chambers; the
composition change of the air is neglected (only the flow rate and the
temperature change), as in the original.

Powers are counted with the sign convention of the original: compressor powers
positive, turbine powers negative.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `m_dot_a` air flow | 100 kg/s | `W_dot_t2` **LP turbine shaft power** | −29.43 MW |
| `pi_c` compressor pressure ratio | 4 | `W_dot_el` electrical power | 27.96 MW |
| `eta_is_c` / `eta_is_t` | 0.83 / 0.83 | `eta_tg` **overall efficiency** | 34.2 % |
| `TET` turbine entry temperature | 1250 K (976.85 °C) | `W_dot_c1` / `W_dot_c2` compressor powers | 17.24 / 18.31 MW |
| `p_amb` / `T_amb` | 1 bar / 20 °C | `Q_dot_b` / `Q_dot_b2` heat released | 61.26 / 20.42 MW |
| `eta_b` / `eta_m` / `eta_alt` | 0.98 / 0.95 / 0.95 | `m_dot_f` / `m_dot_f2` fuel flows | 1.42 / 0.47 kg/s |
| `eta_ref` / `eta_reg` | 0.9 / 0.7 | `Q_dot_intercooler` / `Q_dot_reg` | −15.52 / +26.38 MW |

## How to run

Open `gas_turbine_two_shaft_intercooled_regenerative.eescode` in the CoolSolve
GUI and press *Solve*, or from a terminal:

```bash
coolsolve ./gas_turbine_two_shaft_intercooled_regenerative.eescode
```

`eta_ref` and `eta_reg` are the two inputs a parametric sweep is most useful
on (the commented-out lines in the original file announce that intent).

## Results

| State | T [°C] | p [bar] |
|---|---:|---:|
| 1 compressor inlet | 20.0 | 1.000 |
| 2 LP compressor outlet | 190.3 | 4.000 |
| 3 intercooler outlet | 37.1 | 4.000 |
| 4 HP compressor outlet | 217.5 | 16.00 |
| 5 regenerator outlet (cold side) | 467.4 | 16.00 |
| 6 HP turbine inlet | 976.9 (1250 K) | 16.00 |
| 7 HP turbine outlet | 657.7 | 3.643 |
| 8 reheat combustor outlet | 825.0 | 3.643 |
| 9 LP turbine outlet | 570.5 | 1.000 |
| 10 regenerator outlet (hot side) | 331.0 | 1.000 |

| Result | Value |
|---|---:|
| `W_dot_c1` + `W_dot_c2` compressor power | 35.56 MW |
| `W_dot_t1` HP turbine power (drives the compressors) | −37.43 MW |
| `W_dot_t2` LP turbine shaft power | −29.43 MW |
| `W_dot_el` electrical power (after `eta_alt`) | 27.96 MW |
| `Q_dot_b` + `Q_dot_b2` total heat released | 81.68 MW |
| `eta_tg` overall efficiency | 34.2 % |

Two observations from the numbers: the HP turbine delivers 37.43 MW of which
35.56 MW reaches the compressors (mechanical efficiency `eta_m`), the LP
turbine keeps the rest for the alternator; and since the turbine entry
temperature `TET` is imposed, the cooling and the regeneration show up as a
lower fuel flow — 1.42 + 0.47 = 1.89 kg/s for 27.96 MW of electricity.

Air is an ideal-gas substance here, so the machine has no thermodynamic diagram
in CoolSolve (`CS-FEAT-DIAGRAM-IDEAL`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. overall efficiency and LP turbine power vs. the regenerator effectiveness eta_reg
     or vs. the compressor pressure ratio pi_c (1D/2D plot of the Parametric tab) -->

## Verification

**Faithful import vs. the EES stored solution** (`tools/compare_solution.py
--ees-units`, `reference/ees_variables.csv` of the source file: 92 common
variables). The air enthalpy and entropy of EES and of CoolProp have different
absolute reference states, so the variables carrying them are compared through
their **differences**; they are excluded from the relative deviations below:

| | EES | CoolSolve | rel. deviation |
|---|---:|---:|---:|
| `W_dot_t2` LP turbine shaft power [W] | −2.95018e+07 | −2.94274e+07 | 2.5e-03 |
| `W_dot_el` electrical power [W] | 2.80267e+07 | 2.79561e+07 | 2.5e-03 |
| `W_dot_c2` HP compressor power [W] | 1.82565e+07 | 1.83129e+07 | 3.1e-03 |
| `Q_dot_b` heat released [W] | 6.10895e+07 | 6.12609e+07 | 2.8e-03 |
| `m_dot_f` fuel flow [kg/s] | 1.41739 | 1.42137 | 2.8e-03 |
| `p[7]` HP turbine outlet pressure [Pa] | 3.65617e+05 | 3.64301e+05 | 3.6e-03 |
| `eta_tg` overall efficiency [–] | 0.344086 | 0.342259 | **5.3e-03** |

- **60 of the 92 common variables** (every variable that is not an absolute `h`
  or `s` of air) agree with a maximum relative deviation of **5.3e-03**, on
  `eta_tg`; every other one is at or below 3.6e-03.
- Absolute enthalpies of air differ by a constant reference-state offset
  (+126.0 kJ/kg on average over the ten stations) and absolute entropies by
  −1.815 kJ/kg·K; through station 1 the **enthalpy differences** agree to
  **2.8e-03** (worst case `h[4]−h[1]`) and the **entropy differences** to
  **2.3e-03** (worst case `s[10]−s[1]`).
- The remaining deviations come from the different ideal-gas models of air
  (EES `Air` vs. CoolProp `Air`), the same cause as the offset: they grow with
  the temperature range covered by each compressor (the first compressor, which
  starts at 20 °C, agrees to 1.1e-04 while the second, starting at 37 °C after
  cooling, differs by 3.1e-03).
- Only in EES: `m`, `cp`, `R`, `n`, four leftover entries of the EES variable
  list that appear in none of the equations (they are dropped from the
  `.initials`); only in CoolSolve: `fluid$`, the string variable of the
  working fluid.

## Source and attribution

Exercise solution of the ULiège course *Thermodynamique appliquée* (MECA0002),
2022-2023, repetition 6, exercise 3. **No author is named in the file**: its
header is the statement, its comments are unsigned, and the EES `$ID$` stamp
only identifies the laboratory's student/staff licence. Written in French;
`model.json` therefore lists `TBD (ULiège Thermodynamics Laboratory, course
Thermodynamique appliquée)`.

Source file (EES 10.836), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R6/R06_E03_2022.EES`
(inventory candidate `TM-0441`).

**Same exercise, earlier repetitions.** The ULiège collection also holds the
same gas turbine for repetition 5 of 2020-2021 and of 2021-2022, with
Python/CoolProp solutions (`~/Nextcloud/thermo_models/thermodynamique
appliquee/2022-2023/R6/old/ThAp21_R05E03.py` and
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R6/v-1/ThAp20_R05E03.py`).
Those scripts solve the single-shaft variant of the exercise — one expansion
5 → 8 and `W_dot_el = eta_alt*(W_dot_t+(W_dot_c1+W_dot_c2)/eta_m)` — with the
same intercooler (25 kg/s of water) and regenerator (effectiveness 0.7); they
were used to confirm the structure of the exercise and not as a numerical
reference: CoolProp is not installed in the import environment, so the scripts
could not be re-run here.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): EES
  10.836 file, `SI MASS DEG KPA C KJ` unit system, decimal comma converted to
  the dot convention by the tool, EES licence/display tags removed, 96 stored
  variables, no lookup and no parametric table. Comments translated to
  English (paraphrasing the original ones), standard header added, no equation
  changed.
- **Unit conversion by hand** (`docs/ees_import.md` §6): pressures ×1 000
  (`p_amb = 100E3`), the LHV `PCI = 43.1E6 [J/kg]`, the four cooling-water
  property calls `enthalpy/temperature/quality(Water,P=1e2[kPa],…)` →
  `P=1E5`, and `.initials` (pressures, powers, specific energies and entropies
  ×1 000, temperatures unchanged). The turbine entry temperature was written
  `TET = 1250[C]-273.15[C]` in the original, i.e. 976.85 °C = 1250 K; it is now
  `TET = 976.85 [C]` with the original value in the comment. No other equation
  contains a unit factor or an absolute temperature.
- The extraction was first checked **unmodified** (only the two lines CoolSolve
  cannot parse rewritten, see *Limitations*): `coolsolve -d` reports
  *93 equations, 93 variables, System square: Yes* — the original model is
  neither over- nor under-determined, so nothing had to be replaced by a stored
  value. The variables that look like free inputs (`eta_is_c`, `eta_is_t`,
  `Q_dot_intercooler`, `Q_dot_reg`, `Q_dot_b2`) are assigned several times in
  the original; each assignment solves for a different unknown, and all of them
  are kept as they are (EES and CoolSolve both keep the whole set).
- `m`, `cp`, `R` and `n` are entries of the EES variable list used by no
  equation; they were left out of the `.initials`.
- **Level**: taxonomy score 4 (93 equations → 1; largest block 20 → 1; arrays →
  1; three or more coupled components → 1; no off-design or dynamics → 0;
  converges from the stored values without tuning → 0), which gives level 3;
  lowered by one to **level 2** because the pedagogical intent is a complete
  textbook cycle walked through component by component, with every component
  described at the same (constant-efficiency) level of detail.
- No state-point arrays (`P[i]`, `h[i]`, `T[i]`, `s[i]`) were added: the working
  fluid is an ideal gas, for which CoolSolve has no diagram (`CS-FEAT-DIAGRAM-IDEAL`);
  the figure is a parametric sweep (workflow §7, decision D7).

## Limitations and CoolSolve gaps

- **Gap reported, not blocking**: a unit annotation inside a **named argument**
  of a function call (`enthalpy(Water,P=1e2[kPa],T=T_su_ref)`, valid EES) is a
  parse error in CoolSolve — registered as `CS-GAP-UNIT-NAMEDARG`. The hand
  unit conversion rewrites those four lines, so the converted file runs; the
  gap is not in `missing_features`. The `[C]` annotations of the original
  (`1250[C]-273.15[C]`) are an annotation on a sub-expression, already
  registered as `CS-GAP-UNIT-SUBEXPR`, and are handled by the same conversion.
- The efficiency of each heat exchanger is defined on the maximum (limiting
  fluid) heat transfer rate rather than on `m_dot*cp`, as in the original; the
  diagnostic variables `a_cycle`/`a_ref` and `a_4_5`/`a_9_10` show that the air
  side is limiting in both exchangers (17.2 vs 69.3 MW and 37.7 vs 38.4 MW).
- The intercooling water leaves at 99.6 °C with a quality of 0.127: it is
  partially evaporated, which is why the original defines the exchanger
  effectiveness with enthalpies and not with `m_dot*cp`.
- The composition change of the combustion gases is neglected (as in the
  original): the air is modelled with its own `cp(T)` before and after
  combustion, so the extra fuel mass only appears in the mass flows.
- `eta_ref` and `eta_reg` are plain inputs; the original announces that they
  were meant to be swept by a parametric table (no table is stored in the
  file). In CoolSolve they can be swept numerically from the *Parametric* tab.

## Related models

- `CSL-0011` *two_shaft_gas_turbine_compressor_map*: the same machine concept
  (two mechanically independent shafts, HP turbine driving the compressor) but
  with a compressor performance map instead of a constant pressure ratio, and
  with the mean specific heats of the combustion-library function `cpbar`.
- `CSL-0005` *cpbar_combustion_products*: mean specific heats of combustion
  products (`cpbar`), the closure this model does without.
- `CSL-0049` *otto_cycle_air_standard*: the other air-standard cycle of the
  course (constant specific heats).
- `CSL-0060` *gas_turbine_reheat*: the ideal-gas air version of the same
  machine (single-shaft architecture for the compressors), with the reheat
  combustion chamber added between the turbine stages.

- `CSL-0052` *combined_gas_steam_cycle*: the gas cycle of the same course,
  simplified (single shaft, constant pressure ratio) and driving a Rankine
  bottoming cycle through the exhaust gases.
- `CSL-0059` *stirling_cycle_ideal_regenerator*: the same course family and the
  same perfect-gas station-by-station method, for an ideal Stirling cycle whose
  regenerator is perfect (this model's is a real gas-turbine one).
