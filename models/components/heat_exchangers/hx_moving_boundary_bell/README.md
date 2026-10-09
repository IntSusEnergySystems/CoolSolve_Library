# Moving-boundary heat exchanger (Bell 2015), evaporator regime

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0138`

Counter-flow heat exchanger modelled by the moving-boundary method of Bell
et al. (2015): the sections of the exchanger are delimited by the cumulative
heats at the phase changes of the fluids, each section transfers
`Q_j = U_j * LMTD_j * A_j` with zone heat-transfer coefficients, and the
**Bell area constraint** `A = sum(Q_j / (U_j * LMTD_j))` sizes the hot-side
area from the zone conductances. The main program reproduces the five
oracle cases of the original paper's Section A (water / n-propane, areas
0.2 to 7 m2) simultaneously; the active zone set changes with the operating
point (1, 2 or 3 zones) and is handled by min/max-clamped zone boundaries.
Translation of the TESPy `MovingBoundaryHeatExchanger`.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Water, Propane (R290) |
| **Size** | 124 equations (largest block: 18) |
| **Source** | TESPy, `src/tespy/components/heat_exchangers/sectioned.py` + `movingboundary.py`, commit `19425523` |
| **Authors** | Francesco Witte and the TESPy contributors; method: I. Bell, S. Quoilin, E. Georges, J. Braun, E. Groll, W. Horton, V. Lemort (2015) |
| **License** | MIT (translation with credits, roadmap decision D3) |
| **CoolSolve** | 0.3.0@7addbbc — verified against the Bell 2015 oracle cases (see *Verification*) |

## Problem statement

Reproduce Section A of the Bell (2015) moving-boundary oracle: 0.1 kg/s of
liquid water at 330 K, 1 atm is cooled against 0.01 kg/s of n-propane at
275 K entering an evaporator at 9.9768 bar (close to saturation). The
single-phase (liquid/vapour) heat-transfer coefficient is 100 W/m2-K, the
two-phase one 1000 W/m2-K, wall conduction resistance zero, cold/hot area
ratio 1. For hot-side areas A = 0.2, 1, 2, 4, 7 m2, find the heat rate and
the outlet temperatures. The propane outlet crosses the saturation dome as
the area grows: the exchanger is one liquid zone (A = 0.2), then liquid +
two-phase (A = 1), then liquid + two-phase + vapour (A = 2 to 7).

## Model

The exchanger is discretised along the cumulative heat `x` released from the
cold-inlet end. The zone boundaries are the cumulative heats at which the
cold stream reaches the saturated-liquid and saturated-vapour lines (constant
cold-side pressure, as in the oracle cases, `pr = 1`):

- `Q_b1 = Q * clamp((h_f - h_c,in)/(h_c,out - h_c,in), 0, 1)`,
  `Q_b2 = Q * clamp((h_g - h_c,in)/(h_c,out - h_c_in), 0, 1)` — the clamps
  (min/max, as in the TESPy implementation) remove zones that shrink to zero
  duty, so the active zone set follows the operating point: case 1 has one
  active zone, case 2 two, cases 3-5 three;
- zone temperatures at each boundary from `(P, h)` calls on both sides (the
  hot-side boundary enthalpy follows the counter-flow position
  `h_h,in - (Q - Q_b)/m_h`; inside the two-phase zone the cold-side call
  returns the saturation temperature);
- zone mean temperature differences with the smoothed LMTD of Quoilin (2011)
  as implemented in TESPy (`smoothed_lmtd`, threshold eps = 0.001 K,
  slope xi = 5 1/K; Quoilin's original values are 1 K and 1e4) — the EES
  `FUNCTION LMTD_sm`;
- zone overall coefficients as in the original `area_zones_func`:
  `U_j = 1 / (1/alpha_h,j + A*R_cond + A/(alpha_c,j * A_c))` with
  `A_c = area_ratio * A` (zones 1/2/3 use the liquid/two-phase/vapour
  alphas; the hot side stays liquid here);
- the **area constraint** `A = Q_b1/(U_1 LMTD_1) + (Q_b2-Q_b1)/(U_2 LMTD_2)
  + (Q-Q_b2)/(U_3 LMTD_3)` closes the system (the TESPy `area_zones`
  equation group; with the clamps, a vanished zone contributes an identical
  zero term).

With `A` imposed, the unknowns are `Q` and the outlet states. The TESPy test
solves the same problem in two steps (Q pinned to the oracle value to warm
start, area computed as a post-processing result, then Q released with
`area_hot` imposed); the simultaneous-equation form solves it in one step.
Units converted from the oracle's SI-K to the CoolSolve SI-°C convention
(330 K -> 56.85 °C, 275 K -> 1.85 °C); enthalpies keep the CoolProp
reference (no °C offset). CoolProp `'n-Propane'` maps to the EES real-fluid
name `Propane`; `'Water'` stays `Water`.

## How to run

```bash
coolsolve ./hx_moving_boundary_bell.eescode
```

The five cases are solved simultaneously (`DUPLICATE i=1,5`). `.initials`
holds the oracle solution (all variables); it is needed — from default
guesses (1.0) the Newton iteration wanders on this stiff, clamped system
(see *Limitations*).

## Results

| case | A [m2] | Q [W] (oracle) | T_h,out [°C] (oracle) | T_c,out [°C] (oracle) | active zones |
|---|---|---|---|---|---|
| 1 | 0.2 | 451.824 (451.8242) | 55.770 (55.770) | 19.406 (19.406) | 1 (liquid) |
| 2 | 1 | 2289.303 (2289.3026) | 51.377 (51.3767) | 26.850 = T_sat (26.850) | 2 (liquid + two-phase) |
| 3 | 2 | 4163.456 (4163.4556) | 46.894 (46.8943) | 36.053 (36.0526) | 3 |
| 4 | 4 | 4577.242 (4577.2422) | 45.904 (45.9044) | 56.638 (56.6385) | 3 |
| 5 | 7 | 4582.159 (4581.5014) | 45.893 (45.8943) | 56.882 (56.8498) | 3 |

Case 5 sits at effectiveness 0.999999 (pinch ≈ 0.2 mK), hence its slightly
larger deviation. TESPy's own sign convention stores `Q < 0` on the hot
side; this model uses the positive heat rate.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric plot,
     e.g. Q vs hot-side area with the zone-transition points marked -->

## Verification

Reference: the Bell 2015 oracle stored in TESPy
`tests/test_components/bell2015_five_cases.json` (section A, 5 cases), whose
values were re-generated with the local TESPy clone (commit `19425523`) in a
throw-away venv: `pytest tests/test_components/test_bell2015_oracle.py`
→ 7 passed (5 section-A cases + 2 area-ratio round-trips), CoolProp 8.x
backend. Comparison script: `work/csl0138/compare_bell2015.py` (deleted with
the work folder; table above), deviations over Q, T_h,out, T_c,out of the
five cases:

**max |dQ| = 0.0144 % (test tolerance 0.1 %), max |dT| = 0.0327 K (test
tolerance 0.5 K)** — all cases within the oracle tolerances.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the `MovingBoundaryHeatExchanger` of TESPy, files
`src/tespy/components/heat_exchangers/sectioned.py` (zone and area
equations) and `movingboundary.py`, commit `19425523`.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff /
version control history). Original model released under the MIT License.
Changes: translated from Python to CoolSolve; solver plumbing (network,
two-step warm start, oscillation damping) replaced by simultaneous
equations; fixed regime: hot side single-phase, cold side liquid/two-phase/
vapour with clamped boundaries.

Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in
Python", J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.

Scientific basis: I. H. Bell, S. Quoilin, E. Georges, J. E. Braun, E. A.
Groll, W. T. Horton, V. Lemort, "A moving-boundary heat exchanger model with
pressure drop", Applied Thermal Engineering 79 (2015) — the oracle of
`bell2015_five_cases.json` reproduces the paper's HX.py results.

## Conversion log

- **2026-10-09 — import**: hand translation (no extraction tool: Python
  source); SI-K-Pa-J oracle values converted to SI-°C-Pa-J by hand (°C =
  K − 273.15; enthalpies untouched); the iterative zone-boundary
  identification (`_get_moving_steps`, brentq on the linear dp~dh
  assumption) becomes explicit boundary equations at constant pressure (all
  oracle cases have `pr1 = pr2 = 1`; the linear dp~dh handling of pressure
  drops is out of scope, see *Limitations*); `smoothed_lmtd` becomes the
  `LMTD_sm` FUNCTION (block IF/ENDIF form; the single-line form is not
  used, see CoolSolve register `CS-BUG-IF-SINGLELINE`); the TESPy two-step
  solve (Q pinned, then area imposed) becomes one square system per case;
  the per-section area post-processing `_calc_area_hot` and the
  `area_zones` residual are algebraically identical at R_cond = 0 and are
  written as the single area constraint above.
- **2026-10-09 — formulation note**: the min/max-clamped boundaries are
  faithful to the original but make the starting Jacobian singular when a
  zone is shrunk exactly at the solution (cases 1 and 2): convergence
  requires the oracle values as `.initials` (all variables). With default
  guesses the iteration wanders; multi-start/TrustRegion also converge but
  can land on a spurious root with a temperature cross (negative zone ΔT
  admitted by the smoothed LMTD) — the exact initials avoid both.
- **Level**: multi-zone semi-empirical model with property calls, a
  smoothing FUNCTION and careful guesses (taxonomy §3: content level 3)
  → level 3.

## Limitations and CoolSolve gaps

- Fixed regime: the hot side must stay single-phase and the cold side must
  follow liquid → two-phase → vapour (evaporator). A condenser regime
  (vapour → two-phase → liquid) or two phase-changing sides (the oracle's
  section B, propane/propane) needs the same treatment with the zone
  fractions of both sides sorted together — not implemented here.
- Pressure drops are zero (all oracle cases); the original's linear dp~dh
  assumption for locating boundaries under pressure drop is not translated.
- No CoolSolve gap blocks this model (`missing_features` empty): MIN/MAX,
  `DUPLICATE`, user FUNCTIONs and two-phase `(P, h)` property calls all
  behave as in EES.

## Related models

- CSL-0008 (condenser_three_zones): three-zone condenser, fixed zone set.
- CSL-0014 (hx_constant_pinch): three-zone condenser sized by an imposed
  pinch (LaboThapPy pilot).
- CSL-0112 (three_zone_hx_procedures): three-zone/eps-NTU function library.
- CSL-0127 (hx_constant_effectiveness_discretised): discretised HX with
  pinch logic, same fixed-regime spirit.
