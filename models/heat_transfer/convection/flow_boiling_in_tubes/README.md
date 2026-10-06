# Flow and film boiling inside tubes: heat-transfer coefficients

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0098`

Ten EES `FUNCTION`s returning the two-phase (flow-boiling) heat-transfer
coefficient `h_tp` of a fluid flowing and boiling inside a tube, in W/m²/K:
five film-boiling / flow-boiling correlations from `ht` (Lazarek-Black, Li-Wu,
Sun-Mishima, Thome, Yun-Heo-Kim) and three convective + nucleate ones (Chen with
the Edelstein and the Bennett forms, Liu-Winterton), plus the two correlations
that `ht` does **not** have and that this model takes from the ThermoCycle
Modelica library, **Shah 1982** and **Gungor-Winterton 1987** (inventory row
`THC-004`). Every function takes the mass flow rate, the quality (where the
correlation needs it), the tube diameter and the liquid and vapour properties as
**arguments**: no property function is called inside a function, so the calling
model passes the properties itself. The file is the layout set by `CSL-0087`:
one `FUNCTION` per correlation, a comment block per function with the formula,
the validity range, the original paper and the `ht` (or ThermoCycle) module,
function, version and commit, and a demonstration program calling every
correlation.

## Problem statement

For a given mass flow rate `m`, vapour quality `x`, tube diameter `D`, wall heat
flux `q` (or wall excess temperature `Te`) and liquid/vapour properties, compute
the heat-transfer coefficient of the tube wall in the two-phase (boiling) flow
regime. Ten historical correlations are available for that, each with its own
validity range and its own combination of single-phase convection and nucleate
or film boiling; the choice between them is left to the user, who knows the
fluid and the geometry.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `h_Lazarek_Black` | m, D, mul, kl, Hvap, q/Te | h_tp = 30·Re_lo^0.857·Bg^0.714·kl/D | x 0–0.6, Re_lo 860–5500, G 125–750 kg/m²/s, q 1.4–38 W/cm², D = 3.1 mm, R113 data |
| `h_Li_Wu` | + x, rhol, rhog, sigma | h_tp = 334·Bg^0.3·(Bo·Re_l^0.36)^0.4·kl/D | D_h 0.19–3.1 mm, 12 fluids, 18 data sets |
| `h_Sun_Mishima` | m, D, rhol, rhog, mul, kl, Hvap, sigma, q/Te | h_tp = 6·Re_lo^1.05·Bg^0.54 / [We_l^0.191·(rhol/rhog)^0.142]·kl/D | D_h 0.21–6.05 mm, 11 fluids, 2501 points |
| `h_Thome` | + mul, mug, kg, Cpl, Cpg, sigma, Psat, Pc, q | hydrodynamic slug model: h = (t_l/tau)·h_l + (t_film/tau)·h_film + (t_dry/tau)·h_g | 7 studies, 7 fluids, D_h 0.7–3.1 mm, q 0.5–17.8 W/cm², x 0.01–0.99, G 50–564 kg/m²/s |
| `h_Yun_Heo_Kim` | m, x, D, rhol, mul, Hvap, sigma, q/Te | h_tp = 136876·(Bg·We_l)^0.1993·Re_l^−0.1626 | none quoted |
| `h_Chen_Edelstein` | m, x, D, rhol, rhog, mul, mug, kl, Cpl, Hvap, sigma, dPsat, Te | h_tp = S·h_nb + F·h_sp,l, F = (1+X_tt^−0.5)^1.78, S = 0.9622 − 0.5822·atan(Re_l·F^1.25/6.18·10⁴) | none quoted |
| `h_Chen_Bennett` | same | as above with F = [(Pr_l+1)/2]^0.444·(1+X_tt^−0.5)^1.78 and S = [1−exp(−F·h_sp,l·X₀/kl)]/(F·h_sp,l·X₀/kl) | none quoted |
| `h_Liu_Winterton` | m, x, D, rhol, rhog, mul, kl, Cpl, MW, P, Pc, Te | h_tp = √[(F·h_l)² + (S·h_nb)²] | none quoted |
| `h_Shah_1982` | m, x, D, q, rhol, rhog, mul, kl, Cpl, i_fg, vertical | h_tp = psi·h_l, psi from Co, Bo, Fr_l and the Eq. 6–14 of the chart correlation | saturated flow boiling in a tube (as in the original) |
| `h_Gungor_Winterton_1987` | same without `vertical` | h_tp = h_l·[1 + 3000·Bo^0.86 + 1.12·(x/(1−x))^0.75·(rhol/rhog)^0.41]·Term2 | turbulent two-phase flow (as in the original) |

Arguments: `m` [kg/s] mass flow rate, `x` [-] vapour quality, `D` [m] tube
(hydraulic) diameter, `q` [W/m²] wall heat flux, `Te` [K] wall excess
temperature (T_wall − T_sat), `dPsat` [Pa] difference between the saturation
pressure at the wall temperature and at the saturation temperature, `i_fg` [J/kg]
latent heat of vaporization, `rhol`/`rhog` [kg/m³] liquid and vapour densities,
`mul`/`mug` [Pa·s] viscosities, `kl`/`kg` [W/m/K] thermal conductivities,
`Cpl`/`Cpg` [J/kg/K] heat capacities, `Hvap` [J/kg] heat of vaporization,
`sigma` [N/m] surface tension, `Psat`/`P`/`Pc` [Pa] saturation, fluid and critical
pressure, `MW` [g/mol] molar mass, and the flags `by_Te` (1 = Te given, 0 = q
given) and `vertical` (1 = vertical flow, 0 = horizontal flow).

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`** (or the original, for the two ThermoCycle
correlations), (iii) the original paper or book and (iv) the `ht` module,
function, version and commit it was taken from — for `h_Shah_1982` and
`h_Gungor_Winterton_1987`, the ThermoCycle Modelica file (and the `ht`
correlations they reuse).

