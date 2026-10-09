# Pressure drop in straight pipes: friction factors and two-phase correlations

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0130`

EES `FUNCTION` library of the pipe pressure-drop correlations of
[LaboThapPy](https://github.com/PyLaboThap/LaboThapPy): six single-phase Darcy
friction factors, the single-phase pressure drop of a straight pipe
(Darcy-Weisbach + hydrostatic term), the three two-phase frictional
correlations (Friedel 1979, Muller-Steinhagen & Heck 1986, Choi-Kedzierski-
Domanski 2001), the two-phase acceleration term (with the homogeneous or the
Zivi void fraction) and the two-phase gravity term. The friction factors are
returned by six separate functions, each with its formula, validity range,
original reference and source module in its comment block; the Reynolds, Froude
and Weber numbers, the two void fractions and the homogeneous two-phase
density are provided as helper functions. It is the first pressure-drop
correlation family of the LaboThapPy triage in the library: the friction factor
of `CSL-0018` (Colebrook-White) was the only one available before.

| | |
|---|---|
| **Category** | Heat transfer › Pressure drop |
| **Fluids** | the correlations are fluid-independent; the demonstration program uses R134a (two-phase), Water (single-phase) and R744 (supercritical CO2) |
| **Size** | 104 equations after analysis (largest block: 1); 22 functions of 3–45 lines |
| **Source** | [`LaboThapPy`](https://github.com/PyLaboThap/LaboThapPy), commit `f03f7f47`, file `labothappy/correlations/pressure_drop/pipe_DP.py` (Apache-2.0 `LICENSE.txt`, MIT `pyproject.toml`); inventory row `LTP-028` of `sources/labothappy/inventory.csv` |
| **Authors** | Elise Neven (the `pipe_DP.py` module); the authors of the correlations are credited in the comment block of each function and in `model.json` |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against LaboThapPy `f03f7f47` (34 values, max deviation 1.0·10⁻¹²) |

## Problem statement

For a pipe (diameter `d_hyd`, roughness `K`, length `L`, inclination `theta`)
carrying a fluid at a known mass flux `G = m_dot/A`, compute the pressure drop:
single phase (Darcy-Weisbach friction plus a hydrostatic term) or two phase
(frictional drop from one of the three correlations, plus the acceleration and
gravity terms). The friction factor itself is a choice: each correlation has
its own validity range, and the user knows the fluid, the roughness and the
geometry.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in the source) |
|---|---|---|---|
| `f_Churchill` | K, d_hyd, Re | f = 8·[(8/Re)¹² + 1/(A+B)^1.5]^(1/12), A = [2.457·ln(1/((7/Re)^0.9 + 0.27·K/d_hyd))]¹⁶, B = (37530/Re)¹⁶ | Re > 0 (all regimes), any K/d_hyd |
| `f_Swamee_Jain` | K, d_hyd, Re | f = 0.25/[log₁₀(K/(3.7·d_hyd) + 5.74/Re^0.9)]² | Re ≥ 5000 (≥ 4000 acceptable), ±2 % of Colebrook |
| `f_Konakov` | Re | f = (1.8·log₁₀Re − 1.5)⁻² | 4·10³ ≤ Re ≤ 3·10⁶, smooth pipes |
| `f_Petukhov` | Re | f = (0.79·ln Re − 1.64)⁻² | 3·10³–10⁴ ≤ Re ≤ 5·10⁶, 0.5 ≤ Pr ≤ 200, smooth pipes |
| `f_Haaland` | K, d_hyd, Re | f = 1/(−1.8·log₁₀[(K/(3.75·d_hyd))^1.11 + 6.9/Re])² | 4·10³ ≤ Re ≤ 10⁸, 10⁻⁶ ≤ K/d_hyd ≤ 0.05 |
| `f_Cheng_CO2` | G, d_hyd, P, h, mu | x_pb = (h − h_LL)/(h_LV − h_LL) from the Banuti (2019) pseudo-boiling bounds; LL/VL: f = 1.5·(1.82·log₁₀Re − 1.64)⁻²; TPL: Fr_VL = G²·x_pb/(ρ²·g·d_hyd), f = 4.379·Re^(−0.388)·Fr_VL^(−0.0167) | d_hyd = 10 mm, G = 496.7–1346.2 kg/m²·s, 7.53–23.51 MPa, horizontal tube, no roughness |
| `T_pseudo_critical_CO2` | P | T_pc = −31.40 + 12.15·p − 0.6927·p² + 0.03160·p³ − 0.0007521·p⁴ (+273.15 K), p = P/1 MPa | 7.5 ≤ p ≤ 14 MPa |
| `dP_pipe_friction` | f, L, d_hyd, G, ρ | ΔP = f·(L/d_hyd)·ρ·v²/2 with v = G/ρ | Darcy-Weisbach |
| `dP_pipe_gravity` | L, ρ, theta | ΔP = g·ρ·L·sin(theta) | — |
| `dP_pipe_single_phase` | f, L, d_hyd, G, ρ, theta | ΔP = friction + gravity | — |
| `dP_Muller_Steinhagen_Heck` | G, x, ρ_l, ρ_v, μ_l, μ_v, d_hyd, L, K | ΔP = G_MSH·(1−x)^(1/3) + ΔP_vo·x³, G_MSH = ΔP_lo + 2(ΔP_vo − ΔP_lo)·x (Swamee-Jain factors of both phases at the total mass flux) | 0 < x < 1; fitted on 9300 measurements, channels of 4–392 mm |
| `dP_Friedel` | G, x, ρ_l, ρ_v, μ_l, μ_v, σ, d_hyd, L, K | ΔP = ΔP_lo·Φ_l², Φ_l² = E + 3.24·F·H/(Fr^0.0454·We^0.035) (Churchill factors, homogeneous density) | separated flow, 0 < x < 1; Φ_l² typically 2–10 |
| `dP_Choi` | G, ρ_su, ρ_ex, x_su, x_ex, μ_l_sat, h_lv_sat, L, d_hyd | Re_fo = G·d_hyd/μ_l_sat, K_f = |x_ex − x_su|·h_lv_sat/(g·L), f_N = 0.00506·Re_fo^(−0.0951)·K_f^0.1554, ΔP = f_N·L·(v_ex + v_su)/d_hyd·G² | evaporation and condensation; R125, R134a, R32, R410A, R22, R407C, R32/R134a |
| `dP_acceleration_two_phase` | G, ρ_l, ρ_v, x_in, x_out, void_model | ΔP = G²·(f(x_out) − f(x_in)), f(x) = x²·v_v/α + (1−x)²·v_l/(1−α) | void_model = 1 homogeneous, 2 Zivi |
| `dP_gravity_two_phase` | L, ρ_l, ρ_v, x_in, x_out, theta | ΔP = g·ρ_h·L·sin(theta), ρ_h at the mean quality | — |
| `dP_pipe_two_phase` | ΔP_f, ΔP_a, ΔP_g | ΔP = friction + acceleration + gravity | — |
| `Re_pipe`, `Fr_pipe`, `We_pipe` | … | Re = G·d_hyd/μ, Fr = G/(√(g·d_hyd)·ρ), We = G²·d_hyd/(σ·ρ) | — |
| `alpha_homogeneous`, `alpha_Zivi` | ρ_l, ρ_v, x | α = 1/(1 + S·(ρ_v/ρ_l)·(1−x)/x), S = 1 resp. (ρ_l/ρ_v)^(1/3) | — |
| `rho_two_phase_homogeneous` | x, ρ_l, ρ_v | ρ = 1/(α/ρ_v + (1−α)/ρ_l) with the homogeneous α | — |

Arguments (SI): `K` absolute roughness `[m]`, `d_hyd` hydraulic diameter `[m]`
(the pipe inner diameter for a round pipe), `Re` `[-]`, `G` mass flux
`[kg/(m²·s)]`, `ρ_l`, `ρ_v` saturated liquid and vapour densities
`[kg/m³]`, `μ_l`, `μ_v`, `mu_l_sat` dynamic viscosities `[Pa·s]`, `sigma`
surface tension `[N/m]`, `L` length `[m]`, `theta` inclination from the
horizontal `[deg]`, `x_su`, `x_ex`, `x_inlet`, `x_outlet` qualities `[-]`,
`h_lv_sat` latent heat `[J/kg]`, `P` pressure `[Pa]`, `h` specific enthalpy
`[J/kg]`.

`dP_pipe_single_phase` takes the friction factor as an argument: the Python
original selects it with a `correlation='…'` string; here the caller calls the
`f_*` function it wants (the same convention as `CSL-0087` for its
method-dispatch functions). The two Python dispatchers
(`pressure_drop_pipe_single_phase`, `pressure_drop_pipe_frictional_two_phase`,
`pressure_drop_pipe_two_phase`) are therefore not translated as such; their
physics is in the three `dP_pipe_*` functions above.

## How to run

```bash
coolsolve ./pipe_pressure_drop_correlations.eescode
```

The demonstration program after the definitions calls every function and solves
without any iteration (`Solver: SUCCESS (0 iterations)`, every equation is
explicit). It is the regression baseline `pipe_pressure_drop_correlations.sol`.

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies the
definitions in a block `{--- Library functions copied from CSL-0130 ---}` and
lists `CSL-0130` in its `related` field.

## Results

Values of the demonstration program (full precision in
`pipe_pressure_drop_correlations.sol`):

| Case | Quantity | Value |
|---|---|---:|
| A — smooth pipe, Re = 10⁵ | `f_Churchill` | 0.0178748 |
| | `f_Swamee_Jain` | 0.0178626 |
| | `f_Konakov` | 0.0177778 |
| | `f_Petukhov` | 0.0179920 |
| | `f_Haaland` | 0.0178249 |
| A2 — K/d_hyd = 5·10⁻³ | `f_Churchill` | 0.0315493 |
| | `f_Swamee_Jain` | 0.0315601 |
| | `f_Haaland` | 0.0311627 |
| B — water, 2 bar, 20 °C, 20 mm × 10 m, 1.0225 kg/s (Re = 6.4995·10⁴, v = 3.2605 m/s) | `dP_pipe_single_phase` (Churchill) | 52 002.2 Pa |
| | (Swamee-Jain) | 51 964.4 Pa |
| | (Konakov) | 51 706.1 Pa |
| | (Petukhov) | 52 411.3 Pa |
| | (Haaland) | 51 849.7 Pa |
| B2 — same pipe at 45° | friction / gravity / total (Churchill) | 52 002.2 / 69 245.9 / 121 248.1 Pa |
| C — R134a, 10 °C, 10 mm × 3 m, 0.05 kg/s, x = 0.5081 | `dP_Friedel` | 35 365.7 Pa |
| | `dP_Muller_Steinhagen_Heck` | 35 825.0 Pa |
| D — same tube, evaporation x = 0.3 → 0.7 | `dP_Choi` | 76 524.3 Pa |
| E — acceleration, x = 0.3 → 0.7 | homogeneous void fraction | 7 886.7 Pa |
| | Zivi void fraction | 7 886.7 Pa |
| | liquid inlet (x_in = 0) | 13 801.6 Pa |
| | vapour outlet (x_out = 1) | 13 801.6 Pa |
| | gravity at +45° / −45° | +427.5 / −427.5 Pa |
| E — total, outlet quality read at h = const. | `x_out` | 0.30957 |
| | friction / acceleration / total (horizontal) | 22 111.3 / 188.7 / 22 300.0 Pa |
| | total at 45° | 22 736.0 Pa |
| F — CO2, 90 bar, 8 mm × 2 m, 0.05 kg/s | `f_Cheng_CO2` at 0 / 30 / 60 °C | 0.0290717 / 0.0256176 / 0.0207664 |
| | `dP_pipe_single_phase` at 0 / 30 / 60 °C | 3 713.9 / 4 256.9 / 10 911.4 Pa |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the six friction
     factors over a Reynolds-number sweep, e.g. f vs Re at K/d_hyd = 0 and 0.005,
     figures/pipe_pressure_drop_correlations_f_re.png -->

## Verification

**Reference.** The LaboThapPy correlations of the local clone, commit
`f03f7f47`, recomputed in a throw-away virtual environment under `work/`
(`pip install -e ~/git/LaboThapPy`, script `work/pipe_dp/ref_pipe_dp.py`): the
34 output values of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
34 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 71
```

