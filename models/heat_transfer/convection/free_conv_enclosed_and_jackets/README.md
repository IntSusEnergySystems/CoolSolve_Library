# Natural convection in enclosures and vessels: plates, critical Rayleigh numbers, helical coils, vessel jackets

🔵 **Level 2 · Intermediate**  |  🧩 **Function library**  |  ✅ **Verified**  |  `CSL-0100`

Ten EES `FUNCTION`s for the natural convection of a fluid layer enclosed between
plates, of a helical coil in a tank and of the fluid in a vessel jacket: the
Nusselt numbers of the Rayleigh–Bénard problem between parallel horizontal
plates (Hölling–Herwig, Probert, Hollands), between vertical plates (Thess), the
critical Rayleigh number of parallel disks, the coil correlations of Ali,
Prabhanjan–Rennie–Raghavan and Xin–Ebadian, and the average heat-transfer
coefficients of the jackets of Lehrer and Stein–Schmidt. Ten of the twelve
functions of the `ht` family `HT-014` are translated; the two exceptions and the
reason are listed under *Not translated* below. The heat-transfer coefficients
of the plates and coils follow from `h = Nu*k/L` and are left to the caller, as
in the source library; the two jacket correlations return `h` directly.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Pr, Gr, the geometry and the jacket fluid properties are arguments) |
| **Size** | 69 equations after analysis (largest block: 1); 10 functions of 6–31 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), files `ht/conv_free_enclosed.py`, `ht/conv_free_immersed.py` (one function) and `ht/conv_jacket.py` (MIT); inventory row `HT-014` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (33 values, max deviation 8.8·10⁻¹³) |

## Problem statement

Three situations are covered.

1. **Enclosed layers.** Between two horizontal plates (the Rayleigh–Bénard
   problem) the Nusselt number is known only as a correlation of the Rayleigh
   number `Ra = Gr·Pr`; above the critical Rayleigh number (1708 for infinite
   plates, higher for a finite box) convection sets in and `Nu` rises with
   `Ra`. Two of the correlations take the critical Rayleigh number of the
   actual geometry as an argument, so they describe finite boxes and disks.
2. **Helical coils in tanks.** A coil immersed in a still fluid is cooled (or
   heated) by natural convection; the three correlations give `Nu` with respect
   to the total length of the coil or to its outer diameter.
