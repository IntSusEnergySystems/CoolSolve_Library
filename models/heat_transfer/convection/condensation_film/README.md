# Film condensation: heat-transfer coefficients

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0089`

Six EES `FUNCTION`s returning the heat-transfer coefficient `h` of condensing
film: the Nusselt analysis of 1916 for a laminar film on a (possibly inclined)
flat plate, Boyko-Kruzhilin for a vertical tube or bundle, Akers-Deans-Crosser
for condensation in horizontal tubes, the molecular-kinetic resistance of the
vapor diffusing to the condensing surface, Cavallini-Smith-Zecchin for
forced-convection condensation inside a tube and Shah (1979) for condensation
inside a tube in reduced-pressure form. Every property, the mass flow rate, the
geometry and (for the in-tube forms) the quality `x` are **arguments**: no
property function is called inside the functions, so the calling model passes
the liquid and vapor properties itself. This is the third of the 24 `ht`
families planned for the library (roadmap cards C-96…C-119) and follows the
layout of `CSL-0087`.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; the properties are arguments) |
| **Size** | 80 equations after analysis (largest block: 1); 6 functions of 2–14 lines |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/condensation.py` (MIT); inventory row `HT-003` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (18 values, max deviation 2.0·10⁻¹²) |

## Problem statement

Condensation is a heat-transfer problem with a *moving* interface: the vapor
condenses on a wall, the condensate falls as a film and the film is the thermal
resistance. Six historical correlations give the resulting heat-transfer
coefficient `h` for the main configurations:

- a laminar film on a flat plate, where the analytical solution of Nusselt
  still holds (flat-plate condenser of a steam plant);
- a laminar film inside a vertical tube or a bundle (Boyko-Kruzhilin), which
  covers most shell-side condensers;
- condensation in horizontal tubes (Akers-Deans-Crosser), with two branches of
  the original correlation;
- the molecular-kinetic resistance of the vapor, small in practice but the only
  term that grows when the condensate film is removed perfectly;
- condensation inside a tube with the vapor and the liquid flowing together
  (Cavallini-Smith-Zecchin and Shah), i.e. the two-phase heat-transfer
  coefficients a refrigeration or ORC condenser design needs.

The choice between them is left to the user, who knows the fluid, the geometry
and the flow regime.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `h_Nusselt_laminar` | Tsat, Tw, rhog, rhol, kl, mul, Hvap, L, angle | h = 0.943·[g·sin(θ)·rhol·(rhol − rhog)·kl³·Hvap / (mul·(Tsat − Tw)·L)]^0.25 | none quoted (laminar film, pure substance) |
| `h_Boyko_Kruzhilin` | m, rhog, rhol, kl, mul, Cpl, D, x | h = h_LO·[1 + x·(rhol/rhog − 1)]^0.5, h_LO = 0.021·kl/D·Re_LO^0.8·Pr_l^0.43 | none quoted (vertical tube or bundle, pure substance) |
| `h_Akers_Deans_Crosser` | m, rhog, rhol, kl, mul, Cpl, D, x | Nu = C·Re_e^n·Pr_l^(1/3), h = Nu·kl/D, C = 0.0265, n = 0.8 for Re_e > 5·10⁴; C = 5.03, n = 1/3 for Re_e < 5·10⁴; Re_e = D·G·[(1 − x) + x·(rhol/rhog)^0.5]/mul | the two branches of the original; no other limit quoted |
| `h_kinetic` | T, P, MW, Hvap, f | h = (2f/(2 − f))·(MW/(1000·2·π·R·T))^0.5·(Hvap²·P·MW)/(1000·R·T²) | none quoted |
| `h_Cavallini_Smith_Zecchin` | m, x, D, rhol, rhog, mul, mug, kl, Cpl | Nu = 0.05·Re_eq^0.8·Pr_l^0.33, Re_eq = Re_g·(mug/mul)·(rhol/rhog)^0.5 + Re_l, h = Nu·kl/D | none quoted (forced-convection condensation in a tube) |
| `h_Shah` | m, x, D, rhol, mul, kl, Cpl, P, Pc | h = h_L·[(1 − x)^0.8 + 3.8·x^0.76·(1 − x)^0.04/Pr^0.38], h_L = 0.023·Re_L^0.8·Pr_l^0.4·kl/D, Pr = P/Pc | none quoted (condensation inside a tube) |

