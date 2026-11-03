# Shell-side heat-transfer coefficient: Kern, Donohue and Bell-Delaware with its J corrections

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0321`

Twenty-two EES `FUNCTION`s for the **heat-transfer coefficient** of the shell side
of a shell-and-tube exchanger with segmental baffles: the crossflow areas and the
hydraulic diameter, the Kern coefficient, the Donohue coefficient, and the
Bell-Delaware method (ideal-bank Colburn factor `ji` from the tabulated
coefficients `a1…a4`, the five correction factors `Jc`, `Jl`, `Jb`, `Jr`, `Js`
computed from the exchanger geometry, and the assembled
`h = h_id·Jc·Jl·Jb·Jr·Js`). No property function is called inside a function:
the caller passes `cp`, `mu`, `mu_w`, `Pr`, `k`, `rho`.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none inside the functions; the demo program uses water (CoolProp) |
| **Size** | 76 equations after analysis (largest block: 1); 22 functions |
| **Source** | LaboThapPy (PyLaboThap), commit `f03f7f47`, file `labothappy/correlations/convection/shell_and_tube_htc.py`; inventory row `LTP-037` |
| **Authors** | Basile Chaudoir (only author of the file in the git history); correlations of D. Q. Kern, K. J. Bell, J. P. Donohue |
| **License** | Apache-2.0 (LaboThapPy `LICENSE.txt`); translation published under the library license |
| **CoolSolve** | 0.4.0 — **verified** against a re-run of the source (47 values, max relative deviation 3.5·10⁻¹³) |

## Problem statement

For a shell fluid of mass flow `m` crossing a tube bundle of outside diameter
`Do` and pitch ratio `pratio` in a shell of inside diameter `Ds` with baffles at
spacing `B`, give the shell-side heat-transfer coefficient. Three levels are
available: Kern's equivalent-diameter correlation, Donohue's correlation on the
geometric mean of the crossflow and window velocities, and the Bell-Delaware
method, which starts from the ideal tube-bank coefficient and multiplies it by
the effects of the baffle window, the leakage, the bypass, the laminar
temperature gradient and unequal end spacings.

## Niche

The library already holds the Bell-Delaware **correction-factor equations** and
the Kern **pressure drop** (`CSL-0103`, from `ht`), the tube-bank Nusselt
numbers (`CSL-0095`) and the TEMA mechanical sizing (`CSL-0110`), but **no shell-side heat-transfer coefficient**. This
model adds what is missing to get from a geometry to `h`: (i) the crossflow
areas, hydraulic diameter and tube pitch relative to the flow for the three
layouts (0°, 45°, 60°); (ii) the Bell-Delaware ideal-bank `ji` with its
`a1…a4` coefficient table interpolated on log10 Re; (iii) the J factors
computed **from the geometry** (window fraction `Fw`, leakage areas `Ssb`, `Stb`,
rows `Ntcc`, `Ntcw`, baffle count) — `CSL-0103` takes `Fc`, `Ssb`, `Stb`, `Fsbp`
as given; (iv) the Kern (McAdams-type) and Donohue coefficients; (v) the
assembly `h_BD`. The nearest model is `CSL-0103`; its `Jl`, `Js` and `Jc` (linear
form) are the same equations, which the demo confirms (below).

## Model

| EES `FUNCTION` | Content |
|---|---|
| `Smax_Kern`, `Dh_Kern`, `Re_Kern`, `h_Kern` | Kern: `Ss = Ds(pT−Do)B/pT`, `De` (square or triangular), `Nu = 0.36·Pr^(1/3)·Re^0.55·(mu/mu_w)^0.14`, `h = Nu·k/De` |
| `Smax_BD`, `Pp_BD` | minimum crossflow area (layouts 0, 45, 60), pitch relative to the flow |
| `SL_Donohue`, `h_Donohue` | window area, `VR = sqrt(VL·VT)`, `Nu = 0.22·Re^0.6·Pr^0.33`, `h = Nu·k/Do` |
| `BD_coef`, `ji_BD` | coefficients `a1…a4` (interpolated on log10 Re, held constant outside 1…1e5), `a = a3/(1+0.14Re^a4)`, `ji = a1·(1.33/pratio)^a·Re^a2` |
| `Fw_BD`, `Jc_BD` | window fraction `Fw = (θ−sinθ)/2π`, `θ = 2·arccos(Ds(1−2Bc/100)/(Dotl−Do))`; `Jc = 0.55+0.72(1−2Fw)` |
| `Stb_BD`, `Ssb_BD`, `Jl_BD` | tube-to-baffle and shell-to-baffle leakage areas; `Jl = 0.44(1−rS)+(1−0.44(1−rS))·exp(−2.2·rL)` |
| `Ntcc_BD`, `Ntcw_BD`, `Jb_BD` | rows crossed; bypass factor with sealing strips (`Cj` 1.35 for Re < 100, else 1.25) |
| `NB_BD`, `Jr_BD`, `Js_BD` | baffle count; laminar correction; unequal end spacing |
| `h_BD` | assembly: `Sm`, `Re = Do·G/mu`, `h_id = ji·cp·G·Pr^(−2/3)·(mu/mu_w)^0.14`, `h = h_id·Jc·Jl·Jb·Jr·Js` |

Units: SI; baffle cut `Bc` in per cent as in the source; tube-layout angle
`layout` ∈ {0, 45, 60} degrees; `method` flag (see below). The `b` coefficients
of the same table (pressure drop) are not used by the heat-transfer coefficient
in the source and are not translated (see `CSL-0103` for the shell-side
pressure drop).

## How to run

```bash
coolsolve ./shell_side_htc.eescode
```

The demonstration program (everything explicit, `Solver: SUCCESS (0
iterations)`, 76 equations) solves: case **A**, the `__main__` example of the
source (water at 3 atm, 53.85 °C bulk, wall 214.41 °C, 150 t/h, 1 m shell, 445
tubes of 27 mm, pitch ratio 1.5, 25 % baffle cut, square layout), Kern and
Bell-Delaware, the latter step by step and through `h_BD`; the **12 cases**
`h_BD_<layout>_<i>` (layouts 0, 45, 60 × mass flows 41.7, 5, 0.3, 0.05 kg/s,
i.e. shell Reynolds numbers 5 to 6400, which exercises the laminar branches of
`Jr`, `Jb`, `Js`); the Donohue coefficient; and the textbook Kern geometry.
`shell_side_htc.sol` is the regression baseline.

## Results

Case A (square layout, `Re_BD = 4503.7`):

| Quantity | Value |
|---|---:|
| Kern: `S_T` / `D_hydro` / `Re_kern` / `h_kern` | 0.2 m² / 0.05035 m / 20446 / **2610.97 W/m²K** |
| Bell-Delaware: `S_m` / `G_s` / `ji` / `h_id` | 0.48690 m² / 85.58 kg/m²s / 0.012374 / 3208.98 W/m²K |
| `Jc` / `Jl` / `Jb` / `Jr` / `Js` | 1.00789 / 0.73800 / 0.99687 / 1 / 1 |
| `h_BD_A` (= `h_BD` function) | **2379.45 W/m²K** |
| Donohue (repaired call, see below) | 1796.37 W/m²K |

12 cases `h_BD` [W/m²K] (`m` = 41.7, 5, 0.3, 0.05 kg/s): layout 0: 2379.4, 487.2,
21.92, 1.735; layout 45: 2756.0, 630.6, 35.95, 1.874; layout 60: 2438.6, 678.0,
41.50, 2.151.

Plausibility: `h_kern/h_BD = 1.10` at the source example; the viscosity ratio
`(mu/mu_w)^0.14 = 1.61` is large because the source takes the "wall" viscosity
of **steam** (487.56 K is above the saturation temperature at 3 atm, CoolProp
phase = gas), as in the source's own example. The very small `h` of the
laminar cases comes from the `Jr` expression of the source (next section).

## Verification

**Source re-run.** The source file was loaded from the local clone
(`f03f7f47`) in a throw-away virtual environment (CoolProp 8.0.0, numpy); its
`__main__` example (Kern and Bell-Delaware with water) and the same function
called for 3 layouts × 4 mass flows were run, the local variables of the two
functions were captured with `sys.setprofile`, and compared with the `.sol`
using `CoolSolve/tools/compare_solution.py`:

```
47 common variables, 0 differ (rtol=1e-09); only in EES: 0; only in CoolSolve: 29
```

Largest relative deviation 3.5·10⁻¹³ (`N_tcc`); the property values (`rho`,
`mu`, `cp`, `k`, `Pr`, `mu_w`) agree with CoolProp from CoolSolve to the same
level, so the properties are not a source of difference. The 29 variables only in
CoolSolve are the inputs. Compared quantities: `S_T`, `D_hydro`, `Re_kern`,
`h_kern`; `S_m`, `G_s`, `Re_BD`, `a_coef`, `j_i`, `h_id`, `F_w`, `F_c`, `J_c`,
`S_tb`, `S_sb`, `J_l`, `P_p`, `N_tcc`, `N_tcw`, `J_b`, `N_B`, `J_r`, `J_s`,
`h_BD_A`, `h_BD_A_fn`, the 12 `h_BD_<layout>_<i>`.

Two further references that are **not** a pure re-run of the source:

- `h_BD_0_4_Jr2` (`method` = 2): compared with the source text patched in the
  throw-away environment at the two places described below (a modified copy of
  the source, not the source itself): same agreement.
- `h_Donohue_A`: the source function stops with a `TypeError` (below), so there
  is no source result. The reference is the source's own `s_max` (6 arguments)
  plus the formula of its commented-out `s_L` with the shell area `π·Ds²/4`,
  evaluated in Python: agreement to the level above.

**Cross-model check with `CSL-0103`** (functions of that file, run in
CoolSolve with the case-A geometry): `Jl_Bell` = 0.7380024576733,
`Jb_Bell` (laminar = 0) = 0.9968693132880, `Jc_Bell(Fc, 2)` = 1.007891006740,
`Js_Bell` = 1, equal to `J_l`, `J_b`, `J_c`, `J_s` of this model to the printed
digits; `Jr_Bell(5.4, 67.3)` = 0.70951, equal to `Jr_BD` with `method` = 2 at
the same inputs (the lower limit 0.4 of `CSL-0103` is not active there).

**Kern geometry, analytic.** For the textbook case (21.25 in shell, ¾ in
tubes on 1 in square pitch, 5 in baffle spacing; `S_T_K`, `D_hydro_K`): the demo
gives 0.0171371 m² = 0.18446 ft² and 0.024070 m = 0.9477 in; the hand
calculation of Kern's equations `a_s = ID·C'·B/(144·PT)` = 21.25·0.25·5/144 =
0.18446 ft² and `De = 4(PT² − πd²/4)/(πd)` = 0.9477 in gives the same numbers.
I recall that Kern's book quotes about 0.18 ft² and 0.95 in for this geometry; that
was **not checked against the book** (no copy available; the cheguide.com page
cited by the source could not be fetched). No independent reference value for
`h` itself (handbook or paper) was checked.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented)
of the shell-side heat-transfer correlations from LaboThapPy, file
`labothappy/correlations/convection/shell_and_tube_htc.py`, commit `f03f7f47`
(functions `s_max_kern`, `s_max`, `d_h`, `shell_htc_kern`, `shell_htc_donohue`,
`bell_delaware_coefs`, `shell_bell_delaware_htc`).

