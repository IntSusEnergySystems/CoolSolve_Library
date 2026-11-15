# Gas spring: a ball oscillating on a gas column

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0339`

A ball of 15 g is displaced by 5 cm in a glass tube (internal radius 0.8 cm);
the gas below it — 1 litre of helium at 24 °C and atmospheric pressure, in the
bottle — is compressed and expanded adiabatically and behaves as a spring,
while the friction damps the motion. The model integrates Newton's law for the
ball with the `INTEGRAL` function over 5 s and returns the trajectory of the
ball position, of the pressure and of the gas temperature, together with the
period of the small oscillations and the specific heat ratio of the gas.

| | |
|---|---|
| **Category** | Fundamentals › Piston-cylinder devices |
| **Fluids** | Helium |
| **Size** | 28 equations (the `-d` analysis reports no block: the block statistics of a model with `INTEGRAL` calls are not usable, `CS-DOC-SQUARE-INTEGRAL`) |
| **Source** | EES example library of F-Chart Software — `~/Nextcloud/thermo_models/EES_library/gas spring.EES` (EES X9.067); plain-text mirror: [EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/gas_spring.ees) (MIT); inventory row `EEL-058` |
| **Authors** | S. A. Klein — the examples are © F-Chart Software |
| **License** | MIT (via the EES-Community mirror) |
| **CoolSolve** | 0.4.0@cc582a6 — verified against the solution and the integral table stored in the EES file (see *Verification*) |

## Problem statement

The original file (F-Chart's EES example "gas spring") states: *"This file
animates the gas spring experiment. A small mass is displaced in a glass tube
and it then oscillates with its amplitude affected by friction. The
oscillation period can be used to identify the specific heat ratio of the
ideal gas in the bottle."*

The data of the experiment are: a glass tube of 1.6 cm internal diameter
(the original writes `Rad = 1.6 [cm]/2`, i.e. a radius of 0.8 cm, and the
cross-section `Area`), a ball of 15 g, an initial volume of gas of 1 litre
at 24 °C, a displacement of the ball of 5 cm from its equilibrium position
and a friction coefficient of 0.01 N·s/m. The atmospheric pressure is
758.7 mmHg.

**Niche.** This model is **not** the spring-loaded piston of `CSL-0210`
(*piston_cylinder_spring_water*), which is a **steady** exercise (water
heated in a cylinder closed by a piston loaded by a linear spring, with
several stages and stops, and a boundary work computed from an integral).
Here the spring is the **gas itself** — an adiabatic gas column under a
ball — and the model is **dynamic**: the motion of the ball is integrated in
time (`INTEGRAL`), the gas state is a function of the ball position, the
friction damps the oscillation, and the model returns a *trajectory*. The
two models share neither the physics (water at 7 MPa against helium at
1 atm), nor the kind (steady against dynamic), nor the purpose (a boundary
work against a period and a damping).

## Model

The ball sits on the gas column (the gas of the bottle below the ball). The
state of the gas follows from the position `L` of the ball (measured from its
equilibrium position, positive upwards):

- the volume of the gas, `V = L·Area + V_o`;
- the ideal-gas law between the current state and the equilibrium state
  (`P_o`, `V_o`, `T_o`), `P·V/T = P_o·V_o/T_o`;
- the adiabatic (reversible) relation of the original, `−R·ln(V/V_o) = c_v·ln(T/T_o)`,
  which with `c_v = c_p − R` and the ideal-gas law gives the classical
  `P·V^γ = const` with `γ = k = c_p/c_v`.

The force balance on the ball is the Newton equation of the original:

    F = P·Area − (P_atm·Area + M_ball·g) − Friction         [N]
    Friction = k_friction·Velocity                            [N]
    F = M_ball·acc                                            [N]

with the two states obtained by integration (`INTEGRAL`), exactly as in the
original file:

    Velocity = INTEGRAL(acc, time, 0, Time_final)             [m/s]
    L = L_o + INTEGRAL(Velocity, time, 0, Time_final)          [m]

The equilibrium pressure is the one that balances the weight of the ball,
`P_static = P_atm + M_ball·g/Area`, and the initial state is the gas at
24 °C and that pressure.

The model also returns the **period of the small oscillations**, the result of
the differential analysis of the original ("the force on the ball is linearly
related to the displacement of the ball from its equilibrium position … the
condition for simple harmonic motion"):

    Tau = 2·pi·sqrt(M_ball·V_o / (k·P_o·Area²))               [s]

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `P_atm` atmospheric pressure | 101 151.7 Pa | `Tau` period of the small oscillations | 0.293711 s |
| `Rad` internal radius of the tube | 0.008 m | `k` specific heat ratio of the gas | 1.66666 [-] |
| `M_ball` mass of the ball | 0.015 kg | `P_static` equilibrium pressure | 101 883.3 Pa |
| `V_o` initial volume of the gas | 0.001 m³ | `c_p`, `c_v` molar specific heats | 20 786.3 / 12 471.8 J/kmol-K |
| `T_o` initial temperature | 24 °C | `L`, `Velocity`, `acc` at *t* = 5 s | 9.345 mm, −0.0268 m/s, −4.248 m/s² |
| `L_o` initial displacement | 0.05 m | `P`, `T` at *t* = 5 s | 101 565 Pa, 23.628 °C |
| `k_friction` friction coefficient | 0.01 N·s/m | | |
| `Time_final` end of the integration | 5 s | | |

## How to run

```bash
coolsolve ./gas_spring_oscillator.eescode
```

The model needs **no guess file**: the two integral states start from their
initial conditions (the ball at `L_o` with a zero velocity), and the solve
ends with *ALL EQUATIONS SATISFIED* (26 equations checked, maximum residual
5.4e-10; the two integral equations are skipped by the verification). The
trajectory is written in the `.sol` file (section *IntegralTable*) and, at
each run, in the file `gas_spring_oscillator-integral.csv` next to the model
(a generated file, not kept in the library).

The model uses no CoolSolve-only syntax: the file is valid EES and can be
solved by EES as well (the values restored in the *Conversion log* are the
ones EES stored for this file).

## Results

Run of `gas_spring_oscillator.eescode` (CoolSolve 0.4.0@cc582a6):

| Quantity | Value |
|---|---|
| Equilibrium pressure `P_static` | 101 883.3 Pa (1.00516 bar) |
| Specific heat ratio `k` | 1.666658 [-] (5/3, as expected for a monatomic gas) |
| Molar specific heats `c_p`, `c_v` | 20 786.3 / 12 471.8 J/kmol-K |
| Period of the small oscillations `Tau` | 0.293711 s |
| First minimum of the displacement | *t* = 0.145 s, `L` = −0.047159 m |
| Period read from the trajectory | 0.2945 s (11 half-periods between 0.145 s and 1.765 s) |
| Ratio of two successive amplitudes | 0.96 (0.047159 m → 0.045302 m), 0.905 after one full period (0.045302 m → 0.041017 m) |
| Amplitude at *t* = 5 s | 9.43 mm (the last extremum, at 4.995 s) |
| State at *t* = 5 s | `L` = 9.3454e-3 m, `Velocity` = −0.026815 m/s, `acc` = −4.2482 m/s² |
| State at *t* = 5 s | `P` = 101 565.0 Pa, `T` = 23.628 °C, `V` = 1.0018790e-3 m³ |

The oscillation is damped but far from being at rest after 5 s: the amplitude
of the oscillation falls from 50 mm (the initial displacement) to 9.4 mm, i.e.
4.8 % per half period, and the ball is still moving at 27 mm/s at the end of
the integration. The period read from the trajectory (0.2945 s) is 0.3 %
above the value of the linearised differential analysis of the original
(`Tau` = 0.29371 s): the analysis is a linearisation about the equilibrium
position, while the gas spring is slightly non-linear over the ±5 cm
excursion (and the friction lowers the frequency a little). The EES
trajectory gives the same period (its extrema are at 0.15, 0.29, 0.44,
0.59 s …, within the 0.01 s step of its table) and the same amplitude ratios
(0.959, 0.948 … against 0.961, 0.945 …).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): trajectory of the
     integration (time, L, Velocity), e.g. from the CoolSolve GUI *Integral* tab,
     figures/gas_spring_oscillator_integral.png -->

## Verification

1. **Against the solution stored in the original EES file** (29 variables
   decoded by `tools/ees_extract.py`), after a hand conversion of the units
   (kPa → Pa, K → °C, kJ/kmol-K → J/kmol-K, cm → m). The stored run of EES
   stopped at *t* = 2.5725 s (its integral table is `inf` beyond *t* = 2.57 s),
   whereas the model integrates to 5 s, so the **variables that depend on the
   end of the integration** (`L`, `Velocity`, `acc`, `P`, `T`, `V`, `F`,
   `Friction`, `time`) are compared separately (point 2). For the variables
   that do not depend on it, `compare_solution.py` gives:

   | Variable | EES | CoolSolve | rel. diff | |
   |---|---:|---:|---:|---|
   | c_p | 20785.5 | 20786.3 | 4.06e-05 | ok |
   | c_v | 12471.1 | 12471.8 | 5.78e-05 | ok |
   | g | 9.807 | 9.80665 | 3.57e-05 | ok |
   | k | 1.66669 | 1.66666 | 1.72e-05 | ok |
   | P_o, P_static | 101883 | 101883 | 3.04e-07 | ok |
   | P_atm | 101152 | 101152 | 4.84e-08 | ok |
   | R | 8314.34 | 8314.46 | 1.47e-05 | ok |
   | Tau | 0.293709 | 0.293711 | 8.76e-06 | ok |
   | Area, L_o, M_ball, Rad, T_o, T_o_abs, V_o, k_friction, Time_final | – | – | 0 (1.48e-10 on Area) | ok |

   `18 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
   CoolSolve: 14` — the fourteen variables that only the model has: the nine
   states and diagnostics (`acc`, `F`, `Friction`, `L`, `P`, `T`, `T_abs`,
   `V`, `Velocity`), the integration variable `time`, the string variable
   `G$` and the built-in constants `g#`, `R#` and `pi`. No variable was
   excluded from this comparison.

   The largest deviation (5.78e-05 on `c_v`) comes from the **properties of
   the helium**: EES evaluates the molar specific heat of its own helium
   (20 785.47 J/kmol-K) while CoolSolve uses CoolProp's (20 786.31 J/kmol-K,
   4.1e-05 apart); `R` differs by 1.5e-05 (EES `R#` = 8314.34 J/kmol-K,
   CoolSolve `R#` = 8314.462618 J/kmol-K) and `g` by 3.6e-05 (9.807 against
   9.80665 m/s²).