(the 71 “only in CoolSolve” variables are the inputs and intermediate
properties of the demonstration program — the mass fluxes, the geometry, the
fluid states, the saturated properties, the dimensionless numbers —; the
reference table holds only the 34 outputs). The largest relative deviation
over the 34 values is **1.0·10⁻¹²** (`dP_F3`, the supercritical-CO2 pressure
drop), i.e. round-off in the double-precision evaluation. Per-value table
(see the `.sol` and `reference_values.csv` for full precision):

| Quantity | LaboThapPy | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `f_Churchill_A` | 0.017874821628 | 0.017874821628 | 1.5e-13 |
| `f_Swamee_Jain_A` | 0.017862577892 | 0.017862577892 | 1.4e-13 |
| `f_Konakov_A` | 0.017777777778 | 0.017777777778 | 1.2e-13 |
| `f_Petukhov_A` | 0.017992027544 | 0.017992027544 | 1.3e-13 |
| `f_Haaland_A` | 0.017824939201 | 0.017824939201 | 2.6e-13 |
| `f_Churchill_A2` | 0.031549341822 | 0.031549341822 | 6.0e-14 |
| `f_Swamee_Jain_A2` | 0.031560131492 | 0.031560131492 | 1.3e-14 |
| `f_Haaland_A2` | 0.031162722510 | 0.031162722510 | 1.0e-13 |
| `dP_B_Churchill` | 52002.196291 | 52002.196291 | 2.8e-13 |
| `dP_B_Swamee_Jain` | 51964.380029 | 51964.380029 | 2.2e-13 |
| `dP_B_Konakov` | 51706.100968 | 51706.100968 | 1.7e-13 |
| `dP_B_Petukhov` | 52411.274669 | 52411.274669 | 3.2e-13 |
| `dP_B_Haaland` | 51849.731666 | 51849.731666 | 1.7e-13 |
| `dP_B2_friction` | 52002.196291 | 52002.196291 | 2.8e-13 |
| `dP_B2_gravity` | 69245.945537 | 69245.945537 | 5.8e-14 |
| `dP_B2_Churchill` | 121248.141828 | 121248.141828 | 3.3e-13 |
| `dP_Friedel_C` | 35365.679715 | 35365.679715 | 4.2e-13 |
| `dP_MSH_C` | 35824.999902 | 35824.999902 | 4.1e-13 |
| `dP_Choi_D` | 76524.274093 | 76524.274093 | 4.4e-13 |
| `dP_acc_hom_E` | 7886.651486 | 7886.651486 | 5.0e-13 |
| `dP_acc_zivi_E` | 7886.651486 | 7886.651486 | 4.9e-13 |
| `dP_acc_x0_E` | 13801.640101 | 13801.640101 | 9.4e-14 |
| `dP_acc_x1_E` | 13801.640101 | 13801.640101 | 9.2e-14 |
| `dP_grav_45_E` | 427.542586 | 427.542586 | 1.1e-13 |
| `dP_grav_m45_E` | −427.542586 | −427.542586 | 1.1e-13 |
| `dP_friction_E` | 22111.279350 | 22111.279350 | 5.5e-13 |
| `x_out` | 0.309569246 | 0.309569246 | 4.9e-14 |
| `dP_acc_E` | 188.673265 | 188.673265 | 9.2e-13 |
| `dP_grav_E_45` | 436.045087 | 436.045087 | 1.5e-14 |
| `dP_total_E` | 22299.952615 | 22299.952615 | 1.5e-13 |
| `dP_total_E_45` | 22735.997702 | 22735.997702 | 5.5e-13 |
| `f_Cheng_CO2_F1/F2/F3` | 0.0290717 / 0.0256176 / 0.0207664 | same | ≤ 1e-12 |
| `dP_F1` / `dP_F2` / `dP_F3` | 3713.882 / 4256.912 / 10911.358 | same | ≤ 1.0e-12 |

