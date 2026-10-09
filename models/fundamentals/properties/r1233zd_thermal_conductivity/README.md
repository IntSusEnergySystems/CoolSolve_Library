# Thermal conductivity of R1233zd(E) — Perkins & Huber correlation

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0132`

Two EES `FUNCTION`s giving the thermal conductivity of the refrigerant
R1233zd(E) — `conductivity_R1233zd` (the coefficient set of the original
LaboThapPy code) and `conductivity_R1233zd_published` (the coefficient set of
Table 1 of the paper) — as a function of temperature and pressure. The density
comes from the built-in R1233zd(E) property functions. This is the `LTP-048`
row of the LaboThapPy triage (roadmap card C-177, batch B-12).

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | R1233zd(E) |
| **Size** | 26 equations after analysis (largest block: 1); 2 functions |
| **Source** | [`LaboThapPy`](https://github.com/PyLaboThap/LaboThapPy) commit `f03f7f47` (2026-09-25), file `labothappy/correlations/properties/thermal_conductivity.py` (Apache-2.0); inventory row `LTP-048` of `sources/labothappy/inventory.csv` |
| **Authors** | the correlation: R. A. Perkins and M. L. Huber; the code: the LaboThapPy contributors (see `AUTHORS.txt`) |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against the re-run of the original function (8 values, 0 differ) |

## Problem statement

A heat-transfer model working with R1233zd(E) (the working fluid of many
organic-Rankine and high-temperature heat-pump cycles) needs the thermal
conductivity `k` of the fluid at a given state. The source implements it as a
correlation of the state rather than a table, because no transport property of
this refrigerant is available in the property backend it uses.

## Model

Both functions take `T` (`[C]`) and `P` (`[Pa]`) and return `k` (`[W/m-K]`).
They have the same shape — a dilute-gas term quadratic in the reduced
temperature plus a residual term polynomial in the reduced density:

| | `conductivity_R1233zd` (original) | `conductivity_R1233zd_published` |
|---|---|---|
| dilute-gas coefficients `A_0`, `A_1`, `A_2` | −0.0103589, 0.0308929, 0.000230348 | −0.0140033, 0.037816, −0.00245832 |
| residual pairs `B_i1`, `B_i2` | 5 pairs | 6 pairs |
| `T_c` | 382.52 K | 439.6 K |
| `rho_c` | 489.24 kg/m3 | 480.219 kg/m3 |

`rho = DENSITY('R1233zd(E)', T = T, P = P)` — the same source of density as in
the original (CoolProp). The original wraps this call in a `try`/`except` and
falls back on the saturated-liquid density when the `(T, P)` call fails; EES has
no exception handling and `DENSITY` accepts a state inside the two-phase
region, so the fallback is not needed and is not transcribed.

**Neither function implements the critical enhancement** (Eqs. 7–10 of the
paper), exactly as in the original: near the critical point both underestimate
`k`. The `conductivity_R1233zd_published` variant is the one that reproduces
the published data (see *Verification*); it is the closest match to the
coefficient set the CoolProp transport model now uses for this fluid
(coolprop `dev/fluids/R1233zd(E).json`, blocks `dilute` and `residual`, which
quote the same paper).

## How to run

```bash
coolsolve ./r1233zd_thermal_conductivity.eescode
```

The model solves with `Solver: SUCCESS (0 iterations)` — every equation is
explicit, no `.initials` or `coolsolve.conf` is needed — and
`r1233zd_thermal_conductivity.sol` is the regression baseline. It is a
function library: until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies the two
definitions in a block `{--- Library functions copied from CSL-0132 ---}` and
lists `CSL-0132` in its `related` field.

## Results

The demonstration program evaluates both functions at six states: **A** and
**B** are the two state points of Table 2 of the paper (given there as a
temperature and a density; the pressure is the one of R1233zd(E) at that
temperature and density), **C** to **F** are states of a heat-pump cycle
working with this fluid. `k [W/m-K]`:

| Case | State | `conductivity_R1233zd` | `conductivity_R1233zd_published` | Δ (original vs published) |
|---|---|---:|---:|---:|
| A | 26.85 °C, 1.99864·10⁷ Pa (liquid, ρ = 1308.8 kg/m³) | 0.0990339 | 0.0913456 | +8.4 % |
| B | 171.85 °C, 3.00028·10⁶ Pa (ρ = 168.52 kg/m³) | 0.0304972 | 0.0239922 | +27.1 % |
| C | 5 °C, 1 bar (evaporator outlet) | 0.0964019 | 0.0888095 | +8.6 % |
| D | 0 °C, 1 bar (evaporator inlet) | 0.0980073 | 0.0903687 | +8.5 % |
| E | 40 °C, 10 bar (condenser outlet) | 0.0860569 | 0.0786307 | +9.4 % |
| F | 25 °C, 10 bar (condenser inlet) | 0.0905916 | 0.0831219 | +9.0 % |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): a parametric
     sweep of k against temperature at three pressures (1 bar, 10 bar, 20 MPa)
     for both functions,
     figures/r1233zd_thermal_conductivity_k_T.png -->

The two coefficient sets agree on the shape of the dependence (k falls with
temperature in the liquid, and the residual term dominates at high density) but
the coefficient set of the original sits 8–9 % above the published one in the
liquid and supercritical states and 27 % above it near the critical point.

## Verification

The card names the coefficients of Perkins & Huber (2017) — the same paper as
the EES transport data of this fluid — as the reference, and the source's own
code as the model being translated. Both were checked, in a throw-away virtual
environment under `work/r1233zd_cond/` (`python3 -m venv`, then
`pip install ~/git/LaboThapPy`, which brings CoolProp 8.0.0); the venv has been
deleted with the rest of `work/`. One script, `work/r1233zd_cond/ref_r1233zd.py`,
re-runs the original function at the six demonstration states and writes two
reference files for `../CoolSolve/tools/compare_solution.py`.

**(a) Translation, against the re-run of the original function** — six values of
`k` and the six densities:

```bash
python3 ../CoolSolve/tools/compare_solution.py \
  models/fundamentals/properties/r1233zd_thermal_conductivity/r1233zd_thermal_conductivity.sol \
  work/r1233zd_cond/ref_r1233zd.csv