### Conventions of the translation

* **Heat flux or excess temperature.** In `ht`, `Lazarek_Black`, `Li_Wu`,
  `Sun_Mishima`, `Thome` and `Yun_Heo_Kim` take `q` **or** `Te` (two optional
  Python arguments). EES has no optional arguments: both are mandatory and the
  `by_Te` flag selects the form. The `Te` forms of `ht` are the algebraic
  inversions of the `q` forms (derived there with sympy), so both are reproduced
  literally, with the rational exponents of `ht` (`71/143`, `357/143`,
  `857/286`, `500/143`, `10/7`, `3/7`, `50/23`, `27/23`, `10000/8007`).
* **`h_Thome` with a prescribed excess temperature.** `ht` solves an inner
  equation for the heat flux (`to_solve_q_Thome`, a secant iteration). EES has
  no iteration inside a function body, so `h_Thome` takes `q` only and the caller
  adds the heat flux as an unknown with the equation `q = h_Thome(...)*Te` —
  exactly the equation the secant solves. The demonstration program does this
  (case B) and needs one initial guess (`q_Thome_Te_B = 3E6` in the `.initials`).
* **Correlations of other files written out in the body.** The single-phase
  coefficients are the Dittus-Boelter correlation (`Nu_Dittus_Boelter` and
  `Nu_Gnielinski` of `CSL-0087`) and the pool-boiling coefficients are
  Forster-Zuber and Cooper (`h_Forster_Zuber` and `h_Cooper` of `CSL-0088`).
  CoolSolve cannot import the functions of another library file yet
  (`CS-FEAT-IMPORT`), so they are written out as local equations with a comment
  giving the model and function they come from — the same convention as the
  Dittus-Boelter coefficient in `h_Shah` of `CSL-0089`. The function names of
  this file are unique in the library.
* **`tr_factor_Richter2`** is the smooth transition function (weight from 0 at
  `start` to 1 at `stop`, two continuous derivatives) that ThermoCycle uses to
  blend the branches of Shah 1982; it is written as an EES `FUNCTION` of order
  2 (Richter 2008, p. 68 ff). Its three branches are nested `IF … THEN / ELSE`
  blocks (one `ENDIF` each), not an `ELSEIF` chain.
