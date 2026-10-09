# Air-to-air glycol run-around heat-recovery loop

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0162`

Two air coils (one on the extraction air, one on the fresh air of an air
handling unit) linked by a glycol loop with a pump: a run-around heat-recovery
system. Each coil is described by classical epsilon-NTU equations under Braun's
hypothesis (the fully dry and fully wet regimes are computed simultaneously and
the regime of largest capacity is kept), the wet coil using a fictitious gas at
the wet-bulb temperature. The glycol properties come from the ULiège BrineProp
library, the piping pressure drop from the Colebrook equation, and the pump
power closes the glycol loop (the pump heat input warms the glycol).

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | AirH2O (humid air), ethylene glycol 25 % (BrineProp) |
| **Size** | 169 equations / 144 unknowns in the native file (both `$IF` branches kept, see *Conversion log*); the winter-resolved variant is square at 271 equations (largest block: 65) |
| **Source** | ULiège model bank — air-to-air glycol recovery loop, 10 January 2008 (`GLYCOL_RECOVERY_LOOP_SB080110.EES`) |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@7addbbc — native file blocked (CS-GAP-IF-DIRECTIVE, CS-GAP-IF5, CS-GAP-CALL-EXPR-OUT, CS-GAP-INCLUDE); the runnable `_coolsolve` variant is in turn blocked by the solver bug `CS-BUG-NEWTON-CYCLE` |

## Problem statement

An air handling unit extracts 11 500 m³/h of air at 23 °C / 50 % RH and blows
the same fresh-air flow, supplied at −12 °C / 90 % RH, through a recovery
loop: the extracted air first passes a coil where it is cooled (partly below
its dew point, so it is dehumidified), the recovered heat is carried by 3.2
m³/h of a 25 % ethylene-glycol solution and a pump to a second coil where the
cold fresh air is preheated. The two coils are supposed to have the same
characteristics (nominal thermal resistances R_a_n = 1.511e-4 K/W on the air
side, R_gw_n = 1.46e-5 K/W on the glycol side, corrected with the mass-flow
exponents 0.6 and 0.8; metal resistance zero). The model returns the outlet
states of both airs, the recovered power (total, sensible, latent), the
condensate flow, the loop pumping power and a recovery effectiveness.

## Model

- **Coils** (heating and cooling): `Q = C_min·ε·(T_w,su − T_a,su)` with the
  counterflow effectiveness
  ε = (1 − exp(−NTU(1−ω)))/(1 − ω·exp(−NTU(1−ω))), NTU = AU/C_min and
  ω = C_min/C_max; AU is the series of the two convective resistances and the
  metal resistance, corrected from the nominal flows.
- **Wet coil** (Braun hypothesis, following Braun, Klein & Mitchell, 1989,
  and Ding, Eppe, Lebrun & Wasacz, 1990): the air is replaced by a fictitious
  gas whose specific heat is the one of the moist air at constant wet-bulb
  temperature; a fictitious semi-isothermal contact surface gives the outlet
  humidity. The regime kept is the one of largest capacity
  (`Q_dot_cooling = MAX(dry, wet)`), the regime selections being written with
  the EES intrinsic `IF(A,B,X,Y,Z)`.
- **Glycol loop**: Colebrook friction in the piping (roughness 0.1 mm), the
  pressure drop of the two coils at nominal flow, and the pump
  `W_dot = V_dot·ΔP/η` whose heat is added to the glycol between the coils.
- **Glycol properties** (specific heat, density, dynamic viscosity at the mean
  glycol temperature): the `BRINEPROP` procedure of the ULiège BrineProp
  library, see `CSL-0079`.

Inputs and outputs are listed in the header of the `.eescode` files.

## How to run

The native file `glycol_runaround_recovery_loop.eescode` cannot be solved by
CoolSolve (see *Conversion log*); it is kept in native EES syntax. The runnable
transcription `glycol_runaround_recovery_loop_coolsolve.eescode` (winter
regime, values of the stored run) currently **fails to converge** on the
solver bug `CS-BUG-NEWTON-CYCLE` (65-equation block; the equations are all
satisfied at the EES stored point, see *Verification*). It has no `.sol` yet;
when the bug is closed, solve it and commit its `.sol` to enable the
regression test (`CSL-0162:coolsolve`). The BrineProp coefficient tables are
shipped as the companion tables `glycol_runaround_recovery_loop_coolsolve-Brine1/2.csv`
(same decoded values as in `CSL-0079`).

## Results

Values of the EES stored run (winter regime): extracted air 23 °C / 50 % RH →
11.04 °C / 88.3 % RH; fresh air −12 °C / 90 % RH → 3.91 °C / 24.2 % RH;
recovered power 62 359 W (sensible 47 001 W, latent 15 358 W), condensate
21.15 kg/h, glycol −2.57 °C → 15.27 °C, pump 173.4 W (Colebrook λ = 0.0340,
Δp = 78 031 Pa), ε_recovery = 0.4534.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric plot
     (e.g. recovered power or epsilon_recovery vs glycol flow rate), figures/… -->

## Verification

The native file cannot be solved (gaps of the card), so the verification
concerns the runnable variant, and is **pointwise**: at the EES stored point
(`.initials`, the 144 stored values) the residuals of the 65 equations of the
failing block are ≤ 0.04, except the humid-air enthalpy
`h_cooling_c_wet = ENTHALPY(AirH2O, t=t_cooling_c_wet, R=1, P=P_atm)`:
25 778 J/kg against 25 835 J/kg, i.e. a residual of 57 J/kg (0.22 %, the EES
vs CoolProp humid-air formulation difference at saturation, as in the other
humid-air models of the library); the wet-bulb calls agree to 0.034 K. The
flattened BrineProp chain reproduces the stored glycol properties exactly
(μ = 0.0029435 Pa·s, ρ = 1036.229 kg/m³, c_p = 3805.351 J/kg-K). The model
itself stops there today: the block solver reports `SingularJacobian` from
iteration 0 although the block Jacobian is full rank (condition number 1.9e7)
— bug `CS-BUG-NEWTON-CYCLE` in the CoolSolve register. The equations being
satisfied at the stored point, the stored values are also reproduced as
outputs of the variant once the bug is fixed; a `T-RECHECK` of this model
should solve the variant, compare it with
`~/Nextcloud/thermo_models/modeles/Recovery_Loop/GLYCOL_RECOVERY_LOOP_SB080110.EES`
via `compare_solution.py` and commit the `.sol`.

## Source and attribution

Model of the ULiège model bank by **Stéphane Bertagnolio** (ULiège
Thermodynamics Laboratory), 10 January 2008; the file header carries the
laboratory disclaimer ("freely distributed, may not be sold, cite origin").
References cited by the original: Braun J. E., Klein S. A., Mitchell J. W.
(1989), *Effectiveness Models for Cooling Towers and Cooling Coils*, ASHRAE
Transactions 92(2), 164–174; Ding X., Eppe J. P., Lebrun J., Wasacz M. (1990),
*Cooling Coil Models to be used in Transient and/or Wet Regimes…*, SSB'90,
Liège; EES (Klein, F-Chart software).

Source file (EES 7.888, comments in English), collection of S. Quoilin:
`~/Nextcloud/thermo_models/modeles/Recovery_Loop/GLYCOL_RECOVERY_LOOP_SB080110.EES`
(inventory candidate `TM-0321`, duplicate group DG-0076 with TM-0320, Jaccard
0.92, and TM-0476 inside a zip, Jaccard 0.99 — both left untouched, see
*Conversion log*).

## Related models

- `CSL-0074` *cooling_coil_refsim*: the same Braun wet-coil formulation
  (fictitious wet-bulb gas, contact surface, dry/wet selection by maximum
  capacity) for a cooling coil with a brine side; sibling of the same model bank.
- `CSL-0079` *brineprop_secondary_refrigerants*: the BrineProp library model;
  its runnable variant contains the same flattened `BRINEPROP` procedure and
  the same coefficient tables.
- `CSL-0161` *plate_hx_thermal_resistances*: imported in the same wave with the
  same pattern (native blocked by `$IF` and `CALL` gaps, runnable variant).

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`, CoolSolve repository): unit
  system already SI-°C-Pa-J; the EES licence tag removed; comments kept in
  English; standard header added. **Diagram-window inputs restored as
  equations** with the values of the stored run: `t_ge_a_su = 23 [C]` (the
  diagram text of the original says 22 [C]) and `L_pipe = 6 [m]` (diagram text
  2 [m]); all other inputs agree with the diagram text. The trailing
  commented-out results block of the original (≈125 lines, values of an older
  run with `L_pipe = 4`, `t_ge_a_su = 22` and λ = 0.6861) was removed — it is
  inconsistent with the stored solution and with the Colebrook closure; the
  commented polynomial fits of the wet-bulb/humidity calls (4 lines) and the
  output declarations of the diagram window (16 lines) were removed too
  (logged here, listed in the README *Results* instead).
