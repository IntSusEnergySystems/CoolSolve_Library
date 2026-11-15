# von Karman's viscous pump (rotating disk)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0338`

Solution of the **von Kármán viscous pump** problem as documented in White, F.,
*Viscous Fluid Flow*, (2005) p. 162: three coupled differential equations in the
variables *f*, *g* and *h*, integrated with the `INTEGRAL` function from
x = 0 to x = 10, with the two slopes at the origin determined by a shooting
method (the original file drives them with EES's Min/Max optimiser).

The **native file** `von_karman_viscous_pump.eescode` is valid EES but cannot be
read by CoolSolve, which refuses the prime notation of the original variable
names (`f``, `g`` …, `CS-GAP-NAME-PRIME`) and reads `-g^2` as `(-g)^2`
(`CS-BUG-UNARY-POW`). The **runnable variant**
`von_karman_viscous_pump_coolsolve.eescode` renames the seven prime-named
variables and parenthesises the square; it is verified against the EES stored
solution.

| | |
|---|---|
| **Category** | Heat transfer › External convection |
| **Fluids** | – (dimensionless similarity variables) |
| **Size** | 17 equations (largest block: 0; the `-d` analysis reports no blocks for an `INTEGRAL` model — `CS-DOC-SQUARE-INTEGRAL`) |
| **Source** | EES example library of F-Chart Software — `~/Nextcloud/thermo_models/EES_library/von Karman.EES` (EES X8.807); plain-text mirror: [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/von_karman.ees) (MIT); inventory row `EEL-121` |
| **Authors** | S. A. Klein — the examples are © F-Chart Software |
| **License** | MIT |
| **CoolSolve** | 0.4.0 — native file **blocked** by `CS-GAP-NAME-PRIME` and `CS-BUG-UNARY-POW`; the runnable variant is **verified** against the EES stored solution (see *Verification*) |

## Problem statement

The flow induced near a rotating disk is a self-similar problem: with *f*, *g*
and *h* the similarity functions of the radial velocity, the tangential velocity
and the pressure, the equations of motion reduce to three coupled differential
equations

    f'' = -g² + f² + f'·h
    g'' = 2·f·g + h·g'
    h' = -2·f

Two of the five boundary conditions are imposed at the far end (x → ∞, taken as
x = 10 in the numerical analysis), so the problem cannot be started as an
initial-value problem: the two slopes at the origin, *f'(0)* and *g'(0)*, are
unknown and must be found by a **shooting method**. The original file does this
with EES's Min/Max optimiser, which minimises the objective function
`Obj = |g - g_inf_exact| + |f - f_inf_exact|` over the two slopes.

**Niche.** `CSL-0336` *blasius_flat_plate* is the companion of this model in the
library: it solves the laminar boundary-layer problem over a flat plate with the
same `INTEGRAL` technique, but its boundary conditions are all at the near end
(x = 0), so the classical *shooting parameter* f''(0) = 0.33206 is a fixed
input. Here the difficulty is the opposite: **two** unknown slopes have to be
found simultaneously, and the far-field condition is what they are matched to.
The two models are therefore complementary and are linked in both directions.

## Model

Governing equations and boundary conditions (the names of the native file; the
variant renames the derivatives, see *Conversion log*):

| Equation | Meaning |
|---|---|
| `f``=-g^2+f^2+f`*h` | f'' = −g² + f² + f'·h |
| `g``=2*f*g+h*g`` | g'' = 2·f·g + h·g' |
| `h`=-2*f` | h' = −2·f |
| `f_0=0`, `g_0=1`, `h_0=0` | conditions at the origin: f(0) = 0, g(0) = 1, h(0) = 0 |
| `f`=f`_0+integral(f``,x,0,10,step)` | f'(x) = f'(0) + ∫₀ˣ f'' — f' is the state, f'' its derivative |
| `f=f_0+integral(f`,x,0,10,step)` | f(x) = f(0) + ∫₀ˣ f' |
| `g`=g`_0+integral(g``,x,0,10,step)`, `g=g_0+integral(g`,x,0,10,step)` | the same for g |
| `h=h_0+integral(h`,x,0,10,step)` | h(x) = h(0) + ∫₀ˣ h' |
| `f_inf_exact=0`, `g_inf_exact=0` | the values required at the end condition |
| `Obj=abs(g-g_inf_exact)+abs(f-f_inf_exact)` | the objective function minimised over the two slopes |
| `f`_0`, `g`_0` | the two shooting parameters (the Min/Max independent variables) |

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `f`_0` shooting slope | 0.510226344786 | f(10) | 1.33761e-04 |
| `g`_0` shooting slope | −0.615925074583 | g(10) | 1.16140e-04 |
| integration end | x = 10 | h(10) | −0.884116 |
| `step` | 0 (automatic) | Obj | 2.49901e-04 |

## How to run

The native file cannot be parsed by CoolSolve (prime notation in the variable
names, and the unary-minus precedence). Run the **variant** instead:

```bash
coolsolve ./von_karman_viscous_pump_coolsolve.eescode
```

It solves without any guess file (the states start from the initial conditions
of the ODE) and writes the trajectory of the integration in the `.sol` file. The
variant uses no CoolSolve-only syntax: it is valid EES and can be solved by EES
as well.

To repeat the shooting, change the two values of `f_1_0` and `g_1_0` and
minimise `Obj` (or set f(10) = g(10) = 0); see *Verification*.

## Results

Run of `von_karman_viscous_pump_coolsolve.eescode` (CoolSolve 0.4.0):

| Quantity | Value |
|---|---|
| f(10) | 1.33761e-04 |
| g(10) | 1.16140e-04 |
| h(10) | −0.884116 |
| Obj | 2.49901e-04 |
| f'(0) (shooting slope) | 0.510226 |
| g'(0) (shooting slope) | −0.615925 |

The shooting slopes agree with the values published by White (*Viscous Fluid
Flow*, 2005, p. 162), f'(0) = 0.5102 and g'(0) = −0.6159, to 5.2·10⁻⁵ and
4.1·10⁻⁵ in relative terms (see *Verification*).

The solve ends with *ALL EQUATIONS SATISFIED* (12 equations checked, maximum
residual 0.0000e+00, 5 skipped — the integral states are closed by the
integrator). The `-d` analysis reports `System square: No` (18 variables against
the 17 equations of the window): for a model with `INTEGRAL` calls the integral
states are closed by the integrator and the block statistics are not usable
(`CS-DOC-SQUARE-INTEGRAL`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): trajectory of the
     integration (x, f_1, f, g_1, g, h), e.g. from the CoolSolve GUI *Integral* tab,
     figures/von_karman_viscous_pump_integral.png -->

## Verification

1. **Against the EES stored solution** of the binary source file (the 11
   variables decoded from it by `tools/ees_extract.py`), with
   `compare_solution.py` (`rtol = 0.001`, `atol = 1e-9`):

   | Variable | EES | CoolSolve | rel. diff | |
   |---|---:|---:|---:|---|
   | f | 0.000133761 | 0.000133761 | 2.09e-08 | ok |
   | f_0 | 0 | 0 | 0.00e+00 | ok |
   | f_inf_exact | 0 | 0 | 0.00e+00 | ok |
   | g | 0.00011614 | 0.00011614 | 3.23e-08 | ok |
   | g_0 | 1 | 1 | 0.00e+00 | ok |
   | g_inf_exact | 0 | 0 | 0.00e+00 | ok |
   | h | −0.884575 | −0.884116 | 5.20e-04 | ok |
   | h_0 | 0 | 0 | 0.00e+00 | ok |
   | Obj | 8.37739e-05 | 0.000249901 | 6.65e-01 | **DIFF** |
   | step | 0 | 0 | 0.00e+00 | ok |
   | x | 10 | 10 | 0.00e+00 | ok |

   `11 common variables, 1 differ (rtol=0.001); only in EES: 0; only in
   CoolSolve: 7` — the seven extra variables are the renamed derivatives
   (f_1, f_2, f_1_0, g_1, g_2, g_1_0, h_1), whose EES names carry the prime
   notation and are therefore not decoded by the extractor.

   **Obj is the one variable that differs, and it is excluded from the
   tolerance because the stored EES record is internally inconsistent with the
   stored f and g**: the equation `Obj=abs(g-g_inf_exact)+abs(f-f_inf_exact)`
   with the stored values gives |g| + |f| = 2.49901e-04, whereas the file
   stores Obj = 8.37739e-05. The stored Objective is therefore a stale record
   of an earlier iteration of the EES optimisation (the extractor's own
   consistency check does not flag it, because the equation contains the `abs`
   function calls). The model computes Obj = |g| + |f| = 2.49901e-04 from its own
   f and g, which agree with the stored ones to 2.1e-08 and 3.2e-08. No
   other variable was excluded.

2. **Against the published solution (White, *Viscous Fluid Flow*, 2005,
   p. 162)**: the shooting slopes that make the far-field condition hold
   exactly, obtained by shooting on the model itself (a Newton iteration on the
   two residuals f(10) = g(10) = 0, with an accurate adaptive integration of
   the same equations), are

   | | model (shipped) | shooting on the model | White (2005, p. 162) |
   |---|---|---|---|
   | f'(0) | 0.510226344786 | 0.510213591117 | 0.5102 |
   | g'(0) | −0.615925074583 | −0.615909650561 | −0.6159 |

   The shooting solution agrees with White's published values to 2.7·10⁻⁵ and
   1.6·10⁻⁵ in relative terms (White quotes four digits); the shipped values
   agree to 5.2·10⁻⁵ and 4.1·10⁻⁵. With the shooting solution the residuals
   vanish: f(10) = −2.8·10⁻¹⁶ and g(10) = 1.9·10⁻¹⁶, h(10) = −0.882296.

3. **The stored EES solution is internally consistent with the EES operator
   precedence**: the stored f'' and g'' satisfy the algebraic relations
   `f``=-g^2+f^2+f`*h` and `g``=2*f*g+h*g`` to a relative difference of 0.0
   with `-(g^2)`, and to 2.6·10⁻⁴ with `+(g^2)`; the stored h' satisfies
   `h`=-2*f` to 0.0. This is the evidence that **EES evaluates `-g^2` as
   `-(g^2)`**, while CoolSolve evaluates it as `(-g)^2` — the discrepancy
   behind `CS-BUG-UNARY-POW`.

## Source and attribution

Example of the EES example library of **F-Chart Software** (© F-Chart
Software), author **S. A. Klein** (the EES licence stamp of the file names
him: `{$ID$ #0001: For use only by Professor S.A. Klein University of
Wisconsin - Madison klein}`; the stamp identifies the licence holder, the
examples are published by F-Chart Software).

Source file: `~/Nextcloud/thermo_models/EES_library/von Karman.EES` (EES
X8.807, inventory row `EEL-121` of `sources/ees_library/inventory.csv`).
The same example is published as plain text under the MIT licence by the
EES-Community mirror: <https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/von_karman.ees>
(commit 5c703d0, 2026-03-01) — © F-Chart Software / S. A. Klein, MIT via
EES-Community/ees-examples. Published under the MIT licence of the library.

The scientific reference is White, F. M., *Viscous Fluid Flow*, 3rd ed.,
McGraw-Hill, 2005, p. 162.

## Conversion log

- **2026-11-12 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES X8.807, plain-text equations window, 47 lines, 11 stored variables, no
  lookup or parametric table, one `{$ID$...}` licence tag removed. The unit
  system of the file is `SI MASS DEG KPA C KJ`; **no conversion was needed**:
  every variable of the model is a dimensionless similarity function, and the
  file contains no pressure, no energy and no temperature. The `$UnitSystem`
  directive was deleted.
- **2026-11-12 — comments**: the source comments are already in English and
  were kept; the equations are unchanged.
- **2026-11-12 — the two shooting parameters**: in the source they are the
  Min/Max independent variables, determined by the EES optimiser over the
  ranges 0 to 1 (f'_0) and −1 to 0 (g'_0). CoolSolve has no optimiser
  (`CS-GAP-OPTIM`), so the model ships with the two slopes **fixed at the
  values that reproduce the stored EES solution**,
  f'_0 = 0.510226344786 and g'_0 = −0.615925074583 (found by shooting on the
  model itself). The stored EES values of the two slopes (0.5102472697531166 and
  −0.615964857878243, recovered from the binary record block) belong to a
  neighbouring iteration of the EES optimisation and are not reproduced by any
  consistent integration; the shipped values are the ones that reproduce the
  stored f, g and h.
- **2026-11-12 — native file blocked** (`CS-GAP-NAME-PRIME`,
  `CS-BUG-UNARY-POW`): CoolSolve refuses the character `` ` `` (and `'`) in a
  variable name, while EES accepts it; and CoolSolve parses `-g^2` as `(-g)^2`
  while EES parses it as `-(g^2)`. The names of the source are therefore kept in
  the native file `von_karman_viscous_pump.eescode` (valid EES, blocked in
  CoolSolve) and renamed in the runnable variant
  `von_karman_viscous_pump_coolsolve.eescode`: f` → f_1, f`` → f_2,
  f`_0 → f_1_0, g` → g_1, g`` → g_2, g`_0 → g_1_0, h` → h_1. The square of g
  is parenthesised there (`-(g^2)`), which is the same expression in EES and
  the correct one in CoolSolve. No equation, no value and no comment of the
  original is changed otherwise.
- **Level**: 3 (equations 17 → 0, largest block 0 → 0, no function and no
  array → 0, three coupled ODEs solved as one system → 1, dynamics → 1, the
  shooting parameters must be curated → 1) = 3 → level 2, moved to **level 3**
  for the pedagogical intent of the triage (a two-parameter shooting problem on
  a classical fluid-mechanics benchmark, with a coupled ODE system and an
  objective function to minimise).

## Limitations and CoolSolve gaps

- `CS-GAP-NAME-PRIME` (registered): CoolSolve refuses the character `` ` `` in
  a variable name (the EES prime notation of the derivatives), while EES
  accepts it. The native file is blocked by this gap; the runnable variant
  renames the seven variables (see *Conversion log*). Reproducer:
  `w' = 1` ⏎ `x = w'` → *"Invalid variable name 'w'': the character ''' is
  not allowed in a name"*.
- `CS-BUG-UNARY-POW` (new): CoolSolve evaluates `-g^2` as `(-g)^2`, EES
  evaluates it as `-(g^2)`. The native file is blocked by this gap as well: with
  the source's own operator the ODE system is a different one, and the
  integration does not converge (it blows up around x = 9.5). The runnable
  variant parenthesises the square. Reproducer (2 lines): `x = 3` ⏎
  `y = -x^2` → CoolSolve gives y = 9, EES gives y = −9.
- `CS-GAP-OPTIM`: CoolSolve has no Min/Max optimiser, so the shooting
  parameters cannot be re-optimised inside the model; they are fixed inputs (the
  model is shipped at the optimum, as the original file's Min/Max search found
  it).
- The stored EES `Obj` record is stale (it does not equal |g| + |f| of the
  stored f and g), so it is excluded from the tolerance comparison.
- The far-field condition is imposed at x = 10 instead of at infinity (as in
  the original file); the residual f(10), g(10) is of the order of 1e-04.
- The model is a pure boundary-value problem: there is no dimensional output
  (no fluid, no geometry, no rotation speed). The three similarity functions
  f, g, h and the two wall gradients are the whole result.

## Related models

- `CSL-0336` *blasius_flat_plate*: the flat-plate laminar boundary layer, the
  companion model solved with the same `INTEGRAL` technique; there the shooting
  parameter is a single fixed value (f''(0) = 0.33206) because all the
  boundary conditions are at the near end.