> LaboThapPy - https://github.com/PyLaboThap/LaboThapPy -
> Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université de
> Liège (ULiège), Université de Mons (UMONS), Apache License 2.0. Author of the
> file: Basile Chaudoir (git history: 15 commits, one author); contributors in
> `AUTHORS.txt` of the repository.

Changes: translated from Python to CoolSolve; the property calls of the Python
functions (CoolProp `PropsSI`/`AbstractState`) are replaced by arguments computed
in the demo program; the Python dictionary `params` becomes explicit arguments;
the numpy interpolation of the coefficients becomes a piecewise-linear
interpolation on log10 Re; angles use degrees as CoolSolve does (`arccos`
returns degrees, converted to radians by `·π/180`). Scientific basis cited by
the source: D. Q. Kern, *Process Heat Transfer*, McGraw-Hill, 1950; K. J. Bell,
Delaware method (1963, 1988); the coefficient table and the J formulas are
those of cheguide.com `heat_exchanger_rating` (cited by the source; not
consulted here). Donohue's correlation is attributed in the source to Kern.

## Conversion log

- **`method` flag.** Two expressions of the source look like slips and are kept
  as the default (`method` = 1, needed to reproduce the source); `method` = 2
  gives the usual forms:
  1. `s_max`: the source divides the whole sum `(Ds−Dotl) + (Dotl−Do)(pT−Do)` by
     `p_eff` (the sum mixes m and m², hence is dimensionally inconsistent);
     method 2 divides only the second term: `B[(Ds−Dotl) + (Dotl−Do)(pT−Do)/pe]`.
     At case A this changes `S_m` from 0.2026 m² (method 2) to 0.4869 m²
     (method 1, the source): a factor 2.40.
  2. `J_rl`: the source writes `(10/N_C)*0.18`, whereas `ht` / the HEDH use the power
     `(10/N_C)^0.18` (`Jr_Bell` of `CSL-0103`). At case A geometry `N_C` = 67.3,
     giving 0.027 (source) instead of 0.710, a factor 26. Consequence: with
     `method` = 1 the laminar shell flow (Re < 20) gets a very small coefficient
     (`h_BD_0_4` = 1.735 W/m²K against 45.9 W/m²K with `method` = 2, where the
     `S_m` form changes too). Not verified against the original text of Bell:
     it is a comparison with `ht` and with the dimension check only.
