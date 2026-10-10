# Condensing boiler reference model (RefSim)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0080`

Reference simulation model of a **condensing boiler** of the ULiège model bank
(Laborelec toolkit lineage). The boiler is described as an assembly of a supposed
to be adiabatic combustion chamber and three heat exchangers (dry gas-water,
wet gas-water — a cooling coil where the fumes condense — and a
water-environment exchanger standing for the heat losses). The combustion is
represented by five fictitious processes and the mean specific heat of the
combustion products comes from the `cpbar` function of the bank. The file is
shipped as valid EES and is **blocked**; a runnable `_coolsolve` variant is
shipped and verified against the solution stored by EES (see *Verification*).

| | |
|---|---|
| **Category** | Components › Boilers and burners |
| **Fluids** | Water (real), AirH2O (moist air), Air, N2, O2, CO2, H2O, CH4, C2H6, C3H8, C4H10 (ideal gases, formation enthalpy included), Methane (real) |
| **Size** | 258 equations, largest block 52 (native file and variant; the native file stops at its first `C4H10` call) |
| **Source** | ULiège model bank (Laborelec toolkit lineage), heat production by combustion, condensing boiler reference simulation model, 9 January 2008 (`CondensingBoiler_RefSim_EES_Model_VLAR080109.EES`, EES 7.888) |
| **Authors** | Vincent Lemort, Andrés Rodríguez (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | native file **blocked** by `CS-GAP-FLUIDS-C8H18`; runnable variant `condensing_boiler_refsim_coolsolve.eescode` verified against the solution stored by EES |

## Problem statement

Purpose and context (reference model, not an exercise). The model answers: for a
gas-fired condensing boiler, what are the useful power, the efficiency on the
higher and the lower heating value, the temperature of the water at the exhaust,
the temperature and humidity of the fumes at the exhaust, and how much water is
condensed in the coil — as functions of the load `x_load`, the water inlet
temperature `T_w_su_boil` and the water flow rate `V_dot_w_boil_ls`? The
original ships a parametric table (see *Results*) that sweeps the load between
0.75 and 1 and the water inlet temperature between 27 and 82 °C.

## Model

**Combustion chamber (section 5).** Adiabatic, described by five fictitious
processes, as in the original's own short description: (i) cooling the inlet air
to the reference temperature `T_ref` = 20 °C (`Q_dot_1`), (ii) the same for the
fuel (`Q_dot_2`, `T_f_su_boil = T_amb`), (iii) the release of the lower heating
value (`Q_dot_3 = −M_dot_f_boil·LHV`), (iv) the energy of the dissociation of
CO2 into CO corresponding to the air excess (zero here, as in the original:
`Q_dot_4 = 0`, the combustion is complete), (v) heating the products to the
adiabatic flame temperature (`Q_dot_5`, closed by the balance
`Q_dot_1+…+Q_dot_5 = 0`). The fuel is a natural gas given by its volumetric
composition (90 % CH4, 2.7…4.6 % C2H6, N2 and CO2), its density is the average
of 0.72 and 0.81 kg/m³, its LHV is an input (44 MJ/kg) and its HHV is computed
from the water formed (`HHV = LHV + q_cond_H2O`). The molar fractions of the
products (`x_CO2_ex`, `x_H2O_ex`, `x_O2_ex`, `x_N2_ex`) and their mass fractions
(`y_*_ex`) follow from the stoichiometry written in the comment of section 5.7.1;
the air excess is `e = 0.01`.

**Mean specific heat.** `c_p_g = cpbar(m, n, f, T_adiab, T_ref)`: the `cpbar`
FUNCTION of the file (same function as the library model `CSL-0005
cpbar_combustion_products`, kept here in the file because the source calls it
directly) returns the mean specific heat of the complete combustion products of a
C_mH_n fuel between two temperatures, from the ideal-gas enthalpies of CO2, H2O,
O2 and N2 and the simplified air 0.79 N2 / 0.21 O2; for `f = 0` it returns the
specific heat of pure air.

**Dry gas-water exchanger (section 6).** Counter-flow, effectiveness-NTU model:
`AU_gw = AU_gw_N·(M_dot_g_boil/M_dot_g_boil_n)^a_gw`, capacity flow rates
`C_dot_g_gw = M_dot_g_boil·c_p_g_gw` and `C_dot_w_gw = M_dot_w_boil·c_w_gw`
(4186 J/kg·K), `NTU_gw = AU_gw/C_dot_min_gw` and the counter-flow effectiveness.
The three forms of `Q_dot_gw` and the two forms of `p_w_s_su_gw` are consistency
checks of the original. The dew point `T_dp_su_gw` of the fumes drives the flag
`flag_dp` of the coil.

**Cooling coil (section 8), the wet exchanger.** Three thermal resistances in
series (air, metal, water) whose air-side and water-side values are referred to
nominal flows by the exponents `a_coil` and `b_coil`. The coil is solved **twice**:
- *dry regime*: `Q_dot_coil_dry` from the air-side equation, with the relative
  humidity at the exhaust (`RELHUM`), 3.997 in the EES stored solution — the
  diagnosis that the dry regime is impossible;
- *wet regime*: the wet-bulb temperature of the inlet air is obtained by
  adiabatic saturation (the humidity ratio `W_s_wb_su_coil` and the enthalpy of
  the saturated air `h_s_wb_su_coil`), the wet cooling power follows from the
  effectiveness of the wet coil (Merckel theory, Lewis number = 1,
  `R_af_coil = R_a_coil·c_p_a_su_coil/c_p_af_coil`, fictitious air capacity rate
  `C_dot_af_coil`), and the exhaust air is saturated
  (`RH_a_ex_coil_wet = 1`, "simplification" in the original); the wet power is
  zero when `flag_dp = 0` (water inlet above the dew point of the fumes), written
  with the five-argument `IF`;
- the **regime of highest cooling power is kept** (Jim Braun's proposal, as in
  the original): `Q_dot_coil = max(Q_dot_coil_dry, Q_dot_coil_wet)`, written with
  the five-argument EES `IF`, and the condensed water `M_dot_w_cond_coil` is set
  to zero in the dry case. The coil power is split into a sensible part
  (`Q_dot_sens_coil`) and a latent one (`Q_dot_lat_coil`).

**Water-environment exchanger (section 7).** Semi-isothermal
(`epsilon_wenv = 1−exp(−NTU_wenv)`): the heat loss `Q_dot_wenv` to the ambient
temperature `T_env = T_amb`, taken from the water (the assumption of the
original is that the combustion chamber is entirely surrounded by water).

**Boiler balance (section 9).** `Q_dot_u_boil = M_dot_w_boil·c_w·(T_w_ex_boil − T_w_su_gw) + Q_dot_coil`,
and the efficiencies `eta_HHV = Q_dot_u_boil/(M_dot_f_boil·HHV)`,
`eta_LHV = Q_dot_u_boil/(M_dot_f_boil·LHV)`.

Inputs: `P_w` 2 bar, `T_w_su_boil`, `V_dot_w_boil_ls`, `T_amb`, `T_a_su_boil`
25 °C, `P_atm` 1 bar, `RH_amb` 0.5, `x_load` (operating point), and the 11 model
parameters of section 2.2 (`V_dot_f_boil_n_m3h`, `AU_gw_N`, `M_dot_g_boil_n`,
`a_gw`, `AU_wenv`, `R_a_coil_n`, `R_w_coil_n`, `R_m_coil`, `M_dot_a_coil_n`,
`M_dot_w_coil_n`, `a_coil`, `b_coil`), plus `e = 0.01`, `LHV = 44 MJ/kg` and
`V_dot_w_boil_ls_n = 9.5 l/s`.

Outputs: `Q_dot_u_boil`, `T_w_ex_boil`, `M_dot_f_boil`, `M_dot_g_boil_kgh`,
`M_dot_w_cond_coil_kgh`, `T_g_ex_boil`, `eta_HHV`, `eta_LHV`, `RH_a_ex_coil`,
`Q_dot_sens_coil`, `Q_dot_lat_coil` (plus about eighty intermediate quantities,
including the consistency checks of the original).

## How to run

The native file does **not** run in CoolSolve (it parses, and the solve stops at
*"Unknown fluid: 'C4H10'"*). The runnable variant
is `condensing_boiler_refsim_coolsolve.eescode` (baseline
`condensing_boiler_refsim_coolsolve.sol`, tested as `CSL-0080:coolsolve`):

```bash
coolsolve ./condensing_boiler_refsim_coolsolve.eescode     # 258 equations, SUCCESS (28 iterations)
```

`coolsolve.conf` (in the folder) keeps the solver pipeline `Newton,
LevenbergMarquardt` with 2000 iterations: the cooling-coil block (52 variables,
coupling moist-air properties, the `cpbar` function and the ε-NTU laws) needs
them at the shipped operating point. The guesses of `.initials` are the values
the block takes at that operating point.

**Operating point of the variant.** The variant runs the operating point of the
solution stored by EES in the source file (`x_load` 0.37, `T_w_su_boil` 30 °C,
`V_dot_w_boil_ls` 5.6 l/s, `T_amb` 20 °C, `T_a_su_boil` 25 °C, `P_atm` 1 bar,
`RH_amb` 0.5) instead of the input block of the file (`x_load` 1,
`T_w_su_boil` 20 °C, `V_dot_w_boil_ls` 5 l/s, `T_amb` 25 °C): at full load the
cooling-coil block does not converge (Newton: *LineSearchFailed* at iteration 0,
residual 1.34e5; with multi-start the residual plateaus at 6.4e-2), and only the
stored operating point has a reference. The **native** file keeps the input
block of the source file.

## Results

Results of the runnable variant at its operating point (compare with the EES
stored solution of the source file, last column):

| Variable | CoolSolve | EES stored |
|---|---:|---:|
| `Q_dot_u_boil` [W] | 106 671.004 | 106 670.473 |
| `Q_dot_u_boil_kW` [kW] | 106.671 | 106.670 |
| `eta_HHV` [−] | 0.978721 | 0.978704 |
| `eta_LHV` [−] | 1.088779 | – |
| `T_w_ex_boil` [°C] | 34.5739 | 34.5734 |
| `T_g_ex_boil` [°C] | 38.3890 | 38.5009 |
| `Q_dot_coil` [W] | 12 176.14 | 11 882.65 |
| `Q_dot_sens_coil` [W] | 2 742.65 | 2 472.87 |
| `Q_dot_lat_coil` [W] | 9 433.49 | 9 409.78 |
| `M_dot_w_cond_coil_kgh` [kg/h] | 13.2412 | 13.1748 |
| `M_dot_f_boil_kgh` [kg/h] | 8.01598 | 8.01598 |
| `M_dot_g_boil_kgh` [kg/h] | 146.1834 | 146.1834 |
| `T_adiab` [°C] | 1827.064 | 1828.635 |
| `Q_dot_gw` [W] | 94 591.83 | 94 863.10 |
| `epsilon_gw` [−] | 0.962064 | 0.965360 |
| `Q_dot_wenv` [W] | 29.1490 | 7.28680 |

The differences on `epsilon_gw`, `Q_dot_gw`, `Q_dot_coil`, `Q_dot_sens_coil` and
`Q_dot_wenv` follow from the model parameters, not from the transcription (see
*Verification*).

The **parametric table of the original** (Table 1, 17 × 9, decoded by
`tools/ees_extract.py` from the binary; rows ordered by `x_load` = 1, 0.75 then
the unfilled template rows, `inf` marks the points EES could not converge — the
water inlet temperature is then below the dew point of the exhaust and the coil
works in the dry regime). Columns: `T_w_su_boil` [°C], `x_load` [−],
`V_dot_w_boil_ls` [l/s] (inputs) and `eta_HHV`, `eta_HHV_cons`, `DELTAT_w_boil`
[K], `epsilon_gw`, `Q_dot_u_boil` [W], `Q_dot_coil` [W] (outputs). The three
converged full-load rows: `eta_HHV` 0.9172 / 0.9078 / 0.8859 (water inlet 26.5 /
29.95 / 37.8 °C) with `Q_dot_u_boil` 269 576 / 266 829 / 260 390 W and
`Q_dot_coil` 28 483 / 26 142 / 20 629 W; at 75 % load `eta_HHV` 0.9314 /
0.9193 / 0.8876.

The water side of the boiler is also given as the state-point arrays `P[i]`,
`h[i]`, `T[i]`, `s[i]` (i = 1 boiler supply, 2 cooling coil supply, 3 dry
exchanger exhaust, 4 boiler exhaust) for the GUI diagrams. The fumes are a
mixture of four ideal gases and are therefore not plotted.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep
     eta_HHV vs T_w_su_boil from the table above, figures/condensing_boiler_refsim_sweep.png -->

## Verification

The transcription is verified against the **solution stored by EES** in the
source file (243 of its 258 variable records hold a value) with the **runnable
variant** at the operating point of that stored solution:

```
compare_solution.py condensing_boiler_refsim_coolsolve.sol <reference>/ees_variables.csv
225 common variables, 74 differ (rtol=0.001)
```

The useful power, the efficiencies and the water temperature agree to better
than 2·10⁻⁵ (`Q_dot_u_boil` 106 671.004 / 106 670.473 W = 5·10⁻⁶,
`eta_HHV` 0.978721 / 0.978704 = 1.8·10⁻⁵, `T_w_ex_boil` 34.5739 / 34.5734 °C =
1.4·10⁻⁵, `M_dot_g_boil_kgh` and `M_dot_f_boil_kgh` identical). The remaining
differences have three documented causes:

1. **The stored EES solution is stale** (`CS-BUG-EXTRACT-STALE`): it belongs to
   an older set of model parameters than the equations window of the file, and to
   older loads. With the parameters of the equations window,
   `AU_gw = AU_gw_N·(M_dot_g_boil/M_dot_g_boil_n)^a_gw = 310·(0.04060649/0.09423)^0.65 = 179.36 W/K`,
   while the stored `AU_gw` is 183.9473657 W/K, the value obtained with
   `a_gw = 0.62` (the exponent of the *Example of solution* block of the file);
   the stored `R_a_coil` = 0.0056699 K/W is the one of `R_a_coil_n` = 0.003 K/W
   (0.003·(0.102/0.03530528)^0.6 = 0.0056699) and not of the 0.0025 K/W of the
   equations window (0.0047249); the stored `Q_dot_wenv` = 7.2868 W corresponds to
   `AU_wenv` = 0.5 W/K and not to the 2 W/K of the equations window
   (2 W/K gives 29.15 W, the value of the variant). This explains the whole
   family of differences on `epsilon_gw` (+3.4·10⁻³), `Q_dot_gw` (−2.9·10⁻³),
   `Q_dot_coil` (+2.5·10⁻²), `Q_dot_sens_coil` (+1.1·10⁻¹) and `ratio_loss`
   (7.5·10⁻¹). Re-running the variant with the parameters of the stored solution
   (`a_gw` = 0.62, `R_a_coil_n` = 0.003 K/W, `R_m_coil` = 10⁻⁴ K/W,
   `AU_wenv` = 0.5 W/K, work copy) gives `Q_dot_u_boil` 106 660.6 W (−9·10⁻⁵),
   `eta_HHV` 0.978626 (−8·10⁻⁵), `T_w_ex_boil` 34.57344 °C, `T_g_ex_boil`
   38.5179 °C (+4.4·10⁻⁴), `Q_dot_coil` 11 888.4 W (+4.8·10⁻⁴),
   `Q_dot_wenv` 7.28680 W (2·10⁻⁸) and 43 differing variables only.
2. **Moist-air properties**: `c_p_a_coil` (+1.1·10⁻²), `c_p_a_su_coil`
   (+8.3·10⁻³), `c_p_a_ex_coil_dry` (+2.1·10⁻²), `T_wb_su_coil` (+2.4·10⁻³),
   `W_a_ex_coil_dry` (+9.7·10⁻³), `h_a_su_coil` (+8.7·10⁻³) — the specific heat
   and the enthalpy of humid air differ between EES 7.888 and CoolProp. All the
   differences stay below 2.1·10⁻² and none of them changes the regime selected
   by the coil.
3. **`h_C4H10_ref` and `h_C4H10_su`**: relative difference 1 (the variant
   replaces them by constants, `CS-GAP-FLUIDS-C8H18`); `x_C4H10 = 0`, so the
   enthalpy difference cancels in `Q_dot_2_bis` and no result is affected.

**Maximum relative difference over the 225 common variables: 1.00** (`h_C4H10_ref`
and `h_C4H10_su`, the constants of the variant); excluding those two, **0.75**
(`ratio_loss = Q_dot_wenv/Q_dot_u_boil`, a consequence of the stale `AU_wenv` of
the stored solution). `RH_a_ex_coil_dry` (1.55·10⁻¹ in the parameter set of the
stored solution) is a diagnostic output of the *dry* regime, which feeds no
equation when the wet regime is selected.

Four records of the stored solution have no value — `C_dot_af_coil`,
`c_p_af_coil`, `AU_coil_wet` and `epsilon_coil_wet`: the internal variables of
the `SUBPROGRAM WETCOIL`, local in EES, which confirms that they must not share
the names of the main program (the suffix `_wc` of the flattening). The 18
variables that exist only in the EES reference are the local variables of the
`cpbar` FUNCTION; the 33 that exist only in the CoolSolve solution are the
internal variables of the flattened coil and the state points of the diagrams.

## Source and attribution

Reference simulation model by **Vincent Lemort** and **Andrés Rodríguez**
(ULiège Thermodynamics Laboratory, Faculty of Applied Sciences), ULiège model
bank (Laborelec toolkit lineage), heat production by combustion, 9 January 2008.
The file header gives their names and the laboratory address; the file is
distributed with the disclaimer *"this model is freely distributed and may not be
sold or distributed for commercial purpose. the user is asked to cite his sources
and the origin of this model."*, the ID stamp `{$ID$ #1206: Jean Lebrun,
Laboratoire de Thermodynamique, Univ. Liege}`. The scientific references are
listed in the header of the model file (ASHRAE HVAC Toolkit 1999; Bourdouxhe et
al. 1994, *ASHRAE Transactions* 100(2), Part 1: Boiler Model; Lebrun and Lemort
2007).

Source file: `~/Nextcloud/thermo_models/Model data bank/Heat_and_Cool_Production_Systems/Heat_Production_by_Combustion/CondensingBoiler_RefSim_Model_VLAR080109.zip!/CondensingBoiler_RefSim_EES_Model_VLAR080109.EES`
(EES 7.888, inside a zip archive, not extracted in the collection). The siblings
of the folder (`BoilerWithModulatingBurner_RefSim_Model_SB080212.zip`,
`CLASSICALBOILER_PARAM_IDENTIFICATION_MODEL_SBJL080212.zip`,
`CLASSICAL_ONOFF_BOILER_SIMULATION_REFERENCE_MODEL_SBJL080212.zip`) are
different components (modulating burner, classical boilers), not variants of
this file; they are separate candidates.

## Conversion log

- **2026-10-06 — import**: `tools/ees_extract.py` (RTF equations window of 831
  lines, EES 7.888, unit system `SI MASS DEG PA C J`: **no unit conversion was
  needed**). `$UnitSystem` directive removed, trailing NUL byte stripped
  (`CS-BUG-EXTRACT-NUL`). The seven input values (section 1) and the eleven
  model parameters (section 2.2) that EES holds in its **control panel**, not in
  the equations window, are written as display strings by the extraction and
  were restored as statements with their original values and units
  (`CS-GAP-PARAMETRIC`); the parametric table of the file is documented in
  *Results*. The display strings of the original (description, nomenclature,
  references) are kept as comments and the French section titles of `cpbar` were
  translated. The eleven output names and the "HHV = 1.11·LHV, rule of thumb"
  line are **display strings in the source file**, not equations, and are kept as
  comments (reading them as equations — as a first transcription of this import
  did — invents twelve redundant equations and makes the system non-square).
- **`PROCEDURE COILWET` / `SUBPROGRAM WETCOIL` flattened into the main program,
  decision D10**: the source calls the subprogram from the `else` branch of
  `COILWET` (`if (flag_dp=0)`: no wet power). Call tag `wc`; formal = actual
  arguments (`flag_dp`, `M_dot_a_coil`, `C_dot_w_coil`, `c_p_a_su_coil`,
  `T_w_su_coil`, `T_wb_su_coil`, `h_a_su_coil`, `R_a_coil`, `R_m_coil`,
  `R_w_coil`, `P_atm` → `Q_dot_coil_wet`, `T_wb_ex_coil_wet`). Renamed internal
  variables: `C_dot_af_coil` → `C_dot_af_coil_wc`, `C_dot_max_coil_wet` →
  `C_dot_max_coil_wet_wc`, `C_dot_min_coil_wet` → `C_dot_min_coil_wet_wc`,
  `omega_coil_wet` → `omega_coil_wet_wc`, `R_af_coil` → `R_af_coil_wc`,
  `AU_coil_wet` → `AU_coil_wet_wc`, `NTU_coil_wet` → `NTU_coil_wet_wc`,
  `epsilon_coil_wet` → `epsilon_coil_wet_wc`, `T_a_ex_coil_wet` →
  `T_a_ex_coil_wet_wc`, `RH_a_ex_coil_wet` → `RH_a_ex_coil_wet_wc`,
  `h_a_ex_coil_wet` → `h_a_ex_coil_wet_wc`, `c_p_af_coil` → `c_p_af_coil_wc`
  (the suffix is needed because the main program uses the same names without it;
  no collision was created). The two outputs of the procedure are
  `Q_dot_coil_wet = IF(flag_dp,0,Q_dot_coil_wet_if,0,Q_dot_coil_wet_if)` and
  `T_wb_ex_coil_wet = IF(flag_dp,0,T_wb_ex_coil_wet_if,T_wb_su_coil,T_wb_ex_coil_wet_if)`,
  where `Q_dot_coil_wet_if` and `T_wb_ex_coil_wet_if` are the two equations of the
  subprogram that define them.
- **2026-10-06 — comment-only edit**: the stoichiometry block of section 5.7.1
  (a display string whose opening `"` ended its line) was written as one string
  per line (`CS-BUG-MULTILINE-COMMENT-START`), which changes no equation.