**The example of the source was re-run** in the same throw-away virtual
environment (`work/pipe_dp`, the file itself, commit `f03f7f47` of the local
clone) and prints:

```
A) Friction factor at Re=1e5 (smooth pipe):
   Churchill     : f = 0.01779        Haaland : f = 0.01774
   Swamee-Jain   : f = 0.01778        Konakov : f = 0.01769
                                     Petukhov: f = 0.01790
B) Pressure drop at m_dot=1.023 kg/s:  0.4 to 0.8 Pa
C) Two-phase dP at x=0.51 (R134a, T_sat=10 degC): 0.0 to 0.6 Pa
D) Supercritical CO2 dP range over T in [0, 60] degC: min 0.0 Pa, max 0.1 Pa
```

Two things are read from this output and checked against the numbers:

1. **The friction factors of case A are reproduced exactly** by the functions
   of this file when they are evaluated at the Reynolds number of the example's
   own grid, Re = 10²·⁵⁺¹¹¹·(7−2.5)/199 = **102 341.14** (the `argmin` of
   `|logspace(2.5, 7, 200) − 10⁵|` is index 111, not the point Re = 10⁵):
   0.01779 / 0.01778 / 0.01774 / 0.01769 / 0.01790 for
   Churchill / Swamee-Jain / Haaland / Konakov / Petukhov. Our demonstration
   program uses Re = 10⁵ exactly, hence the slightly different values of the
   case-A table above (0.017875 etc.).