Arguments: Tsat [K] saturation temperature, Tw [K] wall temperature, `T` [K]
vapor temperature, `P` [Pa] vapor pressure, rhog / rhol [kg/m³] vapor and liquid
densities, kl [W/m·K⁻¹] liquid thermal conductivity, mul / mug [Pa·s] liquid and
vapor viscosities, Cpl [J·kg⁻¹·K⁻¹] liquid constant-pressure heat capacity,
Hvap [J/kg] heat of vaporization, `L` [m] plate length, `angle` [deg] plate
inclination, `m` [kg/s] mass flow rate, `D` [m] tube or channel diameter,
`x` [−] quality at the interval, `Pc` [Pa] critical pressure, MW [g/mol]
molecular weight, `f` [−] kinetic-resistance correction factor.

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. The scientific basis is
Hewitt, G. L., G. F. Shires and T. R. Bott, *Process Heat Transfer*, 1E, CRC
Press, 1994 (Nusselt 1916 and Boyko-Kruzhilin), Kakaç, S. (ed.), *Boilers,
Evaporators, and Condensers*, 1st ed., Wiley-Interscience, 1991 (Akers-Deans-
Crosser, Berman, Cavallini-Smith-Zecchin, Shah), plus the original articles
quoted there and in the `ht` docstrings.

`h_kinetic` is not a film coefficient: it is the **kinetic (diffusion)
resistance** of the vapor, used as a correction of the condensation
heat-transfer coefficient. `ht` gives its factor `f` the default value 1; here
`f` is an argument (as `ht` documents it, `f` is quite close to one).

`h_Shah` calls the Dittus-Boelter correlation for its single-phase coefficient
`h_L` with the default arguments of `ht` (heating and revised coefficients); in
this library that correlation is `Nu_Dittus_Boelter` of `CSL-0087`, but the
equation is written out in the function so that the file stays self-contained
(`$INCLUDE library:…` is not supported yet, `CS-FEAT-IMPORT`).

No member of the `ht` family is a dispatcher, so nothing is excluded from the
translation.

## How to run

Open `condensation_film.eescode` in the CoolSolve GUI and press *Solve*, or
from a terminal:

```bash
coolsolve ./condensation_film.eescode
```

