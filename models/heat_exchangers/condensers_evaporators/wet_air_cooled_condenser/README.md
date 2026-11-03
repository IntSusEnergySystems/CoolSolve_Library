# Wet air-cooled condenser (spray evaporative cooling)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0032`

An air-cooled condenser operating in wet regime (spray evaporation cooling).
Given the condenser duty and the inlet/outlet air conditions, the model
determines the overall heat transfer coefficient (`AU_f`), the fictitious
heat capacity rate (`C_dot_a_f`), the air mass flow rate and the
spray/condensate water flow rate. The air side is treated as a fictitious dry
fluid whose temperatures are the wet-bulb temperatures (as in the original
exercise), closed by an effectiveness–NTU relation.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | AirH2O (humid air) |
| **Size** | 27 equations (largest block: 2), incl. 6 post-processing state points |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 5, exercise 3 (SB solution, EES file `MSTh-SB-R5-Ex3.EES`); CoolSolve example `condenser_wet` |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

An air-cooled condenser is operated with evaporative spray cooling of the
air. The condenser duty is 35 kW; air enters at 25 °C, 60 % relative
humidity, 1 atm, and leaves saturated at 30 °C; the condensing temperature is
45 °C. The parameters assumed constant (as in the original) are the contact
effectiveness ε_c = 1, `NTU_f` = 0.532 and `C_dot_a_f` = 3322 W/K. Determine
the overall heat transfer coefficient `AU_f`, the fictitious capacity rate,
the air mass flow rate and the spray/condensate water flow rate.

## Model

- **Fictitious dry fluid on wet-bulb temperatures** (as in the original):
  `Q_dot_cd = C_dot_a_f (T_wb_ex − T_wb_su)`, with the wet-bulb temperatures
  of the inlet/outlet air (`WETBULB(AirH2O, …)`);
- **effectiveness–NTU closure**: `Q_dot_cd = ε_cd_f C_dot_a_f (T_cd − T_wb_su)`,
  `ε_cd_f = 1 − exp(−NTU_f)`, `NTU_f = AU_f/C_dot_a_f` — the same structure as
  a dry exchanger exchanging with a fluid at the wet-bulb temperature;
- **air mass flow rate**: energy balance
  `Q_dot_cd = M_dot_a (h_a_ex − h_a_su) − M_dot_cd c_pw T_w_cd` with the
  humidity balance `M_dot_cd = M_dot_a (w_su − w_ex)`, moist-air states from
  `HUMRAT`/`ENTHALPY(AirH2O, …)` and c_pw = 4187 J/(kg·K) (as in the original).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `Q_dot_cd` duty | 35 kW | `AU_f` overall conductance | 1767.5 W/K |
| `T_a_su` / `RH_su` | 25 °C / 0.6 | `C_dot_a_f` capacity rate | 3323.0 W/K |
| `T_a_ex` / `RH_ex` | 30 °C / 1 (saturated) | `M_dot_a` air flow | 0.7394 kg/s |
| `T_cd` condensing temperature | 45 °C | `M_dot_cd` spray/condensate flow | −0.01137 kg/s |
| `P_su` | 101325 Pa | `T_wb_su` / `T_wb_ex` | 19.467 / 30 °C |
| `NTU_f` (guess, as in the original) | 0.532 | `epsilon_cd_f` | 0.4125 |

The negative `M_dot_cd` comes from the sign convention of the original
(`M_dot_cd = M_dot_a (w_su − w_ex)`): the air leaves saturated, so
`w_ex > w_su`. The original states the values `M_dot_a` = 0.7398 kg/s and
`C_dot_a_f` = 3322 W/K in its comments; they agree with the computed
solution to 0.05 %.

Two alternative closures of the original are kept **commented out, as in the
original**: a mass-transfer effectiveness formulation (ε_c applied to the
enthalpy and humidity differences) and an LMTD formulation on the wet-bulb
temperatures.

## How to run

Open `wet_air_cooled_condenser.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./wet_air_cooled_condenser.eescode
```

No guess values are needed (`.initials` not required).

## Results

| `AU_f` [W/K] | `C_dot_a_f` [W/K] | `M_dot_a` [kg/s] | `M_dot_cd` [kg/s] | `T_wb_su` [°C] | `epsilon_cd_f` [-] |
|---:|---:|---:|---:|---:|---:|
| 1767.5 | 3323.0 | 0.7394 | −0.01137 | 19.467 | 0.4125 |

