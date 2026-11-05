# Air-to-air glycol run-around heat-recovery loop

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0162`

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
| **Size** | 146 equations / 146 unknowns (winter branch of the `$IF`, square; largest block 61) |
| **Source** | ULiège model bank — air-to-air glycol recovery loop, 10 January 2008 (`GLYCOL_RECOVERY_LOOP_SB080110.EES`) |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — verified: the native file includes `BRINEPROP` and its lookup tables from `CSL-0079` (`$INCLUDE brineprop_secondary_refrigerants`) and reproduces the EES stored solution from its `.initials` |

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

```bash
coolsolve ./glycol_runaround_recovery_loop.eescode
```

The native file `glycol_runaround_recovery_loop.eescode` is kept in native EES
syntax, plus the line `$INCLUDE brineprop_secondary_refrigerants` that brings
in the `BRINEPROP` procedure of `CSL-0079` with its lookup tables
(`BrineSolutions`, `BrineCoefficients`). It needs its `.initials` (the EES stored solution, 144
values): from the default guesses the 61-variable block of the glycol
properties and the two coils fails with *SingularJacobian* (the structure of
`CS-BUG-NEWTON-CYCLE`); with it the model solves in 9 iterations (146
equations, largest block 61).

## Results

Values of the EES stored run (winter regime): extracted air 23 °C / 50 % RH →
11.04 °C / 88.3 % RH; fresh air −12 °C / 90 % RH → 3.91 °C / 24.2 % RH;
recovered power 62 359 W (sensible 47 001 W, latent 15 358 W), condensate
21.15 kg/h, glycol −2.57 °C → 15.27 °C, pump 173.4 W (Colebrook λ = 0.0340,
Δp = 78 031 Pa), ε_recovery = 0.4534.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric plot
     (e.g. recovered power or epsilon_recovery vs glycol flow rate), figures/… -->

## Verification

**Native file** (2026-11-04, `tools/compare_solution.py` against the stored
solution of `GLYCOL_RECOVERY_LOOP_SB080110.EES`):

```
143 common variables, 29 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 4
```

The 29 deviations are all humid-air quantities, from the EES vs CoolProp
humid-air formulations: the humidity ratios (4.2·10⁻³ to 5.3·10⁻³, maximum
5.31e-03 on `W_cooling_c_wet`; already 4.4·10⁻³ on `w_ge_a_su` at the imposed
23 °C / 50 %), the enthalpies and the fictitious-air properties of the wet
extraction coil (2.0·10⁻³ to 3.8·10⁻³) and the condensate and latent power
(1.1·10⁻³ to 1.3·10⁻³). The glycol properties agree within 1.9·10⁻⁵ (BrineProp
of `CSL-0079`), the pump power to 1.7·10⁻⁷, `epsilon_recovery` to 3.0·10⁻⁵,
the recovered sensible power to 3.7·10⁻⁴ and the air outlet temperatures
within 4·10⁻⁴. `epsilon` is a stale variable of the source (no equation); the
four CoolSolve-only variables are `PI` and three expression outputs of the
`CALL BRINEPROP` statements.

Before the native file ran, a runnable variant was checked pointwise (the
equations satisfied at the EES stored point, see the conversion log of
2026-10-08); it was removed on 2026-11-05.

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
- `CSL-0079` *brineprop_secondary_refrigerants*: the BrineProp library model
  whose `BRINEPROP` procedure and tables the native file includes.
- `CSL-0161` *plate_hx_thermal_resistances*: imported in the same wave, also a
  user of the BrineProp library (`BRINEPROP2`).
- `CSL-0163` *cooling_coil_paramid*: the same one-zone wet-coil formulation
  used for parameter identification from a measured point (same model bank,
  card C-155).

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
- **Gaps blocking the native file**: `CS-GAP-INCLUDE` (BrineProp comes from the implicit
  `USERLIB` of EES, `Brineprop.lib`, TM-0479); closed 2026-11-04, see below.

- **2026-10-08 — runnable variant** `glycol_runaround_recovery_loop_coolsolve.eescode`,
  changing only what the gaps force, each change valid EES unless noted:
  1. the `$IF` branches are resolved for the stored run (winter): the winter
     block is kept unconditional, the summer block is removed
     (no longer needed), as in CSL-0009/CSL-0012/CSL-0161;
  2. the four 5-argument `IF(A,B,X,Y,Z)` regime selections are written with
     the 3-argument `if(cond, a, b)`, `cond = Q_dot_cooling_wet −
     Q_dot_cooling_dry` (**CoolSolve-only syntax**, not valid EES; CoolSolve accepts the
     five-argument form now). EES selects the wet value also at equality (`A = B`), CoolSolve the
     dry one there — a measure-zero case, not met in the stored run; the
     condensate `IF` (whose equality branch is 0) is strictly equivalent;
  3. the three `CALL BRINEPROP` calls are **flattened into the main program**
     (`CS-GAP-INCLUDE`), one block per property, in the
     manner of the `CSL-0079` variant: the concentration selector of the
     original (22 range checks and an 11-branch ladder, procedure-only
     statements) reduces here to `Fl_brine_gw = 1` ('EG' 25 % within its range
     0–56.1 %); the property indicator `Pr` = 3 / 2 / 5 (SPECHEAT / DENSITY /
     DYNVISC) selects the coefficient column read from the companion tables;
     the internal variables are renamed per call with the suffix `_gw`
     (`Row_cp_gw[k]`, `Funkt_cp_gw`, …); the DUPLICATE loop of the original
     procedure is kept as a `DUPLICATE` (allowed in the main program);
  4. the **expression outputs** of the calls are applied as separate equations
     `c_p_gw = Funkt_cp_gw/1000`,
     `rho_gw = Funkt_rho_gw`, `mu_gw = exp(Funkt_mu_gw)/1000` — the values
     match the stored ones (see *Verification*).
  The variant inherits the `.initials` of the stored solution plus guesses for
  its new internal variables; it is **not solved yet**
  (`CS-BUG-NEWTON-CYCLE`).
- **2026-10-08 — inventory**: TM-0321 (the representative of DG-0076) set to
  `added` → `CSL-0162`. TM-0320 (Jaccard 0.92) and TM-0476 (Jaccard 0.99,
  inside a zip) kept at the C-137 decision (`todo`): near-duplicates that
  could be `duplicate` after an equation diff, left to the manager.
- **2026-11-04 — native file runs**: CoolSolve now has `$INCLUDE`
  (`CS-FEAT-IMPORT`, `CS-GAP-INCLUDE` closed), and an included library model
  brings its lookup tables; the line
  `$INCLUDE brineprop_secondary_refrigerants` is added at the top of the native
  file (the only change to the EES source), which then reads `BRINEPROP` and
  its tables `Units`, `Brine1`, `Brine2` from `CSL-0079` (no table is copied
  into this folder). The native file gets a `.initials`: the 144 values of the
  EES stored solution, as extracted by `tools/ees_extract.py` (the variant's
  `.initials` holds the same values plus guesses for its flattened BrineProp
  variables). From the default guesses its 61-variable block fails
  (*SingularJacobian*). It then solves in 9 iterations and agrees with the EES
  stored solution (see *Verification*); `.sol` baseline of the native file
  added, status `blocked` → `verified`. The variant, re-run with the same
  binary, now converges (111 iterations) but to a nonphysical root
  (`t_gp_a_ex` = −11.9 °C instead of 3.9 °C, negative condensate; 78 of 143
  variables differ from EES), so it still has no `.sol`.
- **2026-11-05 — runnable variant removed**: the native file is verified and
  nothing forces a rewrite any more, so
  `glycol_runaround_recovery_loop_coolsolve.eescode` (which never reached the
  stored solution and had no `.sol`), its `.initials` and its two companion
  tables are deleted. The header of the native file loses a line, so the
  `.sol` is regenerated: the auxiliary variables of the `CALL` outputs are
  named after their line (`__out1_BRINEPROP_L…`); every other variable is
  unchanged.
- **Level justification** (taxonomy.md §3): equations 271 (variant) → 2;
  largest block 65 → 2; procedures/arrays/DUPLICATE present → 1; three coupled
  components (two coils + pump/piping on one loop) → 1; no calibration/off-design → 0;
  curated guesses + two solver pipelines tried, needs Try Harder-class
   numerics → 1. Score 7 → level 4; moved down to **level 3**: the structure is
   a textbook ε-NTU pair (the level-4 rating is driven by the size of the
   explicit cycle, a CoolSolve artefact).

## Limitations and CoolSolve gaps

- The native file solves only from its `.initials` (the EES stored
  solution); from the default guesses its 61-variable block fails with
  *SingularJacobian*, the symptom of the solver bug `CS-BUG-NEWTON-CYCLE`.
- The two coils are supposed to have the same characteristics (nominal
  resistances corrected with mass-flow exponents 0.6 / 0.8, zero metal
  resistance), as in the original.

## Related models