2. **Against the same stored solution, at the end of the EES run.** The model
   was re-run with `Time_final = 2.5725 s` (the time at which EES stopped) and
   compared with the **full** stored solution:

   | Variable | EES | CoolSolve | rel. diff | |
   |---|---:|---:|---:|---|
   | L | 0.000522597 | 0.000735081 | 2.89e-01 | **DIFF** |
   | acc | −0.54027 | −0.637143 | 1.52e-01 | **DIFF** |
   | F | −0.00810406 | −0.00955714 | 1.52e-01 | **DIFF** |
   | Velocity | 0.451713 | 0.451216 | 1.10e-03 | **DIFF** |
   | Friction | 0.00451713 | 0.00451216 | 1.10e-03 | **DIFF** |
   | Time_final | 5 | 2.5725 | 4.86e-01 | **DIFF** |
   | T | 23.9792 | 23.9707 | 3.53e-04 | ok |
   | T_abs | 297.129 | 297.121 | 2.85e-05 | ok |
   | P | 101866 | 101858 | 7.15e-05 | ok |
   | V | 0.00100011 | 0.00100015 | 4.27e-05 | ok |

   `28 common variables, 6 differ (rtol=0.001); only in EES: 1; only in
   CoolSolve: 4` (`T_abs`, `T_o_abs` and the three built-in constants
   `g#`, `R#`, `pi`; the variable only in the EES reference is `V_o_liters`,
   which the converted model does not use).

   The large *relative* deviations are on quantities that are nearly zero at
   that instant (the ball crosses its equilibrium position: `acc` and `F`
   change sign, `L` is 0.5 mm) and on the position itself. In **absolute**
   terms the position differs by 0.21 mm on an excursion of ±47 mm. This
   difference is the **integration error of EES**, not a difference of
   physics: an independent integration of the same equations (Runge-Kutta 4,
   step 1e-4 s, with the constants and the initial conditions of EES) gives
   `L` = 7.4535e-4 m at *t* = 2.5725 s, against 7.3508e-4 m for CoolSolve
   (1.3e-5 m) and 5.2260e-4 m for the stored EES solution (2.2e-4 m). The
   same 1e-4 m is seen when the EES trajectory is compared with the model
   (point 3).

