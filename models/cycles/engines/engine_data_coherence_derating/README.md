# Engine data-sheet coherence check and ISO 3046-type derating

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0273`

Worked example from the ULiège course *Moteurs à combustion interne* (MCI,
Prof. Ph. Ngendakumana): the instructor solution ("RD") of a diesel-engine
problem first checks the internal coherence of a data sheet (swept volume,
mean piston speed, shaft power from the torque, charge-air cooler duty,
exhaust flow), then computes the engine thermal efficiency, the excess air,
the volumetric efficiency and the compressor isentropic efficiency, and
finally derates the engine to the site conditions of Lac Victoria
(ISO 3046-type correction) and estimates its CO2 emissions per distance.
All equations are as in the original; published as an example.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas) |
| **Size** | 72 equations (largest block: 3) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/Examen/resolultion_RD.EES` (TM-0223) |
| **Authors** | Rémi Dickes, Ph. Ngendakumana (ULiège) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (see verification field) |

## Problem statement

A 5-cylinder diesel engine (bore 130 mm, stroke 140 mm, 2100 rpm, torque
1337 N.m, 294 kW gross shaft power) has a data sheet that must be checked for
internal coherence: computed swept volume, mean piston speed, shaft power,
charge-air cooler duty and exhaust flow against the tabulated values. From the
fuel consumption (209 g/kWh) and the heat flows (226 kW coolant, 204 kW
exhaust, 15 kW environment, LHV 42.75 MJ/kg) the thermal efficiency and the
energy-balance residual are computed; the fuel is C12H26 (excess air), the
volumetric efficiency is taken from the measured intake air flow, and the
compressor (pressure ratio 2.5, inlet 25 °C, outlet 165 °C) gets an isentropic
efficiency. Last, the engine runs at Lac Victoria (1133 m, 30 °C): derate the
shaft power with the ISO 3046-type law (exponents m = 0.7, n = 1.2,
mechanical efficiency 0.85) and estimate the CO2 emissions in g/km at a ship
speed of 25 knots.

## Model

Faithful transcription of the instructor solution; all equations unchanged,
comments translated. Blocks (sections of the original):

1. **Data coherence**: V_s = n_s·π·d²/4·L vs 9.3 L; C_m = 2·L·N/60 vs 9.8 m/s;
   W_dot_gr = C·2π·N/60 vs 294 kW; Q_dot_air = m_dot_air·cp(T_mean)·ΔT vs 49 kW;
   m_dot_ex = m_dot_air + m_dot_fuel vs 26 kg/min.
2. **Questions**: clearance fraction from rv = V_bdc/V_tdc; design parameters
   L_star = L/d and N_star = (N/60)·(W_dot/n_s)^0.5; thermal efficiency
   η_mot = W_dot/(m_fuel·PCI) and from the heat balance; balance residual;
   excess air from the stoichiometric ratio of C12H26; volumetric efficiency
   from the theoretical air flow; compressor isentropic efficiency from the
   isentropic enthalpy rise (ideal-gas air, absolute h and s of the property
   backend, differences only).
3. **Site derating**: atmospheric pressure from the barometric formula of the
   original; K = (P/P_ref)^m·(T/T_ref)^n with m = 0.7, n = 1.2;
   α = K − 0.7·(1−K)·(1/η_m − 1) (same law as CSL-0151); derated power and
   CO2 emission per distance from the site air density.

Inputs are the data-sheet values of the original (kept in their original
units: rpm, N.m, kW, °C, m). Unknowns are solved simultaneously; the system is
square (72 equations, 72 variables) and needs no curated guesses.

## How to run

```bash
coolsolve ./engine_data_coherence_derating.eescode
```

`.initials` carries the EES stored solution as guesses (the model also solves
from the default guesses, 9 iterations). No variants, no `coolsolve.conf`.

## Results

