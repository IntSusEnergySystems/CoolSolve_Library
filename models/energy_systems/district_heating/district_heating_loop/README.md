# District heating loop (consumer, feed pump, pipes with pressure drop and heat loss)

🟠 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0142`

Translation of the TESPy basic tutorial *District Heating Network*: a small
district-heating loop of a heating plant (heat source without pressure drop),
a feed pump with isentropic efficiency, a consumer (a heat exchanger with a
2 % pressure drop and a given heat demand), a control valve and two pipes
(feed and return) that lose heat to the ambient and drop pressure by pipe
friction (Darcy-Weisbach with the Colebrook-White friction factor). The model
returns the mass flow, the pump power, the heat duties, the state points and
the loop efficiency, and it reproduces the tutorial's part-load studies of the
ambient temperature, of the consumer heat load and of the heating temperature
level.

| | |
|---|---|
| **Category** | Energy systems › District heating |
| **Fluids** | Water (liquid; TESPy uses the incompressible back end `INCOMP::Water`) |
| **Size** | 71 equations (largest block: 10) |
| **Source** | TESPy tutorial `tutorial/basics/district_heating.py` ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`), companion docs `docs/basic_tutorials/district_heating.rst` |
| **Authors** | Francesco Witte (TESPy lead developer) and the TESPy contributors |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; verified against the TESPy tutorial re-run and its loop energy balance (see *Verification*) |

## Problem statement

A district heating loop delivers hot water at 90 °C and 10 bar from a central
heating plant to a consumer that needs 10 kW and returns the water at 65 °C.
A feed pump raises the pressure to 13 bar; the consumer has a 2 % pressure
drop; a control valve drops the residual pressure. The feed and the return
pipe are 100 m long, their roughness is 0.5 mm and they are sized for a 2 %
pressure loss (diameters 17.75 mm and 18.55 m), and their heat loss to an
ambient at 0 °C corresponds to UA values of 2.786 W/K and 3.086 W/K.
Determine the mass flow, the pump power, the heat duties and the state points,
and study the loop efficiency and the heat losses when the ambient
temperature, the consumer heat load or the temperature level changes.

## Model

State points are the six TESPy connections 1…6 of the loop
(connection 6 = the return pipe outlet = connection 0, the heat source inlet,
identified by the cycle closer; the translation writes the loop once, so
connection 0 is not repeated).

| Component (TESPy class) | Equations |
|---|---|
| Heat source (`SimpleHeatExchanger`, `pr` = 1) | `p[6] = p[1]` |
| Feed pump (`Pump`, `eta_s`) | `η_s·(h₂ − h₁) = h(p₂, s₁) − h₁`, pump outlet pressure `p₂` given |
| Feed pipe (`Pipe`, `UA_group`, `darcy_group`) | `ṁ·(h₃ − h₂) = −UA_feed·ΔT_log(T₂, T₃, T_amb)`, Darcy-Weisbach pressure drop with `Re = 4ṁ/(π·D·(μ₂+μ₃)/2)` and the Colebrook-White friction factor |
| Consumer (`SimpleHeatExchanger`, `Q`, `pr`) | `Q̇_cons = ṁ·(h₄ − h₃)`, `p₄ = pr_cons·p₃` |
| Control valve (`Valve`) | `h₅ = h₄` (isenthalpic; its pressure drop is a result) |
| Return pipe (`Pipe`) | same two equations as the feed pipe, with its own `D`, `UA` |

Fluid properties of the six states come from the EES property calls
(`h = ENTHALPY(fluid$, T, P)`, `v = VOLUME(...)`, `μ = VISCOSITY(...)`), so
the model is a closed algebraic system of 71 equations, 53 of them explicit
and the largest implicit block of size 10 (a pipe: energy balance, Reynolds
number, friction factor and pressure drop together with the state properties).

The friction factor uses the EES built-in procedure `Colebrook(Re, RR, f)`,
i.e. the Colebrook-White equation in implicit form, the same equation TESPy
solves in `darcy_friction_factor`
(`src/tespy/tools/fluid_properties/helpers.py`, commit `19425523`, reference
Nirschl 2018 in the TESPy docs). The log-mean temperature difference against
the ambient is the `FUNCTION lmtd_ambient` of the file.

