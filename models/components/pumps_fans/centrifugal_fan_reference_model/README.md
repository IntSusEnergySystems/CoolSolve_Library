# Centrifugal fan reference model (dimensionless factors)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0071`

Reference simulation of a centrifugal fan transporting humid air. The fan is
given by its geometry (impeller diameter, exhaust area) and its rotation speed;
the operating point is imposed by the supply state and the air mass flow rate.
The model returns the dimensionless factors of the machine — flow factor,
pressure factor, isentropic effectiveness, power factor — together with the
static and total pressure rises, the exhaust speed and the shaft power. The
factors are closed on the operating point by two cubic fits in the pressure
factor (the `alpha_i` and `beta_i` coefficients), which is how the ULiège
reference model makes the fan curve act on the inlet state.

| | |
|---|---|
| **Category** | Components › Pumps and fans |
| **Fluids** | Humid air (`AirH2O`, per kg of dry air) |
| **Size** | 34 equations, all explicit (largest block: 1): 19 of the original model, 15 assigning the 5 inputs and 10 parameters |
| **Source** | ULiège Thermodynamics Laboratory, model data bank, *Distribution systems › Fans* — "FAN REFERENCE MODEL", 2008-03-18 (EES file `Centrifugal_Fan_RefSim_EES_Model_ARJL080121.EES`, EES 7.966) |
| **Authors** | Vlad Teodorese and Andrés Rodríguez, reviewed by Jean Lebrun (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

The model data bank of the ULiège Thermodynamics Laboratory ships a
*reference* and a *parameter-identification* version of the same fan. This is
the reference version: it takes the fan (impeller diameter, exhaust area,
rotation speed) and the air arriving at the fan (pressure, temperature,
relative humidity, mass flow rate) and returns the dimensionless factors that
characterise the fan at that point.

Its purpose is to give a fan manufacturer or a system designer a *transfer
function*: enter the fan data and the inlet state, read the flow, the pressure
rise and the shaft power. The parameter-identification companion
(`thermo_models` candidate `TM-0485`, not yet imported) fits the `alpha_i` and
`beta_i` coefficients of these two polynomial curves to catalogue points instead
of taking them as given.

Default operating point of the original file: 4500 min⁻¹, impeller diameter
0.323 m, exhaust area 0.161 m², supply air at 80 °C / 101 325 Pa / 50 % RH,
air mass flow rate 2.7 kg/s.

## Model

The four factors of the fan are, as in the original file:

| Factor | Definition | Value |
|---|---|---:|
| flow factor | $\phi = \dot V / (A\,U)$ | 0.5653 |
| pressure factor | $\psi = \Delta p_{total} / (U^2/2v)$ | 0.6033 |
| isentropic effectiveness | $\epsilon_s = \dot W_s / \dot W_{shaft}$ | 0.6633 |
| power factor | $\lambda = \phi\,\psi / \epsilon_s$ | 0.5145 |

with the reference area $A = \pi D^2/4$, the peripheral speed $U = \pi D N$ and
$N$ in s⁻¹, the exhaust speed $C_{ex} = \dot V/A_{ex}$, and the dynamic
pressures $U^2/2v$ and $C_{ex}^2/2v$ built on the specific volume $v$ of the
humid air at the fan supply. The isentropic (ideal) power of the air stream is
$\dot W_s = \dot V\,\Delta p_{total}$ (flow coefficient = 1). The mass flow rate
fixes the volume flow rate, $\dot V = \dot m\,v$, and $\dot V$ is also reported
in m³/h.

Two cubic polynomials close the operating point, as in the original:

$$\phi = \alpha_0 + \alpha_1 \psi + \alpha_2 \psi^2 + \alpha_3 \psi^3,
\qquad
\lambda = \beta_0 + \beta_1 \psi + \beta_2 \psi^2 + \beta_3 \psi^3$$

Because $\psi$ (through $\Delta p_{stat}$) and $\epsilon_s$ are unknowns of the
system, the two polynomials and the two definitions of $\phi$ and $\lambda$ are
mutually consistent: $\phi$ is fixed by the flow factor, $\psi$ follows from the
polynomial, then $\Delta p_{total}$, $\Delta p_{stat}$, $\lambda$,
$\epsilon_s$ and $\dot W_{shaft}$ follow in turn. `M_dot`, `phi` and `lambda`
therefore each carry two equations, as in the original file (`M_dot` is both an
input and `M_dot = V_dot/v`; `phi` and `lambda` are both a factor and a
polynomial), and the system is consistent at the solution.
`coolsolve -d` reports `System square: Yes`, 34 equations / 34 variables,
largest block 1.

The specific volume and the specific heat of the humid air come from
CoolProp's humid-air model (`AirH2O`) at $(T_{su}, P_{su}, RH_{su})$; the
thermal capacity flow rate $\dot C = \dot m c_p$ is a diagnostic output (it
feeds no other equation).

| Inputs | Value | Outputs | Value |
|---|---:|---|---:|
| `P_su` supply air pressure [Pa] | 101 325 | `V_dot_mh` volume flow [m³/h] | 12 700 |
| `T_su` supply air temperature [°C] | 80 | `phi` flow factor [-] | 0.5653 |
| `RH_su` supply air relative humidity [-] | 0.5 | `psi` pressure factor [-] | 0.6033 |
| `M_dot` air mass flow rate [kg/s] | 2.7 | `DELTAP_stat` static pressure rise [Pa] | 1153 |
| `rpm` fan rotation speed [min⁻¹] | 4500 | `DELTAP_total` total pressure rise [Pa] | 1337 |
| `D` impeller diameter [m] | 0.323 | `C_ex` exhaust speed [m/s] | 21.91 |
| `A_ex` average exhaust area [m²] | 0.161 | `epsilon_s` isentropic effectiveness [-] | 0.6633 |
| `alpha_0..3` flow fit coefficients [-] | 0.7733, −0.389, 0.4471, −0.6178 | `W_dot_shaft` fan power [W] | 7111 |
| `beta_0..3` power fit coefficients [-] | 0.408, 0.357, −0.07773, −0.3671 | `lambda` power factor [-] | 0.5145 |

## How to run

Open `centrifugal_fan_reference_model.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./centrifugal_fan_reference_model.eescode
```

`.initials` holds the guess values of the stored EES solution; they are not
needed for convergence — the model also converges from deliberately poor
guesses (checked with `v` = 0.8, `psi` = 0.2, `DELTAP_total` = 300 Pa,
`epsilon_s` = 0.4: 27 iterations, same solution). Change `rpm`, `M_dot`,
`D`, `A_ex` or the eight polynomial coefficients to study another fan or
another point; the model is a plain explicit system (34 equations, largest
block 1).

## Results

Default operating point of the original file:

| Quantity | EES 7.966 | CoolSolve 0.3.0 | rel. diff |
|---|---:|---:|---:|
| `V_dot` volume flow rate [m³/s] | 3.525133 | 3.527816 | 7.6e-04 |
| `V_dot_mh` volume flow rate [m³/h] | 12 690.5 | 12 700.1 | 7.6e-04 |
| `phi` flow factor [-] | 0.5652843 | 0.5657146 | 6.9e-07 |
| `psi` pressure factor [-] | 0.6040722 | 0.6032511 | 1.4e-03 |
| `DELTAP_stat` static pressure rise [Pa] | 1156.31 | 1153.33 | 2.6e-03 |
| `DELTAP_total` total pressure rise [Pa] | 1339.91 | 1337.07 | 2.1e-03 |
| `C_ex` exhaust speed [m/s] | 21.8952 | 21.9119 | 4.7e-04 |
| `W_dot_s` isentropic power [W] | 4723.35 | 4716.93 | 1.4e-03 |
| `epsilon_s` isentropic effectiveness [-] | 0.6638647 | 0.6633205 | 1.0e-03 |
| `W_dot_shaft` fan power [W] | 7114.93 | 7111.08 | 5.2e-04 |
| `lambda` power factor [-] | 0.5143708 | 0.5144842 | 8.7e-04 |
| `c_p` specific heat [J/(kg·K)] | 1364.99 | 1381.36 | 1.2e-02 |
| `C_dot` thermal capacity flow rate [W/K] | 3685.46 | 3729.68 | 1.2e-02 |

At the default operating point the fan moves 2.7 kg/s of humid air through a
32.3 cm impeller turning at 4500 min⁻¹: 1337 Pa of total pressure rise (1153 Pa
static, 184 Pa exhaust dynamic pressure) for 7111 W of shaft power, i.e. an
isentropic effectiveness of 0.663 and a power factor of 0.514.

The figure suggested for this model is a **parametric sweep** (the humid-air
pseudo-fluid has no thermodynamic diagram in CoolSolve yet,
`CS-FEAT-DIAGRAM-IDEAL`): pressure factor, shaft power and flow factor versus
the pressure factor `psi`, with `M_dot` as the swept input.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7):
     figures/centrifugal_fan_reference_model_sweep.png -->