* **Constants and functions.** `pi` is not resolved inside a `FUNCTION` body in
  CoolSolve (`CS-BUG-PI-FUNCTION`, silent, evaluates as 1), so `pi` is a local
  constant `pi_val` in the bodies that need it; `g = 9.80665 m/s²` likewise
  (`fluids.constants.g`, the value `ht` uses for `Lockhart_Martinelli_Xtt` and
  Bond numbers). `ATAN` returns **degrees** in EES and in CoolSolve, so the
  `atan` of `h_Chen_Edelstein` is written `ATAN(...)*pi_val/180`. `SIN`/`COS`
  take degrees, so the angle of the transition function is written in degrees.

## How to run

Open `flow_boiling_in_tubes.eescode` in the CoolSolve GUI and press *Solve*, or
from a terminal:

```bash
coolsolve ./flow_boiling_in_tubes.eescode
```

The demonstration program after the definitions calls every correlation:

* **case A** — the input set of the `ht` doctest of the corresponding correlation
  (published values); for the two ThermoCycle correlations, the same fluid
  (CO₂-like properties at 1 bar, as in the reviews `ht` quotes);
* **case B** — one uniform, realistic input set: R134a saturated at 5 °C
  (CoolProp 8.0.0 saturation properties), 0.2 kg/s, quality 0.4, 10 mm tube,
  4·10⁴ W/m², wall 30 K above the saturation temperature;
* **case C** — a low liquid Froude number (Fr_l = 0.037, 0.85 kg/s in a 100 mm
  tube), the only region where the vertical and the horizontal form of Shah 1982
  differ, and where the low-velocity term of Gungor-Winterton is active.

It solves in 3 Newton iterations (the two-equation block of the `h_Thome`
excess-temperature case, everything else explicit) and is the regression
baseline (`flow_boiling_in_tubes.sol`, with the guess of that block in
`flow_boiling_in_tubes.initials`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0098 ---}` and
lists `CSL-0098` in its `related` field.

## Results

Values of the demonstration program (full precision in
`flow_boiling_in_tubes.sol`), all in W/m²/K:

| Quantity (case A) | h_tp [W/m²/K] | Quantity (case B) | h_tp [W/m²/K] |
|---|---:|---|---:|
| `h_Lazarek_Black` (Te = 100 K) | 9 501.9 | (q = 4·10⁴ W/m²) | 6 302.1 |
| `h_Lazarek_Black` (q = 10⁷ W/m²) | 51 009.9 | (Te = 30 K) | 304 431.0 |
| `h_Li_Wu` (q = 10⁵ W/m²) | 5 345.4 | (q) | 5 792.7 |
| `h_Li_Wu` (Te implied by q) | 5 345.4 | (Te = 30 K) | 10 871.5 |
| `h_Sun_Mishima` (Te = 10 K) | 507.67 | (q) | 6 478.2 |
| `h_Sun_Mishima` (q = 10⁵ W/m²) | 2 538.4 | (Te = 30 K) | 41 434.8 |
| `h_Thome` (m = 1, x = 0.4, q = 10⁵) | 1 633.0 | (q = 4·10⁴) | 7 844.9 |
| `h_Thome` (m = 10, x = 0.5, q = 10⁵) | 3 120.2 | (Te = 30 K, q = 3.21·10⁶) | 107 004.0 |
| `h_Yun_Heo_Kim` (q = 10⁴ W/m²) | 9 479.3 | (q) | 18 823.5 |
| `h_Yun_Heo_Kim` (Te implied by q) | 9 479.3 | (Te = 30 K) | 36 381.9 |
| `h_Chen_Edelstein` | 3 289.1 | | 19 617.4 |
| `h_Chen_Bennett` | 4 938.3 | | 27 856.3 |
| `h_Liu_Winterton` | 4 747.7 | | 48 166.3 |
| `h_Shah_1982` (vertical) | 68 762.1 | (vertical) | 18 459.3 |
| `h_Shah_1982` (horizontal) | 68 762.1 | (horizontal) | 18 459.3 |
| `h_Gungor_Winterton_1987` | 55 755.9 | | 15 982.4 |
| | | `hl_B`, the liquid-only coefficient of Shah / Gungor-Winterton | 2 368.8 |

Case C (low liquid Froude number, Fr_l = 0.0372): `h_Shah_1982` vertical
**1 418.9**, horizontal **1 409.9** (the two forms differ by 0.6 %, because
N = Co for the vertical flow and N = 0.38·Fr_l^−0.3·Co = 0.2521 for the
horizontal one); `h_Gungor_Winterton_1987` **1 411.1** (its low-velocity term
Fr_l^(0.1−2·Fr_l) = 0.75 is active).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the ten
     coefficients over a quality or a wall-excess-temperature sweep for R134a in
     a 10 mm tube, e.g. h_tp vs x at q = 4E4 W/m^2,
     figures/flow_boiling_in_tubes_htp_x.png -->

## Verification

Two independent references, both reproduced in a throw-away virtual environment
under `work/` (the local clone of `ht`, version 1.2.0, plus CoolProp 8.0.0):

1. the **doctest values published in the docstrings of `ht` 1.2.0**
   (`ht/boiling_flow.py`, commit `85e0ee6`) and the regression values of
   `ht/tests/test_boiling_flow.py`, for the eight `ht` correlations — case A
   reproduces the doctests (Lazarek-Black Te = 100 K → 9501.932636079, Li-Wu
   q = 10⁵ → 5345.409399239, Sun-Mishima Te = 10 K → 507.670916837, Thome
   q = 10⁵ → 1633.008836502 and 3120.178771512 for the two test cases, Yun-Heo-Kim
   q = 10⁴ → 9479.313988550, Chen-Edelstein → 3289.058731974, Chen-Bennett →
   4938.275351219, Liu-Winterton → 4747.749477191) plus the `Te` forms implied by
   those heat fluxes, which `ht` checks by equality with the `q` form;
2. an **independent Python transcription of the Modelica equations** of Shah 1982
   and Gungor-Winterton 1987 (case A, B and C above), written from the
   ThermoCycle sources, with `smoothOrder` blends kept.

Case B is compared with values computed by calling the same `ht` functions (and
the same Python transcription) on the same R134a input set. The 37 output values
of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
37 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 119
```

