# Turbocompressor optimal-regime similarity laws

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0177`

Teaching exercise on the similarity laws of the optimal regime of a
turbocompressor. At the design point (2000 m³/h of air, 1 bar and 20 °C to
3 bar, 10 000 rpm) the model evaluates the reduced mass flow, the reduced
rotation speed and the two constants of those laws.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 13 equations (largest block: 1) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 4 (2004-10-12), exercise 5 (EES file `MSTH_041012_exercice_7.EES`; the filename says exercice_7) |
| **Authors** | TBD (ULiège MSTh). The file names no person. The inventory attributes the course to J. Lebrun, V. Lemort and S. Bertagnolio. |
| **License** | MIT |
| **CoolSolve** | v0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The optimal operating regime of a turbocompressor is described by laws of the
type: ...

The turbocompressor is designed to compress 2000 m³/h of air from 1 bar and
20 °C to 3 bar. Its rotation speed is then 10 000 rpm.

What could the optimal rotation speed and flow rate of this compressor be if
it were supplied with air at 0.9 bar and 50 °C, with the discharge pressure
fixed this time at 2.5 bar?

The equations of this file are the design point: they compute the reduced
variables and the two constants. The new inlet state is the continuation file
`MSTH_041012_exercice_7_suite.EES` (inventory `TM-0060`).

## Model

The original defines the reduced variables with the temperature in kelvin,
written `t_su+273`, and the pressure in bar, written `p_su/1E5`. The two
constants of the optimal-regime laws are then

\[
M_r = \dot M \frac{\sqrt{t_{su}+273}}{p_{su}/10^{5}}, \quad
N_r = \frac{N}{\sqrt{t_{su}+273}}, \quad
cste_1 = \frac{r_p}{M_r^2}, \quad
cste_2 = \frac{N_r}{M_r}
\]

with \(\dot M = \dot V_{su}/v_{su}\), \(v_{su} = v(\mathrm{Air},T_{su},P_{su})\),
\(N = \mathrm{rpm}/60\) and \(r_p = p_{ex}/p_{su}\).

Every equation is explicit, so CoolSolve splits the 13 equations into 13
blocks of one equation.

| Inputs | Value | Outputs (design point) | Value |
|---|---|---|---|
| `V_dot_su` | 2000 m³/h | `M_dot` | 0.6605 kg/s |
| `p_su` / `t_su` | 1 bar / 20 °C | `v_su` | 0.8412 m³/kg |
| `p_ex` | 3 bar | `M_r` | 11.305 |
| `rpm` | 10 000 rev/min | `N` / `N_r` | 166.667 rev/s / 9.7368 |
| | | `r_p` | 3 |
| | | `cste_1` / `cste_2` | 0.023473 / 0.86127 |

## How to run

Open `turbocompressor_similarity_laws.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./turbocompressor_similarity_laws.eescode
```

The system is fully explicit. CoolSolve reports 0 iterations with the
`.initials` file and 0 iterations without it. The `.initials` file stores the
EES solution (specific volume on the EES `Air` reference, 0.841425 m³/kg).

## Results

Design point (air, 1 bar / 20 °C to 3 bar, 2000 m³/h, 10 000 rpm):

| Quantity | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `cste_1` | 0.0234871 | 0.023473 | 6.02e-04 |
| `cste_2` | 0.861528 | 0.861268 | 3.01e-04 |
| `M_dot` [kg/s] | 0.660255 | 0.660454 | 3.01e-04 |
| `M_r` | 11.3017 | 11.3052 | 3.01e-04 |
| `v_su` [m³/kg] | 0.841425 | 0.841172 | 3.01e-04 |
| `N` [rev/s] | 166.667 | 166.667 | 2.00e-10 |
| `N_r` | 9.73677 | 9.73677 | 3.94e-11 |
| `r_p` [-] | 3 | 3 | 0 |
| `rpm` [rev/min] | 10 000 | 10 000 | 0 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. M_r and cste_1 against suction temperature at fixed volume flow, saved in figures/.
     Air is an ideal-gas substance here, which has no CoolSolve diagram
     (CS-FEAT-DIAGRAM-IDEAL), so the figure is a sweep plot. -->

## Verification

Compared with the solution stored by EES 7.210 in
`MSTH_041012_exercice_7.EES` (`tools/compare_solution.py`, `rtol=0.001`):
*"13 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0"*.

The largest relative difference over the 13 common variables is **6.02e-04**
(`cste_1`). It stays under the tolerance. `v_su` is 0.841172 m³/kg in CoolProp
`Air` against 0.841425 m³/kg stored by EES (relative difference 3.01e-04).
`M_dot` and `M_r` follow that specific volume, and `cste_2 = N_r/M_r` follows
`M_r`, all at 3.01e-04. `cste_1 = r_p/M_r^2` scales with the square of the
specific volume, so its relative difference is twice as large (6.02e-04).
`N`, `N_r`, `r_p` and the five inputs agree. No variable exceeds `rtol=0.001`.

## Source and attribution

Exercise of the ULiège course *Machines et systèmes thermiques* (repetition 4
of 2004-10-12, exercise 5). The file names no person. The EES licence tag
names the ULiège Thermodynamics Laboratory, which identifies the laboratory.
The inventory attributes the course to J. Lebrun, V. Lemort and S. Bertagnolio.

Source file (EES 7.210, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/MSTH_041012_exercice_7.EES`
(inventory candidate `TM-0059`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): the extract report gives
  the unit system `$UnitSystem SI MASS DEG PA C J`, so no value was rescaled.
  Pressures in the file are already in pascal (`1E5`, `3E5`). The factor
  `p_su/1E5` is the original definition of the reduced mass flow (pressure in
  bar, temperature via `t_su+273`), and it is kept. Decimal commas were
  already replaced by the extractor. `$UnitSystem` and the embedded EES
  solution printout were removed. The licence tag was removed. Comments were
  translated to English. The system is square (13 equations, 13 variables);
  no Diagram-window input was restored and no computed unknown was replaced
  by a stored value. **No equation was changed.**