| Inputs | Base value | Outputs (base case) | Value |
|---|---|---|---|
| `T[1]` feed temperature | 90 °C | `m_dot` mass flow | 0.09758 kg/s |
| `p[1]` / `p[2]` pressure (10 / 13 bar) | 1.0 / 1.3 MPa | `W_pump` pump power | 40.41 W |
| `eta_s` pump efficiency | 0.75 | `Q_hs` heat source duty | 10.410 kW |
| `Q_cons` consumer heat demand | −10 kW | `Q_pipes` heat loss of the two pipes | −450.0 W |
| `pr_cons` consumer pressure ratio | 0.98 | `dp_valve` valve pressure drop | 2.283 bar |
| `T[4]` return temperature | 65 °C | `eta` loop efficiency | 95.694 % |
| `L`, `ks` pipe length and roughness | 100 m, 0.5 mm | `Q_bal` energy balance residual | −3.4e−9 W |
| `D_feed` / `D_return` pipe diameters | 17.75 / 18.55 mm | | |
| `UA_feed` / `UA_return` pipe heat transfer coefficients | 2.786 / 3.086 W/K | | |
| `T_amb` ambient temperature | 0 °C | | |

## How to run

Open `district_heating_loop.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./district_heating_loop.eescode
```

The system has implicit blocks of size 10 (pipe energy balance, friction
factor and pressure drop) and does **not** converge from the default guesses;
the `.initials` file of the model holds the TESPy state of the base case and
is required (the GUI uses it automatically, the command line picks up the
file of the same stem).

The three part-load studies of the tutorial are obtained by editing the
inputs: `T_amb` (−10…20 °C), `Q_cons` (−12…−3 kW) and both temperature
levels `T[1]` and `T[4]` (keeping `T[1] − T[4] = 20 K`); in the GUI they are
parametric sweeps (*Parametric* tab). A faster first convergence for a far
from the base case is obtained by shifting the temperatures of the `.initials`
file as well.

## Results

Base case (TESPy tutorial sec_4/sec_5, `INCOMP::Water` there):

| Point | TESPy connection | p [bar] | T [°C] | h [kJ/kg] |
|---|---|---:|---:|---:|
| 1 heat source outlet = pump inlet | c1 | 10.000 | 90.00 | 292.93 |
| 2 pump outlet | c2 | 13.000 | 90.04 | 293.35 |
| 3 consumer inlet (feed pipe outlet) | c3 | 12.741 | 89.44 | 290.79 |
| 4 consumer outlet | c4 | 12.486 | 65.00 | 188.69 |
| 5 valve outlet | c5 | 10.203 | 65.05 | 188.69 |
| 6 return pipe outlet = heat source inlet | c6 = c0 | 10.000 | 64.56 | 186.64 |

`ṁ = 0.097936 kg/s`, `Ẇ_pump = 40.46 W`, `Q̇_hs = 10.410 kW`,
`Q̇_feed = −250 W`, `Q̇_return = −200 W`, `Δp_valve = 2.281 bar`,
`η = 95.694 %`.

