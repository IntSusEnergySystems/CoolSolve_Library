# Curved-duct single-phase heat-transfer coefficients (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0330`

Seven EES FUNCTIONS returning the convection heat-transfer coefficient h [W/m²-K] of
single-phase flow in curved ducts: helically coiled pipes (all regimes, the
laminar–turbulent transition following the Ito critical Reynolds number
Re_cr = 12730·curv_ratio^0.2), curved rectangular ducts (Dean-number correlation),
straight rectangular ducts (Shah-London polynomial + Gnielinski with linear
interpolation in the transition region) and the single-phase channel of a
spiral-plate (SPHE) heat exchanger. A short demonstration program calls every
function with water data.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | any (properties given as arguments) |
| **Size** | 18 equations (largest block: 1) + 7 FUNCTION definitions |
| **Source** | LaboThapPy, branch `origin/Basile_Chaudoir`, commit `98b78ebd` — https://github.com/PyLaboThap/LaboThapPy/blob/98b78ebda930157e5f51820cd59db13aa3bc210c/labothappy/correlations/convection |
| **Authors** | Basile Chaudoir (ULiège) |
| **License** | Apache-2.0 (original: `LICENSE.txt`; `pyproject.toml` declares MIT); translation published under the library MIT license |
| **CoolSolve** | 0.4.0@2dc1367 — verified (see `verification` field) |

## Problem statement

Return the convection heat-transfer coefficient h [W/m²-K] of single-phase
flow in curved ducts — helically coiled pipes (all regimes, with the
laminar–turbulent transition following the Ito critical Reynolds number),
curved rectangular ducts, straight rectangular ducts with a linearly
interpolated transition region and the single-phase channel of a
spiral-plate (SPHE) heat exchanger — directly usable by ε-NTU or
moving-boundary heat-exchanger models.

## Niche

The library had no h-regime-switching correlation set for curved ducts:

- **CSL-0091** (`internal_laminar_and_curved_nu`) returns **Nusselt numbers only** (h = Nu·k/Dh is
  left to the caller), has **no regime switching** (no Ito critical Reynolds) and other helical
  correlations (Mori-Nakayama, Schmidt factor, Xin-Ebadian; Morimoto-Hotta spiral). This model adds
  the Xhan, Zhang, Di Piazza-Ciofalo helical correlations, the Facao-Oliveira **curved rectangular
  duct**, the Shah-London **polynomial in the aspect ratio** with the **Gnielinski + linear
  interpolation** transition treatment, and returns **h** directly, ready for ε-NTU or
  moving-boundary heat-exchanger models.
- **CSL-0087** (`internal_turbulent_nusselt`) covers straight circular pipes only.
- **CSL-0095** (tube banks), **CSL-0111** (chevron-plate channels) and **CSL-0321**
  (shell-and-tube) are other geometries.
- **CSL-0322** (`pche_htc`) covers straight semicircular PCHE channels, not coiled ones.

The **spiral-plate (SPHE) channel functions** did not exist anywhere in the library; they serve the
charge-sensitive moving-boundary SPHE model of LaboThapPy (`hex_MB_charge_sensitive`, translated as
CSL-0138 for plate geometries).

## Model

Geometry inputs: `Dh` hydraulic diameter [m], `R_curv` coil (mean) radius [m], `L` flow length [m],
`AR` duct aspect ratio [-], `ch_w` SPHE channel width [m]; flow inputs: `G` mass flux [kg/m²-s],
`mu`, `mu_w` viscosities [Pa-s], `Pr` [-], `k` [W/m-K]. All functions return h [W/m²-K].

| Function | Regime logic | Correlations (originals cited in the function blocks) |
|---|---|---|
| `curved_pipe_1P_htc` | Re vs Re_cr = 12730·(Dh/2R_curv)^0.2 (Ito); Re ≥ 1E5 → turbulent | laminar: Xhan (0.01 < cr ≤ 0.1), Zhang (cr > 0.1); transition: Xhan with the Ito friction factor; turbulent: Schmidt factor on the straight-pipe correlation, Di Piazza-Ciofalo for cr > 0.2 |
| `laminar_curved_pipe_1P_htc` | cr ≤ 0.01 → straight pipe | Xhan / Zhang |
| `transition_curved_pipe_1P_htc` | idem | Xhan + Ito f / Di Piazza-Ciofalo |
| `turbulent_curved_pipe_1P_htc` | idem | Gnielinski × Schmidt / Di Piazza-Ciofalo |
| `curved_rect_duct_1P_htc` | Re < 2300; De < 1000 / 1000–1200 / > 1200 | Facao-Oliveira De power law, plateau Nu = 38.5, linear interpolation; Re ≥ 2300 → `curved_pipe_1P_htc` |
| `rect_duct_1P_htc` | Re < 2300 / 2300–10000 / > 10000 | Shah-London polynomial (laminar), Gnielinski (turbulent), linear h interpolation (transition) |
| `gnielinski_pipe_htc` | Re < 2300 / ≥ 2300 | Stephan-Preusser (laminar), Gnielinski |
| `single_phase_spiral_plate_htc` | Re vs Re_cr (Ito) | laminar: 0.023·Re^-0.2·Pr^-2/3 × (1 + 3.5·cr); turbulent: 1.86·Re^-2/3·Pr^-2/3·(ch_w/2R_curv)^(1/6) |

