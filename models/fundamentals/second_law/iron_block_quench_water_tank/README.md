# Iron block quenched in a water tank (exergy destruction)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0056`

A classic closed-system second-law exercise: a hot iron block is dropped into
an insulated rigid tank of water, and the model computes the final equilibrium
temperature (first law) and the exergy destroyed by the quench — the *wasted
work potential* of the process. The exergy of the combined system is evaluated
at the initial and final states with the incompressible-substance formula,
which makes it a good introduction to exergy balances on isolated systems.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | None (iron and water as incompressible substances with constant specific heats) |
| **Size** | 21 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition session 10, exercise 1 (EES file `R10_E01_2022.EES`, session 2022-2023) |
| **Authors** | TBD (ULiège, course *Thermodynamique appliquée*; the companion course files name S. Quoilin and the repetition assistants N. Paulus and B. Dechesne) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

A 5 kg iron block initially at 350 °C is quenched in an insulated tank
containing 100 kg of water at 30 °C. The water that vaporises during the
process is assumed to condense back in the tank, and the surroundings are at
20 °C and 100 kPa. Determine:

1. the final equilibrium temperature of the combined system;
2. the wasted work potential (exergy destruction) of the process.

The original also evaluates the exergy of the combined system at the initial
and final states (parts of the same exercise in the course Python solution).

## Model

The combined system (block + water + rigid tank) is closed, rigid and
adiabatic, so the first law reduces to $\Delta U = 0$; with constant specific
heats and thermal equilibrium at the end:

$$m_b c_b (T_f - T_{b,i}) + m_w c_w (T_f - T_{w,i}) = 0$$

The exergy of an incompressible substance at temperature $T$ in an environment
at $T_0$ (rigid tank, so the $P_0 \Delta V$ term drops) is
$X = m\,c\,[(T - T_0) - T_0 \ln(T/T_0)]$, summed over block and water at the
initial and final states. The exergy balance of the isolated system
($X_{in} = X_{out} = 0$) gives the exergy destruction
$X_{destroyed} = X_{tot,i} - X_{tot,f}$, which the original also rewrites in a
direct form (`X_destroyed_bis`, algebraically identical).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `m_b`, `T_b_i` block | 5 kg, 350 °C | `T_f` final temperature | 31.713 °C |
| `m_w`, `T_w_i` water | 100 kg, 30 °C | `X_tot_i` initial exergy | 314 817 J |
| `T_0`, `p_0` environment | 20 °C, 100 kPa | `X_tot_f` final exergy | 95 800 J |
| `c_b`, `c_w` specific heats | 450 / 4180 J/(kg·K) | `X_destroyed` = wasted work potential | 219 017 J |

`p_0` is given by the statement but enters no equation (rigid tank,
$\Delta V = 0$), as in the original.

## How to run

Open `iron_block_quench_water_tank.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./iron_block_quench_water_tank.eescode
```

Every equation is explicit: no guess values (`.initials`), no solver settings
and no runnable variant are needed.

## Results

| Variable | Value | Unit |
|---|---:|---|
| `T_f` (final equilibrium temperature) | 31.7133 | °C |
| `X_b_i` / `X_w_i` (exergy of block / water, initial) | 245 103 / 69 714 | J |
| `X_tot_i` (combined system, initial) | 314 817 | J |
| `X_b_f` / `X_w_f` (exergy of block / water, final) | 513 / 95 287 | J |
| `X_tot_f` (combined system, final) | 95 800 | J |
| `X_destroyed` = `X_destroyed_bis` | 219 017 | J |

Almost 70 % of the initial exergy of the combined system is destroyed by the
unrestrained heat transfer over the large temperature difference of the
quench.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. X_destroyed vs the dead-state temperature T_0 (Parametric tab, 1D plot),
     figures/iron_block_quench_water_tank_sweep.png -->

## Verification

