# Centrifugal brine pump reference simulation model (RefSim)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** (runnable variant verified) &nbsp;|&nbsp; `CSL-0072`

Reference simulation (RefSim) model of a single-stage centrifugal pump
conveying a brine (water/antifreeze mixture). The pump is described by
dimensionless characteristics: cubic polynomials in the flow factor
$\phi = \dot V/(A\,U)$ give the pressure factor $\psi$ and the power factor
$\Lambda$; the isentropic (hydraulic) efficiency follows as
$\epsilon_s = \phi\,\psi/\Lambda$. The brine density and specific heat come
from the BrineProp library procedure `BRINEPROP` (18-coefficient polynomials
in temperature and antifreeze concentration, coefficient tables `Brine1` /
`Brine2`), so the temperature rise across the pump follows from the shaft
power. This model comes from the ULiège model bank (Laborelec toolkit
lineage); a sibling parameter-identification (ParamID) model of the same
pump exists in the collection (inventory `TM-0486`, a separate, more
detailed model).

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | brine EG (ethylene glycol/water), any BrineProp fluid |
| **Size** | native: 33 main-program equations + the `BRINEPROP` procedure (≈ 45 statements); variant: 119 equations after analysis, largest block 1 |
| **Source** | ULiège model bank *Model data bank*, Distribution_Systems/Pumps, 2008-02-18 |
| **Authors** | Vincent Lemort (file header; inventory adds V. Teodorese, J. Lebrun) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked**; variant `*_coolsolve.eescode` verified against the EES stored solution (see *Verification*) |

## Problem statement

A centrifugal pump (impeller diameter 0.1333 m) runs at 1300 rpm and delivers
1 m³/h of an ethylene-glycol/water brine (25 % antifreeze) at 100 000 Pa and
25 °C. Determine the operating point on the dimensionless characteristics:
pressure rise, shaft power, isentropic efficiency, mass flow rate and the
brine temperature at the pump exhaust.

## Model

With $U = \pi D N$ the peripheral speed and
$P_{dyn,periph} = U^2/(2v)$ the peripheral dynamic pressure:

- pressure factor: $\psi = \alpha_0 + \alpha_1\phi + \alpha_2\phi^2 + \alpha_3\phi^3$,
  $\Delta p_{pump} = \psi\,P_{dyn,periph}$;
- power factor: $\Lambda = \beta_0 + \beta_1\phi + \beta_2\phi^2 + \beta_3\phi^3$;
- isentropic power $\dot W_s = \dot V\,\Delta p_{pump}$,
  $\dot W_{shaft} = \dot W_s/\epsilon_s$ with
  $\epsilon_s = \phi\psi/\Lambda$;
- exhaust state: $p_{ex} = p_{su} + \Delta p_{pump}$ and
  $c_p\,(t_{ex} - t_{su}) = \dot W_{shaft}/\dot m$ with
  $\dot m = \dot V/v$.

| Inputs | Value | Outputs | Value |
|---|---:|---|---:|
| `rpm_pump` rotational speed | 1300 1/min | `DELTAP_pump` pressure rise | 49 766 Pa |
| `V_dot_pump_m3h` volume flow | 1 m³/h | `W_dot_shaft_pump` shaft power | 89.64 W |
| `P_su_pump` supply pressure | 100 000 Pa | `epsilon_s_pump` isentropic efficiency | 0.1542 |
| `T_su_pump` supply temperature | 25 °C | `M_dot_pump` mass flow | 0.2861 kg/s |
| `X_brine` antifreeze | 25 % | `p_ex_pump` exhaust pressure | 149 766 Pa |
| `brine$` brine | 'EG' | `t_ex_pump` exhaust temperature | 25.081 °C |

`D_pump` and the 8 polynomial coefficients (`alpha_0..3_pump`,
`beta_0..3_pump`) are parameters of the original's panel; their values come
from the EES stored solution (0.1333 m; 1.18, −1.466, −614, −6002; 0.01585,
0.2436, 69.42, −2098).

## How to run

The native file `centrifugal_brine_pump_refsim.eescode` is kept in valid EES
and is **blocked** in CoolSolve (gaps below). Solve the runnable variant:

```bash
coolsolve ./centrifugal_brine_pump_refsim_coolsolve.eescode
```

The brine is changed by editing `brine$` (`'EG'`, `'PG'`, `'CaCl2'`, …) and
`X_brine` within the validity range of the BrineProp library.

## Results

