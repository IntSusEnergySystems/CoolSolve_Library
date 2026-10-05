# Piston compressor - parameter identification from two operating points

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0021`

A piston (reciprocating) air compressor whose four parameters — swept volume
`V_s`, clearance factor `C`, constant electromechanical losses `W_dot_loss_0`
and loss factor `alpha` — are identified from two measured operating points
(flow rate and power at two discharge pressures), then imposed at their
rounded values to predict the flow rate and power at two new operating
points (10 bar at 3000 rpm, 7 bar at 2500 rpm).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air (EES ideal-gas `Air` → CoolProp `Air`) |
| **Size** | 62 equations, all steady (largest block: 4) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 1, exercise 1 (EES file `MSTh-SB-R1-Ex1.EES`); CoolSolve example `piston_compressor` |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory, EES solution); Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A piston compressor is supplied with dry air at 1 bar and 15 °C and runs at
3000 rpm. Two operating points are measured: 0.10 kg/s and 32 kW at 7 bar
discharge, 0.11 kg/s and 20 kW at 3 bar discharge. Identify the compressor
characteristics (swept volume, clearance factor, loss parameters), then
evaluate the air flow rate and the power consumption (1) at 3000 rpm and
10 bar discharge, (2) at 2500 rpm and 7 bar discharge.

## Model

- **Volumetric efficiency** with clearance volume:
  `epsilon_v = 1 - C*(r_v - 1)` with `r_v = v_su/v_ex,s` the volume ratio of
  the isentropic internal compression; `V_dot_su = epsilon_v*V_dot_s`,
  `V_dot_s = N*V_s`, `V_dot_su = M_dot*v_su`.
- **Power**: `W_dot = W_dot_loss_0 + (1 + alpha)*W_dot_in` with
  `W_dot_in = M_dot*(h_ex_s - h_su)` the isentropic compression power.
- The four parameters are solved from the two measured points (square
  system: 2 flow equations + 2 power equations), then imposed at their
  rounded values (`alpha_cp`, `C_cp`, `V_s_cp`, `W_dot_loss_0_cp`) for the
  two predictions — hence the tag `parameter identification`, kind `steady`
  (taxonomy.md §2).

| Inputs | Value | Outputs (identified) | Value |
|---|---|---|---|
| `P_su` / `T_su` | 1 bar / 15 °C | `V_s` swept volume | 0.001927 m³ |
| `rpm` | 3000 rpm | `C` clearance factor | 0.04694 |
| point 1: `P_ex_1`, `M_dot_1`, `W_dot_1` | 7 bar, 0.10 kg/s, 32 kW | `W_dot_loss_0` constant losses | 5592 W |
| point 2: `P_ex_2`, `M_dot_2`, `W_dot_2` | 3 bar, 0.11 kg/s, 20 kW | `alpha` loss factor | 0.2271 |

## How to run

Open `piston_compressor_identification.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./piston_compressor_identification.eescode
```

The `.initials` file (guess values from the EES stored solution) is
required: without initial values most solver configurations fail (as noted
in the CoolSolve example).

## Results

| Point | Speed / discharge | ṁ [kg/s] | ε_v [-] | Ẇ_in [kW] | Ẇ [kW] |
|---|---|---:|---:|---:|---:|
| 1 (measured) | 3000 rpm / 7 bar | 0.1000 | 0.858 | 21.52 | 32.00 |
| 2 (measured) | 3000 rpm / 3 bar | 0.1100 | 0.944 | 11.74 | 20.00 |
| 3 (predicted) | 3000 rpm / 10 bar | 0.09371 | 0.804 | 25.23 | 36.59 |
| 4 (predicted) | 2500 rpm / 7 bar | 0.08342 | 0.859 | 17.95 | 27.64 |

At higher discharge pressure the volumetric efficiency drops (0.944 at
3 bar → 0.804 at 10 bar) through the clearance-volume term, and the power
rises accordingly.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot
      (flow rate and power vs discharge pressure), saved in figures/ -->

## Verification

Vs the EES stored solution of the original file (TM-0015,
`MSTh-SB-R1-Ex1.EES`, EES 7.458, full solution of all 62 variables):
34 of 62 variables agree within 0.1 %. The 28 remaining deviations are all
explained by the fluid model — EES ideal-gas `Air` vs CoolProp real `Air`:

| Quantity | EES | CoolSolve | rel. diff. | Explanation |
|---|---:|---:|---:|---|
| `h_su_1`, `h_ex_s_*` | 288 501 … 557 315 J/kg | +125 874 J/kg | 19–30 % | constant reference-state offset; energy *differences* agree: `w_s_1` 214 967 / 215 201 (0.11 %), `w_s_2` 106 696 / 106 739 (0.04 %) |
| `s_su` | 5 665 J/kg-K | 3 850 J/kg-K | 32 % | same reference-state offset (not used in any balance) |
| `v_ex_*`, `r_v_*` | e.g. `r_v_3` 5.216 | 5.193 | 0.14–0.44 % | real-gas compressibility in the isentropic exhaust state |
| `alpha` / `C` / `W_dot_loss_0` | 0.2295 / 0.04671 / 5570 | 0.2271 / 0.04694 / 5592 | 1.0 / 0.50 / 0.39 % | identification absorbs the EOS difference (same balances: 32 000 = 5 592 + 1.2271·21 520) |
| `M_dot_3` / `W_dot_3` / `M_dot_4` / `W_dot_4` | 0.09355 / 36 490 / 0.08333 / 27 595 | 0.09371 / 36 589 / 0.08342 / 27 641 | 0.10–0.27 % | predictions |
| `V_s` | 0.0019270 m³ | 0.0019266 m³ | 0.02 % | — |

All derived results (identified parameters ≤ 1.0 %, predictions ≤ 0.27 %)
agree within the tolerances for different equations of state
(CoolSolve `docs/ees_import.md` §11).

## Source and attribution

Exercise statement by **Vincent Lemort** (ULiège Thermodynamics
Laboratory), course *Machines et systèmes thermiques*, repetition 1,
exercise 1 (files `VL050919_1-1-*.EES`). EES solution by
**Stéphane Bertagnolio** (file `MSTh-SB-R1-Ex1.EES`); transcribed
equation-for-equation into the CoolSolve example by **S. Quoilin**
(comments translated to English — verified above by diff).

Source file (EES 7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 01/SB/MSTh-SB-R1-Ex1.EES`
(inventory candidate `TM-0015`). No EES original exists in CoolSolve
`misc/EES_ok.zip` for this example. The CoolSolve example
(`examples/piston_compressor.eescode`) is kept in the CoolSolve repository
as a test case.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already SI-°C-Pa-J, no conversion needed; the EES licence tag
  was removed; no lookup or parametric tables; no external functions.
  Equations taken over unchanged from the EES original (checked by diff
  against the CoolSolve example: identical apart from comments, header and
  the removed `$UnitSystem` line). Comments translated to English, standard
  header added, input/parameter meanings and SI units added to the trailing
  comments. Solved with the default pipeline (17 iterations) from
  `.initials` curated from the EES stored solution; verified (see above).
