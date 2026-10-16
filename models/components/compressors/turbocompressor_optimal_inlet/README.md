# Teaching exercise: turbocompressor optimal speed and flow at a new inlet

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0231`

Teaching exercise on the optimal regime of a turbocompressor. The two
constants of the similarity laws are given. The model computes the optimal
rotation speed and the suction volume flow when the machine is supplied with
air at 0.9 bar and 50 °C and discharges at 2.5 bar.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 13 equations (largest block: 1) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 4 (2004-10-12), exercise 5 continued (EES file `MSTH_041012_exercice_7_suite.EES`; the equation window says exercice 5 suite) |
| **Authors** | TBD (ULiège MSTh). The equation window names no person. |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

What could the optimal rotation speed and flow rate of this compressor be if
it were supplied with air at 0.9 bar and 50 °C, with the discharge pressure
fixed this time at 2.5 bar?

The two constants of the optimal-regime laws are given:
`cste_1 = 0.02349` and `cste_2 = 0.8615`. The previous operating point,
2000 m³/h (`V_dot_su = 2000/3600`) and 10 000 rpm, is commented out in the
original. Those two lines stay comments. They are not equations of this file.

The equation window titles the run "MSTH 041012 exercice 5 suite". The
filename is `MSTH_041012_exercice_7_suite.EES`.

## Model

The original defines the reduced variables with the temperature in kelvin,
written `t_su+273`, and the pressure in bar, written `p_su/1E5`. The same
constants are also written from the reduced variables, which closes the
optimal speed and the optimal flow:

\[
cste_1 = \frac{r_p}{M_r^2}, \quad
M_r = \dot M \frac{\sqrt{t_{su}+273}}{p_{su}/10^{5}}, \quad
cste_2 = \frac{N_r}{M_r}, \quad
N_r = \frac{N}{\sqrt{t_{su}+273}}
\]

with \(r_p = p_{ex}/p_{su}\), \(\dot M = \dot V_{su}/v_{su}\),
\(v_{su} = v(\mathrm{Air},T_{su},P_{su})\) and \(N = \mathrm{rpm}/60\).
`t_su` and `T_su` are the same suction temperature, and `p_su` and `P_su`
the same suction pressure: EES is case-insensitive, and CoolSolve keeps both
spellings in one square system.

CoolSolve splits the 13 equations into 13 blocks of one equation.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `cste_1` | 0.02349 | `rpm` | 10102.2 rev/min |
| `cste_2` | 0.8615 | `V_dot_su` | 0.561195 m³/s |
| `p_su` / `t_su` | 0.9 bar / 50 °C | `M_dot` | 0.544563 kg/s |
| `p_ex` | 2.5 bar | `v_su` | 1.030541 m³/kg |
| | | `M_r` | 10.8744 |
| | | `N` / `N_r` | 168.370 rev/s / 9.36834 |
| | | `r_p` | 2.77778 |

## How to run

Open `turbocompressor_optimal_inlet.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./turbocompressor_optimal_inlet.eescode
```

The system is square (13 equations, 13 variables). CoolSolve reports 9
iterations with the `.initials` file and 28 iterations without it. The
`.initials` file stores the EES solution, including the EES specific volume
of `Air` (1.030594 m³/kg). No `coolsolve.conf` is used.

## Results

New inlet state (air, 0.9 bar / 50 °C to 2.5 bar; `cste_1` and `cste_2` given):

| Quantity | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `V_dot_su` [m³/s] | 0.5612235712 | 0.561195187 | 5.06e-05 |
| `v_su` [m³/kg] | 1.030593528 | 1.030541406 | 5.06e-05 |
| `rpm` [rev/min] | 10102.17848 | 10102.178478 | 1.98e-10 |
| `M_dot` [kg/s] | 0.5445634537 | 0.5445634536 | 1.09e-10 |
| `M_r` | 10.87444857 | 10.87444857 | 0 |
| `N` [rev/s] | 168.3696413 | 168.3696413 | 0 |
| `N_r` | 9.368337444 | 9.368337444 | 0 |
| `r_p` [-] | 2.777777778 | 2.777777778 | 7.99e-11 |
| `cste_1` | 0.02349 | 0.02349 | 0 |
| `cste_2` | 0.8615 | 0.8615 | 0 |
| `p_su` [Pa] | 90000 | 90000 | 0 |
| `p_ex` [Pa] | 250000 | 250000 | 0 |
| `t_su` [°C] | 50 | 50 | 0 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Compared with the solution stored by EES 7.210 in
`MSTH_041012_exercice_7_suite.EES` (`tools/compare_solution.py`, `rtol=0.001`,
without `--ees-units`):
*"13 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0"*.

The largest relative difference over the 13 common variables is **5.06e-05**
(`V_dot_su`). `v_su` prints the same **5.06e-05**. Both stay under the
tolerance. CoolProp `Air` gives `v_su` = 1.030541 m³/kg against the EES
stored 1.030594 m³/kg. `M_dot` is fixed by the reduced-flow law before that
property call, so `V_dot_su = M_dot*v_su` carries the same relative
difference. `rpm` differs by 1.98e-10 and `M_dot` by 1.09e-10. The inputs,
`M_r`, `N` and `N_r` agree. No variable exceeds `rtol=0.001`.

With the `.initials` file, CoolSolve reports all 13 equations satisfied
(max relative residual 2.6124e-10).

A second comparison with `--ees-units` converted no reference value and
rewrote no name. The equations were left unchanged. The quoted summary above
is the run without `--ees-units`.

## Source and attribution

Exercise of the ULiège course *Machines et systèmes thermiques* (repetition 4
of 2004-10-12, exercise 5 continued). The equation window names no person.
The EES licence tag names the ULiège Thermodynamics Laboratory, which
identifies the laboratory.

Source file (EES 7.210, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/MSTH_041012_exercice_7_suite.EES`
(inventory candidate `TM-0060`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): the extract report gives
  the unit system `$UnitSystem SI MASS DEG PA C J`, so no value was rescaled.
  Pressures in the file are already in pascal (`0.9E5`, `2.5E5`). The factor
  `p_su/1E5` and the offset `t_su+273` are the original definition of the
  reduced groups, and both are kept. `t_su` was not rewritten into kelvin.
  Decimal commas were already replaced by the extractor. `$UnitSystem` was
  deleted. The file contains no `$TABSTOPS` and no `$Export`. The licence tag
  and the embedded solution printout were removed. Comments were translated
  to English. **No equation was changed.**
