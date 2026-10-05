# Piston compressor with inlet pressure drop and internal leakage

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ☑️ **Runs** &nbsp;|&nbsp; `CSL-0067`

A 2-litre piston compressor tested on dry air at 1500 rpm (suction 1 bar /
15 °C, discharge 5 bar). The measured overall volumetric and isentropic
efficiencies, the dead-volume factor `C` and the proportional loss factor
`alpha` are imposed; the suction pressure drop and the internal leakage are
modelled by equivalent isentropic nozzles whose areas are solved as
characteristics of the machine, the leakage flow mixes back into the suction
flow, and the internal compression is isentropic, closed by the
clearance-volume volumetric efficiency `epsilon_v_2 = 1 − C·(r_v − 1)`. The
model is meant to be swept over speed (1500–6000 rpm) to show how the mass
flow and the consumed power vary.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air (dry air, EES real-fluid `Air` → CoolProp `Air`) |
| **Size** | 80 equations, all steady (largest block: 11) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 2, TP 02 extra exercise (file signed "JD"); CoolSolve example `internal_combustion_engine.eescode` (misnamed) |
| **Authors** | TBD (ULiège MSTh course, exercise signed "JD") |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs; compared with the EES stored solution, deviations explained (see *Verification*) |

## Problem statement

A 2-litre piston compressor is tested in the laboratory on dry and pure air at
1500 rpm, suction 1 bar / 15 °C, discharge 5 bar. Identified at this operating
point: volumetric and isentropic efficiencies (0.75 and 0.55 — the
problem-statement comment of the original says 0.65, see *Conversion log*),
dead-volume factor `C = 0.07` and proportional loss factor `alpha = 0.2`.
Show how the mass flow and the consumed power of this compressor could vary
with speed between 1500 and 6000 rpm, taking into account the inlet pressure
drop and the internal leakage (as in the original).

## Model

- **Global efficiencies**: `epsilon_v = V_dot_su/V_dot_s` gives the delivered
  mass flow `M_dot`; `epsilon_s = W_dot_s/W_dot` gives the shaft power from
  the global isentropic power `W_dot_s = M_dot·(h_ex_s − h_su)`.
- **Loss model**: `W_dot = W_dot_loss_0 + (1 + alpha)·W_dot_in` — a constant
  loss plus the internal isentropic power weighted by the proportional factor.
- **Admission nozzle**: the suction pressure drop is an isentropic throttle of
  equivalent area `A_thr_admission`; the throat velocity follows from
  `h_thr_1 + C_thr_1²/2 = h_su` and the throat pressure is
  `P_thr_1 = max(P_crit_1, P_su_1)` with the critical pressure of the nozzle
  `P_crit_1 = (2/(γ₁+1))^(γ₁/(γ₁−1))·P_su` (γ₁ solved, 1.3997 in EES,
  1.3993 in CoolSolve).
- **Internal leakage**: the leak expands isentropically from the internal
  discharge state `h_ex_s_2` to the leakage throat of area `A_thr_leakage`
  (nozzle choked: `P_thr_2 = P_crit_2 ≈ 2.64 bar > P_su_1`) and mixes back
  with the fresh gas (`M_dot·h_su_1 + M_dot_l·h_ex_s_2 = M_dot_in·h_su_2`
  at the plenum pressure `P_su_2 = P_su_1`).
- **Internal compression**: isentropic from the mixed state to `P_ex`;
  consistency with the clearance volume:
  `epsilon_v_2 = 1 − C·(r_v_2 − 1) = M_dot_in/M_dot_th_2`.

In both the EES stored solution and the CoolSolve solution the leakage flow
`M_dot_l` is **negative** (the leak flows from the plenum towards the
discharge, `A_thr_leakage < 0`): the clearance-volumetric-efficiency
consistency forces `M_dot_in < M_dot`. This unphysical sign is *as in the
original*; the CoolSolve example of the same exercise avoided it by imposing
`M_dot_l = 0.1·M_dot`.

| Inputs | Value | Outputs (default run) | Value |
|---|---|---|---|
| `V_s` swept volume | 0.002 m³ | `M_dot` delivered flow | 0.04534 kg/s |
| `rpm` | 1500 | `W_dot` shaft power | 13 936 W |
| `P_su` / `T_su` | 1 bar / 15 °C | `W_dot_in` / `W_dot_loss_0` | 6 383 / 6 276 W |
| `P_ex` | 5 bar | `P_su_1` plenum pressure | 0.574 bar |
| `epsilon_v` / `epsilon_s` | 0.75 / 0.55 | `T_su_2` internal suction | −42.3 °C |
| `C` / `alpha` | 0.07 / 0.2 | `M_dot_l` / `M_dot_in` | −0.01317 / 0.03218 kg/s |
| `A_thr_admission` (closure) | 1.9142e-4 m² | `A_thr_leakage` | −1.348e-5 m² |