- **Donohue.** `shell_htc_donohue` cannot run in the source (it calls `s_max`
  with 5 of its 6 arguments and `s_L`, which is commented out: reproduced with
  `TypeError: s_max() missing 1 required positional argument: 'tube_layout'`).
  The translation uses `D_OTL` in the call and the formula of the commented-out
  `s_L` with `π·Ds²/4` (the commented text has `π·Ds/4`); the result is a repaired
  version, not the source behaviour. In `h_Donohue` the `method` argument selects
  the `S_T` form.
- **Kern.** `shell_htc_kern` returns `h, Re, Pr` (and mentions the pressure drop in
  its docstring but does not compute it); the translation keeps `h_Kern` and
  `Re_Kern`. `s_max_kern` ignores the layout, `d_h` uses the square form for 0°
  and 45°, as in the source.
- The comments of `s_max` in the source call layout 45 "triangular staggered" and
  60 "squared staggered"; the code and `bell_delaware_coefs` use 45 = rotated
  square and 60 = triangular, which is what is translated.
- Name clash: `pr` (pitch ratio) and `Pr` (Prandtl) are the same variable in
  EES (case-insensitive); the pitch ratio is `pratio`.
- Source functions not translated: none. The `b` columns of the coefficient table
  (`bell_delaware_coefs` returns them, unused by the heat-transfer function).