2. **The pressure drops of cases B–D of the example are wrong by the pipe
   area**: the example passes `m_dot` [kg/s] where the correlations take the
   mass flux `G = m_dot/A_cross` [kg/(m²·s)] —
   `pressure_drop_pipe_single_phase(AS_1p, pipe_geom_1p, m_dot,
   correlation=corr)` and likewise in cases C and D. Reproducing the example
   exactly with the same library gives 0.8207 / 0.3709 / 0.3640 / 0.3557 /
   0.4743 Pa in case B (the printed 0.8 / 0.4 / 0.4 / 0.4 / 0.5 Pa), 0.588 and
   0.0081 Pa in case C and 0.0012–0.0703 Pa in case D: at Re = 20.4 the pipe
   flow is *laminar* (f ≈ 3.2) and the velocity is 3·10⁴ times too small, so
   the printed drops are 4–5 orders of magnitude below the physical ones. With
   the correct `G = m_dot/A_cross = 3254.8` kg/(m²·s) the same call returns
   Re = 6.4995·10⁴, f ≈ 0.0179 and **52 002 Pa** over the 10 m pipe — the
   Darcy-Weisbach value f·(L/D)·ρv²/2. The demonstration program therefore
   uses `G = M_dot/A`, as the function signature requires, and that is what the
   comparison table above verifies. This is a defect of the *example*, not of
   the correlations; it is reported here so that nobody uses the printed values
   as reference data.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the pipe pressure-drop module of LaboThapPy, the