Default run (see table above): the pump raises the pressure by 0.498 bar
(49 766 Pa), absorbs 89.6 W of shaft power at an isentropic efficiency of
15.4 % and the brine leaves 0.081 K warmer — the low flow factor
$\phi$ = 0.0022 (1 m³/h against a 0.133 m impeller at 1300 rpm) sits on the
far left of the characteristics, hence the low efficiency.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): pump characteristics
     psi(phi) and epsilon_s(phi) with the operating point, or a Parametric sweep of
     V_dot_pump_m3h; figures/centrifugal_brine_pump_refsim_*.png -->

## Verification

The variant `centrifugal_brine_pump_refsim_coolsolve.eescode` was compared
with the solution stored in the original EES file (`compare_solution.py`):
**32 common variables, 0 differ (rtol=0.001); only in EES: 2; only in
CoolSolve: 88** — the maximum relative deviation on the physical results is
6.4·10⁻⁸ (`DELTAP_pump`, `W_dot_shaft_pump`; `rho_pump` 2.9·10⁻⁹,
`c_p_pump` 6.2·10⁻⁹, `t_ex_pump` 4.2·10⁻¹⁰), from the rounding of the
80-bit table coefficients to 64-bit floats. The two EES-only variables are
leftovers of the original variable-information table — dead variables of an
earlier version of the equations (`b` = −0.236, `v` = 1), absent from the
extracted equations; the 88 CoolSolve-only variables are
the internal names of the flattened property evaluation (see conversion
log). The lookup tables were decoded by hand from the binary `.lkt` files
and validated: the decoded `Brine1`/`Brine2` coefficients reproduce the
stored `rho_pump` = 1030.000008 kg/m³ and `c_p_pump` = 3852.099981 J/kg-K
to ≤ 6·10⁻⁹ relative.

The native file cannot be solved by CoolSolve: it fails at parse time on the
`ELSE IF … ENDIF;ENDIF` ladders of `BRINEPROP` (`CS-GAP-ELSEIF-CHAIN`).

## Source and attribution

