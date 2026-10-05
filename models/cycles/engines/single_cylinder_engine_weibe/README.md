# Single-cylinder engine with Weibe combustion (crank-angle dynamic)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ☑️ **Runs** &nbsp;|&nbsp; `CSL-0024`

Crank-angle-resolved model of one cylinder of a four-stroke spark-ignition
engine, integrated over the crank angle with `INTEGRAL`: it follows the
cylinder pressure, temperature and gas mass during the intake stroke, with a
Weibe combustion heat-release rate, a choked intake flow through the intake
valve and wall heat losses. It is the reference dynamic (crank-angle) model of
the library and the simplest example of a `PROCEDURE` called from an
`INTEGRAL` model.

| | |
|---|---|
| **Category** | Cycles › Engines |
| **Fluids** | none (ideal gas, constant γ, molar mass given: no property call) |
| **Size** | 72 equations, 5 of them states integrated over the crank angle (largest algebraic block: 1; the `-d` block statistics are unusable for `INTEGRAL` models, see `CS-DOC-SQUARE-INTEGRAL`) |
| **Source** | CoolSolve example `engine_weibe_cycle` (ULiège engine thermodynamics course exercise, 2008-2009, *Weibe combustion model*, repetition 4) |
| **Authors** | TBD (ULiège course exercise, 2008-2009; author not identified in the source); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs; results reproduce the CoolSolve example and its committed regression value |

## Problem statement

One cylinder of a four-stroke engine (bore 100 mm, stroke 100 mm, connecting
rod 150 mm, compression ratio 10) runs at 3000 rpm with a 0.7 discharge
coefficient intake valve of 6.4 cm² opening at −360° and closing at −180°.
The cylinder is filled from ambient air at 1 bar and 300 K (air/fuel mass
ratio 14.6, fuel LHV 43 MJ/kg); the clearance volume contains residual gas at
1400 K, the walls are at 400 K with an overall coefficient of
500 W/(m²·K). Following the state of the charge along the crank angle gives
the work of the stroke, the mean effective pressure and (with 6 cylinders, a
0.5 mechanical efficiency) the engine power. The combustion is described by
the Weibe function starting at θ_s = −20° with a duration θ_d = 40°.

## Model

The charge is a single ideal gas with a constant ratio of specific heats
(γ = 1.3) and a constant molar mass (29 kg/kmol), so no property call is
needed; the state is closed by the ideal-gas law `p·V = m·r_mel·T`.

> **Temperatures are absolute (kelvin) in this model, as in the original.**
> `T` comes out of the ideal-gas law, so it must be an absolute temperature, and
> it is used as such in the heat flows (`T − T_w`, `T_out − T`). The values of
> the original are consistent with kelvin (ambient 300 K, residual gas 1400 K,
> walls 400 K) and not with the °C of the library's SI-°C-Pa-J convention (the
> example declares no `$UnitSystem` directive). The
> equations are therefore kept as they are and the temperature variables are
> annotated in kelvin; the results are unchanged with respect to the original
> (see *Conversion log*).

- **Kinematics** (θ in degrees, slider-crank with rod ratio B/R = 3):
  piston position `y` from the closed-form slider-crank expression, cylinder
  volume `V = V_c + y·A_p`, and volume rate `V_dot` = piston speed × piston area.
- **States integrated over θ** (5 `INTEGRAL` calls, fixed step 1°, RK4 in
  CoolSolve): `p` (from `p_dot`), `m` (from the intake mass flow), and the
  three accumulators `Q_tot` (combustion heat released), `W_tot` (piston work,
  `p·V_dot`) and `Q_tot_w` (wall losses). Each rate is divided by the crank
  angular speed (`/ (360·N)`) so that the integral is taken with respect to θ.
- **Pressure dynamics**: the ideal-gas energy balance differentiated with
  respect to θ,
  `p_dot = −γ·p/V·V_dot + (γ−1)/V·Q_dot_net + M_dot/m·p`, with the net heat
  rate `Q_dot_net = Q_dot_weibe − Q_dot_w + Q_dot_mel` (combustion, wall losses
  `A_w·U_w·(T − T_w)` with `A_w` the wall plus crown area, and the energy
  carried in by the incoming air `M_dot·C_v·(T_out − T)`).