## How to run

Open `piston_compressor_suction_drop_leakage.eescode` in the CoolSolve GUI
and press *Solve*, or from a terminal:

```bash
coolsolve ./piston_compressor_suction_drop_leakage.eescode
```

The `.initials` file (EES stored values, absolute `h`/`s` shifted by the
EES↔CoolProp reference-state offset) and `coolsolve.conf` (full solver
pipeline; the default Newton-only pipeline fails on the leakage loop) are
required. To sweep the speed, replace `rpm=1500` (1500–6000 rpm per the
problem statement).

## Results

At the default point the admission nozzle is **not choked**
(`P_su_1 = 0.574 bar > P_crit_1 = 0.528 bar`, `C_thr_1 = 291 m/s`), the
leakage nozzle **is choked** (`P_thr_2 = P_crit_2 = 2.645 bar > P_su_1`,
`C_thr_2 = 378 m/s`), and mixing with the (back-flowing) leak brings the
internal suction to `T_su_2 = −42.3 °C`. The global consistency
`epsilon_s = W_dot_s/W_dot = 7664.56/13935.6 = 0.5500` and
`epsilon_v_2 = 1 − 0.07·(4.68755 − 1) = 0.7419` hold.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot
      (mass flow and power vs speed), saved in figures/ -->

## Verification

Reference: the EES stored solution of the original file (EES 7.458, 55
variables). `compare_solution.py`:
**55 common variables, 38 differ (rtol=0.001); only in EES: 0; only in
CoolSolve: 25** (the 25 are the state-point array variables `P[i]`, `h[i]`,
`T[i]`, `s[i]`, `T_ex_s`, added at import for the diagrams; maximum rel. diff
on the common set: 1.26e+00 on `W_dot_loss_0`).

The deviations are of three kinds, in decreasing order of importance:

1. **`W_dot_loss_0` (rel. diff 1.26)**: the value stored in the original file
   (−1648.98 W) is **stale** — it contradicts the original's own equations:
   `W_dot = W_dot_loss_0 + 1.2·W_dot_in` gives
   −1648.98 + 1.2·11189.5 = 11 778 W while `W_dot_s/epsilon_s` = 7655.98/0.55
   = 13 920 W (the file also stores this 13 920 W). The stored value
   corresponds to an earlier version of the file (computed with the 0.65
   isentropic efficiency of the problem-statement comment:
   7655.98/11 778.4 = 0.650). CoolSolve solves the file as it stands:
   `W_dot_loss_0 = +6276 W` (a physically sensible positive loss).
2. **Leakage/mixing branch — second root**: the leakage loop
   (`M_dot_l`, mixing, clearance consistency) admits different solutions
   depending on the air properties. Under CoolProp's `Air` the loop has one
   root, `M_dot_l = −0.01317` (independent scan of the loop equations with
   CoolProp 8.0.0: sign change between −0.015 and −0.0125, no other root down
   to −0.012 and up to +0.01); the EES 7.458 point (`M_dot_l = −0.00921`) is
   not a root of the same system under CoolProp properties. The EES-7 air
   property formulation (2007-era) differs from CoolProp's, which shifts this
   steeply-coupled root (same situation as the R22 case of `CSL-0001`, EES 7
   vs CoolProp, 1.4 %). Both roots share the negative-leak sign discussed
   above.
3. **Reference-state offsets** (not deviations): absolute `h` and `s` of
   EES `Air` vs CoolProp `Air` differ by a constant (≈ +125.9 kJ/kg on `h`,
   ≈ −1.8 kJ/kg-K on `s` at these states); the 10 `h_*`/`s_*` rows of the
   comparison only reflect this offset, as for `CSL-0020`/`CSL-0023`.

On the admission branch, which is weakly coupled to the leakage loop, the two
solutions agree: `P_su_1`/`P_thr_1`/`P_su_2` within 2.8e-03, `C_thr_1` 1.9e-03,
`V_dot_thr_1` 1.9e-03, `v_thr_1` 1.6e-03, `T_thr_1` 6.2e-03, and the
input-side quantities `W_dot`, `W_dot_s`, `M_dot`, `epsilon_v` within 1.2e-03.
Status **runs**: the model is square (80 equations / 80 variables), converges
to solver tolerance (1e-9) and passes the balance checks above, but the
leakage branch does not reproduce the EES 7.458 stored values.

## Source and attribution

Classroom exercise by the ULiège *Machines et systèmes thermiques* course
(repetition 2, TP 02, extra exercise on the combined suction pressure drop and
internal leakage), file signed "JD" (unidentified author; the `{$ID$}` tag is
the ULiège Thermodynamics Laboratory EES licence). Author to be completed by
the maintainer.

