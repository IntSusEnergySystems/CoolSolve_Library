# Internal turbulent convection: Nusselt-number correlations for pipe flow

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0087`

Twenty-three EES `FUNCTION`s returning the Nusselt number of single-phase
turbulent flow inside a circular pipe, from Dittus-Boelter (1930) to
Bhatti-Shah (1987). All of them take dimensionless arguments only
(Re, Pr, the Darcy friction factor `fd`, the relative roughness `eD`, plus the
viscosities, the diameter and the distance from the inlet where those appear);
the wall heat-transfer coefficient follows from `h = Nu*k/Di` and is left to the
caller, as in the source library. The friction factors are **inputs**: `ht`
ships no friction-factor correlation (they belong to the companion library
`fluids`). This is the first of the 24 `ht` families planned for the library
(roadmap cards C-96…C-119) and sets its layout: one `FUNCTION` per
correlation, a comment block per function with the formula, the validity range
and the dual citation, and a demonstration program calling every function.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Re, Pr and `fd` are arguments) |
| **Size** | 70 equations after analysis (largest block: 1); 23 functions of 3–20 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_internal.py` (MIT); inventory row `HT-001` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (52 values, max deviation 3.2·10⁻¹³) |

## Problem statement

For a given flow regime (Re, Pr) and wall state of a smooth or rough pipe
(Darcy friction factor `fd`, relative roughness `eD`), compute the Nusselt
number Nu of the pipe; multiply it by `k/Di` to obtain the wall heat-transfer
coefficient. Twenty-three historical correlations are available for that, each
with its own validity range; the choice between them is left to the user, who
knows the fluid and the geometry.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_Dittus_Boelter` | Re, Pr, heating, revised | Nu = m·Re^0.8·Prⁿ, m = 0.023 (revised) or 0.0243 / 0.0265 (original), n = 0.4 heating, 0.3 cooling | 0.6 ≤ Pr ≤ 160, Re ≥ 10⁴, L/Di ≥ 10 |
| `Nu_Sieder_Tate` | Re, Pr, mu, mu_w | Nu = 0.027·Re^0.8·Pr^(1/3)·(mu/mu_w)^0.14 | as in `ht`, none quoted |
| `Nu_Hausen_turbulent_entry` | Re, Pr, Di, x | Nu = 0.037·(Re^0.75 − 180)·Pr^0.42·[1+(x/Di)^(−2/3)] | 0.7 < Pr ≤ 3, 10⁴ ≤ Re ≤ 5·10⁶ |
| `Nu_Colburn` | Re, Pr | Nu = 0.023·Re^0.8·Pr^(1/3) | 0.5 < Pr < 3, 10⁴ < Re < 10⁵ |
| `Nu_Drexel_McAdams` | Re, Pr | Nu = 0.021·Re^0.8·Pr^0.4 | Pr ≤ 0.7, 10⁴ ≤ Re ≤ 5·10⁶ |
| `Nu_von_Karman` | Re, Pr, fd | Nu = (fd/8)·Re·Pr / {1 + 5·(fd/8)^0.5·[Pr − 1 + ln((5Pr+1)/6)]} | 0.5 ≤ Pr ≤ 3, 10⁴ ≤ Re ≤ 10⁵ |
| `Nu_Prandtl` | Re, Pr, fd | Nu = (fd/8)·Re·Pr / {1 + 8.7·(fd/8)^0.5·(Pr − 1)} | 0.5 ≤ Pr ≤ 5, 10⁴ ≤ Re ≤ 5·10⁶ |
| `Nu_Friend_Metzner` | Re, Pr, fd | Nu = (fd/8)·Re·Pr / {1.2 + 11.8·(fd/8)^0.5·(Pr − 1)·Pr^(−1/3)} | 50 < Pr ≤ 600, 5·10⁴ ≤ Re ≤ 5·10⁶ |
| `Nu_Petukhov_Kirillov_Popov` | Re, Pr, fd | Nu = (fd/8)·Re·Pr / {C + 12.7·(fd/8)^0.5·(Pr^(2/3) − 1)}, C = 1.07 + 900/Re − 0.63/(1+10Pr) | 0.5 < Pr ≤ 10⁶, 4000 ≤ Re ≤ 5·10⁶ |
| `Nu_Webb` | Re, Pr, fd | Nu = (fd/8)·Re·Pr / {1.07 + 9·(fd/8)^0.5·(Pr − 1)·Pr^0.25} | 0.5 < Pr ≤ 100, 10⁴ ≤ Re ≤ 5·10⁶ |
| `Nu_Sandall` | Re, Pr, fd | Nu = (fd/8)^0.5·Re·Pr / {12.48Pr^(2/3) − 7.853Pr^(1/3) + 3.613 ln Pr + 5.8 + C}, C = 2.78·ln((fd/8)^0.5·Re/45) | 0.5 < Pr ≤ 2000, 10⁴ ≤ Re ≤ 5·10⁶ |
| `Nu_Gnielinski` | Re, Pr, fd | Nu = (fd/8)·(Re − 1000)·Pr / {1 + 12.7·(fd/8)^0.5·(Pr^(2/3) − 1)} | 0.5 < Pr ≤ 2000, 2300 ≤ Re ≤ 5·10⁶ |
| `Nu_Gnielinski_smooth_1` | Re, Pr | Nu = 0.0214·(Re^0.8 − 100)·Pr^0.4 | 0.5 < Pr ≤ 1.5, 10⁴ ≤ Re ≤ 5·10⁶ |
| `Nu_Gnielinski_smooth_2` | Re, Pr | Nu = 0.012·(Re^0.87 − 280)·Pr^0.4 | 1.5 < Pr ≤ 500, 3·10³ ≤ Re ≤ 10⁶ |
| `Nu_Churchill_Zajic` | Re, Pr, fd | Nu = 1/{(Pr_T/Pr)/Nu_di + [1 − (Pr_T/Pr)^(2/3)]/Nu_D∞}, Nu_di = Re·(fd/8)/{1 + 145·(8/fd)^(−5/4)}, Nu_D∞ = 0.07343·Re·(Pr/Pr_T)^(1/3)·(fd/8)^0.5, Pr_T = 0.85 + 0.015/Pr | none quoted |
| `Nu_ESDU` | Re, Pr | Nu = 0.0225·Re^0.795·Pr^0.495·exp(−0.0225·ln²Pr) | 4000 < Re < 10⁶, 0.3 < Pr < 3000, L/Di > 60 |
| `Nu_Martinelli` | Re, Pr, fd | Nu = Re·Pr·(fd/8)^0.5 / {5·[Pr + ln(1+5Pr) + 0.5·ln(Re·(fd/8)^0.5/60)]} | none quoted (liquid metals) |
| `Nu_Nunner` | Re, Pr, fd, fd_smooth | Nu = Re·Pr·(fd/8) / {1 + 1.5·Re^(−1/8)·Pr^(−1/6)·[Pr·(fd/fd_smooth) − 1]} | Pr ≈ 0.7; bad results for Pr > 1 |
| `Nu_Dipprey_Sabersky` | Re, Pr, fd, eD | Nu = Re·Pr·(fd/8) / {1 + (fd/8)^0.5·[5.19·Re_e^0.2·Pr^0.44 − 8.48]}, Re_e = Re·eD·(fd/8)^0.5 | 1.2 ≤ Pr ≤ 5.94, 1.4·10⁴ ≤ Re ≤ 5·10⁵, 0.0024 ≤ eD ≤ 0.049 |
| `Nu_Gowen_Smith` | Re, Pr, fd | Nu = Re·Pr·(fd/8)^0.5 / {4.5 + [0.155·(Re·(fd/8)^0.5)^0.54 + (8/fd)^0.5]·Pr^0.5} | 0.7 ≤ Pr ≤ 14.3, 10⁴ ≤ Re ≤ 5·10⁴, 0.0021 ≤ eD ≤ 0.095 |
| `Nu_Kawase_Ulbrecht` | Re, Pr, fd | Nu = 0.0523·Re·Pr^0.5·(fd/4)^0.5 | none quoted |
| `Nu_Kawase_De` | Re, Pr, fd | Nu = 0.0471·Re·Pr^0.5·(fd/4)^0.5·(1.11 + 0.44·Pr^(−1/3) − 0.7·Pr^(−1/6)) | 5.1 ≤ Pr ≤ 390, 5000 ≤ Re ≤ 5·10⁵, 0.0024 ≤ eD ≤ 0.165 |
| `Nu_Bhatti_Shah` | Re, Pr, fd, eD | Nu = Re·Pr·(fd/8) / {1 + (fd/8)^0.5·[4.5·Re_e^0.2·Pr^0.5 − 8.48]}, Re_e = Re·eD·(fd/8)^0.5 | 0.5 ≤ Pr ≤ 10, 0.002 ≤ eD ≤ 0.05, 10⁴ ≤ Re |

Arguments: Re (Reynolds number on `Di`, `[-]`), Pr (bulk Prandtl number,
`[-]`), `fd` (Darcy friction factor, `[-]`), `eD` (relative roughness ε/Di,
`[-]`), `fd_smooth` (Darcy friction factor of a smooth pipe, `[-]`), `mu` and
`mu_w` (bulk and wall viscosity, `[Pa·s]`), `Di` (inside diameter, `[m]`), `x`
(distance from the pipe inlet, `[m]`), `heating` and `revised` (flags: 1 or 0).

Every function carries in its comment block (i) the equation, (ii) the
validity range **as quoted by `ht`**, (iii) the original paper or book and
(iv) the `ht` module, function, version and commit it was taken from. The
scientific basis is, for most correlations, the presentation in Rohsenow, W.,
J. Hartnett and Y. Cho, *Handbook of Heat Transfer*, 3E, McGraw-Hill, 1998,
which is where `ht` itself takes them from; the original papers are named
individually (Dittus-Boelter 1930, Sieder-Tate 1936, Colburn 1964, von Karman
1939, Friend-Metzner 1958, Petukhov-Kirillov 1958 / Petukhov-Popov 1963, Webb
1971, Sandall-Hanna-Mazet 1980, Gnielinski 1976, Churchill-Zajic 2002,
Martinelli 1947, Nunner 1956, Dipprey-Sabersky 1963, Gowen-Smith 1968,
Kawase-Ulbrecht 1982, Kawase-De 1984, Bhatti-Shah 1987, Hausen 1959, ESDU as
given in Hewitt, Shires & Bott, *Process Heat Transfer*, 1994).

Two members of the `ht` family are **not** translated: `Nu_conv_internal` and
`Nu_conv_internal_methods` are dispatchers that map a method name to a
correlation; an EES caller calls the chosen `FUNCTION` directly.

## How to run

Open `internal_turbulent_nusselt.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./internal_turbulent_nusselt.eescode
```

The demonstration program after the definitions calls each of the 23
functions twice: once (case *A*) with the input set of the `ht` doctest of the
corresponding correlation, once (case *B*) with a single uniform input set
(Re = 2.5·10⁵, Pr = 5, fd = 0.0215, eD = 0.0025, Di = 0.03 m, x = 0.25 m,
mu = 4·10⁻⁴ Pa·s, mu_w = 6·10⁻⁴ Pa·s, fd_smooth = 0.0155). It solves without any iteration (`Solver: SUCCESS (0 iterations)`, every
equation is explicit) and is the regression baseline
(`internal_turbulent_nusselt.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0087 ---}` and
lists `CSL-0087` in its `related` field.

## Results

Values of the demonstration program (full precision in
`internal_turbulent_nusselt.sol`):

| Quantity (case A) | Nu [−] | Quantity (case B) | Nu [−] |
|---|---:|---|---:|
| `Nu_Dittus_Boelter` (heating, revised) | 247.40 | | 911.31 |
| `Nu_Dittus_Boelter_cool` (cooling, revised) | 242.93 | | 775.84 |
| `Nu_Dittus_Boelter_orig` (heating, original) | 261.38 | | 962.82 |
| `Nu_Sieder_Tate` (mu/mu_w = 0.149) | 219.84 | | 907.93 |
| `Nu_Sieder_Tate_equalmu` (mu = mu_w) | 286.92 | | 960.96 |
| `Nu_Hausen_turbulent_entry` (x = 5 cm, Di = 0.154 m) | 677.72 | (x = 0.25 m, Di = 0.03 m) | 994.83 |
| `Nu_Colburn` | 244.41 | | 818.60 |
| `Nu_Drexel_McAdams` (Pr = 0.6) | 171.19 | (Pr = 5) | 832.07 |
| `Nu_von_Karman` | 255.72 | | 1389.95 |
| `Nu_Prandtl` | 256.07 | | 1198.04 |
| `Nu_Friend_Metzner` (Pr = 100) | 1738.34 | (Pr = 5) | 1276.86 |
| `Nu_Petukhov_Kirillov_Popov` | 250.12 | | 1443.04 |
| `Nu_Webb` | 239.10 | | 870.14 |
| `Nu_Sandall` | 229.05 | | 1285.20 |
| `Nu_Gnielinski` | 254.63 | | 1476.10 |
| `Nu_Gnielinski_smooth_1` | 227.89 | | 843.84 |
| `Nu_Gnielinski_smooth_2` (Pr = 7) | 577.77 | (Pr = 5) | 1128.55 |
| `Nu_Churchill_Zajic` | 260.56 | | 1470.67 |
| `Nu_ESDU` | 232.30 | | 920.92 |
| `Nu_Martinelli` (Pr = 100) | 887.17 | (Pr = 5) | 1184.05 |
| `Nu_Nunner` (Pr = 0.7) | 101.16 | (Pr = 5) | 1376.89 |
| `Nu_Dipprey_Sabersky` | 288.33 | | 2029.10 |
| `Nu_Gowen_Smith` | 131.73 | | 615.63 |
| `Nu_Kawase_Ulbrecht` | 389.63 | | 2143.46 |
| `Nu_Kawase_De` | 296.50 | | 1606.06 |
| `Nu_Bhatti_Shah` | 302.70 | | 2091.41 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the 23 correlations
     over a Reynolds-number sweep, e.g. Nu vs Re at Pr = 1 and Pr = 100,
     figures/internal_turbulent_nusselt_nu_re.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_internal.py`, commit `85e0ee6`, installed from the local clone in a
throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for case *B*. The 52 output values of the demonstration
program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
52 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 18
```

(the 18 “only in CoolSolve” variables are the 18 inputs of the demonstration
program — `Re_A`, `Pr_A`, `fd_A`, `eD_A`, `Di_A`, `x_A`, `mu_A`, `mu_w_A`,
`fd_smooth_A` and their nine `_B` counterparts —; the reference table holds
only the 52 outputs). The largest relative deviation over the 52 values is
**3.2·10⁻¹³** (`Nu_Churchill_Zajic_B`), i.e. round-off in the double-precision
evaluation.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_Dittus_Boelter` | 247.400364094491 | 247.4003640945 | 3.5e-14 |
| `Nu_Dittus_Boelter_cool` | 242.930592741030 | 242.9305927410 | 1.2e-13 |
| `Nu_Dittus_Boelter_orig` | 261.383862934615 | 261.3838629346 | 5.6e-14 |
| `Nu_Sieder_Tate` | 219.840164557660 | 219.8401645577 | 1.8e-13 |
| `Nu_Sieder_Tate_equalmu` | 286.917813679305 | 286.9178136793 | 1.8e-14 |
| `Nu_Hausen_turbulent_entry` | 677.722827590176 | 677.7228275902 | 3.6e-14 |
| `Nu_Colburn` | 244.411470912001 | 244.4114709120 | 2.8e-15 |
| `Nu_Drexel_McAdams` | 171.190553017244 | 171.1905530172 | 2.6e-13 |
| `Nu_von_Karman` | 255.724354124327 | 255.7243541243 | 1.1e-13 |
| `Nu_Prandtl` | 256.073339689557 | 256.0733396896 | 1.7e-13 |
| `Nu_Friend_Metzner` | 1738.335626205532 | 1738.335626206 | 2.7e-13 |
| `Nu_Petukhov_Kirillov_Popov` | 250.119350889051 | 250.1193508891 | 2.0e-13 |
| `Nu_Webb` | 239.101303768159 | 239.1013037682 | 1.7e-13 |
| `Nu_Sandall` | 229.051435297024 | 229.0514352970 | 1.0e-13 |
| `Nu_Gnielinski` | 254.626827493596 | 254.6268274936 | 1.4e-14 |
| `Nu_Gnielinski_smooth_1` | 227.888004943734 | 227.8880049437 | 1.5e-13 |
| `Nu_Gnielinski_smooth_2` | 577.769252451345 | 577.7692524513 | 7.8e-14 |
| `Nu_Churchill_Zajic` | 260.556490781796 | 260.5564907818 | 1.5e-14 |
| `Nu_ESDU` | 232.301714343065 | 232.3017143431 | 1.5e-13 |
| `Nu_Martinelli` | 887.171068639635 | 887.1710686396 | 3.9e-14 |
| `Nu_Nunner` | 101.158410109199 | 101.1584101092 | 5.3e-15 |
| `Nu_Dipprey_Sabersky` | 288.333651985667 | 288.3336519857 | 1.2e-13 |
| `Nu_Gowen_Smith` | 131.725304538241 | 131.7253045382 | 3.1e-13 |
| `Nu_Kawase_Ulbrecht` | 389.626224733398 | 389.6262247334 | 6.4e-15 |
| `Nu_Kawase_De` | 296.501973327132 | 296.5019733271 | 1.1e-13 |
| `Nu_Bhatti_Shah` | 302.703761741427 | 302.7037617414 | 9.0e-14 |