- **Weibe combustion** (`PROCEDURE weibe`): burned fraction
  `x_b = 1 − exp(−a·((θ−θ_s)/θ_d)^n)` and its rate `x_dot_b` per degree, zero
  before θ_s and the total energy released after θ_s + θ_d; the state
  `Q_tot` integrates `x_dot_b·Q_comb`, and `Q_dot_weibe = x_dot_b·Q_comb·360·N`
  is the rate in W.
- **Intake mass flow**: the choked (sonic) flow through the valve,
  `M_dot = C_d·A_v·p_out/c_son·γ·(2/(γ+1))^((γ+1)/(2(γ−1)))` with
  `c_son = sqrt(γ·r_mel·T_out)`, applied through three nested `IF`s so that it
  is non-zero only between the valve opening and closing angles and only while
  the cylinder pressure is below the ambient pressure.
- **Performance indicators**: `eta_eng = W_tot/Q_comb`,
  `DELTAp_e = W_tot/V_s`, `W_dot_eng = W_tot·i·n_c·N`.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `D` bore | 0.1 m | `W_tot` piston work of the stroke | 59.76 J |
| `L` / `B` stroke / rod length | 0.1 m / 0.15 m | `DELTAp_e` mean effective pressure | 75 993 Pa |
| `R_v` compression ratio | 10 | `eta_eng` work per unit fuel energy | 0.0222 |
| `N` engine speed | 50 1/s | `W_dot_eng` engine power (6 cyl.) | 8.96 kW |
| `A_v` / `C_d` valve area / coefficient | 6.4·10⁻⁴ m² / 0.7 | `p` pressure at −180° | 89 222 Pa |
| `p_out` / `T_out` ambient state | 1 bar / 300 K | `T` temperature at −180° | 276.1 K |
| `MM_mel` / `γ` molar mass / γ | 29 kg/kmol / 1.3 | `m` gas mass at −180° | 9.83·10⁻⁴ kg |
| `f` / `LHV` air–fuel ratio / LHV | 14.6 / 43 MJ/kg | `Q_comb` fuel energy of the charge | 2.689 kJ |
| `T_c` residual gas temperature | 1400 K | `Q_tot` heat released | 0 J (see below) |
| `U_w` / `T_w` wall coefficient / temperature | 500 W/(m²·K) / 400 K | `Q_tot_w` wall losses | −14.48 J |
| `θ_s` / `θ_d` Weibe start / duration | −20° / 40° | `M_dot` intake mass flow | 0.1019 kg/s |
| `a` / `n` Weibe parameters | 5.14 / 3 | `V` volume at −180° | 8.727·10⁻⁴ m³ |

## How to run

Open `single_cylinder_engine_weibe.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./single_cylinder_engine_weibe.eescode
```

No guess values are needed: the model converges from the cold start in about
180 solver iterations (540 for the `RK4` trajectory, 180 accepted steps of 1°,
no rejected step). The trajectory of the integrated states and of the requested
columns is written next to the model as
`single_cylinder_engine_weibe-integral.csv` (read every 5°, as requested by the
`$IntegralTable` directive), and is the basis of the figure
(placeholder below).

## Results

Final state at the end of the integrated stroke (θ = −180°, i.e. bottom dead
centre):

| p [Pa] | T [K] | m [kg] | V [m³] | W_tot [J] | Q_tot_w [J] |
|---:|---:|---:|---:|---:|---:|
| 89 222 | 276.1 | 9.835·10⁻⁴ | 8.727·10⁻⁴ | 59.76 | −14.48 |

Along the stroke the cylinder is filled with 300 K ambient air: the fresh
charge dilutes the 1400 K residual gas, so the temperature falls from 1400 K to
a minimum of 264.8 K at θ ≈ −245° and then rises to 276.1 K. The pressure stays
close to the ambient value during the first ~15° (read every 1°, it oscillates
by about ±1 kPa around 1 bar while the gas mass is still very small — a
step-size effect, see *Limitations*), then drops to a minimum of 66.1 kPa at
θ = −255° and rises to 89.2 kPa at bottom dead centre. The intake mass flow
`M_dot` is 0 until θ ≈ −347° (while `p ≥ p_out`), equals the constant choked
value 0.1019 kg/s from there on, and is 0 again at θ = −180° itself (closing
condition).