- **2026-10-15 — square system**: with `T_su`/`t_su` and `P_su`/`p_su` left
  as written, CoolSolve reports `System square: Yes` (13 equations, 13
  variables). No spelling was unified. No stored unknown was added. The
  commented lines `V_dot_su=2000/3600` and `rpm=10000` were not turned into
  equations. No diagram-state arrays were added.
- **2026-10-15 — `.initials`**: the 13 values stored by EES, including
  `v_su` on the EES `Air` value. Convergence does not need them (9 iterations
  with the file, 28 without it).
- **Level 1** (taxonomy.md §3): 13 equations (0) + largest block 1 (0) + no
  function, procedure, array or `DUPLICATE` (0) + one machine, not three
  coupled components (0) + one inlet state from two given constants, with no
  calibration, part-load curve or dynamics (0) + converges from default
  guesses, no curated bootstrap and no `coolsolve.conf` (0) = 0 → Introductory.

## Limitations and CoolSolve gaps

- The two constants are imposed. The file computes one new optimal speed and
  one new suction flow. It does not build a performance map.
- The original writes `t_su+273` (not 273.15) inside the reduced variables.
  That offset is kept.
- The `VOLUME(): fluid 'Air'` hint (suggesting `AirH2O` for moist air) is
  not followed. The fluid stays `Air`.
- `t_su = 50` is the Celsius value of the original. It matches the stored
  solution and was not changed.
- No registered CoolSolve gap blocks this model (`missing_features` is empty).

## Related models

No other library model is linked (`related` is empty).