Case *B* (second input set, computed with the same Python functions):

| Function | `ht` | CoolSolve | Function | `ht` | CoolSolve |
|---|---:|---:|---|---:|---:|
| `Nu_Dittus_Boelter_B` | 911.3136 | 911.3136 | `Nu_Gnielinski_smooth_1_B` | 843.8440 | 843.8440 |
| `Nu_Dittus_Boelter_cool_B` | 775.8376 | 775.8376 | `Nu_Gnielinski_smooth_2_B` | 1128.5546 | 1128.5546 |
| `Nu_Dittus_Boelter_orig_B` | 962.8226 | 962.8226 | `Nu_Churchill_Zajic_B` | 1470.6684 | 1470.6684 |
| `Nu_Sieder_Tate_B` | 907.9313 | 907.9313 | `Nu_ESDU_B` | 920.9237 | 920.9237 |
| `Nu_Sieder_Tate_equalmu_B` | 960.9610 | 960.9610 | `Nu_Martinelli_B` | 1184.0468 | 1184.0468 |
| `Nu_Hausen_turbulent_entry_B` | 994.8257 | 994.8257 | `Nu_Nunner_B` | 1376.8915 | 1376.8915 |
| `Nu_Colburn_B` | 818.5964 | 818.5964 | `Nu_Dipprey_Sabersky_B` | 2029.0956 | 2029.0956 |
| `Nu_Drexel_McAdams_B` | 832.0689 | 832.0689 | `Nu_Gowen_Smith_B` | 615.6291 | 615.6291 |
| `Nu_von_Karman_B` | 1389.9493 | 1389.9493 | `Nu_Kawase_Ulbrecht_B` | 2143.4627 | 2143.4627 |
| `Nu_Prandtl_B` | 1198.0352 | 1198.0352 | `Nu_Kawase_De_B` | 1606.0602 | 1606.0602 |
| `Nu_Friend_Metzner_B` | 1276.8648 | 1276.8648 | `Nu_Bhatti_Shah_B` | 2091.4146 | 2091.4146 |
| `Nu_Petukhov_Kirillov_Popov_B` | 1443.0393 | 1443.0393 | | | |
| `Nu_Webb_B` | 870.1378 | 870.1378 | | | |
| `Nu_Sandall_B` | 1285.1988 | 1285.1988 | | | |
| `Nu_Gnielinski_B` | 1476.1020 | 1476.1020 | | | |

