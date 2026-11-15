# Spherical fuel element with exponential heat generation

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0348`

A 50-node finite-volume model of a spherical nuclear-fuel element: the
volumetric heat generation decays exponentially from the centre of the fuel
sphere, the fuel is covered by a highly conductive cladding shell, and the
outer surface rejects heat by convection to a gas at 500 °C. The nodal
energy balances are solved simultaneously with the analytical solution for
a uniform generation rate (b = 0), so the effect of the exponential decay
on the centre temperature can be read directly.

| | |
|---|---|
| **Category** | Heat transfer › Conduction, fins and radiation |
| **Fluids** | none (solid conduction and a convection boundary) |
| **Size** | 263 equations (largest block: 50) |
| **Source** | Nellis & Klein, *Heat Transfer*, Cambridge University Press, 2009, example 1.4-1 ([EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/example_1.4-1_fuel_element.ees)) |
| **Authors** | G. F. Nellis and S. A. Klein (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0 — native file blocked by `CS-GAP-NAME-PRIME`, `CS-GAP-LINE-CONTINUATION`, `CS-GAP-INDEX-VAR`; the runnable variant is verified (see *Verification*) |

## Problem statement

A fuel sphere of radius r_fuel = 5 cm (k_fuel = 1 W/m-K) generates heat at
g```(r) = g```_dot_0·exp(−b·r/r_fuel) with g```_dot_0 = 5·10⁵ W/m³ at the
centre and b = 1. It is covered by a cladding shell up to r_clad = 7 cm
(k_clad = 300 W/m-K) and convects to a gas at T_infinity = 500 °C with
h_bar = 100 W/m²-K. Discretise the fuel into N = 50 radial nodes and find
the temperature profile and its maximum; compare with the analytical
solution for a uniform generation rate (b = 0).

## Model

- FUNCTION `gen(r, r_fuel)`: the exponential generation rate at radius r
  [W/m³], with the centre rate g```_dot_0 and the decay constant b as
  body constants.
- Node layout: r[i] = r_fuel·(i−1)/(N−1), spacing DELTAr = r_fuel/(N−1).
- Interior nodes i = 3…N−1 (`DUPLICATE`): energy balance of the spherical
  shell between r[i] ∓ DELTAr/2 — conduction from both neighbours through
  the (1/r)-form spherical resistances plus the generation in the shell.
- Node 1 (centre) and node 2: balances on the half-innermost and second
  shells; node N (fuel surface): conduction out of the outer shell plus
  generation, rejected through the cladding conduction resistance
  R_cond_clad = (1/r_fuel − 1/r_clad)/(4π·k_clad) in series with the
  convection resistance R_conv = 1/(4π·r_clad²·h_bar).
- Outputs: T[i] in K and T_C[i] in °C (`ConvertTemp`), T_max_C; the
  analytical parabolic profile T_an[i] for b = 0 with its integration
  constant C_2 from the surface boundary condition.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| r_fuel / r_clad | 0.05 / 0.07 m | T[1] centre | 923.56 K (650.41 °C) |
| k_fuel / k_clad | 1 / 300 W/m-K | T[50] fuel surface | 793.83 K (520.68 °C) |
| h_bar | 100 W/m²-K | T_max_C | 650.41 °C |
| T_infinity | 500 °C | R_cond_clad / R_conv | 1.516e-3 / 0.16240 K/W |
| g```_dot_0 / b | 5e5 W/m³ / 1 | T_an[1] centre (b = 0) | 1024.40 K (751.25 °C) |
| N | 50 | T_an[50] surface (b = 0) | 816.06 K (542.91 °C) |

The exponential decay spreads the generation towards the centre: the total
generated power is 126.1 W instead of 261.8 W for a uniform 5·10⁵ W/m³, so
the uniform-generation analytical solution is 100 K hotter at the centre.
The maximum temperature is at the centre node (generation decays outward).

## How to run