(the 119 "only in CoolSolve" variables are the input sets of the three cases, the
local constants `pi_val` of the function bodies and the intermediate
demonstration variables; the reference table holds only the 37 outputs). The
largest relative deviation over the 37 values is **4.2·10⁻¹²**
(`h_Lazarek_Black_Te_B`), i.e. round-off in the double-precision evaluation.

| Variable | reference | CoolSolve | rel. dev. | | Variable | reference | CoolSolve | rel. dev. |
|---|---:|---:|---:|---|---|---:|---:|
| `h_Lazarek_Black_Te_A` | 9501.932636079 | 9501.932636079 | 3.1e-14 | | `h_Lazarek_Black_q_B` | 6302.082470244 | 6302.082470252 | 1.2e-12 |
| `h_Lazarek_Black_q_A` | 51009.870019671 | 51009.870019670 | 2.1e-14 | | `h_Lazarek_Black_Te_B` | 304431.015094029 | 304431.015095300 | 4.2e-12 |
| `h_Li_Wu_q_A` | 5345.409399239 | 5345.409399239 | 9.2e-14 | | `h_Li_Wu_q_B` | 5792.725692750 | 5792.725692757 | 1.3e-12 |
| `h_Li_Wu_Te_A` | 5345.409399239 | 5345.409399239 | 9.2e-14 | | `h_Li_Wu_Te_B` | 10871.453990215 | 10871.453990230 | 1.4e-12 |
| `h_Sun_Mishima_Te_A` | 507.670916837 | 507.670916837 | 6.2e-13 | | `h_Sun_Mishima_q_B` | 6478.207252165 | 6478.207252166 | 1.5e-13 |
| `h_Sun_Mishima_q_A` | 2538.445542435 | 2538.445542434 | 2.4e-13 | | `h_Sun_Mishima_Te_B` | 41434.780626414 | 41434.780626430 | 3.9e-13 |
| `h_Thome_q_A` | 1633.008836502 | 1633.008836502 | 2.0e-14 | | `h_Thome_q_B` | 7844.929528493 | 7844.929528479 | 1.8e-12 |
| `h_Thome_q2_A` | 3120.178771512 | 3120.178771512 | 1.5e-13 | | `h_Thome_Te_B` | 107003.984002166 | 107003.984002200 | 3.2e-13 |
| `h_Yun_Heo_Kim_q_A` | 9479.313988550 | 9479.313988551 | 8.6e-14 | | `q_Thome_Te_B` | 3210119.520064984 | 3210119.520065000 | 4.9e-15 |
| `h_Yun_Heo_Kim_Te_A` | 9479.313988550 | 9479.313988551 | 8.6e-14 | | `h_Yun_Heo_Kim_q_B` | 18823.534034465 | 18823.534034480 | 7.9e-13 |
| `h_Chen_Edelstein_A` | 3289.058731974 | 3289.058731973 | 3.2e-13 | | `h_Yun_Heo_Kim_Te_B` | 36381.895080045 | 36381.895080070 | 6.9e-13 |
| `h_Chen_Bennett_A` | 4938.275351219 | 4938.275351219 | 7.5e-14 | | `h_Chen_Edelstein_B` | 19617.444465679 | 19617.444465690 | 5.9e-13 |
| `h_Liu_Winterton_A` | 4747.749477191 | 4747.749477191 | 9.8e-14 | | `h_Chen_Bennett_B` | 27856.286759775 | 27856.286759770 | 1.7e-13 |
| `h_Shah_1982_v_A` | 68762.109746566 | 68762.109746560 | 8.1e-14 | | `h_Liu_Winterton_B` | 48166.265487448 | 48166.265487440 | 1.7e-13 |
| `h_Shah_1982_h_A` | 68762.109746566 | 68762.109746560 | 8.1e-14 | | `h_Shah_1982_v_B` | 18459.335325066 | 18459.335325070 | 2.0e-13 |
| `h_Gungor_Winterton_A` | 55755.915761610 | 55755.915761600 | 1.7e-13 | | `h_Shah_1982_h_B` | 18459.335325066 | 18459.335325070 | 2.0e-13 |
| `h_Shah_1982_v_C` | 1418.891177689 | 1418.891177689 | 4.1e-14 | | `h_Gungor_Winterton_B` | 15982.440964222 | 15982.440964230 | 4.9e-13 |
| `h_Shah_1982_h_C` | 1409.877323353 | 1409.877323353 | 9.3e-14 | | `hl_B` | 2368.818278953 | 2368.818278951 | 7.0e-13 |
| `h_Gungor_Winterton_C` | 1411.070237117 | 1411.070237117 | 2.0e-13 | | | | | |