## Verification

The original equations were transcribed unchanged (the 19 model equations of the
extraction, plus the 15 assignments that give the inputs and parameters the
values they had in the EES file) and solved; `tools/compare_solution.py`
against the solution stored in the original EES file gives:

```
34 common variables, 6 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1
| Variable | EES | CoolSolve | rel. diff |
| C_dot | 3685.46 | 3729.68 | 1.19e-02 |
| c_p | 1364.99 | 1381.36 | 1.19e-02 |
| DELTAP_stat | 1156.31 | 1153.33 | 2.58e-03 |
| DELTAP_total | 1339.91 | 1337.07 | 2.12e-03 |
| psi | 0.604072 | 0.603251 | 1.36e-03 |
| W_dot_s | 4723.35 | 4716.93 | 1.36e-03 |
```

`coolsolve -d` reports `System square: Yes` (34 equations, 34 variables, largest
block 1), 34 equations checked and satisfied, max |residual| 4.996e-13 — so the
three variables that carry two equations in the original (`M_dot`, `phi`,
`lambda`) are consistent at the solution.

**Explanation of the deviations.** All of them come from the humid-air
properties, i.e. from the moist-air models of EES 7.966 and of CoolProp, not
from the fan equations:

- *specific heat* (1.19e-02, the largest deviation of the model): at
  80 °C / 101 325 Pa / RH 0.5 the humidity ratio is `w` = 0.19139 kg/kg dry
  air, so a mixture specific heat per kg of dry air of
  $c_{p,da} + w\,c_{p,v}$ with $c_{p,da}$ = 1009.46 J/(kg·K) implies
  $c_{p,v}$ = 1857.6 J/(kg·K) for EES and 1943.2 J/(kg·K) for CoolProp — a
  4.6 % difference on the vapour part, which the 19 % humidity ratio scales
  down to 1.2 % on the mixture. `c_p` feeds only the diagnostic output
  `C_dot`, which feeds no equation.
