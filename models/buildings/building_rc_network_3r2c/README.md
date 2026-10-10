# 3R2C building thermal network with weather lookup

⏱️ **Level 2 · Intermediate** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0042`

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
| **Size** | 55 equations (largest block: 1) |
| **Source** | CoolSolve example `examples/building_rc_network.eescode`, itself simplified from the EES model of the CLIM R06 repetition exercise 2 (University of Liège) |
| **Authors** | S. Quoilin and the ULiège Thermodynamics Laboratory (CoolSolve example); course author of the original EES model `TBD` |
| **License** | MIT |
| **CoolSolve** | 0.3.0@d5d6b37 (branch `fix/library-gaps-2`) — **verified** against an independent RK4 integration of the same equations (max 0.0028 K on `T_in`, 0.0002 K on the two wall temperatures); the native file runs as written (about 8 s) since `CS-GAP-INTEGRAL-LOOKUP` is closed |

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
trajectory (`$IntegralTable tau:600 …`: 1001 rows, 604.8 s apart in the CoolSolve
output) is written to `building_rc_network_3r2c-integral.csv` and at the end of the
`.sol` file.

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
coolsolve ./building_rc_network_3r2c.eescode        # about 8 s
```

No `.initials` and no `coolsolve.conf` are needed. The file keeps the three
`INTERPOLATE` calls in valid EES; its table `building_rc_network_3r2c-week.csv`
is shipped as EES expects it and CoolSolve reads it at every step of the time
march. `building_rc_network_3r2c.sol` is the regression baseline. (Before
CoolSolve `fix/library-gaps-2` the file stopped with *"lookup table 'week' not
found"* and a `_coolsolve` variant with a reconstructed weather was used; it was
removed on 2026-10-10, see the conversion log.)

## Verification

No EES original of this model exists: it is not among the 20 EES files of
CoolSolve `misc/EES_ok.zip`, no file of the ULiège collection
(`~/Nextcloud/thermo_models`) uses this system (`A_opaque`, `C_opaque`,
`R_in_1`, `I_dot_south`, `f_occ` … were searched for), and the CoolSolve
example carries no `.sol`. There is therefore **no EES stored solution to
compare with**; the status **verified** rests on independent re-computations
(the same criterion as the other verified models of the library without an EES
file), done in two ways at the import (on the runnable variant) and repeated on
the native file at the re-check:

1. **Weather against `INTERPOLATE` itself.** At the import, a check model
   evaluated the analytic reconstruction of the variant and
   `INTERPOLATE('week', 'tau', …, tau)` of the shipped table at eight times of
   the week for the three signals: 19 of the 24 differences were exactly 0 and
   the other 5 at double round-off level (max 1.07e-14 °C). Since the native
   file now calls `INTERPOLATE` directly, this check is the file itself.
2. **Trajectory against an independent integration.** Classical RK4 integration
   (Python, fixed step 15 s, hourly linear interpolation of the same table) of
   the *same* equations written from the native file, compared with the
   CoolSolve trajectory (RK45, 1001 output rows) at the output times
   (re-check of 2026-10-10, native file, CoolSolve 0.3.0@d5d6b37):

   | Variable | max &#124;CoolSolve − RK4(h = 15 s)&#124; | at |
   |---|---|---|
   | `T_in` | 0.0028 K (relative 9.8e-5) | `tau` = 115 517 s |
   | `T_c_wall` | 0.0002 K | `tau` = 113 702 s |
   | `T_c_in` | 0.0002 K | `tau` = 503 798 s |

   `T_in` at the end of the week: 30.68246 (RK4) against 30.6825 (CoolSolve).
   The import-time comparison used the 600 s output rows, interpolated: 0.0081 K
   on `T_in` (at `tau` = 0, RK4 grid offset), relative 9.2e-4 — it measured the
   interpolation of the output rows, not the model.
3. **Native file against the former variant.** The `.sol` of the native file
   equals the one of the `_coolsolve` variant (weather reconstructed by
   `clamp01` sums, removed on 2026-10-10) on all 56 common variables (max
   relative difference 5.1e-12, `Q_dot_capa_c_wall`) and on the 13 columns of
   the 1001-row trajectory (identical to the 6 digits printed). The CoolSolve
   example `building_rc_network` (same model, register `CS-GAP-INTEGRAL-LOOKUP`)
   gives the same `T_in` = 30.6825 °C.

Range checks (physical sanity): `T_in` 23.99 – 35.91 °C, `T_c_wall`
21.64 – 28.09 °C, `T_c_in` 24.65 – 33.75 °C, `Q_dot_sens` 0 – 2572.5 W over the
week.

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
- **2026-10-10 — re-check (`T-RECHECK`) with CoolSolve `fix/library-gaps-2`
  @d5d6b37**: `CS-GAP-INTEGRAL-LOOKUP` is closed (the lookup table store is
  now given to the `IntegralSolver`). The native file solves as written (8 s,
  `SUCCESS`), equals the `.sol` of the variant on all 56 common variables
  (max relative difference 5.1e-12) and agrees with an independent RK4
  integration (*Verification*). Status `blocked` → `verified`; the
  `_coolsolve` variant (`.eescode`, `.sol`, its two CSV files) was removed;
  `building_rc_network_3r2c.sol` is the regression baseline. No equation of the
  native file changed (header comment only).
- **2026-10-05 — level**: taxonomy §3 score of the *native* file: equations
  55 (50–300 band → 1), largest algebraic block ≤ 5 (0), no
  functions/procedures/arrays in the native file (0), three coupled
  capacitances → multi-zone (1), dynamics (1), no curated guesses needed (0)
  = **3 → level 2**. The variant adds a `FUNCTION` and the data expansion
  (69 equations, still level ≤ 2 on the count criterion; the variant no longer exists); the pedagogical
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

- **`CS-GAP-INTEGRAL-LOOKUP`** — **closed** in CoolSolve `fix/library-gaps-2`
  (commit `d5d6b37`): a lookup function inside an `INTEGRAL` model now finds
  its table; no gap is left for this model (`missing_features` is empty). A
  lookup written *inline in the base of a state*, `y = LOOKUP(…) + INTEGRAL(…)`,
  is still refused (`CS-GAP-INTEGRAL-BASE-CALL`); this model does not use that
  form (its bases are the variables `T_in_0`, `T_c_wall_0`, `T_c_in_0`).
- *Unverified suggestion (not registered)*: the `$IntegralTable tau:600`
  output interval over 604800 s gives 1001 rows 604.8 s apart (1000 equal
  intervals of the solver's own steps) instead of 1009 rows 600 s apart. The
  repeated last row noted at the import (`604800` twice) no longer occurs with
  CoolSolve 0.3.0@d5d6b37. Reproduced on a 2-equation minimal model
  (`y = 1 + integral(dydt, tau, 0, 604800)`, `dydt = -1e-5·y + 2e-4`,
  `$IntegralTable tau:600 y`), so it is not specific to this import; whether
  EES writes one row per output interval was not verified here.

## Related models

- `CSL-0012` *thermal_comfort_pmv_ppd*: the other model of the `buildings/`
  category (also from the CLIM course; its native file is still blocked, with a
  runnable `_coolsolve` variant).
- `CSL-0106` *conduction_resistances_and_shapes*: the conduction function library of the `ht` source (plane-wall resistance, cylindrical-wall resistance, shape factors, R-value conversions) - the wall resistances written inline in this model as `R = t/(k*A)` are available there as reusable functions.
