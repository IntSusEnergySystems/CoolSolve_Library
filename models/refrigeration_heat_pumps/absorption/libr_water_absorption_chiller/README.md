# LiBr-water absorption chiller cycle with a solution heat exchanger

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0043`

Single-effect absorption chiller on the LiBr-H2O pair at one operating point:
water is the refrigerant, a lithium-bromide solution the absorbent. The
equilibrium concentrations of the weak (absorber) and rich (generator)
solutions are obtained with the EES built-in LiBr solution routines `X_LIBR`
and `H_LIBR`; mass and LiBr conservation give the solution flow rates and a
generator energy balance gives the driving heat and the COP, with a 75 %
effective solution heat exchanger between absorber and generator.

The model file is native EES syntax; CoolSolve evaluates `X_LIBR` and `H_LIBR`
with the ASHRAE LiBr-H2O correlations of the EES routines.

| | |
|---|---|
| **Category** | Cycles and machines › Absorption and sorption |
| **Fluids** | Water (refrigerant), LiBr-H2O solution (absorbent) |
| **Size** | 46 equations (largest block: 3): 30 for the model, 16 for the diagram state points |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 11, exercise 2 (EES file `MSTH-SB-R11-EX2.EES`) |
| **Authors** | TBD (ULiège MSTh course: J. Lebrun, V. Lemort, S. Bertagnolio) |
| **License** | MIT |
| **CoolSolve** | native file runs (59 iterations); verified against the EES stored solution (max 5.6e-04) |

## Problem statement

An LiBr-water absorption cycle runs between an evaporation temperature of
5 °C, an absorber temperature of 40 °C, a condensation temperature of 45 °C
and a generator temperature of 130 °C. A solution heat exchanger of
effectiveness 75 % recovers heat between the rich and weak solution loops.
With a refrigerant (water) flow rate of 1 kg/s, determine the solution
concentrations and flow rates, the heat rates of evaporator, condenser,
generator and solution heat exchanger, and the COP.

## Model

Water loop: saturation pressures at `T_ev` and `T_cd`, isenthalpic expansion,
`Q_dot_ev = M_dot_w (h_w_ev_ex − h_w_ev_su)`, `Q_dot_cd` and the generator
vapour state at `(T_gen, P_cd)` from `ENTHALPY(Water,…)`. Solution loop: the
concentrations `x_abs` and `x_gen` (mass %) are the saturation concentrations
given by `X_LIBR('SI',T,P)`; LiBr conservation (`M_dot_libr = x_abs·M_dot_weak
= x_gen·M_dot_rich`) gives the weak and rich flow rates, and `H_LIBR('SI',T,x)`
gives the solution enthalpies for the absorber/generator energy balance and
the solution heat exchanger (`epsilon_HEX = 0.75`). `COP = Q_dot_ev/Q_dot_gen`.

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 evaporator outlet, 2 generator
outlet, 3 condenser outlet, 4 evaporator inlet) describe the water loop on the
diagrams (added by the library as post-processing).

## How to run

```bash
coolsolve ./libr_water_absorption_chiller.eescode
```

It solves in 59 iterations from the default guesses. The CoolSolve example
`examples/water_libr.eescode` has the same equations.

## Results (EES stored solution of the original, 30 variables, and CoolSolve)

| Variable | EES | CoolSolve |
|---|---:|---:|
| `P_ev` [Pa] | 872.60 | 872.58 |
| `P_cd` [Pa] | 9589.78 | 9595.0 |
| `x_abs` [mass %] | 58.303 | 58.308 |
| `x_gen` [mass %] | 74.776 | 74.772 |
| `M_dot_weak` [kg/s] | 4.5395 | 4.5415 |
| `M_dot_rich` [kg/s] | 3.5395 | 3.5415 |
| `Q_dot_ev` [MW] | 2.3213 | 2.3216 |
| `Q_dot_cd` [MW] | 2.5558 | 2.5563 |
| `Q_dot_gen` [MW] | 3.1088 | 3.1094 |
| `Q_dot_HEX` [MW] | 0.39578 | 0.39600 |
| `epsilon_HEX` [-] | 0.75 | 0.75 |
| `COP` [-] | 0.7467 | 0.7466 |

## Verification

CoolSolve solution against the EES stored solution of the original file
(`MSTH-SB-R11-EX2.EES`, 30 of 30 variables; `compare_solution.py`, rtol 1e-3):
30 common variables, 0 differ; maximum relative difference **5.6·10⁻⁴**
(`M_dot_rich`, `Q_dot_HEX`, `P_cd`: 5.4·10⁻⁴). The 16 variables only in CoolSolve
are the diagram state points added by the library. The small differences are
those expected from the water properties (CoolProp against EES, for example the
saturation pressure at 45 °C, 9595.0 against 9589.78 Pa) and from the stored
EES run; their origin was not separated further.

## Source and attribution

Exercise solution of the ULiège course *Machines et systèmes thermiques*
(repetition 11, exercises 1–4, LiBr-H2O absorption chiller; the file itself
names no author). Source file (EES 7.458, comments in French), collection of
S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 11/MSTH-SB-R11-EX2.EES`
(inventory candidate `TM-0167`).

