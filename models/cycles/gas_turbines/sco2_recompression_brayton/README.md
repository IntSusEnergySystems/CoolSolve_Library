# Supercritical CO2 recompression Brayton cycle (100 MW net)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0144`

Design-point model of the supercritical CO2 recompression Brayton cycle with two
sectioned recuperators delivering 100 MW net power, after the TESPy
model-library example `sco2.ipynb`, which validates it against the published
state table of Penkuhn & Tsatsaronis (2018). The Python network solver of the
original is translated into simultaneous equations; the recompression split is
fixed by equal merge temperatures (states 11 and 12), as in the original
design. Useful as a reference case for sCO2 power-block studies and as a
worked example of translating a TESPy `SectionedHeatExchanger`.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and Brayton cycles |
| **Fluids** | R744 (CO2) |
| **Size** | 486 equations (largest block: 8) |
| **Source** | TESPy `docs/model_library/sco2.ipynb` (commit `19425523`), original model [fwitte/sCO2_exergy](https://github.com/fwitte/sCO2_exergy) |
| **Authors** | Francesco Witte (TESPy lead developer, also author of the sCO2_exergy original) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@e635c85 — verified against the TESPy run and the published table |

## Problem statement

Reproduce the design point of the sCO2 recompression cycle of Penkuhn &
Tsatsaronis (2018): a 100 MW net power cycle with a main compressor and a
recompressor (both eta_s = 0.85), a turbine (eta_s = 0.9), two counterflow
recuperators (lower terminal temperature difference 5 K each), a water cooler
and a heater. Compressor 1 inlet at 35 °C / 75 bar, turbine inlet at 600 °C /
250 bar; the pressure at every state is imposed as in the original; the split
of the flow leaving recuperator 1 between the cooler branch and the
recompressor is an unknown, fixed by the condition T_11 = T_12 (the recompressor
discharge and the recuperated stream have the same temperature at the merge),
which is how the original imposes it (`c11.set_attr(T=Ref(c12, 1, 0))`).

## Model

Topology (state numbers = TESPy connection labels; state 0 = state 4 through
the cycle closer):

```
heater ->(04) turbine ->(05) recuperator 2 (hot) ->(14) recuperator 1 (hot) ->(15) splitter
 splitter ->(06) cooler ->(01) compressor 1 ->(02) recuperator 1 (cold) ->(12) merge
 splitter ->(10) recompressor ->(11) merge ->(13) recuperator 2 (cold) ->(03) heater
```

Equations (all from the original, in TESPy notation):

- turbomachinery: isentropic efficiency, `eta_s*(h_in - h_out,s) = h_in - h_out`
  (turbine) and `eta_s*(h_out - h_in) = h_out,s - h_in` (compressors);
- recuperators: hot-side/cold-side energy balance and lower terminal
  temperature difference `T_hot,out - T_cold,in = 5 K`;
- splitter: enthalpy and pressure equality, mass balance; merge: mass and
  energy balance, pressure equality, `T_11 = T_12`;
- power train: `W_net = eta_gen*W_turb - (W_cp1 + W_cp2)/eta_motor` with
  `eta_motor = 0.97*0.98`, `eta_gen = 0.99*0.99` (motor and generator
  electrical/mechanical efficiencies of the original);
- exergy: thermomechanical split of the publication,
  `e_T = (h - h(T_amb, p)) - T_amb_K*(s - s(T_amb, p))`,
  `e_M = (h(T_amb, p) - h(T_amb, p_amb)) - T_amb_K*(s(T_amb, p) - s(T_amb, p_amb))`.

The **sectioned recuperators** (`SectionedHeatExchanger(num_sections=10)`) are
reproduced as post-processing (the UA is a result, not a specification, in this
design): each recuperator is divided into `n_sec = 10` sections of equal heat;
the enthalpies and pressures of each section boundary are interpolated linearly
between the ends, temperatures are evaluated from `(p, h)`, and the section
conductance is `UA_i = (Q/n_sec)/LMTD_i` with the LMTD of the two boundary
temperature differences (function `Lmtd`). The total `UA_rec1`/`UA_rec2` is the
sum of the sections — the same calculation as TESPy `SectionedHeatExchanger`
(`calc_UA`, sections of equal heat), except that TESPy evaluates the LMTD with
a smoothed formulation (Quoilin 2011) where CoolSolve uses the standard
logarithmic mean (difference 0.04 % on `UA_rec1`, see Verification).

Fluid: R744 (CoolProp `CO2` of the source). The heater and cooler are simple
heat sources/sinks with imposed pressures (their pressure drops are implied by
the imposed state pressures, as in the original).

Inputs and outputs:

| Input | Value | Output | Design-point value |
|---|---|---|---|
| T_1, P_1 | 35 °C, 75 bar | eta_th | 0.4065 |
| P_2 | 258.4 bar | Q_heater | 245.97 MW |
| P_3 | 257 bar | m_15 (total flow) | 1177.78 kg/s |
| T_4, P_4 | 600 °C, 250 bar | y_split = m_10/m_15 | 0.2721 |
| P_5 | 77.95 bar | W_turb | 188.83 MW |
| P_6 | 75.15 bar | W_cp1 / W_cp2 | 45.15 MW / 35.72 MW |
| P_11 (states 11, 12, 13) | 257.51 bar | UA_rec1 | 21.71 MW/K |
| P_14 | 76.94 bar | UA_rec2 | 18.91 MW/K |
| eta_s_t, eta_s_c1, eta_s_c2 | 0.9, 0.85, 0.85 | | |
| dT_ttd | 5 K | | |
| W_net | 100 MW | | |

## How to run

```bash
coolsolve models/cycles/gas_turbines/sco2_recompression_brayton/sco2_recompression_brayton.eescode
```

No `.initials` needed (converges from CoolSolve defaults, 54 iterations,
largest block 8). The optimisation and sensitivity parts of the notebook
(TIT/compressor-inlet sweeps, split-ratio study, NSGA-II Pareto of efficiency
vs UA) are out of scope of this card: run them as GUI parametric studies on
`T_4`, `T_1`, `P_1`, `dT_ttd` or `n_sec` (when lowering the split-ratio limit,
impose the pinch instead of `dT_ttd` as in the notebook to keep the solution
physical).

## Results

Design point (CoolSolve, `.sol` baseline):

| State | T [°C] | p [bar] | e_T [kJ/kg] | e_M [kJ/kg] |
|---|---:|---:|---:|---:|
| 1 | 35.00 | 75.00 | 7.59 | 198.46 |
| 2 | 123.23 | 258.40 | 34.84 | 218.09 |
| 3 | 433.69 | 257.00 | 231.40 | 217.95 |
| 4 | 600.00 | 250.00 | 362.95 | 217.24 |
| 5 | 457.14 | 77.95 | 213.96 | 198.80 |
| 6 | 128.23 | 75.15 | 33.55 | 198.48 |
| 10 | 128.23 | 75.15 | 33.55 | 198.48 |
| 11 | 264.14 | 257.51 | 116.42 | 218.01 |
| 12 | 264.14 | 257.51 | 116.42 | 218.01 |
| 13 | 264.14 | 257.51 | 116.42 | 218.01 |
| 14 | 269.14 | 76.94 | 95.95 | 198.69 |
| 15 | 128.23 | 75.15 | 33.55 | 198.48 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![T-s diagram of the cycle](figures/sco2_recompression_brayton_ts.png)  + one-line caption -->

## Verification

Two independent references, both compared with `tools/compare_solution.py`
(script `compare_solution.py <model>.sol <reference>.csv`; reference CSVs and
the TESPy run script lived in the work folder, deleted after the import):

1. **TESPy run** of `docs/model_library/sco2.ipynb` (commit `19425523`,
   throw-away venv: TESPy 0.11.3.dev0, CoolProp 8.0.1, Python 3.12; script
   re-running the notebook's design point and dumping every connection state):
   **69 common variables, 0 differ (rtol=0.001)**, maximum relative difference
   4.3e-4 on `UA_rec1` (TESPy smoothed LMTD vs standard LMTD, see Model).
2. **Published table** of Penkuhn & Tsatsaronis (2018), as embedded in the
   notebook (T, p, e_T, e_M of the 12 states): **48 values, 0 differ
   (rtol=0.001)**, maximum relative difference 7.5e-4 on `e_T[5]` (the
   published values are rounded to 2 decimals). Temperatures agree within
   0.19 K (worst state 5), the same deviation the TESPy run itself shows
   against the publication (property-library version), and pressures/efficiency
   agree exactly.

The mechanical exergy of the publication is reproduced within 0.01 kJ/kg here;
the notebook notes a larger deviation for the *exerpy* implementation, which
comes from its reference-state choice, not from the cycle model.

## Source and attribution

- Original model: Francesco Witte, *Exergy analysis of supercritical CO2
  power cycles*, sCO2_exergy, https://github.com/fwitte/sCO2_exergy (MIT);
  validated data: J. Penkuhn, G. Tsatsaronis, *A thermodynamic analysis and
  comparison of two detailed sCO2 Brayton cycle configurations*, 6th
  International Symposium on Supercritical CO2 Power Cycles, 2018.
- Translation source: TESPy model library, `docs/model_library/sco2.ipynb`,
  commit `19425523`, https://github.com/oemof/tespy (MIT), TESPy 0.11.3.dev0.
- Published under the CoolSolve Library license (MIT).

## Conversion log

- **2026-10-14 — import (T-TRANSLATE)**: TESPy network (components,
  `Connection`s, power bus, iterative Newton solver) translated into
  simultaneous equations; `PropsSI`/TESPy property calls become CoolSolve
  `enthalpy`/`entropy`/`temperature` calls on R744 (CoolProp `CO2` → EES
  real-fluid name per workflow §5); units SI-°C-Pa-J (source SI-K-Pa-J with
  display units bar/°C/MW); the TESPy `Ref(c12, 1, 0)` temperature reference
  becomes `T_11 = T_12`; splitter/merge equalities written explicitly; the
  power bus becomes one net-power equation with the motor/generator
  efficiencies (the individual bus powers are results, as in the original).
- **2026-10-14 — sectioned recuperators**: the 10-section discretisation
  (post-processing UA) written as two `DUPLICATE` loops per recuperator,
  sections of equal heat, linear interpolation of enthalpies and pressures,
  LMTD per section (function `Lmtd`). Both boundary states of each section are computed per section from the fractions
  `(i-1)/n_sec` and `i/n_sec`.
- **2026-10-14 — exergy**: the published thermomechanical exergy split
  reproduced with the ambient state of the original class
  (`T_amb = 15 °C`, `P_amb = 1.01325 bar`).
- **2026-10-14 — dependencies**: the card's dependencies are not needed at the
  design point: the turbine runs at its design isentropic efficiency (Stodola
  cone law of C-180/CSL for off-design, not used), and the heater is a simple
  heat source (no combustion, C-184/`cpbar` not used).
- **Level**: equations 486 → 2, largest block 8 → 1, functions/`DUPLICATE` → 1,
  ≥ 3 coupled components (cycle) → 1, no off-design/calibration → 0, no
  curated guesses → 0; score 5 → **level 3** (matches the inventory guess).

## Limitations and CoolSolve gaps

- Design point only: the turbomachinery efficiencies are constant; off-design
  behaviour (Stodola, compressor maps) is out of scope, see Related models.
- The recuperator UA uses the standard LMTD; TESPy's smoothed LMTD
  (Quoilin 2011) differs by 0.04 % here (documented above), and the pinch
  detection of the original (`td_pinch`) is not reproduced (not a
  specification of this design point).
- No CoolSolve gap blocks the model.

## Related models

- CSL-0013 (`heat_pump_basic_tespy`): the TESPy translation pilot; same
  translation rules (property calls, component equations).
- CSL-0014 (`hx_constant_pinch`): recuperators specified by a pinch/terminal
  temperature difference, as here.
- CSL-0038 (`orc_co2_polynomial_maps`): the other CO2 power cycle of the
  library (transcritical ORC with polynomial compressor/turbine maps).
- CSL-0317 (`pseudo_critical_properties`): pseudo-critical temperature and pseudo-boiling bounds of R744 against pressure (the main compressor inlet of this cycle, 35 C at 75 bar, lies 3.2 K above the pseudo-critical temperature of 31.77 C computed there at 75 bar).
