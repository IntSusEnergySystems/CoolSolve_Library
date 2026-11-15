# Spring-loaded piston with helium: damped dynamic oscillation

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0342`

A steel piston latched in a well-insulated cylinder encloses helium at 400 kPa
and 290 K; a compressed spring in the evacuated compartment on the other side
pushes it back. When the latch is released, the piston oscillates and the
dynamic friction damps the motion, while the gas expands and cools. The model
integrates Newton's law in time (`INTEGRAL`) and returns the trajectory of the
piston position, pressure, volume and temperature over 1 s.

| | |
|---|---|
| **Category** | Fundamentals › Piston-cylinder devices |
| **Fluids** | Helium |
| **Size** | 24 equations (the `-d` analysis reports no block: the block statistics of a model with `INTEGRAL` calls are not usable, `CS-DOC-SQUARE-INTEGRAL`) |
| **Source** | EES example library of F-Chart Software — `~/Nextcloud/thermo_models/EES_library/spring.EES` (EES X8.802); plain-text mirror: [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/spring.ees) (MIT); inventory row `EEL-106` |
| **Authors** | S. A. Klein — the example is © F-Chart Software |
| **License** | MIT (via the EES-Community mirror) |
| **CoolSolve** | 0.4.0@cc582a6 — verified against the solution and the integral table stored in the EES file (see *Verification*) |

## Problem statement

The original file (F-Chart's EES example "spring") states: *"A piston, latched
into place within a well-insulated cylinder encloses helium, initially at a
pressure of 400 kPa and a temperature of 290 K. The inside diameter of the
cylinder is 0.2 m. A compressed spring is located in the right compartment of
the cylinder which is evacuated. The spring exerts a force towards the left of
a magnitude F=K x where the spring constant K is 6000 N/m and x is the distance
from the far left side of the cylinder. The piston is latched in place at a
location of x=0.30 m. […] The piston is made of steel and its thickness is
[5 mm]. The latch is released, allowing the piston to move with dynamic
friction until it finally ceases oscillating and stops. The thermal capacitance
of the piston and cylinder may be neglected."*

## Niche

This model is **not** a duplicate of `CSL-0210` (*piston_cylinder_spring_water*),
which is a **steady** exercise (water heated in a cylinder closed by a piston
loaded by a linear spring, stages and stops, boundary work of a heating
process). Here the spring-loaded piston is a **dynamic helium oscillation**:
Newton's law is integrated in time (`INTEGRAL`), the friction damps the motion
and its dissipation appears in the energy balance of the gas, which expands
adiabatically and cools from 16.85 °C to −137 °C at the first minimum of the
pressure (53.7 kPa). Nor is it `CSL-0339` (*gas_spring_oscillator*), where the
**gas column itself** is the spring under a free ball: here the spring is an
external linear spring and the gas (initially at 400 kPa, 26 times the
amplitude of `CSL-0339`) only resists through its pressure — the rest position
of the piston is set by the spring, `P·A = K·x`, not by the atmosphere. The two
models are the same class of damped `INTEGRAL` oscillator (they are linked) and
make the comparison instructive: spring- vs gas-stiffness, 0.055 s vs 0.29 s
period.

## Model

Geometry and initial state (variables of the original):

    A = pi·(d²/4)            cross-section of the piston           [m²]
    V_1 = A·x_1              initial volume of the helium          [m³]
    m_p = A·density_steel·thk  mass of the piston                  [kg]
    n = P_1·V_1/(R·T_1_abs)  moles of helium (ideal gas law)       [kmol]

with `d` = 0.2 m, `x_1` = 0.3 m, `thk` = 0.005 m, `density_steel` = 8000
kg/m³, `T_1` = 16.85 °C (290 K in the original), `P_1` = 400 000 Pa (400 kPa),
`R` = `R#` = 8314.46 J/kmol-K and the molar specific heat of the helium
`c_v = MOLARMASS(Helium)·cv(Helium, T=T_1, P=P_1)` [J/kmol-K].