The CoolSolve example `examples/water_libr.eescode` is a verbatim transcription
of the same file (equation diff identical, only the comments differ); it stays
in the CoolSolve repository as an example.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): unit
  system already SI-C-Pa-J; EES licence tag removed. Comments translated to
  English and standard header added; no equation changed with respect to the
  original `MSTH-SB-R11-EX2.EES` (verified identical to the verbatim
  transcription of the CoolSolve example). Original quirks kept as they are
  and documented in the file comments: `DELTAT_oh`/`DELTAT_sc` are given but
  unused, saturation pressures are evaluated at `x=0.5` (mid-quality, i.e. the
  saturation pressure), and `M_dot_libr = x_abs·M_dot_weak` comes out on a
  100 kg/s scale because `X_LIBR` returns mass % — it does not enter the
  energy balances.
- **2026-10-05 — diagram support**: block of 16 post-processing equations
  (water-loop state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`) added at the end;
  pure post-processing on existing variables, results unchanged by
  construction.
- **Level justification** (taxonomy.md §3): 46 equations (<50 → 1), largest
  block 3 (≤5 → 0), no procedures/arrays (0), ≥3 coupled components (0/1 →
  1), no calibration/off-design (0), no curated guesses needed (0); score 2 →
  level 2, as pre-assigned by the card.

## Limitations and CoolSolve gaps

- `X_LIBR` and `H_LIBR` are the ASHRAE-handbook correlations (validity
  ranges 45…75 % and 40…70 %, documented and not enforced, as in EES). The
  `V_LIBR` routine of the variant files is not available in CoolSolve
  (`CS-GAP-FLUIDS-ABS`).
- The solution pump work is neglected (as in the original exercise; the VL
  version of the same exercise computes it with `V_LIBR`, same gap).

## Variants of the same exercise (triaged into this model, described only)

- *Repetition 11, exercise 1* (`TM-0164`, `TM-0166`, `TM-0168`): same cycle
  **without** solution heat exchanger — `h_weak_gen_su = h_weak_abs_ex`
  closes the solution loop at the absorber temperature; no `Q_dot_HEX`.
  COP 0.6624 (EES stored value of the VL version `TM-0466`, vs 0.7467 with
  the exchanger; the MSTh exercise-1 files `TM-0164/0166/0168` were last run
  from the parametric table and store no COP).
- *Repetition 11, exercise 3* (`TM-0466/0467/0468`, VL version): same
  temperatures; exercise 2 adds the exchanger, exercise 3 imposes
  `Q_dot_ev = 1 MW` instead of `M_dot_w = 1` and asks for the solution flow
  rate and the exchanger duty, and computes the pump work with `V_LIBR`
  (same gap). Same physics, other imposed values.

## Related models

- CoolSolve example `examples/water_libr.eescode` (verbatim transcription of
  the same original, kept in the CoolSolve repository).
- `CSL-0249` *nh3h2o_absorption_chiller*: the ammonia-water single-effect
  chiller with rectifier, the other working pair of the library.