All 52 relative deviations are below 3.3·10⁻¹³.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the turbulent internal-convection correlations of `ht`,
the heat-transfer component of ChEDL, file `ht/conv_internal.py`, functions
`turbulent_Dittus_Boelter`, `turbulent_Sieder_Tate`, `turbulent_entry_Hausen`,
`turbulent_Colburn`, `turbulent_Drexel_McAdams`, `turbulent_von_Karman`,
`turbulent_Prandtl`, `turbulent_Friend_Metzner`,
`turbulent_Petukhov_Kirillov_Popov`, `turbulent_Webb`, `turbulent_Sandall`,
`turbulent_Gnielinski`, `turbulent_Gnielinski_smooth_1`,
`turbulent_Gnielinski_smooth_2`, `turbulent_Churchill_Zajic`,
`turbulent_ESDU`, `turbulent_Martinelli`, `turbulent_Nunner`,
`turbulent_Dipprey_Sabersky`, `turbulent_Gowen_Smith`,
`turbulent_Kawase_Ulbrecht`, `turbulent_Kawase_De` and `turbulent_Bhatti_Shah`,
version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one
EES `FUNCTION` named after the `ht` function (with the `Nu_` prefix of the
library convention), the two Python default arguments of
`turbulent_Dittus_Boelter` (`heating`, `revised`) became explicit 1/0 flags,
the optional viscosity arguments of `turbulent_Sieder_Tate` became mandatory
(pass `mu = mu_w` for the form without the correction), and the Python
`log` became the EES `LN`. No equation was changed. Scientific basis per
function: the original paper or book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block
of each function and in `model.json` (`origin.authors`); the reference most of
them come from in `ht` is Rohsenow, Hartnett & Cho, *Handbook of Heat
Transfer*, 3E, McGraw-Hill, 1998.

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-96, family `HT-001`).** One EES
  `FUNCTION` per `ht` correlation (23 functions), named `Nu_<method>`, with the
  formula, the validity range as quoted by `ht`, the original reference and the
  `ht` module/function/version/commit in the comment block. Arguments are the
  Python arguments, all dimensionless or in SI (`Pa·s`, `m`); no property
  functions are used inside the functions, so the calling model passes Re, Pr,
  `fd`, `eD` itself (rule 5 of `sources/ht/README.md` §7).