Dynamic analysis, exactly the equations of the original (unit factors removed,
see the *Conversion log*):

    F_net = m_p·acc                              Newton's law            [N]
    F_net = P·A − K·x − k_fric·vel               net force               [N]
    vel = INTEGRAL(acc, time, 0, time_final)     velocity                [m/s]
    x = x_1 + INTEGRAL(vel, time, 0, time_final) position of the piston  [m]
    V = A·x                                      volume of the helium    [m³]
    P·V = n·R·T_abs                              ideal gas law
    n·c_v·(T−T_1) = INTEGRAL(−P·A·vel + k_fric·vel², time, 0, time_final)
                                                 energy balance          [J]

The gas does work on the piston (`−P·A·vel`) and receives the friction power
(`k_fric·vel²`); both terms are in the energy balance of the original. The
trajectory is tabulated every 1 ms by `$IntegralTable time:0.001 x, P, V, T`,
as in the original. The animation objects of the original (positions, widths
and the lock of the diagram window) are **not imported** (see the *Conversion
log*).

| Inputs | Value | Outputs (at *t* = 1 s) | Value |
|---|---|---|---|
| `d` piston diameter | 0.2 m | `x` piston position | 0.695414 m |
| `x_1` initial (latched) position | 0.3 m | `vel` piston velocity | 0.106138 m/s |
| `T_1` initial temperature | 16.85 °C | `P` helium pressure | 136 538 Pa |
| `P_1` initial pressure | 400 000 Pa | `V` helium volume | 0.0218471 m³ |
| `K` spring constant | 6000 N/m | `T` helium temperature | −43.6873 °C |
| `k_fric` friction coefficient | 10 N·s/m | `c_v` molar specific heat | 12 475.7 J/kmol-K |
| `thk` piston thickness | 0.005 m | `m_p` piston mass | 1.256637 kg |
| `density_steel` steel density | 8000 kg/m³ | `n` moles of helium | 1.563504e-3 kmol |
| `time_final` end of the integration | 1 s | | |

## How to run

```bash
coolsolve ./spring_piston_helium_dynamic.eescode
```

The model needs **no guess file**: the three integral states start from their
initial conditions (the piston at `x_1` with zero velocity and the gas at
`T_1`), and the solve ends with *ALL EQUATIONS SATISFIED* (24 equations, 21
checked, the three integral equations skipped by the verification). The
trajectory is written in the `.sol` file (section *IntegralTable*) and, at each
run, in the file `spring_piston_helium_dynamic-integral.csv` next to the model
(a generated file, not kept in the library).

The file is valid EES except for the unit conversions of the *Conversion log*
and can be solved by EES as well.

## Results

Run of `spring_piston_helium_dynamic.eescode` (CoolSolve 0.4.0@cc582a6):

| Quantity | Value |
|---|---|
| First extremum | *t* = 0.027 s, `x` = 1.0455 m (the piston moves right, the gas expands) |
| Extrema of `x` (maxima) | 1.0455, 0.9793, 0.9256, 0.8821, 0.847 … m at *t* = 0.027, 0.081, 0.136, 0.192, 0.247 s |
| Extrema of `x` (minima) | 0.380, 0.4444, 0.4962, 0.5378, 0.5706 … m at *t* = 0.054, 0.109, 0.164, 0.219, 0.275 s |
| Period read from the trajectory | ≈ 0.055 s (≈ 18 oscillations in the 1 s integrated) |
| Amplitude decay | ≈ 6 % per period at the start, slowing down as the amplitude falls |
| Range over the trajectory | `x` from 0.3 to 1.0455 m, `P` from 400 kPa down to 53.7 kPa, `T` from 16.85 °C down to −137.4 °C |
| State at *t* = 1 s | `x` = 0.695414 m, `vel` = 0.106138 m/s, `P` = 136 538 Pa, `V` = 0.0218471 m³, `T` = −43.6873 °C |

