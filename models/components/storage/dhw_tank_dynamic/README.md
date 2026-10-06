# Domestic hot-water storage tank: dynamic temperature evolution

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0009`

A 500 L domestic hot-water (DHW) tank, modelled as a fully mixed lumped
capacity: the transient first law is integrated over a 5-hour scenario
(heating, cooldown, tap draw with cold make-up water, ambient losses), giving
the tank temperature trajectory T_tank(τ). It is the library's example of an
EES `INTEGRAL`/`$IntegralTable` time-integration model.

| | |
|---|---|
| **Category** | Components › Storage |
| **Fluids** | Water (constant cp = 4186 J/kg·K in the balance) |
| **Size** | 20 equations, all explicit per time step (largest block: 1); 1 state variable (`DELTAu`), 18 000 steps of 1 s |
| **Source** | ULiège — course *Thermodynamique appliquée et introduction aux machines thermiques* (MECA0002-1), repetition 3, exercise 3 (EES file `R3_E3_2022.EES`) |
| **Authors** | N. Paulus, B. Dechesne (ULiège repetition assistants, per the source inventory and its companion files) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked** by `CS-GAP-IF5`, `CS-GAP-INTEGRAL-LIMITS`, `CS-BUG-INTEGRAL-TABLE-SEP` and `CS-BUG-INTEGRAL-MAXSTEPS`; the variant `dhw_tank_dynamic_coolsolve.eescode` runs and is verified against the EES integral table (≤ 6.1·10⁻⁵) |

## Problem statement

A 500 L domestic hot-water storage tank initially at 60 °C and atmospheric
pressure is equipped with a 10 kW electric heater that runs for one hour and
then stops for one hour. A constant tap draw of 0.05 kg/s then flows for two
hours; the withdrawn water is replaced by city water at 12 °C. Ambient losses
are considered during the whole process (global exchange coefficient
AU_amb = 20 W/K, ambient at 20 °C). Plot the tank temperature over 5 hours.

## Model

Transient first law over the whole tank (kinetic and potential energy
neglected, no work):

$$\dot Q_{res} + \dot Q_{amb} + \dot Q_{tap} = \frac{dU}{d\tau},
\qquad \Delta U = M_{tank}\, c_p\, (T_{tank} - T_{tank,0})$$

- heater schedule: $\dot Q_{res} = 10\,000$ W for $\tau \le 3600$ s, 0 after
  (EES `IF(tau,3600,10000,10000,0)`),
- tap draw: $\dot m = 0.05$ kg/s for $7200 \le \tau \le 14\,400$ s
  (two nested `IF` functions),
- draw power (fully mixed tank, outlet at $T_{tank}$):
  $\dot Q_{tap} = -\dot m\, c_p\, (T_{tank} - T_{in})$,
- ambient losses: $\dot Q_{amb} = -AU_{amb}\,(T_{tank} - T_{amb})$,
- tank mass from the water specific volume at the initial state
  (`volume(Water, T=60, P=1e5)`, 491.6 kg),
- $T_{tank}$ is the implicit state: $\Delta U = $ `INTEGRAL(dU/dτ, τ, 0, 18 000, 1)`
  with a fixed step of 1 s, tabulated every second (`$IntegralTable`).

| Inputs | Value | Main outputs |
|---|---|---|
| `Vol_tank` | 0.5 m³ | `T_tank(τ)` trajectory (60 → 75.8 → 39.4 °C) |
| `T_tank_0` / `T_in_tank` / `T_amb` | 60 / 12 / 20 °C | `Q_dot_res`, `Q_dot_tap`, `Q_dot_amb` [W] |
| `Q_dot_res` (heater) | 10 kW, 0–1 h | final `T_tank` = 39.44 °C at τ = 5 h |
| `M_dot_in_tank` (draw) | 0.05 kg/s, 2–4 h | final `DELTAu` = −42.31 MJ |

## How to run

The original file `dhw_tank_dynamic.eescode` keeps the native EES syntax
(5-argument `IF`, symbolic limits `tau_1`/`tau_2`, `;`-separated
`$IntegralTable`) and does **not** run in CoolSolve v0.3.0 (see *Limitations
and CoolSolve gaps*). The runnable transcription is:

```bash
coolsolve ./dhw_tank_dynamic_coolsolve.eescode    # ~2 min, 18 000 RK4 steps
```

It needs `coolsolve.conf` (`integralMaxSteps = 20000`, see
`CS-BUG-INTEGRAL-MAXSTEPS`). The trajectory is written every second to
`dhw_tank_dynamic_coolsolve-integral.csv` (18 001 rows) and shown in the GUI
*Integral* tab.

## Results

| τ [h] | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `T_tank` [°C] | 60.00 | 75.82 | 73.90 | 53.67 | 40.13 | 39.44 |
| `Q_dot_res` [kW] | 10 | 10→0 | 0 | 0 | 0 | 0 |
| `M_dot_in_tank` [kg/s] | 0 | 0 | 0 | 0.05 | 0.05→0 | 0 |

The heater raises the tank by 15.8 K in one hour; the draw removes 33.8 K
between 2 and 4 h; after the draw the tank keeps cooling towards the ambient
at ~0.16 K per half hour.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T_tank and the
     heat rates vs time from the Integral tab, figures/dhw_tank_dynamic_trajectory.png -->

## Verification

The source EES file stores the **integral table** of the last run. The
extractor mis-decodes the embedded grid (a false-positive "table1" 761×2, see
the conversion log), but the six plot objects of the file each embed one full
column of the table (18 002 80-bit floats, identified and decoded during this
import; the columns are mutually consistent to ~1e-12: `dU/dτ = Q̇_res +
Q̇_tap + Q̇_amb`, `Q̇_amb = −20·(T−20)`, `Q̇_tap = −ṁ·4186·(T−12)` and the
schedules match the `IF` equations exactly).

The runnable variant was compared with this reference over **all 18 001
points** (CoolSolve v0.3.0, RK4, 1-s step):

| Quantity | max. relative deviation |
|---|---:|
| `T_tank` | 3.1·10⁻⁵ |
| `dU\dtau`, `Q_dot_amb` | 6.1·10⁻⁵ |
| `Q_dot_tap` | 1.3·10⁻⁵ |
| `Q_dot_res`, `M_dot_in_tank` (schedules) | exact (0) |

Selected time steps and the final value:

| τ [s] | 0 | 1800 | 3600 | 7200 | 10800 | 14400 | 18 000 |
|---|---|---|---|---|---|---|---|
| `T_tank` EES [°C] | 60.00000 | 67.97734 | 75.81634 | 73.89638 | 53.67363 | 40.13338 | 39.43974 |
| `T_tank` CoolSolve [°C] | 60.00000 | 67.97730 | 75.81630 | 73.89690 | 53.67400 | 40.13360 | 39.44090 |

The residual differences (≤ 0.003 K) come from the different integration of
the discontinuous `IF` schedules at 3600/7200/14 400 s (EES vs RK4 midpoint
sampling); far from the switches the trajectories agree to ~1e-4 K. The
water properties match the EES stored solution to 10 digits
(`v_tank` = 1.017091982·10⁻³ m³/kg, `M_tank` = 491.5976223 kg). The stored
main-solution values of the EES file are unreliable here (`T_tank = 1`,
leftovers of an older equation set), which is why the integral table is the
reference.

## Source and attribution

Exercise of the ULiège course *Thermodynamique appliquée et introduction aux
machines thermiques* (MECA0002-1, 2022–2023), repetition 3, exercise 3. The
EES file names no author; the repetition assistants of that year
(N. Paulus, B. Dechesne) are credited following the source inventory —
to be confirmed by the maintainer.

Source file (EES X10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R3/R3_E3_2022.EES`
(inventory candidate `TM-0413`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): unit system already
  `SI MASS DEG PA C J` (no conversion needed); decimal comma converted to the
  dot convention; licence tag removed; comments translated to English and
  standard header added; the equations are unchanged.