1. **EES stored solution.** Compared with the solution stored in the source
   file (`compare_solution.py … --ees-units`): **17 common variables, 0 differ
   (rtol=0.001)**, largest relative deviation **4.15·10⁻¹⁰** (`T_f`); every
   input agrees exactly. The `KJ` unit string that EES stored for the `X_*`
   variables is not converted by `--ees-units` (tool bug
   `CS-BUG-COMPARE-UNIT-CASE`, registered on the CoolSolve side): the
   comparison above was run on a copy of the reference with `KJ` → `kJ`; on
   the raw reference the same 8 variables are falsely reported **DIFF** with
   rel. diff 9.99e-01 (a factor 1000).
   - Five records of the EES reference are not variables of the model: `ds`,
     `dT` and `T` (values 1, 1, 623.15) do not appear in the equations window
     of either file of the duplicate group (stale Variable Info records), and
     `T_f_ad` / `T_f_Celcius` were the original's K→°C display hack, dropped in
     the conversion (`T_f` is in °C natively).
   - Four CoolSolve variables have no EES counterpart: the absolute-temperature
     helpers `T_b_i_K`, `T_w_i_K`, `T_0_K`, `T_f_K` added by the conversion.
2. **Course Python solution.** The course folder holds a Python solution of
   the same exercise of the previous session
   (`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R10/old/ThAp21_R10E01.py`,
   plain Python + `math`, no property call): run here, it prints 31.7 °C for
   the final temperature and 219.02 kJ for the exergy destruction (labelled
   "entropy destruction" in its print statement), in agreement with the table
   above. It is used as an independent reference only, not copied.

## Source and attribution

Solution of repetition exercise 1 (session 10, exergy on closed systems) of
the ULiège course *Thermodynamique appliquée* (MECA0002), session 2022-2023.
The EES file names no author (its `{$ID$}` tag is the laboratory's
student/staff licence); the companion course files attribute the session to
the repetition assistants N. Paulus and B. Dechesne (course by S. Quoilin) —
to be confirmed by the maintainer.

Source file (EES X10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R10/R10_E01_2022.EES`
(inventory candidate `TM-0388`, representative of the 2-file duplicate group
`DG-0092`; `TM-0543` is the same file inside `R10.zip`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES X10.836, 22 variable records, no lookup or parametric table, only the
  built-in `ln` as function call; decimal comma converted to the dot
  convention by the extractor; `{$ID$}`, `{$PX$96}` and `{$ST$OFF}` tags
  removed. Unit system `SI MASS DEG KPA K KJ` converted **by hand** to
  `SI MASS DEG PA C J`: `T_b_i = 350 [C]` (623.15 K), `T_w_i = 30 [C]`
  (303.15 K), `T_0 = 20 [C]` (293.15 K), `p_0 = 100E3 [Pa]` (100 kPa),
  `c_b = 450 [J/kg-K]` (0.450 kJ/kg-K), `c_w = 4180 [J/kg-K]`
  (4.180 kJ/kg-K), each with the original value in the comment. The first-law
  equation is unchanged (temperature differences only). Because the exergy
  equations need absolute temperatures in their logarithms, four explicit
  helpers `T_b_i_K`, `T_w_i_K`, `T_0_K`, `T_f_K` (`= T + 273.15`) were added
  and used there, keeping the original form of the equations. The original's
  display-hack lines `T_f_ad = T_f*1[1/K]` and
  `T_f_Celcius = T_f_ad*1[C] - 273.15 [C]` (K→°C conversion for display) are
  superseded by the native °C `T_f` and were removed (dead code). Comments
  translated to English (paraphrasing the French original), section titles in
  the `"!…"` display form, standard header added, equations otherwise
  unchanged. The unmodified extraction fails to parse on the four
  `350[K]+273.15`-style lines — the already-registered unit-annotation gap
  `CS-GAP-UNIT-SUBEXPR`; the hand unit conversion rewrites exactly those
  lines, so the converted file needs no workaround. Verified against the EES
  stored solution (see above).
- **Level**: equations 21 (< 50 → 0), largest algebraic block 1 (≤ 5 → 0),
  no arrays/`DUPLICATE` (0), no multi-zone/discretisation (0), no
  semi-empirical/off-design physics (0), no curated guesses or solver
  settings (0) → score 0 → level 1.

## Limitations

- Constant specific heats evaluated near ambient temperature, block and water
  incompressible, no vaporisation modelled (the statement assumes any formed
  vapour condenses back), as in the original: the final temperature comes out
  below 100 °C, which the original checks in a comment.
- `p_0` (ambient pressure) is not used by the equations, as in the original.
- No CoolSolve gap blocks this model.

## Related models

- `CSL-0045` *steam_turbine_exergy_balance*: same course and session family
  (repetition 10, 2022-2023), exergy balance of an *open* system (flow
  exergy) against the closed-system exergy of this model.
