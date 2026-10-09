# Chilled-water air cooling coil, dry and wet regimes

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0017`

A chilled-water air cooling coil fed with 1 kg/s of air at 30 °C and 50 %
relative humidity and 2 kg/s of water at 5 °C. The coil is described by its
three thermal resistances in series (air side, wall, water side). The model
first computes the dry regime with the counterflow epsilon-NTU relation and
checks the condensation risk at the dry-regime outlet; the outlet relative
humidity exceeds 100 %, so the coil actually runs wet. The wet regime is then
computed with the wet-bulb-based (fictitious-capacity) effectiveness, and the
outlet air state follows from the contact (bypass) factor at the saturated
coil-surface state, giving also the condensate flow rate.

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | AirH2O (moist air), Water (chilled water) |
| **Size** | 60 equations, implicit (largest block: 23) |
| **Source** | ULiège MSTh exercise (SB solution) + CoolSolve example `cooling_coil` |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory, SB solution); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs with the shipped `.initials`; import verified against the solution stored in the original EES file |

## Problem statement

A chilled-water air cooling coil has the following data (as in the
original):

- resistances: `R_a = 0.5e-3`, `R_m = 0.1e-3`, `R_w = 0.3e-3 m2-K/W`;
- air: `M_dot_a = 1 kg/s` at `T_a_su = 30 °C`, `RH_su = 50 %`, `P = 101325 Pa`;
- water: `M_dot_w = 2 kg/s` at `T_w_su = 5 °C`.

Compute the dry-regime performance (counterflow epsilon-NTU), check whether
condensation occurs, compute the wet-regime performance and the outlet air
conditions (contact-factor method), and the condensate flow rate.

## Model

Dry regime (counterflow epsilon-NTU, as in the original):

- air- and water-side balances `Q_dot_dry = C_dot_a_dry·(T_a_su − T_a_ex_dry)`
  and `Q_dot_dry = C_dot_w_dry·(T_w_ex_dry − T_w_su)`, with the specific heats
  evaluated by EES property calls (`CP(AirH2O, …)`, `CP(Water, …)` at the mean
  temperatures — implicit loop);
- `Q_dot_dry = epsilon_dry·C_dot_min_dry·(T_a_su − T_w_su)` with the
  counterflow `epsilon_dry(NTU_dry, omega_dry)` and
  `1/AU_dry = R_a + R_m + R_w`;
- condensation check: `w_ex_dry = w_su`, `RH_ex_dry = RELHUM(…)` = 1.35 >
  1, so the coil runs wet.

Wet regime:

- air-side balance with the condensate enthalpy
  `Q_dot_wet = M_dot_a·(h_a_su − h_a_ex_wet) − M_dot_cd·cp_w_wet·T_cd`;
- wet-bulb-based effectiveness
  `Q_dot_wet = epsilon_wet_f·C_dot_min_wet_f·(T_wb_su − T_w_su)` with the
  fictitious capacity `C_dot_a_wet_f` and
  `R_a/R_a_f = cp_a_wet_f/cp_a_dry` (relation giving the fictitious air-side
  resistance `R_a_f`, as in the original);
- outlet air from the contact factor
  `epsilon_c = 1 − exp(−NTU_c)`, `NTU_c = 1/(R_a·C_dot_a_dry)`, applied to
  the enthalpies and to the humidity ratios against the saturated surface
  state (`T_c_wet`, `w_c_wet`), with the equivalent bypass-flow formulation
  (`epsilon_c_bis`) as a cross-check; condensate
  `M_dot_cd = M_dot_a·(w_su − w_ex_wet)`.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `R_a` / `R_m` / `R_w` | 0.5 / 0.1 / 0.3e-3 m2-K/W | `Q_dot_dry` / `Q_dot_wet` | 16.49 / 21.65 kW |
| `M_dot_a` at 30 °C, 50 % RH | 1 kg/s | `T_a_ex_dry` / `T_a_ex_wet` | 13.86 / 16.12 °C |
| `M_dot_w` at 5 °C | 2 kg/s | `T_w_ex_dry` / `T_w_ex_wet` | 6.96 / 7.58 °C |
| `P_a_su` / `P_w_su` | 101325 Pa | `RH_ex_dry` (→ wet) / `RH_ex_wet` | 1.35 / 0.90 |
| | | `epsilon_dry` / `epsilon_wet_f` / `epsilon_c` | 0.646 / 0.403 / 0.859 |
| | | `M_dot_cd` condensate | 2.98 g/s |

## How to run

Open `chilled_water_cooling_coil.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./chilled_water_cooling_coil.eescode
```

The 23-equation implicit block (mean-temperature property calls inside the
NTU loop) does not converge from default guesses (singular Jacobian), so the
shipped `.initials` file (EES stored solution) is required. No solver
configuration is needed; solution in 13 iterations.

## Results

| `Q_dot_dry` [kW] | `Q_dot_wet` [kW] | `epsilon_dry` [-] | `epsilon_wet_f` [-] | `epsilon_c` [-] | `M_dot_cd` [g/s] |
|---:|---:|---:|---:|---:|---:|
| 16.49 | 21.65 | 0.646 | 0.403 | 0.859 | 2.98 |

The dry-regime outlet would be at 13.86 °C with `RH_ex_dry = 1.35`
(supersaturated), so the coil runs wet: the air leaves at 16.12 °C and 90 %
relative humidity, the water warms from 5 to 7.58 °C, and 2.98 g/s of water
condense.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
      sweep plot, e.g. Q_dot_wet and M_dot_cd vs T_a_su or RH_su (Parametric tab).
      Psychrometric-chart overlays are not available in CoolSolve
      (CS-FEAT-PSYCHRO). -->

## Verification

Reference: the solution stored in the original EES file
`MSTh-SB-R5-Ex1.EES` (EES 7.458), compared with
`tools/compare_solution.py` (60/60 variables, no unit conversion — the
original is already SI-°C-Pa-J):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `Q_dot_dry` | 16486.4 W | 16487.4 W | 0.006 % |
| `Q_dot_wet` | 21638.8 W | 21650.3 W | 0.05 % |
| `epsilon_dry` / `epsilon_wet_f` / `epsilon_c` | 0.64550 / 0.40315 / 0.85881 | 0.64550 / 0.40312 / 0.85880 | ≤ 0.01 % |
| `T_a_ex_dry` / `T_a_ex_wet` | 13.863 / 16.121 °C | 13.862 / 16.125 °C | ≤ 0.02 % |
| `T_w_ex_dry` / `T_w_ex_wet` | 6.964 / 7.579 °C | 6.961 / 7.576 °C | ≤ 0.04 % |
| `h_a_su` / `h_a_ex_wet` | 64343 / 42503 J/kg | 64356 / 42503 J/kg | ≤ 0.02 % |
| `w_su` / `w_ex_wet` | 0.013363 / 0.010386 | 0.013373 / 0.010391 | ≤ 0.07 % |
| `cp_w_dry` / `cp_w_wet` | 4196.4 / 4195.5 J/kg-K | 4202.8 / 4202.1 J/kg-K | 0.15–0.16 % |
| `M_dot_cd` | 0.002977 kg/s | 0.002982 kg/s | 0.17 % |
| `RH_ex_dry` | 1.3396 | 1.3477 | 0.60 % |

All derived design results (duties, effectivenesses, temperatures,
enthalpies, humidity ratios) agree within 0.07 %. The water specific heats
are 0.15 % high in CoolSolve (CoolProp vs EES water formulation,
propagating to `C_dot_w` and `omega`); `RH_ex_dry` is 0.6 % high — a ratio
evaluated above saturation, carrying the same humid-air formulation
difference documented for `CSL-0016` (humidity ratios +0.5 %, CoolProp with
enhancement factor vs EES psychrometrics). Both deviations are within the
different-equation-of-state tolerance of CoolSolve `docs/ees_import.md` §11.

## Source and attribution

Original exercise (in French, header `MSTh - SB - R5 - Exercice 1`) solved by
**Stéphane Bertagnolio** (ULiège Thermodynamics Laboratory, `SB` initials —
see `docs/model_workflow.md` §3) — MSTh répétition 5, exercise 1. The model
was rewritten in English as the CoolSolve example
`examples/cooling_coil.eescode` by S. Quoilin; this library model follows the
EES original (faithful import), which remains the reference; the example
stays in the CoolSolve repository as a test case (see *Conversion log* for
the differences).

Sources (not copied into the library):

- original EES file with its stored solution:
  `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 05/MSTh-SB-R5-Ex1.EES`
  (inventory candidate `TM-0077`);
- CoolSolve example: `~/git/CoolSolve/examples/cooling_coil.eescode`
  (inventory candidate `CSX-010`).

Exercise variants of the same R5-Ex1 coil in the `thermo_models` inventory
are recorded as duplicates of this model: `TM-0075`/`TM-0076` (question
files, duplicate group DG-0017) and `TM-0080` (exercise file with only the
dry regime solved, wet regime commented out). `TM-0082` (alternative SB
solution with renamed variables, `R5 - SB - Ex 1.EES`) is recorded as
merged: its dry regime is identical, but its wet regime closes the contact
factor differently (`NTU_c = 1/(R_a_f*C_dot_a_f)` and the wet-regime air
specific heat `c_a_wet` taken at the mean wet-regime temperature, instead of
`NTU_c = 1/(R_a*C_dot_a_dry)` and `cp_a_dry` here); its stored results differ
slightly (`Q_dot_wet` 21 635 W, `T_a_ex_wet` 16.01 °C, `M_dot_cd` 2.93 g/s,
`epsilon_c` 0.8585, against 21 639 W, 16.12 °C, 2.98 g/s and 0.8588 for
`MSTh-SB-R5-Ex1.EES`). It is not shipped as a variant file. The R5-Ex2 refrigerant coils
(`TM-0074`, `TM-0078`, `TM-0081`, `TM-0083`, `TM-0084`), the R5-Ex3 air-flow
exercise (`TM-0079`) and the evaporative condensers (`TM-0085`, `TM-0086`)
are different systems and stay `todo` for their own cards.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on `MSTh-SB-R5-Ex1.EES`):
  unit system already SI-°C-Pa-J (no conversion needed); EES licence tag (the
  lab licence, not the author) removed; no tables, no external functions
  (only `cp`, `enthalpy`, `humrat`, `relhum`, `temperature`, `wetbulb`, all
  CoolSolve built-ins — `epsilon_c` in the tool report is a variable, not a
  missing function); full stored solution available (60/60 variables).
  Faithful run of the raw extraction with the stored values as guesses:
  success in 13 iterations; 50/60 variables within 0.1 % of EES, 10 within
  0.6 % (see *Verification*).
- **2026-10-05 — curation**: standard header added, French comments
  translated to English (paraphrasing the original), SI units added to every
  comment (`[W]`, `[W/K]`, `[J/kg-K]`, `[C]`, `[Pa]`, `[kg/s]`,
  `[kg/kg dry air]`, `[-]`); the `$UnitSystem` line deleted per the library
  convention; the wet-regime section title corrected (the original repeats
  the dry-regime title — equations unchanged). No change to any equation or
  value (re-verified: results identical to the faithful run).
- **2026-10-05 — differences with the CoolSolve example** (`CSX-010`): the
  example is a simplified transcription of the same exercise — the property
  calls `cp_a_dry`, `cp_w_dry`, `cp_w_wet` and `RH_ex_wet` are commented out
  with provisional values (1200, 4187, 4187, 0.9), and `cp_a_wet_f = 3000`
  and `epsilon_wet_f = 0.4` are imposed instead of the wet-regime NTU
  relation (which is commented out). With those simplifications the example
  gives `Q_dot_dry = 17.57 kW` and `Q_dot_wet = 21.50 kW` vs 16.49/21.65 kW
  here. Per the card rule the library model follows the EES original; the
  example is kept in CoolSolve unchanged.
- **2026-10-05 — level**: 60 equations (1) + largest block 23 (1) +
  curated `.initials` required (1) = 3 → level 2, as rated on the card.

## Limitations and CoolSolve gaps

- Dry- and wet-regime calculations are juxtaposed (the dry regime is the
  nominal design point, the wet regime the actual operating point); there is
  no regime switch — the condensation check is left to the reader.
- The contact-factor outlet state reuses the dry air-side capacity rate in
  `NTU_c`; the bypass-flow formulation (`epsilon_c_bis`) reproduces the same
  duty and condensate flow, as in the original.
- No CoolSolve gaps encountered during the import. One benign solver
  warning: `HUMRAT(): t=30 looks like Fahrenheit` is a false positive
  (30 °C is the legitimate supply temperature; same warning as `CSL-0016`).

## Related models

- `CSL-0016` (Moist-air cooling coil with contact factor): the contact-factor
  (bypass) outlet method used here, as a standalone level-1 model on imposed
  outlet temperature.
- `CSL-0062` *cooling_coil_condensate_ratio*: exam revision exercise on a
  cooling coil treated with global first-law balances (two methods, with and
  without the condensate term) instead of the coil-resistance detail.
- `CSL-0073` *cooling_coil_with_control_simplified*: the same cooling coil of
  the ULiège model bank at the simplified level of detail (contact
  temperature driven by a control law on the exhaust air temperature, no
  refrigerant side).
- `CSL-0074` *cooling_coil_refsim*: the same cooling coil of the ULiège model
  bank at the reference-simulation level of detail (one zone, dry and wet
  regimes described simultaneously, secondary refrigerant side with the
  BrineProp correlations).
- `CSL-0163` *cooling_coil_paramid*: parameter identification of a wet cooling
  coil of the same ULiège model bank (one-zone wet model, resistances
  identified from one measured point, card C-155).
