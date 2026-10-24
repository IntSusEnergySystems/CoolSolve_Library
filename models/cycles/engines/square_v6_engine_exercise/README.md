# Square V6 four-stroke engine (MCI TP3 exercises 1-3)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ❌ **Failing** (runnable variant verified) &nbsp;|&nbsp; `CSL-0275`

Teaching exercise (ULiège MCI, TP3, exercises 1-3 on one square V6 engine:
bore = stroke, connecting-rod length, volumetric compression ratio). Exercise 1
computes the bore and stroke from the displacement, the clearance volume, the
mean piston speed and the instantaneous piston speed and cylinder volume at the
end of the combustion (crank angle 20° after TDC). Exercise 2 computes the
shaft and indicated power from the dynamometer torque and the mechanical
efficiency, the brake mean effective pressure and the friction losses.
Exercise 3 (the default of the file) computes the air-fuel mixture mass per
cycle from the intake state, the fuel and air mass flows, the volumetric
efficiency, the specific fuel consumption and the thermal efficiency. The
exercise is selected by the string `Exercice$` (`$IF`, constant string).

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air, CH4 (ideal gases, molar masses and one air-density check) |
| **Size** | 46 equations, largest block 9 (default exercise 3) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP3_EX-1-2-3-4-5/MCI_TP3_EX-1-2-3.EES` (EES X10.589, stored as RTF) |
| **Authors** | P. Ngendakumana, R. Dickes |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — native file **failing** (over-determined by one redundant identity in the default branch); runnable variant `square_v6_engine_exercise_coolsolve` verified against the EES stored solution (max rel. diff 8.33e-04) |

## Problem statement

Paraphrase of the exercise (the original is the ULiège MCI TP3 sheet, 2017,
exercises 1-3; the French comments of the file are translated in the model).
A square V6 four-stroke engine: 6 cylinders, intermittency factor 0.5,
displacement 3 L, speed 3600 1/min, compression ratio 9.5, connecting-rod
length 0.166 m, end of combustion 20° after TDC. Exercise 2 adds the
dynamometer torque 205 N·m, intake pressure 85 kPa, intake temperature 60 °C
and mechanical efficiency 0.85. Exercise 3 adds the air-fuel ratio 15,
fuel (CH4) lower heating value 50 MJ/kg and combustion efficiency 0.97.
The file's default selection is exercise 3, kept as the regression case.

## Model

Common data and the `L = D` square-engine relation; the exercise branches are
guarded by `$IF Exercice$ = '1' | '2' | '3'` exactly as in the original.

Exercise 1: `V_s = V_s_tot/n_c = pi*(D^2/4)*L` gives the bore and stroke;
`C_m = 2*L*N` the mean piston speed; `r_v = V_bdc/V_tdc` with
`V_bdc = V_c + V_s`, `V_c = V_tdc` the clearance volume; and the standard
slider-crank kinematics give the instantaneous piston speed `C` and the
cylinder volume `V` at the crank angle `theta` of the end of the combustion.

Exercise 2: shaft power `W_dot_sh = -C_fr*omega` (negative, as energy leaving,
as in the original), indicated power `W_dot_in = W_dot_sh/eta_m`, friction
power `W_dot_loss = W_dot_in - W_dot_sh`, theoretical volume flow
`V_dot_th = V_s*N*n_c*i` and brake mean effective pressure
`bmep = (-W_dot_sh/V_dot_th)*1e-5` (the factor reports bar, as written).
`W_dot_sh_hp = W_dot_sh/745.7` converts to hp.

Exercise 3: the mixture mass per cycle `Masse = P_in*V_bdc/(r_mixt*T_in)`
(ideal-gas law at BDC, as in the original) with `r_mixt = R_u/MM_mixt`;
the mass balances `M_f/epsilon_c = f*M_a`, `Masse = M_f + M_a`, the mass
fractions `y_air`, `y_f` and the molar fractions `x_f`, `x_a` of the air-CH4
mixture; the fuel and air mass flows through `M_dot_tr` and the combustion
efficiency; the volumetric efficiency `epsilon_v = M_dot_a/(rho_a*V_s*N*n_c*i)`;
the specific consumption `csp` in g/kWh and the thermal efficiency
`eta_therm` in %.

| Quantity | Role | Value (exercise 3) |
|---|---|---:|
| `n_c`, `i`, `V_s_tot`, `N|star` | cylinders, intermittency, displacement, speed | 6, 0.5, 3×10⁻³ m³, 3600 1/min |
| `r_v`, `B`, `theta` | compression ratio, rod length, end-of-combustion angle | 9.5, 0.166 m, 20° |
| `C_fr`, `P_in`, `T_in`, `eta_m` | dynamometer torque, intake state, mechanical efficiency | 205 N·m, 85 kPa, 60 °C, 0.85 |
| `AFR`, `LHV_f`, `epsilon_c` | air-fuel ratio, heating value, combustion efficiency | 15, 50 MJ/kg, 0.97 |
| `D`, `L` | bore and stroke (square engine) | solved, m |
| `W_dot_sh`, `omega` | shaft power, angular speed | solved, W, rad/s |
| `Masse`, `M_f`, `M_a` | mixture/fuel/air mass per cycle | solved, kg |
| `M_dot_f_cons`, `M_dot_a`, `M_dot_tr` | consumed fuel, air, total mass flows | solved, kg/s |
| `epsilon_v`, `csp`, `eta_therm` | volumetric efficiency, specific consumption, thermal efficiency | solved, −, g/kWh, % |

## How to run

The **native file** `square_v6_engine_exercise.eescode` is valid EES; the
default exercise-3 branch is **over-determined by one equation** (46 numeric
equations, 45 unknowns, `coolsolve -d`: *System square: No*) — see
*Limitations*. Exercises 1 and 2 of the native file are square.

The **runnable variant** is `square_v6_engine_exercise_coolsolve.eescode`
(tested as `CSL-0275:coolsolve`, with its `.sol` baseline):

```bash
../../../../../CoolSolve/build/coolsolve ./square_v6_engine_exercise_coolsolve.eescode
```

It solves from the default guesses (30 iterations). The shipped `.initials`
holds the stored EES values of the equation-window names (temperatures
converted to °C); with it the solver takes 32 iterations. No `coolsolve.conf`.

## Results

Default operating point (exercise 3), runnable variant:

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `D`, `L` bore/stroke [mm] | 86.025 | 86.025 |
| `V_c` clearance volume [cm³] | 58.82 | — |
| `W_dot_sh` shaft power [kW] | −77.283 | −77.283 |
| `Masse` mixture per cycle [g] | 0.4735 | — |
| `M_dot_a` air flow [kg/s] | 0.08006 | — |
| `M_dot_f_cons` consumed fuel [kg/s] | 0.005337 | — |
| `epsilon_v` volumetric efficiency [-] | 0.7507 | 0.7514 |
| `csp` specific consumption [g/kWh] | 248.62 | 248.75 |
| `eta_therm` thermal efficiency [%] | 28.96 | — |

Orders of magnitude: a 3 L V6 at 3600 1/min with 205 N·m at the brake gives
77.3 kW (103.6 hp); a specific consumption near 250 g/kWh and a thermal
efficiency near 29 % at a volumetric efficiency of 0.75 are plausible for a
spark-ignition engine of this size.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![Specific consumption vs speed](figures/square_v6_engine_exercise_param.png)  + one-line caption -->

No thermodynamic state arrays were added: the only property call is the air
density check `rho_a = Density(Air,T=T_amb,P=P_amb)`. The figure placeholder
is left for the maintainer (a parametric sweep over `N|star`, roadmap D7).

## Verification

Reference: the solution stored in `MCI_TP3_EX-1-2-3.EES` (45 names decoded by
`ees_extract.py`). The unit system of the file is `SI MASS DEG PA K J`, so the
comparison uses `--ees-units` (K → °C for `T_in`, `T_amb`). The stored solution
also holds the results of the other exercise branches and of variables absent
from the equation window (`rho_mixt`), left out silently only where named:
`bmep`, `C`, `C_m`, `eta_m`, `R`, `rapV_c`, `rho_mixt`, `V_dot_th`, `W_dot_in`,
`W_dot_in_hp`, `W_dot_loss`, `W_dot_sh_hp`, `W_dot_sh_hp_bis`, `y`.

`compare_solution.py` of the runnable variant (exercise 3) against
`reference/ees_variables.csv --ees-units`:

> 31 common variables, 0 differ (rtol=0.001); only in EES: 14; only in CoolSolve: 17

Maximum relative difference over all common variables, as printed in the
tool's table: **8.33e-04** (`epsilon_v`). Nothing exceeds rtol 0.001.

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `epsilon_v` | 0.751356 | 0.750730 | 8.33e-04 |
| `csp` | 248.749 | 248.622 | 5.07e-04 |
| `r_mixt` | 300.939 | 301.092 | 5.07e-04 |
| `R_u` | 8310.26 | 8314.46 | 5.06e-04 |
| `rho_a` | 1.18453 | 1.18492 | 3.26e-04 |
| `MM_f` | 16.043 | 16.0428 | 1.25e-05 |

The deviations come from the EES-vs-CoolProp backends: EES's stored `R#`
(8310.26 vs 8314.46 J/(kmol·K) in CoolSolve, 5.06e-04) and the molar masses
and air density built on it (`MM_a` and `MM_mixt` agree to 3.5e-07 and
1.6e-06). `W_dot_sh`, `omega`, `T_in` and the geometry agree to ≤ 1e-10.

