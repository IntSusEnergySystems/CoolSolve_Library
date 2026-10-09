# Refrigeration compressor - parameter identification from two operating points

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0022`

A R22 reciprocating refrigeration compressor in a simple vapour-compression
cycle (3 K subcooling, 5 K superheat) whose four parameters — swept volume
flow rate `V_dot_s`, clearance factor `C`, constant electromechanical
losses `W_dot_loss_0` and loss factor `alpha` — are identified from two
measured operating points (cooling capacity and power at two
condensing/evaporating temperature pairs), then imposed at their rounded
values to predict the cooling capacity and power at a third operating
point (40 °C condensing, 2 °C evaporating).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R22 |
| **Size** | 102 equations, all steady (largest block: 4) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 1, exercise 2 (EES file `MSTh-SB-R1-Ex2.EES`); CoolSolve example `refrigeration_compressor` |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory, EES solution); Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A piston-compressor manufacturer announces the following performances
(refrigerant R22, 3 K subcooling at the condenser outlet, 5 K superheat at
the evaporator outlet): 64 kW cooling and 16 kW power at 34 °C condensing /
−6 °C evaporating; 70 kW cooling and 20 kW power at 46 °C condensing /
0 °C evaporating. Determine the compressor characteristics (swept volume,
clearance factor, loss parameters), then the cooling capacity and power at
40 °C condensing / 2 °C evaporating, at constant running speed, subcooling
and superheat.

## Model

- **Cycle**: evaporator (`Q_dot_ev = M_dot*(h_1 - h_4)`), isentropic
  compression reference (`W_dot_s = M_dot*(h_2_s - h_1)`),
  condenser with subcooling (`T_3 = T_cd - DELTAT_sc`), isenthalpic
  expansion (`h_4 = h_3`), suction superheat (`T_1 = T_ev + DELTAT_oh`).
- **Volumetric efficiency** with clearance volume:
  `epsilon_v = 1 - C*(r_v - 1)` with `r_v = v_1/v_2_s` the volume ratio of
  the isentropic internal compression; `V_dot_su = M_dot*v_1`,
  `epsilon_v = V_dot_su/V_dot_s`.
- **Power**: `W_dot = W_dot_loss_0 + (1 + alpha)*W_dot_s`.
- The four parameters are solved from the two measured points (square
  system: 2 flow equations + 2 power equations), then imposed at their
  rounded values (`alpha_cp`, `C_cp`, `V_dot_s_cp`, `W_dot_loss_0_cp`) for
  the regime-3 prediction — hence the tag `parameter identification`, kind
  `steady` (taxonomy.md §2).

| Inputs | Value | Outputs (identified) | Value |
|---|---|---|---|
| `DELTAT_sc` / `DELTAT_oh` | 3 K / 5 K | `V_dot_s` swept volume flow rate | 0.02511 m³/s |
| point 1: `T_cd_1`, `T_ev_1` | 34 °C / −6 °C | `C` clearance factor | 0.06070 |
| point 1: `Q_dot_ev_1`, `W_dot_1` | 64 kW, 16 kW | `W_dot_loss_0` constant losses | 2231 W |
| point 2: `T_cd_2`, `T_ev_2` | 46 °C / 0 °C | `alpha` loss factor | 0.2054 |
| point 2: `Q_dot_ev_2`, `W_dot_2` | 70 kW, 20 kW | | |
| prediction: `T_cd_3`, `T_ev_3` | 40 °C / 2 °C | `Q_dot_ev_3` / `W_dot_3` | 81.75 kW / 18.50 kW |

## How to run

Open `refrigeration_compressor_identification.eescode` in the CoolSolve GUI
and press *Solve*, or from a terminal:

```bash
coolsolve ./refrigeration_compressor_identification.eescode
```

The `.initials` file (guess values from the EES stored solution) is
required: without initial values most solver configurations fail (as noted
in the CoolSolve example).

## Results

| Point | Condensing / evaporating | ṁ [kg/s] | ε_v [-] | Q̇_ev [kW] | Ẇ [kW] |
|---|---|---:|---:|---:|---:|
| 1 (measured) | 34 °C / −6 °C | 0.3800 | 0.887 | 64.00 | 16.00 |
| 2 (measured) | 46 °C / 0 °C | 0.4513 | 0.869 | 70.00 | 20.00 |
| 3 (predicted) | 40 °C / 2 °C | 0.4990 | 0.903 | 81.75 | 18.50 |

The identified clearance factor (0.061) and volumetric efficiencies
(0.87–0.90) are typical of a reciprocating refrigeration compressor.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of
      regimes 1 and 3 (arrays h[1..8]/P[1..8], T[1..8]/s[1..8] for the T-s
      diagram), saved in figures/ -->

## Verification

Vs the EES stored solution of the original file (TM-0016,
`MSTh-SB-R1-Ex2.EES`, EES 7.458, full solution of all 86 stored variables):
77 of 86 variables agree within 0.1 %. The 9 remaining deviations all trace
to the R22 property formulation (EES 7.4 vs CoolProp — the same deviation
as the R22 cycle `CSL-0001`, documented at 1.4 %):

| Quantity | EES | CoolSolve | rel. diff. | Explanation |
|---|---:|---:|---:|---|
| `C` / `alpha` / `W_dot_loss_0` | 0.06018 / 0.2040 / 2238 | 0.06070 / 0.2054 / 2231 | 0.85 / 0.71 / 0.32 % | identification absorbs the EOS difference (same balances: 16 000 = 2 231 + 1.2054·11 423) |
| `M_dot_1` / `M_dot_2` | 0.3804 / 0.4519 kg/s | 0.3800 / 0.4513 kg/s | 0.11 / 0.12 % | via `v_1` (suction vapour) |
| `v_2_1` / `v_2_2` / `v_2_3` | e.g. 0.02048 m³/kg | +0.11 % | 0.11 % | isentropic exhaust specific volume (real-gas compressibility) |
| `epsilon_v_2` | 0.8704 | 0.8695 | 0.11 % | follows `v_2_2` |
| `P_ev` / `P_cd` (all regimes) | e.g. 407 803 / 1 321 444 Pa | −0.03 % | ≤ 0.04 % | saturation pressures |
| `h_1` / `h_2_s` / `h_3` | e.g. 406 289 / 436 341 / 238 028 J/kg | ≤ 0.06 % | ≤ 0.06 % | — |
| `V_dot_s` | 0.025100 m³/s | 0.025106 m³/s | 0.02 % | — |
| `M_dot_3` / `Q_dot_ev_3` / `W_dot_3` | 0.4991 / 81 680 / 18 495 | 0.4990 / 81 747 / 18 496 | 0.02–0.08 % | predictions |

All derived results (identified parameters ≤ 0.85 %, predictions ≤ 0.08 %)
agree within the tolerances for different equations of state
(CoolSolve `docs/ees_import.md` §11).

## Source and attribution

Exercise statement by **Vincent Lemort** (ULiège Thermodynamics
Laboratory), course *Machines et systèmes thermiques*, repetition 1,
exercise 2 (files `VL050919_1-2-*.EES`). EES solution by
**Stéphane Bertagnolio** (file `MSTh-SB-R1-Ex2.EES`, including the
regime-3 prediction with imposed parameters); transcribed
equation-for-equation into the CoolSolve example by **S. Quoilin**
(see *Conversion log* for the differences).

Source file (EES 7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 01/SB/MSTh-SB-R1-Ex2.EES`
(inventory candidate `TM-0016`). No EES original exists in CoolSolve
`misc/EES_ok.zip` for this example. The CoolSolve example
(`examples/refrigeration_compressor.eescode`) is kept in the CoolSolve
repository as a test case.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already SI-°C-Pa-J, no conversion needed; the EES licence tag
  was removed; no lookup or parametric tables; no external functions.
  Equations taken over unchanged from the EES original TM-0016 (checked by
  diff: only comments, header and the removed `$UnitSystem` line differ).
  Comments translated to English, standard header added, input/parameter
  meanings and SI units added to the trailing comments. Solved with the
  default pipeline (13 iterations) from `.initials` curated from the EES
  stored solution; verified (see above).