3. **Against the integral table stored in the EES file** (502 rows, the
   trajectory of the original run, Δ*t* = 0.01 s). The model was re-run with
   `Time_final` equal to the time of the selected row and compared with
   `compare_solution.py --row`:

   | Row (time) | Variable | EES | CoolSolve | rel. diff | |
   |---|---|---:|---:|---:|---|
   | 51 (0.5 s) | L | −0.012887 | −0.0128253 | 4.79e-03 | **DIFF** |
   | | P | 102325 | 102323 | 2.11e-05 | ok |
   | | T | 24.5144 | 24.5119 | 1.02e-04 | ok |
   | 151 (1.5 s) | L | 0.0241935 | 0.0241028 | 3.75e-03 | **DIFF** |
   | | P | 101063 | 101066 | 3.01e-05 | ok |
   | | T | 23.0402 | 23.0438 | 1.57e-04 | ok |
   | 251 (2.5 s) | L | −0.0215842 | −0.0215661 | 8.35e-04 | ok |
   | | P | 102625 | 102624 | 6.49e-06 | ok |
   | | T | 24.8629 | 24.8621 | 3.06e-05 | ok |

   `4 common variables, 1 differ (rtol=0.001); only in EES: 0; only in
   CoolSolve: 28` (the 28 variables of the model that the row of the table
   does not contain), for the rows 51 and 151; for the row 251 the tool
   prints `4 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
   CoolSolve: 28`. The position differs by at most 0.09 mm (the relative
   deviation is large only because the ball passes through its equilibrium
   position, where `L` is small and its derivative is not); the pressure and
   the temperature agree to 3e-05 and 1.6e-04.