- **2026-10-05 — differences vs the VL original** (TM-0007/TM-0008,
  documented, model follows the SB solution): the VL statement files split
  the exercise (identification only, then imposed parameters with a
  `T_m` loss-torque form `W_dot_loss = 2·π·N·T_m` and a parametric table
  over the discharge pressure); at 3000 rpm both loss forms give the same
  5570 W (`T_m` = 17.73 N·m). Impact: none on the default run.

## Limitations and CoolSolve gaps

- The constant-loss form `W_dot_loss_0` is speed-independent; the VL
  torque form (`2·π·N·T_m`) is equivalent at fixed speed but scales with
  speed — the point-4 prediction at 2500 rpm keeps the 3000 rpm loss
  value, as in the original.
- No CoolSolve gap blocks this model. The absolute enthalpies/entropies of
  `Air` carry the CoolProp reference state, offset from EES ideal-gas air
  by a constant (see *Verification*); only differences and derived results
  are comparable.
- Ideal-gas model (dry air): no thermodynamic diagram is available in
  CoolSolve yet (`CS-FEAT-DIAGRAM-IDEAL`); the figure is a parametric sweep
  plot (roadmap decision D7).

## Related models

- `CSL-0020` (dry air screw compressor with internal leakage): same course
  and exercise family (repetition 2), parameter identification then
  prediction at another operating point, with internal leakage added.
- `CSL-0022` (refrigeration compressor identification): same
  identification method on R22 (repetition 1, exercise 2).
- CoolSolve example `piston_compressor.eescode` (CSX-034): same model,
  kept in CoolSolve as a test case.