- **2026-10-05 — diagram-ready state arrays** (workflow §3, step 5): the
  original already stores `h[1..4]/P[1..4]` (regime 1) and `h[5..8]/P[5..8]`
  (regime 3); added the matching `T[1..8]/s[1..8]` post-processing block
  (compressor exhaust via `TEMPERATURE(R22,h,P)`, condenser outlet via
  `ENTROPY(R22,T,P)`, evaporator inlet via `TEMPERATURE`/`ENTROPY(R22,h,P)`
  — the pattern of `CSL-0001`). Post-processing only: the 86 stored
  variables are unchanged (see *Verification*).
- **2026-10-05 — differences vs the CoolSolve example** (CSX-041, kept in
  CoolSolve; model follows the EES original TM-0016): the example was
  transcribed equation-for-equation from the SB variant TM-0017
  (`MSTh-SB-R1-Ex2_2.EES`, verified by diff: identical apart from comments,
  header, `//` hints and the dropped commented-out regime-3 block), which
  differs from TM-0016 in three ways: (1) `V_dot_su_2 = M_dot_1*v_1_2`
  uses the regime-1 flow rate — a typo (TM-0016, TM-0010 and TM-0011 all use
  `M_dot_2`); it corrupts the identification stored in that file
  (`C = 0.28`, `V_dot_s = 0.047 m³/s`, `epsilon_v ≈ 0.39–0.47` — the `//C =
  0.28` hint of the example — instead of `C = 0.060`, `V_dot_s = 0.0251
  m³/s`, `epsilon_v ≈ 0.87–0.90` confirmed by the VL originals and TM-0016);
  (2) the swept volume is parameterised per revolution (`V_dot_s = N*V_s`,
  3000 rpm) instead of directly as a volume flow rate; (3) the regime-3
  prediction block is commented out, so the example identifies but never
  predicts. Impact on the library model: none (TM-0016 imported as is).
  The maintainer may want to fix the example in CoolSolve (one character:
  `M_dot_1` → `M_dot_2` in `V_dot_su_2`).

