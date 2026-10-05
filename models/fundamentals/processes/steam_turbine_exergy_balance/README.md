# Steam turbine exergy balance

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0045`

A short second-law (exergy) exercise on a steam turbine: with the two inlet /
outlet states and the heat loss to the ambient given, the model computes the
actual power delivered by the turbine, the maximum (reversible) power, the
second-law efficiency, the exergy destruction rate and the specific flow exergy
at the turbine inlet. It is a good starting point to compare the first-law and
the exergy balances of an open system, and to see the sign conventions of the
two.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water (real fluid: superheated steam in the turbine, liquid water at the ambient state) |
| **Size** | 33 equations, all explicit (largest block: 1): 21 for the model, 12 for the diagram state points |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition session 10, exercise 2 (EES file `R10_E02_2022.EES`, session 2022-2023) |
| **Authors** | TBD (ULiège, course *Thermodynamique appliquée*; the companion course files name S. Quoilin and the repetition assistants N. Paulus and B. Dechesne) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

Steam enters a turbine at 3 MPa and 450 °C with a mass flow rate of 8 kg/s. At
the outlet the conditions are 0.2 MPa and 150 °C. The steam loses 300 kW of
heat to the ambient, which is at 100 kPa and 25 °C. The changes of potential and
kinetic energy are neglected. Determine:

1. the actual power delivered by the turbine;
2. the maximum possible power;
3. the second-law efficiency of the turbine;
4. the exergy destruction;
5. the specific exergy of the steam at the inlet conditions.

## Model

Steam flows through the turbine (control volume with one inlet and one outlet);
the ambient conditions define the dead state. The properties of steam at the two
states and of water at the ambient state come from the `Water` real-fluid
property functions.

- **First law** on the turbine alone gives the actual power:
  $\dot W_t = \dot m (h_2 - h_1) - \dot Q_{loss}$
- **Exergy balance** on the *extended* control volume (turbine + immediate
  environment), where the heat loss to the ambient happens at the ambient
  temperature and therefore carries no exergy, gives the maximum reversible
  power, computed here as the flow-exergy drop:
  $\dot W_{rev} = \dot m (\varphi_2 - \varphi_1)$ with
  $\varphi = (h - h_0) - T_0 (s - s_0)$
  (the dead-state enthalpy and entropy cancel out in $\varphi_1 - \varphi_2$,
  but the dead-state *temperature* $T_0$ does not);
- **Second-law efficiency** $\eta_{II} = \dot W_t / \dot W_{rev}$;
- **Exergy destruction** $\dot X_{destroyed} = \dot W_{rev} - \dot W_t$.

Sign convention as in the original: a power delivered by the turbine is
negative, so `W_dot_t`, `W_dot_rev` and `X_dot_destroyed` are negative; the
delivered powers and the destroyed exergy are their absolute values.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `p_1`, `T_1` inlet | 3 MPa, 450 °C | `W_dot_t` actual power | −4.3060 MW (4.306 MW delivered) |
| `p_2`, `T_2` outlet | 0.2 MPa, 150 °C | `W_dot_rev` reversible power | −5.0720 MW (5.072 MW) |
| `p_0`, `T_0` ambient | 100 kPa, 25 °C | `eta_II` second-law efficiency | 84.90 % |
| `Q_dot_loss` heat loss | −300 kW | `X_dot_destroyed` exergy destruction | −766.0 kW (766 kW destroyed) |
| `m_dot` mass flow | 8 kg/s | `phi_1`, `phi_2` specific flow exergy | 1236.8 / 602.8 kJ/kg |

## How to run

Open `steam_turbine_exergy_balance.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./steam_turbine_exergy_balance.eescode
```

Every equation is explicit: no guess values (`.initials`), no solver settings
and no runnable variant are needed.

## Results

| Variable | Value | Unit |
|---|---:|---|
| `W_dot_t` (actual power) | −4 305 959 | W |
| `W_dot_rev` (reversible power) | −5 072 005 | W |
| `eta_II` | 0.84897 | – |
| `X_dot_destroyed` | −766 045 | W |
| `phi_1` (inlet flow exergy) | 1 236 830 | J/kg |
| `phi_2` (outlet flow exergy) | 602 829 | J/kg |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 turbine inlet, 2 turbine
outlet, 3 outlet of the reversible *adiabatic* expansion of the inlet state to
the outlet pressure) give the process path on the P-h or T-s diagram (CoolSolve
*Diagram* tab, *Overlay array path*); state 3 is a post-processing addition, not
an equation of the original model.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the
     steam expansion with the isentropic outlet state 3, figures/steam_turbine_exergy_balance_ts.png -->

## Verification

Compared with the solution stored by EES in the source file
(`compare_solution.py … --ees-units`, the three reference temperatures
converted from K to °C): **20 common variables, 0 differ (rtol=0.001)**, largest
relative deviation **4.12·10⁻¹⁰** (`W_dot_t`), i.e. exact agreement to
round-off — both tools evaluate the same `Water` properties on this state, and
the absolute enthalpies and entropies need no reference-state correction.

| Variable | EES (converted) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `h_1` [J/kg] | 3 344 842.97 | 3 344 842.97 | 1.8·10⁻¹⁰ |
| `h_2` [J/kg] | 2 769 098.06 | 2 769 098.06 | 2.3·10⁻¹⁰ |
| `s_1` [J/(kg·K)] | 7085.6109 | 7085.6109 | 2.5·10⁻¹⁰ |
| `W_dot_t` [W] | −4 305 959.30 | −4 305 959.30 | 4.1·10⁻¹⁰ |
| `W_dot_rev` [W] | −5 072 004.59 | −5 072 004.59 | 2.6·10⁻¹⁰ |
| `X_dot_destroyed` [W] | −766 045.29 | −766 045.29 | 1.8·10⁻¹⁰ |
| `phi_1` [J/kg] | 1 236 829.86 | 1 236 829.86 | 5.3·10⁻¹¹ |
| `eta_II` | 0.8489660 | 0.8489660 | 2.2·10⁻¹¹ |

Five records of the EES reference are not variables of the model: `X_dot_in`,
`X_dot_out`, `dX_system` and `dt` are the symbols written in the section
comment of the exergy balance (EES lists them as variables with the value
`inf`), and `eta_II_bis` is the commented alternative of the original. The 13
CoolSolve variables without counterpart are the input temperatures (converted
to °C, so not comparable), `T_0_K` and the 12 state-array entries.

**Additional reference (not used for the numbers above).** The course folder
holds a Python/CoolProp solution of the same exercise of the previous session
(`old/ThAp21_R10E02.py`): it uses the same balances and the same sign
conventions (verified by reading it), so the stored EES solution and this
model agree with it equation by equation. It could not be run here (no CoolProp
module in this environment).

## Source and attribution

Solution of repetition exercise 2 (session 10, exergy) of the ULiège course
*Thermodynamique appliquée* (MECA0002), a session on exergy analysis of open
systems; the exercise asks for the actual power, the maximum power, the
second-law efficiency, the exergy destruction and the specific exergy at the
inlet. The EES file names no author (its `{$ID$}` tag is the laboratory's
student/staff licence); the companion course files attribute the session to the
repetition assistants N. Paulus and B. Dechesne (course by S. Quoilin) — to be
confirmed by the maintainer.

Source file (EES X10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R10/R10_E02_2022.EES`
(inventory candidate `TM-0389`, representative of the 2-file duplicate group
`DG-0093`; `TM-0544` is the same file inside `R10.zip`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): EES
  X10.836, 25 variable records, no lookup or parametric table, no external
  function; `{$ID$}`, `{$PX$96}` and `{$ST$ON}` tags removed. Unit system
  `SI MASS DEG PA K J` converted **by hand** to `SI MASS DEG PA C J` (pressures,
  powers and specific properties were already SI): `T_1 = 450 [C]`
  (723.15 K), `T_2 = 150 [C]` (423.15 K), `T_0 = 25 [C]` (298.15 K), each with
  the original value in the comment. Because `T_0` is now in °C and enters the
  exergy terms as an absolute temperature, an explicit absolute-temperature
  variable `T_0_K = T_0 + 273.15 [K]` was added and used in `phi_1`, `phi_2`.
  Comments translated to English (paraphrasing the French original, including
  its sign conventions and its note on the alternative second-law efficiency),
  section titles in the `"!…"` display form, standard header added, equations
  otherwise unchanged. Verified against the EES stored solution (see above).