```

> `8 common variables, 0 differ (rtol=0.001); only in EES: 4; only in CoolSolve: 18`

All eight values are **bit-identical** (maximum relative deviation 0 at the
printed precision: the `.sol` file and the reference CSV carry the same 12–13
significant digits), the two codes performing the same operations in the same
order on the same CoolProp backend. The four variables "only in EES" (`rho_C`,
`rho_D`, `rho_E`, `rho_F`) are the densities the reference script prints but
the demonstration program does not store; the 18 "only in CoolSolve" are the
two functions' internal intermediates and the six `k_published_*` values of the
second function.

**(b) Physics, against Table 2 of the paper** — the two published points are
compared through `k_published_A` (the same command with
`work/r1233zd_cond/ref_paper_A.csv`, which holds the published value 0.091399
W/(m K) at 300 K / 1308.8 kg/m³):

| Point (paper Table 2) | Published `k` | `conductivity_R1233zd_published` | deviation | `conductivity_R1233zd` (original) | deviation |
|---|---:|---:|---:|---:|---:|
| 300 K, 1308.8 kg/m³ (liquid) | 0.091399 | 0.091346 | −0.06 % | 0.099034 | +8.35 % |
| 445 K, 168.52 kg/m³ (near-critical vapour) | 0.026141 | 0.023992 | −8.22 % | 0.030497 | +16.66 % |

`compare_solution.py` prints `1 common variables, 0 differ (rtol=0.001)` for the
first point. At the second point the published value includes the critical
enhancement, which neither function implements (−8.2 % is the size of that
term); the residual contribution of `conductivity_R1233zd` there is also far
from the published value, which is why both functions are shipped: the
coefficient set of the original does not reproduce the paper's data.

### The two coefficient sets differ

The paper fits `k` on the Mondéjar et al. (2015) equation of state, whose
critical point is `T_c` = 439.6 K, `rho_c` = 480.219 kg/m³. The code writes
`T_c` = 382.52 K and `rho_c` = 489.24 kg/m³ and a different set of `A` and `B`
coefficients. Reproducing the paper's Table 1 with the original's `T_c`,
`rho_c` does not close the gap (at 300 K / 1308.8 kg/m³ it gives 0.098814
instead of 0.099034), so the difference is in the `A`/`B` values themselves, not
only in the reducing constants. The original is transcribed unchanged (the
model is `verified` against it); the published set is offered beside it so that
a user needing published-quality values has them.

### CoolProp now has a conductivity model for R1233zd(E)

The inventory row states that CoolProp has none — verified with CoolProp 7.2.0,
where `PropsSI('L', …, 'R1233zd(E)')` raises *Thermal conductivity model is not
available for this fluid*, reproduced here with CoolProp 8.0.0 in the venv. The
CoolProp revision bundled with this CoolSolve build (`dev/fluids/R1233zd(E).json`,
version 8.1.0-dev per `build/CMakeCache.txt`) **does** ship one, from the same
paper, so `CONDUCTIVITY('R1233zd(E)', T = T, P = P)` now evaluates:

| Case | `CONDUCTIVITY` (CoolProp 8.1-dev) | `conductivity_R1233zd_published` | `conductivity_R1233zd` |
|---|---:|---:|---:|
| A | 0.0913947 | 0.0913456 | 0.0990339 |
| B | 0.0260490 | 0.0239922 | 0.0304972 |
| C | 0.0888666 | 0.0888095 | 0.0964019 |
| D | 0.0904173 | 0.0903687 | 0.0980073 |
| E | 0.0787728 | 0.0786307 | 0.0860569 |
| F | 0.0832192 | 0.0831219 | 0.0905916 |

The `published` function agrees with `CONDUCTIVITY` to 0.1 % in the liquid (the
small difference is the critical enhancement, which the CoolProp model adds and
the paper states to be negligible at 300 K) and sits 8 % below it at the
near-critical point B, exactly the missing enhancement. This model therefore
remains useful — it makes the correlation available in any CoolSolve build,
independent of the property backend version, and documents the original's
coefficient set — but the card's premise that CoolProp has no conductivity model
for this fluid no longer holds for the bundled CoolProp.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented)
of `conducticity_R1233zd` from LaboThapPy, file
`labothappy/correlations/properties/thermal_conductivity.py`, commit `f03f7f47`.
LaboThapPy — https://github.com/PyLaboThap/LaboThapPy
Copyright (C) 2025 Universite catholique de Louvain (UCLouvain), Universite de Liege (ULiege),
Universite de Mons (UMONS). Original authors: E. Neven, B. Chaudoir et al. (see `AUTHORS.txt`).
Changes: translated from Python to CoolSolve; the `try`/`except` density fallback dropped;
temperatures expressed in °C (the function adds 273.15, the original takes kelvin); a second
function with the coefficient set of Table 1 of the paper added. Scientific basis:
R. A. Perkins and M. L. Huber, "Measurement and Correlation of the Thermal Conductivity of
trans-1-Chloro-3,3,3-trifluoropropene (R1233zd(E))", *J. Chem. Eng. Data* 62(9): 2659–2665,
2017, doi:10.1021/acs.jced.7b00487 (Eqs. 5–6, Table 1, Table 2).

## Conversion log

- **2026-10-09 — translation**: `conducticity_R1233zd(T, P)` written as an EES `FUNCTION`;
  the Python `try`/`except` density fallback dropped (no exception handling in EES;
  `DENSITY` accepts a two-phase state); the temperature unit converted from kelvin to °C at
  the library convention (`T_K = T + 273.15` inside the function); the `SUM` of powers split
  into five named equations, one per power, so each term is readable in the `.sol`.
  No coefficient was changed.
- **2026-10-09 — second function**: `conductivity_R1233zd_published(T, P)` added with the
  coefficient set of Table 1 of the paper (`T_c` = 439.6 K, `rho_c` = 480.219 kg/m³, six
  residual powers), because the coefficient set of the original does not reproduce the
  published data (8–17 % off, see *Verification*). Not part of the original file; documented
  here and in the function's comment block.
- **2026-10-09 — demonstration states**: the two Table 2 points of the paper are given there
  as `(T, rho)`; the demonstration program takes `(T, P)`, so the pressures were converted
  with the R1233zd(E) property functions (300 K / 1308.8 kg/m³ → 1.99864·10⁷ Pa;
  445 K / 168.52 kg/m³ → 3.00028·10⁶ Pa). Four extra states (C to F) are heat-pump states
  with this fluid, added so that the demo is a usable regression case.
- **Level**: equations 0 (26 < 50), largest algebraic block 0 (≤ 5), structure 1 (two
  functions), multi-zone 0, semi-empirical calibration 0, curated guesses 0 → score 1 →
  **level 1**.

## Limitations and CoolSolve gaps

- The critical enhancement (Eqs. 7–10 of the paper) is not implemented in either function,
  as in the original: both are a few per cent low near the critical point.
- The coefficient set of the original differs from the published one; see *Verification*.
- No CoolSolve gap blocks this model (`missing_features` empty).

## Related models

- `CSL-0131` *void_fraction_correlations*: the void fraction of a two-phase
  heat-transfer fluid, from the same LaboThapPy triage; both take the saturated
  properties of the fluid that R1233zd(E) provides.
- `CSL-0130` *pipe_pressure_drop_correlations*: friction and pressure-drop
  correlations of the same LaboThapPy correlation sweep.
- `CSL-0121` *heat_transfer_fluid_properties*: fluid-property library for the
  secondary and heat-transfer fluids (glycols, therminols); this model covers
  a refrigerant, from a correlation rather than a data sheet.