- The two boolean options of `turbulent_Dittus_Boelter` (`heating`, `revised`)
  are **1/0 integer arguments** and the choice of the coefficient is made with
  a nested EES `IF` (the non-smooth regime switch, not a function call).
- `turbulent_Sieder_Tate`: `ht` makes `mu` and `mu_w` optional (no correction
  when they are absent); EES has no optional arguments, so they are mandatory
  and the caller passes `mu = mu_w` for the uncorrected form. Both calls are
  exercised in the demonstration program.
- `turbulent_Sandall`: the equation printed in the `ht` docstring shows
  `(fd/8)` in the numerator, its **code** uses `(fd/8)^0.5` (which is what
  reproduces its doctest value 229.0514352970239 at Re = 10⁵, Pr = 1.2,
  fd = 0.0185). The EES function follows the code; the discrepancy is noted in
  the function comment.
- `turbulent_Churchill_Zajic`: the intermediate quantities (`Pr_T`, `Nu_di`,
  `Nu_Dinf`) are local variables of the function, as `ht` computes them
  internally.
- **Selectors not translated**: `Nu_conv_internal` and
  `Nu_conv_internal_methods` only map a method name to a correlation; the
  caller chooses the `FUNCTION` directly.
- **Level**: equations 70 → 1 point (50–300), largest block 1 → 0,
  functions present → 1, multi-zone no → 0, semi-empirical/off-design no → 0,
  curated guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The two demonstration input sets are chosen to be realistic, not to stay
  inside every quoted validity range: some calls fall outside it (case A:
  `Nu_Dipprey_Sabersky` and `Nu_Bhatti_Shah` with eD = 10⁻³ < 0.0024 / 0.002,
  `Nu_Gowen_Smith` with Re = 10⁵ > 5·10⁴, `Nu_Kawase_De` with Pr = 1.2 < 5.1;
  case B: `Nu_Nunner`, `Nu_Colburn`, `Nu_Drexel_McAdams` and
  `Nu_Friend_Metzner` with Pr = 5 outside their Pr ranges). `ht` does not check
  the ranges in these functions, so its values are reproduced as they are; the
  numbers of the *Results* and *Verification* tables are a check of the
  **equations**, not recommended design values. The validity column of the table
  above is the one to use when choosing an input.
