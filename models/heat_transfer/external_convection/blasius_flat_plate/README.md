# Blasius boundary layer over a flat plate

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0336`

Solution of the classic **Blasius equation** of the laminar boundary layer over
a flat plate, as in the EES example of F-Chart Software: the nonlinear
third-order ODE `f''' + 0.5·f·f'' = 0` is integrated with the `INTEGRAL`
function between the similarity coordinates η = 0 and η = 5, the shooting
parameter `f''(0)` being the classical 0.33206 (the value for which
`f'(η) → 1` at large η). The dimensionless velocity profile `f'(η)` is then
mapped to the dimensional coordinates *x* and *y* for air at 25 °C.

The **native file** `blasius_flat_plate.eescode` is valid EES but cannot be read
by CoolSolve, which refuses the prime notation of the original variable names
(`w'`, `w''`, `w'''`, `CS-GAP-NAME-PRIME`). The **runnable variant**
`blasius_flat_plate_coolsolve.eescode` renames those five variables and is
verified against the EES stored solution.

| | |
|---|---|
| **Category** | Heat transfer › External convection |
| **Fluids** | Air |
| **Size** | 20 equations; the `-d` analysis reports no blocks (`CS-DOC-SQUARE-INTEGRAL`: the block statistics of an `INTEGRAL` model are not usable) |
| **Source** | EES example library of F-Chart Software — `~/Nextcloud/thermo_models/EES_library/Blasius.EES` (EES X8.805); plain-text mirror: [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/blasius.ees) (MIT); inventory row `EEL-025` |
| **Authors** | S. A. Klein — the examples are © F-Chart Software |
| **License** | MIT (via the EES-Community mirror) |
| **CoolSolve** | 0.4.0 — native file **blocked** by `CS-GAP-NAME-PRIME`; the runnable variant is **verified** against the EES stored solution (see *Verification*) |

## Problem statement

The laminar boundary layer of a fluid flowing over an isothermal flat plate
reduces, with the similarity variable η = y/√(x·ν/U∞), to the Blasius boundary
value problem

    f''' + 0.5·f·f'' = 0        f(0) = 0,   f'(0) = 0,   f''(0) = unknown

with the boundary condition `f'(η) → 1` for η → ∞ (the velocity reaches the
free-stream value). The third initial condition is therefore a **shooting
parameter**: the classical solution is `f''(0) = 0.33206`. The model
integrates the ODE over η = 0 … 5 (`Stop = 5`, "it is traditional to use eta=5
as the top of the boundary layer", as in the original file) and gives the
dimensionless velocity profile `f'(η) = u/U∞`; the dimensional velocity at the
station *x* is obtained from `u = f'(η)·U∞` and the distance from the plate
from `y = η·√(x·ν/U∞)`.

**Niche.** `CSL-0101` *external_forced_conv_plates* is the flat-plate
Nusselt-number library of the library (Baehr-Stephan, Churchill-Ozoe,
Schlichting, Kreith): it returns the *average* heat-transfer coefficient of a
flat plate from the plate-length Reynolds number and the Prandtl number, with
the boundary layer represented by an empirical correlation. This model is one
level more fundamental in the modelling hierarchy: it solves the boundary-layer ODE
itself and returns the velocity profile and its derivatives (the skin-friction
and the displacement quantities follow from `f''(0)` and `f'(η)`), for a
prescribed free-stream velocity and a given Reynolds number. The two models
are complementary and are linked in both directions.

## Model

Governing equations (the names of the native file; the variant renames the
derivatives, see *Conversion log*):

| Equation | Meaning |
|---|---|
| `w''' + 0.5·w·w'' = 0` | Blasius equation, with w = f(η) the dimensionless velocity |
| `w_0 = 0`, `w'_0 = 0`, `w''_0 = 0.33206` | initial conditions; `w''_0` is the shooting parameter |
| `w = w_0 + INTEGRAL(w', eta, start, stop, step)` | the three states, integrated with the fixed step `step = 0.1` |
| `u\u_infinity = 1.5·(eta/5) − 0.5·(eta/5)³` | cubic in η of the original file (section *Integral solution*), not used by any equation |
| `Re = 1e5`, `Re = (u_infinity·x)/nu`, `x = 0.5` | free-stream conditions at the station *x* = 0.5 m |
| `mu = viscosity(air, T=T_air)`, `rho = density(air, T=T_air, P=101300)`, `nu = mu/rho` | properties of air at 25 °C and 1 atm |
| `eta = y/sqrt((x·nu)/u_infinity)` | similarity coordinate → distance from the plate |
| `u/u_infinity = w'` | dimensional velocity `u = f'(η)·U∞` |

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `w''_0` shooting parameter | 0.33206 | `w` = f(η = 5) | 3.283296 |
| `Stop` top of the boundary layer | 5 | `w'` = f'(η = 5) | 0.991547 |
| `step` integration step | 0.1 | `w''` = f''(η = 5) | 0.0159067 |
| `Re` Reynolds number | 1e5 | `u_infinity` free-stream velocity | 3.11475 m/s |
| `x` station | 0.5 m | `u` velocity at η = 5 | 3.08843 m/s |
| `T_air` air temperature | 25 °C | `y` distance from the plate | 7.9057e-3 m |

## How to run

The native file cannot be parsed by CoolSolve (prime notation in the variable
names). Run the **variant** instead:

```bash
coolsolve ./blasius_flat_plate_coolsolve.eescode
```

It solves without any guess file (the states start from the initial conditions
of the ODE) and writes the trajectory of the `$IntegralTable` directive
(η, w, w', w'', w''') in the `.sol` file. The variant uses no CoolSolve-only
syntax: it is valid EES and can be solved by EES as well.

To reproduce the shooting, change the value of `w''_0` and re-run (the
residual is `w' − 1` at the end of the integration; see *Verification*).

## Results

Run of `blasius_flat_plate_coolsolve.eescode` (CoolSolve 0.4.0):

| Quantity | Value |
|---|---|
| f(5) | 3.283296 |
| f'(5) | 0.991547 |
| f''(5) | 0.0159067 |
| f'''(5) | −0.0261132 |
| U∞ (from Re = 1e5 at x = 0.5 m) | 3.11475 m/s |
| u at η = 5 | 3.08843 m/s |
| y at η = 5 | 7.90569e-3 m |
| μ, ρ, ν of air at 25 °C, 1 atm | 1.84337e-5 Pa·s, 1.18364 kg/m³, 1.55738e-5 m²/s |

The profile reproduces the published Blasius solution: f(5) = 3.2833,
f'(5) = 0.9916 and f''(5) = 0.0159 (Schlichting, *Boundary-Layer Theory*;
White, *Viscous Fluid Flow*).

The solve ends with *ALL EQUATIONS SATISFIED* (17 equations checked, maximum
residual 1.46e-11). The `-d` analysis reports `System square: No` (21 variables
against the 20 equations of the window): for a model with `INTEGRAL` calls the
integral states are closed by the integrator and the block statistics are not
usable (`CS-DOC-SQUARE-INTEGRAL`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): trajectory of the
     integration (η, f, f', f''), e.g. from the CoolSolve GUI *Integral* tab,
     figures/blasius_flat_plate_integral.png -->

## Verification

1. **Against the EES stored solution** of the binary source file (the 16
   variables decoded from it by `tools/ees_extract.py`), with
   `compare_solution.py` (`rtol = 0.001`, `atol = 1e-9`):

   | Variable | EES | CoolSolve | rel. diff | |
   |---|---:|---:|---:|---|
   | w | 3.28267 | 3.2833 | 1.92e-04 | ok |
   | y | 0.00790569 | 0.00790569 | 5.33e-11 | ok |
   | u | 3.09728 | 3.08843 | 2.86e-03 | **DIFF** |
   | u_infinity | 3.12361 | 3.11475 | 2.84e-03 | **DIFF** |
   | mu | 1.84874e-05 | 1.84337e-05 | 2.91e-03 | **DIFF** |
   | nu | 1.56181e-05 | 1.55738e-05 | 2.84e-03 | **DIFF** |
   | rho, Re, x, T_air, eta, start, stop, step, w_0, u\u_infinity | – | – | 0 (7.02e-05 on rho) | ok |

   `16 common variables, 4 differ (rtol=0.001); only in EES: 0; only in
   CoolSolve: 5` — the five variables that only the variant has
   (`w_1`, `w_1_0`, `w_2`, `w_2_0`, `w_3`, the renamed derivatives; the
   extractor did not decode the EES names that carry the prime notation).
   The four deviations come from the **dynamic viscosity of air**
   (EES 1.84874e-5 Pa·s against CoolProp 1.84337e-5 Pa·s, 0.29 %): `nu`,
   `u` and `u_infinity` follow from it. No variable was excluded.

2. **Against the parametric table stored in the EES file** (501 rows, the
   table-based integration of the original file, Δη = 0.01): at η = 5 the EES
   table holds w = 3.283289405 and w' = 0.991547628, against 3.283295772 and
   0.991547343 in CoolSolve — relative differences 1.94e-06 and 2.87e-07. The
   extracted CSV has two columns named `w` (the extractor could not decode the
   name with the prime), so this comparison was done on the values, not with
   `compare_solution.py --row`.

   The EES `$IntegralTable` (7 rows, the fixed-step integration of the
   original file) holds w = 3.282666194 and w' = 0.9915686753 at η = 5
   (relative differences 1.92e-04 and 2.15e-05): the stored EES solution is
   the one of the fixed-step integration of EES, which is less accurate than
   the Runge-Kutta integration of CoolSolve (the difference is the truncation
   error of the two methods, not a model difference).

3. **Shooting on f''(0).** The shooting parameter of the model (0.33206) was
   checked with a Newton iteration on the residual `f'(η) − 1` at the end of
   the integration (with `Stop` changed from 5 to 30, where `f'` has
   converged): the model gives **f''(0) = 0.332057344620** (RK4, step 0.1) and
   0.332057336215 with an accurate adaptive integration (DOP853,
   rtol = 1e-13) — the classical value **0.3320573362** (Blasius 1908; White,
   *Viscous Fluid Flow*). The value of the original file (0.33206) is its rounded form; with
   it, f'(5) = 0.991547, i.e. the free-stream value is approached from below,
   as the shooting condition requires.

## Source and attribution

Example of the EES example library of **F-Chart Software** (© F-Chart
Software), author **S. A. Klein** (the EES licence stamp of the file names
him: `{$ID$ #0001: For use only by Professor S.A. Klein University of
Wisconsin - Madison klein}`; the stamp identifies the licence holder, the
examples are published by F-Chart Software).

Source file: `~/Nextcloud/thermo_models/EES_library/Blasius.EES` (EES
X8.805, inventory row `EEL-025` of `sources/ees_library/inventory.csv`).
The same example is published as plain text under the MIT licence by the
EES-Community mirror: <https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/blasius.ees>
(commit 5c703d0, 2026-03-01) — © F-Chart Software / S. A. Klein, MIT via
EES-Community/ees-examples. Published under the MIT licence of the library.

## Conversion log

- **2026-11-12 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES X8.805, plain-text equations window, 51 lines, 16 stored variables, no
  lookup table, three parametric tables (501×2, 501×3 and 7×3). The `$ID$`
  licence tag was removed, the standard header added, the comments kept (they
  are already in English) and the unit system converted by hand
  (`SI MASS DEG KPA C KJ` → SI-°C-Pa-J: the pressure of the air
  `P = 101.3` kPa became `P = 101300` Pa; every other number of the file is
  already SI — the `step = 0.1` is dimensionless in the model). The
  `$UnitSystem` directive was deleted.
- **2026-11-12 — GUI directives removed**: `$TabStops 0.2 3.5 in` and
  `$HideWindow Parametric` are display settings of the EES editor (the second
  one gives a "Unknown directive" warning in CoolSolve); they carry no model
  meaning and were dropped. The `$if ParametricTable` / `$elseIf` / `$endif`
  structure is kept: CoolSolve resolves the directive and takes the
  `$elseIf` branch (the fixed-step integration), as EES does for a normal
  run (`PARAMETRICTABLE` is false in a CoolSolve solve). The third method of
  the original file (the EES automatic step size) is kept commented out, as in
  the original.
- **2026-11-12 — native file blocked** (`CS-GAP-NAME-PRIME`): CoolSolve
  refuses the character `'` (and `` ` ``) in a variable name, while EES takes
  any keyboard character except `( ) * / + - ^ { } ;`. The names `w'`, `w''`,
  `w'''`, `w'_0` and `w''_0` of the original are therefore kept in the native
  file `blasius_flat_plate.eescode` (valid EES, blocked in CoolSolve) and
  renamed in the runnable variant `blasius_flat_plate_coolsolve.eescode`:
  `w' → w_1`, `w'' → w_2`, `w''' → w_3`, `w'_0 → w_1_0`, `w''_0 → w_2_0`
  (the same renaming in the `$if ParametricTable` branch and in the
  `$IntegralTable` directive). No equation, no value and no comment of the
  original is changed otherwise; the variant is valid EES as well.
- **Level**: 1 (equations 20 → 0, largest block ≤ 5 → 0, no function and no
  array → 0, not multi-zone → 0, dynamics → 1, no curated guess needed → 0)
  → level 1; moved to **level 2** with the pedagogical intent of the triage
  (a nonlinear boundary-layer ODE solved by shooting, an advanced
  fluid-mechanics topic).

## Limitations and CoolSolve gaps

- `CS-GAP-NAME-PRIME` (new): CoolSolve refuses the character `'` in a
  variable name (the EES prime notation of the derivatives), while EES
  accepts it. The native file is blocked by this gap; the runnable variant
  renames the five variables (see *Conversion log*). Reproducer:
  `w' = 1` ⏎ `x = w'` → *"Invalid variable name 'w'': the character ''' is
  not allowed in a name"*.
- The shooting parameter `f''(0)` is **not solved by the model**: it is an
  input (0.33206), as in the original file, and the boundary condition
  `f'(η) → 1` is a condition at infinity that a one-sided integrator cannot
  impose. The shooting has to be done by the user (or by an external
  Newton iteration, see *Verification*).
- The profile is that of an isothermal, incompressible, laminar boundary
  layer with a constant free-stream velocity (the Blasius assumptions); no
  pressure gradient, no thermal boundary layer.
- The free-stream velocity is not an input: it follows from the Reynolds
  number (`Re = 1e5`), the station (`x = 0.5` m) and the properties of the
  air.
- The `u\u_infinity` variable of the original file (a cubic in η) is not used
  by any equation of the file; it is kept as it is.

## Related models

- `CSL-0101` *external_forced_conv_plates*: the flat-plate Nusselt-number
  correlations (average heat-transfer coefficient from Re and Pr) — the
  empirical closure of the boundary layer that this model solves explicitly.
- `CSL-0338` *von_karman_viscous_pump*: the companion model solved with the
  same `INTEGRAL` technique — the von Kármán viscous pump, where two slopes at
  the origin are found simultaneously by a shooting method (the far-field
  condition is what they are matched to).