The piston first accelerates to the right (the gas at 400 kPa pushes with
12.6 kN against a spring force of 1.8 kN), overshoots to `x` = 1.0455 m while
the gas expands and cools by 154 °C, and then oscillates around the rest
position of the spring, `P·A = K·x`, with a slowly decaying amplitude (the
friction of the original is a viscous force `k_fric·vel`, so the decay is
exponential and the piston is still moving at 0.106 m/s at *t* = 1 s — it does
not "cease oscillating" within the integrated time). The EES trajectory stored
in the file stops at *t* = 0.721 s (see *Verification*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): trajectory of the
     integration (time, x, P, T), e.g. from the CoolSolve GUI *Integral* tab,
     figures/spring_piston_helium_dynamic_integral.png -->

## Verification

1. **Against the solution stored in the original EES file** (29 variable
   records decoded by `tools/ees_extract.py`), after the hand conversion of the
   units (`$UnitSystem SI MOLE DEG KPA K KJ` → SI-°C-Pa-J, §6 of
   `docs/ees_import.md`). The stored run of EES stopped at *t* = 0.7212 s (its
   integral table is `inf` beyond *t* = 0.721 s), whereas the model integrates
   to 1 s, so the **variables that depend on the end of the integration** were
   compared with a re-run of the model at `time_final = 0.7212471652 s` (point
   2). Point 1 is the comparison of the full model at *t* = 1 s:

   `23 common variables, 9 differ (rtol=0.001); only in EES: 1; only in
   CoolSolve: 4` — the nine differing variables are the eight end-of-integration
   states (`x`, `vel`, `acc`, `F_net`, `P`, `T`, `V`, `time`) and `k_fric`
   (the reference stores 0.01 **kN**-s/m, a unit the `--ees-units` conversion of
   the tool does not touch: 0.01 kN-s/m = 10 N-s/m, the value of the model).
   The only variable of the EES reference that the model does not have is `SF`,
   an animation scale factor (not imported); the model adds `T_abs`, `T_1_abs`
   and the built-in constants `pi`, `R#`. All the variables that do not depend
   on the end of the integration agree: `c_v` 1.01e-04, `n` and `R` 1.47e-05,
   `m_p` 3.47e-10, `A` 1.31e-10, the inputs exactly (`d`, `x_1`, `T_1`, `P_1`,
   `K`, `thk`, `density_steel`).

2. **Against the same stored solution, at the end of the EES run** (model
   re-run with `time_final = 0.7212471652 s`):

   `23 common variables, 6 differ (rtol=0.001); only in EES: 1; only in
   CoolSolve: 4` — the six: `k_fric` and `time_final` (see point 1) and four
   physics deviations, `vel` 3.02e-01, `acc` and `F_net` 6.26e-03, `T` 3.91e-03,
   while `x` (1.90e-04), `P` (4.91e-04), `V` (1.90e-04) and `time` (0.00e+00)
   agree.

   The velocity deviation is a **phase effect** at the end of an oscillation of
   period 0.055 s, not a difference of physics (point 4): an independent
   integration of the same equations (Runge-Kutta 4, step 1e-5 s) gives
   `x` = 0.6805755 m and `vel` = 0.276770 m/s at *t* = 0.7212471652 s, against
   0.680577 m and 0.278717 m/s for CoolSolve — and 0.6807065 m and
   0.1945957 m/s for the stored EES solution, whose trajectory lags by about
   0.5 ms. The same picture as for `CSL-0339`: the stored EES trajectory
   carries the integration error of EES.