**The combustion does not take place in the simulated stroke.** The Weibe
window starts at θ_s = −20° and ends at θ_s + θ_d = +20°, while the model is
integrated from −360° to −180° (the intake stroke; the example's header
announces "intake valve opening to exhaust valve opening", see *Conversion
log*). Consequently `Q_tot` =
0 and `x_b` = 0 at the end of the stroke, and the two indicators
`eta_eng = W_tot/Q_comb` = 0.0222 and `DELTAp_e = W_tot/V_s` = 0.76 bar are
*not* an efficiency and a mean effective pressure: they normalise the piston
work of the filling stroke by the energy of a complete fuel charge. This
inconsistency is in the original (see *Conversion log*); the values are kept
unchanged.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): p and T along the
     crank angle, e.g.  ![Pressure and temperature along the crank angle](figures/single_cylinder_engine_weibe_pt.png) -->

## Verification

There is **no independent reference** for this model: the CoolSolve example
`examples/engine_weibe_cycle.eescode` has no companion `.sol` file and no
original EES file exists for it (neither in `CoolSolve misc/EES_ok.zip` nor in
the ULiège collection `~/Nextcloud/thermo_models`, searched for the Weibe
function, `theta_s`/`theta_d` and `x_dot_b`: 0 hits; the only engine file of the
collection with crank-angle variables is the diesel injection exercise
`TM-0247`, a different exercise). The status is therefore **runs**, with the
following checks.

**1. Reproduction of the example (exact).** The curated file reproduces the
solution of the CoolSolve example on all 75 scalar variables to the last
digit (bit-identical), and therefore also the five-digit final pressure
committed in the CoolSolve regression test for that example
(`tests/test_examples.cpp`: `{"engine_weibe_cycle.eescode", {"p", 89221.7}}`),
i.e. 89 221.7 Pa against the 89 222.2 Pa computed here.

| Variable | CoolSolve example | CSL-0024 | rel. diff |
|---|---:|---:|---:|
| `p` (final pressure) | 89 221.7 Pa | 89 221.7 Pa | 0 |
| `T` (final temperature) | 276.138 K | 276.138 K | 0 |
| `m` (final mass) | 9.834561·10⁻⁴ kg | 9.834561·10⁻⁴ kg | 0 |
| `W_tot` | 59.7635 J | 59.7635 J | 0 |
| `Q_tot_w` | −14.4804 J | −14.4804 J | 0 |
| `eta_eng` / `DELTAp_e` / `W_dot_eng` | 0.0222222 / 75 993.2 Pa / 8 964.5 W | identical | 0 |

**2. CoolSolve solution check.** `coolsolve -d` reports *ALL EQUATIONS
SATISFIED* (67 checked, 0 violated, max |residual| 0), the integral solver
reports RK4 with 180 accepted and 0 rejected steps of 1°.

**3. Geometric check.** The volume computed by the model's slider-crank
expressions agrees with the geometric volume $V(\theta) = V_c + (B + R −
\sqrt{B^2 − R^2\sin^2\theta} − R\cos\theta)A_p$ at the 37 rows of the
trajectory (largest deviation 2·10⁻⁵ m³ on $V_{BDC}$ = 8.73·10⁻⁴ m³), and the
volume ranges from `V_c` at −360° to `V_s + V_c` at −180°, as it should
(top dead centre to bottom dead centre).

**4. Intake flow check.** `M_dot` is 0 before −360°, after −180° and whenever
`p ≥ p_out`, and equals 0.10193 kg/s otherwise; this is the choked (isentropic
throat) flow rate `C_d·A_v·p_out·sqrt(γ/(r_mel·T_out))·(2/(γ+1))^((γ+1)/(2(γ−1)))`
through the discharge section. Over the stroke the model admits
9.617·10⁻⁴ kg, i.e. 5 % more than a full swept volume of ambient air
(`V_s·rho_out` = 9.131·10⁻⁴ kg): the residual gas accounts for 2.17·10⁻⁵ kg of
it, the rest being the cooling of the charge (density at −180°: 1.127 kg/m³
against 1.163 kg/m³ at the intake state, both from `p/(r_mel·T)`). At the
choked rate this corresponds to 9.4 ms of valve opening, i.e. 170 of the 180
crank degrees of the stroke.

