# Two-dimensional steady conduction in a square plate

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0341`

Finite-difference solution of the **two-dimensional steady conduction
equation in a square plate**, written in EES as a demonstration of
two-dimensional arrays: the temperature of every node of a square grid is
the average of its four neighbours, with **two edges held at 100 °C, one
edge at 0 °C and one edge insulated** (no temperature gradient). The model
gives the whole temperature field `T[i,j]` of the plate (729 node
temperatures), not a resistance or a shape factor.

| | |
|---|---|
| **Category** | Heat transfer › Conduction, fins and radiation |
| **Fluids** | none (pure conduction; no property call) |
| **Size** | 730 equations after analysis (largest block: 650) |
| **Source** | `~/Nextcloud/thermo_models/EES_library/2-D Conduction.EES` (EES X8.821), inventory row `EEL-009` of `sources/ees_library/inventory.csv`; plain-text mirror of the same example: [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/2-d_conduction.ees) |
| **Authors** | S. A. Klein (University of Wisconsin–Madison); F-Chart Software (EES) |
| **License** | MIT — © F-Chart Software / S. A. Klein, MIT via EES-Community/ees-examples |
| **CoolSolve** | 0.4.0 — native file **blocked** by `CS-GAP-INDEX-VAR`; the runnable variant `conduction_2d_square_plate_coolsolve.eescode` is **verified** against the EES stored solution |

## Problem statement

A square plate, of constant thermal conductivity and without heat
generation, has two of its four edges at 100 °C, one edge maintained at
0 °C and one edge insulated. Compute the steady temperature distribution
inside the plate.

The original EES example states: *"This program calculates the
two-dimensional steady-state temperature distribution in a square plate. Two
of the four edges are at 100°C, one is maintained at 0°C and one is
insulated. The solution illustrates the use of 2-dimensional arrays and
contour and 3-D plots."* and *"Notice that it is not necessary for the user
to program any iterative procedures to solve the equations."* (the field is
obtained by solving the whole algebraic system at once, as CoolSolve does).

## Model

The plate is divided into a square grid of `N` × `N` interior nodes
(`N` = 25 in the original), surrounded by a ring of boundary nodes
(`0` and `N+1` in both directions). The steady conduction equation
`d²T/dx² + d²T/dy² = 0` is discretised with the five-point scheme on the
uniform grid (unit spacing), which gives one equation per interior node:

| Quantity | Relation | Unit |
|---|---|---|
| interior nodes (`i` = 1…N, `j` = 1…N) | `T[i,j] = (T[i+1,j] + T[i-1,j] + T[i,j+1] + T[i,j-1])/4` | °C |
| edge `j = 0` (`i` = 0…N+1) | `T[i,0] = 100` | °C |
| edge `i = 0` (`j` = 1…N) | `T[0,j] = 100` | °C |
| edge `i = N+1` (`j` = 1…N) | `T[N+1,j] = 0` | °C |
| edge `j = N+1` (`i` = 0…N+1) | `T[i,N+1] = T[i,N]` (insulated) | °C |

The names of the sides are those of the original (which names them after
the orientation of its contour plot): the edge `j = 0` is the *"Left hand
side set to 100°C"*, the edge `i = 0` the *"Bottom surface at 100°C"*, the
edge `i = N+1` the *"Top surface at 0°C"* and the edge `j = N+1` the
*"Insulated right hand side - no temperature gradient"*. The index `i`
runs along X and `j` along Y.

The insulation condition is the first-order (zero-gradient) finite-
difference approximation of the Neumann condition: it makes the node
`N+1` an *image* of the node `N` and carries no heat. The corner nodes
that belong to two edges at once keep the value of the edge that is set
first in the original: `T[0,0] = T[N+1,0] = T[0,N+1] = 100 °C` (the edges
`j = 0` and `i = 0`) and `T[N+1,N+1] = 0 °C` (the edge `i = N+1`, reached
through the insulated edge `j = N+1`).

The model computes temperatures only: a heat rate would need the thermal
conductivity, the grid spacing and the depth of the plate.

## How to run

```bash
coolsolve ./conduction_2d_square_plate_coolsolve.eescode
```

The native file `conduction_2d_square_plate.eescode` is the faithful
transcription of the original EES file; it is **blocked** by
`CS-GAP-INDEX-VAR` (CoolSolve does not resolve an array index that is an
expression of a model variable, so `T[N+1,j]` and `T[i,N+1]` become
variables of their own and the system is not square: *"There are 730
equations and 807 unknowns"*). The runnable variant
`conduction_2d_square_plate_coolsolve.eescode` differs from it by
**two lines only** (the three array indices that the gap forces):

```
T[i,N+1]=T[i,N]        "native file, valid EES"
T[N+1,j]=0             "native file, valid EES"
```

becomes

```
T[i,26]=T[i,25]        "runnable variant"
T[26,j]=0              "runnable variant"
```

i.e. the indices that EES resolves at run time (26 = N+1 and 25 = N for
`N` = 25) are written with their value, as the gap register suggests for
`CSL-0329`. Every equation, input and variable name is unchanged and the
file is valid EES. The loop bounds (`duplicate i=0,N+1`) are left as they
are: CoolSolve accepts a bound that is a variable set to a constant.

The variant is the regression baseline
(`conduction_2d_square_plate_coolsolve.sol`, tested as
`CSL-0341:coolsolve`). It is **linear** and converges in 2 iterations
from the default guesses: the `.initials` file (the values stored by EES)
is not needed, but it is shipped with the model.

## Results

Default run (`N` = 25, edges at 100 °C / 100 °C / 0 °C, one insulated):

| Node | `T` [°C] | position |
|---|---:|---|
| `T[1,1]` | 99.771264 | near the two 100 °C edges (corner) |
| `T[1,25]` | 96.828315 | near the 100 °C edge `i = 0`, insulated side |
| `T[13,1]` | 96.186572 | middle of the 100 °C edge `j = 0` |
| `T[13,13]` | 63.669282 | centre of the plate |
| `T[13,25]` | 55.853285 | middle of the insulated edge `j = N+1` |
| `T[25,13]` | 5.940517 | near the 0 °C edge `i = N+1` |
| `T[25,25]` | 4.587095 | near the 0 °C edge and the insulated edge |

The field decreases from the two 100 °C edges towards the 0 °C edge and
stays smooth (the maximum of the solution is 100 °C and its minimum
0 °C).

## Verification

Reference: the **solution stored in the original EES file** (the Variable
Information records of `2-D Conduction.EES`, 729 node temperatures and
`N`), compared with the runnable variant with
`CoolSolve/tools/compare_solution.py`:

```
730 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0
```

The largest relative deviation over the 730 variables is **1.63·10⁻⁸**
(on `T[23,26]` and `T[23,25]`, 13.71 °C); the deviation is the same order
(1.6·10⁻⁸) on every node and comes from the display format of the EES
records, which keep six significant digits (`13.7118` against
`13.71176345`): the field is reproduced to the digits stored by EES.

**Edge temperatures.** The solution satisfies the boundary conditions
exactly: `T[i,0] = 100 °C` and `T[0,j] = 100 °C` on the two heated
edges, `T[26,j] = 0 °C` on the cold edge, and `T[i,26] = T[i,25]` on the
insulated edge for every `i` (difference below 10⁻¹²).

**Energy balance.** With a uniform grid of unit spacing, the discrete
heat flow through an edge segment is the temperature difference across
it; the sums over the 25 segments of each edge (unit depth, in K) are

| Edge | Flow |
|---|---:|
| `i = 0` (100 °C, in) | 54.238234 |
| `j = 0` (100 °C, in) | 199.222902 |
| `i = N+1` (0 °C, out) | 253.461136 |
| `j = N+1` (insulated) | 0 |

so that the heat entering through the two hot edges equals the heat
leaving through the cold edge: 54.238234 + 199.222902 − 253.461136 =
**−9.1·10⁻¹²** (relative residual below 10⁻¹³). The insulated edge carries
no heat, as it must.

**Grid convergence.** Solving the same problem on a grid twice as fine
(`N` = 51) moves the temperature of a node by at most 0.04 °C (the
centre of the plate: 63.669282 °C at `N` = 25 against 63.629490 °C at
`N` = 51), which is the expected second-order discretisation error: the
`N` = 25 field is converged to about 0.01 °C.

## Source and attribution

Source: `~/Nextcloud/thermo_models/EES_library/2-D Conduction.EES`
(EES X8.821), inventory row `EEL-009` of
`sources/ees_library/inventory.csv` (the file `2-D Conduction (1).EES` of
the same folder is a byte-identical copy, inventory row `EEL-008`).
Author: **S. A. Klein** (University of Wisconsin–Madison); the file is an
EES example of **F-Chart Software** (`{$ID$ #0001: For use only by
Professor S.A. Klein University of Wisconsin - Madison klein}`). The
plain-text mirror of the same example is published in the
[EES-Community/ees-examples](https://github.com/EES-Community/ees-examples)
repository (commit `5c703d0`, folder `Case_Study/`), under the MIT licence;
its equations were compared with the binary file and are identical.

> © F-Chart Software / S. A. Klein, MIT via EES-Community/ees-examples

The model is published under the CoolSolve Library MIT licence.

## Conversion log

- **2026-11-12 — import (T-IMPORT card C-513, candidate `EEL-009`).**
  `tools/ees_extract.py` on the binary source: 730 variables (the 729 node
  temperatures and `N`), **no** lookup table and **no** parametric table,
  EES X8.821, unit system `SI MASS DEG KPA C KJ`. The absence of tables was
  checked against the file itself: the equations contain no
  `LOOKUP`/`INTERPOLATE` call, the extraction report lists none and the
  `tables` column of the inventory row is empty (the `730/730` of the
  `stored_solution` column is the number of decoded variables and of the
  stored values).
- **Unit system: nothing to convert.** The file is saved in the EES
  `KPA`/`KJ` setting, but the model contains **no pressure and no
  energy**: its only physical quantity is the temperature, in °C (the
  plain-text mirror of the same example declares it with
  `$VarInfo T[] Units='C'`). No input, constant or equation needed a
  conversion; the `$UnitSystem` directive was removed (CoolSolve has a
  single unit system, SI-°C-Pa-J).
- **`$TabStops` directive dropped** (tab stops of the EES equations
  window, dead code for CoolSolve).
- **Comments**: the original is already in English; the trailing comments
  of the boundary conditions were kept and given their SI unit (100 °C,
  0 °C instead of "100°C", "0°C").
- **No equation was changed** in the native file; the standard header was
  added. The runnable variant writes the three array indices that the gap
  forces with their value (`N+1` → 26, `N` → 25, with `N` = 25); every
  other line, and every variable name, is unchanged and the file stays
  valid EES.
- **Level**: equations 730 → 2 points (300–1500); largest block 650 → 2
  points (> 30); arrays / `DUPLICATE` → 1 point; discretised (finite-
  difference grid) → 1 point; semi-empirical / off-design / dynamics → 0;
  numerics → 0 (the system is linear and converges in 2 iterations from
  the default guesses, no curated guess needed). Score 6 → level 3, moved
  to **level 2** (pedagogical intent: a single textbook example of the
  conduction category, one linear algebraic block, no correlation and no
  closure; the same rating as the sibling model `CSL-0340`).

## Limitations and CoolSolve gaps

- **`CS-GAP-INDEX-VAR`** (already registered): an array element indexed by
  a main-program variable that an equation sets to a constant is not
  resolved by CoolSolve: `T[N+1,j]` and `T[i,N+1]` become variables of
  their own (`T[0,expr]`, `T[0,N]`, …) and the system is not square
  (*"There are 730 equations and 807 unknowns"*). This gap blocks the
  native file (`missing_features`); the runnable variant works around it
  by writing the indices with their value, as the gap register suggests
  for `CSL-0329`. Resolving such an index like the bounds of a
  `DUPLICATE` would close the gap.
- The grid is uniform and the plate is square, with a unit grid spacing:
  the geometry does not enter the equations, so the field computed is that
  of the original square plate whatever its side length; a heat rate needs
  the conductivity, the spacing and the depth.
- The insulated edge is treated with a first-order (zero-gradient)
  approximation, as in the original.
- The corners of the plate take the value of one of their two edges
  (see *Model*); the discrete energy balance of the model closes on the
  25 interior segments of each edge, not on the corners.

## Niche

- **`CSL-0106`** *conduction_resistances_and_shapes* is the **resistance
  library** of the conduction category: it gives the plane-wall and
  cylindrical-wall resistances, the isothermal shape factors and the
  R-value conversions as reusable EES functions. It cannot give what this
  model gives: a **discretised two-dimensional temperature field**. This
  model is not a resistance model — it computes the temperature of every
  node of a square plate with mixed (Dirichlet and insulated) boundary
  conditions, and no shape factor enters it.
- **`CSL-0340`** *transient_conduction_plane_wall* is the **transient,
  one-dimensional** counterpart of the same EES example collection: the
  separation-of-variables series of a plane wall (with a convective
  boundary condition) compared with the semi-infinite-wall (`erfc`)
  solution. This model adds what a transient 1-D resistance cannot: the
  **steady two-dimensional field** of a square plate, discretised on a
  grid, with an insulated edge.
- The library has no other two-dimensional conduction model.

## Related models

- `CSL-0106` *conduction_resistances_and_shapes*: the steady conduction
  resistances and shape factors that this discretised 2-D field
  complements (a resistance cannot give a temperature field).
- `CSL-0340` *transient_conduction_plane_wall*: the transient 1-D
  counterpart of this steady 2-D conduction model.
