# Rankine cycle with cooling-water condenser, generator/motor and part load

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0140`

A superheated-steam Rankine cycle on water after the TESPy basic tutorial
*Rankine Cycle*: a steam turbine (isentropic efficiency), a feed pump, a
steam generator with a pressure drop and a main condenser cooled by a
cooling-water stream. The model solves **two operating points of the same
plant simultaneously**: the design point (live steam mass flow and turbine
outlet pressure given) with its generator and pump-motor efficiencies, and a
**part-load point** whose turbine inlet pressure is given by Stodola's cone
law, whose condenser heat-transfer coefficient `UA` keeps its design value and
whose cooling-water volumetric flow stays constant — so the condensing
pressure and the cooling-water return temperature move with the load.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water (working fluid and cooling water) |
| **Size** | 105 equations, largest implicit block: 17 (two coupled cycle points + 16 post-processing state arrays) |
| **Source** | TESPy tutorial `tutorial/basics/rankine.py` ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`), companion docs `docs/basic_tutorials/rankine_cycle.rst` |
| **Authors** | Francesco Witte (TESPy lead developer) and the TESPy contributors; Stodola cone law from TESPy `Turbine.cone_func`; LMTD smoothing from S. Quoilin (PhD thesis 2011) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; translation verified against TESPy (see *Verification*) |

## Problem statement

A steam power plant delivers live steam at 600 °C and 150 bar with a mass flow
of 10 kg/s to a steam turbine whose outlet pressure is 0.1 bar. The steam
generator has a pressure ratio of 0.9, the turbine an isentropic efficiency of
0.9 and the feed pump an isentropic efficiency of 0.75. The main condenser
has no steam-side pressure drop (pr1 = 1), a 2 % pressure drop on the cooling
water side (pr2 = 0.98) and is cooled by a cooling-water stream entering at
20 °C / 1.2 bar and leaving at 30 °C. Determine the duties, the turbine and
pump powers, the cycle efficiency and the turbine outlet quality. With a
generator and a pump motor of efficiency 0.97 each, compute the net power
delivered to the grid. Then study the plant at part load, assuming that the
turbine follows Stodola's cone law, that the condenser keeps its `UA` value
and that the cooling-water volumetric flow is constant.

## Model

State numbering follows the TESPy connection labels: 1 live steam at the
turbine inlet, 2 turbine outlet, 3 condensate at the condenser outlet, 4 feed
water at the pump outlet, 11/12 cooling water at the condenser inlet/outlet;
the suffix `_pl` marks the part-load point.

- **Cycle closer** (TESPy `CycleCloser`): `h_0 = h_1`, `p_0 = p_1`, so the
  steam generator is written once.
- **Steam generator** (TESPy `SimpleHeatExchanger pr`): `p_0 = pr_sg·p_4`,
  `Q_sg = m_1·(h_0 − h_4)` (adiabatic).
- **Feed pump** (TESPy `Pump eta_s`): `h_4 = h_3 + (h_4s − h_3)/eta_s_fp`
  with `h_4s = h(s_3, p_4)`.
- **Main condenser** (TESPy `Condenser`, `pr1`, no subcooling): `p_3 = pr_mc1·p_2`
  and the condensate sits on the bubble line, `h_3 = h(p_3, x = 0)`;
  cooling water `p_12 = pr_mc2·p_11`; energy balance
  `m_11 = Q_mc/(h_12 − h_11)`.
- **Steam turbine** (TESPy `Turbine eta_s`):
  `h_2 = h_1 − eta_s_tu·(h_1 − h_2s)` with `h_2s = h(s_1, p_2)`.
- **Condenser rating** (TESPy `Condenser.calculate_lmtd`, `ttd_u_func`,
  `HeatExchanger.UA_func`): terminal temperature differences to the dew line
  `ttd_u = T_dew(p_2) − T_12` and `ttd_l = T_3 − T_11`, smoothed LMTD
  (`LMTD_smoothed`, copied from `CSL-0137`), and `UA = Q_mc/lmtd`.
- **Power chain** (TESPy sec_6, `Generator` / `Motor`, `eta` = 0.97):
  `P_gen = eta_gen·P_tu`, `P_mot = P_fp/eta_mot`, `P_grid = P_gen − P_mot`,
  and the plant efficiency `eta_el = P_grid/Q_sg`.