Branch checks (the variant, `Exercice$` switched in a scratch copy):

- exercise 1: 14 common variables, 0 differ (rtol=0.001), maximum 5.41e-08
  (`y`, the piston displacement);
- exercise 2: 19 of 20 common variables agree to ≤ 1.80e-10, including
  `bmep` 8.58701992 bar; the 20th is `T_in`, 60 °C against the 333.15 K of
  the reference before `--ees-units` — with `--ees-units` the tool also
  converts the stored `bmep` (bar) to Pa, which the equation reports in bar.

The removed identity holds at the solution of the variant to 7.7e-16
(`x_f*MM_f + x_a*MM_a` against `MM_mixt`).

## Source and attribution

Source file
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP3_EX-1-2-3-4-5/MCI_TP3_EX-1-2-3.EES`
(EES X10.589, equations stored as RTF). The `{$ID$}` tag is the EES licence of
the ULiège Thermodynamics Laboratory student/staff licence. The inventory row
TM-0239 names P. Ngendakumana and R. Dickes; the authors column of the
inventory and the `PNG07032019`-style stamps of the sibling files of the
series point to Philippe Ngendakumana (author initials PNG) and Rémi Dickes
(RD). ULiège course MCI (*Machines, combustion et énergie*), TP3, exercises
1-3. Published under the library licence (MIT). Near-duplicate inside the zip
archive of the same folder: TM-0469 (not imported; separate card).

## Conversion log

- **2026-10-22 — import** (card C-315, candidate TM-0239): extracted with
  `CoolSolve/tools/ees_extract.py` (EES X10.589, RTF equations, 152 lines,
  `{$ID$…}`/`{$WD$…}`/`{$PX$…}`/`{$ST$…}` tags removed, 45 names decoded, no
  lookup or parametric table; the trailing NUL byte of the RTF conversion
  removed — `CS-BUG-EXTRACT-NUL`). `$UnitSystem` and `$TABSTOPS` removed.
  Comments translated to English; standard header added; variable names kept
  (`N|star` pipe subscript included). The `{Exercice$ = '1'}` / `{…'2'}`
  comment-braces that select the exercise are kept as in the original; the
  two `//convert(W,hp)` lines of exercise 2 stay as comments (they document
  the alternative hp conversion of the original). No equation was replaced by
  a stored value; the stored values of the unknowns live in the `.initials`.
