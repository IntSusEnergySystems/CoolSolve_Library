# Steam turbine with Stodola's cone law and efficiency characteristic

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0135`

Off-design model of a gas or steam turbine, translated from the TESPy
class `Turbine`. The design point (inlet state, mass flow and isentropic
efficiency given) supplies the reference values of Stodola's cone law; the
off-design point, defined by its mass flow, gets its inlet pressure from
the cone law and its isentropic efficiency from a characteristic line
`eta_s/eta_s,design = f(m/m_ref)` read from the lookup table shipped with
TESPy (the DEFAULT line and the Traupel (2001) line). Both points are
solved simultaneously in one model, as in the original example: the
`design` solution of TESPy is stored and read by the `offdesign` solve,
here the design point is simply computed together with the operating
point and hands over `M_dot_ref`, `P_in_ref`, `v_in_ref`, `pr_ref` and
`eta_s_des`.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Water (any fluid name known to CoolProp: the model is not steam-specific) |
| **Size** | 32 equations (largest block: 3), 12-point lookup table |
| **Source** | TESPy `src/tespy/components/turbomachinery/turbine.py` and `src/tespy/data/char_lines.json` ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`) |
| **Authors** | Francesco Witte (TESPy lead developer) and the TESPy contributors; the Traupel characteristic line is Traupel's (2001) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; verified against the TESPy example of the class docstring (see *Verification*) |

## Problem statement

A steam turbine expands 10 kg/s of superheated steam at 550 °C and 110 bar
to 0.5 bar at an isentropic efficiency of 0.9. It is then operated
part-load at 8 kg/s with the same inlet temperature and the same outlet
pressure: where does the inlet pressure settle, what is the isentropic
efficiency and what power does the machine deliver then?

This is the example of the docstring of the TESPy `Turbine` class
(inventory candidate `TSP-003`). In TESPy the machine is solved twice —
once with the isentropic efficiency given (`mode='design'`) and once
with the efficiency taken from a characteristic line and the inlet
pressure from Stodola's cone law (`mode='offdesign'`, `design_path` = the
stored design state).

## Model

Design point (`1_ref` → `2_ref`), all inputs except the outlet state:

- `h_in_ref = h(T_in_ref, P_in_ref)`, `s_in_ref = s(T_in_ref, P_in_ref)`
- `h_out_ref_s = h(s_in_ref, P_out_ref)` — isentropic outlet enthalpy
- `h_out_ref = h_in_ref − eta_s_des·(h_in_ref − h_out_ref_s)` — TESPy
  `eta_s_func`, `-(h_out - h_in) + (h_out,s - h_in)·eta_s = 0`
- `x_out_ref = quality(h_out_ref, P_out_ref)`,
  `P_dot_ref = M_dot_ref·(h_in_ref − h_out_ref)`,
  `v_in_ref = volume(h_in_ref, P_in_ref)`, `pr_ref = P_out_ref/P_in_ref`
  (the `pr.design` of TESPy's cone law)

Off-design point (`1` → `2`), mass flow `M_dot` given, `T_in` and `P_out`
taken from the design point (as in the original example, where only the
mass flow is changed):

- `h_in = h(T_in, P_in)`, `s_in = s(T_in, P_in)`, `v_in = volume(h_in, P_in)`
- `h_out_s = h(s_in, P_out)` — isentropic outlet enthalpy
- characteristic line, TESPy `eta_s_char` with parameter `m`:
  `f_eta_s = f(x_char)` with `x_char = M_dot/M_dot_ref`,
  `eta_s = eta_s_des·f_eta_s`
- `h_out = h_in − eta_s·(h_in − h_out_s)` — TESPy `eta_s_char_func`
- `x_out = quality(h_out, P_out)`, `P_dot = M_dot·(h_in − h_out)`

**Stodola's cone law** (TESPy `cone_func`, exponent `(n+1)/n = 2` for
`n = 1`), written here in logarithmic form:

```
ln(M_dot/M_dot_ref) = ln(P_in/P_in_ref)
                   + 0.5·ln(P_in_ref·v_in_ref/(P_in·v_in))
                   + 0.5·ln(|(1 − (P_out/P_in)²)/(1 − pr_ref²)|)
```

which is TESPy's residual divided by `M_dot_ref` and logged; the log form
is the same relation with a better-scaled residual (the model converges in
9 Newton iterations without guesses, the direct form diverges to a
non-physical root, see *Conversion log*).

**Characteristic line** (`turbine_stodola_offdesign-char_lines.csv`,
12 points, columns `m_ref_ratio`, `eta_s_ratio` for the TESPy DEFAULT line
and `m_ref_ratio_trau`, `eta_s_ratio_trau` for the Traupel line):