- *specific volume*: `v` = 1.305605 (EES) against 1.306599 m³/kg (CoolProp),
  7.6e-04. It enters the two dynamic pressures, hence `psi` and
  `DELTAP_total`/`DELTAP_stat` (1.4e-03 to 2.6e-03), `W_dot_s` (1.4e-03),
  `V_dot` (7.6e-04) and, at second order, `phi`, `C_ex`, `lambda`,
  `epsilon_s` and `W_dot_shaft` (≤ 1.0e-03).

Both properties are per kg of **dry** air (EES `AirH2O` convention); the file's
own unit hints give `A_ex` in m², `v` in m³/kg. Not compared: `pi`, which
CoolSolve writes into the `.sol` as a constant although the original equations
call `pi` (this is the "only in CoolSolve" variable).

Sanity checks (recomputed with one-liners on the printed solution):

- `V_dot` = `M_dot`·`v` = 2.7 × 1.306599 = 3.527816 m³/s, i.e.
  `M_dot`/`V_dot` = 2.7/3.527816 = 0.76535 kg/m³ = 1/`v` ✓
- `phi` = `V_dot`/(`A`·`U`) = 3.527816/(0.0819398 × 76.1051) = 0.565715 ✓
- operating-point closure: the `alpha` polynomial at `psi` = 0.6032511 gives
  0.7733 − 0.389 × 0.6032511 + 0.4471 × 0.6032511² − 0.6178 × 0.6032511³ =
  0.565715 = `phi`, and the `beta` polynomial at the same `psi` gives 0.514484
  = `phi`·`psi`/`epsilon_s` = `lambda` (both to 1e-13) ✓