- **2026-10-05 — reference data.** The report announced a parametric table
  "table1 (761×2)" but the decoded grid is a false positive (it chains the
  variable-units list: `Btu/lbm`, `psia`, `kJ/kg`…, no usable values). The
  real integral table (18 001 rows × 7 columns at 1-s interval, as announced
  by `$IntegralTable tau:1`) was recovered from the six plot objects embedded
  in the file (each plot stores one full column after the series name, offset
  +651) and cross-checked for internal consistency (~1e-12) and against the
  `IF` schedules. The stored main solution is stale (`T_tank = 1`,
  `T_out_tank = 31.07` from an older equation set; `M_tank`, `v_tank`,
  `tau = 18 000` valid).
- **2026-10-05 — runnable variant** `dhw_tank_dynamic_coolsolve.eescode`:
  identical physics and 1-s step, three syntactic transcriptions — the EES
  5-argument `IF(A,B,X,Y,Z)` replaced by the 3-argument `if(cond,a,b)` with
  the condition shifted by half a step (`if(3600.5-tau,10000,0)` is true for
  τ ≤ 3600 s, exactly the EES schedule at the 1-s grid; gap
  `CS-GAP-IF5`); the symbolic limits `tau_1`, `tau_2` replaced by their
  literal values (gap `CS-GAP-INTEGRAL-LIMITS`); `$IntegralTable` columns
  space-separated (`CS-BUG-INTEGRAL-TABLE-SEP`). `coolsolve.conf` raises
  `integralMaxSteps` because the default 1000 silently truncates the run at
  τ = 4000 s with a SUCCESS message (`CS-BUG-INTEGRAL-MAXSTEPS`). Verified
  against the EES integral table (see *Verification*).