- **2026-10-22 — unit conversion by hand** (`SI MASS DEG PA K J` → SI-°C-Pa-J,
  ees_import.md §6): `T_in = 60+273.15` → `T_in = 60 "°C (333.15 K in the
  original)"` and `T_amb = 298` → `T_amb = 24.85 "°C (298 K in the original)"`;
  the one absolute-temperature use of `T_in` (ideal-gas mixture mass) became
  `Masse = P_in*V_bdc/(r_mixt*(T_in+273.15))`. The property call
  `Density(Air,T=T_amb,P=P_amb)` now takes T_amb in °C (CoolProp). No other
  value or constant needed rescaling (all other units were already SI).
  Verified with `compare_solution.py --ees-units`.
- **2026-10-22 — over-determination of the default branch** (checked per
  workflow §3 on the extraction with only `$UnitSystem` removed: 47 equations,
  46 unknowns, *System square: No*). In the exercise-3 branch the equation
  `MM_mixt = x_f*MM_f + x_a*MM_a` is an exact identity given
  `x_f = y_f*MM_mixt/MM_f`, `x_a = y_air*MM_mixt/MM_a`, `x_f + x_a = 1` and
  `y_f + y_air = 1`, so the system is over-determined by one equation and
  consistent. EES removed it as redundant when it stored the solution (all 45
  stored values satisfy all 46 equations); CoolSolve rejects non-square
  systems. The native file keeps every equation (valid EES, status `failing`);
  the runnable variant removes this one equation (logged in its header and at
  the place of removal) and is verified above. Not a CoolSolve gap (the same
  treatment as `CSL-0078`); no register row added.
- **Level**: equations 46 (< 50) → 0; largest block 9 (6–30) → 1; no user
  function, procedure, array or `DUPLICATE` → 0; one engine, no multi-zone
  discretisation and no set of three coupled components → 0; textbook
  efficiencies, no calibration, off-design, part-load or dynamics → 0;
  converges from the default guesses in 30 iterations, no tuned
  configuration → 0. Score 1 → **level 1** (the inventory guessed 2).

## Limitations and CoolSolve gaps

- The native file **does not solve** (status `failing`): the exercise-3 branch
  is over-determined by the redundant identity `MM_mixt = x_f*MM_f + x_a*MM_a`
  as the original stands — a property of this file, not a CoolSolve gap
  (EES drops the equation as redundant); the runnable variant above is
  shipped next to it. Exercises 1 and 2 of the native file are square.
- The hp conversions of exercise 2 keep the divisor 745.7 of the original.
- `bmep` is in bar because of the factor `1e-5`, as written.
- The stored EES solution also contains variables of the other exercise
  branches and one name (`rho_mixt`) absent from the equation window; they
  are not part of the model.
- No CoolSolve gap blocks this file. `missing_features` is empty.

## Related models

- `CSL-0244` *engine_dynamometer_test*: TP3 exercise 5 of the same series
  (dynamometer test: shaft power, friction power, bmep, torque).
- `CSL-0178` *intake_valve_sizing*: square engine with mean piston speed
  (TP5 exercise 1).