component library of the ULiège Thermodynamics Laboratory, file
`labothappy/correlations/pressure_drop/pipe_DP.py`, commit `f03f7f47`, with the
helper relations of `labothappy/correlations/properties/dimensionless.py`
(`compute_reynolds`, `compute_froude`, `compute_weber`),
`labothappy/correlations/void_fraction/void_fraction.py`
(`void_fraction_homogeneous`, `void_fraction_zivi`),
`labothappy/correlations/properties/two_phase.py`
(`compute_two_phase_density`) and
`labothappy/correlations/properties/supercritical.py`
(`pseudo_boiling_bounds`, `pseudo_critical_temperature_CO2`).

> LaboThapPy — https://github.com/PyLaboThap/LaboThapPy — ULiège Thermodynamics
> Laboratory. `LICENSE.txt`: Apache-2.0; `pyproject.toml`: MIT. Module author:
> Elise Neven (elise.neven@uliege.be). Please cite the LaboThapPy project and
> the original paper of each correlation.

The scientific authors are credited in the comment block of each function and
in `model.json` (`origin.authors`): Churchill (1977), Swamee & Jain (1976),
Khlapuk, Bezusyak, Volk & Zhang (2021, the Konakov formula as quoted by the
source), Petukhov (1970), Haaland (1983), Cheng, Xu, Cao, Zhou & Liu (2024),
Yang & Yang (2012, pseudo-critical temperature of CO₂), Banuti (2019,
pseudo-boiling bounds), Friedel (1979), Muller-Steinhagen & Heck (1986), Choi,
Kedzierski & Domanski (2001, 1999), Wallis (1969), Collier & Thome (1994).