| `m/m_ref` | 0.0 | 0.3 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 | 1.1 | 1.2 | 1.3 | 1.4 | 1.5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DEFAULT `eta_s/eta_s,des` | 0.95 | 0.98 | 0.993 | 0.996 | 0.998 | 0.9995 | 1.0 | 0.999 | 0.996 | 0.99 | 0.98 | 0.96 |
| Traupel `eta_s/eta_s,des` | 0.0 | 0.3975 | 0.6772 | 0.8581 | 0.9593 | 0.9985 | 1.0 | 0.9875 | 0.9357 | 0.8464 | 0.7219 | 0.5643 |

Both lines are read in the main program (the DEFAULT line feeds the
model, the Traupel line is evaluated at the same point as a reference,
`eta_s_traupel`). The table is the TESPy file
`src/tespy/data/char_lines.json`, section `Turbine/eta_s_char`.

| Inputs | Value (original) | Outputs | Value |
|---|---|---|---|
| `M_dot_ref` design flow | 10 kg/s (36 t/h) | `P_dot_ref` design power | 10.453 MW |
| `T_in_ref` | 550 °C | `x_out_ref` design outlet quality | 0.9138 |
| `P_in_ref` | 110 bar | `P_in` off-design inlet pressure | 88.646 bar |
| `P_out_ref` | 0.5 bar | `eta_s` off-design isentropic efficiency | 0.8982 |
| `eta_s_des` | 0.9 | `P_dot` off-design power | 8.195 MW |
| `M_dot` off-design flow | 8 kg/s (28.8 t/h) | `x_out` off-design outlet quality | 0.9322 |

## How to run

Open `turbine_stodola_offdesign.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./turbine_stodola_offdesign.eescode
```

No `.initials` and no `coolsolve.conf` are needed: 28 of the 30 equations
are explicit and the three-equation cone-law block converges from the
default guesses. The part-load study of a machine (`M_dot` from 0.8 to 1.5
times its design flow, with the characteristic line read from the table) is
a CoolSolve parametric sweep of `M_dot`; `P_in`, `eta_s` and `P_dot` are
the results to plot.

## Results

Base case, TESPy example (design point and off-design point at 28.8 t/h):

| Point | p [bar] | T [°C] | h [kJ/kg] | v [m³/kg] | x [-] |
|---|---:|---:|---:|---:|---:|
| 1_ref design inlet | 110.000 | 550.00 | 3491.86 | 0.032191 | 1 (superheated) |
| 2_ref design outlet | 0.500 | 81.32 (sat.) | 2446.60 | — | 0.9138 |
| 1 off-design inlet | 88.646 | 550.00 | 3513.29 | 0.040531 | 1 (superheated) |
| 2 off-design outlet | 0.500 | 81.32 (sat.) | 2488.95 | — | 0.9322 |

Design power `P_dot_ref` = 10.453 MW (`eta_s` = 0.9 by construction), the
off-design point settles at `P_in` = 88.646 bar with
`eta_s` = 0.8982 (`f_eta_s` = 0.998 on the DEFAULT line, 0.9671 on the
Traupel line, i.e. `eta_s_traupel` = 0.8704) and delivers
`P_dot` = 8.195 MW.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): part-load study of the
     turbine (P_in and P_dot vs mass flow), figures/turbine_stodola_offdesign_partload.png -->

## Verification

The reference is the example of the docstring of the TESPy class
(`turbine.py`, commit `19425523`), re-run in a throw-away virtual
environment (`work/turbine_stodola/`, deleted at the end of the task):

```bash
python3 -m venv work/turbine_stodola/venv
work/turbine_stodola/venv/bin/pip install ~/git/tespy     # tespy 0.11.3.dev0, CoolProp 8.0.0
```

The script `run_ref2.py` repeats the docstring example (`Source`,
`Sink`, `Turbine`, two `Connection`s; `t.set_attr(eta_s=0.9,
design=['eta_s'], offdesign=['eta_s_char', 'cone'])`,
`inc.set_attr(fluid={'water': 1}, m=36, T=550, p=110, design=['p'])`,
`outg.set_attr(p=0.5)`, `nw.solve('design')`, then
`inc.set_attr(m=28.8)`, `nw.solve('offdesign', design_path=design_state)`)
and writes the quantities of both solves to `tespy_reference.csv`. It reproduces the numbers stored in the
docstring: `round(P, 0) = -10452574`, `round(x, 3) = 0.914` for the design
point, then `round(eta_s, 3) = 0.898` and `round(p_in, 1) = 88.6` bar for
the off-design point at `m = 28.8` t/h. The script also writes the
design-point and off-design quantities of the two solves to
`tespy_reference.csv`, compared with the CoolSolve `.sol` by
`tools/compare_solution.py` (no unit conversion: both sides are SI).

