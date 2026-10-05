# LiBr-water absorption chiller cycle with a solution heat exchanger

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0043`

Single-effect absorption chiller on the LiBr-H2O pair at one operating point:
water is the refrigerant, a lithium-bromide solution the absorbent. The
equilibrium concentrations of the weak (absorber) and rich (generator)
solutions are obtained with the EES built-in LiBr solution routines `X_LIBR`
and `H_LIBR`; mass and LiBr conservation give the solution flow rates and a
generator energy balance gives the driving heat and the COP, with a 75 %
effective solution heat exchanger between absorber and generator.

**Blocked**: CoolSolve has no LiBr-H2O solution properties (`X_LIBR`/`H_LIBR`
unknown, gap `CS-GAP-FLUIDS-ABS`, registered for the CoolSolve example
`water_libr`). The model file is kept in native EES syntax; CoolSolve parses
it, finds the system square (46 equations / 46 variables, largest block 3)
and stops on `Block 16 failed: Unknown or unsupported function: X_LIBR with 3
arguments`.

| | |
|---|---|
| **Category** | Cycles and machines › Absorption and sorption |
| **Fluids** | Water (refrigerant), LiBr-H2O solution (absorbent) |
| **Size** | 46 equations (largest block: 3): 30 for the model, 16 for the diagram state points |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 11, exercise 2 (EES file `MSTH-SB-R11-EX2.EES`) |
| **Authors** | TBD (ULiège MSTh course: J. Lebrun, V. Lemort, S. Bertagnolio) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — blocked by `CS-GAP-FLUIDS-ABS` (no LiBr solution properties) |

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
diagrams (added by the library as post-processing; not exercised until the
blocking gap is closed).

## How to run

Not runnable: CoolSolve stops on the unknown LiBr functions (see above). Open
`libr_water_absorption_chiller.eescode` in EES, or solve the CoolSolve example
`examples/water_libr.eescode` once `CS-GAP-FLUIDS-ABS` is closed (same
equations, same blocked status).

## Results (EES stored solution of the original, 30/30 variables)

| Variable | Value | Variable | Value |
|---|---:|---|---:|
| `P_ev` | 872.60 Pa | `Q_dot_ev` | 2.3213 MW |
| `P_cd` | 9589.78 Pa | `Q_dot_cd` | 2.5558 MW |
| `x_abs` | 58.303 mass % | `Q_dot_gen` | 3.1088 MW |
| `x_gen` | 74.776 mass % | `Q_dot_HEX` | 0.39578 MW |
| `M_dot_weak` | 4.5395 kg/s | `epsilon_HEX` | 0.75 |
| `M_dot_rich` | 3.5395 kg/s | `COP` | 0.7467 |

These are the reference values a future CoolSolve run must reproduce
(verification when `CS-GAP-FLUIDS-ABS` is closed).

## Verification

Not verified: the model is blocked and no CoolSolve run exists. The EES stored
solution of the original file (`MSTH-SB-R11-EX2.EES`, 30/30 variables, table
above) is the reference for the re-check. CoolSolve reproduces the water-side
properties (the example `water_libr.eescode` parses and the system is square);
only the LiBr routines are missing.

## Source and attribution

Exercise solution of the ULiège course *Machines et systèmes thermiques*
(repetition 11, exercises 1–4, LiBr-H2O absorption chiller; the file itself
names no author). Source file (EES 7.458, comments in French), collection of
S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 11/MSTH-SB-R11-EX2.EES`
(inventory candidate `TM-0167`).

The CoolSolve example `examples/water_libr.eescode` is a verbatim transcription
of the same file (equation diff identical, only the comments differ); it stays
in the CoolSolve repository as a test case for `CS-GAP-FLUIDS-ABS`.

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
  construction; not exercised until the gap is closed.
- **2026-10-05 — no runnable variant**: the register's workaround for
  `CS-GAP-FLUIDS-ABS` ("external correlations as EES functions") requires a
  published LiBr property correlation, which is not available in the source
  collection (the originals call the EES built-in routines); no correlation
  constants were at hand, so none were invented. A variant will be added at
  the re-check, once a correlation source is chosen.
- **Level justification** (taxonomy.md §3): 46 equations (<50 → 1), largest
  block 3 (≤5 → 0), no procedures/arrays (0), ≥3 coupled components (0/1 →
  1), no calibration/off-design (0), no curated guesses needed (0); score 2 →
  level 2, as pre-assigned by the card.

## Limitations and CoolSolve gaps

- Blocked by `CS-GAP-FLUIDS-ABS` (no `X_LIBR`/`H_LIBR`/`LiBrH2O` support in
  CoolSolve); the only gap of the native file.
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
- No other absorption model in the library yet (2026-10-05).
