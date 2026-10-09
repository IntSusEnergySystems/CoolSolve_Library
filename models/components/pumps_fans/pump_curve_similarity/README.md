# Centrifugal pump from manufacturer curves and similarity laws

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0125`

A pump whose performance is described by the four characteristic curves of a
catalogue (volumetric flow rate, head rise, isentropic efficiency, required
NPSH versus flow rate at a rated speed), scaled to any other speed with the
classical affinity (similarity) laws — the model of a pump selected from a
manufacturer catalogue and operated away from its rated point. Three operating
modes are shipped, one file each, as in the original component: `P_N`
(suction and discharge pressures and speed given → flow rate and power), `P_M`
(pressures and mass flow rate given → speed) and `M_N` (suction conditions, mass
flow rate and speed given → discharge pressure).

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | R744 (CO2); any liquid accepted by the property functions |
| **Size** | 33 equations (largest block: 1) in the main file, 31 / 32 in the two variants |
| **Source** | LaboThapPy (Apache-2.0 / MIT), file `labothappy/component/pump/pump_curve_similarity.py`, commit `f03f7f47` |
| **Authors** | Basile Chaudoir, Elise Neven (ULiège Thermodynamics Laboratory; LaboThapPy contributors, see `AUTHORS.txt`) |
| **License** | MIT (translation with credits, roadmap decision D3) |
| **CoolSolve** | main 2026-10-05 — runs; verified against the LaboThapPy component in its three modes (see *Verification*) |

## Problem statement

Reproduce the CO2 case of the LaboThapPy example `pump_curve_similarity_example.py`:
a pump with the catalogue curves of the example (head 1211 m at 1298 m³/h,
efficiency 0.867, rated speed 2900 rpm) sucks CO2 at 45.6 bar, 9.19 °C and
delivers it at 152.54 bar at 2900 rpm. Find the flow rate, the mass flow rate,
the isentropic efficiency, the required NPSH, the discharge state and the shaft
power; then answer the two reciprocal questions of the model: which speed is
needed for a given mass flow rate between the same two pressures, and which
discharge pressure is obtained for a given mass flow rate at a given speed.

## Model

Manufacturer curves at the rated speed `N_rot_rated`, read from the lookup
table `pump_curves` (columns `V_dot_rated` [m³/h], `Delta_H_rated` [m],
`eta_is_rated` [-], `NPSH_r_rated` [m]) with linear interpolation:

$$\Delta H(Q_r) = \mathrm{INTERPOLATE}(\text{curves}, Q_r),\quad
\varepsilon_{is}(Q_r),\quad \mathrm{NPSH}_r(Q_r)$$

Similarity laws (affinity laws, speed ratio $s = N/N_\text{rated}$), as in the
original:

$$Q = s\,Q_r,\qquad \Delta H = s^2\,\Delta H_r,\qquad
\mathrm{NPSH}_r = s^2\,\mathrm{NPSH}_{r,r},\qquad \varepsilon_{is}\ \text{unchanged}$$

Pump thermodynamics (incompressible-fluid approximation for the head, as in the
original): $\Delta H = \Delta P/(g\rho)$,
$h_{ex} = h_{su} + (h_{ex,s}-h_{su})/\varepsilon_{is}$ with
$h_{ex,s} = h(P_{ex},s_{su})$, ideal hydraulic power $\dot W_{hyd}=g\,\Delta H\,\dot m$
and shaft power $\dot W_{shaft}=\dot m\,(h_{ex}-h_{su})$.

The Python `interp1d` objects, the scaled curve arrays and the scalar
root-find on the speed are replaced by simultaneous equations (see
*Conversion log*); the mode selects which variable is unknown:

| Mode | Known | Unknown | Equations that close it |
|---|---|---|---|
| `P_N` (main file) | `P_su`, `T_su`, `P_ex`, `N_rot` | `V_dot`, `m_dot` | head curve inverted at the scaled head: $V_dot = s\,\Delta H_r^{-1}(\Delta H/s^2)$ |
| `P_M` (`…_mode_PM`) | `P_su`, `T_su`, `P_ex`, `m_dot` | `N_rot` | scaled head curve equals the required head (implicit equation in `N_rot`) |
| `M_N` (`…_mode_MN`) | `P_su`, `T_su`, `m_dot`, `N_rot` | `P_ex` | $P_{ex} = P_{su} + \rho g\,\Delta H_r(Q/s)\,s^2$ |

`V_dot_flag` (1 when the operating flow rate falls outside the range covered by
the curves) reproduces the original's out-of-range flag, through the small
`FUNCTION flow_outside_curve`.

| Inputs | Value (default run) | Outputs | Value |
|---|---|---|---|
| `fluid$` | R744 | `V_dot` | 1233.72 m³/h |
| `P_su` / `T_su` | 45.5955 bar / 9.194 °C | `m_dot` | 297.88 kg/s |
| `P_ex` | 152.540 bar | `eta_is` | 0.8628 |
| `N_rot` / `N_rot_rated` | 2900 / 2900 rpm | `NPSH_r` | 2.4517 m |
| curves | table `pump_curves` | `Delta_H` / `W_dot_hyd` | 1254.18 m / 3.665 MW |
| | | `h_ex` / `T_ex` | 237.14 kJ/kg / 20.22 °C |
| | | `W_dot_shaft` | 4.146 MW |

## How to run

```bash
coolsolve ./pump_curve_similarity.eescode            # mode P_N (main file)
coolsolve ./pump_curve_similarity_mode_PM.eescode   # mode P_M
coolsolve ./pump_curve_similarity_mode_MN.eescode   # mode M_N
```

Each file has its own companion table `<file stem>-pump_curves.csv` (identical
content, the CoolSolve per-file convention). No `.initials` file is needed: the
three files converge from the default guesses (0, 10 and 0 Newton iterations).
The three modes are shipped as three files (instead of the commented
alternatives suggested for mode switches) so that each of them is solved and
regression-tested: `CSL-0125`, `CSL-0125:mode_PM`, `CSL-0125:mode_MN`.

## Results

All three modes describe the same operating point (the mass flow rate of the
`P_N` run is fed to the other two), so they agree by construction:

| Quantity | `P_N` (main) | `P_M` | `M_N` |
|---|---:|---:|---:|
| `V_dot` [m³/h] | 1233.72 | 1233.72 | 1233.72 |
| `m_dot` [kg/s] | 297.882 | 297.882 | 297.882 |
| `Delta_H` [m] | 1254.18 | 1254.18 | 1254.18 |
| `eta_is` [-] | 0.86280 | 0.86280 | 0.86280 |
| `NPSH_r` [m] | 2.4517 | 2.4517 | 2.4517 |
| `P_ex` [bar] | 152.540 | 152.540 | 152.540 |
| `N_rot` [rpm] | 2900 | 2900 | 2900 |
| `W_dot_hyd` [MW] | 3.6650 | 3.6650 | 3.6650 |
| `W_dot_shaft` [MW] | 4.1461 | 4.1461 | 4.1461 |
| `T_ex` [°C] | 20.223 | 20.223 | 20.223 |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (1 suction, 2 discharge) give the pump
path on the P-h or T-s diagram (CoolSolve *Diagram* tab, *Overlay array path*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): pump path
      (suction → discharge) on a P-h diagram of R744,
      figures/pump_curve_similarity_ph.png, or a parametric plot of V_dot,
      W_dot_shaft and NPSH_r versus N_rot (sweep N_rot or P_ex in the Parametric
      tab of the main file) -->

## Verification

1. **Source example reproduced.** The CO2 case of
   `labothappy/component/examples/pump/pump_curve_similarity_example.py`
   (LaboThapPy snapshot `~/git/LaboThapPy`, commit `f03f7f47`) was run in a
   throw-away virtual environment under `work/` (`pip install ~/git/LaboThapPy`,
   CoolProp 8.0.0, SciPy 1.18, Python 3.12; the plotting call of the example
   skipped). Curve data and `P_N` inputs are those of the example; `solved` is
   `True` in the three modes. The `P_M` and `M_N` modes are driven at the
   operating point found by `P_N`. Two temporary driver scripts did this (they
   lived in `work/pump_curve_similarity/`, deleted at the end of the card as
   the workflow requires, and are described here so that the reference can be
   rebuilt): one imports `PumpCurveSimilarity` from the installed clone,
   applies the curve data and the inputs of the example (curve data exactly as
   written there — the four arrays scaled by `V_dot_rated/250.2`,
   `eta_rated/79.2` and `D_H_rated/1105.7`, the NPSH array unchanged,
   `N_rot_rated` = 2900 rpm), runs the three modes and writes the results of
   each as a `name,value,units` CSV read by `compare_solution.py`; the second
   runs the affinity-law check of item 5. The driver also replaces the
   connector update of the component, which raises `KeyError` on `P_ex` in
   mode `M_N` (there `P_ex` is an output, not an input) and would otherwise
   discard the computed discharge pressure; no computed quantity is affected by
   that replacement.
2. **Property backend.** LaboThapPy's `MassConnector` evaluates properties with
   the `BICUBIC&HEOS` backend (spline-augmented CO2 tables,
   `labothappy/connector/mass_connector.py`), CoolSolve with CoolProp's `HEOS`.
   Both are based on the same equation of state; at the suction state they give
   $\rho_{su}$ = 871.60 vs 869.22 kg/m³ (0.27 %) and $h_{su}$ = 222 764 vs
   223 220 J/kg (0.20 %). Since $\Delta H = \Delta P/(g\rho_{su})$, this
   propagates to the flow rate and to the power. The reference was therefore
   re-run with the connector forced to the plain `HEOS` backend (identical code,
   only the backend string changed).
3. **Model vs the HEOS reference** (`tools/compare_solution.py`, `--ees-units`,
   tolerance 1·10⁻³): **all common variables agree, largest relative difference
   1.13e-09** (`NPSH_r`) for the main file; the same 1.13e-09 for
   `…_mode_PM` and `…_mode_MN`. `V_dot_flag` = 0 everywhere (the operating
   point is inside the curves: 1233.7 m³/h between 395.3 and 1533.0 m³/h).
   Against the **default** LaboThapPy run (bicubic backend) the same
   comparison gives a largest difference of 7.2e-03 (`W_dot_shaft`), 6.8e-03
   (`m_dot`), 4.1e-03 (`V_dot`), 2.7e-03 (`Delta_H`), 1.7e-02 (`NPSH_r`,
   a small quantity read on a steep part of its curve) — the effect of the
   backend, item 2.
4. **Self-consistency of the three modes.** Feeding the `P_N` mass flow rate
   (297.8817 kg/s) to `P_M` returns `N_rot` = 2900.000 rpm (5.8e-15 relative),
   and feeding it with `N_rot` = 2900 rpm to `M_N` returns `P_ex` =
   15 254 008.43 Pa (1.3e-12).
5. **Affinity laws exact** (the self-check named in the task card). The
   component was run at half and double the rated speed, with the discharge
   pressure set so that the required head is exactly ¼ and 4 times the
   rated-speed head:

   | Check | LaboThapPy (original) | CoolSolve | expected |
   |---|---|---|---|
   | `P_N`, N = 1450 rpm, head 313.544 m → `V_dot` [m³/h] | 616.857928 | 616.857928 | ½ × 1233.715857 |
   | `P_N`, N = 5800 rpm, head 5016.705 m → `V_dot` [m³/h] | 2467.431713 | 2467.431712 | 2 × 1233.715857 |
   | `P_N`, N = 1450 rpm → `NPSH_r` [m] | 0.612928 | 0.612928 | ¼ × 2.451713 |
   | `P_M`, m_dot = 148.941 kg/s → `N_rot` [rpm] | 1450.000000 | 1450.000001 | 1450 |
   | `P_M`, m_dot = 595.763 kg/s → `N_rot` [rpm] | 5800.000000 | 5799.9999996 | 5800 |

   $Q\sim N$ and $H\sim N^2$ hold to 1.5e-14 relative in the original
   (against the scaled expected value) and the CoolSolve results agree with the
   original to 4e-10 relative; the speed recovered by `P_M` to 1.1e-9 (Newton
   tolerance).

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of `PumpCurveSimilarity` from LaboThapPy, file
`labothappy/component/pump/pump_curve_similarity.py`, commit `f03f7f47`.
LaboThapPy — https://github.com/PyLaboThap/LaboThapPy —
Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université
de Liège (ULiège), Université de Mons (UMONS). Original authors: B. Chaudoir,
E. Neven (see `AUTHORS.txt`). Curve data: the "CO2 pump data" of the example
(docstring of `pump_curve_similarity_example.py`, manufacturer curves
normalised there to a head of 1211 m at 1298 m³/h, efficiency 0.867, rated
speed 2900 rpm); they are shipped as the lookup table `pump_curves` with the
same numbers.
Scientific basis: the affinity (similarity) laws of turbomachinery, developed in
the original as in the PDF documentation
`~/git/LaboThapPy/docs/source/_static/pdf_files/PumpCurveSimilarity.pdf` and
`PumpSimLaw.pdf` (not copied: LaboThapPy documentation is CC BY-SA 4.0); no
correlation is taken from another library in this model.

Source files (not copied into the library):
`~/git/LaboThapPy/labothappy/component/pump/pump_curve_similarity.py` and
`~/git/LaboThapPy/labothappy/component/examples/pump/pump_curve_similarity_example.py`;
reference: URL above + path `labothappy/component/pump/pump_curve_similarity.py`.
No student names or personal data involved.

## Conversion log

- **2026-10-08 — translation**: the four manufacturer curves and the three
  modes of `PumpCurveSimilarity` transcribed as simultaneous EES equations.
  Changes, all logged:
  - `interp1d(..., kind="linear", fill_value="extrapolate")` → lookup table
    `pump_curves` + `INTERPOLATE` (linear); the scaled curve arrays
    (`V_dot_curve*s`, `Delta_H_curve*s²`, `NPSH_r_curve*s²`) are evaluated on
    the rated curves at the equivalent flow rate `V_dot/s`, which is exactly
    equivalent for a linear interpolant. The `P_N` inversion of the head curve
    (`interp1d(Delta_H_curve, V_dot_curve)`) is
    `INTERPOLATE('pump_curves','Delta_H_rated','V_dot_rated', Delta_H/s²)`
    (the head column is in descending order, which EES accepts and CoolSolve
    accepts since `CS-BUG-INTERP-DESC` was fixed; checked on this build: a
    head of 1250.75 m returns 1239.42 m³/h, the hand-computed linear
    interpolation of the curve);
  - the scalar `brentq` root-find on `N_rot` of `solve_PM` → one implicit
    equation for `N_rot`, the algebraic rearrangement
    `N_rot = N_rot_rated*SQRT(H_required/H_rated(V_dot*N_rot_rated/N_rot))`
    (identical root; a residual variable set to zero would need an equation per
    unknown, which CoolSolve rejects as over-determined);
  - the connector/network plumbing (`MassConnector`, `WorkConnector`,
    `check_parametrized`, `solve()` dispatch) → plain equations: the required
    inputs are given as values, the outputs as unknowns;
  - the `x = 0` saturation check on the suction connector
    (`if 1 >= self.su.x > 0`) dropped: the example case is a single-phase
    subcooled liquid (1.32 K below saturation at `P_su`, `Q` = 0, so the check
    is never taken), and the check is a component-level guard;
  - `su.D` → `rho_su`, `g = 9.81` kept (value of the original; EES's built-in
    `G` = 9.80665 m/s² is shadowed);
  - `interp1d`'s **linear extrapolation** outside the curve range is replaced
    by the flat extrapolation (clamping) of CoolSolve/EES lookup tables: see
    *Limitations*; the original's `V_dot_flag` is kept as `V_dot_flag`;
  - the reference run itself is described in *Verification* (the two temporary
    driver scripts lived in `work/`, deleted at the end of the card);
  - the original's printing of `V_dot`, `m_dot`, `P_ex`, `N_rot`, `W_dot`,
    `W_dot_hyd`, `eta_is`, `NPSH_r` and the temperature/entropy of the states is
    replaced by the 8 post-processing state-array equations added for the
    diagrams (results unchanged).
  - K → °C: `T_su = 283.34364983582685 K − 1 K = 282.34365 K = 9.19365 °C`;
    `m_dot` in kg/s, `V_dot` in m³/h, `N_rot` in rpm and head in m are kept
    (SI for these quantities, as in the original).
- **2026-10-08 — modes**: the mode switch of the Python component becomes three
  files (main = `P_N`, `mode_PM`, `mode_MN`), each with its companion table and
  its `.sol` baseline, instead of commented alternatives, so that each mode is
  solved and regression-tested. In `M_N` the original reads `eta_is` and
  `NPSH_r` on the *rated* curves at the actual flow rate (no speed scaling,
  unlike the other two modes); this is reproduced as in the original and
  commented in the file.
- **2026-10-08 — Level**: rubric of taxonomy §3 — 33 equations (< 50 → 0),
  largest block 1 (≤ 5 → 0), functions and arrays present (1), three coupled
  components no (0), semi-empirical / off-design (characteristic curves of a
  catalogue, three operating modes → 1), numerics: converges from the default
  guesses (0) — score 2 → **level 2**.

## Limitations and CoolSolve gaps

- **No extrapolation** (registered gap `CS-GAP-INTERP-EXTRAP`, *not* blocking
  this model). `interp1d(fill_value="extrapolate")` of the original continues
  the curve linearly outside its range, while CoolSolve/EES clamp to the last
  table point. The three shipped cases are inside the curves (1233.7 m³/h
  between 395.3 and 1533.0 m³/h), but an operating point outside them is
  silently returned at the curve end: `V_dot_flag` and the `V_dot_rated_min/max`
  variables are there to be checked, and the extrapolation has to be applied
  by hand (polynomial fit or extended table).
- **Density of the suction state** is used for the head (`Delta_H = DeltaP/(g·rho)`),
  as in the original: for a two-phase or compressible fluid the head is an
  approximation. The `M_N` branch of the original uses the same density for the
  discharge pressure.
- **Catalogue curves are scaled rigidly**: no impeller trimming, no off-design
  efficiency model, and the speed ratio is applied to the head and NPSH only
  (power scaling $P\sim N^3$ is used only in the plotting function of the
  original, which is not translated — the shaft power comes from the
  thermodynamics).
- **`V_dot_flag`** is 0 in the shipped cases; the `M_N` branch of the original
  compares the flow rate with the *rated* range (not the scaled one) and
  `P_M` has no flag at all — reproduced as in the original.
- No CoolSolve gap blocks this model (`missing_features` is empty): the three
  files are valid EES and converge. The only behavioural difference met
  (`CS-GAP-INTERP-EXTRAP`, already registered, and `CS-BUG-INTERP-DESC`, closed)
  does not affect the shipped operating points.

## Related models

- `CSL-0084` (*orc_expander_pump_empirical_maps*): empirical pump/expander
  maps as function library for ORC off-design studies; this model uses
  manufacturer curves + affinity laws (different data and closure).
- `CSL-0072` (*centrifugal_brine_pump_refsim*): brine pump reference model
  (RefSim), component-level; no catalogue curves.
- `CSL-0071` (*centrifugal_fan_reference_model*): centrifugal fan with
  dimensionless factors, i.e. the affinity laws applied to a fan.