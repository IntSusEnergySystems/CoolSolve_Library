# UA part-load scaling after Cecchinato et al. (2010)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0315`

Function library for the part-load scaling of the overall conductance `UA` of a
heat exchanger, as implemented in TESPy for the `UA_cecchinato_hc` parameter
group: the conductance at part load follows from the design conductance, the
mass-flow ratios of the two sides, one Reynolds exponent per side and the
product of the side heat-transfer-coefficient ratio and area ratio. The main
program evaluates the factor at the points of the TESPy tests and applies it to
a sectioned steam condenser cooled by air (design, then off design).

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Water (condensing steam), Air |
| **Size** | 230 equations after analysis (largest block 93) + 4 `FUNCTION`s |
| **Source** | [TESPy](https://github.com/oemof/tespy) commit `19425523`, `src/tespy/components/heat_exchangers/sectioned.py` (`UA_cecchinato_func`, `_UA_cecchinato_residual`); inventory row `TSP-032` |
| **Authors** | Francesco Witte and the TESPy contributors (code); L. Cecchinato, M. Chiarello, M. Corradi (law) |
| **License** | MIT (TESPy MIT, translation under the library licence, decision D3) |
| **CoolSolve** | 0.4.0@9768373: **verified** against a re-run of the TESPy doctest and tests (26 values, max deviation 1.35·10⁻⁵) |

## Niche

The library has UA models that rate a heat exchanger at one point or scale it
with *characteristic lines* (`CSL-0137`, interpolation tables `f(m/m_design)`)
or recompute it from geometry and correlations (`CSL-0128`). The
Cecchinato law is a different, analytic and two-side scaling: UA is rescaled
from design data alone, with four physical constants (two Reynolds exponents,
`alpha_cold/alpha_hot`, `A_cold/A_hot`) and no table. It was absent from the
library: a grep of `models/` for "Cecchinato" only finds the compressor
polynomial of the same paper (`polynomial_compressor_en12900`,
`copeland_catalogue_correlation`), not this law. `CSL-0138` is the
moving-boundary model that this law can be applied to.

## The functions

| Function | Content |
|---|---|
| `fUA_Cecchinato(m_ratio_hot, m_ratio_cold, re_exp_hot, re_exp_cold, alpha_ratio, area_ratio)` | `f_UA = UA/UA_ref = (1 + x)/(m_ratio_cold^(-re_exp_cold) + x*m_ratio_hot^(-re_exp_hot))`, `x = alpha_ratio*area_ratio`; both ratios bounded below by 1E-6 as in TESPy |
| `UA_series_resistance(alpha_hot, area_hot, alpha_cold, area_cold)` | `1/(1/(alpha_hot*A_hot) + 1/(alpha_cold*A_cold))`, the conductance the law is derived from (not a TESPy function) |
| `LMTD_section(td_a, td_b)` | logarithmic mean of the two temperature differences of a section, arithmetic mean when equal |
| `h_grid(j, h_ex, h_f, h_g, h_su, n3, n2, n1)` | hot-side enthalpy at section boundary `j` (equal enthalpy steps in the subcooled, two-phase and superheated zone) |

**Meaning of the arguments (as in TESPy).** `hot` is side 1 of the exchanger,
`cold` side 2; `alpha_ratio = alpha_cold/alpha_hot` and `area_ratio =
A_cold/A_hot` are the values at the design point; the mass-flow ratios are
`m/m_design` of the inlets. In TESPy the residual `0 = UA_ref*f_UA − Σ UA_i` is
what makes the off-design duty depend on the law; here the same equation is
written in Part D.

**Derivation (analytic, not from the original).** With `UA = 1/(1/(α_c A_c) +
1/(α_h A_h))` and `α_side = α_side,ref·(m/m_ref)^Re_side` (the exponent is the
Reynolds exponent, `Re ~ m`), dividing by the reference conductance gives the
formula above with `x = (α_c,ref A_c)/(α_h,ref A_h)`. Limits: `x → ∞` gives
`f_UA = (m_hot/m_ref)^Re_hot` (the hot side controls), `x → 0` gives
`f_UA = (m_cold/m_ref)^Re_cold`. I did not read the paper (not accessible
here); the formula is taken from the TESPy source and docstring, and the
derivation above only shows that it is the series-resistance law.

## Main program

* **Part A.** `f_UA` at the off-design points of the TESPy
  `SectionedHeatExchanger` doctest (`area_ratio = 20`, `alpha_ratio = 1e-2`,
  `re_exp_hot = 0.8`, `re_exp_cold = 0.55`) for hot flows 0.5, 0.6, 0.8, 1.2.
  The cold flow ratio is the one TESPy solved (not an input of the law).
* **Part B.** `f_UA` for the three `MovingBoundaryHeatExchanger` tests
  `test_..._offdesign_cecchinato_condenser/_new_api/_evaporator`
  (R410A condenser with air, water-cooled R410A evaporator; parameters
  21.64/8.4e-3/0.8/0.55 and 1/1.013/0.5/0.5) at their reduced-duty points.
* **Part C.** The law from the two resistances with illustrative
  `alpha_h = 2000 W/m²-K`, `A_h = 5 m²` (only the ratios matter): `f_C − f_A3 = 2.2e-16`.
* **Part D.** The doctest condenser. Water, 1 kg/s, 15 K above the dew line at the
  inlet, 5 K subcooled at the outlet, no pressure drop, air 15 → 25 °C at 1 bar.
  *Design* (suffix `_1`): the pinch of 5 K (at the dew-line boundary, where the
  doctest `td_pinch` sits, checked by `DT_min_1 = MIN(dT_1[0..13]) = 5`) fixes the
  condensing pressure; `UA_1` is the sum of the section conductances.
  *Off design* (suffix `_2`): hot flow 0.8 kg/s, the unknown is the condensing
  pressure, closed by `UA_sum_2 = UA_1*f_UA_2` with the air flow ratio solved
  from the energy balance. `Q_dot` is positive for the heat released by the hot
  side (TESPy: negative).
  The sections are 6 + 1 + 6 equal-enthalpy steps of the subcooled, condensing
  and superheated zones; TESPy uses 50 equal-heat sections plus the phase
  boundaries (52). A run with 3 + 1 + 3 sections gives `UA_1` 273 451.7 W/K
  against 273 452.2 W/K with 6 + 1 + 6, so the discretisation is converged to
  2·10⁻⁶; the remaining 1.35·10⁻⁵ difference to TESPy was not further analysed.

A `.initials` file is shipped: without guesses for the pinch block (condensing
pressure, duty, section enthalpies) the Newton solver stopped in a line-search
failure in my first run.

## Verification

Re-run of the TESPy sources in a throw-away virtual environment
(`python3 -m venv`, `pip install -e ~/git/tespy`: TESPy 0.11.3.dev0,
commit `19425523`, CoolProp 8.0.0), deleted at the end of the card:

1. the `SectionedHeatExchanger` class doctest (design; `UA_cecchinato_hc` off
   design with hot flow 0.8, 0.5, 0.6, 1.2 kg/s);
2. the three `MovingBoundaryHeatExchanger` Cecchinato tests. They are skipped
   without REFPROP, so I re-ran them with `REFPROP::R410A` replaced by
   CoolProp `R410A` (HEOS) in my own script (`run_mb.py`), same inputs. The
   original pinch assertions are 7.61134 K (condenser) and 4.662423 K
   (evaporator); the HEOS run gives 7.611332 and 4.662363 K, so the two runs
   are consistent, but the original assertions themselves were not executed. Each
   run prints the mass-flow ratios and `UA/UA_design`; TESPy's own test asserts that this
   equals the formula, which is what Part B reproduces.

The values were written to a reference CSV and compared with

```bash
python3 ../CoolSolve/tools/compare_solution.py ua_cecchinato_partload.sol reference.csv --all
# 26 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 204
```

| Quantity | TESPy | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `f_UA` hot flow 0.5 / 0.6 / 0.8 / 1.2 (A1..A4) | 0.662684 / 0.738773 / 0.876393 / 1.113435 | idem | ≤ 3.8e−13 |
| `f_UA` condenser / evaporator test (B1, B2) | 0.927695 / 0.918906 | idem | ≤ 2.9e−11 |
| `P_h_1` [Pa] (design) | 4218.999 | 4218.999 | 1.9e−12 |
| `Q_dot_1` [W] / `M_dot_c_1` [kg/s] | 2 479 524 / 246.4429 | idem | ≤ 2.0e−10 |
| `UA_1` [W/K] | 273 455.9 | 273 452.2 | 1.35e−05 |
| `DT_min_1` [K] | 5 | 5 | 0 |
| `P_h_2` [Pa] (off design, 0.8 kg/s) | 4051.130 | 4051.119 | 2.7e−06 |
| `Q_dot_2` [W] / `M_dot_c_2` [kg/s] | 1 984 950 / 197.2866 | idem | ≤ 4.5e−08 |
| `UA_sum_2` [W/K] | 239 654.7 | 239 651.5 | 1.35e−05 |
| `f_UA_2` = `UA_ratio_2` | 0.876393 | 0.876393 | 2.0e−08 |
| `DT_min_2` [K] | 4.29505 | 4.29510 | 1.2e−05 |

The doctest prints `round(Q/Q_design, 2) = 0.8`, `round(UA/UA_design, 2) = 0.88`,
`round(td_pinch, 2) = 4.3` (off design) and `round(UA) = 273456` (design). The model gives
0.8005, 0.8764 (0.88), 4.295 (4.3) and 273 452: the first three
reproduced, the last differs by 4 W/K. The mass-flow ratios of Part A/B
are TESPy results used as inputs (not independent). The paper values were **not**
checked. Comparisons with TESPy stop at its own numbers: no check against measured data.

The CoolSolve water states match those of TESPy (hot inlet and outlet enthalpies
agree to ≤ 2e−06, `compare_solution.py` rows `h_su_*`, `h_ex_*`), and so do the air
flows (`M_dot_c_*`, ≤ 4.5e−08).

## Limitations

* The law needs the design state: `UA_ref`, the design mass flows, and the four
  constants; it is meaningful only where `alpha ~ m^Re` holds on each side
  (no phase-change regime shift in the coefficients).
* The sectioned UA of Part D is for a counterflow exchanger with a pure hot
  fluid and air; the pinch is placed at the dew-line boundary (it is the
  minimum of the temperature differences for the doctest data, checked in the
  results, but not for any other data set).
* Convergence of the pinch block depends on the shipped `.initials`.
* No CoolSolve gap or bug was found; nothing was added to the gap register.

## Source and attribution

* TESPy, F. Witte and the TESPy contributors, <https://github.com/oemof/tespy>,
  commit `19425523ff7ecd67b36e7b90efe04a9480a9ebe3`, MIT licence, files
  `src/tespy/components/heat_exchangers/sectioned.py` (`UA_cecchinato_func`,
  `_UA_cecchinato_residual`, class docstring with the doctest),
  `src/tespy/components/heat_exchangers/base.py` (`_calc_lmtd_per_section`),
  `tests/test_components/test_heat_exchangers.py`.
* L. Cecchinato, M. Chiarello, M. Corradi, *A simplified method to evaluate the
  seasonal energy performance of water chillers*, Int. J. Thermal Sci. 49 (2010)
  1776–1786, doi:10.1016/j.ijthermalsci.2010.04.010 (law cited via TESPy).

## Conversion log

* Python solver plumbing (design/off-design switch, `design_path`) became two
  equation sets `_1`/`_2` in one file; the `max(m_ratio, 1e-6)` bound is kept.
* The 52 TESPy sections became 13 sections on a zone-wise enthalpy grid
  (`h_grid`), because the number of sections changes with the phase
  boundaries and a `DUPLICATE` range must be fixed.
* The doctest pinch spec `td_pinch = 5` is written as the temperature difference at the
  dew-line boundary (`dT_1[7]`); the global minimum is output as `DT_min_1`.
* TESPy's smoothed section LMTD is replaced by the exact `LMTD_section`
  (identical for positive temperature differences, as here).
* Sign: `Q_dot` is the heat released by the hot side (TESPy: negative).
* No (T, h) property call or MODULE was needed.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): f_UA versus hot-side mass-flow ratio -->

## Related models

* `CSL-0137` *hx_lmtd_ua*: the other TESPy off-design UA law, characteristic lines.
* `CSL-0138` *hx_moving_boundary_bell*: moving-boundary exchanger to which the law is applied in TESPy.
* `CSL-0014` *hx_constant_pinch*: three-zone condenser sized by an imposed pinch.
* `CSL-0127` *hx_constant_effectiveness_discretised*: discretised exchanger with pinch.
* `CSL-0013` *heat_pump_basic_tespy*: TESPy tutorial cycle (same source library).

## How to run

```bash
coolsolve ./ua_cecchinato_partload.eescode
```