- **Part-load point** (TESPy sec_9–sec_11, `offdesign` with `design_path`):
  the mass flow `m_1_pl` is the only free specification; the turbine inlet
  pressure comes from **Stodola's cone law** (`Turbine.cone_func`, n = 1)

  ```
  m_1_pl = m_1 · (p_1_pl/p_1) · sqrt(p_1·v_1/(p_1_pl·v_1_pl)) · sqrt((1 − (p_2_pl/p_1_pl)²)/(1 − (p_2/p_1)²))
  ```

  (written in logarithmic form; `v` is the specific volume at the design inlet
  temperature, as in the source), the condenser `UA` and the cooling-water
  volumetric flow `V_dot_cw` keep their design values (`mc offdesign='UA'`,
  `c11 offdesign='v'`), the cooling-water return temperature is free
  (`c12 design='T'`) and the live steam pressure is free (`c1 design='p'`).
  The turbine isentropic efficiency is *not* a characteristic line here: the
  source applies only `offdesign=['cone']`, so `eta_s_tu` is unchanged.

| Inputs (design point) | Base value | Outputs (design point) | Value |
|---|---|---|---|
| `m_1` live steam mass flow | 10 kg/s | `Q_sg` steam generator duty | 33.69 MW |
| `T_1` / `p_1` live steam state | 600 °C / 150 bar | `Q_mc` condenser duty | 20.70 MW |
| `p_2` turbine outlet pressure | 0.1 bar | `P_tu` turbine power | 13.211 MW |
| `eta_s_tu` / `eta_s_fp` | 0.9 / 0.75 | `P_fp` pump power | 0.2236 MW |
| `pr_sg` steam generator | 0.9 | `eta_cycle` (P_tu − P_fp)/Q_sg | 38.55 % |
| `T_11`→`T_12`, `p_11` cooling water | 20→30 °C, 1.2 bar | `x_2` turbine outlet quality | 0.8655 |
| `eta_gen` / `eta_mot` | 0.97 / 0.97 | `P_grid` net power to the grid | 12.584 MW |
| `m_1_pl` part-load steam flow | 15 kg/s | `UA` design heat transfer coefficient | 1.015 MW/K |

## How to run

Open `rankine_cycle_part_load.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./rankine_cycle_part_load.eescode
```

The model needs the shipped `rankine_cycle_part_load.initials`: the part-load
point closes a 17-variable implicit block (condensing pressure and
cooling-water return temperature coupled through `UA` and the cone law) and
the solver starts with `SingularJacobian` without those guesses. The
tutorial's other specification sets are input swaps, verified during the task
in the work folder (see *Verification*):

- `p_2 = PRESSURE(fluid$,T=T_12+4,x=1)` instead of `p_2 = 0.1E5` — the
  `ttd_u = 4 K` specification of TESPy sec_4 (condensing pressure free);
- `P_grid = 10E6` instead of `m_1 = 10` — the net-power specification of
  TESPy sec_7 (steam mass flow free).

The efficiency/power studies of TESPy sec_8 (live steam temperature, cooling
water temperature and live steam pressure sweeps) and the part-load study of
sec_11 (`m_1_pl` from 20 to 10 kg/s) are CoolSolve parametric studies over
`m_1_pl`, `T_1`, `p_1`, `T_11`/`T_12` (GUI *Parametric* tab); the values of
the part-load study are tabulated below.

## Results

Design point (TESPy sec_3/sec_6 base case, `m_1` = 10 kg/s):

| Point | TESPy conn. | p [bar] | T [°C] | h [kJ/kg] | x [-] |
|---|---|---:|---:|---:|---:|
| 1 live steam | c1 | 150.00 | 600.00 | 3583.1 | – (superheated) |
| 2 turbine outlet | c2 | 0.100 | 45.81 | 2262.0 | 0.8655 |
| 3 condensate | c3 | 0.100 | 45.81 | 191.8 | 0 |
| 4 feed water | c4 | 166.67 | 47.71 | 214.2 | 0 |
| 11 cooling water in | c11 | 1.200 | 20.00 | 84.02 | 0 |
| 12 cooling water out | c12 | 1.176 | 30.00 | 125.84 | 0 |