4. **Against an independent integration of the same equations.** The
   trajectory of the model was compared with a Runge-Kutta 4 integration
   (step 1e-5 s) of the equations of the file, written with the constants of
   the model (`R` = 8314.462618 J/kmol-K, `c_v` = 12 471.849 J/kmol-K,
   `P_o` = 101 883.314 Pa, `g` = 9.80665 m/s²): at the end of the
   integration the position agrees to **1.2e-7 m** (9.345238e-3 m against
   9.345356e-3 m) and the velocity to 2.3e-5 m/s; at the intermediate times,
   read from the 5 ms output step of the model, the agreement is 3.3e-6 m.
   The same integration with the *EES* constants gives 7.4535e-4 m at
   *t* = 2.5725 s against the stored EES value of 5.2260e-4 m (see point 2).

## Source and attribution

Example of the EES example library of **F-Chart Software** (© F-Chart
Software), author **S. A. Klein** (the EES licence stamp of the file names
him: `{$ID$ #2177: For use by students and faculty, Dépt Ingénieur
Industriel, HENALLUX, Belgium klein}`; the stamp identifies the licence
holder, not necessarily the author of the model).

Source file: `~/Nextcloud/thermo_models/EES_library/gas spring.EES` (EES
X9.067, inventory row `EEL-058` of `sources/ees_library/inventory.csv`).
The same example is published as plain text under the MIT licence by the
EES-Community mirror: <https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/gas_spring.ees>
(commit 5c703d0, 2026-03-01) — © F-Chart Software / S. A. Klein, MIT via
EES-Community/ees-examples. Published under the MIT licence of the library.

## Conversion log

- **2026-11-12 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES X9.067, equations window stored in RTF (45 lines), 29 variables with
  their stored solution, no lookup table, one parametric table of 502 rows
  (the trajectory stored by the `$IntegralTable` directive). The `$ID$`
  licence tag was removed, the standard header added, the comments kept (they
  are already in English) and the unit system converted **by hand** from
  `SI MOLE DEG KPA K KJ` to SI-°C-Pa-J. The `$UnitSystem` directive was
  deleted.
