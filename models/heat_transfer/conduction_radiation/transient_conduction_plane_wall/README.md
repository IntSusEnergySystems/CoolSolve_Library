# Transient conduction in a plane wall with a convective boundary condition

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0340`

One-dimensional **transient conduction in a plane wall** of half-thickness
`a`, initially at a uniform temperature `Tin` and suddenly submitted, at
`t = 0`, to a convective boundary condition `(h, Tinf)`. The wall temperature
is computed with the **separation-of-variables series** (an infinite series of
cosine × exponential terms, whose eigenvalues solve `tan(zeta) = Bi/zeta`) and
compared with the **semi-infinite-wall solution** (`erfc`) of the original
model. The eigenvalues are found automatically with the arrays
`lowerlimit[]`, `upperlimit[]` and `guess[]`, as in the EES example.

| | |
|---|---|
| **Category** | Heat transfer › Conduction, fins and radiation |
| **Fluids** | none (pure conduction; no property call) |
| **Size** | 76 equations after analysis (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/EES_library/Transient Conduction through a Plane Wall.EES` (EES X8.806), inventory row `EEL-117` of `sources/ees_library/inventory.csv`; plain-text mirror of the same example: [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Arrays/transient_conduction_through_a_plane_wall.ees) |
| **Authors** | S. A. Klein (University of Wisconsin–Madison); F-Chart Software (EES) |
| **License** | MIT — © F-Chart Software / S. A. Klein, MIT via EES-Community/ees-examples |
| **CoolSolve** | 0.4.0 — native file **blocked** by `CS-BUG-UNARY-POW`; the runnable variant `transient_conduction_plane_wall_coolsolve.eescode` is **verified** against the EES stored solution |

## Problem statement

A plane wall of half-thickness `a`, initially at the uniform temperature
`Tin`, is submitted at `t = 0` to a convective boundary condition
(`h`, `Tinf`) on its two faces. Compute the temperature of the wall at any
time `t`, and compare the result with the solution for a semi-infinite wall.

The original EES example states: *"The solution to the 1-d, transient
conduction problem in which a wall (with half-thickness a) is initially at a
uniform temperature (Tin) and is subjected to a convective boundary condition
(h, Tinf) at time = 0 can be solved using separation of variables. The result
is presented in several heat transfer text books including Carslaw and
Jaeger and Incropera and DeWitt. The solution to this problem involves an
infinite series composed of the product of a cosine and exponential term. The
argument of each term in the series is related to the eigenvalues of the
problem, zeta[i] - obtained from the repeated and increasing intersections of
the functions tan(zeta[i])=Bi/zeta[i] where Bi is the Biot number. The process
of finding the eigenvalues is automated in EES by using arrays to set the
ranges in which each consecutive eigenvalue is located."*

## Model

Data (as in the original): `Tinf` = 100 °C, `Tin` = 10 °C, `h` = 20 W/m²-K,
`k` = 1 W/m-K, `a` = 0.05 m, `rho` = 4000 kg/m³, `c` = 350 J/kg-K, time
`t` = 17 500 s (an input of the EES model, see *Conversion log*).

| Quantity | Relation | Unit |
|---|---|---|
| thermal diffusivity | `alpha = k/(rho·c)` | m²/s |
| Biot number | `Bi = h·a/k` | – |
| Fourier number | `Fo = alpha·t/a²` | – |
| dimensionless location | `x = xbar·a` | m |
| eigenvalues | `tan(zeta[i]) = Bi/zeta[i]`, `i` = 1…10 | – |
| series coefficients | `C[i] = 4·sin(zeta[i])/(2·zeta[i] + sin(2·zeta[i]))` | – |
| series terms | `theta[i] = C[i]·exp(-zeta[i]²·Fo)·cos(zeta[i]·xbar)` | – |
| wall temperature ratio | `theta_t = sum(theta[1..10])` | – |
| semi-infinite wall | `theta_si = 1-(erfc((a-x)/sqrt(4·alpha·t)) - exp(h·(a-x)/k + (h/k)²·alpha·t)·erfc((a-x)/sqrt(4·alpha·t) + h·sqrt(alpha·t)/k))` | – |

`theta` is the dimensionless temperature of the wall (1 at the initial
temperature, 0 at the ambient temperature); the wall temperature is
`T = Tin + theta·(Tinf - Tin)`. The default run evaluates the mid-plane
(`xbar` = 0, the symmetry plane of the wall); the surface (`xbar` = 1) is
reached by changing `xbar`.

The ten eigenvalues are searched in the intervals `((i-1)·pi, (i-1)·pi + pi/2)`,
which bracket the successive roots of `tan(zeta) = Bi/zeta`; the arrays
`lowerlimit[]`, `upperlimit[]` and `guess[]` reproduce the search of the
original (in EES they also set the bounds and the initial guess of the
variable `zeta[]`; CoolSolve has no bounds, `CS-GAP-BOUNDS`, so the
initial-guess file `.initials` is needed — see *Limitations*).