3. **Vessel jackets.** The heat-transfer coefficient of the jacket fluid — which
   is driven both by the inlet velocity and, in a radial inlet, by the buoyancy
   of the temperature difference across the vessel height — is returned directly
   in `W/m²·K` for a tangential or a radial inlet, with or without the natural
   convection contribution.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_Nusselt_Rayleigh_Holling_Herwig_err` | Nu, Ra, D2 | residual `err = Ra^(1/3)·[0.05·ln(Ra·Nu/16) + D2]^(−4/3) − Nu`, set to zero by the caller (`D2 = 2·(−14.94/Ra^0.25 + 3.43)`) | `Ra ≥ Rac = 1708`; 10⁵ < Ra < 10¹⁵ recommended |
| `Nu_Nusselt_Rayleigh_Probert` | Pr, Gr, buoyancy | Nu = 0.208·Ra^0.25 (laminar, Ra ≤ 2.2·10⁴), Nu = 0.092·Ra^(1/3) (turbulent); Nu = 1 if not buoyancy-assisted or Ra < 1708 | none quoted ("rough model") |
| `Nu_Nusselt_Rayleigh_Hollands` | Pr, Gr, buoyancy, Rac | Nu = 1 + [1 − Rac/Ra]⁺·[k₁ + 2·(Ra^(1/3)/k₂)^(1 − ln(Ra^(1/3)/k₂))]⁺ + [(Ra/5803)^(1/3) − 1]⁺·t₅, k₁ = 1.44/(1 + 0.018/Pr + 0.00136/Pr²), k₂ = 75·exp(1.5·Pr^(−0.5)), t₅ = 1 for Rac = 1708 else 1 − exp(−0.95·[(Ra/Rac)^(1/3) − 1]⁺) | supports real, finite plates through Rac |
| `Nu_Nusselt_vertical_Thess` | Pr, Gr, H, L, geometry | Nu = 0.42·Pr^0.012·Ra^0.25·(L/H)^0.25 (10⁴ < Ra < 10⁷, geometry known), Nu = 0.049·Ra^0.33 (otherwise) | H/L < 80 recommended |
| `Rac_Nusselt_Rayleigh_disk` | H, D, insulated | Rac = exp(1/p(x)), x = min(max(D/H, 0.4), 6), p the 17-coefficient polynomial of Buell–Catton at 0.357143·(x − 3.2) | 0.4 ≤ D/H ≤ 6 (values outside are clamped) |
| `Nu_vertical_helical_coil_Ali` | Pr, Gr | Nu_L = 0.555·Gr_L^0.301·Pr^0.314 | 4.4 ≤ Pr ≤ 345, 10 ≤ D_tank/D_coil ≤ 30 |
| `Nu_vertical_helical_coil_Prabhanjan_Rennie_Raghavan` | Pr, Gr | Nu_H = 0.0749·Ra_H^0.3421 | 9·10⁹ < Ra < 4·10¹¹ |
| `Nu_coil_Xin_Ebadian` | Pr, Gr, horizontal | Nu_D = 0.318·Ra_D^0.293 (horizontal), 0.290·Ra_D^0.293 (vertical) | 5·10³ < Ra < 10⁵ |
| `h_jacket_Lehrer` | m, Dtank, Djacket, H, Dinlet, rho, Cp, k, mu, muw, isobaric_expansion, dT, radial_inlet, bottom_inlet | Nu_S,L = [0.03·Re_S^0.75·Pr/(1 + 1.74·(Pr−1)/Re_S^0.125)]·(mu/mu_w)^0.14, h = Nu_S,L·k/d_g, d_g = (8/3)^0.5·δ, v_h = (v_s·v_inlet)^0.5 + v_A | none quoted |
| `h_jacket_Stein_Schmidt` | m, Dtank, Djacket, H, Dinlet, rho, Cp, k, mu, muw, rhow, radial_inlet, bottom_inlet, fd | Nu_J = (Nu_A³ + Nu_B³ + Nu_C³ + Nu_D³)^(1/3)·(mu/mu_w)^0.14 with Nu_A = 3.66, Nu_B = 1.62·Pr^(1/3)·Re_J,eq^(1/3)·(d_ch/l_ch)^(1/3), Nu_C = 0.664·Pr^(1/3)·(Re_J,eq·d_ch/l_ch)^0.5, Nu_D = 0.0115·Pr^(1/3)·Re_J,eq^0.9·(1 − (2300/Re_J,eq)^2.5)·(1 + (d_ch/l_ch)^(2/3)) for Re_J,eq ≥ 2300 (else 0); h = Nu_J·k/d_ch | none quoted |

Arguments: Pr, Gr, Ra, Rac, `Nu`, D2 dimensionless `[−]`; H, L, Dtank,
Djacket, H, Dinlet, `fd` in m and `fd` `[−]`; jacket `m` [kg/s], `rho`
[kg/m³], `Cp` [J/kg/K], `k` [W/m/K], `mu` and `muw` [Pa·s], `rhow` [kg/m³],
`isobaric_expansion` [m³/mol/K], `dT` [K]; the flags `buoyancy`, `insulated`,
`horizontal`, `geometry`, `radial_inlet`, `bottom_inlet` are 1 (yes) or 0 (no).
Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. The scientific basis is
Hölling & Herwig (2006), Probert, Brooks & Dixon (1970), Hollands (1984),
VDI Heat Atlas (2010) for the plates, Rohsenow, Hartnett & Cho (1998) and
Buell & Catton (1983) for the critical Rayleigh numbers, Ali (2006),
Prabhanjan, Rennie & Raghavan (2004), Xin & Ebadian (1996) for the coils,
Lehrer (1970) and Stein & Schmidt (1993) for the jackets.

**Arguments that are optional in `ht`** become mandatory here, following the
convention of `CSL-0087`: a boolean is a 1/0 flag (`buoyancy`, `insulated`,
`horizontal`, `geometry`, `radial_inlet`, `bottom_inlet`), and an optional
number is passed as **0 to omit it** (`muw` = 0 → no viscosity correction,
`rhow` = 0 → purely forced flow, `isobaric_expansion`/`dT` → only used for a
radial inlet). The Python strings `'tangential'`/`'radial'`,
`'auto'`/`'bottom'`/`'top'` become the flags `radial_inlet` and
`bottom_inlet`.

### Not translated

* **`Nu_Nusselt_Rayleigh_Holling_Herwig`** — the correlation itself is *implicit*
  in `Nu` (no closed form exists, as `ht` itself notes) and `ht` obtains the root
  with a secant iteration. Its residual is translated as
  `Nu_Nusselt_Rayleigh_Holling_Herwig_err` and the demonstration program solves
  it as a simultaneous equation of the main program, which is how EES obtains the
  root:
  `Nu = Nu + Nu_Nusselt_Rayleigh_Holling_Herwig_err(Nu, Ra, D2)`.
  The residual evaluated at the root is a value of the program, so the
  reproduction of the doctest value 77.5466 is verified as well. A root-returning
  `FUNCTION` would be wrong in CoolSolve (see *Limitations and CoolSolve gaps*).
* **`Rac_Nusselt_Rayleigh`** — the critical Rayleigh number of a finite
  rectangular box is a bivariate B-spline fit (SciPy `bisplrep`/`bisplev`, 81 and
  144 coefficients) of Catton's table; it is not expressible as EES equations,
  and reading a table inside a `FUNCTION` is the registered gap
  `CS-GAP-LOOKUP-PROC`. `Rac_Nusselt_Rayleigh_disk`, the equivalent for disks,
  is a polynomial and **is** translated; for plates of infinite extent the
  critical Rayleigh number is the constant 1708 (used by `ht` as the default of
  `Rac_Nusselt_Rayleigh` and of `Nu_Nusselt_Rayleigh_Hollands`). The two
  demonstration calls that pass a box value (606001 for a 1 × 2 × 0.2 m box and
  6974 for a 1 m³ cube, the values `ht` returns) exercise the `Rac ≠ 1708`
  branch of `Nu_Nusselt_Rayleigh_Hollands`.
* **`Nu_free_vertical_plate` / `Nu_free_vertical_plate_methods`** — dispatchers
  that map a method name to a correlation; an EES caller calls the chosen
  `FUNCTION` directly.

## How to run

Open `free_conv_enclosed_and_jackets.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./free_conv_enclosed_and_jackets.eescode
```

The demonstration program after the definitions calls each of the ten functions
twice: once (case *A*) with the input set of the `ht` doctest of the
corresponding correlation, once (case *B*) with a second input set (plates:
Pr = 1, Gr = 10⁶; coils: Pr = 100 and 7; jacket: a 5 kg/s cooling-water jacket on
a 0.6 m tank of 1 m height, radial inlet at the bottom). It solves in 9
iterations (the two implicit equations of the Holling–Herwig correlation, 5
iterations each) and is the regression baseline
(`free_conv_enclosed_and_jackets.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0100 ---}` and
lists `CSL-0100` in its `related` field.

## Results

Values of the demonstration program (full precision in
`free_conv_enclosed_and_jackets.sol`):

| Quantity (case A) | value | Quantity (case B) | value |
|---|---:|---|---:|
| `Nu_HH` (Hölling–Herwig, root of the residual) | 77.547 | (Pr = 1, Gr = 10⁶) | 8.1234 |
| `…Holling_Herwig_err` (residual at the root) | 2.8·10⁻¹⁴ | | 7.3·10⁻¹² |
| `…Holling_Herwig_noboy` (buoyancy = 0) | 1.0000 | | |
| `Nu_Nusselt_Rayleigh_Probert` | 111.46 | | 9.2000 |
| `…Probert_noboy` / `…Probert_sub` (Ra < 1708) | 1.0000 / 1.0000 | | |
| `Nu_Nusselt_Rayleigh_Hollands` (Rac = 1708) | 69.027 | | 7.1116 |
| `…Hollands_Rac_A1` (Rac = 606001) | 4.6662 | | |
| `…Hollands_Rac_A2` (Rac = 6974) | 8.7864 | | |
| `Nu_Nusselt_vertical_Thess` (geometry unknown) | 6.1126 | (H = 1 m, L = 4 m) | 22.337 |
| `Nu_Nusselt_vertical_Thess_geom` (H = 1 m, L = 10 m) | 28.793 | | |
| `Rac_Nusselt_Rayleigh_disk` (D/H = 0.4, uninsulated) | 151 200 | (D = 2 m, insulated) | 2266.9 |
| `Rac_Nusselt_Rayleigh_disk_ins` (D/H = 0.5, insulated) | 24 347 | | |
| `Nu_vertical_helical_coil_Ali` | 1808.6 | (Pr = 100, Gr = 10¹⁰) | 2411.5 |
| `Nu_vertical_helical_coil_Prabhanjan_Rennie_Raghavan` | 720.62 | (Pr = 100, Gr = 10⁹) | 434.09 |
| `Nu_coil_Xin_Ebadian` (vertical) | 4.7557 | (Pr = 7, Gr = 10⁴) | 7.6210 |
| `Nu_coil_Xin_Ebadian_horiz` (horizontal) | 5.2149 | | |
| `h_jacket_Lehrer` [W/m²·K] (tangential inlet) | 2922.1 | (radial inlet, cooling) | 1114.6 |
| `h_jacket_Lehrer_radial` (radial, buoyancy) | 3269.4 | | |
| `h_jacket_Lehrer_novisc` (mu_w = 0) | 2608.9 | | |
| `h_jacket_Stein_Schmidt` [W/m²·K] (tangential) | 5695.2 | (radial, cooling) | 1266.7 |
| `h_jacket_Stein_Schmidt_nograv` (rhow = 0) | 5685.5 | | |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): Nu vs Ra for the
     three enclosed-plate correlations at Pr = 1 and Pr = 100, or the critical
     Rayleigh number of two parallel disks vs D/H,
     figures/free_conv_enclosed_and_jackets_nu_ra.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_free_enclosed.py`, `ht/conv_free_immersed.py`, `ht/conv_jacket.py`,
