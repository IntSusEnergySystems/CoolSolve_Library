# ORC expander and pump empirical maps (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0084`

Empirical performance maps of the volumetric machines of an organic Rankine
cycle: the isentropic-efficiency and filling-factor fits of three expander
technologies (hermetic scroll, open-drive scroll, single screw), the
mass-flow and isentropic-efficiency curves of the ULiège test-rig pump, the
pump efficiency curve of the SQ thesis and the quadratic pressure-drop fits of
the test-rig lines. All eleven routines come from the ThermoCycle Modelica
library and keep their original names and signatures, so a model can copy them
in a `{--- Library functions copied from CSL-0084 ---}` block (until
`$INCLUDE library:orc_expander_pump_empirical_maps` is available). A small
closed ORC demo on R245fa couples the hermetic-scroll map to the pump curve.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | R245fa (demo only — the maps take density, pressure ratio, speed and pressure, no fluid) |
| **Size** | 79 equations (largest block: 1); 11 `FUNCTION`s (one per map) |
| **Source** | ThermoCycle Modelica library, `ThermoCycle/Functions/*.mo` and `Components/Units/ExpansionAndCompressionMachines/{Expander,Pump}.mo`, commit `b4f16c0b`, MIT — <https://github.com/thermocycle/Thermocycle-library> |
| **Authors** | Adriano Desideri, Sylvain Quoilin, Jorrit Wronski (git history of the correlation files, ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@536d427 — verified against an independent Python/CoolProp re-evaluation (max. 9.74e-11) |

## Problem statement

A map-based machine model needs two things: a filling factor (or volumetric
efficiency) that says how much fluid the machine swallows per revolution, and
an isentropic efficiency that says how much of the ideal work is actually
delivered or consumed. ThermoCycle ships measured-data fits for three
volumetric expander technologies and for the pumps of the ULiège ORC rigs,
plus the quadratic pressure-drop fits of the rig lines. They are the
map-based counterpart of the semi-empirical expander `CSL-0037` and of the
polynomial CO₂ ORC `CSL-0038`, and they cover part-load behaviour, which a
constant-efficiency machine model cannot.

## Model

Eleven `FUNCTION`s (one per map, equations exactly as in the original):

| Function | Signature | Returns |
|---|---|---|
| `correlation_hermetic_scroll_epsilon_s` | `(rho, rp)` | isentropic efficiency [−], polynomial in ln(ρ) and ln(rp), clamped 0…0.65 |
| `correlation_hermetic_scroll_FF` | `(rho, rp)` | filling factor [−], same variables, clamped 1…1.2 |
| `correlation_open_expander_epsilon_s` | `(N_rot, rho, log_rp)` | isentropic efficiency [−], clamped 0…0.79; `N_rot` is passed the speed in rev/min and `log_rp` = ln(p_su/p_ex), as by the original caller |
| `correlation_open_expander_FF` | `(log_Nrot, rho)` | filling factor [−], clamped 0.576…1.592; `log_Nrot` = ln(rpm) |
| `GenericScrewExpander_IsentropicEfficiency` | `(rp, rpm, p)` | isentropic efficiency [−], `D·sin(C·atan(…))` curve of the pressure ratio shifted by speed and supply pressure (`p` in Pa → bar inside) |
| `GenericScrewExpander_FillingFactor` | `(p_su_exp, rho_su_exp, rpm)` | FFVs = ṁ/(n·ρ) [m³/s]; `Expander.mo` uses it as `FF` with the swept volume set to `V_s = 1 m³` (comment of the original) |
| `GenericCentrifugalPump_IsentropicEfficiency` | `(f_pp, r_p)` | pump isentropic efficiency [−], clamped 0…0.8 (`f_pp` in Hz, `r_p` = p_ex/p_su) |
| `GenericCentrifugalPump_MassFlowRate` | `(f_pp)` | pump mass flow rate [kg/s] (rig curve, `f_pp` in Hz) |
| `correlation_eta_is_pump` | `(Xpp)` | pump isentropic efficiency [−] at the flow fraction, `0.931 − 0.11·ln X − 0.2·ln²X − 0.06·ln³X` |
| `PressureDropCorrelation_HP` / `_LP` | `(M_flow)` | rig line pressure drop [Pa] = k1·ṁ + k2·ṁ² |

Governing equations of the machine blocks (as in `Expander.mo` and `Pump.mo`):

- expander: `V_dot_su = FF·V_s·N_rot`, `V_dot_su = ṁ/ρ_su`,
  `h_ex = h_su − (h_su − h_ex_s)·ε_s`, `Ẇ = ṁ·(h_su − h_ex)`;
- pump: `h_ex = h_su + (p_ex − p_su)/(η·ρ_su)`, `Ẇ = ṁ·(h_ex − h_su)`,
  `η = η_in·η_em`, `X_pp = f_pp/50`.

The demo program after the definitions runs one point of a small closed ORC
on R245fa: condenser 35 °C (3 K subcooled), evaporator 80 °C (5 K
superheated), pump at `f_pp` = 40 Hz through the `PumpTypes.SQThesis` branch
of `Pump.mo` (`Ṁ = Ṿ_max·min(X_pp, 1)·ρ`, `η_in` from log₁₀ of the flow
fraction), hermetic-scroll expander map (`ExpTypes.HermExp`), swept volume
`V_s` = 1.0·10⁻⁴ m³. The expander speed is an *output*: the pump fixes the
mass flow and the map fixes the swallowed volume. All blocks are explicit
(the system is square with largest block 1), so no `.initials` file is needed.

**Inputs** (demo): `T_ev`, `T_cd` [°C], `DELTAT_sh`, `DELTAT_sc` [K],
`f_pp` [Hz], `V_dot_max` [m³/s], `V_s` [m³], `eta_em` [−].
**Outputs**: `M_dot` [kg/s], `N_rot` [Hz] and `rpm` [rev/min], `epsilon_s`,
`FF`, `η`, `W_dot_pump`, `W_dot_exp`, `W_dot_net` [W], `Q_dot_ev`,
`Q_dot_cond` [W], `eta_th` [−], `err_bal` [W], state points `P[i]`, `h[i]`,
`T[i]`, `s[i]` (i = 1 pump suction, 2 pump discharge, 3 expander supply,
4 expander exhaust).

## How to run

Open `orc_expander_pump_empirical_maps.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./orc_expander_pump_empirical_maps.eescode
```

No guesses are needed. Change `T_ev`, `f_pp` or `V_s` to explore the map; the
demonstration program is the regression baseline
(`orc_expander_pump_empirical_maps.sol`).

## Results

Map check points (each function called once with typical values; the Python
column is the independent re-evaluation of the same polynomials):

| Function | Inputs | CoolSolve | Python |
|---|---|---:|---:|
| `correlation_hermetic_scroll_epsilon_s` | ρ = 50 kg/m³, rp = 6 | 0.56108191 | 0.56108191 |
| `correlation_hermetic_scroll_FF` | ρ = 50 kg/m³, rp = 6 | 1.00456018 | 1.00456018 |
| `correlation_open_expander_epsilon_s` | 3000 rev/min, ρ = 50, ln 6 | 0.68215583 | 0.68215583 |
| `correlation_open_expander_FF` | ln 3000, ρ = 50 | 1.01562606 | 1.01562606 |
| `GenericScrewExpander_IsentropicEfficiency` | rp = 4, 3000 rev/min, 10 bar | 0.44336774 | 0.44336774 |
| `GenericScrewExpander_FillingFactor` | 10 bar, ρ = 50, 3000 rev/min | 1.60310e-4 m³/s | 1.60310e-4 m³/s |
| `GenericCentrifugalPump_IsentropicEfficiency` | 40 Hz, r_p = 9 | 0.20753851 | 0.20753851 |
| `GenericCentrifugalPump_MassFlowRate` | 40 Hz | 0.42133135 kg/s | 0.42133135 kg/s |
| `correlation_eta_is_pump` | X = 0.8 | 0.94625384 | 0.94625384 |
| `PressureDropCorrelation_HP` / `_LP` | ṁ = 0.3 kg/s | 10542.2 / 13631.6 Pa | 10542.2 / 13631.6 Pa |

ORC demo (R245fa, 80/35 °C):

| Output | Value | Output | Value |
|---|---:|---|---:|
| `p_ev` | 7.89 bar | `epsilon_s` | 0.5201 |
| `p_cd` | 2.12 bar | `FF` | 1.000 (clamped at the lower bound) |
| `M_dot` | 0.2111 kg/s | `N_rot` / `rpm` | 49.73 Hz / 2984 rev/min |
| `η_in` (pump) | 0.9396 | `W_dot_exp` | 2723.8 W |
| `W_dot_pump` | 98.3 W | `Q_dot_ev` / `Q_dot_cond` | 47.81 / 45.18 kW |
| `W_dot_net` | 2625.6 W | `eta_th` | 5.49 % |
| `T[4]` expander exhaust | 61.0 °C | `err_bal` | 5.5e-12 W |

The pump delivers 0.211 kg/s at 80 % of `V_dot_max`; the expander map returns
ε_s = 0.52 and a filling factor at its lower clamp of 1, and the loop closes at
2.63 kW of net power (5.5 % thermal efficiency — a small single-stage ORC with
no recuperator). The expander needs 2984 rev/min to swallow the pumped flow at
`V_s` = 0.1 L/rev.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the demo ORC,
     figures/orc_expander_pump_empirical_maps_ph.png -->

## Verification

**Reference: independent Python/CoolProp re-evaluation** (ThermoCycle stores no
reference results — its test models are dynamic drivers without asserted
values, and OpenModelica/Dymola are not installed here). A throw-away virtual
env under `work/orc_maps/` (deleted when the card was closed) re-implemented
the eleven polynomials directly from the `.mo` sources (`log` in Modelica is
the natural logarithm) and rebuilt the ORC states with CoolProp 8.0.0, the
property backend CoolSolve uses; the results were written to a
`name,value` CSV and compared with the solved file:

```text
62 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 17
```

The maximum relative difference over the 62 common variables is **9.74e-11**
(`eta_th`), i.e. round-off only. `err_bal` is excluded from that maximum: it
is 0 by construction in Python and 5.5e-12 W in CoolSolve. The 17 variables
only in CoolSolve are the inputs of the demo (`T_ev`, `T_cd`, `DELTAT_*`,
`f_pp`, `V_dot_max`, `V_s`, `eta_em`, `fluid$`) and the constants of the check
points (`rho_map`, `rp_map`, `rpm_map`, `p_map`, `rp_screw`, `r_p_pump`,
`X_pp_map`, `M_dot_rig`).

Physical sanity (also checked): all efficiencies stay in their clamped ranges,
the powers are positive and `Ẇ_exp − Ẇ_pump = Q̇_ev − Q̇_cond` to 5.5e-12 W.
The hermetic-scroll fit really needs its clamp: its raw polynomial returns
−1.608 at ρ = 10 kg/m³ and rp = 2 (recomputed in Python), so outside its
calibration range the map is unusable without the `min`/`max` of the original.

## Source and attribution

```text
This CoolSolve model is a translation (EES-compatible language, equation-oriented) of
the expander and pump performance maps from the ThermoCycle Modelica library, files
ThermoCycle/Functions/correlation_*.mo, ThermoCycle/Functions/TestRig/*.mo,
ThermoCycle/Components/Units/ExpansionAndCompressionMachines/{Expander,Pump}.mo,
commit b4f16c0b.
ThermoCycle - https://github.com/thermocycle/Thermocycle-library
Copyright (c) 2018 Thermodynamics Laboratory (University of Liege), MIT License.
Original authors: S. Quoilin, A. Desideri, J. Wronski, I. Bell (see the git history of the files).
Changes: translated from Modelica to CoolSolve; der() terms set to zero (steady state);
radian/degree conversions of the screw map; log -> ln; boundary connectors dropped
(see the conversion log). Scientific basis: the fits of the ULiège ORC test rigs
(Quoilin PhD thesis 2011; Desideri et al., screw-expander waste-heat ORC) — the exact
sources of the coefficients are not documented in the library; the maintainer can confirm.
```

Source (local clone of the public repository):
`~/git/Thermocycle-library/ThermoCycle/Functions/…`, inventory candidate `THC-003`.

## Conversion log

- **2026-10-06 — translation** (card C-91, `T-FUNC`/`T-TRANSLATE`): the eleven
  `.mo` function files and the two machine models translated to EES. Units
  already SI; the machine models carry no temperature equation (properties were
  in `setState_ph/ps`), so no °C/K conversion was needed. Modelica `log` is the
  natural logarithm → EES `ln` (in `correlation_hermetic_scroll_*`,
  `correlation_open_expander_*` at the call sites, and
  `correlation_eta_is_pump`); Modelica `log10` stays EES `log10` (the form the
  EES files of the ULiège collection use). Modelica trigonometry is in radians
  and EES in degrees, so the screw efficiency curve writes
  `atan(…)*pi()/180` where the original has `atan(…)` and `tan(90/C)` where it
  has `tan(pi/(2C))`; the outer `sin(C·atan(…))` is form-invariant between the
  two angle conventions and is written as in the original. `pi()` (not bare
  `pi`) is used inside the `FUNCTION`: see *Limitations*.
- **2026-10-06 — steady state.** `Expander.mo` and `Pump.mo` contain no `der()`
  (the rotor inertia lives in the flange equation `der(phi) = 2π·N`, dropped
  with the mechanical connector). Dropped from the two machine models: the
  `inStream`/`noEvent` flow-reversal boundary branches, the connector equations
  and the initialisation parameters (`*_start`, `constinit`, `t_init`), which
  only serve the dynamic solver; the demo imposes one flow direction. The
  machine equations themselves are unchanged.
- **2026-10-06 — clamps kept.** The five `min`/`max` clamps of the original
  maps are non-smooth but they are equations of the source (and the only thing
  that keeps the fits physical outside their range), so they are kept as EES
  `min`/`max`; the demo point lies at the `FF` clamp (raw value below 1).
- **2026-10-06 — conventions kept.** Screw `FFVs` is a volume flow
  [m³/s] (`Expander.mo` uses it as `FF` with `V_s = 1 m³`, source comment);
  `correlation_open_expander_epsilon_s` takes the speed in rev/min although its
  argument is called `N_rot` (the caller passes `rpm`); the pump fit is centred
  on `f_pp` = 30 Hz and `r_p` = 9, where it returns 0.164 — a rig-specific fit,
  reported as it is, while the demo uses the `SQThesis` branch of `Pump.mo`
  (0.940 at `X_pp` = 0.8).
- **Source defects checked** (`sources/thermocycle/README.md` §8): none of the
  listed defects is in this row — `Eps_t[N]` belongs to THC-001, the missing
  `ORCNext` enum value only affects the stale `step_by_step` examples (not
  translated), and the undocumented validity range of the maps is documented
  above instead.
- **Level**: 79 equations → 1; largest block 1 → 0; 11 functions → 1;
  no multi-zone/discretised structure → 0; semi-empirical off-design maps → 1;
  no curated guesses → 0. Score 3 → level 2.

## Limitations and CoolSolve gaps

- The maps have **no documented validity range** (source defect): outside the
  calibration range the polynomials leave the physical range and only the
  clamps hold them (`ε_s` = −1.608 before the clamp at ρ = 10 kg/m³, rp = 2).
  Use the check points of the *Results* table as a sanity anchor.
- The rig curves are machine-specific: `GenericCentrifugalPump_*` returns
  η_in = 0.164 at its own anchor (`f_pp` = 30 Hz, `r_p` = 9), and
  `GenericScrewExpander_FillingFactor` returns a volume flow, not a
  dimensionless factor. No registered gap blocks the file (`missing_features`
  is empty).
- CoolSolve prints the spurious *"looks like Fahrenheit"* warning for
  `T_ev` = 80 °C, `T_cd` = 35 °C and `T_1` = 32 °C — an instance of the
  registered `CS-BUG-HINT-FAHRENHEIT`; the values are used as °C (evidence:
  `p_ev` matches the Python saturation pressure at 80 °C).
- **Unverified suggestion** (not registered): in a `FUNCTION` body the bare
  constant `pi` resolves to an undefined variable (value 1) in CoolSolve, while
  `pi()` and the main program give π; CoolSolve's own `language_reference.md`
  documents `pi` / `pi()` as the constant. The file therefore writes `pi()`
  inside the `FUNCTION`, which is the form EES documents as well.

## Related models

- `CSL-0037` *scroll_expander_semi_empirical*: the same machine at the
  semi-empirical level of detail; this library is the map-based alternative.
- `CSL-0038` *orc_co2_polynomial_maps*: another map-based ORC (CO₂, polynomial
  performance surfaces) — same approach, other fluid and maps.
- `CSL-0019` *orc_simple_r245fa*: the same fluid and a similar screening
  purpose; there the component performance is imposed instead of mapped.
- `CSL-0125` *pump_curve_similarity*: pump from manufacturer curves scaled
  with the affinity laws (three operating modes); the same off-design purpose
  with catalogue data instead of a fitted map.
- `CSL-0117` *double_stage_scroll_expander*: the original ULiège EES
  correlations of the same hermetic scroll expander (Lemort/Quoilin/Pire)
  from which the ThermoCycle hermetic-scroll maps of this library derive.
