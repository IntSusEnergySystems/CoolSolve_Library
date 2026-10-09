# Dry air screw compressor with internal leakage

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0020`

A dry (oil-free, no clearance volume) screw compressor for air, suction
1 bar / 15 °C, discharge 3 bar. At the 7000 rpm nominal point the measured
volumetric and isentropic efficiencies (90 % and 70 %) identify three model
parameters — the swept volume `V_s`, the mechanical-loss torque `T_m` and the
equivalent leakage-throat area `A_thr` — which are imposed here; the model
predicts the performance at another speed (2000 rpm default run): the leakage
flow through the equivalent throat (choked isentropic nozzle) is mixed back
into the suction flow, the internal compression is assumed isentropic, and the
shaft power adds the mechanical losses, assumed dissipated to the surroundings
(adiabatic compressor).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air (`air_ha`, EES real-gas dry air → CoolProp `Air`) |
| **Size** | 40 equations, all steady (largest block: 13) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 2, exercise 1 (second part); CoolSolve example `air_screw_compressor` |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — verified against the EES stored solutions (see *Verification*) |

## Problem statement

A dry screw compressor is designed for dry air at 1 bar / 15 °C suction and
3 bar discharge. Run at 7000 rpm, its overall volumetric and isentropic
efficiencies are 90 % and 70 %. The compressor model parameters (`V_s`,
`T_m`, `A_thr`) being imposed from that nominal test, what is the performance
of the same compressor at 2000 rpm? Suction and discharge pressure drops are
neglected; the internal leakage is accounted for.

## Model

- **Leakage loop**: the theoretical flow `M_dot_th = V_dot_s/v_su` splits into
  the delivered flow `M_dot` and the leakage `M_dot_leak`
  (`epsilon_v = M_dot/M_dot_th`); the leakage, expanded isentropically through
  the equivalent throat of area `A_thr`, mixes back with the suction flow
  (`M_dot_leak·h_ex + M_dot·h_su = M_dot_in·h_su1`), which raises the suction
  specific volume `v_su1` seen by the rotors
  (`M_dot_in = V_dot_s/v_su1`).
- **Nozzle**: the throat pressure is the critical pressure
  `P_thr = (2/(γ+1))^(γ/(γ−1))·P_ex` (γ = 1.4 fixed); the discharge pressure
  is above it, so the nozzle is choked. Throat velocity from the isenthalpic
  relation `h_ex = h_thr + C_thr²/2`, cross-checked by the perfect-gas sound
  speed `C_thr_bis = √(γ·r·T_thr)` (both agree within 0.01 %).
- **Power**: `W_dot_in = M_dot_in·(h_ex1_s − h_su1)` (isentropic internal
  compression), `W_dot_loss = 2·π·N·T_m`,
  `epsilon_s = M_dot·(h_ex_s − h_su)/W_dot`; the exhaust state is the
  isentropic one (`h_ex = h_ex1_s`, i.e. no reheating by the mechanical
  losses).

| Inputs | Value | Outputs (2000 rpm) | Value |
|---|---|---|---|
| `V_s` swept volume | 0.007876 m³ | `M_dot` delivered flow | 0.1998 kg/s |
| `A_thr` leakage throat area | 1.309e-4 m² | `M_dot_leak` leakage (27 % of inlet) | 0.07425 kg/s |
| `T_m` loss torque | 46.25 N-m | `epsilon_v` / `epsilon_s` | 0.629 / 0.490 |
| `P_su` / `T_su` | 1 bar / 15 °C | `W_dot` shaft power | 43.55 kW |
| `P_ex` | 3 bar | … internal / losses | 33.87 / 9.69 kW |
| `N` | 2000 rpm | `P_thr` / `C_thr` | 1.585 bar / 391 m/s |

## How to run

Open `dry_air_screw_compressor_leakage.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./dry_air_screw_compressor_leakage.eescode
```

The `.initials` file (guesses from the EES stored solution) is required:
the Newton solver alone fails on the leakage loop and the default pipeline
falls back to TrustRegion. Set `N = rpm/60` with `rpm` as in the `simple`
variant to sweep the speed (see *Related models*).

## Results

At 2000 rpm the leakage (`M_dot_leak/M_dot_in` = 27 %) depresses the
volumetric efficiency to 0.629 (from 0.90 at 7000 rpm, where the leakage is
relatively smaller) and the overall isentropic efficiency to 0.490 (from
0.70). The internal consistency check `C_thr` vs `C_thr_bis` agrees within
0.01 %, and `s_ex = s_su1` confirms the isentropic internal compression.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot
      (shaft power and efficiencies vs speed), saved in figures/ -->

## Verification

1. **Vs the EES original** (`thermo_models` TM-0039,
   `VL050926_2-1-2 questionsVL051023.EES`, EES 7.403 — the French file the
   CoolSolve example transcribes equation-for-equation): 16 of its 19 stored
   variables agree (inputs, `N`, `V_dot_s`, `v_su`, `gamma`, `r`,
   `MM_air`…); the 3 absolute enthalpies/entropies differ by a constant
   reference-state offset (EES `air_ha` vs CoolProp `Air`: +125.97 kJ/kg on
   `h`), while the energy differences agree (`h_ex_s − h_su`: 106 736 vs
   106 761 J/kg, i.e. 0.02 %).
2. **Vs the SB variant** (TM-0032, `MSTh-SB-R2-Ex1-2.EES`, EES 7.458, full
   stored solution at the same 2000 rpm point; `Air` fluid, parameters within
   0.15 %, γ solved as 1.395 instead of fixed 1.4): all 16 comparable derived
   results within 0.15 % — `M_dot` 0.08 %, `epsilon_v` 0.05 %, `epsilon_s`
   0.07 %, `W_dot` 0.04 %, `W_dot_in` 0.03 %, `M_dot_leak` 0.14 %,
   `W_dot_s` 0.11 %, `V_dot_leak` 0.03 %.

## Source and attribution

Classroom exercise by **Vincent Lemort** (ULiège Thermodynamics Laboratory),
course *Machines et systèmes thermiques*, repetition 2, exercise 1 (second
part: imposed model parameters, prediction at 2000 rpm). Transcribed into the
CoolSolve example by **S. Quoilin** (comments translated to English, equations
unchanged — verified above by diff).

Source files (EES 7.x, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 02/VL050926_2-1-2 questionsVL051023.EES`
(inventory candidate `TM-0039`, representative of the 8-file duplicate group
`DG-0007`) and
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 02/SB/MSTh-SB-R2-Ex1-2.EES`
(`TM-0032`). No EES original exists in CoolSolve `misc/EES_ok.zip` for this
example. The CoolSolve example is kept in the CoolSolve repository as a test
case.

## Conversion log

- **2026-10-05 — import**: equations taken over unchanged from the CoolSolve
  example (byte-identical to the EES original TM-0039 apart from the
  translated comments — checked by diff); unit system already SI-°C-Pa-J, no
  conversion needed. Standard header added; one leftover French fragment in a
  dead comment translated (`M_dot = 1` guess); input/parameter meanings and
  SI units added to the trailing comments. Solved with the default pipeline
  (TrustRegion fallback) from `.initials` curated from the EES stored
  solutions; verified (see above).
- **2026-10-05 — differences vs the SB variant** (TM-0032, documented, model
  follows the VL original): fluid `air_ha` instead of `Air`, γ fixed at 1.4
  instead of solved (1.395 in EES), parameters `V_s`/`A_thr`/`T_m` at the VL
  rounding (0.007876 / 0.0001309 / 46.25 vs 0.007877 / 0.0001311 / 46.21);
  impact ≤ 0.15 % on all derived results.

## Limitations and CoolSolve gaps

- The leakage nozzle is assumed always choked (checked: `P_ex` is above the
  critical pressure at all speeds of interest); the `max()` form of the SB
  variant is not needed.
- No CoolSolve gap blocks this model. The absolute enthalpies/entropies of
  `air_ha` carry the CoolProp reference state, offset from EES by a constant
  (see *Verification*); only differences and derived results are comparable.
- Ideal-gas model (dry air): no thermodynamic diagram is available in
  CoolSolve yet (`CS-FEAT-DIAGRAM-IDEAL`); the figure is a parametric sweep
  plot (roadmap decision D7).

## Related models

- `CSL-0007` (semi-empirical scroll compressor): same internal-leakage physics
  (equivalent-nozzle leakage mixed back into suction) at semi-empirical
  reference-model level.
- `CSL-0021` (piston compressor identification on dry air): same course
  (repetition 1) and the same identification-then-prediction approach on
  dry air.
- `CSL-0023` (centrifugal turbocompressor performance): same fluid (`Air`)
  and the same EES-vs-CoolProp reference-state offset on `h` and `s`.
- CoolSolve example `air_screw_compressor_simple.eescode` (CSX-003): same
  model with `N = rpm/60` and `rpm` as the sweep variable (parametric study
  on the speed) — merged here as a documented variant, no separate file.
- `CSL-0067` (piston compressor with inlet pressure drop and internal
  leakage): same course (repetition 2), same equivalent-nozzle leakage
  physics on dry air; there the file's own leakage-consistency loop gives a
  backward leak and the admission-area closure is added at import.
- `CSL-0156` *refrigeration_screw_compressor_r22*: the same leakage (nozzle +
  diffuser) screw-machine concept as a reference model on a real-fluid (R22)
  refrigeration cycle, with sliding-valve part load.
