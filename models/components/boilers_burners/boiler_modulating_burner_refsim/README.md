# Boiler with modulating burner: steady-state reference model

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0166`

Steady-state reference simulation model (RefSim) of a fuel-oil or gas boiler
with a limited-modulating burner, from the 2008 ULiège model bank. The burner
runs in one of four regimes selected from the water exhaust-temperature set
point: **OFF**, **ON/OFF** (cycling between the minimum modulating limit and
off), **MODULATING** (the fuel flow is modulated so that the water exhaust
temperature reaches the set point) and **FL** (full load). Every regime
evaluates the same boiler: adiabatic combustion with excess air, gas-water
epsilon-NTU exchanger, water-environment exchanger, efficiency.

| | |
|---|---|
| **Category** | Components › Boilers and burners |
| **Fluids** | combustion products of a fuel oil C₁₂.₈H₂₃.₃ (y_C = 86.9 %, y_H = 13.1 %) via the ideal-gas substances CO2, CO, H2O, N2, O2 |
| **Size** | 128 equations in the runnable variant (largest block: 13); native file refused as over-determined (198 equations / 176 unknowns) |
| **Source** | ULiège model bank 2008-02-12 — `BoilerWithModulatingBurner_RefSim_Model_SB080212.zip` |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory) |
| **License** | MIT (lab disclaimer of the original: freely distributed, may not be sold, cite origin) |
| **CoolSolve** | v0.3.0@7addbbc — native file **blocked** by `CS-GAP-IF-DIRECTIVE`, `CS-GAP-IF5`, `CS-BUG-STRING-CALL-OUT`; runnable variant verified against the EES stored solution |

## Problem statement

Modelling a heating boiler whose burner can only modulate between a minimum
fraction `X_MOD_MIN = 0.2` of the full-load fuel flow and full load, and
cycles on/off below that. Given the water volume flow (2150 l/h), supply
temperature (70 °C) and exhaust-temperature set point, the model returns the
regime, the water exhaust temperature `t_w_ex`, the useful power `Q_dot_u`,
the consumed power `Q_dot_c = M_dot_f*LHV`, the efficiency
`eta = Q_dot_u/Q_dot_c`, the ON/OFF duty fraction `theta`, the fuel flow
`M_dot_f`, the burner fraction `X_burner` and the auxiliary (pump + fan)
electric consumptions.

## Model

Boiler module (identical in the three evaluations of the original — see
*Conversion log* for the MODULE flattening):

- **Combustion reference model**: adiabatic combustion chamber. Fuel
  C_nH_m characterised by its carbon mass fraction `y_C` (n = 12·(1−y_C)/y_C);
  stoichiometric fuel-air ratio from the molar mass of air; excess air `e`
  from the fuel-air ratio `f = 0.06` (1/f = (1/f_st)(1+e)); energy balance
  Q̇₁+Q̇₂+Q̇₃+Q̇₄+Q̇₅ = 0 with the mean specific heat of the products from the
  `cpbar` procedure (library model `CSL-0005`), giving the adiabatic
  combustion temperature ≈ 1929 °C.
- **Gas-water exchanger**: epsilon-NTU, `AU_gw = AU_gw_FL·(M_dot_f/M_dot_f_FL)^0.65`
  (part-load law of the original, ASHRAE HVAC1 Toolkit).
- **Water-environment exchanger**: epsilon-NTU with constant `AU_wenv`,
  losses to the ambient at 25 °C.
- **Efficiency** `eta = Q_dot_u/Q_dot_c`, Q̇_c = ṁ_f·LHV.

Regime algorithm (PROCEDURE `BOILER_REGIME`): FL if set ≥ t_w_ex_FL,
modulating if between t_w_ex_MIN and t_w_ex_FL, ON/OFF if between t_w_ex_OFF
and t_w_ex_MIN, OFF below. In the ON/OFF regime the duty fraction
`theta_ON\OFF` interpolates the exhaust temperature between the MIN-limit and
OFF states. Auxiliary consumptions from the nominal power `Q_dot_u_n`
(correlations of the original, with the 5-argument `IF` of EES).

| Inputs (stored operating point) | Value | Outputs (ON/OFF regime) | Value |
|---|---|---|---|
| `V_dot_w_l\h` water flow | 2150 l/h | regime | ON\OFF |
| `t_w_su` water supply temp. | 70 °C | `t_w_ex` water exhaust temp. | 71.00 °C (set point) |
| `t_w_ex_set` set point | 71 °C | `theta` duty fraction | 0.2802 |
| `X_MOD_MIN` min burner fraction | 0.2 | `Q_dot_u` useful power | 2500.6 W |
| `M_dot_f_FL` full-load fuel flow | 0.0013 kg/s | `Q_dot_c` consumed power | 3132.9 W |
| `f` fuel-air ratio | 0.06 | `eta` efficiency | 0.798 |
| `AU_gw_FL` / `AU_wenv` conductances | 84 / 12 W/K | `M_dot_f` fuel flow | 3.643·10⁻⁴ kg/s |
| `y_C` / `y_H` fuel C / H mass fractions | 0.869 / 0.131 | `X_burner` burner fraction | 1 |
| `Q_dot_u_n` nominal useful power | 55 000 W | `W_dot_aux_lf` / `_gf` auxiliaries | 124.8 / 90.0 W |

Seven of the inputs (`V_dot_w_l\h`, `t_w_su`, `t_w_ex_set`, `X_MOD_MIN`,
`M_dot_f_FL`, `AU_gw_FL`, `AU_wenv`) were supplied by the parametric table of
the original EES file and are restored as equations (values of the stored
run); see *Conversion log*.

## How to run

The native file `boiler_modulating_burner_refsim.eescode` is valid EES and is
**refused by CoolSolve** (*"There are 198 equations and 176 unknowns. The
system is not square"*, then `IF with 5 arguments` and
*"String variable not found: regime$"* once the first gap is worked around):
the compile-time `$if` directives on the runtime string `regime$` are parsed
but not evaluated, so all four regime branches are kept as equations.

The runnable variant resolves the branches for the stored operating point
(ON/OFF regime):

```bash
coolsolve ./boiler_modulating_burner_refsim_coolsolve.eescode
```

It needs `.initials` (guesses; the implicit blocks are the three
combustion/exchanger evaluations). Tested by `tools/test_models.py` as
`CSL-0166:coolsolve`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. eta or t_w_ex vs t_w_ex_set
     showing the four regimes (parametric sweep in the CoolSolve GUI),
     figures/boiler_modulating_burner_refsim_regimes.png -->

## Results

Stored operating point (ON/OFF regime): the set point 71 °C lies between the
OFF-state exhaust temperature (t_w_ex_OFF = 69.78 °C, burner off, water
cooling to the environment) and the MIN-limit exhaust temperature
(t_w_ex_MIN = 74.12 °C, burner at the minimum modulating fraction), so the
burner cycles with duty fraction θ = 0.280 and delivers on average 2500.6 W
with η = 0.798. The MIN-limit state itself gives 10307.8 W at η = 0.922; the
full-load state 51214.6 W at η = 0.916 with t_w_ex_FL = 90.48 °C (a set point
above 74.12 °C and below 90.48 °C would give the modulating regime, above
90.48 °C full load).

## Verification

**The variant is the verified file** (the native file does not solve in
CoolSolve, by definition of its status). Reference: the EES stored solution
(`ees_variables.csv`, 116 variables). The stored values are **stale**
(`CS-BUG-EXTRACT-STALE`): the last run of the original was the ON/OFF run
(inputs above), while the module variables still carry values of an earlier
MODULATING run (e.g. `t_w_ex_MOD` = 90 °C = an older set point) and of an even
older run. Only the 43 variables common with the variant are compared:

```text
43 common variables, 0 differ (rtol=0.001)
```

Maximum relative difference **2.25e-4** (`Q_dot_u_FL`; likewise `eta_FL`,
`t_w_ex_FL` 5.1e-5), consistent with the CoolProp vs EES difference on the
mean specific heats of the combustion products at the 1929 °C adiabatic
temperature. The variables of the last ON/OFF run match to 4.6e-5 or better
(`t_w_ex`, `theta`, `Q_dot_u`, `Q_dot_c`, `M_dot_f`, `W_dot_aux_*`, the OFF
block and the FL/MIN states).

Not compared, by name:

- the stored `*_MOD`/`*_ss` values and the singletons `n`, `e`, `f_st`, `MMa`,
  `c_p_p`, `c_p_g`…: stale or renamed by the D10 flattening. Cross-checked by
  hand against the variant's `n_min/n_fl` = 1.808975834 (exact), `e_fl` =
  1.4897e-1 (5.7e-5), `f_st_fl` = 6.8938e-2 (5e-5), `t_adiab_fl` = 1929.06 °C
  (0.07 %), `e1_fl` = 0.153555 (1e-4);
- `eta` and `theta_ON\OFF` (no variable-info record in the file); recomputed
  from the stored values: 2500.569/3132.736 = 0.7981 and
  (71−69.7846)/(74.1222−69.7846) = 0.28021 ✓;
- the strings `regime$`, `Write_Results$`.

The results lookup table `Lookup_Results` that the original fills through
`WRITERESULTS` (the decoded "parametric table1 (11840×2)" of the extraction is
a false positive, see *Conversion log*) is not reconstructed: CoolSolve
silently drops lookup writes inside a procedure (`CS-BUG-LOOKUP-WRITE`), and
its 14 cells are exactly the 14 arguments of the call, all verified above.

## Source and attribution

Model by **Stéphane Bertagnolio** (ULiège Thermodynamics Laboratory), model
bank "Heat and Cool Production Systems", 2008-02-12; header of the original:
"Classical Boiler with Modulating Burner", contact and disclaimer of the
laboratory included. References cited by the original: ASHRAE TC4.7 **HVAC1
Toolkit** (J.P. Bourdouxhe, M. Grodent, J. Lebrun, C. Saavedra) for the
auxiliary-consumption correlations and the part-load `AU_gw` law.

Source file (EES 7.888, comments in English), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/Heat_and_Cool_Production_Systems/Heat_Production_by_Combustion/BoilerWithModulatingBurner_RefSim_Model_SB080212.zip!/BoilerWithModulatingBurner_RefSim_EES_Model_SB080212.EES`
(inventory candidate `TM-0491`; the zip also carries the `UserLib/` copy of
the combustion library, imported as `CSL-0005`).