- `W_dot_shaft` = `W_dot_s`/`epsilon_s` = 4716.93/0.6633205 = 7111.08 W ✓
- `DELTAP_total` = `DELTAP_stat` + `C_ex`²/(2`v`) = 1153.33 + 183.73 =
  1337.07 Pa ✓
- `C_dot` = `M_dot`·`c_p` = 2.7 × 1381.363 = 3729.68 W/K ✓
- dimensional consistency: $\phi$, $\psi$ and $\lambda$ are dimensionless
  (m³/s ÷ (m²·m/s); Pa ÷ (m²/s² ÷ m³/kg); and a product of the two) ✓
- the physical words agree with the numbers: `DELTAP_total` (1337 Pa) >
  `DELTAP_stat` (1153 Pa) as it must be, the difference being the exhaust
  dynamic pressure (184 Pa); the impeller area `A` = π·0.323²/4 = 0.0819 m² is
  the area the flow factor is referred to, and `U` = π·D·N = 76.1 m/s is the
  peripheral speed at 75 s⁻¹ ✓

## Source and attribution

Fan reference model by **Vlad Teodorese** and **Andrés Rodríguez**, reviewed by
**Jean Lebrun** (Thermodynamics Laboratory, Faculty of Applied Sciences,
University of Liège, Campus of Sart Tilman), dated 2008-03-18 in the file
header, which also names the reference used: *ASHRAE (2004) HVAC Systems and
Equipment Handbook*, American Society of Heating, Refrigerating and
Air-Conditioning Engineers, Inc.

The file carries the laboratory disclaimer reproduced in the header: the
accuracy or reliability of the information is not guaranteed, every use incurs
the liability of the user only, the model is freely distributed and may not be
sold, and the user is asked to cite the sources and the origin of the model.
The EES licence stamp (`{$ID$ #1206: Jean Lebrun, Laboratoire de
Thermodynamique, Univ. Liege}`) was removed on import. The authors are taken
from the header comments of the file itself.