- **2026-10-06 — added**: the state-point arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`
  of the water side (16 post-processing equations), for the GUI diagrams; the
  results of the model are unchanged.
- **2026-10-06 — removed**: the `Example of solution` comment block of the
  original (224 lines of values of an older run), documented in *Verification*.
  No equation was touched.
- **2026-10-06 — runnable variant** `condensing_boiler_refsim_coolsolve.eescode`,
  changes forced by the gaps only, each one valid EES (no CoolSolve-only
  syntax): (1) `C%` → `C_pc` and `H%` → `H_pc`, a renaming that CoolSolve no
  longer requires;
  (2) `MM_C4H10=molarmass(C4H10)` → `MM_C4H10=58.12` (the value EES returns,
  `CS-GAP-FLUIDS-C8H18`) and `h_C4H10_su`/`h_C4H10_ref` → 0 (they only enter
  `Q_dot_2_bis` multiplied by `y_C4H10_su = 0`); (3) the seven five-argument
  `IF(A,B,X,Y,Z)` calls (the five of the source and the two that select the
  outputs of the flattened coil) rewritten as three-argument `IF(cond,X,Z)`
  (CoolSolve accepts the five-argument form now, so this rewrite is not
  required): the original returns X if A<B, Y if A=B and Z if A>B, so
  `IF(A,B,X,X,Z) = IF(X−A, X, Z)` and `IF(A,B,1,1,0) = IF(B−A, 1, 0)`; the two
  coil outputs read `Q_dot_coil_wet=if(flag_dp, Q_dot_coil_wet_if, 0)` and
  `T_wb_ex_coil_wet=if(flag_dp, T_wb_ex_coil_wet_if, T_wb_su_coil)`. The
  operating point of the variant is the one of the stored EES solution (see
  *How to run*).
- **Level**: taxonomy §3 — one adiabatic combustion chamber (five fictitious
  processes), three heat exchangers (two of them ε-NTU models, one of them
  solved twice with a regime selection), a moist-air block (wet-bulb by
  adiabatic saturation, humidity ratios, dew points), a user `FUNCTION`
  (`cpbar`), a parametric study in the original and 258
  equations: above level 2 (several sub-models and closures, moist air,
  ideal-gas chemistry), below level 4 (no optimisation, no
  distribution/discretisation, no dynamic behaviour) → **level 3**.
## Limitations and CoolSolve gaps

Gaps blocking the native file (all in `model.json` `missing_features`, see the
CoolSolve register `docs/model_library_support.md`):

- **`CS-GAP-FLUIDS-C8H18`** — the EES ideal-gas substance `C4H10` of
  `molarmass(C4H10)` and `enthalpy(C4H10,T=…)` is unknown to CoolSolve
  (*"Unknown fluid: 'C4H10'"*); the same gap as `C8H18`, "the other hydrocarbons
  of the EES ideal-gas substance list beyond C3". `x_C4H10 = 0`, so the terms
  that use it vanish, but the calls must still evaluate.
- **`CS-BUG-MULTILINE-COMMENT-START`** is worked around by a comment-only edit
  (stoichiometry block) and does not block the file.

Convergence: at the input block of the source file (full load) the cooling-coil
block does not converge (Newton *LineSearchFailed* at iteration 0, residual
1.34·10⁵; with multi-start the residual plateaus at 6.4·10⁻²). The same block
converges in 28 iterations at the operating point of the stored EES solution,
which is the operating point shipped in the variant. This is a convergence
question, not a registered gap: the simplest remedy would be a
`[deepsearch]`-style pipeline or better scaling of the moist-air block.

Physical limitations of the model (as in the original): the combustion is
adiabatic and the heat loss is taken from the water only; the dissociation of
CO2 is not modelled (`Q_dot_4 = 0`); the conductance of the water-environment
exchanger is a fixed input; the air excess is constant; the water side of the
water-environment exchanger is isothermal; the fumes are treated as an
ideal-gas mixture with a mean specific heat, so they are not a CoolProp fluid
and cannot be drawn on a diagram; at full load the ε-NTU model of the dry
exchanger leaves the fumes at about 205 °C (the conductance grows as
`M_dot_g^0.65` while the capacity rate grows as `M_dot_g`, so `NTU_gw` falls with
the load).

## Related models

- `CSL-0006` *boiler_mean_specific_heat* — same component family (boiler, mean
  specific heat of the combustion products, ε-NTU exchangers, adiabatic flame
  temperature).
- `CSL-0005` *cpbar_combustion_products* — the `cpbar` function used by this
  model (section 5.5 and the gas-water exchanger); the copy kept in this file is
  the one of the source.
- `CSL-0081` *vertical_ghes_refsim* — another reference model of the same ULiège
  model bank (ground heat exchangers, 13 February 2008).
- `CSL-0166` *boiler_modulating_burner_refsim*: the condensing boiler of the same model bank (modulating-burner RefSim model, 2008 model bank).