## Source and attribution

Eight of the ten correlations are a translation (into the EES-compatible
language CoolSolve reads) of `ht`, the heat-transfer component of ChEDL, file
`ht/boiling_flow.py`, functions `Lazarek_Black`, `Li_Wu`, `Sun_Mishima`, `Thome`,
`Yun_Heo_Kim`, `Chen_Edelstein`, `Chen_Bennett` and `Liu_Winterton`, version
1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

The other two, **Shah 1982** and **Gungor-Winterton 1987**, are a translation of
the ThermoCycle Modelica library, files
`ThermoCycle/Components/HeatFlow/HeatTransfer/TwoPhaseCorrelations/Shah1982.mo`
and `…/GungorWinterton1987.mo`, with
`ThermoCycle/Functions/transition_factor.mo` and
`ThermoCycle/Components/HeatFlow/HeatTransfer/SinglePhaseCorrelations/DittusBoelter1930.mo`
(inventory row `THC-004`; `ht` has no Shah and no Gungor-Winterton
correlation, so this model completes the `ht` family — see the roadmap card
C-107, which replaces C-92).

> ThermoCycle - https://github.com/JeSoftware/Thermocycle-library - Modelica
> implementation of two-phase heat-transfer correlations, used as the
> documented, equation-by-equation reference of the Shah (1982) and
> Gungor-Winterton (1987) correlations.