The native file `fuel_element_sphere.eescode` keeps the original EES text
(backtick names, `&` line continuations, variable array indices); CoolSolve
cannot parse it (three gaps, see *Limitations and CoolSolve gaps*). Run the
runnable variant instead:

```bash
coolsolve ./fuel_element_sphere_coolsolve.eescode
```

No `.initials` needed: the system is linear in the temperatures and
converges from the default guesses (7 iterations). The variant is
regression-tested as `CSL-0348:coolsolve` against its `.sol` baseline.

## Results

| Quantity | Exponential (b = 1) | Analytical (b = 0) |
|---|---:|---:|
| Centre temperature [°C] | 650.41 | 751.25 |
| Fuel-surface temperature [°C] | 520.68 | 542.91 |
| Generated / rejected power [W] | 126.1 | 261.8 |

Nodal profile: 923.6 K at the centre, 884.0 K at mid-radius (node 25),
793.8 K at the fuel surface, monotonically decreasing — as in the original.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of T_C[i] and T_an_C[i] vs r[i],
     figures/fuel_element_sphere_profile.png + one-line caption -->

## Verification

The verification concerns the **runnable variant** (the native file does not
parse in CoolSolve). Reference: the solution stored in the binary example
`ees-examples-raw/uncategorized/example_1.4-1_fuel_element.eez`, extracted
with `tools/ees_extract.py` (EES X11.908, 3114 decoded records, warnings
"stored solution may be STALE" and one `inf` value on the loop index `i`).