The arrays `T[i]`, `w[i]`, `h[i]` (i = 1 supply, 2 exhaust) give the air-side
states for post-processing (CoolSolve has no psychrometric chart yet,
`CS-FEAT-PSYCHRO`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. AU_f and M_dot_a vs T_a_ex or RH_su (Parametric tab) -->

## Verification

Reference: the solution stored in the original EES file
(`MSTh-SB-R5-Ex3.EES`, EES 7.458), compared with
`tools/compare_solution.py`:

> 15 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 12

Maximum relative difference 7.4·10⁻⁴, on `w_ex` (EES 0.0273125, CoolSolve
0.0273329 kg/kg dry air); it traces back to the humid-air formulation
(CoolProp humid air vs EES 7.4 psychrometrics), within the property tolerance
of CoolSolve `docs/ees_import.md` §11. The other stored variables (wet-bulb
temperatures, enthalpies, humidity ratios, inputs) agree to better than
2·10⁻⁴. The 12 CoolSolve-only variables are the results whose values EES had
cleared in the stored solution (their last-solution **guesses** are still in
the file) plus the state-point arrays; they match those guesses (`AU_f`
1767.45, `C_dot_a_f` 3322.28, `M_dot_a` 0.7398, `NTU_f` 0.532,
`epsilon_cd_f` 0.41257, `M_dot_cd` −0.011371) to 5·10⁻⁴.

## Source and attribution

Exercise solution by **Stéphane Bertagnolio** (ULiège Thermodynamics
Laboratory) for the course *Machines et systèmes thermiques* (repetition 5,
exercise 3), identified from the file title (`SB` initials); the file itself
names no author.

Source file (EES 7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 05/MSTh-SB-R5-Ex3.EES`
(inventory candidate `TM-0079`). The CoolSolve example
`examples/condenser_wet.eescode` is a verbatim transcription of the same file
with the comments translated to English (equation diff: identical); the
example stays in the CoolSolve repository as a test case.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on
  `MSTh-SB-R5-Ex3.EES`): unit system already SI-°C-Pa-J (no conversion); the
  EES licence tag (`Laboratoire de Thermodynamique, U. de Liege`, the lab
  licence, not the author) removed; no tables; functions called
  (`WETBULB`, `HUMRAT`, `ENTHALPY`, `exp`) are all CoolSolve built-ins.
- **2026-10-05 — curation**: standard header added, comments translated from
  French to English, units added to every dimensional quantity, one equation
  per line. No change to any equation or value; the two commented-out
  alternative closures of the original are kept, marked "as in the original".
- **2026-10-05 — state points**: 6 post-processing equations (`T[i]`, `w[i]`,
  `h[i]`, i = 1 supply, 2 exhaust) added for the GUI array overlay; the model
  results are unchanged. Full `P/h/T/s` cycle arrays are not meaningful for a
  single-component humid-air model without a psychrometric chart.
- **Level**: 21 model equations (27 with state points, largest block 2) score
  0 in the taxonomy §3 table (< 50 equations, block ≤ 5, no special
  structure/numerics); rated level 2 (+1, within the ±1 rule) for the
  psychrometric property calls and the fictitious wet-bulb-fluid
  representation, in line with the level of the source inventories.

## Limitations and CoolSolve gaps

- The fictitious-fluid treatment on wet-bulb temperatures with a single
  `AU_f` is a coarse representation of the wet air side (no separate
  sensible/latent conductances); ε_c = 1 (contact effectiveness) is assumed.
- `cp_w` = 4187 J/(kg·K) constant (as in the original).
- No blocking CoolSolve gap. Note: CoolSolve emits the spurious input hint
  *"T=30 looks like Fahrenheit"* on the `WETBULB(AirH2O, T=30, …, R=1)` call
  (registered false positive `CS-BUG-HINT-FAHRENHEIT`, harmless: results
  unaffected).

## Related models

- `CSL-0008` *condenser_three_zones*: three-zone model of the same component
  in dry operation (R134a/air, desuperheating/condensing/subcooling).
- `CSL-0030` *two_speed_cooling_tower*: same fictitious dry-fluid treatment
  on wet-bulb temperatures, for a direct-contact cooling tower.