- **2026-10-15 — `.initials`**: the 13 values stored by EES, including
  `v_su` on the EES `Air` value. Convergence does not need them (0 iterations
  with and without the file).
- **Level 1** (taxonomy.md §3): 13 equations (0) + largest block 1 (0) + no
  function, procedure or array (0) + single component (0) + the constants are
  evaluated at one given design point, with no calibration, off-design or
  dynamics (0) + explicit equations, no curated guesses (0) = 0 → Introductory.

## Limitations and CoolSolve gaps

- The two constants describe the optimal regime at the design point only. The
  new speed and flow at 0.9 bar, 50 °C and 2.5 bar are the continuation file
  (`TM-0060`), which is a separate candidate.
- The original writes `t_su+273` (not 273.15) inside the reduced variables.
  That offset is kept.
- The `VOLUME(): fluid 'Air'` hint (suggesting `AirH2O` for moist air) is
  spurious here: dry-air ideal-gas properties are intended.
- No registered CoolSolve gap blocks this model (`missing_features` is empty).

## Related models

- `CSL-0069` *centrifugal compressor design and similarity*: same course and
  repetition (exercise 4), a compressor sized from given flow and enthalpy
  factors. Different equations (φ and ψ, 6000 m³/h, 1 to 2.5 bar).
- `CSL-0023` *centrifugal turbocompressor performance*: same course and
  repetition (exercise 2), off-design performance at constant isentropic
  efficiencies.
- `thermo_models` `TM-0060` (`MSTH_041012_exercice_7_suite.EES`): continuation
  of this exercise, with `cste_1` and `cste_2` imposed and the optimal speed
  and flow solved at 0.9 bar, 50 °C and 2.5 bar.