## Conversion log

- **2026-10-09 — translation (T-FUNC card C-175, inventory row `LTP-028`).**
  One EES `FUNCTION` per correlation, named after the Python function
  (`friction_factor_churchill` → `f_Churchill`, `pressure_drop_friedel` →
  `dP_Friedel`, …), with the formula, the validity range **as quoted in the
  source**, the original paper and the source module, function and commit in
  the comment block. Arguments are the Python arguments, all in SI
  (`Pa·s`, `kg/m³`, `N/m`, `m`, `deg`, `kg/(m²·s)`); the Python `math.log`
  became the EES `LN` and `math.log10` the EES `LOG10`.
- **String dispatchers not translated.** `pressure_drop_pipe_single_phase`,
  `pressure_drop_pipe_frictional_two_phase` and `pressure_drop_pipe_two_phase`
  select the correlation with a `correlation='…'` argument; in EES the caller
  calls the chosen `FUNCTION` directly (same convention as `CSL-0087`).
  `dP_pipe_single_phase`, `dP_pipe_two_phase` keep the physics (sum of the
  frictional, acceleration and gravity terms) and take the friction factor, the
  three terms or the properties as arguments.
- **`void_fraction_model` as a flag.** `pressure_drop_pipe_acceleration_two_phase`
  takes the string `'Homogeneous'`/`None` or `'Zivi'`; it became the integer
  argument `void_model` (1 = homogeneous, 2 = Zivi) and the two branches are
  the existing `alpha_homogeneous` / `alpha_Zivi` functions.
- **Newton's EPS clamps dropped.** The Python module clamps every divisor
  (`max(EPS, …)`, `EPS = 1e-12`) and `compute_reynolds` returns `max(1, …)`;
  these guards only bite outside the validity ranges (Re = 0, zero viscosity,
  x = 0 or 1). In EES they are replaced by explicit branch tests where they
  carry a *physical* meaning — `x = 0` and `x = 1` of the acceleration term,
  which the source also branches on (`f(x) = 1/ρ_l` resp. `1/ρ_v`) — and
  dropped elsewhere. The clamps have no effect on any value of the
  demonstration program.
- **`G_GRAVITY = 9.81` written as the literal `9.81` inside the functions.**
  A variable of the main program is not visible inside a `FUNCTION` body (as in
  EES); the module constant of the source therefore appears literally, with
  its unit in the comment of each line.
- **`T_max` constant of the pseudo-boiling model.** `pseudo_boiling_bounds`
  evaluates the vapour-like anchor `cp_IG = cp(P, T_max)` at the upper
  temperature limit `T_max` of the fluid tables (`AS.keyed_output(iT_max)`);
  CoolSolve has no property function for it, so `T_max_CO2 = 1500` K (the
  CoolProp upper limit of the CO₂ tables) is written as a local constant of
  `f_Cheng_CO2`, with a comment. The other anchors use `P_crit('R744')`,
  `P_triple('R744')`, `temperature('R744', P=p_L, x=0)`, `cp` and `enthalpy`.