- **Gaps blocking the native file** (all pre-registered; no new gap of the
  card): `CS-GAP-IF-DIRECTIVE` (the `$IF recovery_regime$='winter'` /
  `'summer'` branches are both kept → 169 equations / 144 unknowns),
  `CS-GAP-IF5` (four `IF(Q_dot_cooling_dry,Q_dot_cooling_wet,…)` regime
  selections), `CS-GAP-CALL-EXPR-OUT` (the three `CALL BRINEPROP(…:c_p_gw/1000)`
  style outputs), `CS-GAP-INCLUDE` (BrineProp comes from the implicit
  `USERLIB` of EES, `Brineprop.lib`, TM-0479).
- **2026-10-08 — runnable variant** `glycol_runaround_recovery_loop_coolsolve.eescode`,
  changing only what the gaps force, each change valid EES unless noted:
  1. the `$IF` branches are resolved for the stored run (winter): the winter
     block is kept unconditional, the summer block is removed
     (`CS-GAP-IF-DIRECTIVE`), as in CSL-0009/CSL-0012/CSL-0161;
  2. the four 5-argument `IF(A,B,X,Y,Z)` regime selections are written with
     the 3-argument `if(cond, a, b)`, `cond = Q_dot_cooling_wet −
     Q_dot_cooling_dry` (`CS-GAP-IF5`; **CoolSolve-only syntax**, not valid
     EES). EES selects the wet value also at equality (`A = B`), CoolSolve the
     dry one there — a measure-zero case, not met in the stored run; the
     condensate `IF` (whose equality branch is 0) is strictly equivalent;
  3. the three `CALL BRINEPROP` calls are **flattened into the main program**
     (`CS-GAP-INCLUDE` / `CS-GAP-LOOKUP-PROC`), one block per property, in the
     manner of the `CSL-0079` variant: the concentration selector of the
     original (22 range checks and an 11-branch ladder, procedure-only
     statements) reduces here to `Fl_brine_gw = 1` ('EG' 25 % within its range
     0–56.1 %); the property indicator `Pr` = 3 / 2 / 5 (SPECHEAT / DENSITY /
     DYNVISC) selects the coefficient column read from the companion tables;
     the internal variables are renamed per call with the suffix `_gw`
     (`Row_cp_gw[k]`, `Funkt_cp_gw`, …); the DUPLICATE loop of the original
     procedure is kept as a `DUPLICATE` (allowed in the main program);
  4. the **expression outputs** of the calls are applied as separate equations
     (`CS-GAP-CALL-EXPR-OUT`): `c_p_gw = Funkt_cp_gw/1000`,
     `rho_gw = Funkt_rho_gw`, `mu_gw = exp(Funkt_mu_gw)/1000` — the values
     match the stored ones (see *Verification*).
  The variant inherits the `.initials` of the stored solution plus guesses for
  its new internal variables; it is **not solved yet**
  (`CS-BUG-NEWTON-CYCLE`, new row of the CoolSolve register).
- **2026-10-08 — inventory**: TM-0321 (the representative of DG-0076) set to
  `added` → `CSL-0162`. TM-0320 (Jaccard 0.92) and TM-0476 (Jaccard 0.99,
  inside a zip) kept at the C-137 decision (`todo`): near-duplicates that
  could be `duplicate` after an equation diff, left to the manager.
- **Level justification** (taxonomy.md §3): equations 271 (variant) → 2;
  largest block 65 → 2; procedures/arrays/DUPLICATE present → 1; three coupled
  components (two coils + pump/piping on one loop) → 1; no calibration/off-design → 0;
  curated guesses + two solver pipelines tried, needs Try Harder-class
  numerics → 1. Score 7 → level 4; moved down to **level 3**: the structure is
  a textbook ε-NTU pair (the level-4 rating is driven by the size of the
  explicit cycle, a CoolSolve artefact).
- `CSL-0163` *cooling_coil_paramid*: the same one-zone wet-coil formulation
  used for parameter identification from a measured point (same model bank,
  card C-155).