ULiège model bank *Model data bank* (Laborelec toolkit lineage), sub-folder
*Model data bank*: `Centrifugal_Brine_Pump_Refsim_Model_VTJLVL080219.zip` /
`Centrifugal_Brine_Pump_RefSim_EES_Model_VTJLVL080219.EES` (EES 7.888, file
tag VTJLVL = V. Teodorese, J. Lebrun; file header: "Authors: Vincent
Lemort"), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/Distribution_Systems/Pumps/Centrifugal_Brine_Pump_Refsim_Model_VTJLVL080219.zip`
(inventory candidate `TM-0487`). The zip also carries the compiled `.EXE`
version of the model and the BrineProp user library. The lab disclaimer of
the original applies ("freely distributed, may not be sold; cite the origin
of this model").

The `BRINEPROP` procedure and the `Brine1`/`Brine2` coefficient tables come
from the BrineProp library shipped in the same collection
(`Brineprop.lib`, inventory `TM-0479`, EES 4.631 binary lookup tables
`Brine1.lkt`/`Brine2.lkt`), which EES loads implicitly from the USERLIB
folder.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already SI-C-Pa-J, no tables, no warnings; the EES licence tag
  was removed. The extraction contains only the equations: the inputs and
  the 9 pump parameters were completed from the stored EES solution (values
  in the *Model* table above); `brine$` is a string variable, which the
  extractor does not export — identified as `'EG'` from the stored solution
  (only ethylene glycol at 25 % / 25 °C gives the stored
  $\rho$ = 1030.000008 kg/m³ and $c_p$ = 3852.099981 J/kg-K; checked
  against all 11 BrineProp fluids).
- **X_brine default**: the original equations read `X_brine=50`, but the
  stored reference run (diagram-window input) used **25 %**; the library
  file keeps the stored value as the default run and says so in a comment.
- **BrineProp library**: `BRINEPROP` copied from `Brineprop.lib` (TM-0479)
  into the native file, unchanged except the removal of the dead code after
  `END` (an `x=1` statement and a commented-out example block) and of the
  `$tabStops` display directive — standard workaround of `CS-GAP-INCLUDE` /
  `CS-FEAT-IMPORT`. The binary lookup tables `Brine1.lkt` (198 rows × 5
  columns) and `Brine2.lkt` (11 × 2) were **decoded by hand** (EES 4.631
  `.lkt` layout reverse-engineered from the hex dump, cf. `ees_import.md`
  §13: per column, a 31-byte name field, 10-byte Extended values, display
  bytes) and shipped as companion CSVs (`-Brine1.csv`, `-Brine2.csv`;
  EES column names `Column1..5` kept); validated against the stored
  solution as described under *Verification* (`CS-GAP-LKT` worked around).
- **Comments**: the original comments are already in English; the section
  title "Water state at pump exhaust" is rendered as "Brine state at pump
  exhaust (section titled water in the original)" since the fluid handled
  is the brine of `brine$`. Units added to the comments (`[-]` only for the
  dimensionless factors); `N_pump` is given in 1/s (the EES variable-info
  unit "min^-1" contradicts `rpm_pump/60`).
- **Level**: score 3 per taxonomy §3 (119 equations after the CoolSolve
  analysis of the variant, but largest block 1; procedure present; empirical
  characteristic curves; no curated guesses) — one point above the ≤ 1 band
  only because of the equation count, which comes from the flattened
  property polynomial, not from model depth. Moved down to **1** as
  pre-assigned by the roadmap card: a small, fully explicit single-
  component model.
- **2026-10-05 — runnable variant** `centrifugal_brine_pump_refsim_coolsolve.eescode`
  (valid EES; no CoolSolve-only syntax). Changes forced by the gaps, logged
  in the variant header:
  1. `CS-GAP-ELSEIF-CHAIN` + `CS-GAP-UPPERCASE` + `CS-GAP-STRING-ARRAY` +
     `CS-GAP-LOOKUP-PROC` break `BRINEPROP`. It is split into (a) a selector
     procedure `BRINEPROP_SELECT(Conc,Fl$:Fl_brine)` holding the 22
     concentration range checks and the 11-branch fluid ladder, rewritten as
     sequential single-line IF statements (mutually exclusive conditions;
     property selection by tag, see below); and (b) the property evaluation
     flattened into the main program for the two used properties (`_d`:
     Density = 2, `_cp`: SpecHeat = 3), keeping the polynomial, the table
     reads (`Row[k]=k+(Fl-1)*18` as a `DUPLICATE` loop — `REPEAT` is not
     allowed in a main program) and the output scaling exactly as in the
     original; internal variables renamed per call (`<variable>_d`,
     `<variable>_cp`). The formal arguments `Conc`/`Fl$` are replaced by the
     actual `X_brine`/`brine$` (`Conc` → `x_d = X_brine - xm_d`).
  2. `CS-GAP-CALL-EXPR-OUT`: the expression output `:c_p_pump/1000` becomes
     an output into `c_p_pump_kJ` plus `c_p_pump = c_p_pump_kJ*1000`.
  Verified against the same EES reference (see *Verification*).

## Limitations and CoolSolve gaps

The native file is **blocked**; `missing_features` lists every gap that
blocks it:

- `CS-GAP-ELSEIF-CHAIN` — the `ELSE IF … ENDIF;ENDIF` ladders of
  `BRINEPROP` do not parse ("IF ... THEN without a matching ENDIF");
- `CS-GAP-UPPERCASE` — the intrinsic `Uppercase$` is unknown;
- `CS-GAP-CALL-EXPR-OUT` — an expression as `CALL` output argument
  (`…:c_p_pump/1000`) is rejected;
- `CS-GAP-STRING-ARRAY` — reading a string-array element (`UO$=U$[Pro]`)
  fails ("String variable not found");
- `CS-GAP-LOOKUP-PROC` — `LOOKUP` inside a procedure fails ("no table store
  is available in this context"); the main program reads the same companion
  tables fine.

`CS-GAP-INCLUDE` (implicit USERLIB library) is worked around by copying
`BRINEPROP` into the file; `CS-GAP-LKT` (binary `.lkt` tables) is worked
around by the hand-decoded companion CSVs.

Limitations of the variant: `REPEAT`/`IF` statements are procedure-only in
EES, hence the `DUPLICATE` loop and the selector procedure of the conversion
log; the model has no figure yet (maintainer, workflow §7).

## Related models

- `CSL-0079` *brineprop_secondary_refrigerants*: the BrineProp library this
  model copies its `BRINEPROP` procedure and its two coefficient tables from,
  as a function model of its own (same tables, same polynomial, verified
  against an independent EES stored solution).
- `CSL-0078` *brine_to_water_heat_pump_refsim* — another model of the bank
  that calls the same BrineProp library (density and specific heat of a 25 %
  propylene glycol solution), with the same blocked-native-file treatment.
- `TM-0486` (inventory): sibling **ParamID** model of the same pump in the
  source collection (parameter identification from measurements, level 2) —
  a separate model if imported; not in the library yet.

No library model of this component existed yet (the folder
`components/pumps_fans/` was empty).