## Conversion log

- **2026-10-09 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already `SI MASS DEG PA C J`; the `{$ID$…}` licence tag (J.
  Lebrun lab licence) was removed; comments kept in English. **Inputs
  restored from the stored solution** (parametric-table inputs of the
  original, §8 of `ees_import.md`): `V_dot_w_l\h` = 2150, `t_w_su` = 70,
  `t_w_ex_set` = 71, `X_MOD_MIN` = 0.2, `M_dot_f_FL` = 0.0013, `AU_gw_FL` =
  84, `AU_wenv` = 12 — the values commented out in the original text
  (0.001292, 83.4, 11.65) are older table values, quoted in the model as
  comments. Cross-checked: `AU_gw_MIN` = 84·0.2^0.65 = 29.5086 = stored,
  `Q_dot_c_FL` = 0.0013·43e6 = 55900 = stored, `NTU_wenv_OFF` = 12/2500.569 =
  0.0047989 = stored. The MODULATING-call inputs `t_w_su_MOD` = 70, `f_MOD` =
  0.06, `AU_wenv_MOD` = 11.65 are restored from the stale stored MODULATING
  solution (their stored records hold 1 = never rewritten): `Q_dot_u_MOD` =
  2500.569·(90−t_w_su_MOD) gives t_w_su_MOD = 69.995 ≈ 70.