```
$ python3 /…/CoolSolve/tools/compare_solution.py turbine_stodola_offdesign.sol tespy_reference_h.csv
| Variable | EES | CoolSolve | rel. diff | |
|---|---:|---:|---:|---|
16 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 16
```

Maximum relative deviation **3.71e-05** over the 16 common variables
(`--rtol 1e-9 --all` run): the design point, which is the verification
target of the docstring, agrees to 1.1e-10 (`P_dot_ref` 10452573.75 W,
`x_out_ref` 0.9138224, `pr_ref` 0.0045455); at the off-design point the
deviations are `v_in` 3.71e-05, `P_in` 3.48e-05, `P_dot` 3.20e-06,
`x_out` 2.95e-06, `s_in` 2.77e-06, `h_in` 8.72e-07 — they come from the
CoolProp version of the two runs (8.0.0 in the reference environment,
8.1.0dev in the CoolSolve build `0.3.0@4c80b25`), which is below the
property tolerance of CoolSolve `docs/ees_import.md` §11. `eta_s` = 0.8982
and `f_eta_s` = 0.998 are exact (a table value).

The two outlet temperatures are not compared: both points end in the
two-phase region, where TESPy's own `Connection.T` reports 354.4669 °C
(non-physical for a state at 0.5 bar with `x` = 0.914, an extrapolation
of the superheated side) whereas the CoolProp flash on `(P, h)` returns the
saturation temperature of the outlet, 81.32 °C, which the model reports as
`T_out_ref` / `T_out`.

Not compared: the connection specific volume printed by TESPy
(`Connection.v.val_SI` = 0.3219 m³/kg at the design point, ten times the
specific volume, and not the value its own cone law uses — the cone law
uses `Connection.calc_vol`, which gives 0.032191 m³/kg). The comparison
uses the `calc_vol` values, i.e. the ones entering the cone law.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the TESPy class `Turbine`, files
`src/tespy/components/turbomachinery/turbine.py` and
`src/tespy/data/char_lines.json`, commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff / version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve; the network, the connections,
the `Source`/`Sink` connectors and the `design`/`offdesign` solve modes
replaced by simultaneous equations (design point and off-design point in
one model); the cone-law residual written in logarithmic form; units
normalised to SI-°C-Pa-J (TESPy displays bar/degC/kJ/kg/t/h); the
characteristic lines shipped as the lookup-table companion
`turbine_stodola_offdesign-char_lines.csv`; the power reported as a
positive output (TESPy's `PowerConnection` carries `P = -m(h_out - h_in)`).
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems
in Python", J. Open Source Softw. 5(49), 2178 (2020),
doi:10.21105/joss.02178.
Scientific basis: Stodola's cone law for turbomachinery (A. Stodola,
*Die Dampfturbinen*, 1895) as implemented by TESPy (`Turbine.cone_func`,
same docstring); the DEFAULT efficiency characteristic of
`data/char_lines.json` and the Traupel characteristic line, A. Traupel,
"Leistungsverhalten von Dampfturbinen großer Leistung", VDI-Zeitschrift
113 (2001) — the reference is named by TESPy in the `"ref": "Traupel2001"`
field of the line.

Source file (Python, comments in English), local snapshot of S. Quoilin:
`~/git/tespy/src/tespy/components/turbomachinery/turbine.py`
(companion: `~/git/tespy/src/tespy/data/char_lines.json`; the tool
mechanics are in `~/git/tespy/src/tespy/tools/characteristics.py`;
inventory candidate `TSP-003`).

## Conversion log

- **2026-10-13 — translation** (workflow `T-TRANSLATE`): the TESPy network
  (2 connections, 1 `Turbine` with a `PowerConnection`) rewritten as 30
  simultaneous EES equations. The `Source`/`Sink` connectors and the
  `power` connector disappear (no state, no equation): the energy balance
  `0 = E + m(h_out - h_in)` becomes `P_dot = M_dot*(h_in - h_out)`,
  positive as the power *produced*. The two solve modes become two sets of
  state variables in the same model (`_ref` suffix = design state), the
  `design_path` dictionary becoming the five design constants the cone law
  needs (`M_dot_ref`, `P_in_ref`, `v_in_ref`, `pr_ref`, `eta_s_des`), all
  of them computed by the design-point equations of the same file.