Changes: translated from Python (or Modelica) to CoolSolve; every correlation
became one EES `FUNCTION` named after the `ht` function (with the `h_tp` return
value, so the name is prefixed by `h_`), the two optional inputs `q`/`Te` of the
five `ht` functions became mandatory arguments selected by the flag `by_Te`, the
inner iteration of `ht` for `Thome` with a prescribed `Te` became an unknown of
the calling system, the smooth transition function of ThermoCycle became the
EES `FUNCTION` `tr_factor_Richter2`, and the correlations of `CSL-0087` /
`CSL-0088` used inside `h_Thome`, `h_Chen_Edelstein`, `h_Chen_Bennett`,
`h_Liu_Winterton`, `h_Shah_1982` and `h_Gungor_Winterton_1987` are written out
in the body. `pi` and `g` are local constants (`CS-BUG-PI-FUNCTION`),
`ATAN` is converted from degrees, `SIN`/`COS` take degrees. No equation was
changed. Scientific basis per function: the original paper or book quoted in its
comment block.

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-107, family `HT-012` of the `ht`
  triage, which also covers `THC-004`).** Eleven EES `FUNCTION`s (ten
  correlations + the transition function of the Shah blends), named
  `h_<method>`; formula, validity range as quoted by `ht`, original reference and
  the `ht` module/function/version/commit in each comment block (for the two
  ThermoCycle correlations, the Modelica file and the original paper). All
  arguments are SI (K, Pa, kg/s, W/m², J/kg, kg/m³, Pa·s, W/m·K, J/kg·K, N/m,
  g/mol) or dimensionless numbers computed inside the function; no property
  function is called inside a function (rule 5 of `sources/ht/README.md` §7).
- `Lazarek_Black`, `Li_Wu`, `Sun_Mishima`, `Yun_Heo_Kim`: `ht` gives the two
  optional inputs `q` and `Te`; both are mandatory here and the `by_Te` flag
  selects the branch with an EES `IF` (the non-smooth regime switch, not a
  function call). Both branches are exercised in the demonstration program.
- `Thome`: only the `q` form is a `FUNCTION`; the `Te` form (which `ht` obtains
  by a secant iteration on `q`) is demonstrated in the main program with `q` as
  an unknown and the equation `q = h_Thome(...)*Te`, the equation the secant
  solves. One initial guess is needed (`q_Thome_Te_B = 3E6`, in the
  `.initials`): the function is not monotone enough over the whole range for a
  blind Newton step from 1, although the solution itself is unique and smooth.
- `Chen_Edelstein`: `ATAN` returns degrees in EES and in CoolSolve, so the angle
  is converted to radians with the local constant `pi_val`.
- **Not translated (helpers, not correlations):** `to_solve_q_Thome`, the inner
  solver of `ht` (replaced by the simultaneous equation above); no selector or
  dispatcher function exists in `ht/boiling_flow.py`.
- `h_Shah_1982` and `h_Gungor_Winterton_1987` come from ThermoCycle (row
  `THC-004`), which `ht` does not have; `Cooper 1984`, the third correlation of
  `THC-004`, is already in the library as `h_Cooper` (`CSL-0088`) and is used
  (written out) inside `h_Liu_Winterton`. The Modelica sources store the
  intermediate quantities in Kelvin (`i_fg = h_v − h_l`); here `i_fg` is an
  explicit SI argument [J/kg], the caller passes `h_v − h_l`.
- **Level**: equations 156 → 1 point (50–300), largest block 2 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses → 1 (the single `.initials` value of the `h_Thome` block). Score 3 →
  **level 2** (the intended audience is the correlation library of the same
  family, `CSL-0087`…`CSL-0097`, all level 2).

## Limitations and CoolSolve gaps

