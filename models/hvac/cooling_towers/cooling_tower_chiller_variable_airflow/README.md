# Cooling tower of a chiller plant with variable air flow

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0287`

Revision exercise of the ULiège MSTh course (session of 2005-12-23, file 05
of a series of 3): a direct-contact cooling tower rejects the condenser heat
of a water chiller while the air flow is varied. The air side, the fan and
the chiller are coupled: the fan laws scale the pressure rise and the dry-side
UA with the air mass flow, and the chiller COP follows the condenser water
temperature, so the plant `COP_global` results at each air flow.

| | |
|---|---|
| **Category** | HVAC and psychrometrics › Cooling towers and evaporative equipment |
| **Fluids** | Moist air (`AirH2O`); water with constant c = 4187 J/(kg·K) |
| **Size** | 42 equations (largest block: 16) |
| **Source** | `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 10/Revision JL051223-05.EES` (candidate TM-0162, EES X7.458) |
| **Authors** | Jean Lebrun (file header date 2005-12-23; EES licence stamp *J. Lebrun, Laboratoire de Thermodynamique, Univ. Liège*) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Paraphrase of the original comments (French): "Révision JL051223-05 — let's
vary the air flow" (`M_dot_a = 10.51` commented out). Data as written:
nominal air flow 10.51 kg/s, nominal fan pressure rise 281.2 Pa, nominal
dry-side UA 7453 W/K; chiller evaporator duty 230 kW, nominal COP 4 with a
-0.025 K⁻¹ correction on the condenser water exit temperature (nominal
35 °C); condenser (tower) water flow 13 kg/s; atmosphere 101325 Pa, inlet air
20 °C at 80 % relative humidity; fan efficiency 0.5. The tower outlet air is
assumed saturated. Default data of a centrifugal-fan tower
(`M_dot_a = a·Q_dot_ct + b`, `AU_dry_ct = c·Q_dot_ct + d`) and the constant
fan power `W_dot_fan = 5 kW` of exercise 04 are present only as comments, as
in the original.

## Model

Steady-state algebraic model, equations as in the original:

- **Fan and air flow**: fan laws `DELTAp = DELTAp_n·(M_dot_a/M_dot_a_n)²`,
  `AU_dry = AU_dry_n·M_dot_a/M_dot_a_n`, fan power
  \(\dot W_{fan} = \dot V_a \Delta p / \eta\), air volume flow from the
  `AirH2O` specific volume at the inlet state.
- **Chiller**: `W_dot_chiller = Q_dot_ev/COP_chiller`,
  `COP_chiller = COP_chiller_n·(1 − 0.025·(t_w_ex_cd − t_w_ex_cd_n))`, tower
  duty `Q_dot_ct = Q_dot_ev + W_dot_chiller` (approximate balance, as in the
  original), `COP_global = Q_dot_ev/(W_dot_chiller + W_dot_fan)`.
- **Tower**: counter-flow effectiveness–NTU with
  \(\varepsilon = \frac{1-e^{-NTU(1-\omega)}}{1-\omega e^{-NTU(1-\omega)}}\),
  `NTU = AU_f/C_dot_f`, wet-side UA `AU_f = AU_dry·c_p_f/c_p`, fictitious
  air-side specific heat `c_p_f = (h_a_ex − h_a_su)/(t_wb_ex − t_wb_su)`,
  capacity rates `C_dot_f = M_dot_a·c_p_f` and `C_dot_w_ct` with
  `min`/`max`, heat rate from water side, air enthalpy rise and
  effectiveness; `t_wb_ex = t_a_ex` (saturated outlet air).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `M_dot_a` | 30 kg/s (stored EES operating point) | `t_w_ex_ct` | 24.039 °C |
| `Q_dot_ev`, `M_dot_w_cd`, `p` | 230 kW, 13 kg/s, 101325 Pa | `t_w_ex_cd` | 29.187 °C |
| `t_a_su`, `RH_su` | 20 °C, 0.80 | `W_dot_fan` | 116.27 kW |
| `eta_fan`, nominal data | 0.5, see above | `W_dot_chiller` | 50.204 kW |
| | | `COP_chiller` / `COP_global` | 4.581 / 1.382 |
| | | `Q_dot_ct` | 280.20 kW |

## How to run

```
coolsolve ./cooling_tower_chiller_variable_airflow.eescode
```

`.initials` carries the EES stored-solution guesses; without them the
16-variable block fails with `SingularJacobian`. To study another air flow,
change the single input equation `M_dot_a = 30` (the original comment marks
the nominal 10.51 kg/s; that point needs the comment-block guesses, see
*Verification*).

## Results

At the stored operating point (`M_dot_a` = 30 kg/s, i.e. `W_dot_fan`
116.31 kW from the last run of the EES parametric table): tower outlet water
24.04 °C, air outlet wet-bulb/dry-bulb 20.50 °C, effectiveness 0.447, NTU
0.690, tower duty 280.20 kW, chiller COP 4.581 (cooler condenser water than
nominal, 29.19 vs 35 °C, raises the COP above 4), global COP 1.382 (at this
high air flow the fan draws 2.3× the compressor power, 116.3 vs 50.2 kW).

*(figure placeholder — the maintainer adds a parametric plot of
`COP_global` vs `M_dot_a` in `figures/`, docs/model_workflow.md §7)*

## Verification

Reference: the solution stored in the source EES file (42 of 47 stored
variables carry values; `a`, `b`, `c`, `d`, `AU_dry_ct` belong to commented
equations and have none), decoded with `tools/ees_extract.py` to
`reference/ees_variables.csv`. The stored state is the last run of the
parametric table (sweep of `W_dot_fan`, 120 rows), which corresponds to
`M_dot_a` = 30 kg/s through the fan law — that value is the model's input
equation.

```
python3 tools/compare_solution.py cooling_tower_chiller_variable_airflow.sol reference/ees_variables.csv
→ 42 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0
```

Largest relative difference over the 42 common variables: **3.84e-04**
(`v_a`, `W_dot_fan`, `V_dot_a` — the humid-air specific-volume backend,
EES 0.846115 vs CoolSolve 0.84579 m³/kg); everything else is below that.

Secondary check: with `M_dot_a = 10.51` (nominal, the commented original
input) and the guesses of the solution comment block stored in the equation
window, CoolSolve reproduces that stored point: `W_dot_fan` 4999.3 vs 5000 W
(1.4e-04), `t_w_ex_ct` 29.716 vs 29.72 °C, `Q_dot_ct` 287496 vs 287500 W,
`COP_global` 3.680 vs 3.68, `t_a_ex` 25.185 vs 25.19 °C — the comment block
stores 4 significant digits.

The lookup table `Lookup 1` (3×3) stored in the EES file (columns
`M_r_cp, r_p, epsilon_s_cp` — compressor data left over from an earlier
exercise) is not referenced by any equation; it is shipped unchanged as
`cooling_tower_chiller_variable_airflow-lookup_1.csv`. The parametric table
`Table 1` (120×2: `W_dot_fan` input, `N_rN` a leftover column with no
equation) is kept only as extraction reference; it is not needed to run.

## Niche

Nearest models: `CSL-0215` (MSTh tower at nominal and half fan speed) and `CSL-0030` (two-speed tower): they solve the tower alone. This model couples
the tower to the **condenser of a water chiller** (COP as a function of the condenser water exit temperature) and to the fan laws, so the *plant*
`COP_global` is a function of the air flow, i.e. the optimum air flow of a chiller plant.

## Source and attribution

- Author: Jean Lebrun (ULiège, Laboratoire de Thermodynamique), file dated
  2005-12-23, French comments.
- Source: `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh -
  Repetitions/TP 10/Revision JL051223-05.EES` (candidate TM-0162, duplicate
  group DG-0034, 6 files: series 04–06 in TP 10 and copies in *TP 13
  Révisions*; TM-0163/0179/0180 have identical equations, TM-0161/0178 the
  fan-curve variant of exercise 04). Exams/exercises are published as
  examples under the library licence (MIT).

## Conversion log

- **2026-10-23 — import**: extracted with `tools/ees_extract.py` (EES
  X7.458, unit system already `SI MASS DEG PA C J` — no unit conversion);
  `$UnitSystem` directive removed; standard header added; French comments
  translated (meaning preserved: "bilan approximatif", "air saturé en sortie
  de tour", "donnée à vérifier"); EES's auto-appended *Solution* comment
  block removed from the equation window (its values are quoted in
  *Verification*); dead commented equations kept as comments as in the
  original.
- **2026-10-23 — under-determined completion**: solved unmodified first:
  `coolsolve -d` reports *There are 41 equations and 42 unknowns. The system
  is not square* — EES supplied the missing equation from the parametric
  table (`W_dot_fan` of each row). The input equation
  `M_dot_a = 30 [kg/s]` (the air flow of the stored solution) is therefore
  added as the model's operating point; no original equation was changed.
- **2026-10-23 — lookup table**: `Lookup 1` renamed `lookup_1` by the
  extractor (file-name safety); no equation references it.
- **Level**: score of taxonomy.md §3: equations 42 → 0; largest block 16 →
  1; no functions/arrays → 0; 3 coupled components (chiller, tower, fan) →
  1; off-design physics (fan laws, COP vs water temperature) → 1; needs the
  stored guesses (fails `SingularJacobian` without `.initials`) → 1;
  total 4 → **level 3**.

## Limitations and CoolSolve gaps

No CoolSolve gap blocks the file (`missing_features` empty). Physical
limitations as in the original: approximate condenser/tower heat balance
(evaporation not subtracted), constant water specific heat, saturated tower
outlet, fan efficiency constant, chiller COP linear in the condenser water
temperature. Cosmetic: the `.sol` labels `v_a` as `kg/m^3`
(`CS-BUG-UNIT-VOLUME`, registered; values are unaffected).

## Related models

- `CSL-0232` *cooling_tower_water_air_sides*: the same counter-flow ε-NTU
  tower core on wet-bulb/fictitious-fluid terms at fixed air flow; here it is
  coupled to the chiller and to a variable-flow fan.
- `CSL-0215` *cooling_tower_half_speed*: fan laws for two discrete regimes
  (nominal/half speed) mixed at the outlet; here a continuous air-flow
  variation with plant `COP_global` as the objective.
- `CSL-0065` *cooling_tower_condenser_water*: tower balancing of a steam
  plant condenser (mass/energy balance exercise); here a chiller plant with
  effectiveness–NTU rating and off-design air flow.
