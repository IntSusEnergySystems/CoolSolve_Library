# Classical fuel-oil boiler: parameter identification from the nominal point

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0265`

Steady-state parameter-identification (ParamID) companion of the classical
ON/OFF fuel-oil heating-boiler reference model of the 2008 ULiège model bank.
The three boiler parameters — gas-to-water conductance `AU_gw`, envelope
conductance `AU_wenv` and fuel mass flow `M_dot_f` — are the unknowns of a
square system closed by the nominal-point data (efficiency, useful power,
water volume flow, water supply temperature) and one stand-by measurement
(heat loss to the environment in the OFF regime). The boiler itself is the
same building block as in the simulation reference: adiabatic combustion of a
fuel oil with excess air (mean specific heat of the products from the `cpbar`
procedure), a gas-water and a water-environment epsilon-NTU exchanger.

| | |
|---|---|
| **Category** | Components › Boilers and burners |
| **Fluids** | combustion products of a fuel oil C₁₂.₈H₂₃.₃ (y_C = 86.9 %, y_H = 13.1 %) via the ideal-gas substances CO2, H2O, N2, O2 (mean specific heat from `cpbar`) |
| **Size** | 68 equations (largest block: 7) |
| **Source** | ULiège model bank 2008-02-12 — `CLASSICALBOILER_PARAM_IDENTIFICATION_MODEL_SBJL080212.zip` |
| **Authors** | Stéphane Bertagnolio, Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT (lab disclaimer of the original: freely distributed, may not be sold, cite origin) |
| **CoolSolve** | 0.4.0@9768373 — verified (see *Verification*) |

## Problem statement

Identify the three parameters of the classical ON/OFF boiler model from
measurements taken at one nominal point and one stand-by point, instead of
imposing them: given the nominal efficiency `eta_N`, the nominal useful power
`Q_dot_u_n_ON`, the water volume flow `V_dot_w_l\h_n`, the water supply
temperature `t_w_su_N`, the duty fraction `theta_N = 1` and the stand-by heat
loss `Q_dot_wenv_n_OFF`, compute `AU_gw`, `AU_wenv` and `M_dot_f` together
with the full internal state of the boiler (flame temperature, flue-gas
exit temperature, water temperatures, efficiencies).

## Model

- **Combustion reference model** (as in the original): fuel CₙHₘ with m = 1
  and n = 12(1−y_C)/y_C from the carbon mass fraction; stoichiometric
  fuel-air ratio `f_st` from the molar mass of air; excess air `e` from
  `f = 0.06`; adiabatic energy balance Q̇₁+Q̇₂+Q̇₃+Q̇₄+Q̇₅ = 0 with the mean
  specific heat of the products from `cpbar` (library model `CSL-0005`),
  giving the adiabatic flame temperature t_adiab ≈ 1929 °C.
- **Gas-water exchanger**: epsilon-NTU (cross-flow form of the original),
  duty fixed usefully as Q̇_u,ON + Q̇_wenv; the identification of `AU_gw`
  follows from the required number of transfer units.
- **Water-environment exchanger** (envelope losses): single-stream
  epsilon-NTU with constant `AU_wenv`; identified from the stand-by point
  Q̇_wenv,OFF = ε Ċ_w (t_w,su − t_env), ε = 1 − exp(−AU_wenv/Ċ_w).
- **Fuel flow**: `M_dot_f` = Q̇_u,n,ON/(η_N·LHV) from the efficiency definition.
- **ON/OFF control**: duty fraction θ = θ_N = 1 (boiler ON at the stored
  point); water exhaust temperature blended between the ON and OFF states.

| Inputs (operating point of the stored run) | Value | Identified parameters | Value (CoolSolve / EES) |
|---|---|---|---|
| `eta_N` nominal efficiency | 0.91 | `M_dot_f` fuel flow | 1.29200e-3 / 1.29200e-3 kg/s |
| `Q_dot_u_n_ON` nominal useful power | 50 556 W | `AU_wenv` envelope conductance | 18.324 / 18.324 W/K |
| `V_dot_w_l\h_n` water volume flow | 2150 l/h | `AU_gw` gas-water conductance | 80.186 / 80.078 W/K |
| `t_w_su_N` water supply temp. | 60 °C | `t_adiab` flame temperature | 1929.06 / 1930.49 °C |
| `Q_dot_wenv_n_OFF` stand-by losses | 639 W | `t_g_ex` flue-gas exit temp. | 187.21 / 187.555 °C |
| `f`, `y_C`, `y_H`, `theta_N` | 0.06, 0.869, 0.131, 1 | `eta_ON` | 0.91 / 0.91 |

The constants (`t_a` = `t_f` = `t_env` = 25 °C, `c_w` = 4187 J/kg-K,
`rho_w` = 1000 kg/m³, `c_f` = 1800 J/kg-K, `LHV` = 43 MJ/kg, `c_p_a` =
1005 J/kg-K) and the five operating-point inputs above were supplied by the
EES diagram window of the original file (not extracted) and are restored as
equations with the values of the stored run; the quoted comments of the
original show an unused 1.15 MW nominal brochure point that the author had
replaced before the last calculation (see *Conversion log*).

## How to run

```
coolsolve ./boiler_param_identification.eescode
```

Solve with the shipped `.initials` (values of the stored EES run): the flame
temperature sits inside the two `cpbar` CALLs, as in `CSL-0006`. No
`coolsolve.conf` is needed; the model converges in 33 iterations.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `AU_gw` gas-water conductance | 80.186 W/K | 80.0777 W/K |
| `AU_wenv` envelope conductance | 18.3241 W/K | 18.3241 W/K |
| `M_dot_f` fuel mass flow | 1.29200e-3 kg/s | 1.29200e-3 kg/s |
| `t_adiab` adiabatic flame temperature | 1929.06 °C | 1930.49 °C |
| `c_p_p` mean c_p 25 °C → flame | 1278.30 J/kg-K | 1277.34 J/kg-K |
| `c_p_g` mean c_p over the gas exchanger | 1297.13 J/kg-K | 1296.31 J/kg-K |
| `t_g_ex` flue-gas exit temperature | 187.21 °C | 187.555 °C |
| `t_w_ex_1` water temp. after the gas exchanger | 80.6239 °C | 80.6239 °C |
| `t_w_ex_ON` water exhaust temp. (ON) | 80.2178 °C | 80.2178 °C |
| `t_w_ex_OFF` water exhaust temp. (OFF) | 59.7445 °C | 59.7445 °C |
| `Q_dot_gw` gas-water duty | 51 571.5 W | 51 571.5 W |
| `Q_dot_wenv` envelope loss (ON) | 1015.53 W | 1015.53 W |
| `eta_ON` / `epsilon_gw` | 0.91 / 0.93194 | 0.91 / 0.93181 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric plot, e.g. identified AU_gw vs nominal efficiency eta_N -->

## Verification

Reference: the **EES stored solution** of
`BOILER_PARAM_IDENTIFICATION_EES_MODEL_SBJL080212.EES` (EES X7.888, 66
numeric values). With the shipped `.initials`:

```
66 common variables, 2 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 2
| AU_gw  | 80.0777 | 80.1864 | 1.36e-03 | **DIFF** |
| t_g_ex | 187.555 | 187.21  | 1.84e-03 | **DIFF** |
```

i.e. **max relative difference 1.84e-3** (`t_g_ex`); at `rtol=1e-2` all 66
variables agree. The two deviations trace to the property backend of the
`cpbar` mean specific heat (ideal-gas enthalpies of CO2/H2O/N2/CO): 0.075 %
on `c_p_p` and 0.06 % on `c_p_g` between EES 7.888 and CoolProp, amplified
by the gas-side temperature approach into `t_g_ex` and the identified
`AU_gw`. The two CoolSolve-only names are `V_dot_w_l\h` and
`V_dot_w_l\h_n` (subscript notation of the original; these two names are
absent from the extracted EES variable records — `M_dot_w` = 0.59722 kg/s
confirms V̇ = 2150 l/h). All 68 equations are satisfied (max |residual|
7.6e-10). The identification chain was recomputed by hand:
`M_dot_f` = 50556/(0.91·43e6) = 1.29200e-3 kg/s and
`AU_wenv` = −Ċ_w·ln(1 − 639/(Ċ_w·35)) = 18.324 W/K, both equal to the
stored EES values.

## Source and attribution

Original EES model: ULiège Thermodynamics Laboratory model bank, 2008-02-12
(`Model data bank/Heat_and_Cool_Production_Systems/Heat_Production_by_
Combustion/CLASSICALBOILER_PARAM_IDENTIFICATION_MODEL_SBJL080212.zip`,
file `BOILER_PARAM_IDENTIFICATION_EES_MODEL_SBJL080212.EES`, EES X7.888,
unit system SI MASS DEG PA C J). Authors: S. Bertagnolio, J. Lebrun (from
the file name tag SBJL080212 and the inventory `authors` column). The
original carries the lab disclaimer "freely distributed, may not be sold,
cite origin"; the model is published under the library license (MIT) with
this citation. The zip also ships the `CombCmHn_SI_PNG2003_V2` user library
(`cpbar`, TM-0253 / `CSL-0005`, P. Ngendakumana 2003).

## Conversion log

- **2026-10-22 — import**: extracted with `ees_extract.py` (EES X7.888;
  unit system already `SI MASS DEG PA C J`, no unit conversion needed);
  `$UnitSystem` directive removed; `cpbar` copied from `CSL-0006`/`CSL-0005`
  and called with `CALL` as in the original (`CSL-0005`); comments translated
  to English with SI units; variable names kept, including the subscript
  notation `V_dot_w_l\h` of the original.
- **2026-10-22 — diagram-window inputs restored**: the original fixed 13
  values through its EES diagram window (constants `t_a`, `t_f`, `t_env`,
  `c_w`, `rho_w`, `c_f`, `LHV`, `c_p_a` and the operating point
  `t_w_su_N`, `eta_N`, `Q_dot_u_n_ON`, `V_dot_w_l\h_n`,
  `Q_dot_wenv_n_OFF`); they are restored as equations with the values of
  the stored run (60 °C, 0.91, 50 556 W, 2150 l/h, 639 W). The quoted
  comments of the original (70 °C, 0.892, 1.15 MW, 1800 l/h, 320 W) document
  an earlier nominal brochure point and are kept as comments; the regression
  case follows the stored solution, per the import workflow.
- **Level**: taxonomy §3 score: equations 68 → 1; largest block 7 → 1;
  copied `cpbar` procedure only, no own procedures/arrays → 0; no multi-zone
  discretisation → 0; parameter identification (semi-empirical calibration)
  → 1; no curated guesses beyond the stored-value initials → 0; total 3 →
  level 2.

## Limitations and CoolSolve gaps

No CoolSolve gap blocks this model (`missing_features` is empty). Physical
limitations of the original, kept as-is: complete combustion only (Q̇₄ = 0),
constant mean water properties, constant `AU` values (no part-load law, in
contrast with the modulating-burner reference `CSL-0166`), and a single
nominal + stand-by identification (no regression over many measured points).

## Related models

- `CSL-0005` (`cpbar_combustion_products`): the mean-specific-heat procedure
  copied into this model.
- `CSL-0006` (`boiler_mean_specific_heat`): forward simulation model of the
  same boiler building block (TM-0492, the ON/OFF simulation companion of
  this file, was merged there); same combustion + two-exchanger structure,
  but the parameters are inputs there and outputs here.
- `CSL-0166` (`boiler_modulating_burner_refsim`): same authors and date
  (SBJL080212 model bank), same fuel and `cpbar` combustion block, but a
  modulating-burner reference simulation (native file blocked).
- `CSL-0263` (`fuel_oil_boiler_onoff_setpoint`): MSTh teaching exercise of
  the same boiler family, closed by a flue-gas enthalpy balance instead of
  the nominal-point identification.