commit `85e0ee6`, installed from the local clone in a throw-away virtual
environment) for case *A*, plus values computed with the same Python functions
for case *B*. The 33 output values of the demonstration program were compared
with `CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
33 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 36
```

(the 36 “only in CoolSolve” variables are the 36 inputs and intermediate
quantities of the demonstration program — `Pr_A`, `Gr_A`, `Ra_A`, `D2_A`, the
jacket geometry and fluid properties, their `_B` counterparts … —; the
reference table holds only the 33 outputs). The largest relative deviation over
the 33 values is **8.8·10⁻¹³** (`Nu_HH_B`), i.e. round-off in the double-precision
evaluation. The two residuals are compared against an exact zero, so they are
absolute: 2.8·10⁻¹⁴ (case A) and 7.3·10⁻¹² (case B), below the `atol = 10⁻⁹` of
the tool.

Per-function values, `ht` / CoolSolve:

| Quantity (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_HH_A` | 77.5465680189691 | 77.54656801897 | 1.1e-14 |
| `Nu_Nusselt_Rayleigh_Holling_Herwig_err_A` | 0 | 2.842170943e-14 | — (abs.) |
| `Nu_Nusselt_Rayleigh_Holling_Herwig_noboy_A` | 1 | 1 | 0 |
| `Nu_Nusselt_Rayleigh_Probert_A` | 111.461810482891 | 111.4618104829 | 7.8e-14 |
| `Nu_Nusselt_Rayleigh_Probert_noboy_A` | 1 | 1 | 0 |
| `Nu_Nusselt_Rayleigh_Probert_sub_A` | 1 | 1 | 0 |
| `Nu_Nusselt_Rayleigh_Hollands_A` | 69.0266864951016 | 69.02668649510 | 2.4e-14 |
| `Nu_Nusselt_Rayleigh_Hollands_Rac_A1` | 4.66624913187648 | 4.666249131876 | 1.0e-13 |
| `Nu_Nusselt_Rayleigh_Hollands_Rac_A2` | 8.78636261412954 | 8.786362614130 | 5.3e-14 |
| `Nu_Nusselt_vertical_Thess_A` | 6.11258756960278 | 6.112587569603 | 3.5e-14 |
| `Nu_Nusselt_vertical_Thess_geom_A` | 28.7932862604165 | 28.79328626042 | 1.2e-13 |
| `Rac_Nusselt_Rayleigh_disk_A` | 151199.999999994 | 151200.0000000 | 3.6e-14 |
| `Rac_Nusselt_Rayleigh_disk_ins_A` | 24347.3147921192 | 24347.31479212 | 3.4e-14 |
| `Nu_vertical_helical_coil_Ali_A` | 1808.57749972971 | 1808.577499730 | 1.6e-13 |
| `Nu_vertical_helical_coil_Prabhanjan_Rennie_Raghavan_A` | 720.621106771823 | 720.6211067718 | 3.2e-14 |
| `Nu_coil_Xin_Ebadian_A` | 4.75568972625045 | 4.755689726250 | 9.5e-14 |
| `Nu_coil_Xin_Ebadian_horiz_A` | 5.21485976878498 | 5.214859768785 | 4.1e-15 |
| `h_jacket_Lehrer_A` | 2922.12812476183 | 2922.128124762 | 5.9e-14 |
| `h_jacket_Lehrer_radial_A` | 3269.43896326666 | 3269.438963267 | 1.1e-13 |
| `h_jacket_Lehrer_novisc_A` | 2608.86026937069 | 2608.860269371 | 1.2e-13 |
| `h_jacket_Stein_Schmidt_A` | 5695.20416980886 | 5695.204169809 | 2.4e-14 |
| `h_jacket_Stein_Schmidt_nograv_A` | 5685.53299155643 | 5685.532991557 | 1.0e-13 |

Case *B* (second input set, computed with the same Python functions):

| Quantity | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_HH_B` | 8.12338515963517 | 8.123385159628 | 8.8e-13 |
| `Nu_Nusselt_Rayleigh_Holling_Herwig_err_B` | 0 | 7.316813821e-12 | — (abs.) |
| `Nu_Nusselt_Rayleigh_Probert_B` | 9.2 | 9.200000000000 | 1.9e-16 |
| `Nu_Nusselt_Rayleigh_Hollands_B` | 7.1116470423549 | 7.111647042355 | 1.4e-14 |
| `Nu_Nusselt_vertical_Thess_geom_B` | 22.336842767169 | 22.33684276717 | 4.7e-14 |
| `Rac_Nusselt_Rayleigh_disk_B` | 2266.9035553026 | 2266.903555303 | 1.8e-13 |
| `Nu_vertical_helical_coil_Ali_B` | 2411.53174415222 | 2411.531744152 | 9.2e-14 |
| `Nu_vertical_helical_coil_Prabhanjan_Rennie_Raghavan_B` | 434.092035502052 | 434.0920355021 | 1.1e-13 |
| `Nu_coil_Xin_Ebadian_B` | 7.62099582351504 | 7.620995823515 | 5.8e-15 |
| `h_jacket_Lehrer_radial_B` | 1114.6153110982 | 1114.615311098 | 1.8e-13 |
| `h_jacket_Stein_Schmidt_radial_B` | 1266.66168454788 | 1266.661684548 | 9.5e-14 |

All 33 relative deviations are below 8.9·10⁻¹³.

Two input sets were needed for the jackets: with the demonstration case *B* of
the first attempt (1 kg/s instead of 5 kg/s) the buoyancy velocity of the radial
inlet exceeds the forced velocity, `v_h` becomes negative and `ht` returns a
**complex** number (−271.1 + 149.2·i); the correlation has no real value in that
case, as noted in the comment block of `h_jacket_Lehrer`. Case *B* therefore uses
5 kg/s.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the free-convection-in-enclosures and vessel-jacket
correlations of `ht`, the heat-transfer component of ChEDL: files
`ht/conv_free_enclosed.py`, `ht/conv_free_immersed.py` (function
`Nu_coil_Xin_Ebadian` only) and `ht/conv_jacket.py`, functions
`Nu_Nusselt_Rayleigh_Holling_Herwig_err`, `Nu_Nusselt_Rayleigh_Probert`,
`Nu_Nusselt_Rayleigh_Hollands`, `Nu_Nusselt_vertical_Thess`,
`Rac_Nusselt_Rayleigh_disk`, `Nu_vertical_helical_coil_Ali`,
`Nu_vertical_helical_coil_Prabhanjan_Rennie_Raghavan`, `Nu_coil_Xin_Ebadian`,
`Lehrer` and `Stein_Schmidt`, version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` (the two jacket correlations are named `h_jacket_Lehrer` and
`h_jacket_Stein_Schmidt` since they return `h`, not `Nu`), the optional
arguments of `ht` became mandatory arguments (1/0 flags and the “pass 0 to omit”
convention above), the Python `log` became the EES `LN`, and `pi` is written as
a local constant `pi_val` in the two jacket functions because CoolSolve does not
resolve `pi` inside a `FUNCTION` body (`CS-BUG-PI-FUNCTION`). No equation was
changed. Scientific basis per function: the original paper or book quoted in its
comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-109, family `HT-014`).** Ten EES
  `FUNCTION`s, named after the `ht` functions (`Nu_Nusselt_…`, `Rac_…`,
  `Nu_vertical_helical_coil_…`, `Nu_coil_…`, `h_jacket_…`), each with the
  formula, the validity range as quoted by `ht`, the original reference and the
  `ht` module/function/version/commit in its comment block. Arguments are the
  Python arguments, dimensionless or in SI (`m`, `kg/s`, `kg/m³`, `J/kg/K`,
  `W/m/K`, `Pa·s`, `K`, `m³/mol/K`); no property function is used inside a
  function, so the calling model passes Pr, Gr and the fluid properties (rule 5
  of `sources/ht/README.md` §7).
- `Nu_Nusselt_vertical_Thess`: the equation printed in the `ht` docstring shows
  `(H/L)^-0.25`, its **code** uses `(L/H)^0.25`, which is what reproduces its
  doctest values 6.1126 and 28.7933; the EES function follows the code, as
  `CSL-0087` does for `Nu_Sandall`.
- `Rac_Nusselt_Rayleigh_disk`: `ht` evaluates a 17-coefficient polynomial and
  then inverts it, `Rac = exp(1/p)`; both sets of coefficients are written out as
  local constants of the function and the polynomial is evaluated in the Horner
  scheme, which is what `fluids.numerics.horner` does.
- `h_jacket_Lehrer` and `h_jacket_Stein_Schmidt`: the strings `inlettype` and
  `inletlocation` became the flags `radial_inlet` and `bottom_inlet`; the sign of
  the buoyancy velocity `v_A` (Lehrer) and of the Grashof term of `Re_J,eq`
  (Stein–Schmidt) follows the nested `IF` of `ht`, i.e. it is *added* when the
  buoyancy assists the forced flow. `g` is written as the local constant
  `g_acc = 9.80665 m/s²` (the value of `fluids.constants.g`).
- `h_jacket_Stein_Schmidt`: `ht` runs five passes over the tangential-inlet
  velocity, refining the Darcy friction factor with the Colebrook formula of the
  current jacket Reynolds number at every pass; it uses the factor of the fourth
  pass. `ht` has no friction-factor correlation (it is in `fluids`), so `fd` is
  an argument of the EES function and the demonstration program passes
  0.020546184803580985, the value `ht` ends up with for case *A*; the calling
  model computes it (e.g. with `CSL-0018`).
- **Selectors not translated**: `Nu_free_vertical_plate` and
  `Nu_free_vertical_plate_methods` only map a method name to a correlation.
- **Level**: equations 69 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- `Nu_Nusselt_Rayleigh_Holling_Herwig` is implicit in `Nu`. Writing that
  equation inside a `FUNCTION` body is silently wrong in CoolSolve v0.3.0: the
  self-referencing equation is evaluated **once** with the initial guess (1) and
  the solver reports `SUCCESS (0 iterations)`. Minimal reproducer (the Holling–
  Herwig branch, valid EES):
  `FUNCTION Nu_Ray_Demo(Pr, Gr, buoyancy)` ⏎ `  Ra = Pr*Gr` ⏎
  `  IF buoyancy = 0 OR Ra < 1708 THEN` ⏎ `    Nu_Ray_Demo = 1` ⏎ `  ELSE` ⏎
  `    D2 = 2*(-14.94*Ra^-0.25 + 3.43)` ⏎
  `    Nu_Ray_Demo = Ra^(1/3)*(0.05*LN(Ra*Nu_Ray_Demo/16) + D2)^(-4/3)` ⏎ `  ENDIF`
  ⏎ `END` ⏎ `Nu_A = Nu_Ray_Demo(5.54, 3.21E8, 1)` → *SUCCESS (0 iterations)*,
  `Nu_A = 80.5043` instead of 77.5466. The same equation written in the main
  program (`Nu_A = Nu_A + Nu_Nusselt_Rayleigh_Holling_Herwig_err(Nu_A, Ra, D2)`)
  converges to 77.5466 in 5 iterations, which is what this model does. No gap is
  registered: no EES manual page or existing EES file was found here that shows
  an implicit equation inside a user function, so this is an *unverified
  suggestion* for the maintainer (roadmap Phase 5).
- `pi` is not resolved inside a `FUNCTION` body (`CS-BUG-PI-FUNCTION`,
  registered with `CSL-0089`): the two jacket functions use a local `pi_val`.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- The demonstration input sets are chosen to be realistic, not to stay inside
  every quoted validity range: one call is just outside it
  (`Nu_vertical_helical_coil_Prabhanjan_Rennie_Raghavan` case *A*,
  Ra = 4.4·10¹¹ > 4·10¹¹) and two sit exactly on a limit
  (`Nu_vertical_helical_coil_Ali` case *A*, Pr = 4.4 the lower end of 4.4–345;
  `Rac_Nusselt_Rayleigh_disk` case *A*, D/H = 0.4 the lower end of 0.4–6). `ht`
  does not check the ranges, so its values are reproduced as they are; the
  numbers of the *Results* and *Verification* tables check the **equations**,
  not recommended design values. The validity column of the table above is the
  one to use when choosing an input.
- No friction-factor correlation is included (as in `ht`); `CSL-0018` provides the
  Colebrook-White factor for smooth and rough pipes in EES.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` family of the library,
  same layout, same comment blocks and same demonstration program; its
  functions take Re, Pr and the Darcy friction factor, these take Pr, Gr, Rac
  and the geometry.
- `CSL-0092` *free_conv_cylinders* and `CSL-0093` *free_conv_plates_and_sphere*:
  the free-convection families of the same `ht` triage (cylinders; open plate
  and sphere), same layout; this file completes them with the *enclosed* layer,
  the coils and the jackets.
- `CSL-0089` *condensation_film*: the condensation side of the same triage; the
  Nusselt numbers of its film correlations and of this file are the two halves of
  a condensing or a boiling coil.
- `CSL-0009` *vessel_storage* and `CSL-0041*: agitated vessel models whose jacket
  or coil heat transfer can be rated with `h_jacket_Lehrer` or
  `h_jacket_Stein_Schmidt`.
- `CSL-0018` *pipe_pressure_drop_colebrook*: the Darcy friction factor that
  `h_jacket_Stein_Schmidt` needs for a tangential inlet.
- `CSL-0101` *external_forced_conv_plates*: the other **external** forced-convection geometry of the same `ht` module `ht/conv_external.py` (isothermal flat plate in crossflow: Baehr-Stephan and Churchill-Ozoe laminar, Schlichting and Kreith turbulent), same layout.
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.
