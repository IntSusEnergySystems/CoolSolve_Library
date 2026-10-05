# Gas turbine with reheat (intercooler and regenerator)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0060`

A two-shaft ideal-gas turbine (air as ideal gas) with two compression stages
and a water-cooled intercooler, a regenerator, a main combustion chamber, an HP
turbine that drives both compressors, a **second (reheat) combustion chamber**
between the turbine stages and an LP turbine that expands to the ambient
pressure. The exercise asks for the extra fuel consumption due to the reheat
and its effect on the cycle efficiency. The LP expansion to `p_amb` maximises
the LP turbine power, as in the original.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines |
| **Fluid** | Air (ideal gas) |
| **Size** | 94 equations, system square, largest block 14 |
| **Source** | ULiège — course *Thermodynamique appliquée* (THD10), repetition session 7, exercise 4 (EES file `THD10_R07_E4.EES`; 2010 exercise reused in 2022-2023) |
| **Authors** | TBD (ULiège course MECA0002; the source inventory suggests S. Quoilin with repetition assistants N. Paulus and B. Dechesne) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; verified against the EES stored solution (see *Verification*) |

## Problem statement

A gas turbine of the previous exercise (two compression stages with
intercooler, regenerator, TIT 1250 K) is modified: a second combustion chamber
of efficiency 0.98 is added between the two turbine stages, and the gas leaves
it at 1250 K as well. Calculate the extra fuel consumption and the effect of
this modification on the cycle efficiency. Air (100 kg/s at 20 °C, 1 bar)
is treated as an ideal gas; each compression has a pressure ratio of 4 and a
polytropic efficiency of 0.83; the turbines have the same polytropic
efficiency; kerosene LHV 43.1 MJ/kg; mechanical efficiency 0.95, alternator
efficiency 0.95; intercooler effectiveness 0.9 (25 l/s of cooling water entering
at 20 °C), regenerator effectiveness 0.7.

## Model

- **Stations 1–2 / 3–4**: each compressor, `p_out = pi_c·p_in`, polytropic
  relation `(T_out+273)/(T_in+273) = pi_c^((gamma-1)/(gamma·eta_c))` with
  `gamma = cp/cv` evaluated at the compressor inlet.
- **Intercooler (2→3)**: isobaric; effectiveness 0.9 on
  `Q_dot_max = min(C_dot_air, C_dot_eau)·(T[2] - T_su_eau)`; the heat taken by
  the water gives its outlet temperature.
- **Regenerator (4→5 air side, 9→10 gas side)**: isobaric, effectiveness 0.7 on
  the maximum power with the minimum heat-capacity rate.
- **Main combustor (5→6)** and **reheat combustor (7→8)**: isobaric,
  `T = TET = 1250-273` (°C, i.e. 1250 K, as in the original); first law on the
  gas flow with combustion efficiency 0.98 gives the fuel flows `q_m_e`,
  `q_m_e2` (the gas mass flow grows by the injected fuel).
- **HP turbine (6→7)**: the shaft balance
  `eta_m·W_dot_t1 + W_dot_c1 + W_dot_c2 = 0` fixes its enthalpy drop; the
  polytropic relation then gives `p[7]`.
- **LP turbine (8→9)**: expands to `p_amb`; it drives the alternator alone,
  `W_dot_el = eta_alt·eta_m·q_m_p2·(h[8] - h[9])` (through `W_dot_alt`).
- **Results**: `eta_tg = W_dot_el/(Q_dot_b + Q_dot_b2)` and
  `deltaq_m_e = q_m_e2/q_m_e·100` (reheat fuel as % of the main-chamber fuel).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `q_m_a` air flow | 100 kg/s | `eta_tg` cycle efficiency | 0.3265 |
| `pi_c` (per stage) | 4 | `deltaq_m_e` extra fuel (reheat/main) | 80.8 % |
| `TET` | 977 °C (1250 K) | `W_dot_el` net power | 30.48 MW |
| `eta_c` = `eta_t` polytropic | 0.83 | `q_m_e` / `q_m_e2` fuel flows | 1.198 / 0.968 kg/s |
| `eta_ic` / `eta_rec` | 0.9 / 0.7 | `p[7]` between the turbines | 3.35 bar |
| `eta_b` / `eta_m` / `eta_alt` | 0.98 / 0.95 / 0.95 | `T[9]` exhaust | 706.4 °C |

With reheat the efficiency drops below the exercise-3 value (0.3389 stored in
E3: the additional heat enters at a lower mean temperature while the extra LP
work is limited by the ambient back-pressure), but the specific work increases:
the reheat chamber burns an additional fuel flow equal to 80 % of the
main-chamber flow (`deltaq_m_e` = 80.8 %) for a modest power gain — the
physical conclusion of the exercise.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): ideal-gas model — parametric sweep plot,
     e.g. eta_tg vs pi_c (CoolSolve *Parametric* tab; decision D7: no ideal-gas diagram yet, CS-FEAT-DIAGRAM-IDEAL) -->

## How to run

Open `gas_turbine_reheat.eescode` in the CoolSolve GUI and press *Solve*, or
from a terminal:

```bash
coolsolve ./gas_turbine_reheat.eescode
```

The model converges from CoolSolve's default guesses (no `.initials` needed).

## Verification

Solved unchanged and compared with the EES stored solution of the source file
(98 variables; EES kPa/kJ units converted by `compare_solution.py --ees-units`):