## How to run

```bash
coolsolve ./transient_conduction_plane_wall_coolsolve.eescode
```

The native file `transient_conduction_plane_wall.eescode` is the faithful
transcription of the original EES file; it is **blocked** by
`CS-BUG-UNARY-POW` (CoolSolve reads `-x^2` as `(-x)^2`, EES as `-(x^2)`) and
gives wrong results silently. The runnable variant
`transient_conduction_plane_wall_coolsolve.eescode` differs from it by
**one line only** (the parentheses of that power):

```
theta[i]=C[i]*exp(-zeta[i]^2*Fo)*cos(...)              "native file, valid EES"
theta[i]=C[i]*exp(-(zeta[i]^2*Fo))*cos(...)            "runnable variant"
```

The variant is valid EES as well (EES reads both as `-(zeta[i]^2*Fo)`), keeps
every variable name and is the regression baseline
(`transient_conduction_plane_wall_coolsolve.sol`, tested as
`CSL-0340:coolsolve`).

The `.initials` file is **required**: without it, the ten eigenvalues all
converge to the first root (0.8603) and the results are silently wrong
(`theta_t` = 10.78 instead of 0.99975 at `Fo` = 0.05). It holds the values
stored by EES.

## Results

Default run (`t` = 17 500 s, `Fo` = 5, mid-plane `xbar` = 0):

| Quantity | Value |
|---|---:|
| `Fo` (Fourier number) | 5 |
| `t` [s] | 17 500 |
| `alpha` [m²/s] | 7.14286·10⁻⁷ |
| `Bi` (Biot number) | 1 |
| `zeta[1]`, `zeta[2]` | 0.8603336, 3.4256185 |
| `C[1]` | 1.1191320 |
| `theta_t` (series) | 0.0276448 |
| `theta_si` (semi-infinite wall) | 0.4515865 |

At `Fo` = 5 the wall is not semi-infinite: the thermal penetration depth
`sqrt(alpha·t)` = 0.1118 m is larger than the half-thickness `a` = 0.05 m
and `Bi` = 1, so the mid-plane of the finite wall is colder than the
semi-infinite-wall solution (`theta_t` = 0.0276 against `theta_si` = 0.4516).

## Verification

Reference: the **solution stored in the original EES file**
(`reference/ees_variables.csv` of the extraction, i.e. the Variable
Information records of `Transient Conduction through a Plane Wall.EES`),
compared with the runnable variant with
`CoolSolve/tools/compare_solution.py`:

```
69 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8
```

The largest relative deviation over the 69 variables is **6.3·10⁻⁷**
(`theta[3]` = 4.84·10⁻⁹², the smallest value of the model); `theta_t`
agrees to 1.5·10⁻⁷ and `theta_si` to 3.9·10⁻¹¹. The eight variables "only in
CoolSolve" are the seven terms `theta[4]`…`theta[10]` (EES stores no record
for them, their value underflows to zero) and the built-in constant `pi`.

The EES file also stores three data tables (the curve data of its plot
window), extracted as `ees_parametric-table_1.csv` (1001×3: `tan(zeta)` and
`Bi/zeta` against `zeta`), `_2.csv` (101×2: `theta_t` against `xbar`) and
`_3.csv` (101×4: `theta_si`, `theta_t` and `theta[1]` against `Fo`). They were
checked against the file before being used: table 1 reproduces
`tan(zeta)` and `Bi/zeta` to the last digit of the EES values (e.g. row 1:
`zeta` = 0.0001, `y1` = 0.0001, `y2` = 10 000), and table 3 is reproduced by
the model itself:

| Run | Reference (EES table 3) | `compare_solution.py` |
|---|---|---|
| `t` = 175 s (`Fo` = 0.05) | row 2 | `4 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 73` |
| `t` = 17 500 s (`Fo` = 5) | row 101 | `4 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 73` |

(`Fo`, `theta_t`, `theta_si` and `theta[1]` are the four common variables;
the largest deviation is 2.5·10⁻⁹, on `theta[1]` of the `Fo` = 0.05 run.)

The eigenvalues were also checked by hand: the first root of
`tan(zeta) = 1/zeta` is `zeta` = 0.8603336 and
`C[1] = 4·sin(zeta)/(2·zeta + sin(2·zeta))` = 1.1191320, the values of the
EES file.

## Source and attribution

Source: `~/Nextcloud/thermo_models/EES_library/Transient Conduction through a
Plane Wall.EES` (EES X8.806), inventory row `EEL-117` of
`sources/ees_library/inventory.csv`. Author: **S. A. Klein** (University of
Wisconsin–Madison); the file is an EES example of **F-Chart Software**
(`{$ID$ #0001: For use only by Professor S.A. Klein University of Wisconsin -
Madison klein}`). The plain-text mirror of the same example is published in
the [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples)
repository (commit `5c703d0`, folder `Arrays/`), under the MIT licence.

> © F-Chart Software / S. A. Klein, MIT via EES-Community/ees-examples