- Level: 76 equations → 1, largest block 1 → 0, functions → 1, no multi-zone,
  semi-empirical or guesses: score 2 → level 2.

## Limitations and CoolSolve gaps

- Defaults reproduce the source, including the two slips above; use
  `method` = 2 for the usual forms. The J formulas are those of the source,
  without the lower limit 0.4 on `Jr`.
- Layout angles other than 0, 45, 60 give 0 coefficients and a huge `pe`.
- The coefficient table covers 1 ≤ Re ≤ 1e5 and is held constant outside.
- The calling model must copy the functions (`CS-FEAT-IMPORT`, `$INCLUDE
  library:` for functions is not available yet).
- No CoolSolve gap or bug was found or registered.

## Related models

- `CSL-0103` *tube_bank_dp_bell_delaware*: shell-side pressure drop (Kern) and the
  Bell-Delaware factors taking `Fc`, `Ssb`, `Stb`, `Fsbp` as arguments; this model
  computes them from the geometry and adds `ji`, Kern, Donohue and the assembly.
- `CSL-0095` *tube_bank_nusselt*: open tube-bank Nusselt numbers (Zukauskas, ESDU,
  HEDH), the alternative to the `ji` of Bell for the ideal bank.
- `CSL-0330` *curved_duct_htc*: curved-duct single-phase h correlations (helical coil, curved rectangular duct, spiral-plate channel) from the unmerged LaboThapPy branch `origin/Basile_Chaudoir`, another single-phase h function family.