The demonstration program after the definitions calls each function at least
once: case *A* with the input set of the `ht` doctest of the corresponding
correlation (published values), case *B* with one uniform, realistic input set
(R134a condensing at 40 °C in a 24 mm tube, 0.4 kg/s, quality 0.6, wall 10 K
below saturation). The regime switch of `h_Akers_Deans_Crosser` (the two
branches at Re_e = 5·10⁴) and the inclination of `h_Nusselt_laminar` (60° and
45°) and the factor `f` of `h_kinetic` (1 and 0.9/0.95) are exercised twice.
The file solves without any iteration (`Solver: SUCCESS (0 iterations)`, every
equation is explicit) and is the regression baseline (`condensation_film.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0089 ---}` and
lists `CSL-0089` in its `related` field.

## Results

Values of the demonstration program (full precision in
`condensation_film.sol`):

| Quantity (case A) | h [W/m²·K⁻¹] | Quantity (case B) | h [W/m²·K⁻¹] |
|---|---:|---|---:|
| `h_Nusselt_laminar` (vertical plate) | 1482.21 | | 1284.81 |
| `h_Nusselt_laminar_inclined` (45° / 60°) | 1359.19 | | 1239.43 |
| `h_Boyko_Kruzhilin` | 10 598.7 | | 7339.01 |
| `h_Akers_Deans_Crosser` (Re_e = 7.7·10⁵) | 7117.24 | (Re_e = 3.4·10⁵) | 5407.62 |
| `h_Akers_Deans_Crosser_lowRe` (Re_e = 4.4·10⁴) | 929.27 | (Re_e = 1.7·10⁴) | 988.33 |
| `h_kinetic` (f = 1) | 3.079·10⁷ | | 2.890·10⁷ |
| `h_kinetic_f` (f = 0.9 / 0.95) | 2.519·10⁷ | | 2.615·10⁷ |
| `h_Cavallini_Smith_Zecchin` | 5578.22 | | 10 168.2 |
| `h_Shah` | 2561.26 | | 6619.72 |

Sanity checks of the numbers above (case B, R134a at 40 °C, 24 mm tube):

- G = m/(π/4·D²) = 884.2 kg·m⁻²·s⁻¹ and Re_L = ρ_L·G·D/μ_L = 8.49·10⁴;
  Pr_l = μ_L·Cp_L/k_L = 2.79; reduced pressure P/Pc = 0.394.
- `h_Nusselt_laminar` decreases with the inclination as sin^0.25(θ):
  1239.43/1284.81 = 0.9646 = sin(60°)^0.25 ✓.
- the four in-tube correlations agree within a factor 2 of each other for the
  same state (5407.6 Akers-Deans-Crosser, 6619.7 Shah, 7339.0 Boyko-Kruzhilin,
  10 168.2 W·m⁻²·K⁻¹ Cavallini-Smith-Zecchin), one order of magnitude above the
  pool film value 1284.8 W·m⁻²·K⁻¹ of the vertical plate, as expected when the
  condensate is swept away by the vapour.
- `h_kinetic` is about four orders of magnitude larger than the film
  coefficients (2.89·10⁷ against 1.3·10³…10⁴ W·m⁻²·K⁻¹); as in the original,
  the kinetic resistance is negligible in practice, it matters only when the
  condensate film is removed perfectly.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the six
     coefficients for one condensing state of R134a (x = 0.6) against the
     quality x, or h vs plate inclination for h_Nusselt_laminar,
     figures/condensation_film_h_x.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/condensation.py`, commit `85e0ee6`, installed from the local clone in a
throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for case *B*. The 18 output values of the demonstration
program were compared with `CoolSolve/tools/compare_solution.py` (tolerance
`rtol = 0.001`):

```
18 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 63
```

(the 63 “only in CoolSolve” variables are the 63 inputs of the demonstration
program; the reference table holds only the 18 outputs). The largest relative
deviation over the 18 values is **2.0·10⁻¹²** (`h_Shah_A`), i.e. round-off in
the double-precision evaluation.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. | Function (case B) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|---|---:|---:|---:|
| `h_Nusselt_laminar` | 1482.206403 | 1482.206403 | 2.2e-13 | `h_Nusselt_laminar` | 1284.814013 | 1284.814013 | 2.4e-13 |
| `h_Nusselt_laminar_inclined` | 1359.189265 | 1359.189265 | 9.0e-14 | `h_Nusselt_laminar_inclined` | 1239.432622 | 1239.432622 | 3.4e-13 |
| `h_Boyko_Kruzhilin` | 10 598.657227 | 10 598.657227 | 4.1e-15 | `h_Boyko_Kruzhilin` | 7339.007058 | 7339.007058 | 8.7e-14 |
| `h_Akers_Deans_Crosser` | 7117.241773 | 7117.241773 | 1.4e-15 | `h_Akers_Deans_Crosser` | 5407.618921 | 5407.618921 | 7.0e-14 |
| `h_Akers_Deans_Crosser_lowRe` | 929.274274 | 929.274274 | 1.1e-14 | `h_Akers_Deans_Crosser_lowRe` | 988.326606 | 988.326606 | 3.7e-14 |
| `h_kinetic` | 3.0788830e7 | 3.0788830e7 | 3.7e-14 | `h_kinetic` | 2.8901301e7 | 2.8901301e7 | 1.8e-14 |
| `h_kinetic_f` | 2.5190861e7 | 2.5190861e7 | 1.8e-13 | `h_kinetic_f` | 2.6148797e7 | 2.6148797e7 | 1.7e-14 |
| `h_Cavallini_Smith_Zecchin` | 5578.218369 | 5578.218369 | 2.2e-12 | `h_Cavallini_Smith_Zecchin` | 10 168.237008 | 10 168.237008 | 4.7e-13 |
| `h_Shah` | 2561.259342 | 2561.259342 | 2.0e-12 | `h_Shah` | 6619.723609 | 6619.723609 | 9.0e-14 |

The case *A* column reproduces the six `ht` doctest values exactly
(1482.206403453679, 10598.657227479956, 7117.24177265201, 30788829.908851154,
5578.218369177804 and 2561.2593415479214); the second call of
`h_Akers_Deans_Crosser` (Re_e = 4.4·10⁴ < 5·10⁴, the low branch),
`h_Nusselt_laminar_inclined` (45°) and `h_kinetic_f` (f = 0.9) were computed
with the same Python functions.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the film-condensation correlations of `ht`, the
heat-transfer component of ChEDL, file `ht/condensation.py`, functions
`Nusselt_laminar`, `Boyko_Kruzhilin`, `Akers_Deans_Crosser`, `h_kinetic`,
`Cavallini_Smith_Zecchin` and `Shah`, version 1.2.0, commit 85e0ee6
(2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` named after the `ht` function with the `h_` prefix of the library
convention; the optional `angle` of `Nusselt_laminar` and the optional factor
`f` of `h_kinetic` became mandatory arguments (both are exercised in the
demonstration program); the Python `pi` and `math.sin` became the local
constant `pi_val` and the EES `SIN` (see the conversion log). No equation was
changed. Scientific basis per function: the original paper or book quoted in
its comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`); the books `ht` takes them
from are Hewitt, Shires & Bott, *Process Heat Transfer*, 1994, and Kakaç (ed.),
*Boilers, Evaporators, and Condensers*, 1991.

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-98, family `HT-003`).** One EES
  `FUNCTION` per `ht` correlation (6 functions), named `h_<method>`, with the
  formula, the validity range as quoted by `ht`, the original reference and the
  `ht` module/function/version/commit in the comment block. Arguments are the
  Python arguments in SI units (K, Pa, kg/s, kg/m³, W/m/K, Pa·s, J/kg, m, deg);
  no property functions are used inside the functions, so the calling model
  passes the properties itself (rule 5 of `sources/ht/README.md` §7).
- **Units**: the source is already SI (K, Pa, kg/s), no `$UnitSystem`
  conversion was needed. The one hand conversion is the angle of
  `h_Nusselt_laminar`: `ht` calls `sin(angle*pi/180)` with `angle` in degrees,
  and the trigonometric functions of EES (setting `DEG`) and of CoolSolve take
  degrees (`CS-DOC-TRIG`, `docs/ees_import.md` §6 step 6), so the function
  reads `sin(angle)` — same physical angle.
- **`pi` inside a function body**: written as the local constant
  `pi_val = 3.141592653589793` (with the comment “pi, as a local constant
  (see the header)”) instead of the EES constant `pi`, because CoolSolve does
  not resolve `pi`/`PI` inside a `FUNCTION` body and evaluates it as **1**,
  silently (registered with this card as `CS-BUG-PI-FUNCTION`; the EES function
  form `pi()` does work in CoolSolve, but a plain local assignment is valid in
  both). This changes no equation.
- `Akers_Deans_Crosser`: the non-smooth regime switch of the original
  (Re_e > 5·10⁴ or < 5·10⁴) is written as an EES `IF/THEN/ELSE` block, not as a
  function call; both branches are exercised in the demonstration program.
- `Shah`: the single-phase coefficient h_L of the Dittus-Boelter correlation is
  written out in the body (`Nu_L = 0.023*Re_L^0.8*Pr_l^0.4`, the default
  heating/revised coefficients of `ht`) instead of calling the correlation of
  `CSL-0087`, which cannot be imported yet (`CS-FEAT-IMPORT`).
- `Boyko_Kruzhilin`: the docstring of `ht` writes a length `L` in h_LO, its
  **code** (and the published value it reproduces, Hewitt p. 589) uses the tube
  diameter `D` — as here; the difference is noted in the function comment.
- `Nusselt_laminar`: the coefficient is written `2*2^0.5/3` (the code of `ht`),
  which is the 0.943 of the original; writing the rounded 0.943 would shift the
  result by 2.0·10⁻⁴ relative.
- **Selectors not translated**: none in this family (`ht` has no dispatcher in
  `condensation.py`).
- **Level**: equations 80 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The two demonstration input sets are chosen to be realistic, not to stay
  inside every quoted validity range: `ht` quotes almost no range for these six
  correlations, so the values of the *Results* and *Verification* tables are a
  check of the **equations**, not recommended design values. The case *A*
  inputs of two in-tube correlations (very small liquid viscosity, e.g.
  mul = 1·10⁻⁵ Pa·s, and a vapor viscosity ten times larger) are the published
  ones and are reproduced as they are.
- `h_Nusselt_laminar` is the laminar film theory: it is not valid for a wavy
  or stratified film, for a horizontal plate (angle = 0) or where the
  condensate leaves the plate.
- `h_kinetic` returns a coefficient about four orders of magnitude larger
  than the film coefficients; it is a resistance term to be **combined** with them, not a
  replacement (as in the original).
- **CoolSolve bug `CS-BUG-PI-FUNCTION`** (registered with this card): the `pi`
  constant evaluates as 1 inside a `FUNCTION` body, silently. Worked around
  with the local constant `pi_val`; the model is not blocked, so the ID is not
  listed in `missing_features`.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No other gap: everything else is plain EES (`FUNCTION`, `IF/THEN/ELSE`, `SIN`)
  and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the turbulent in-pipe correlations
  of the same `ht` triage; its `Nu_Dittus_Boelter` is the single-phase
  coefficient `h_L` used by `h_Shah`.
- `CSL-0088` *nucleate_boiling_and_chf*: the same layout for the boiling side
  of the two-phase heat transfer (nucleate boiling and critical heat flux).
- `CSL-0027` *shell_and_tube_steam_condenser* and `CSL-0031`
  *refrigeration_evaporator_wet_coil*: condenser/evaporator component models
  that could use these in-tube film coefficients (`CSL-0031` condenses on the
  air side of a coil).
- `sources/thermo_models` TM-0585 (plate heat exchanger, Kuo-Lie-Hsieh-Lin
  condensation correlation): a different geometry, to be cross-checked.
- `sources/tespy` TSP-009 (condenser component, not a heat-transfer coefficient
  correlation): the `ht` family is the reference for the correlations.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations of a heat
  exchanger (Cmin, Cmax, Cr, NTU<->UA, eps and NTU for the counterflow, parallel,
  crossflow and boiler/condenser arrangements) as EES functions; a condenser
  model combines them with the film coefficients of this file.
- `CSL-0092` *free_conv_cylinders*: natural convection from vertical and
  horizontal cylinders (13 functions of the same `ht` module and layout); the
  laminar natural-convection number that accompanies the film coefficients of
  this file comes from its `Nu_vertical_cylinder_*` / `Nu_horizontal_cylinder_*`
  functions.
- `CSL-0094` *external_crossflow_cylinder*: the forced-convection counterpart
  of this file for a tube in crossflow (8 `FUNCTION`s of the same `ht`
  layout); a condensing tube in an air crossflow uses both.
- `CSL-0097` *two_phase_nonboiling_in_tube*: the two-phase non-boiling
  in-tube heat-transfer coefficients of the same `ht` triage (Davis-David,
  Groothuis-Hendal, Hughmark, Knott, Aggour, 9 functions), same layout; they
  rate an in-tube flow without phase change, where the film correlations of
  this file are the side that has one.
- `CSL-0098` *flow_boiling_in_tubes*: the flow- and film-boiling
  coefficients of the same `ht` triage plus Shah 1982 and Gungor-Winterton
  1987 from ThermoCycle (10 functions), same layout; like h_Shah of this file,
  they start from the Dittus-Boelter coefficient of `CSL-0087`.
- `CSL-0100` *free_conv_enclosed_and_jackets*: the Nusselt numbers of the coil
  around which the film of this file condenses.