`cp = Pr·k/mu` [J/kg-K] is used by the SPHE correlations, as in the source.

## How to run

```bash
coolsolve ./curved_duct_htc.eescode
```

The demonstration program at the end of the file is the main program; to use the functions in
another model, copy the FUNCTION blocks (CoolSolve `$INCLUDE library:…` is planned,
`CS-FEAT-IMPORT`). No guesses needed (explicit equations, 0 iterations).

## Results of the demonstration program

Water at ≈ 50 °C (mu = 5.47E-4 Pa-s, Pr = 3.55, mu_w = 5.0E-4 Pa-s, k = 0.643 W/m-K, L = 2 m):

| Case (branch exercised) | h [W/m²-K] |
|---|---:|
| `h_cp_lam_xhan` — coil Dh = 0.01 m, G = 200, R_curv = 0.1 (Re = 3656 < Re_cr = 6993, cr = 0.05) | 2082.14 |
| `h_cp_lam_zhang` — R_curv = 0.0333333 m (cr = 0.15 > 0.1) | 1937.09 |
| `h_cp_straight` — R_curv = 1 m (cr = 0.005 ≤ 0.01, straight-pipe fallback) | 1490.40 |
| `h_cp_tr_xhan` — G = 500 (Re = 9141, transition band) | 904.59 |
| `h_cp_turb_schmidt` — G = 1000 (Re = 18282, cr ≤ 0.2: Schmidt factor) | 1364.60 |
| `h_cp_turb_dipiazza` — G = 10000, R_curv = 0.02 (Re = 182815 ≥ 1E5, cr = 0.25) | 11256.53 |
| `h_crd_lam` — curved rect. Dh = 0.02 m, G = 50, R_curv = 0.3 (De = 334) | 563.60 |
| `h_crd_turb` — G = 1000 (Re = 36563 → `curved_pipe_1P_htc`) | 912.47 |
| `h_rd_lam` — rect. duct Dh = 0.01 m, AR = 0.5, G = 82.05 (Re = 1500) | 217.90 |
| `h_rd_tr` — G = 273.5 (Re = 5000, interpolation) | 873.46 |
| `h_rd_turb` — G = 1094 (Re = 20000, Gnielinski) | 7423.62 |
| `h_sphe_lam` — SPHE Dh = 0.008 m, R_curv = 0.1, ch_w = 0.002, G = 205.125 (Re = 3000) | 1944.73 |
| `h_sphe_turb` — G = 1367.5 (Re = 20000) | 2873.34 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7) -->

## Verification

The source functions of the **unmerged branch `origin/Basile_Chaudoir` (commit `98b78ebd`)** were
re-run in a throw-away virtualenv (`pip install` of a clone of the branch kept under `work/`;
numpy 2.x, scipy, CoolProp) with exactly the inputs of the demonstration program
(`work/curved_duct_htc/ref_run.py`, deleted with the work folder). `compare_solution.py`:

> 13 common variables, 0 differ (rtol=0.001)

Largest relative deviation **2.92e-13** (`h_cp_straight`), i.e. round-off only. Two cases document
the two source fixes (see conversion log):

| Case | Literal source | Shipped (fixed) |
|---|---:|---:|
| `h_crd_lam` (curv_ratio typo) | 301.097 | 563.599 |
| `h_crd_turb` (typo has no effect in the turbulent path) | 912.469 | 912.469 |

The literal values are the output of the unmodified branch functions; the fixed values were
recomputed with the same one-character corrections applied in Python. No published reference values
exist for these correlations (the papers are cited in the function blocks); the agreement with the
source implementation is the verification.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented) of
`spiral_ducts_htc.py`, `rectangular_duct.py`, `spiral_plate_htc.py` and the `gnielinski_pipe_htc`
helper of `pipe_htc.py` from **LaboThapPy**, branch `origin/Basile_Chaudoir`, commit `98b78ebd`
(unmerged at the time of translation; the pinned main commit of the other models stays `f03f7f47`).