| Quantity | Value (CoolSolve) | EES | Note |
|---|---:|---:|---|
| V_s | 0.0092913 m³ | 0.0092913 | data sheet: 0.0093 m³ |
| C_m | 9.800 m/s | 9.800 | data sheet: 9.8 m/s |
| W_dot_gr | 294022 W | 294022 | data sheet: 294 kW |
| Q_dot_air | 49748 W | 49700 | data sheet: 49 kW (cp of air, EES vs CoolProp) |
| rel_vc | 0.05556 | 0.05556 | clearance volume fraction |
| eta_mot | 0.4029 | 0.4029 | from the fuel consumption |
| eta_mot_bis | 0.3978 | 0.3978 | from the heat balance |
| res_bilan | −0.0128 | −0.0128 | −1.28 % of the LHV |
| e | 0.6334 | 0.6334 | excess air |
| epsilon_v | 2.1924 | 2.1930 | > 1, as in the original (data-sheet air flow) |
| epsilon_s_cp | 0.6330 | 0.6334 | compressor isentropic efficiency |
| alpha_detarage | 0.9292 | 0.9292 | derating factor at Lac Victoria |
| W_dot_victoria | 273175 W | 273175 | derated shaft power |
| emission_CO2 | 298.36 g/km | 298.39 | at 25 knots |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. a parametric
     plot of the derating factor alpha_detarage vs the site temperature,
     saved in figures/engine_data_coherence_derating_derating.png -->

## Verification

Compared with the EES stored solution of `resolultion_RD.EES` (72 variables,
EES X9.721) with `tools/compare_solution.py`: **72 common variables, 5 differ
(rtol=0.001); only in EES: 0; only in CoolSolve: 1** (the constant `pi`).
The 5 differing variables are the *absolute* air enthalpy and entropy of the
ideal-gas backend (`h_su_cp`, `h_ex_cp`, `h_ex_cp_s`, `s_su_cp`, `s_ex_cp_s`;
reference-state offset of CoolProp's Air vs the EES air tables, 22–32 %);
they cancel in the only quantities that use them (the differences
h_ex_cp_s − h_su_cp and h_ex_cp − h_su_cp give `epsilon_s_cp` 6.0e-4 and
`T_ex_cp_s` 0.1 K). Excluding them, the maximum relative difference is
**9.82e-4 on `Q_dot_air`** (cp of air at ~106 °C: CoolProp vs the EES tables);
the next ones are `T_ex_cp_s` 9.4e-4 and `epsilon_s_cp` 7.0e-4. All other 64
common variables agree to < 2.6e-4 (mostly exact).

## Source and attribution

- Source file: `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/Examen/resolultion_RD.EES`
  (inventory candidate TM-0223), instructor solution of the June 2019 MCI exam
  problem by Rémi Dickes; EES licence stamp of the ULiège Thermodynamics
  Laboratory (J. Lebrun lab licence). Published as an example per the
  collection's publication decision (`sources/thermo_models/README.md`).
- Authors: Rémi Dickes (solution, tag "RD"), Ph. Ngendakumana (course).
- The ISO 3046-type derating law and the barometric formula match the library
  model CSL-0151 *engine_derating_iso3046* (full ISO table with humidity and
  coolant terms; here the reduced pressure/temperature form with the
  charge-air-cooled exponents).

## Conversion log

- `$UnitSystem SI MASS DEG PA C J` removed (CoolSolve's fixed unit system;
  no conversion needed, the file was already in SI-°C-Pa-J).
- Header added; comments translated to English and given SI units; equations
  untouched (only whitespace around some operators was normalised, e.g.
  `T_su_cp =T_air_su` → `T_su_cp = T_air_su`).
- `L_star = L/D` keeps the case-insensitive `D` of EES (= d, the bore; the
  stored solution confirms L_star = 0.14/0.13 = 1.0769).
- Level: score 1 (equations 50–300 → 1; largest block ≤ 5 → 0; no procedures,
  no multi-zone, no calibration, no curated guesses) → level 1.
- The original header stamps the file as an exam resolution; per the
  maintainer decision on exams (`sources/thermo_models/README.md`) it is
  published here as a worked example.