## Limitations and CoolSolve gaps

- The identified `V_dot_s` is a volume flow rate at the (constant) running
  speed, not a swept volume per revolution: the model only applies at that
  speed (as in the original; the VL statement imposes constant speed for
  the prediction).
- No CoolSolve gap blocks this model. The R22 saturation pressures agree
  within 0.04 % but the superheated/is compressed volumes within 0.11 %
  (EES 7.4 vs CoolProp formulations, see *Verification*).
- CoolSolve prints spurious heuristic warnings on this model (fluid
  suggestion `Did you mean 'R22'?`, Fahrenheit suspicion on saturation
  temperatures such as `T = 34`): they do not affect the solution.

## Related models

- `CSL-0021` (piston compressor identification on dry air): same
  identification method (four parameters from two points, then prediction
  at new points), same course repetition 1 (exercise 1), ideal-gas fluid.
- `CSL-0001` (refrigeration cycle with a simple compressor model): same SB
  solution series (repetition 1, exercise 3) on R22, with the same EES
  vs CoolProp deviation.
- CoolSolve example `refrigeration_compressor.eescode` (CSX-041): same
  model, kept in CoolSolve as a test case (transcribed from the TM-0017
  variant with the `M_dot_1` typo — see *Conversion log*).
- `CSL-0167` *reciprocating_polynomial_r22*: the JL reference piston
  compressor of the same laboratory series (semi-empirical six-step model
  with clearance re-expansion and motor slip).