> LaboThapPy — https://github.com/PyLaboThap/LaboThapPy
> Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université de Liège (ULiège),
> Université de Mons (UMONS). Author of the translated files (git history, branch
> `origin/Basile_Chaudoir`): B. Chaudoir (see AUTHORS.txt). License: Apache-2.0 (`LICENSE.txt`;
> `pyproject.toml` declares MIT — both permissive, see sources/labothappy/README.md).

Scientific sources of the correlations (as cited in the source docstrings): Sigalotti,
Alvarado-Rodríguez & Rendón, *Fluid Flow in Helically Coiled Pipes*, 2023 (Ito critical Reynolds,
Xhan); Zhang et al. (large-curvature laminar); Di Piazza & Ciofalo, Int. J. Heat Mass Transfer 53,
2010; Schmidt, Chemie-Ing.-Technik 39, 1967 (factor as given by Nellis & Klein, *Heat Transfer*,
2009); Façao & Oliveira (curved rectangular duct); Shah & London, *Laminar Flow Forced Convection
in Ducts*, Academic Press, 1978; Gnielinski, Int. Chem. Eng. 16, 1976; Stephan & Preusser (laminar
entry region).

## Conversion log

- **2026-11-02 — translation** (T-FUNC card C-480, inventory row LTP-078): Python functions → EES
  FUNCTIONs, one per source function, same names and argument order; SI units throughout (the
  source is already SI: Pa-s, W/m-K, kg/m²-s, m — no unit conversion). Comments paraphrase the
  source docstrings/comments; `np.sqrt` → `SQRT`, `np.log10` → `LOG10`, `**` → `^`.
- **2026-11-02 — dead code removed**: `gnielinski_pipe_htc` computes a Sieder-Tate Nu for
  Re > 10000 that its control flow then overwrites with Gnielinski (the second test in the Python
  is an `if`, not `elif`); only the effective physics is translated, `mu_w` stays an (unused)
  argument as in the source.
- **2026-11-02 — genuine error fixed (impact on results)**: `curved_rect_duct_1P_htc` computes
  `curv_ratio = Dh/2*R_curv` (= Dh·R_curv/2, dimensionally wrong); the dimensionally consistent
  `Dh/(2*R_curv)` is shipped. Impact: laminar case of the demo 301.097 → 563.599 W/m²-K; no effect
  on the turbulent path (which passes `R_curv` to `curved_pipe_1P_htc`, correct in the source).
- **2026-11-02 — genuine error fixed (no physics change)**: `rect_duct_1P_htc` calls
  `gnielinski_pipe_htc` without taking the first element of the returned `(hConv, Re, Pr)` tuple:
  its turbulent branch returns a tuple and its transition branch raises `TypeError` (verified on
  the branch). The scalar `hConv` is translated, so the transition interpolation (unreachable in
  the literal source) works.
- **Level**: equations 18 (< 50 → 0), largest block 1 (≤ 5 → 0), functions present (→ 1), no
  multi-zone discretisation (→ 0), semi-empirical correlations (→ 1), explicit numerics (→ 0);
  score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The correlations are valid in the ranges of the original papers; the source only warns
  (Gnielinski: 0 < Re < 1E6, 0.1 < Pr < 1000) and does not enforce ranges.
- The 1000 ≤ De ≤ 1200 interpolation branch of `curved_rect_duct_1P_htc` and the De > 1200 plateau
  need curvature ratios > 0.43 (coil radius ≈ Dh): not reachable with physical coil geometry,
  therefore not exercised numerically (code follows the source).
- The wall-Prandtl correction `(Pr/Pr_w)^0.11` of the Di Piazza-Ciofalo form is commented out in
  the source and is not implemented, as in the original.
- No CoolSolve gap blocks this model (`missing_features` empty).

## Related models

- CSL-0087 (`internal_turbulent_nusselt`): turbulent Nusselt numbers of straight circular pipes
  (Dittus-Boelter, Gnielinski family…), complemented here for curved geometries.
- CSL-0091 (`internal_laminar_and_curved_nu`): Nu-only library for laminar/non-circular/curved
  ducts; nearest model, different correlations and no regime switching (see *Niche*).
- CSL-0095 (`tube_bank_nusselt`): external flow across tube banks.
- CSL-0096 (`plate_hx_heat_transfer`): single-phase ht Nusselt/correlation family of the chevron-plate channel (ht triage).
- CSL-0111 (`plate_hx_correlations`): chevron-plate channels (single-phase and condensation).
- CSL-0138 (`hex_MB_charge_sensitive`): moving-boundary heat exchanger that consumes this
  correlation family in LaboThapPy.
- CSL-0321 (`shell_side_htc`): shell-and-tube exchanger correlations.