- **The Python iteration on the outlet pressure becomes a simultaneous
  equation.** `pressure_drop_pipe_two_phase` reads the outlet quality from
  `AS.update(HmassP_INPUTS, h, p_inlet − ΔP_friction)`; in the demonstration
  program this is the pair of equations `P_out = P_in − dP_friction_E` and
  `x_out = quality(fluid$, P=P_out, H=h_in)` — no iteration, no guess needed.
- **`(P, x)` property pairs.** The saturated liquid/vapour properties that
  `get_saturated_phase_properties` derives from a two-phase state are read
  directly with `density(fluid$, P=P_sat, x=0)`, `viscosity(…, x=1)`,
  `surfacetension(fluid$, T=T_sat, x=x)`, `enthalpy(fluid$, P=P_sat, x=…)`.
  No (T, H) input pair had to be rewritten (decision D11) and no module or
  subprogram was flattened (decision D10).
- **`ELSEIF` written as nested `IF`.** The branch ladder of
  `dP_acceleration_two_phase` is written with nested block `IF … ELSE … ENDIF`
  instead of `ELSEIF` (valid EES, same behaviour): with single-word `ELSEIF`
  this CoolSolve build ignores the `ELSEIF` condition (register §8, card C-111
  observation 1) and silently returns the wrong branch.
- **Sign convention of the gravity term.** The source comments quote a positive
  `theta` as a *downward* flow for `pressure_drop_pipe_single_phase` and as an
  *upward* flow for `pressure_drop_pipe_gravity_two_phase`, while both
  equations are `ΔP = g·ρ·L·sin(theta)`: the two comments cannot both hold.
  The equations are transcribed unchanged (each with a comment reporting what
  the source says); the demonstration program shows the sign (`dP_grav_45_E`
  = +427.5 Pa, `dP_grav_m45_E` = −427.5 Pa).
- **Homogeneous and Zivi acceleration terms are identical** for the
  demonstration case (7886.6515 Pa both). This is not a copy error: with
  f(x) = x²·v_v/α + (1−x)²·v_l/(1−α), the homogeneous and the Zivi models
  (S = (ρ_l/ρ_v)^(1/3)) give the same difference f(x_out) − f(x_in) for these
  densities (checked independently in Python: the two differ by 5·10⁻¹⁵
  relative). The verification table above compares both against LaboThapPy.
- **Level**: equations 104 → 1 point (50–300), largest block 1 → 0,
  functions present → 1, multi-zone no → 0, semi-empirical/off-design no → 0,
  curated guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The demonstration cases are chosen to be realistic, not to stay inside every
  quoted validity range. Case C (R134a at 10 °C in a 10 mm tube at 636.6
  kg/m²·s, x = 0.51) is inside the range of Friedel and of Muller-Steinhagen &
  Heck; the Choi case D is an evaporation from x = 0.3 to x = 0.7 at the same
  saturation temperature, which is the situation the correlation was fitted
  for. The Cheng cases F (90 bar, 8 mm tube, 0.05 kg/s, 0–60 °C, G = 994.7
  kg/(m²·s), Re = 7.0·10⁴–3.7·10⁵) stay inside the stated assumptions of that
  correlation (7.53–23.51 MPa, G = 496.7–1346.2 kg/(m²·s), Re = 6.18·10⁴–5.35·10⁵,
  horizontal tube) except for the tube diameter, 8 mm instead of the 10 mm of
  the source. `Konakov` and `Petukhov` are called with the smooth pipe of case
  B, as they require. The numbers of the *Results* and *Verification* tables
  are a check of the **equations**, not recommended design values.