- The demonstration input sets are chosen to be realistic, not to stay inside
  every quoted validity range: the `ht` doctests themselves are outside the
  stated range of some correlations (e.g. Lazarek-Black was developed for a
  3.1 mm tube, its doctest uses 0.3 m). `ht` does not check the ranges in these
  functions, so its values are reproduced as they are; the numbers of the
  *Results* and *Verification* tables are a check of the **equations**, not
  recommended design values.
- `h_Shah_1982` (vertical = horizontal) and `h_Shah_1982_v_B` =
  `h_Shah_1982_h_B`: with the liquid Froude number of those cases (5142 and 40)
  the vertical and horizontal forms of N coincide, as they must. Case C is the
  demonstration where they differ.
- The two-phase flow boiling in a tube needs its single-phase coefficients too;
  they are the `CSL-0087` correlations (Dittus-Boelter, Gnielinski), written out
  here for the film and slug models. A rating model combines them with
  `CSL-0090` (eps-NTU) or `CSL-0009`-style energy balances.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES (`FUNCTION`,
  `IF/THEN/ELSE`, `LOG10`, `EXP`, `SIN`, `COS`, `MIN`, `MAX`, `SQRT`) and runs in
  CoolSolve v0.3.0. One **unverified suggestion** was found while writing this
  model and is *not* registered, because no evidence was found that the
  single-word `ELSEIF` is valid EES (the EES form documented in the CoolSolve
  language reference is `ELSE IF … THEN`, an ordinary nested `IF`): inside a
  `FUNCTION` body, `IF … THEN … ELSEIF … THEN … ELSE … ENDIF` (one `ENDIF` at
  the end) evaluates **every** branch and keeps the last one, silently.
  Reproducer (valid EES with the nested form): `FUNCTION f1(a)` ⏎ `IF a <= 0
  THEN f1 = -1 ELSEIF a >= 10 THEN f1 = 100 ELSE f1 = 2*a ENDIF` ⏎ `END` ⏎
  `y1 = f1(-5)` ⏎ `y2 = f1(5)` ⏎ `y3 = f1(50)` gives 100, 10, 100 instead of −1,
  10, 100; the same function with the nested `ELSE` + `IF` form (one `ENDIF`
  each) gives the three expected values. `tr_factor_Richter2` therefore uses the
  nested form. (`CS-GAP-ELSEIF-CHAIN` in the register is a different, already
  registered problem: the `ELSE` + `IF` ladder closed by grouped `ENDIF`s is a
  parse error.)

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the single-phase turbulent
  correlations (Dittus-Boelter, Gnielinski) that `h_Thome`, `h_Chen_Edelstein`,
  `h_Chen_Bennett` and `h_Liu_Winterton` write out in their bodies, and
  `h_Shah_1982` / `h_Gungor_Winterton_1987` for the liquid-only coefficient.
- `CSL-0088` *nucleate_boiling_and_chf*: the pool-boiling correlations
  `h_Forster_Zuber` and `h_Cooper` used by `h_Chen_Edelstein`, `h_Chen_Bennett`
  and `h_Liu_Winterton`; the nucleate-boiling side of the same two-phase
  problem.
- `CSL-0089` *condensation_film*: the condensation counterpart of this file
  (same layout, same comment blocks); `h_Shah` there also starts from the
  Dittus-Boelter coefficient of `CSL-0087`.
- `CSL-0097` *two_phase_nonboiling_in_tube*: the in-tube two-phase
  heat-transfer coefficients **without** phase change (Groothuis-Hendal,
  Aggour …); a tube carrying a condensing or an evaporating mixture needs both
  files.
- `CSL-0096` *plate_hx_heat_transfer*: the plate-heat-exchanger family of the
  same `ht` triage, including its plate two-phase boiling correlations.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations a rating
  model combines with the coefficients of this file.
- `CSL-0038`, `CSL-0077` (sCO₂ and air-cooled components) and the evaporator and
  condenser models `CSL-0027`, `CSL-0031`: models that would use these
  correlations.
- sources/thermocycle `THC-004`: the inventory row this model completes with
  Shah 1982 and Gungor-Winterton 1987 (`ht` has neither); its third correlation,
  Cooper 1984, is `CSL-0088` *nucleate_boiling_and_chf* (`h_Cooper`).