Source file (EES 7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 02/Exercice combiné perte de charge - fuite.EES`
(inventory candidate `TM-0019`). No EES original exists in CoolSolve
`misc/EES_ok.zip` for this example. The CoolSolve example
`examples/internal_combustion_engine.eescode` (title and file name mismatched:
it is the piston compressor, not an internal-combustion engine) is a
**simplified variant** of this exercise: basis `M_dot = 1`, imposed leakage
`M_dot_l = 0.1·M_dot`, imposed `epsilon_s = 0.75`, discharge 4 bar, no
clearance-volume and no loss equations, results quoted in its comments. It is
kept in the CoolSolve repository as a test case; the library model follows the
EES original.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, EES 7.458): unit system
  already SI-°C-Pa-J, no conversion; no lookup/parametric tables; comments
  translated to English (paraphrases of the original); standard header added;
  equations unchanged. `(T+273)` kept as in the original (temperature ratios).
- **2026-10-05 — closure of the original file**: as saved, the file is
  **underdetermined by one equation** (54 equations / 55 variables, checked on
  the unmodified extraction: `System square: No`; the matching leaves
  `P_su_1` free, the only constraint on the admission branch being
  `P_thr_1 = max(P_crit_1, P_su_1)`, i.e. the plenum pressure and the
  equivalent admission area cannot both be outputs). Its stored solution is
  also inconsistent with its own `W_dot` equations (see *Verification*, item
  1) — both signs that the file was edited after its last solve. Closure
  added at import, in the spirit of `CSL-0020` (identified parameter
  imposed so the model can be swept over speed):
  `A_thr_admission = 1.9142E-4 [m2]`, the value of the original stored
  solution; all other equations unchanged. With this closure the stored
  values of the admission branch are reproduced (≤ 0.3 %).
- **2026-10-05 — input defaults and comments**: `epsilon_s = 0.55` kept (the
  equations rule; the problem-statement comment says 0.65 — the stored
  solution confirms the file was last solved at 0.65); the commented
  "provisional value: gamma = 1.4" lines kept as comments (γ is solved:
  1.3993 / 1.3963 in CoolSolve vs 1.3997 / 1.3889 stored).
- **2026-10-05 — state points**: post-processing block `P[i]`, `h[i]`, `T[i]`,
  `s[i]` (i = 1…6: suction line, admission throat, internal suction after
  mixing, internal isentropic discharge, leakage throat, global isentropic
  discharge) added for the thermodynamic diagrams; results unchanged.
- **2026-10-05 — `.initials`**: EES stored values, with the absolute `h`
  (`+125874 J/kg`) and `s` (`−1815 J/kg-K`) shifted into the CoolProp
  reference frame and `W_dot_loss_0` re-guessed at 500 W (the stored value is
  stale, see *Verification*).
- **2026-10-05 — solver**: the default pipeline (Newton only) fails on the
  11-variable leakage loop (line-search failure); `coolsolve.conf` enables
  the full solver pipeline, which converges in 45 iterations.
- **Level**: score of docs/taxonomy.md §3 — equations 80 → 1; largest block
  11 → 1; arrays (state points) → 1; multi-zone/discretised → 0;
  semi-empirical identified parameters → 1; curated guesses + solver config
  → 1; total 5 → level 3, **moved to level 2** (±1 allowed): classroom
  exercise, same course and same model family (equivalent-nozzle leakage,
  identified parameter imposed, speed sweep) as the level-2 `CSL-0020`.

## Limitations and CoolSolve gaps

- The leakage flow comes out negative (as in the original's own stored
  solution): the clearance-consistency loop of the original model cannot
  represent a forward internal leak together with the identified global
  efficiencies; the CoolSolve example of the same exercise imposed the leak
  at 10 % instead. The model characterises the machine by two equivalent
  areas (`A_thr_admission`, `A_thr_leakage`) meant to be swept over speed.
- No CoolSolve gap blocks this model (`missing_features` empty). Absolute
  `h`/`s` carry the CoolProp reference state (offset vs EES, see
  *Verification*); only differences and derived results are comparable.
- Ideal-gas-like single-phase model on dry air: no thermodynamic diagram is
  available in CoolSolve yet (`CS-FEAT-DIAGRAM-IDEAL`); the figure is a
  parametric sweep plot (roadmap decision D7).

## Related models

- `CSL-0020` (dry air screw compressor with internal leakage): same course,
  same equivalent-nozzle leakage physics with an identified area imposed;
  there the leak flows forward (positive area) and the model verifies.
- `CSL-0021` (piston compressor identification on dry air): same machine type
  (piston, dry air) with parameters identified from test data.
- CoolSolve example `internal_combustion_engine.eescode` (CSX-025): simplified
  variant of this exercise (imposed 10 % leak, `M_dot = 1` basis, no
  clearance/loss block), merged here; the example stays in CoolSolve.