- No friction-factor correlation is included: `ht` has none (the pipe
  friction factors are in the companion library `fluids`); `CSL-0018` provides
  the Colebrook-White factor for smooth and rough pipes in EES.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES
  (`FUNCTION`, `IF/THEN/ELSE`, `LN`, `EXP`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0096` *plate_hx_heat_transfer*: another `ht` family of the same triage
  (single-phase Nusselt numbers and flow-boiling coefficients of the
  corrugated channel of a plate heat exchanger), same layout and same comment
  blocks; its arguments are the plate geometry and the fluid properties.
- `CSL-0018` *pipe_pressure_drop_colebrook*: the Darcy friction factor `fd` that
  most of these correlations take as an input.
- `CSL-0005` *cpbar_combustion_products* and `CSL-0079`
  *brineprop_secondary_refrigerants*: the other two function libraries of the
  library (same layout: definitions + demonstration program).
- `CSL-0088` *nucleate_boiling_and_chf*: the next family of the same `ht`
  triage (pool nucleate boiling and critical heat flux), same layout; its
  arguments are boiling-fluid properties instead of pipe dimensionless numbers.
- `CSL-0081` *vertical_ghes_refsim*: contains a local `Nusselt` procedure for
  the borehole heat transfer, an application of the same physics.
- `sources/labothappy` LTP-034 (in-tube HTC correlations quoting
  Dittus-Boelter and Gnielinski): the `ht` family is more complete and is the
  reference for the equations.
- `CSL-0089` *condensation_film*: the same `ht` triage, condensation side; its
  `h_Shah` uses the Dittus-Boelter coefficient of this file for the
  single-phase part of the two-phase film.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations of a heat
  exchanger (Cmin, Cmax, Cr, NTU<->UA, eps and NTU for the counterflow, parallel,
  crossflow and boiler/condenser arrangements) as EES functions; a rating model
  combines them with the heat-transfer coefficients of this file.
- `CSL-0092` *free_conv_cylinders*: the free-convection counterpart of this file
  (natural convection from vertical and horizontal cylinders, 13 functions), same
  layout and same comment blocks; its functions take Pr and Gr instead of Re, Pr
  and fd.
- `CSL-0093` *free_conv_plates_and_sphere*: the other free-convection family of
  the same `ht` triage (vertical plate, horizontal plate and sphere, 5 functions),
  same layout; it completes `CSL-0092` with the plate and sphere geometries.
- `CSL-0094` *external_crossflow_cylinder*: the **external** forced-convection
  counterpart of this file (single cylinder in crossflow, Zukauskas,
  Churchill-Bernstein, Sanitjai-Goldstein, Whitaker, Perkins-Leppert, 8
  functions), same layout; a crossflow tube bundle combines both.
- `CSL-0095` *tube_bank_nusselt*: the **tube-bank** forced-convection family of
  the same `ht` triage (Zukauskas with the Bejan fit, ESDU 73031, HEDH, and the
  row and inclination correction factors), same layout; a crossflow bundle
  combines its row/angle corrections with the single-cylinder Nu of this file.
- `CSL-0097` *two_phase_nonboiling_in_tube*: the two-phase non-boiling
  in-tube heat-transfer coefficients of the same `ht` triage (Davis-David,
  Groothuis-Hendal, Knott, Aggour, 9 functions), same layout; a tube carrying
  a condensing or evaporating mixture needs its single-phase Nu together with
  them.
- `CSL-0098` *flow_boiling_in_tubes*: the flow- and film-boiling
  coefficients of the same `ht` triage (Lazarek-Black, Li-Wu, Sun-Mishima,
  Thome, Yun-Heo-Kim, Chen, Liu-Winterton, plus Shah 1982 and Gungor-Winterton
  1987 from ThermoCycle, 10 functions), same layout; the Dittus-Boelter and
  Gnielinski coefficients of this file are written out in their bodies.
- `CSL-0100` *free_conv_enclosed_and_jackets*: the enclosed-plate, helical-coil
  and vessel-jacket correlations of the same `ht` triage (10 functions), same
  layout; this file and that one are the forced- and natural-convection
  counterparts.
- `CSL-0101` *external_forced_conv_plates*: the other **external** forced-convection geometry of the same `ht` module `ht/conv_external.py` (isothermal flat plate in crossflow: Baehr-Stephan and Churchill-Ozoe laminar, Schlichting and Kreith turbulent), same layout.
- `CSL-0103` *tube_bank_dp_bell_delaware*: the shell-side pressure drop of a
  shell-and-tube exchanger (Kern) and the Bell-Delaware correction factors
  `Jc`, `Jl`, `Jb`, `Js`, `Jr` of the same `ht` triage, same layout; a shell-side
  model pairs them with the bundle Nusselt numbers of `CSL-0095` and with the
  pipe correlations of this file.
- `CSL-0104` *supercritical_internal_nu*: the near-supercritical internal
  convection correlations of the same `ht` triage (McAdams, Jackson, Swenson,
  Kitoh, Petukhov …, 18 functions), same layout and same comment blocks; their
  Dittus-Boelter and Gnielinski coefficients are written out in their bodies.
  They apply to the same pipe flow once the wall temperature crosses the
  pseudo-critical point of the fluid (supercritical water, transcritical CO2).
- `CSL-0105` *lmtd_and_f_correction*: the LMTD relations (`LMTD`,
  `F_LMTD_Fakheri`, `Ft_aircooler`) of the same `ht` triage, same layout; a
  rating model combines the heat-transfer coefficients of this file with the
  mean temperature difference of that one.
- `CSL-0107` *radiation_heat_flux*: the radiation relations of the same `ht`
  triage (blackbody spectral radiance, grey-surface heat flux with
  back-radiation, grey transmittance, 3 functions), same layout; its
  temperatures are in °C with `T + 273.15` formed inside the functions.
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.
- `CSL-0108` *packed_bed_nusselt*: the packed-bed forced-convection family
  of the same `ht` triage (Gnielinski, Wakao-Kagei, Achenbach, KTA, 4
  functions), same layout and same comment blocks; its functions take the
  bed operating point (dp, voidage, vs, fluid properties) or Re, Pr and the
  void fraction instead of the pipe dimensionless numbers.
- `CSL-0106` *conduction_resistances_and_shapes*: the conduction family of the same `ht` triage (plane-wall and cylindrical-wall resistances, 6 shape factors, R-value conversions, 14 relations), same layout; no convection input is needed there, only geometry and `k`.
- `CSL-0109` *fin_efficiency_and_wall_factors*: the circular-fin efficiency and
  the Kays-Crawford wall correction factors of the same `ht` triage (3
  functions), same layout; its `(mu/mu_wall)^n` factors are the general form
  of the fixed-exponent Sieder-Tate correction of this file, and its `fd`
  factors apply to the same friction-factor inputs.

- `CSL-0128` *hx_eps_ntu_plate_pipe*: translation of the LaboThapPy
  `HexeNTU` component; `h_conv_pipe_htc` of that model calls `Nu_Gnielinski`
  (with `fd = 8*f` of the original transition branch) and `Nu_Sieder_Tate`
  for the turbulent branches of its pipe/canal convection coefficient, next to
  a laminar branch.
- `CSL-0130` *pipe_pressure_drop_correlations*: the six explicit Darcy
  friction factors that can be computed for the `fd` argument of most functions
  of this file (smooth or rough pipe, single phase or supercritical CO2).