- **The pseudo-boiling bound `T_plus` depends on the enthalpy reference state**
  of the property backend: `T_plus = (h(P,T_pc) − c_p(P,T_pc)·T_pc)/(c_p(P,T_max)
  − c_p(P,T_pc))` is an enthalpy intercept, and an offset Δh shifts it by
  Δh/(c_p,IG − c_p,pc). `T_minus` and `T_pc` do not depend on it. Consequently
  the pseudo-vapour quality `x_pb` of `f_Cheng_CO2`, and hence the choice of
  its flow regime, does depend on the reference state of the property backend.
  CoolSolve and CoolProp share the same reference, which is why the comparison
  with LaboThapPy (also CoolProp) is exact; a different property library would
  not give the same `f_Cheng_CO2`.
- `f_Cheng_CO2` needs `P_triple('R744')`, which this CoolSolve build evaluates
  correctly (5.179 643 434 477·10⁵ Pa) but announces with a spurious
  *“Unknown function 'P_triple'”* warning (the same call with `P_crit` or
  `T_triple` is silent). The warning is cosmetic and the value is right; the
  branch `p_L < P_triple` of the source is inactive for CO₂ anyway
  (0.1·P_crit = 738 kPa > P_triple = 518 kPa). No gap row was added for it: no
  file of the collection or of `misc/EES_ok.zip` uses `P_triple`, so there is no
  evidence that the spelling is valid EES (rule §6 of the workflow); it is
  reported as an unverified suggestion in the progress log of the card.
- The `surface_tension` property function of CoolSolve is spelled
  `surfacetension` (no underscore); the EES spelling `surface_tension` is
  rejected with *“Unknown function”*.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- **No gap registered for this card**: everything in the file is plain EES
  (`FUNCTION`, block `IF/THEN/ELSE`, `LN`, `LOG10`, property functions) and runs
  in CoolSolve v0.3.0 (`Solver: SUCCESS (0 iterations)`).

## Related models

- `CSL-0018` *pipe_pressure_drop_colebrook*: the single-phase pipe pressure drop
  with the implicit Colebrook-White friction factor solved on a real fluid
  (n-pentane); this file gives the explicit factors and the two-phase terms.
- `CSL-0087` *internal_turbulent_nusselt*: the turbulent Nusselt-number
  correlations that take a Darcy friction factor `fd` as an argument; the `f_*`
  functions of this file are one way of computing it.
- `CSL-0103` *tube_bank_dp_bell_delaware*: the shell-side pressure drop of a
  shell-and-tube exchanger (Kern, Bell-Delaware), i.e. the same pressure-drop
  family on another geometry; a shell-side model pairs it with the pipe
  correlations of this file.
- `CSL-0131` *void_fraction_correlations*: the thirteen void-fraction
  correlations of the same LaboThapPy triage. This file's
  `alpha_homogeneous` and `alpha_Zivi` helper functions are the same two
  relations as its `void_fraction_homogeneous` and `void_fraction_Zivi` (same
  equations, same arguments, kept under both names so that either file can be
  included on its own); the other eleven models — Premoli, Hughmark,
  Lockhart-Martinelli, Graham, Armand-Treschev, Bankoff, Cioncolini-Thome,
  Rouhani-Axelsson, Dix, Woldesemayat-Ghajar and Fauske — are the drift-flux and
  slip-ratio choices available when a two-phase model needs more than the
  no-slip baseline, in particular the vertical and inclined cases the drift-flux
  models were fitted for.
- `CSL-0158` *gas_pipe_insulated_pressure_drop*: a single-phase insulated gas
  pipe with its fittings; it uses the Colebrook factor and would use the
  explicit factors of this file.
- `CSL-0132` *r1233zd_thermal_conductivity*: the thermal-conductivity correlation
  of R1233zd(E) from the same LaboThapPy correlation sweep — the property a
  two-phase R1233zd(E) line model of this file would take for its heat-transfer
  calculations.
- `sources/labothappy` LTP-034 (in-tube heat-transfer correlations): the
  friction factor is an input of Gnielinski and Dittus-Boelter.