- **Level 1** (score 1: only the *dynamics* criterion; the `coolsolve.conf`
  setting works around a CoolSolve bug, not an intrinsic difficulty; in line
  with the inventory guess).

## Limitations and CoolSolve gaps

- Fully mixed tank (no stratification), constant water cp, constant tank
  mass, UA_amb independent of temperature — the level of detail of the
  exercise.
- The main file is **blocked** by (see CoolSolve
  `docs/model_library_support.md`):
  - `CS-GAP-IF5` — the EES intrinsic `IF(A,B,X,Y,Z)` (5 arguments) is not
    supported ("Unknown or unsupported function: if with 5 arguments"); the
    heater and draw schedules need it;
  - `CS-GAP-INTEGRAL-LIMITS` — `INTEGRAL` limits must be constants; the
    model uses the variables `tau_1`, `tau_2`;
  - `CS-BUG-INTEGRAL-TABLE-SEP` — `;`-separated `$IntegralTable` columns
    silently produce empty columns;
  - `CS-BUG-INTEGRAL-MAXSTEPS` — the integration silently stops at
    `integralMaxSteps*4` steps before the final time and reports SUCCESS
    (worked around with `coolsolve.conf`).
- Solve time of the variant ≈ 2 min (18 000 RK4 steps, one property call per
  step for the initial state only).

## Related models

- `CSL-0041` *ice_storage_tank_discharge_phase_change*: ice-storage discharge
  with phase change (MSTh R6 Ex4), same `INTEGRAL`/`$IntegralTable` pattern,
  blocked by the same gaps, with its own runnable variant; the DG-0023 copies
  of the exercise (TM-0092/TM-0095/TM-0123) are recorded as its duplicates.
- `CSL-0100` *free_conv_enclosed_and_jackets*: the vessel-jacket heat-transfer
  coefficient of Lehrer and Stein-Schmidt rates the heat transfer of this tank.