3. **Against the integral table stored in the EES file** (1002-row parametric
   table, the trajectory of the `$IntegralTable` directive; 722 rows are
   filled, *t* = 0 to 0.721 s in steps of 1 ms; converted by hand from kPa and
   K). All 722 common rows were compared with the CoolSolve trajectory of the
   same run:

   | Variable | max rel. diff | max abs. diff | |
   |---|---:|---:|---|
   | `x` | 4.952e-03 (row *t* = 0.264 s) | 3.98e-03 m | ok |
   | `P` | 7.858e-03 (row *t* = 0.208 s) | 1208 Pa | ok |
   | `V` | 4.951e-03 | – | ok |
   | `T` | 2.457e-01 (row *t* = 0.11 s) | 0.79 K | ok |

   The relative deviations are largest where the oscillation amplifies the
   phase difference between the two integrators (EES's own integration error,
   point 2 and 4); the largest absolute deviations are 4 mm of piston travel on
   an excursion of 0.75 m and 0.79 K on 154 °C of excursion. The `T` relative
   deviation of 2.457e-01 is at a crossing of the reference value −0.46 °C,
   where the relative measure is meaningless (0.11 K absolute).

4. **Against an independent integration of the same equations.** A Runge-Kutta
   4 integration (step 1e-5 s) of the three state equations of the model, with
   the constants of the solution (`A` = 3.141592654e-2 m², `m_p` = 1.256637061
   kg, `n` = 1.563503781e-3 kmol, `c_v` = 12 475.747915 J/kmol-K, `R` = 8314.46
   J/kmol-K, `K` = 6000 N/m, `k_fric` = 10 N·s/m), agrees with the model at the
   end of the integration: *t* = 1 s, `x` = 0.695414 m (identical to 6e-7 m),
   `vel` = 0.105356 m/s (model 0.106138 m/s, a near-zero-crossing phase
   difference of 7e-4 m/s), `T` = −43.6861 °C (model −43.6873 °C).

## Source and attribution

Example of the EES example library of **F-Chart Software** (© F-Chart
Software), author **S. A. Klein** (the EES licence stamp of the file names him:
`{$ID$ #0001: For use only by Professor S.A. Klein University of Wisconsin -
Madison klein}`; the stamp identifies the licence holder, not necessarily the
author of the model).

Source file: `~/Nextcloud/thermo_models/EES_library/spring.EES` (EES X8.802,
inventory row `EEL-106` of `sources/ees_library/inventory.csv`). The same
example is published as plain text under the MIT licence by the EES-Community
mirror: <https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/spring.ees>
(commit 5c703d0, 2026-03-01) — © F-Chart Software / S. A. Klein, MIT via
EES-Community/ees-examples. Published under the MIT licence of the library.

## Conversion log

- **2026-11-14 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES X8.802, plain-text equations window (48 lines), 29 variable records with
  their stored solution, no lookup table, one parametric table of 1002 rows
  (the trajectory stored by the `$IntegralTable` directive; 722 rows filled,
  the EES run stopped at *t* = 0.721 s). The `$ID$` licence tag was removed,
  the standard header added, the comments kept (they are already in English)
  and the unit system converted **by hand** from `SI MOLE DEG KPA K KJ` to
  SI-°C-Pa-J. The `$UnitSystem` directive was deleted.
- **2026-11-14 — unit conversion** (`docs/ees_import.md` §6):
  - `T_1 = 290 [K]` → `T_1 = 16.85 [°C]`, with `T_1_abs = T_1 + 273.15` and
    `T_abs = T + 273.15` added for the two relations that need an absolute
    temperature (the ideal-gas law of the original is written on `T` in K);
    the temperature *difference* `T − T_1` of the energy balance is unchanged;
  - `P_1 = 400 [kPa]` → `P_1 = 400000 [Pa]`; `P·V = n·R·T` now balances in
    Pa·m³ = J (in the original kPa·m³ = kJ with `R` in kJ/kmol-K);
  - `k_fric = 0.01 [kN-s/m]` → `k_fric = 10 [N-s/m]`;
  - `F_net = P·A·convert(kN,N) − k·x − k_fric·vel·convert(kN,N)` →
    `F_net = P·A − k·x − k_fric·vel`: with `P` in Pa the products are already
    newtons, the two `convert(kN,N)` factors are gone;
  - the **molar** basis of the file is kept explicitly, as in `CSL-0339`:
    `n` [kmol], `R = R#` [J/kmol-K] and
    `c_v = MOLARMASS(Helium)*cv(Helium,T=T_1,P=P_1)` [J/kmol-K] (the original
    calls the EES molar `cv` directly; CoolSolve's `cv` is mass-based, so the
    molar value is obtained through the molar mass).