- **2026-11-12 — unit conversion** (`docs/ees_import.md` §6):
  - `P_atm = 758.7 [mmHg]*convert(mmHg,kPa)` → `P_atm = 101151.7 [Pa]`
    (758.7 mmHg; EES's own value 101 151.7049 Pa);
  - `Rad = 1.6 [cm]/2*convert(cm,m)` → `Rad = 0.008 [m]`;
  - `V_o = V_o_liters*convert(l,m^3)` (1 litre) → `V_o = 0.001 [m^3]`;
    the variable `V_o_liters` is not used any more;
  - `T_o = convertTemp(C,K,24 [C])` → `T_o = 24 [°C]`, with the absolute
    temperature `T_o_abs = T_o + 273.15` added for the two relations that
    need it (the ideal-gas law and the adiabatic relation of the original
    are ratios of absolute temperatures); the temperature of the gas is
    `T` [°C] and `T_abs = T + 273.15` [K];
  - the pressures: `P_static = P_atm + M_ball*g/Area*convert(kg/m-s^2,kPa)`
    → `P_static = P_atm + M_ball*g/Area` (Pa), `P*Area*convert(kPa-m^2,N)`
    → `P*Area` (N), `F = M_ball*acc*convert(kg-m/s^2,N)` → `F = M_ball*acc`,
    `Tau = ... (k*P_o*convert(kPa,Pa)*Area^2)` → `... k*P_o*Area^2`;
  - the **molar** basis of the file is kept explicitly: `R` is the molar gas
    constant (`R#` = 8314.462618 J/kmol-K in CoolSolve, 8314.34 J/kmol-K in
    EES) and the molar specific heats are obtained from the mass-based
    property call, `c_p = MOLARMASS(G$)*cp(G$,T=T_o,P=P_o)` [J/kmol-K];
    the ratio `R/c_v` that drives the adiabatic relation is unchanged by the
    conversion.
- **2026-11-12 — restored inputs**: the equations window of the original file
  does not define three of its inputs (`{L_o=-0.01}` and `{Time_final=5 [s]}`
  are commented out, and `k_friction` appears only in the friction relation)
  and never assigns the string variable `G$`; the model would not run as it
  stands. The values stored by EES for this file are restored:
  `L_o = 0.05 [m]` (5 cm, the value of the animation slider "height of ball
  above equilibrium position at start (-5 to 5)" stored in the file),
  `Time_final = 5 [s]` and `k_friction = 0.01` (the value of the animation
  slider "coefficient of friction (0 to 0.1, 0 is frictionless)").
- **2026-11-12 — the gas of the column**: `G$` is undefined in the original
  file (and in the plain-text mirror of the MIT repository: the same
  undefined string variable appears in `gas_spring.ees`, `spring_2.ees` and
  `spring.ees_2.ees`). It is identified from the **stored solution**: the
  molar specific heat of EES, 20 785.4686 J/kmol-K, is that of a monatomic
  gas (`k` = 1.66669 = 5/3). CoolProp's helium gives 20 786.31 J/kmol-K
  (4.1e-05 apart) while its argon gives 20 835.8 J/kmol-K (2.4e-03 apart),
  and "Helium" is one of the fluids of the recently-used list stored in the
  file (Argon, CO2, Helium, Air, N2, CH4). `G$ = 'Helium'` is therefore used;
  the choice has no effect on the trajectory (the trajectory depends only on
  the ratio `R/c_v`, which is 2/3 for any monatomic gas), it only fixes `c_p`
  and hence `k` and `Tau`.
- **2026-11-12 — GUI and animation objects dropped**: `$tabStops`, the
  `Ball.top` and `ball.fillcolor` diagram objects and the `$IntegralTable`
  directive are display settings of the EES editor, not equations; they are
  not imported (the animation and the diagram window of the original are not
  reproduced — see *Limitations*). CoolSolve always writes the trajectory of
  an `INTEGRAL` model (`gas_spring_oscillator-integral.csv` and the
  *IntegralTable* section of the `.sol` file), so nothing is lost.
- **Level**: equations 28 → 0, largest algebraic block ≤ 5 → 0, a `FUNCTION`
  (`cpg`) → 1, not multi-zone → 0, dynamics → 1, no curated guess needed →
  0 → score 2 → **level 2** (as the triage of the candidate).

## Limitations and CoolSolve gaps

- **No CoolSolve gap blocks this model**: the native file runs as it is and
  `missing_features` is empty. The animation and the diagram window of the
  original file are **not imported** (they are EES GUI objects, not
  equations); this is not registered as a gap here — the register row for the
  diagram and animation windows belongs to card C-518.
- The string variable `G$` of the original is undefined (see the conversion
  log): the file of the library is therefore *not* a byte-for-byte
  transcription of the source, but the restored value is the one EES stored.
- The gas is treated as an **ideal gas** in its adiabatic relation (the
  original writes "adiabatic process: so -Pdv=cv*dT which yields this
  equation where P=R T / V"): the real-gas correction of the helium (its
  compressibility factor is 1.00049 at 1 atm) is neglected, as in the
  original. The molar specific heats, on the other hand, are taken from the
  real-gas properties of the helium (EES and CoolProp), as in the original.
- The friction is a viscous force `k_friction·Velocity` proportional to the
  velocity, with no static friction: the ball does not stay at rest in the
  bottom position, it keeps oscillating around the equilibrium position.
- The ball is a point mass and the tube is a cylinder of constant section;
  no heat transfer to the wall is modelled (the gas is adiabatic).

## Related models

This is the only dynamic gas-column oscillator in the library. The boundary-layer
ODE models use `INTEGRAL` as well, for a different physical system.
`CSL-0342` (*spring_piston_helium_dynamic*) is the same class of damped
`INTEGRAL` oscillator on helium, with an external linear spring returning the
piston instead of the gas column (period 0.055 s against 0.29 s here).