The pipe diameters and UA values are results of the tutorial's design step
(sec_3: 2 % pressure loss with `L` = 100 m and `k_s` = 0.5 mm →
`D_feed` = 17.749 mm, `D_return` = 18.551 mm; sec_4: given heat losses at
`T_amb` = 0 °C → `UA_feed` = 2.786 W/K, `UA_return` = 3.086 W/K). They are
inputs of this model, which computes the operating point of the loop with
them (the tutorial's sec_4/sec_5 configuration).

Part-load studies (TESPy reference values, reproduced point-wise in CoolSolve
by editing the inputs — see *Verification*):

| `T_amb` [°C] | η [%] | `Q̇_pipes` [W] | | `Q̇_cons` [kW] | η [%] | `Q̇_pipes` [W] | | `T[1]` [°C] | η [%] | `Q̇_pipes` [W] |
|---:|---:|---:|---|---:|---:|---:|---|---:|---:|---:|
| −10 | 95.161 | 508.5 | | 3 | 87.043 | 446.6 | | 90 | 95.550 | 465.7 |
| 0 | 95.694 | 450.0 | | 10 | 95.694 | 450.0 | | 80 | 96.088 | 407.1 |
| 20 | 96.778 | 333.0 | | 12 | 96.384 | 450.3 | | 60 | 97.182 | 290.0 |

Efficiency and heat loss of the loop are reproduced to 3.6e-07 and 2.8e-06
relative (see *Verification*); the mass flow is 0.4 % lower than TESPy's,
because the two tools use different liquid-water properties (see below).

The arrays `h_dia[i]`, `P_dia[i]`, `T_dia[i]`, `s_dia[i]`
(i = 1 heat source outlet, 2 consumer inlet, 3 consumer outlet, 4 heat source
inlet) give the loop on a P-h or T-s diagram (CoolSolve *Diagram* tab,
*Overlay array path*, *Close loop*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve -->

## Verification

TESPy stores no numbers for this tutorial (`tests/test_basic_tutorials.py`
only executes the script), so the tutorial itself was re-run in a throw-away
virtual environment (Python 3.12, TESPy installed from the local snapshot at
commit `19425523`, CoolProp 8.0.0) and every value below is a direct TESPy
output. Comparison with `CoolSolve/tools/compare_solution.py` on the 20
common variables (the reference CSV is written by the script of the
verification, kept in the work folder of the task):

```
20 common variables, 0 differ (rtol=0.01); only in EES: 0; only in CoolSolve: 52
```

| Variable | TESPy | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `m_dot` [kg/s] | 0.097936 | 0.0975789 | **3.65e-03** |
| `W_pump` [W] | 40.4556 | 40.4144 | 1.02e-03 |
| `dp_valve` [Pa] | 228112 | 228289 | 7.76e-04 |
| `eta` | 0.956938 | 0.956938 | 6.97e-08 |
| `Q_hs` [W] | 10409.5 | 10409.6 | 3.89e-06 |
| `Q_feed` [W] | −250 | −250.001 | 5.76e-06 |
| `Q_return` [W] | −200 | −199.998 | 1.08e-05 |
| `p[3]`, `p[4]`, `p[5]` [Pa] | — | — | ≤ 8.3e-05 |
| `T[2]`, `T[3]`, `T[5]`, `T[6]` [°C] | — | — | ≤ 1.3e-05 |

**Maximum relative deviation 3.65e-03** (`m_dot`), as printed by
`compare_solution.py` (the quoted table lists the variables above the printed
threshold; `--all --rtol 0.01` prints the 20 lines). Two deviations are
explained by the fluid properties, not by the equations:

- **Fluid back end.** TESPy runs the loop on CoolProp's incompressible back
  end `INCOMP::Water` (`ρ` = 968.3 kg/m³ and `c_p` = 4189 J/kg/K at 90 °C);
  the EES fluid name for liquid water is the real fluid `Water`
  (`ρ` = 965.7 kg/m³, `c_p` = 4203 J/kg/K at the same state). The mass flow
  follows from the consumer duty `Q̇ = ṁ·(h₃ − h₄)` and therefore shifts by
  the difference of the enthalpy differences (−0.36 %), and the pump power,
  which is `ṁ·(h₂ − h₁)` at a 3 bar pressure rise, by −0.10 %.
- **Absolute enthalpies** (`h[i]`, not compared) carry a reference-state
  offset: TESPy's incompressible water has `h = 0` at 0 K, CoolProp's `Water`
  uses the IIR reference state (`h` = 200 kJ/kg at 0 °C). The enthalpy
  *differences*, which drive every result, are compared through the duties.

The energy balance of the loop closes in both tools
(`Q̇_hs + Ẇ_pump = −(Q̇_cons + Q̇_feed + Q̇_return) = 10 450 W`); the model
reports the residual as `Q_bal = −3.4e−9 W`.

The three part-load studies of sec_5 were re-solved by editing the inputs of
the CoolSolve model (two points per sweep: the end points of
`T_amb` ∈ [−10, 20] °C, of `Q̇_cons` ∈ [3, 12] kW and of the temperature level
∈ [90, 60] °C):

| sweep | point | TESPy `ṁ` / CoolSolve `ṁ` [kg/s] | TESPy η / CoolSolve η [%] | TESPy `Q̇_pipes` / CoolSolve [W] |
|---|---:|---:|---:|---:|
| `T_amb` | −10 °C | 0.0982012 / 0.0978431 | 95.16092 / 95.16093 | 508.5 / 508.5 |
| `T_amb` | 20 °C | 0.0974056 / 0.0970504 | 96.77757 / 96.77758 | 333.0 / 333.0 |
| `Q̇_cons` | 3 kW | 0.0310411 / 0.0309278 | 87.04290 / 87.04293 | 446.6 / 446.6 |
| `Q̇_cons` | 12 kW | 0.117037 / 0.116610 | 96.38357 / 96.38357 | 450.3 / 450.3 |
| `T[1]` | 85 °C | 0.122229 / 0.121790 | 95.81834 / 95.81834 | 436.4 / 436.4 |
| `T[1]` | 60 °C | 0.121649 / 0.121338 | 97.18150 / 97.18149 | 290.0 / 290.0 |

Worst relative deviation over these points: **3.65e-03** (mass flow, same
cause as above); efficiency agrees to 3.6e-07 and the pipe heat loss to
2.8e-06.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the TESPy basic tutorial *District Heating Network*,
file `tutorial/basics/district_heating.py`, commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff / version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve; iterative network solver
replaced by simultaneous equations; the incompressible water `INCOMP::Water`
replaced by the real EES fluid `Water`; units normalised to SI-°C-Pa-J
(TESPy displays bar/°C/kJ/kg/kW); the pipe design step (sec_2–sec_4) is not
re-implemented, its results are inputs; parametric loops documented as
CoolSolve parametric studies.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in Python",
J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
Scientific basis: the tutorial itself; the friction factor is the
Colebrook-White equation (Colebrook 1939; as in TESPy
`darcy_friction_factor`, reference Nirschl 2018) and the heat loss of a pipe
is the usual `UA·ΔT_log` model (as in TESPy `SimpleHeatExchanger.UA_group`).

Source file (Python, comments in English), local snapshot of S. Quoilin:
`~/git/tespy/tutorial/basics/district_heating.py`
(companion: `docs/basic_tutorials/district_heating.rst`; test:
`tests/test_basic_tutorials.py`) (inventory candidate `TSP-037`).

## Conversion log

- **2026-10-14 — translation** (workflow `T-TRANSLATE`): the TESPy network
  (`CycleCloser`, 2 × `SimpleHeatExchanger`, `Pump`, `Valve`, 2 × `Pipe`, 7
  connections) rewritten as simultaneous EES equations. The cycle closer
  disappears (state 6 = state 1 of the heating plant, `p[6] = p[1]`), the
  valve is the single equation `h[5] = h[4]` (its pressure drop is a result,
  as in TESPy), the pump is `(h₂ − h₁)·η_s = h(p₂, s₁) − h₁`, and the pipes
  keep TESPy's two equations each (`UA_group` and `darcy_group`). The
  Darcy friction factor comes from the EES built-in `Colebrook` instead of
  TESPy's piecewise `darcy_friction_factor`; the only branch TESPy uses at
  these Reynolds numbers (Re ≈ 1.5e4–2.2e4, `Re·k_s/D` > 65) is the
  Colebrook-White equation, which `Colebrook` solves. TESPy's numerical
  smoothing of the log-mean temperature difference (`smoothed_lmtd`,
  Quoilin 2011) is dropped: it is a regularisation near a temperature
  inversion, which the states of this loop never reach (ΔT ≥ 64 K).
- **2026-10-14 — fluid and units**: `INCOMP::Water` → `Water` (the EES name
  of liquid water; the incompressible back end is not an EES fluid); bar →
  Pa (10 bar → `p[1] = 10E5`, 13 bar → `p[2] = 13E5`), kJ/kg → J/kg, kW → W.
  Sign convention kept: `Q_cons = −10 kW` is heat delivered to the consumer.
- **2026-10-14 — design step as inputs**: the tutorial's sec_2–sec_4 (sizing
  the diameters from a 2 % pressure loss, then the UA values from the given
  heat losses) is a *design* calculation; this model ships the operating
  point (tutorial sec_5), the design results being inputs (`D_feed`,
  `D_return`, `UA_feed`, `UA_return`). Their values are TESPy outputs and are
  listed in *Results*.
- **2026-10-14 — initial values**: `.initials` with the TESPy state of the
  base case; the implicit blocks of size 10 do not converge from the default
  guesses (CoolSolve *SingularJacobian* / *MaxIterations*, see
  CoolSolve `docs/debugging_models.md`).
- **2026-10-14 — diagram support**: block of 16 post-processing equations
  (arrays `h_dia[i]`, `P_dia[i]`, `T_dia[i]`, `s_dia[i]`, i = 1…4) added at
  the end of the model; the results of the model are unchanged.
- **Level**: score 5 of `docs/taxonomy.md` §3 — equations 71 (1), largest
  block 10 (1), functions and `DUPLICATE` present (1), six coupled
  components (1), no off-design/calibration (0), curated guesses needed (1) —
  gives level 3; moved down by one because the physics is the tutorial's
  (no off-design, no parameter identification) → **level 2**.

## Limitations and CoolSolve gaps

- No CoolSolve gap: the model uses property calls, arithmetic, one `FUNCTION`
  and the built-in `CALL Colebrook`. It needs its `.initials` (documented
  above), not a CoolSolve feature.
- The friction factor of a laminar or hydraulically smooth flow is not
  covered: the EES `Colebrook` procedure solves the turbulent Colebrook-White
  equation only (TESPy switches branches at Re ≤ 2320).
- The pipes are modelled as single nodes with their mean specific volume and
  mean viscosity, as in TESPy's `darcy_group`; no axial discretisation and no
  pressure drop from bends or fittings.
- TESPy's sign convention for the pipe heat loss (`Q` negative) is kept.

## Related models

- `CSL-0013` *heat_pump_basic_tespy*: the other TESPy-tutorial translation of
  this series (same source, same translation style).
- `CSL-0018` *pipe_pressure_drop_colebrook*: pipe pressure drop with the
  same Colebrook-White friction factor (EES built-in `Colebrook`).
- `CSL-0130` *pipe_pressure_drop_correlations*: function library of Darcy
  friction factors and straight-pipe pressure drops (alternative closures for
  the two pipe equations).
- `CSL-0137` *hx_lmtd_ua*: TESPy heat exchanger rated by `UA` and a
  (smoothed) log-mean temperature difference, the same heat-loss closure as
  the pipes of this model.
