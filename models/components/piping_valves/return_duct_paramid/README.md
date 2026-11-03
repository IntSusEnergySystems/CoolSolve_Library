# Return duct reference model for parameter identification

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0311`

Reference return-duct model built of three connected components — continuous
pressure drop of a tight adiabatic duct (Colebrook), duct leakage with
infiltration/exfiltration of ambient air (water and energy balances), heat gain
along a tight duct (epsilon-NTU with wall and insulation resistances) — plus the
normalized study outputs `DELTAp\DELTAp_duct_n`, `epsilon\epsilon_M_duct_n`,
`epsilon\epsilon_t_duct_n` and `M\M_ex_duct_n`. It is the model that generated
the parametric study from which the curve-fit coefficients of the simplified
duct model `CSL-0170` (e.g. `DELTAp ~ M^1.89`) were fitted; the fits are quoted
as comments and not used.

| | |
|---|---|
| **Category** | Components › Valves, nozzles and piping |
| **Fluids** | AirH2O (humid air) |
| **Size** | 114 equations (largest block: 16) |
| **Source** | `~/Nextcloud/thermo_models/Model data bank/Distribution_Systems/Ducts/Return_Duct_Simplified_ParamID_Model_JL080317.zip!/Return_Duct_ParamID_EES_Model_JL080317.EES` (EES 7.888) |
| **Authors** | Jean Lebrun (ULiège Thermodynamics Laboratory), 2008-03-17 |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified (see the `verification` field) |

## Problem statement

Purpose and context: the "reference" (detailed) duct model of the ULiège model
bank, used to run the parametric study (sweep of the exit mass flow rate around
its nominal value `M_dot_ex_duct_n` = 1 kg/s) whose results were fitted by the
power laws of the simplified model. The stored solution is the nominal run:
supply air 20 °C, humidity ratio 0.01, 1 bar; ambient air 10 °C, humidity ratio
0.005, 1 bar; the return duct leaks, so ambient air infiltrates
(`M_dot_leakage_duct` = −0.191 kg/s for 1 kg/s leaving at the duct exit) and the
air cools towards the ambient temperature.

## Model

The top-level `Simplified model` block computes, from the outlet state, the
normalized ratios of the study; the `Reference model` block connects three
components (variable names carry the component suffix `_01`, `_02`, `_03`):

1. **01 — continuous pressure drop** of a tight, adiabatic duct: Colebrook's
   implicit friction factor, `DELTAp = lambda*(L/D)*C^2/2`, humid-air viscosity
   and specific volume at the supply state.
2. **02 — duct leakage**: the leakage flow driven by the mean duct pressure
   minus the ambient pressure through a `zeta = xi/Re^n` law on a leakage area
   `A_leakage\L_duct*L_duct`; negative leakage means infiltration of ambient
   air (the EES 5-argument `IF` functions split infiltration/exfiltration).
   Water and energy balances give the outlet humidity ratio and temperature.
3. **03 — heat gain** along a tight duct: epsilon-NTU between the air and the
   ambient, `AU` from the inner convection, insulation layer and outer
   convection resistances (here with no insulation, `e_insulation_duct_03 = 0`).

Inputs (default operating point): `M_dot_ex_duct` = 1 kg/s, `p_su_duct` = 1 bar,
`t_su_duct` = 20 °C, `W_su_duct` = 0.01, `p_env_duct` = 1 bar, `t_env_duct` =
10 °C, `W_env_duct` = 0.005; parameters `L_duct` = 50 m, `A_duct` = 0.1 m²,
`D_hydr_duct` = 0.25 m, `epsilon_duct` = 0.005, `A_leakage\L_duct` = 1.5E-4 m,
`D_hydr_leakage_duct` = 1E-4 m, `xi_leakage_duct` = 10, `n_leakage_duct` = 0.5,
`Perimeter_in_duct` = 0.5 m, `e_insulation_duct` = 0, `k_insulation_duct` =
0.04 W/(m·K); constants `h_in_duct_03` = 25 W/(m²·K), `h_out_duct_03` =
10 W/(m²·K) (as in the original equations).

## How to run

```bash
coolsolve ./return_duct_paramid.eescode
```

The `.initials` file holds the stored EES solution (including the seven
backslash-named ratios); with it the solve takes 23 iterations. Without it the
leakage branch of `abs()` and the `IF` functions may converge to the other root
(positive leakage), as on the sibling model `CSL-0170`. No `coolsolve.conf`, no
variant.

## Results

| Quantity | EES (stored) | CoolSolve |
|---|---:|---:|
| `DELTAp_duct` [Pa] | 234.227 | 233.897 |
| `M_dot_leakage_duct` [kg/s] | −0.190818 | −0.191069 |
| `t_ex_duct` [°C] | 16.8082 | 16.8056 |
| `W_ex_duct` [–] | 0.00904591 | 0.00904465 |
| `epsilon_t_duct` [–] | 0.319183 | 0.319440 |
| `epsilon_M_duct` [–] | 0.190818 | 0.191069 |
| `Q_dot_duct_03` [W] | −1328.25 | −1327.79 |
| `DELTAp\DELTAp_duct_n` [–] | 1.000115 | 0.998706 |

Pressure falls along the duct, ambient air infiltrates and the air leaves cooler
and drier than it enters, close to the ambient state — as in the original.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![DELTAp vs M_dot_ex_duct](figures/return_duct_paramid_dp.png)  + one-line caption -->

## Verification

Against the stored solution of `Return_Duct_ParamID_EES_Model_JL080317.EES`
(`tools/compare_solution.py`, work folder `reference_full.csv`): **114 common
variables, 19 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0.
Maximum relative difference 7.29e-03 on `Re_leakage_duct_02`**.

The seven variables whose names contain a backslash are missing from the
`ees_extract.py` CSV (its variable-name pattern does not allow `\`, same as on
`CSL-0170`); their records were decoded by hand from the binary and added to the
comparison (values `1.0`, `1.0001147476969143`, `1.000096548577734`,
`0.9999461091809451`, `1.000096548577734`, `0.00015`, `0.00015`; the record of
`epsilon\epsilon_t_duct_n` carries format byte 1 instead of 3 — extra evidence
for `CS-BUG-EXTRACT-FMT-BYTE`).

All 19 differences above rtol=1e-3 trace to one root cause: the **humid-air
viscosity** of EES 7.888 differs from CoolProp's by 0.60 %
(`mu_duct_01`: 1.822904306e-05 vs 1.81199e-05 Pa·s); the specific volume differs
by 3.75e-04. Through `Re → zeta → C_leakage → M_dot_leakage` this gives the
0.13–0.73 % on the leakage/Reynolds group and 0.14 % on `DELTAp_duct`; the
thermal results (`t_ex_duct` 1.5e-04, `W_ex_duct` 1.4e-04, enthalpies, `Q_dot`
5e-04 relative) agree far inside the property tolerance. Derived results are
within the "different property backend" tolerance of `ees_import.md` §11.

## Source and attribution

- Source: `~/Nextcloud/thermo_models/Model data bank/Distribution_Systems/Ducts/Return_Duct_Simplified_ParamID_Model_JL080317.zip!/Return_Duct_ParamID_EES_Model_JL080317.EES`
  (the zip also contains a Windows executable pack of the same model).
- Author: Jean Lebrun (JL080317), ULiège Thermodynamics Laboratory; EES licence
  tag `{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege}`.
- IEA Annex 43 / subtask context per the inventory notes of the sibling file
  (TM-0483).
- Published in the library under the MIT license (laboratory collection).

## Conversion log

- **2026-10-22 — import**: `tools/ees_extract.py` (EES 7.888, unit system
  `SI MASS DEG PA C J` — no unit conversion needed); licence tag removed;
  comments kept (English in the original, minor clarifications marked "as in the
  original"). 96 equations, 107 variable records decoded.
- **2026-10-22 — Diagram-window inputs restored as equations** (as on
  `CSL-0170`): 18 values that the original set in the Diagram window and that
  the extraction leaves undefined were added as a `Default operating point`
  block, using the values of the stored run: `M_dot_ex_duct` = 1, `p_su_duct` =
  1E5, `t_su_duct` = 20, `W_su_duct` = 0.01, `p_env_duct` = 1E5, `t_env_duct` =
  10, `W_env_duct` = 0.005, and the parameters `L_duct` = 50, `A_duct` = 0.1,
  `D_hydr_duct` = 0.25, `epsilon_duct` = 0.005, `A_leakage\L_duct` = 1.5E-4,
  `D_hydr_leakage_duct` = 1E-4, `xi_leakage_duct` = 10, `n_leakage_duct` = 0.5,
  `Perimeter_in_duct` = 0.5, `e_insulation_duct` = 0, `k_insulation_duct` =
  0.04. Three of them differ from the values in the original's comment defaults,
  which document an earlier run: `L_duct` 50 m instead of 10 m,
  `A_leakage\L_duct` 1.5E-4 m instead of 2E-4 m (stored `A_leakage_duct_02` =
  0.0075 m² for `L_duct_02` = 50 m), `e_insulation_duct` 0 instead of 0.025 m
  (the stored `AU_duct_03` = 178.571 W/K proves `e = 0`). The commented defaults
  are kept in the file, as in the original. No equation of the original was
  changed; the system becomes square (114 equations, 114 unknowns).
- **2026-10-22 — backslash names**: the seven variable names containing `\`
  (`M\M_ex_duct_n`, `DELTAp\DELTAp_duct_n`, `epsilon\epsilon_M_duct_n`,
  `epsilon\epsilon_t_duct_n`, `epsilon\epsilon_w_duct_n`, `A_leakage\L_duct`,
  `A_leakage\L_duct_02`) are kept; CoolSolve accepts a `\` between two parts of
  a name. `ees_extract.py` omits their records (name-pattern limitation; register
  row `CS-BUG-EXTRACT-NAME-CHARS`), they were decoded by hand (README
  Verification).
- **2026-10-22 — unit annotation correction**: the original comment writes
  `A_duct_01=0.1 [m]`; it is a section, annotated `[m2]` in the restored block.
- **Level**: equations 114 → 1; largest block 16 → 1; functions/arrays none → 0;
  multi-component (3 coupled components) → 1; physics: semi-empirical leakage
  law, parameter-identification context → 1; numerics: no curated guesses needed
  (stored `.initials`) → 0. Score 4 → level 3; moved down to 2: a short,
  well-conditioned component model close to textbook material, in line with the
  `level_guess` of the inventory and the level 1 of `CSL-0170`.

## Limitations and CoolSolve gaps

- Physical: heat-transfer coefficients `h_in_duct_03`, `h_out_duct_03` are fixed
  values in the original ("might be calculated as function of air speed");
  condensation inside the duct is excluded (the humidity effectiveness of the
  simplified model equals the mass effectiveness only in that case, as the
  original comment says).
- No CoolSolve gap blocks the model (the 5-argument `IF` of the leakage split is
  supported, `CS-GAP-IF5` closed). Tool limitation: `CS-BUG-EXTRACT-NAME-CHARS`
  (seven stored records not exported by `ees_extract.py`; hand-decoded here, not
  blocking CoolSolve itself).

## Related models

- `CSL-0170` (*return_duct_simplified*): the simplified curve-fit model whose
  coefficients were fitted on the parametric study generated by this reference
  model; its normalized ratios carry the same names with the `\n` suffix.