- **2026-10-05 — diagram support**: block of 12 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`) added at the end of the model
  for the CoolSolve diagrams. State 3 (isentropic outlet at `p_2`,
  `T[3] = 120.2 °C`) is not computed by the original equations; it was added in
  post-processing only. The results of the model are unchanged.
- **Level**: equations 33 (< 50 → 0), largest algebraic block 1 (≤ 5 → 0),
  structure: state arrays present (1), no multi-zone/discretisation (0), no
  semi-empirical/off-design physics (0), no curated guesses or solver settings
  (0) → score 1 → level 1.

## Limitations and CoolSolve gaps

- Thermally and mechanically simple: a single control volume with one inlet and
  one outlet, no mechanical or heat-transfer losses other than the given heat
  loss, no change of kinetic or potential energy, and the heat loss is assumed
  to happen at the ambient temperature (extended control volume, as in the
  original); no dead-state pressure/temperature sensitivity study is included.
- The sign convention of the original (delivered power negative) is kept; read
  the absolute values.
- No CoolSolve gap blocks this model. For the legitimate 450 °C inlet
  temperature CoolSolve prints the temperature hint of `src/user_hints.cpp`
  (*"enthalpy(): t=450 is interpreted as 450 °C. If you meant 450 K, use
  T=176.85"*), the same noisy-hint family as the registered
  `CS-BUG-HINT-FAHRENHEIT`; the value is correct.

## Related models

- `CSL-0004` (Rankine cycle of a 60 MW steam power plant): the same steam
  turbine physics at plant scale, with the exergy balance of the whole cycle.
- `CSL-0003` (evaporation of liquid methane in a tank): the same course and the
  same session family (properties of a real fluid in °C/Pa/J), imported in the
  same way.
- `CSL-0048` (two rigid tanks connected by a valve, change of the quality of
  R12): another model of the same course and session series (repetition R1,
  exercise 4), imported the same way.
- `CSL-0056` *iron_block_quench_water_tank*: same course and session family
  (repetition 10, 2022-2023), the closed-system counterpart: exergy of an
  incompressible substance and exergy destruction of an isolated system.
- `CSL-0057` *two_tanks_max_work_air*: the maximum-work counterpart of this
  exercise on a closed extended system (two air tanks coupled by a heat engine),
  same session 10 (exergy), exercise 3.