- **2026-10-09 — MODULE flatten (decision D10)**: the two `MODULE`s
  `BOILERSS` (called twice: MIN limit and FL) and `BOILERMOD` (called once in
  the MODULATING branch) have **identical bodies**; each `CALL` is replaced by
  a copy of the body in the main program. Formal → actual arguments and tags:
  call MIN → tag `_min` (`M_dot_f_ss` → `M_dot_f_MIN`, `AU_gw_ss` →
  `AU_gw_MIN`, `t_w_su_ss` → `t_w_su`, `f_ss` → `f`, `V_dot_w_l\h_ss` →
  `V_dot_w_l\h`; outputs → `t_w_ex_MIN`, `Q_dot_u_MIN`, `Q_dot_c_MIN`,
  `eta_MIN`), call FL → tag `_fl` (`M_dot_f_FL`, `AU_gw_FL`; outputs
  `*_FL`), call MOD → tag `_mod` (`M_dot_f_MOD`, `AU_gw_MOD`, `t_w_su_MOD`,
  `f_MOD`, `AU_wenv_MOD`; outputs `*_MOD`). Internal variables renamed with
  the tag (`n_min`, `e_fl`, `t_adiab_mod`, `Q_41_min`, `x2_fl`, …); the
  formal inputs `y_C` and `f_ss`/`f_MOD` are reassigned inside the body, so
  each call gets a local copy (`y_C_min = y_C`, …) as in the module. The
  formal input `y_H` is never used in the body (dead input, kept in the
  mapping). The `FUNCTION`/`PROCEDURE`s (`cpbar`, `BOILER_REGIME`,
  `WRITERESULTS`) are kept as procedures, valid EES.