`Q_sg = 33.690 MW`, `Q_mc = 20.702 MW`, `ṁ_cw = 495.12 kg/s`,
`V̇_cw = 0.4960 m³/s`, `P_tu = 13.211 MW`, `P_fp = 0.2236 MW`,
`eta_cycle = 38.55 %`, `eta_tu = 39.21 %`, `P_grid = 12.584 MW`,
`eta_el = 37.35 %`, `UA = 1.0148 MW/K`.

Part-load study (TESPy sec_11, design point of the table above, constant `UA`
and constant cooling-water volumetric flow):

| `m_1_pl` [kg/s] | `p_1_pl` [bar] | `p_2_pl` [bar] | `T_12_pl` [°C] | `Q_sg_pl` [MW] | `P_grid_pl` [MW] | `eta_el_pl` [%] |
|---:|---:|---:|---:|---:|---:|---:|
| 20.0 | 288.49 | 0.29564 | 38.90 | 62.53 | 22.66 | 36.24 |
| 17.5 | 254.91 | 0.23113 | 36.75 | 55.76 | 20.41 | 36.61 |
| 15.0 | 220.65 | 0.17790 | 34.55 | 48.70 | 17.99 | 36.94 |
| 12.5 | 185.68 | 0.13463 | 32.30 | 41.34 | 15.38 | 37.20 |
| 10.0 | 150.00 | 0.10000 | 30.00 | 33.69 | 12.58 | 37.35 |