The model is published under the CoolSolve Library MIT licence.

## Conversion log

- **2026-11-12 — import (T-IMPORT card C-513, candidate `EEL-117`).**
  `tools/ees_extract.py` on the binary source: 71 variables, 3 data tables
  (the curve data of the plot window), EES X8.806, unit system
  `SI MASS RAD PA C J`.
- **Radians → degrees (the only unit conversion).** The file is saved in the
  EES *RAD* setting; CoolSolve uses degrees. The three trigonometric
  arguments are therefore multiplied by `180/pi`, the values of the variables
  themselves (the eigenvalues, in radians) are unchanged:
  `tan(zeta[i]*180/pi) = Bi/zeta[i]`,
  `C[i] = 4*sin(zeta[i]*180/pi)/(2*zeta[i]+sin(2*zeta[i]*180/pi))`,
  `theta[i] = ...*cos(zeta[i]*xbar*180/pi)`. No other equation, constant or
  input needed a conversion: the file is already SI (Pa, J, kg/m³, W/m-K,
  J/kg-K, m, s, °C).
- **`t` given a value.** In the original, `t` has no equation: it is an input
  of the EES model (the last value stored by EES, 17 500 s, which gives
  `Fo` = 5). The library file writes `t = 17500 [s]`, with the same value, so
  that the system is square; `Fo` remains an output.
- **`$TabStops` directive dropped** (tab stops of the EES equations window,
  dead code for CoolSolve).
- **Comments translated** to English (the original was already in English)
  and the standard header added; the commented-out line `{Fo=0.05}` of the
  original is kept: it documents that the Fourier number can be prescribed
  instead of the time.
- **No equation was changed** in the native file; the runnable variant only
  adds the parentheses forced by `CS-BUG-UNARY-POW` (the file stays valid
  EES: EES reads `-zeta[i]^2*Fo` and `-(zeta[i]^2*Fo)` the same way).
- **Level**: equations 76 → 1 point (50–300); largest block 1 → 0 points
  (≤ 5); arrays / `DUPLICATE` → 1 point; multi-zone → 0; dynamics (transient
  problem) → 1 point; numerics → 1 point (the eigenvalues need the curated
  initial guesses of the `.initials` file). Score 4 → level 3, moved to
  **level 2** (pedagogical intent: a single textbook exercise of the
  neighbouring conduction category, one algebraic block and an explicit
  closed-form series).

## Limitations and CoolSolve gaps

- **`CS-BUG-UNARY-POW`** (already registered): the unary minus binds tighter
  than the power in CoolSolve, so `-zeta[i]^2` is read as `(-zeta[i])^2` and
  the exponent of the series becomes positive: the terms `theta[5]`…`theta[10]`
  overflow to ±infinity and the solution is silently wrong. This gap blocks
  the native file (`missing_features`); the runnable variant works around it
  with the parentheses of the power, as for `CSL-0338`.
- **`CS-BUG-ERF-WARNING`** (registered by this card): the parser does not list
  `erf`/`erfc` among the built-in functions, so every model that calls them
  gets the spurious warning *"Unknown function 'erfc'"* although the function
  is evaluated correctly (`erfc(1)` = 0.1572992). Warning only, the model is
  not blocked by it.
- **`CS-GAP-BOUNDS`**: EES bounds the eigenvalue `zeta[i]` to the interval in
  which its root lies (`lowerlimit[]`, `upperlimit[]`); CoolSolve has no
  bounds, so the `.initials` file is needed to find the ten distinct roots.
- The series is truncated at `Nterm` = 10 terms (as in the original): at
  `Fo` = 5 the truncation error is below 10⁻⁷, but it is not negligible at
  `Fo` < 0.1 (the sum at `Fo` = 0 is 0.99889 instead of 1).

## Niche

- **`CSL-0106`** *conduction_resistances_and_shapes* is the **steady**
  counterpart of this model: it gives the plane-wall resistance, the
  cylindrical-wall resistance, the shape factors and the R-value conversions
  as reusable EES functions. This model adds what a resistance cannot give:
  the **transient** behaviour of a plane wall — the separation-of-variables
  series, the eigenvalues `tan(zeta) = Bi/zeta` and their automatic search
  with arrays, and the comparison with the semi-infinite-wall (`erfc`)
  solution. The two models share the same physics (Fourier conduction in a
  plane wall, `k`, `a`, `h`) but not the same purpose: steady resistance
  versus transient temperature field.
- The library has no other transient 1-D conduction model; the two-dimensional
  steady counterpart of this example (`EEL-009`, *2-D Conduction*) is still
  `todo` in the inventory.

## Related models

- `CSL-0106` *conduction_resistances_and_shapes*: the steady conduction
  relations (plane-wall resistance, shape factors) that this transient model
  complements.
- `CSL-0341` *conduction_2d_square_plate*: the **steady, two-dimensional**
  counterpart of this transient one-dimensional model: a discretised
  temperature field of a square plate (two edges at 100 C, one at 0 C, one
  insulated).