- **2026-11-14 — restored inputs**: the equations window of the original does
  not assign four of its inputs (`P_1 = 400 [kPa]`, `K = 6000 [N/m]`,
  `K_fric = 0.01 [kN-s/m]`, `time_final = 2 [sec]` are inside a commented
  block "Information in Diagram Window" — diagram-window inputs of the
  original). The values stored by EES for this file are restored:
  `P_1 = 400000 [Pa]`, `K = 6000 [N/m]`, `k_fric = 10 [N-s/m]` and
  `time_final = 1 [s]` (the stored run used 1 s, not the 2 s of the comment;
  the stored integral table ends at *t* = 0.721 s). `thk = 0.005 [m]` is
  assigned in the equations of the original (5 mm; the problem statement of
  the MIT mirror says 8 mm, but the stored solution corresponds to 5 mm).
- **2026-11-14 — animation objects dropped**: the "Animation information"
  block of the original (`Cylinder.*`, `Piston.*`, `Spring.*`, `Helium.width`,
  `Lock.*`, `SF`, `PixelsperInch#`, `GetDiagramAttribute`, the `if` on
  `Lock.top`) and the `$tabstops` directive are EES GUI objects of the diagram
  window, not equations; they are not imported. The animation and diagram
  window of the original are not reproduced (this is not registered as a gap —
  the register row for the diagram and animation windows belongs to card
  C-518). CoolSolve always writes the trajectory of an `INTEGRAL` model
  (`spring_piston_helium_dynamic-integral.csv` and the *IntegralTable* section
  of the `.sol` file), so nothing of the physics is lost.
- **Level**: equations 24 → 0, largest algebraic block ≤ 5 → 0, no
  function/array structure → 0, not multi-zone → 0, dynamics → 1, no curated
  guess needed → 0 → score 1 → **level 1**.

## Limitations and CoolSolve gaps

- **No CoolSolve gap blocks this model**: the native file runs as it is and
  `missing_features` is empty. The registered bugs `CS-BUG-UNARY-POW` (unary
  minus and power) and `CS-GAP-NAME-PRIME` (prime in a variable name) are not
  met by this file: it has no `-x^2` form and no prime name. The `vel^2` of the
  energy balance is computed correctly although `vel` changes sign (verified
  against the RK4 integration, point 4).
- The animation and the diagram window of the original file are **not
  imported** (EES GUI objects, not equations — see the *Conversion log*).
- The gas is treated as an **ideal gas** (`P·V = n·R·T`), as in the original;
  the molar specific heat, on the other hand, is taken from the real-gas
  properties of the helium (EES and CoolProp), as in the original. The process
  is adiabatic for the gas (well-insulated cylinder), with the friction power
  dissipated **into** the gas (the `k_fric·vel²` term of the energy balance of
  the original).
- The friction is a viscous force `k_fric·vel` proportional to the velocity,
  although the original calls it "dynamic friction": the amplitude therefore
  decays exponentially and never reaches exactly zero within the 1 s integrated.

## Related models

- `CSL-0339` *gas_spring_oscillator* — the same class of damped `INTEGRAL`
  oscillator on helium, but with the gas column as the spring (free ball,
  period 0.29 s); here a linear spring returns the piston (period 0.055 s).
- `CSL-0210` *piston_cylinder_spring_water* — a **steady** water-heating
  exercise in a spring-loaded piston-cylinder (stages, stops, boundary work):
  the same hardware, another kind of problem.