## Source and attribution

CoolSolve example `examples/engine_weibe_cycle.eescode`, MIT, © S. Quoilin /
ULiège Thermodynamics Laboratory; its header refers to an *engine
thermodynamics course exercise* (ULiège, 2008-2009, *Weibe combustion model*,
repetition 4) whose author could not be identified. The example has no
companion `.sol` file and no original EES file could be found (see
*Verification*), so this library model is the curated version of the example,
which remains in the CoolSolve repository as a test case.

Sources (not copied into the library):

- CoolSolve example: `~/git/CoolSolve/examples/engine_weibe_cycle.eescode`
  (inventory candidate `CSX-014`);
- search of the ULiège collection (`~/Nextcloud/thermo_models`) and of
  `~/git/CoolSolve/misc/EES_ok.zip`: no original EES file for this exercise
  (see *Verification*).

## Conversion log

- **2026-10-05 — import of the CoolSolve example `CSX-014`**: the example was
  already in SI-°C-Pa-J (`unit_hints: SI-C-Pa-J`), contains no `$UnitSystem`
  directive, no lookup/parametric table, no external file and no library
  function: **no unit conversion and no input had to be restored**. The
  library version is the example plus the standard header, English comments
  with the SI unit of every variable, and section titles. **No equation and no
  value was changed**; the solution is bit-identical to that of the example
  (75/75 scalar variables).