- **2026-10-09 — "parametric table1 (11840×2)" is a false positive**: the
  extraction report announces a 11840×2 parametric table with columns `v` and
  `Regime$` (values `inf`, 171, 172…). Hand check of the binary: the
  equations text ends at byte 10494, the unit settings at 10510, and the 116
  variable records of 122 bytes span bytes 10510–24662; the reported table
  sits at offset 10799, **inside the variable records**, and its "columns"
  are fragments of record strings (`Regime$` is the 11th argument of
  `WRITERESULTS`, found at byte 129237 = record area). Calling the decoder
  with the correct start offset (24662) finds **zero** tables. The original
  file has no parametric table readable from the binary and no embedded
  lookup table; `Lookup_Results` is created at run time by `WRITERESULTS`
  (write-only). Registered as `CS-BUG-EXTRACT-TABLE-FP`.
- **2026-10-09 — variant `boiler_modulating_burner_refsim_coolsolve`** (only
  what the gaps force; the native file keeps everything):
  1. the four `$if regime$…` branches resolved for the stored ON/OFF
     operating point (`CS-GAP-IF-DIRECTIVE`): ON/OFF branch active, OFF/FL/
     MODULATING branches kept as comments, `$DOLAST/$ENDDOLAST` (unknown
     directives in CoolSolve, no effect on the equation set) removed;
  2. `IF(Q_dot_u_n,35000,100,0,0)` → `if(35000-Q_dot_u_n,100,0)`
     (`CS-GAP-IF5`; same value 100 W below 35 kW, 0 above, tie included);
  3. the `CALL WRITERESULTS` removed (`CS-BUG-STRING-CALL-OUT`: the call
     fails because `regime$` is produced by another CALL; its lookup writes
     are silently dropped anyway per `CS-BUG-LOOKUP-WRITE`, its only
     surviving effect was `Write_Results$ = 'OK'`). `regime$` is still
     computed by `CALL BOILER_REGIME`;
  4. the MODULATING-call inputs commented with their branch.
  All other equations, names, values and comments are those of the native
  file. The function form `CALL cpbar(...)` with the multi-output procedure
  is as in the original (`CSL-0034` pattern).
- **2026-10-09 — level**: equations 128 (1) + largest block 13 (1) +
  procedures/copied library (1) + three coupled components — combustion
  chamber, gas-water HX, water-environment HX (1) + part-load modulating
  physics (1) + curated guesses (1) = score 5 → **level 3**.

## Limitations and CoolSolve gaps

Gaps blocking the native file (all in `missing_features`):

- `CS-GAP-IF-DIRECTIVE`: the compile-time `$if` directives of the original
  select one regime branch from the runtime string `regime$` (value
  available in EES from the previous calculation — the stored solution mixes
  the ON/OFF run with stale MODULATING values, proving that idiom);
  CoolSolve parses but does not evaluate them, keeps all four branches, and
  refuses the over-determined system (198 equations / 176 unknowns).
- `CS-GAP-IF5`: the 5-argument `IF(Q_dot_u_n,35000,100,0,0)` of the
  auxiliary-consumption correlations is not implemented (evaluation error).
- `CS-BUG-STRING-CALL-OUT`: `regime$`, produced by `CALL BOILER_REGIME`,
  is not found when passed as an argument to `CALL WRITERESULTS`
  (*"String variable not found: regime$"*).

Non-blocking, documented:

- `CS-BUG-LOOKUP-WRITE`: the 14 `lookup('Lookup_Results',…)=…` writes of
  `WRITERESULTS` are silently dropped (the results table of the original is
  not produced; nothing else changes).
- The `$DOLAST/$ENDDOLAST` directives are unknown to CoolSolve (warning);
  they only order the solution in EES and are removed in the variant.
- Cosmetic: the `molarmass(): fluid 'CO2'` and `MolarMass(): fluid 'Air'`
  hints (ideal-gas substances intended, as in `CSL-0005`).

Physical limitations (as in the original): the ON/OFF regime models cycling
by a steady-state duty fraction; condensation is not modelled (see
`CSL-0080` for the condensing case); only complete combustion is evaluated
here (`Q_dot_4 = 0`, `f` below stoichiometric).

## Related models

- `CSL-0005` *cpbar_combustion_products*: its `cpbar` procedure is copied
  into this model (until `$INCLUDE library:…`, `CS-FEAT-IMPORT`).
- `CSL-0006` *boiler_mean_specific_heat*: the classical ON/OFF boiler
  exercise of the same model bank (its `_onoff` variant corresponds to
  inventory row TM-0492).
- `CSL-0080` *condensing_boiler_refsim*: the condensing boiler of the same
  model bank (five-step combustion, dry and wet exchangers).