- **2026-10-13 — cone-law residual**: TESPy's residual
  `0 = m_ref·(p_in/p_ref)·sqrt(p_ref·v_ref/(p_in·v_in))·sqrt(|(1−(p_out/p_in)²)/(1−pr_ref²)|) − m_in`
  is the same relation written as `ln(m_in/m_ref) − … = 0`. The direct
  form made CoolSolve's Newton solver converge to a non-physical root
  (`P_in` = 2.19e12 Pa, `*Solution Verification Failed*`); the log form
  solves in 9 iterations from the default guesses. The model equation is
  unchanged (`|m_in/m_ref| > 0` here, so the log is defined).
- **2026-10-13 — characteristic line in the main program**: the
  correlation is a `FUNCTION` in TESPy (`CharLine.evaluate`). Written as
  an EES `FUNCTION` it does not evaluate in this CoolSolve build (the
  registered gap `CS-GAP-LOOKUP-PROC`, lookup tables inside
  `FUNCTION`/`PROCEDURE` bodies, fixed after v0.3.0), so the two
  `INTERPOLATE` calls are written in the main program; the table, the
  columns and the values are unchanged. No `_coolsolve` variant: the file
  is valid EES in both tools.
- **2026-10-13 — units**: TESPy sets its display units on the `Network`
  (`bar`, `degC`, `kJ/kg`, `t/h`); only the values written in the model
  change: 36 t/h → `M_dot_ref` = 10 kg/s, 28.8 t/h → `M_dot` = 8 kg/s,
  110 bar → `P_in_ref` = 110E5 Pa, 0.5 bar → `P_out_ref` = 0.5E5 Pa
  (the original values are given in the comments).
- **Level**: score of `docs/taxonomy.md` §3 = 1 (32 equations < 50 → 0;
  largest block 3 ≤ 5 → 0; no function/procedure/array → 0; off-design
  physics → 1; no curated guesses → 0) → level 1, raised by one to
  level 2 because the model is a machine characteristic read from a data
  table (the level-1 models of the library have no data tables and no
  off-design coupling).

## Limitations and CoolSolve gaps

- No gap blocks the model: `missing_features` is empty and the status is
  `verified`. Two registered IDs of the CoolSolve gap register are
  referenced here (not re-reported):
  - `CS-GAP-LOOKUP-PROC` (lookup tables inside `FUNCTION`/`PROCEDURE`
    bodies) is why the characteristic line is read in the main program;
  - `CS-GAP-INTERP-EXTRAP`: outside the table, CoolSolve returns the end
    values; TESPy's `CharLine` with its default `extrapolate=False` does
    the same, so the two agree there. The shipped table covers
    `m/m_ref` from 0 to 1.5 (DEFAULT line) and 0 to 1.9 (Traupel line);
    the DEFAULT line is the one the original example uses.
- Modelling scope: the cone law couples the *inlet* pressure to the mass
  flow; with `T_in` and `P_out` fixed (as in the original example) it is a
  closed system. For a real machine the inlet pressure is not free (a
  turbine works on a fixed boiler pressure) — the part-load question is
  then how much flow the machine passes at that pressure, i.e. the cone
  law inverted. The model is written in the direction of the original.
- The cone law is a similarity law: it assumes unchanged blade geometry and
  a negligible change of the Euler work coefficient, as in TESPy.
- `v_in` is reported by CoolSolve with the unit label `kg/m^3` although it
  is a specific volume in m³/kg (registered bug `CS-BUG-UNIT-VOLUME`).

## Related models

- `CSL-0037` (*scroll_expander_semi_empirical*, same category): a
  volumetric expander with a built-in leakage model; its design/off-design
  results come from the machine geometry instead of a cone law.
- `CSL-0013` (*heat_pump_basic_tespy*): the other translation of the same
  TESPy snapshot; the same `eta_s` relation, with the compressor.
- `CSL-0136` (*polynomial_compressor_en12900*): the off-design compressor of
  the same TESPy snapshot (EN 12900 efficiency-map polynomials instead of a
  characteristic line), the counterpart of this cone-law turbine.

- `CSL-0140` *rankine_cycle_part_load*: a Rankine cycle of the same TESPy
  snapshot that uses this cone law for its part-load point (turbine inlet
  pressure of the off-design point, at constant isentropic efficiency).
- `CSL-0141` *gas_turbine_open_cycle*: the gas-turbine tutorial of the
  same TESPy snapshot, which uses the `eta_s` design relation of this
  turbine (without the off-design cone law).
- `CSL-0147` *segs_solar_power_plant*: 7-stage steam turbine train at the design point (fixed
  stage efficiencies), the plant this off-design turbine model could close in part load.
