# 3R2C building thermal network with weather lookup

⏱️ **Level 2 · Intermediate** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0042`

Single-zone building thermal network of the 3R2C type: three thermal
capacitances (indoor air, opaque facade, internal masonry walls) coupled
through thermal resistances, driven over one week (168 h) of July weather
(outdoor temperature, south solar irradiance and occupancy factor read from
a table). Ventilation is the only heat sink: there is no active cooling, so
the zone heats up and the free-running temperature swing of a *passive*
building over a sunny summer week is obtained. Useful as an exercise /
demonstration of a low-order building model and of CoolSolve's
equation-based time integration.

| | |
|---|---|
| **Category** | Buildings |
| **Fluids** | none (property calls) — moist air treated as humid air with constant density and heat capacity |
| **Size** | native file: 55 equations; runnable variant: 69 equations (largest block: 1) |
| **Source** | CoolSolve example `examples/building_rc_network.eescode`, itself simplified from the EES model of the CLIM R06 repetition exercise 2 (University of Liège) |
| **Authors** | S. Quoilin and the ULiège Thermodynamics Laboratory (CoolSolve example); course author of the original EES model `TBD` |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — the native file is **blocked** by `CS-GAP-INTEGRAL-LOOKUP`; the variant `building_rc_network_3r2c_coolsolve.eescode` runs and is verified against an independent RK4 integration of the same equations (max 0.008 K on `T_in`, 0.0002 K on the two wall temperatures) |

## Problem statement

Model a single room of 4 m × 6 m × 2.7 m ventilated at 60 m³/h with 14 °C
supply air, with a glazed south facade (`A_glazing = 4.5 m²`,
`U = 3 W/m²·K`, solar shading factor 0.5), an opaque facade of 6.3 m² and
internal masonry walls, and with occupant, lighting and appliance gains
scaled by an occupancy factor. Starting from 25 °C everywhere, follow the
indoor air temperature, the facade temperature and the internal wall
temperature over one week of July weather (sunny days, 13.5 to 30.5 °C, up
to 850 W/m² of south irradiance, occupancy factor between 0 and 1). No
cooling unit is active (`Q_dot_clim = 0`), so the zone warms up during the
day.

## Model

Three capacitances, three resistances, as in the original:

- **Indoor air node** — capacitance `C_in = 5·V_in·ρ·c_p` (the factor 5 of
  the original, as in the original), fed by the internal gains
  (`Q_dot_sens = Q_dot_clim + Q_dot_light + Q_dot_appl + Q_dot_occ +
  Q_dot_sol`), by the ventilation flow `H_dot_vent = C_dot_su·(T_su − T_in)`
  and by the glazing, the opaque facade and the internal walls through their
  respective resistances.
- **Opaque facade node** — areal capacitance `C_opaque = 360 kJ/m²·K`
  between the internal and external surface resistances
  `R_in_1 = 0.1964` and `R_out_1 = 0.1149 m²·K/W`.
- **Internal masonry walls node** — areal capacitance
  `C_InternalWalls = C_opaque / 2`, seen from the room through
  `R_in = 1/h_in + R_w/2` with `h_in = 8 W/m²·K` and `R_w = 0.1429 m²·K/W`.

Each state is written in the EES integral form and integrated over
`[0, 604800] s` with `INTEGRAL` (CoolSolve time march, RK45 by default); the
trajectory is recorded every 600 s in `building_rc_network_3r2c_coolsolve-integral.csv`
and at the end of the `.sol` file.

The weather signals are the columns `T_out` [°C], `I_dot_south` [W/m²] and
`f_occ` [−] of the table `building_rc_network_3r2c-week.csv` (169 hourly
rows, `tau` = 0 … 604800 s; a July sunny week, from the tables p. 4.12 and
2.23 of the CLIM course as stated in the original). Weather rows:

| `tau` [s] | `T_out` [°C] | `I_dot_south` [W/m²] | `f_occ` [−] |
|---|---|---|---|
| 0 | 25.5 | 0 | 0.0 |
| 28 800 | 15.44 | 425 | 1.0 |
| 43 200 | 19.15 | 850 | 1.0 |
| 64 800 | 29.00 | 0 | 1.0 |
| 198 000 | 16.56 | 220 | 0.3 |
| 604 800 | 25.5 | 0 | 0.0 |

| Inputs (default) | Value | Main outputs (week) | Value |
|---|---|---|---|
| `Haut`×`Prof`×`Larg` | 2.7×6×4 m | `T_in` at the end of the week | 30.68 °C |
| `V_dot_su_m3h` / `T_su` | 60 m³/h / 14 °C | `T_in` range over the week | 23.99 – 35.91 °C |
| `Q_dot_occ_max` / `Q_dot_light_max` / `Q_dot_appl_max` | 160 / 250 / 250 W | `T_c_wall` range | 21.64 – 28.09 °C |
| `A_glazing` / `U_glazing` / `SF` | 4.5 m² / 3 W/m²·K / 0.5 | `T_c_in` range | 24.65 – 33.75 °C |
| `A_opaque` / `C_opaque` | 6.3 m² / 360 kJ/m²·K | `Q_dot_sens` range (internal gains) | 0 – 2572 W |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): for a dynamic
     model the trajectory of the Integral tab (T_in, T_c_wall, T_c_in and T_out
     against tau), exported as PNG, e.g.
     ![Indoor and wall temperatures over one week](figures/building_rc_network_3r2c_trajectory.png)
     — three zone temperatures of a free-running single-zone building over a
     sunny summer week -->

## How to run

```bash
coolsolve ./building_rc_network_3r2c.eescode        # blocked: CS-GAP-INTEGRAL-LOOKUP
coolsolve ./building_rc_network_3r2c_coolsolve.eescode   # runnable variant (about 45 s)
```

No `.initials` and no `coolsolve.conf` are needed. The **native file**
`building_rc_network_3r2c.eescode` keeps the three `INTERPOLATE` calls and is
valid EES, but CoolSolve does not provide the lookup table store to the
time-march loop, so it fails with
`INTERPOLATE(): lookup table 'week' not found (no table store is available in
this context)`; its table `building_rc_network_3r2c-week.csv` is shipped as
EES expects it. The **runnable variant**
`building_rc_network_3r2c_coolsolve.eescode` (+ `.sol`, regression baseline,
tested as `CSL-0042:coolsolve`) replaces only those three calls; its own
companion table `building_rc_network_3r2c_coolsolve-week.csv` holds the same
169 rows (the variant does not read it — see the conversion log).

## Verification

No EES original of this model exists: it is not among the 20 EES files of
CoolSolve `misc/EES_ok.zip`, no file of the ULiège collection
(`~/Nextcloud/thermo_models`) uses this system (`A_opaque`, `C_opaque`,
`R_in_1`, `I_dot_south`, `f_occ` … were searched for), and the CoolSolve
example carries no `.sol`. There is therefore **no EES stored solution to
compare with**, and the verification was done in two independent ways:

1. **Weather reconstruction against `INTERPOLATE` itself.** A check model
   (`work/` folder of the import, not shipped) evaluated the analytic
   reconstruction of the variant and `INTERPOLATE('week', 'tau', …, tau)` of
   the shipped table at eight times of the week (knots 0/1 h, midpoints
   0.5/1.5 h, 20.33 h, 47.25 h, 83.5 h and the end 168 h) for the three
   signals: **19 of the 24 differences are exactly 0 and the other 5 sit at
   double round-off level (max |difference| = 1.07e-14 °C on `T_out`, i.e.
   1.3e-17 relative to a peak signal of 850 W/m²)** — the residue of summing
   the 168 hourly increments instead of interpolating between two of them.
   The reconstruction is therefore numerically identical to the native
   lookup, not an approximation.
2. **Trajectory against an independent integration.** The variant was solved
   with CoolSolve (RK45, trajectory every 600 s) and compared with an
   independent classical RK4 integration of the *same* equations written from
   the native file (fixed step 15 s, hourly linear interpolation of the same
   table), evaluated at the 1002 tabulated times:

   | Variable | max &#124;CoolSolve − RK4(h = 15 s)&#124; | at |
   |---|---|---|
   | `T_in` | 0.0081 K | `tau` = 0 s (25.0000 vs 24.9919 °C) |
   | `T_c_wall` | 0.0002 K | `tau` = 113 702 s |
   | `T_c_in` | 0.0002 K | `tau` = 503 798 s |

   The `T_in` deviation is largest at `tau` = 0, where CoolSolve reports the
   initial condition exactly (25 °C) while the RK4 grid starts one step later;
   the RK4 reference itself converges (300 s → 9.18e-4, 60 s → 9.20e-4,
   15 s → 9.21e-4 relative on the linearly interpolated tabulated values,
   i.e. the difference is the linear interpolation of the 600 s output
   interval, not a modelling error).

Because no independent *reference solution* (EES, publication, other tool)
was available, the status of the model is the status of its **native file**
(`blocked`), as the taxonomy prescribes; the numbers above are the
verification of the runnable variant.

## Source and attribution

- Authors of the source file: S. Quoilin and the ULiège Thermodynamics
  Laboratory (CoolSolve example `examples/building_rc_network.eescode`, MIT).
  The author of the original EES model of the CLIM R06 repetition exercise 2
  is `TBD` (the exercise notes are not part of the collection).
- Course: *CLIM* (Climatisation), University of Liège; the example header
  cites tables p. 4.12 and 2.23 of the course notes as the origin of the
  weather data, and states that the model is a simplification ("variant 2a:
  constant ventilation, no cooling unit") of that original EES model.
- Source path: `~/git/CoolSolve/examples/building_rc_network.eescode`
  (CoolSolve checkout; candidate `CSX-006` of
  `sources/coolsolve_examples/inventory.csv`). The example itself stays in
  the CoolSolve repository; this folder holds the curated copy.
- Weather data: shipped as `building_rc_network_3r2c-week.csv`, taken verbatim
  from the example's companion file `building_rc_network-week.csv`.

## Conversion log

- **2026-10-05 — import (T-IMPORT, roadmap card C-44)**: copied the CoolSolve
  example, replaced its header by the library header, added the SI unit of
  every dimensional variable in the trailing comments and turned the section
  titles into `"!…"` display comments. **No unit conversion was needed**: the
  example is already in `SI-C-Pa-J` (`temperature [C]`, `Pa`, `J`, `s`,
  `m³/h`→`m³/s` conversion already explicit as `V_dot_su_m3h/3600`) and has
  no `$UnitSystem` directive. No equation, constant or variable name was
  changed; no dead code was found (`tau_1`, `tau_2`, `N_h`, `DELTAtau` are
  unused by the equations but document the interval, they were kept).
  Comments paraphrase the original ("as in the original").
- **2026-10-05 — runnable variant** (`building_rc_network_3r2c_coolsolve.eescode`,
  forced by `CS-GAP-INTEGRAL-LOOKUP`): the three lines
  `T_out = INTERPOLATE('week','tau','T_out',tau)` and the two siblings are
  replaced by the exact piecewise-linear reconstruction of the **same 169
  rows** of the table, written as `value(0) + Σ_k Δy_k·clamp01(tau_hour−k)`
  with a new one-argument `FUNCTION clamp01(h)` (`if(h, if(h-1,1,h), 0)`), split
  over one line per day of the week (`T_out_p1…T_out_p8`,
  `I_dot_south_p1…p4`, `f_occ_p1…p2`); the three signal names and every other
  equation of the native file are unchanged. `clamp01` reproduces
  `INTERPOLATE` exactly (value 0 below the first row, linear interpolation in
  between, flat extrapolation above the last row — verified above: 19 of the
  24 sampled differences are exactly 0, the 5 others ≤ 1.07e-14 °C).
  Everything else (geometry, resistances, gains,
  integration interval, output interval, `$IntegralTable` column list) is
  identical to the native file, so the two files differ only in how the
  weather is obtained. The variant uses the 3-argument inline `if(cond,a,b)` of
  `clamp01` (CoolSolve `docs/ees_vs_coolsolve.csv` line 34: *3-arg IF function,
  cond>0 returns true_val*): this is **CoolSolve-only syntax, not valid EES**
  (EES has the 5-argument `IF(A,B,X,Y,Z)`, see `CS-GAP-IF5`; wording corrected
  at the C-46 review). Everything else of the variant is valid EES.
- **2026-10-05 — level**: taxonomy §3 score of the *native* file: equations
  55 (50–300 band → 1), largest algebraic block ≤ 5 (0), no
  functions/procedures/arrays in the native file (0), three coupled
  capacitances → multi-zone (1), dynamics (1), no curated guesses needed (0)
  = **3 → level 2**. The variant adds a `FUNCTION` and the data expansion
  (69 equations, still level ≤ 2 on the count criterion); the pedagogical
  content is unchanged, so the level of the model stays 2 (taxonomy allows
  ±1 with justification).

## Limitations and CoolSolve gaps

Physical limitations (as in the original): the capacitances and resistances
are lumped and constant; the zone is unglazed/unshaded except through a
single constant shading factor; no moisture, no radiative long-wave exchange
with the sky, no internal heat storage beyond the three nodes, no control;
`C_in = 5·V_in·ρ·c_p` carries the factor 5 of the original (as in the
original).

CoolSolve gaps (`../CoolSolve/docs/model_library_support.md`):

- **`CS-GAP-INTEGRAL-LOOKUP`** — a lookup function (`INTERPOLATE`, …) inside
  an `INTEGRAL` model: the lookup table store is not wired into the
  `IntegralSolver`, so the native file fails at the initial algebraic solve
  with *"INTERPOLATE(): lookup table 'week' not found (no table store is
  available in this context)"*. Already registered (P2, with this example as
  its reproducer); not re-reported here. Minimal reproducer confirming it is
  unchanged: 3 equations — `T_out = INTERPOLATE('wk','tau','T_out',tau)` /
  `y = 1 + INTEGRAL(dydt, tau, 0, 604800)` / `dydt = (T_out − y)/3600` with a
  `wk` table of two rows → same error (also when the lookup is called from a
  `FUNCTION`, so it is not a scoping accident of the main program).
- *Unverified suggestion (not registered)*: the trajectory table repeats its
  last row (`604800` appears twice in `$IntegralTable` output) when the
  output interval divides the integration interval; the 600 s interval over
  604800 s also yields 1002 rows instead of 1009 (the rows are written at the
  solver's own step times). Reproduced on a 4-equation minimal model
  (`y = 1 + integral(dydt, tau, 0, 604800)`, `dydt = -1e-5·y + 2e-4`,
  `$IntegralTable tau:600 y`), so it is not specific to this import; whether
  EES writes exactly one row per output interval was not verified here.

## Related models

- `CSL-0012` *thermal_comfort_pmv_ppd*: the other model of the `buildings/`
  category (also from the CLIM course, also blocked, with a runnable
  `_coolsolve` variant).
- `CSL-0106` *conduction_resistances_and_shapes*: the conduction function library of the `ht` source (plane-wall resistance, cylindrical-wall resistance, shape factors, R-value conversions) - the wall resistances written inline in this model as `R = t/(k*A)` are available there as reusable functions.