The cone law returns the design point at `m_1_pl` = 10 kg/s, as it must.
At part load the condensing pressure rises strongly (the cooling water and
`UA` can no longer remove the heat at the design terminal temperature
differences) and the cone law pushes the live steam pressure up as well, so
the net power rises almost proportionally with the steam flow while the
electrical efficiency falls by about one point over the range.

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 live steam, 2 turbine outlet,
3 condensate, 4 feed water) give the design cycle on the P-h or T-s diagram
(CoolSolve *Diagram* tab, *Overlay array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle or
     parametric plot of eta_el_pl vs m_1_pl, figures/rankine_cycle_part_load_ts.png -->

## Verification

TESPy stores no numbers for this tutorial (`tests/test_basic_tutorials.py`
only executes the script), so the tutorial was re-run in a throw-away virtual
env (`work/partload/venv`, Python 3.12, TESPy installed from the local
snapshot at commit `19425523`, CoolProp 8.1.0) and every number below is a
direct TESPy output. The re-run script (`work/partload/rankine_run.py`) is the
tutorial file with the matplotlib/fluprodia blocks removed; the only physics
change is `c2.set_attr(design=['p'])` added to the sec_9 block, because the
base case of the model gives the turbine outlet pressure (`c2 p = 0.1 bar`)
instead of the `ttd_u = 4 K` of sec_4 — in TESPy a directly specified
pressure is not unset by `design=['p']` on `c1`, so it must be declared.
Comparison with `tools/compare_solution.py` (same CoolProp equation of state
on both sides):

1. **Design point** (base case, 22 common variables): maximum relative
   deviation **2.9e-12** (printed by `compare_solution.py`:
   `22 common variables, 0 differ (rtol=0.001)`), e.g. `P_tu` 13211041.4 W,
   `P_fp` 223585.2 W, `Q_sg` 33689672.9 W, `eta_cycle` 0.385503,
   `x_2` 0.865458, `ṁ_cw` 495.12 kg/s, `UA` 1014842.0 W/K — all equal to the
   TESPy values to round-off. The inventory note of `TSP-034` quotes
   `x_out = 0.866` from an independent CoolProp 7.2 check; TESPy (CoolProp
   8.1.0) and CoolSolve give 0.86546.
2. **Part-load point** at `m_1_pl` = 15 kg/s (13 common variables): maximum
   relative deviation **2.8e-11** (`13 common variables, 0 differ
   (rtol=0.001)`): `p_1_pl` 22064697.9 Pa, `p_2_pl` 17790.06 Pa,
   `T_12_pl` 34.5517 °C, `Q_sg_pl` 48696692.9 W, `P_grid_pl` 17988060.8 W,
   `eta_el_pl` 0.369390, `x_2_pl` 0.849572.
3. **Part-load sweep** (`m_1_pl` = 20, 17.5, 12.5 and 10 kg/s, re-solved in
   CoolSolve by editing `m_1_pl`): all tabulated quantities agree with the
   TESPy sweep to ≤ 1e-8 relative.
4. **Specification variants** (TESPy sec_4/sec_7, re-run in TESPy and
   re-solved in CoolSolve with the input swaps listed in *How to run*):
   - sec_4 (`ttd_u` = 4 K, `p_2` free, `m_1` = 10 kg/s): `p_2` 5325.06 Pa,
     `Q_sg` 34.1842 MW, `Q_mc` 20.5466 MW, `P_tu` 13.8602 MW, `P_fp` 0.22262 MW,
     `eta_cycle` 0.398944, `x_2` 0.848929, `ṁ_cw` 491.40 kg/s, `P_grid`
     13.2149 MW — equal to TESPy to round-off;
   - sec_7 (`P_grid` = 10 MW, steam mass flow free): `m_1` 7.5672 kg/s,
     `Q_sg` 25.8680 MW, `Q_mc` 15.5481 MW, `P_tu` 10.4883 MW,
     `P_fp` 0.16846 MW, `x_2` 0.848929, `ṁ_cw` 371.85 kg/s, `T_4` 35.769 °C —
     equal to TESPy to round-off.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the TESPy basic tutorial *Rankine Cycle*, file
`tutorial/basics/rankine.py`, commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff /
version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve; the iterative network solver
and the `design`/`offdesign` mode switches became two blocks of simultaneous
equations (the design point and one part-load point); the `PowerBus`/
`PowerConnection` plumbing became the equations `P_gen`, `P_mot`, `P_grid`;
units normalised to SI-°C-Pa-J (TESPy displays bar/°C/kJ/kg/kW/MW); TESPy's
sign convention (negative = energy produced) replaced by positive
magnitudes; the parametric loops are CoolSolve parametric studies.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in
Python", J. Open Source Softw. 5(49), 2178 (2020),
doi:10.21105/joss.02178.
Scientific basis: Stodola's cone law for the turbine off-design behaviour
(Stodola, *Dampfturbinen*, 1895, as implemented in
`tespy.components.turbomachinery.turbine.cone_func`) and the UA/ttd rating
of the condenser (`tespy.components.heat_exchangers.base`, `.condenser`),
with the smoothed LMTD of S. Quoilin, "Study of cooling and heat pump
systems", PhD thesis, University of Liege, 2011.

Source file (Python, comments in English), local snapshot of S. Quoilin:
`~/git/tespy/tutorial/basics/rankine.py`
(companion: `docs/basic_tutorials/rankine_cycle.rst`; test:
`tests/test_basic_tutorials.py`) (inventory candidate `TSP-034`).

## Conversion log

- **2026-10-14 — translation** (workflow `T-TRANSLATE`): the TESPy network
  (`CycleCloser`, `SimpleHeatExchanger`, `Condenser`, `Turbine`, `Pump`,
  `Source`, `Sink`, sec_6 `PowerBus`/`Generator`/`Motor`/`PowerSink`, 11
  connections) rewritten as simultaneous EES equations: the cycle closer
  disappears (`h_0 = h_1`, `p_0 = p_1`), the power bus becomes the three
  equations `P_gen = eta_gen·P_tu`, `P_mot = P_fp/eta_mot`,
  `P_grid = P_gen − P_mot`, and the components keep the source's attribute
  names (`pr`, `eta_s`, `pr1`, `pr2`, `ttd_u`, `v`, `cone`). Units already
  SI-like; only the display units change (bar → Pa, kJ/kg → J/kg, MW → W).
- **2026-10-14 — part-load point**: TESPy's `design`/`offdesign` keyword
  mechanism (which unsets specifications and takes reference values from a
  stored design state) has no EES equivalent; the design point and **one**
  part-load point (`m_1_pl`, default 15 kg/s, one point of the 20 → 10 kg/s
  sweep of sec_11) are written as two independent blocks of equations solved
  simultaneously, as `CSL-0135` does for the turbine. The reference point of
  the cone law, of `UA` and of the cooling-water volumetric flow is the design
  block of this file (the base case of the tutorial), **not** the 20 kg/s /
  `ttd_u` state of sec_10: the TESPy re-run was adapted to the same reference
  point (verification item 2), so both sides describe the same plant.
  The cone law is the logarithmic form used by `CSL-0135`.
- **2026-10-14 — condenser rating**: `LMTD_smoothed` copied from `CSL-0137`
  (block comment in the file); `UA = Q_mc/lmtd` is the design equation of
  TESPy's `HeatExchanger.UA_func`, `ttd_u = T_dew − T_12` the `ttd_u_func`.
- **2026-10-14 — diagram support**: block of 16 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`) added at the end of the model
  for the CoolSolve diagrams; the results of the model are unchanged.
- **Decision**: the model ships the design point and one part-load point; the
  `ttd_u` and net-power variants and the three parametric studies of sec_8
  are documented input swaps / CoolSolve parametric studies, not separate
  files (verified in the work folder).
- **Naming**: variable names are case-insensitive in EES and in CoolSolve, so
  the specific volumes `v_1`/`v_11` and the cooling-water volumetric flow are
  named `v_1`, `v_11`, `V_dot_cw` (a `V_11` collided with `v_11` and the
  solver reported an over-determined system).
- **Decision**: TESPy's sign convention (negative `P` for produced power,
  negative `Q` for rejected heat) is replaced by positive magnitudes, as in
  the other translations of this source.
- **Level**: taxonomy §3 score = equations 105 (1) + largest block 17 (1) +
  function present (1) + ≥ 3 coupled components (1) + off-design/part-load
  physics (1) + curated guesses needed (1) = **6 → level 3**.

## Limitations and CoolSolve gaps

- No CoolSolve gap encountered: the model uses only property calls, one
  `QUALITY` call, arithmetic and a `FUNCTION`; it solves in 6 iterations with
  the shipped `.initials`. No native/variant split is needed.
- `LMTD_smoothed` is copied from `CSL-0137` rather than included
  (`$INCLUDE library:CSL-0137`, workflow §4), so `tools/build_index.py`
  warns that the function name is defined in two models; this is the
  documented copy pattern, the definitions are identical.
- The model has **no subcooling** (the condensate sits on the bubble line,
  as in the tutorial's default `Condenser` setting) and **no pressure drop in
  the steam generator's cooling side** (the steam generator is adiabatic, as
  `SimpleHeatExchanger` with only `pr`).
- The turbine isentropic efficiency is kept at its design value in the
  part-load point because the source specifies `offdesign=['cone']` only; a
  characteristic line (`CSL-0135` ships the TESPy DEFAULT and Traupel lines)
  can be added for an efficiency characteristic.
- Constant volumetric flow of the cooling water is equivalent to a constant
  mass flow here, because the inlet temperature and pressure of `c11` are
  specifications of both the design and the off-design run; the equation is
  kept in the form of the source so that a future change of `T_11`/`p_11` in
  off-design behaves as in TESPy.
- The tutorial's matplotlib figures (`rankine_parametric.svg`,
  `rankine_partload.svg`, `rankine_ts_diagram.svg`) have no counterpart file
  in the library; the CoolSolve parametric plot is made in the GUI (figure
  step, workflow §7).

## Related models

- `CSL-0135` *turbine_stodola_offdesign*: the Stodola cone law and the
  efficiency characteristic of the same TESPy snapshot, as a standalone
  turbine component (this model needs only the cone law, at constant `eta_s`).
- `CSL-0137` *hx_lmtd_ua*: the TESPy `HeatExchanger` and `Condenser` classes
  of the same snapshot (UA/smoothed LMTD, ttd specifications, off-design
  characteristic lines); its `LMTD_smoothed` function is used in this model.
- `CSL-0004` *rankine_cycle_60mw*: a Rankine cycle of the same category with a
  cooling-water condenser, at 60 MW; this model adds the generator/motor
  power chain and the part-load behaviour.
- `CSL-0053` *steam_power_plant_elementary*: an elementary steam power plant
  as a teaching model (level 2), without off-design.
- `CSL-0013` *heat_pump_basic_tespy*: the pilot translation of the same
  source library (basic tutorial, TESPy `heat_pump.py`).