- **Reference-state offsets** (not errors): absolute `h` and `s` of EES
  ideal-gas `Air` and CoolProp `Air` have different zeros — offsets of
  ≈ 126 kJ/kg on `h[i]` and ≈ 1814 J/kg-K on `s[i]`, constant over all states.
  As printed by `compare_solution.py`, the maximum relative difference over all
  common variables is **3.40e-01** (`s[3]`); absolute `h`/`s` are therefore
  excluded from the verdict (named here: all `h[i]`, `h[10]` and `s[i]`,
  `s[10]` absolute values).
- **Derived results** (temperature rises, powers, fuel flows, efficiency) agree
  within **9.8e-03** (`eta_tg`: 0.329688 EES vs 0.326467 CoolSolve;
  `deltaq_m_e`: 80.14 % vs 80.82 %; `W_dot_el`: 30.68 vs 30.48 MW). This is
  above the same-EOS tolerance and explained by the different air property
  backends (EES ideal-gas polynomials vs CoolProp pseudo-pure Air): a
  0.1–0.2 % difference on `gamma` (1.4001 vs 1.4020) is amplified by the
  polytropic exponents. Within the "different equation of state" band of
  CoolSolve `docs/ees_import.md` §11 (a few %), explained.
- `TET` is reported as DIFF by `compare_solution.py` for a documentation reason:
  the unit annotation stored by EES for `TET` ("K") contradicts the file's own
  equations (`T[6] = TET` and `T[6]` stored as 977 °C): the annotation is wrong,
  not the value. `TET = 977` °C in both.

Status **verified** on the derived results.

## Source and attribution

Exercise of the ULiège course *Thermodynamique appliquée* (MECA0002, THD10),
repetition session 7, exercise 4 (files THD10_R07_E1–E4, written for the 2010
course, reused in 2022-2023). The EES file carries the ULiège Thermodynamics
Laboratory student/staff licence stamp and names no author; the source
inventory attributes the family to S. Quoilin with repetition assistants
N. Paulus and B. Dechesne — left as TBD for the maintainer.

Source file (EES 8.423, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R6/autres exo/THD10_R07_E4.EES`
(inventory candidate `TM-0435`, duplicate group DG-0104).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): EES 8.423, unit system
  `SI MASS DEG KPA C KJ` + decimal comma (converted to dot by the tool).
  Manual conversion to SI-°C-Pa-J (CoolSolve `docs/ees_import.md` §6):
  `p_amb = 100E3 Pa` (100 kPa), `PCI = 43.1E6 J/kg` (43.1e3 kJ/kg),
  `C_eau = 4187 J/kg-K` (4.187 kJ/kg-K); pressures, enthalpies, entropies,
  `cp`/`cv`, heat-capacity rates, powers and heat rates all change unit
  consistently through the property calls, and no equation mixes units or
  carries an explicit factor 1000 — balances are unchanged. The absolute
  temperature relations keep the original's `+273` offset (not 273.15) and
  `TET = 1250-273` stays as written: the results are the original's.
  `.initials` converted from the EES stored solution (pressures/energies
  ×1000); the model also converges from CoolSolve's default guesses.
- **2026-10-05 — curation**: comments translated to English (paraphrase of the
  original), standard header added, one truncated comment of the original
  (`"*cp_45 * (T[5] - T[4])"` left over from an earlier version of the file)
  dropped as dead text. Variable names kept (`q_m_e`, `TET`, `exposant1`…).
- **Duplicate group DG-0104** (decision D4): the session builds the same
  machine progressively — E1 (`TM-0522`) simple cycle (no intercooler, no
  regenerator, no reheat), E2 (`TM-0523`) + intercooler, E3 (`TM-0524`)
  + regenerator, E4 (this model, `TM-0435`, representative) + reheat. The
  equations of E1–E3 are subsets of E4's, except that E1–E2 write the polytropic
  relations in logarithmic form (`eta_c·ln(T2/T1) = (gamma-1)/gamma·ln(pi_c)`)
  and E1–E3 keep `q_m_p` (no second fuel flow) in the LP turbine power. Not
  value-changed copies: parameter/structure variants → `merged` in the
  inventory, documented here; the simpler configurations can be reproduced by
  setting `eta_ic`/`eta_rec` thought is not faithful (they remove equations),
  so they are not shipped as files.
- **Level**: score 1 (94 equations) + 2 (block of 14) + 1 (arrays) + 1 (≥ 3
  coupled components) + 0 + 0 = 5 → level 3, moved to level 2: complete cycle
  with explicit textbook relations and small implicit loops, converging from
  default guesses (taxonomy.md §3 allowance).

## Limitations

- Air is treated as an ideal gas with variable `cp`; the fuel mass is accounted
  for in the gas flow (`q_m_p = q_m_a + q_m_e`) but the combustion products are
  represented by the same `Air` fluid, as in the original.
- The unit annotation of `TET` in the EES variable information ("K") is
  inconsistent with the file itself (see *Verification*); the model uses °C
  throughout.

## Related models

- `CSL-0050` *gas_turbine_two_shaft_intercooled_regenerative*: the same
  intercooled + regenerative two-shaft architecture, without reheat.
- `CSL-0011` *two_shaft_gas_turbine_compressor_map*: two-shaft gas turbine with
  a compressor map (off-design instead of design point).