1. **Full stored CSV** (`compare_solution.py fuel_element_sphere_coolsolve.sol
   reference/ees_variables.csv`): *"262 common variables, 202 differ
   (rtol=0.001); only in EES: 2852; only in CoolSolve: 2"*. All 202
   differences are stale stored records: EES stored value = guess default = 1
   for the whole temperature family (T, T_C, T_an, T_an_C, T_max_C, C_2),
   provably inconsistent with the model's own equations (T_C[i] =
   T[i] − 273.15 while both store 1; C_2 = 1024.4 by the boundary condition).
   The same file holds leftover records r/T/T_C[51…1000] of an older N = 1000
   run whose values are physical: T[1000] = 793.826 K, i.e. the CoolSolve
   surface temperature to 5.8e-7. The only-in-CoolSolve variables are the
   renamed `g_dot` (its EES name `g```_dot` has no stored record) and `pi`.
2. **Trusted subset** (inputs, grid r[1…50], DELTAr, R_cond_clad, R_conv, N —
   every record consistent with the model's explicit equations):
   *"60 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
   CoolSolve: 204"*, maximum relative difference 3.6e-10 (on r[12], last
   digits of the stored values).
3. **Analytical**: C_2 = 1024.397166 K computed by hand from the boundary
   condition against 1024.397165533 in CoolSolve (1.2e-13); the whole
   CoolSolve profile agrees with the exact continuous solution of the
   exponential-generation sphere (quadrature of the exact radial balance) to
   2.0e-4 relative (centre node, the 50-node discretisation error).
4. **Stored N = 1000 records**: CoolSolve T interpolated against the leftover
   fine-grid records at the 47 comparable node radii: max relative difference
   1.4e-4.
5. **Energy balance**: total generation ∫gen dV = 126.137 W against the heat
   rejected at node 50 (T[50] − T_infinity)/(R_cond_clad + R_conv) =
   126.134 W — 2.2e-5.

## Source and attribution

Example 1.4-1 of **G. F. Nellis and S. A. Klein**, *Heat Transfer*,
Cambridge University Press, 2009, distributed as an EES example by
F-Chart Software. The plain-text mirror of the file is published under MIT
by [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/example_1.4-1_fuel_element.ees)
(commit 5c703d0, file `uncategorized/example_1.4-1_fuel_element.ees`, also
the inventory candidate `EEX-011`); the binary `.eez` with the stored
solution is `ees-examples-raw/uncategorized/example_1.4-1_fuel_element.eez`
of the same repository (licence tag `{$ID$ … S.A. Klein, F-Chart Software}`:
licence holder, not authorship).

## Conversion log

- **2026-11-14 — import** (`tools/ees_extract.py` on the `.eez`): EES
  X11.908, unit system `SI MASS RAD PA K J`. No unit conversion: the model
  holds its temperatures in K and converts at the outputs with
  `ConvertTemp(K,C,·)`; the `Convert`/`ConvertTemp` calls are kept as in the
  original and the numbers stay unit-agnostic in CoolSolve (the RAD setting
  is irrelevant: no trigonometric function is used). Comments kept (already
  English); the `[-]` unit annotations of the original comments dropped
  (library rule). Display-only directives `$Tabstops`, `$ShowWindow Plot1`,
  `$hideWindow Arrays` removed (CoolSolve ignores them with a warning);
  `{$ID$}`, `{$PX$}`, `{$ST$}` tags removed by the extractor. No lookup or
  parametric tables; `$ifnot ParametricTable` kept (the branch EES uses in a
  normal run, always kept by CoolSolve). No `.initials`: linear system,
  converges from the default guesses.
- **2026-11-14 — native file blocked** by three CoolSolve gaps (each with a
  minimal reproducer in the gap register): `CS-GAP-NAME-PRIME`
  (*"Invalid variable name 'g```_dot': the character '`' is not allowed in a
  name"* on `g```_dot_0` and `g```_dot`), `CS-GAP-LINE-CONTINUATION` (the
  four equations continued with `&`: *"Could not parse line"*), and
  `CS-GAP-INDEX-VAR` (with the first two worked around, the node-N balance
  still fails: `T[N]`, `T[N-1]`, `r[N-1]`, `r[N]` parse as four extra
  unknowns, *"There are 263 equations and 267 unknowns"*).
- **2026-11-14 — runnable variant** `fuel_element_sphere_coolsolve.eescode`,
  three changes forced by the gaps, physics and variable roles unchanged
  (valid EES, no CoolSolve-only syntax): the backtick names renamed
  `g```_dot_0` → `g_dot_0` and `g```_dot` → `g_dot` (`CS-GAP-NAME-PRIME`);
  the four `&`-continued equations joined into single lines
  (`CS-GAP-LINE-CONTINUATION`); in the node-N balance the variable indices
  written literally as T[50], T[49], r[49], r[50] (`CS-GAP-INDEX-VAR`;
  N = 50 in the model). Solved with CoolSolve 0.4.0: SUCCESS (7 iterations).
- **Level**: 263 equations → 1; largest algebraic block 50 → 2; FUNCTION +
  `DUPLICATE` → 1; 50-node discretisation → 1; curated guesses: no → 0;
  semi-empirical/off-design physics: no → 0. Score 5 → **level 3**.

## Limitations and CoolSolve gaps

- `CS-GAP-NAME-PRIME`: the EES derivative/backtick notation in the variable
  names `g```_dot_0` (FUNCTION body) and `g```_dot` (main program) is a
  parse error; the native file keeps the EES names, the variant renames them.
- `CS-GAP-LINE-CONTINUATION`: equations continued with `&` do not parse
  (native file has four); the variant joins them.
- `CS-GAP-INDEX-VAR`: an array element indexed by a main-program variable
  set to a constant (`T[N]`) becomes an extra unknown; the variant writes the
  literal indices.
- The stored temperatures of the source file are stale (see *Verification*);
  the `.initials`-free solve does not rely on them.
- Steady state, constant properties, one-dimensional spherical conduction —
  as in the original.

## Related models

None in the library yet: the other models of the category are a resistance
and shape-factor library (`CSL-0106` *conduction_resistances_and_shapes*), a
2-D steady plate discretised with `DUPLICATE` (`CSL-0341`
*conduction_2d_square_plate*) and a transient plane wall (`CSL-0340`
*transient_conduction_plane_wall*) — none models a sphere with heat
generation. `CSL-0341` shares the discretised steady-conduction method.