Source file (EES 7.966, comments in English, equations stored as RTF), model
data bank of the collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/Distribution_Systems/Fans/CENTRIFUGAL_FAN_REFSIM_MODEL_ARJL080121/Centrifugal_Fan_RefSim_EES_Model_ARJL080121.EES`
(inventory candidate `TM-0251`). The same folder also ships the distributed
executable `CENTRIFUGAL_FAN_REFSIM_EES_MODEL_ARJL080121.EXE`, which is not part
of the library.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already `SI MASS DEG PA C J`, so no conversion by hand; the EES
  licence tag was removed; the extraction holds 19 model equations, 35 variable
  records (one, `b`, has no value and appears in no equation) and no lookup or
  parametric table. The RTF-to-text converter leaves one trailing NUL byte
  (registered `CS-BUG-EXTRACT-NUL`), removed.
- **2026-10-05 — fixed values written as assignments.** EES stores the state of
  each variable (fixed or solved) in the file; the extraction keeps only the
  guesses in `.initials`. The 5 inputs and 10 parameters the file fixes are
  therefore written as assignments at the top of the model, with the values of
  the stored solution (the file's default operating point), which is the
  library convention (see `CSL-0001`). Without them `coolsolve -d` reports
  *"19 equations and 34 unknowns — the system is not square"*, because nothing
  is then pinned. No equation of the model itself was changed, and the stored
  values of the unknowns went into `.initials`, never into an equation.
- **2026-10-05 — variable-name casing normalised.** EES variable names are
  case-insensitive: the original declares the output `Psi` and the parameters
  `Beta_0..3` but writes `psi`, `beta_0..3` and `Phi` in the equations — the
  same three variables (the extraction reports 34 distinct variables, and a
  two-line model mixing `Phi` and `psi` solves in CoolSolve as one system of
  two equations). Casing was normalised to lower case, which changes no
  equation. Variable names themselves are unchanged.
- **2026-10-05 — comments.** English comments of the original kept and turned
  into trailing comments with the SI unit of each quantity (the original
  declared the units in the variables dialog); section titles `"!…"` added for
  the same groups as in the original (`1. OUTPUTS`, `2. INPUTS`,
  `3. PARAMETERS`, `4. MODEL`). No physical meaning was added that the original
  does not state; the closure of the four factors on the operating point is an
  observation about its equations and is discussed above, not written into the
  model. No diagram state arrays: the fluid is the humid-air pseudo-fluid
  `AirH2O`, for which CoolSolve has no thermodynamic diagram
  (`CS-FEAT-DIAGRAM-IDEAL`); the figure is a parametric sweep.
- **Level** (`docs/taxonomy.md` §3): equations 34 → 0 (< 50); largest algebraic
  block 1 → 0 (≤ 5); functions/procedures/arrays: none → 0; multi-zone or
  discretised, ≥ 3 coupled components: no → 0; semi-empirical calibration: yes
  (the two cubic fits of the fan characteristics) → 1; curated guesses,
  simplified-model bootstrap, *Try Harder* or `coolsolve.conf`: no → 0
  (converges from poor guesses). Score 1 → **level 1**, as on the task card.
- **Decision taken (not a card question).** The candidate has no duplicate
  group. Its sibling `TM-0485`
  (`Centrifugal_Fan_ParamID_Reference_EES_Model_ARJL080121.EES`, inside
  `CENTRIFUGAL_FAN_PARAMID_REFERENCE_MODEL_ARJL080121.zip`) is the
  parameter-identification model of the same fan: a *different level of
  detail*, so it is kept as a separate model (workflow §2, rule 4) and is
  referenced in `related_external`; its inventory row stays `todo` (its own
  card).

## Limitations and CoolSolve gaps

- No gap blocks the model; `missing_features` is empty and the native file is
  valid EES (no `_coolsolve` variant needed).
- `VOLUME(AirH2O, T=80, …)` triggers the input hint *"T=80 looks like
  Fahrenheit (room temperature (~25 °C))"* although 80 °C is the value of the
  original file in its `SI MASS DEG PA C J` unit system: a false positive of the
  registered hint (`CS-BUG-HINT-FAHRENHEIT`). It is a warning only; CoolSolve
  uses Celsius. Related registered items, not blocking and not listed in
  `missing_features`: `CS-BUG-UNIT-VOLUME` (`v` is labelled `kg/m^3` in the
  `.sol`; it is m³/kg of dry air).
- The unit system of the original (K, kPa, kJ) is not read by CoolSolve
  (`CS-GAP-UNITSYSTEM`): this file was already in SI-°C-Pa-J, so no conversion
  was needed, but the directive was deleted as in every library model.
- Physical simplifications of the original, kept as they are: the air is
  treated as a fixed-humidity gas along the machine (the humid-air properties
  are evaluated only at the supply state, so heating across the fan does not
  change `v`); no mechanical efficiency and no bearing/drive losses, the
  isentropic effectiveness absorbs them; the dynamic pressures use the
  supply-state specific volume. The polynomial coefficients are the values
  stored in the file, i.e. the fan is *not* identified here (that is
  `TM-0485`).

## Related models

- No other model of the library yet: `components/pumps_fans` is created by this
  model. The dimensionless flow factor also appears in `CSL-0069`
  *centrifugal_compressor_design_similarity* (air), but for a turbocompressor
  (a different machine); no `related` link was added because the back-link
  would require editing that model.
- Sibling source file, not yet imported and left `todo` in the inventory:
  `thermo_models` `TM-0485`, the parameter-identification model of the same fan
  (identification of the `alpha_i`/`beta_i` factors from catalogue points) —
  a different level of detail, to be imported as a separate model.
- `CSL-0125` *pump_curve_similarity*: pump described by manufacturer curves
  and scaled with the same affinity (similarity) laws, for a liquid and with
  three operating modes (catalogue data instead of dimensionless factors).