- **2026-10-05 — annotation and naming**: units added to every input
  (`MM_mel` is a molar mass in kg/kmol, since `r_mel = R#/MM_mel` is a specific
  gas constant in J/(kg·K)). `DELTAp_bar_e` renamed `DELTAp_e`: in the
  library's unit system `W_tot/V_s` is a pressure in Pa (75 993 Pa = 0.76 bar),
  the original name announced a unit the equation does not produce.
  **Temperature convention (annotation only, no equation changed):** `T` is an
  absolute temperature in the ideal-gas law of the example, and the values given
  (300, 1400, 400) are consistent with kelvin, not with the °C of the library's
  unit system (the example has no `$UnitSystem` directive). The equations are therefore kept as they are and the
  temperature variables are annotated in kelvin, both in the file and here. An
  alternative curation would be to convert the three temperatures to °C
  (26.85, 1126.85 and 126.85 °C) and to add `+273.15` inside the ideal-gas law
  and in `T_start` ([`ees_import.md` §6.5](https://github.com/CoolProp/CoolSolve/blob/main/docs/ees_import.md)
  of the CoolSolve repository): same physics, same results, but the equations
  would no longer be those of the example. Flagged for the maintainer.
- **2026-10-05 — observation on the original (not modified)**: the integrated
  crank-angle window (−360° → −180°) does not contain the Weibe combustion
  window (−20° → +20°), so `Q_tot` = 0 and `eta_eng`/`DELTAp_e` are not a
  thermal efficiency and a mean effective pressure; the header comment of the
  example announces a wider window ("intake valve opening to exhaust valve
  opening", i.e. −360° → +180°) than the limits actually used. The physics of
  the example was left untouched (see *Limitations* for the test done with the
  wider window). `V_bdc`, `theta_evo`, `theta_evc`, `theta_1` and `theta_2`
  are unused in the equations but were kept, as in the original.
- **Level** (taxonomy.md §3, added at the `C-25` review): 72 equations (1) +
  `PROCEDURE` (1) + dynamics, crank-angle `INTEGRAL` (1) = 3 → the rubric gives
  level 2; the card's level 3 (five coupled integrated states, discontinuous
  Weibe/`IF` closure, step-sensitive) is kept, to be confirmed by the
  maintainer.
- **Decision — the model is `runs`, not `verified`**: no EES original and no
  stored reference exist (searched, see above), so the checks of the
  *Verification* section are reproduction and sanity checks, not a comparison
  against an independent reference.
- **Decision — no state-point arrays** (`P[i]`, `h[i]`, `T[i]`, `s[i]`): the
  charge is an ideal gas with a constant γ and no property call, and CoolSolve
  has no ideal-gas diagram (`CS-FEAT-DIAGRAM-IDEAL`); the figure will be a plot
  of the trajectory (p and T vs θ, *Integral* tab or the
  `single_cylinder_engine_weibe-integral.csv` file).

## Limitations and CoolSolve gaps

- The integrated window is the intake stroke only; the combustion, the
  compression and the expansion strokes are not simulated, so `Q_tot` = 0 and
  the performance indicators are not an efficiency and a MEP (see above).
  Extending the five `INTEGRAL` limits to −360° → +180° was tested: the model
  converges (SUCCESS, 540 iterations) and gives `Q_tot` = 1.72 kJ (64 % of the
  fuel energy), `W_tot` = 854 J, `eta_eng` = 0.318 — but neither `eta_eng` nor
  `W_tot` then has a physical meaning, since the exhaust stroke is not
  described and the intake valve law is not reset at the exhaust. The variant
  is therefore *not* shipped; extending the model to a closed cycle is a
  natural follow-up card.
- **Step-size sensitivity** (check of the `C-25` review, same model with the
  `INTEGRAL` step set to 0.1° instead of 1°): the pressure oscillation of the
  first 20° falls to about ±0.2 kPa and the final state moves to
  `p` = 89 425 Pa (+0.23 %), `T` = 275.97 K, `m` = 9.863·10⁻⁴ kg (+0.29 %),
  with 1800 instead of 180 solver iterations; the shipped 1° results are
  therefore step-dependent at the 0.3 % level, and the sampled `M_dot` of
  the first degrees depends on the step too.
- The intake mass flow uses the three-argument `IF(x, a, b)` of CoolSolve
  (value `a` when `x > 0`, else `b`): CoolSolve-only syntax, not valid EES
  (the EES `IF` has five arguments, `CS-GAP-IF5`). With no EES original
  the file is a CoolSolve model, not a verified EES one.
- Single homogeneous ideal gas with constant γ = 1.3 and a constant molar mass
  29 kg/kmol: no dissociation, no composition change after combustion, no
  blow-by, no friction, no heat transfer to the surroundings other than the
  wall losses with a constant wall temperature, no valve flow coefficients
  other than the discharge coefficient, no exhaust.
- The Weibe function is discontinuous at θ_s and θ_s + θ_d (`x_dot_b` jumps to
  zero); the fixed 1° step of `INTEGRAL` is enough for this window but a
  combustion window inside the integrated range would need a smaller step and
  careful guesses.
- No CoolSolve gap met: the native file runs in the current build. One analysis
  issue was reported (`CS-DOC-SQUARE-INTEGRAL`): the `-d` report of a model with
  `INTEGRAL` calls claims that the system is not square and cannot be solved
  (the integral states are counted as unknowns), although the solve succeeds and
  all equations are satisfied — the block statistics used for the level rating
  are unusable for such models. The
  registered items `CS-BUG-INTEGRAL-TABLE-SEP` (semicolon-separated
  `$IntegralTable` columns), `CS-BUG-INTEGRAL-FACTOR` (factor in front of an
  `INTEGRAL`) and `CS-GAP-INTEGRAL-LIMITS` (symbolic limits) are avoided by the
  example itself, which uses space-separated columns, constant literal limits
  and one `*_scaled` variable per integrated rate.

## Related models

- CoolSolve examples `internal_combustion_engine.eescode` and
  `internal_combustion_engine_cpbar.eescode` (steady-state gas engines with and
  without `cpbar`, not yet in the library); the ULiège MSTh repetition 8
  exercises on the 5 L gas engine (`TM-0121`, `TM-0136`, inventory
  `thermo_models`, still `todo`) are steady-state gas-engine models of the same course
  family (not a counterpart of this crank-angle model: other physics).