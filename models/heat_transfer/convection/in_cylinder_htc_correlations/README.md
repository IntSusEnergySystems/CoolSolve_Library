# In-cylinder heat-transfer correlations for reciprocating machines

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0086`

Seven Nusselt-number correlations for the gas side of the cylinder wall of a
reciprocating compressor, expander or engine, translated from the ThermoCycle
Modelica library: Annand (1963), Woschni (1967), Adair (1972), Destoop (1986),
Gnielinski (2010), Irimescu (2013) and the gas-spring correlation of
Kornhauser (1994). Each correlation returns the Nusselt number; the
heat-transfer coefficient follows from `h = Nu*lambda/Gamma` with the
characteristic length of that correlation (bore, equivalent diameter `6V/A` or
hydraulic diameter `4V/A`) and is evaluated in the demonstration program.
Geometry, kinematics and transport properties are **arguments**, so the library
calls no property function and works with any gas (the inventory row says
*any gas: needs viscosity, conductivity, Prandtl number, density*). They are
the first in-cylinder correlations of the library: `CSL-0024` and the engine
candidates of `thermo_models` use a constant wall coefficient instead.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (properties are arguments; the demonstration uses air properties of CoolProp 8.0.0) |
| **Size** | 86 equations after analysis (largest block: 1); 14 `FUNCTION`s |
| **Source** | ThermoCycle Modelica library, `ThermoCycle/Components/Units/ExpansionAndCompressionMachines/Reciprocating/HeatTransfer/*.mo` and `…/BaseClasses/PartialCylinderHeatTransfer.mo`, commit `b4f16c0b` (2019-03-20), MIT — <https://github.com/thermocycle/Thermocycle-library>; inventory row `THC-005` |
| **Authors** | Jorrit Wronski (DTU Mechanical Engineering, 2013 — implementation); the correlation authors are credited in the comment block of each function |
| **License** | MIT (see *Source and attribution* for the DTU notice in the reciprocating package) |
| **CoolSolve** | 0.3.0@536d427 — **verified** against an independent Python re-evaluation (66 values, max. 7.13·10⁻¹²) |

## Problem statement

A piston machine exchanges heat with its wall at every crank angle, and the
instantaneous heat-transfer coefficient of the in-cylinder gas decides how much
of the compression work comes back as heat. The empirical correlations of the
literature all have the form `Nu = a·Re^b·Pr^c` (or a pipe equation) with a
correlation-specific characteristic length and velocity, so they translate
cleanly into a small function library: given the gas state, the geometry and
the kinematics of the crank, return Nu and h.

## Model

### Correlations

| EES `FUNCTION` | Equation | Characteristic quantities |
|---|---|---|
| `Nu_Annand_1963` | Nu = 0.575·Re⁰·⁷ | Λ = c_m (mean piston speed), Γ = bore |
| `Nu_Woschni_1967` | Nu = 0.035·Re⁰·⁸ | Λ = 2.28·c_m, Γ = bore (compression phase only) |
| `Nu_Adair_1972` | Nu = 0.053·Re⁰·⁸·Pr⁰·⁶ | Λ = 0.5·De·ω_g, Γ = De = 6V/A |
| `Nu_Destoop_1986` | Nu = 0.6·Re⁰·⁸·Pr⁰·⁶ | Λ = c_m, Γ = bore |
| `Nu_Gnielinski_2010` | Nu = (ζ/8)·Re·Pr·[1+12.7√(ζ/8)·(Pr²ᐟ³−1)]⁻¹·[1+DL²ᐟ³] | ζ = (1.80·log₁₀Re − 1.50)⁻², Λ = c_m, Γ = D = bore, L = clearance |
| `Nu_Irimescu_2013` | same with (Re − 1000) and the factor K | ζ = (1.82·log₁₀Re − 1.64)⁻², K = (μ/μ_w)⁰·¹⁴, Λ = c_c (current piston speed), Γ = D = bore |
| `Nu_Kornhauser_1994` | Nu = 0.56·Pe⁰·⁶⁹ | Pe = ω_c/(2π)·D_h²/(4·α_f), Γ = D_h = 4V/A |

`Re = ρ·Λ·Γ/μ` for the first six, with the Λ and Γ of the table; `DL = D/L`
with `L` the clearance of the cylinder (see the conversion log).
`h = Nu·λ/Γ` in every case.

### Geometry and kinematics helpers

| EES `FUNCTION` | Equation | Original |
|---|---|---|
| `PistonSpeed(stroke, omega)` | c = ω·stroke/(2π) [m/s] | `c_m = omega_m/(2π)·stroke`, `c_c = omega_c/(2π)·stroke` |
| `CylinderVolume(A_p, position)` | V = A_p·position [m³] | `Kornhauser1994.mo` |
| `HydraulicDiameter(A_p, position)` | D_h = 4V/A_p = 4·position [m] | `Kornhauser1994.mo` ("Hydraulic diameter") |
| `EquivalentDiameter(A_p, position)` | De = 6V/A_p = 6·position [m] | `Adair1972.mo` ("Equivalent diameter 6V/A") |
| `CylinderWallArea(A_p, position)` | A = A_p + 2√(A_p·π)·position [m²] | `PartialCylinderHeatTransfer.mo` (piston face + bore·π·clearance) |
| `TransitionFactor(start, stop, position)` | smooth 0→1 switch, order 2 | `Functions/transition_factor.mo` (Richter 2008, p. 68) |
| `AdairSwirlVelocity(omega_c, theta)` | ω_g = (1 − 0.5·t)·2·N·(1.04 + cos 2θ) [rad/s], N = ω_c/(2π) | `Adair1972.mo`, eq. 15 of the paper with the smooth transition of the library |

### Demonstration program

One machine — bore 0.05 m, stroke 0.04 m, 3000 rev/min (c_m = c_c = 2 m/s) —
evaluated at two crank-angle states; the transport properties of the gas are
inputs taken from CoolProp 8.0.0 (air):

| Input | State A | State B |
|---|---:|---:|
| crankshaft angle θ | 60° | 90° (mid-stroke) |
| clearance `position` | 0.015 m | 0.025 m |
| gas T / p | 80 °C / 3 bar | 150 °C / 10 bar |
| wall T | 60 °C | 120 °C |
| ρ, μ, μ_w, λ, c_p | 2.9591 kg/m³, 2.1034·10⁻⁵ / 2.0126·10⁻⁵ Pa·s, 0.030278 W/(m·K), 1011.59 J/(kg·K) | 8.2128 kg/m³, 2.4129·10⁻⁵ / 2.2872·10⁻⁵ Pa·s, 0.035201 W/(m·K), 1023.41 J/(kg·K) |

State B sits exactly in the middle of the Adair transition interval around
90°, so its transition factor is 0.5 and both branches of the swirl equation
are exercised (state A: factor 0, branch `2N(1.04+cos2θ)`).

## How to run

Open `in_cylinder_htc_correlations.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./in_cylinder_htc_correlations.eescode
```

Every equation is explicit: `Solver: SUCCESS (0 iterations)`, no `.initials`
needed. The solved file is the regression baseline
(`in_cylinder_htc_correlations.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0086 ---}` and
lists `CSL-0086` in its `related` field.

## Results

Values of the demonstration program (full precision in
`in_cylinder_htc_correlations.sol`):

| Quantity | State A | State B |
|---|---:|---:|
| cylinder volume V [m³] | 2.9452·10⁻⁵ | 4.9087·10⁻⁵ |
| hydraulic diameter D_h [m] | 0.06 | 0.10 |
| equivalent diameter De [m] | 0.09 | 0.15 |
| wall area A_w [m²] | 4.3197·10⁻³ | 5.8905·10⁻³ |
| Pr [−] | 0.70277 | 0.70152 |
| swirl velocity ω_g [rad/s] | 54 | 3 |
| Adair transition factor [−] | 0 | 0.5 |
| Re (Λ = c_m) [−] | 14 068 | 34 036 |
| Re (Woschni, Λ = 2.28 c_m) [−] | 32 075 | 77 603 |
| Re (Adair) [−] | 30 767 | 11 487 |
| Pe (Kornhauser) [−] | 4 449 | 29 847 |
| K (Irimescu viscosity ratio) [−] | 1.00620 | 1.00752 |
| `Nu_Annand` [−] / h [W/(m²·K)] | 460.7 / 279.0 | 855.1 / 602.0 |
| `Nu_Woschni` [−] / h [W/(m²·K)] | 140.9 / 85.34 | 285.7 / 201.2 |
| `Nu_Adair` [−] / h [W/(m²·K)] | 167.0 / 56.20 | 75.87 / 17.80 |
| `Nu_Destoop` [−] / h [W/(m²·K)] | 1011 / 612.3 | 2048 / 1442 |
| `Nu_Gnielinski` [−] / h [W/(m²·K)] | 133.2 / 80.64 | 203.1 / 143.0 |
| `Nu_Irimescu` [−] / h [W/(m²·K)] | 127.1 / 76.97 | 201.8 / 142.1 |
| `Nu_Kornhauser` [−] / h [W/(m²·K)] | 184.3 / 93.00 | 685.3 / 241.2 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the seven
     correlations over a crank-angle or Reynolds sweep, e.g. h vs Re at the
     two demo states, figures/in_cylinder_htc_correlations_h_re.png -->

`h_Adair_B` is small because the swirl equation of Adair collapses at 90°
(`1.04 + cos 180° = 0.04`, so ω_g = 3 rad/s): the value follows the equation
as transcribed in the `.mo` file, no meaning is added here.

## Verification

**Reference: independent Python re-evaluation of the equations.** ThermoCycle
stores no reference results (its test models are dynamic drivers without
asserted values, and OpenModelica/Dymola are not installed here), so a
throw-away script under `work/in_cylinder_htc/` (deleted when the card was
closed) re-implemented the seven correlations and the geometry/kinematics
helpers directly from the `.mo` sources (`math` only, Python 3), used the same
property inputs — air properties of
**CoolProp 8.0.0**, the property backend CoolSolve uses, evaluated at the
states of the table — and wrote a `name,value` CSV compared with the solved
file:

```text
66 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 20
```

The largest relative deviation over the 66 common variables is **7.13e-12**
(`Pe_B`), i.e. round-off in the double-precision evaluation. The 20 variables
only in CoolSolve are the demo inputs of the two states (`T_A`, `T_B`,
`T_w_A`, `T_w_B`, `p_A`, `p_B`, `position_A`, `position_B`, `theta_A`,
`theta_B`, `rho_*`, `mu_*`, `mu_w_*`, `k_*`, `cp_*`) — the reference table
holds the 66 outputs and machine constants.

**Cross-check against the papers** (secondary/open sources, coefficients only):

- Woschni: `Nu = 0.035·Re^0.8` with the compression-phase gas velocity
  `U = 2.28·U_piston` and the bore as characteristic length — the form quoted
  for SAE 670931 (1967) on the Colorado State University heat-transfer lecture
  page <https://www.engr.colostate.edu/~allan/heat_trans/page7a/page7a.html>.
- Adair: the open-access paper
  <https://docs.lib.purdue.edu/icec/45/> gives eq. 15 with the two
  `2ω[1.04 + cos 2θ]` branches over π/2 and 3π/2, the equivalent diameter
  `De = 6·Volume/Area`, the Reynolds number on `De` and the mean piston speed
  (its equation OCR is not legible enough to re-check the branch factors
  themselves — see the open question below).
- The friction factor of `Nu_Irimescu_2013`, `(1.82·log₁₀Re − 1.64)⁻²`, is the
  Petukhov smooth-pipe formula used together with the Gnielinski denominator;
  `Nu_Gnielinski_2010` uses the variant `(1.80·log₁₀Re − 1.50)⁻²` of its
  source file.

Sanity checks: every `h` is positive and spans 17.8 … 1442 W/(m²·K) across the
two states, the order of magnitude reported for in-cylinder convection (the
smallest value is the Adair mid-stroke case above); the Reynolds numbers
(1.1·10⁴ … 7.8·10⁴) lie in the turbulent range the Gnielinski forms assume and
the Peclet numbers (4.4·10³, 3.0·10⁴) are above the `Pe > 10` asserted by the
source; and `tf_A = 0`, `tf_B = 0.5` are the exact values of the transition
factor outside and at the centre of its interval.

## Source and attribution

```text
This CoolSolve model is a translation (EES-compatible language, equation-oriented) of
the in-cylinder heat-transfer correlations from the ThermoCycle Modelica library, files
ThermoCycle/Components/Units/ExpansionAndCompressionMachines/Reciprocating/HeatTransfer/
{Annand1963,Woschni1967,Adair1972,Destoop1986,Gnielinski2010,Irimescu2013,Kornhauser1994,
Kornhauser1994Full,GnielinskiHeatTransfer,RePrHeatTransfer}.mo, …/BaseClasses/
PartialCylinderHeatTransfer.mo and ThermoCycle/Functions/transition_factor.mo,
commit b4f16c0b.
ThermoCycle - https://github.com/thermocycle/Thermocycle-library
Copyright (c) 2018 Thermodynamics Laboratory (University of Liege), MIT License.
Original authors: J. Wronski (DTU Mechanical Engineering, 2013 — implementation, see the
git history of the files); S. Quoilin, A. Desideri, I. Bell (library).
Changes: translated from Modelica to CoolSolve; der() terms set to zero (steady state);
smooth() and regularisation wrappers of the dynamic solver removed; dead code dropped
(see the conversion log).
Scientific basis: Annand 1963, Woschni 1967 (SAE 670931), Adair et al. 1972,
Destoop 1986, Gnielinski 1976/2010, Irimescu 2013, Kornhauser & Smith 1994 — cited in
the comment block of each function.
```

Source (local clone of the public repository):
`~/git/Thermocycle-library/ThermoCycle/Components/Units/ExpansionAndCompressionMachines/Reciprocating/HeatTransfer/…`,
inventory candidate `THC-005`.

**DTU notice (checked as the card asked):** the reciprocating-machine package
of ThermoCycle carries "Copyright (c) 2011-2013 Technical University of
Denmark, DTU Mechanical Engineering … Modelica License 2, main contributor
Jorrit Wronski", while the repository `LICENSE` is MIT (2018, Thermodynamics
Laboratory, University of Liège). It is the only third-party copyright of the
library and it concerns this row; the maintainer's decision recorded in
`sources/thermocycle/README.md` §1 is `license_status = open:MIT` with credit
to J. Wronski as for any translated model. **Open question for the maintainer:**
confirm with J. Wronski that the translation of these files may be published
under the library MIT licence.

## Conversion log

- **2026-10-06 — translation** (card C-93, `T-FUNC`): the fourteen `.mo` files
  of row `THC-005` translated to EES. Units already SI; no `$UnitSystem`, no
  property conversion. One EES `FUNCTION` per correlation returning Nu, plus
  seven geometry/kinematics helpers; the demonstration program assembles each
  correlation exactly as the Modelica model does (its `Lambda`/`Gamma` per
  correlation, `Re`, `Pr`, `Pe`, then `h = Nu·λ/Γ`).
- **Steady state.** `PartialCylinderHeatTransfer.mo` contains `omega_c =
  der(crankshaftAngle)` and, for `time > 0`, `omega_m = crankshaftAngle/time`
  (initialisation hack of the dynamic solver). The functions take the angular
  speeds as **arguments**; the demonstration uses the constant-speed case
  `omega_m = omega_c`, which is what the original sets at constant speed. The
  `initialize`/`HTC_gain` initialisation switch (gain 10⁵ or 10⁻⁵ for a few
  hundredths of a second) and the `assert`s of the Modelica files are dropped:
  they only serve the dynamic solver. `Kornhauser1994Full` is **not**
  translated: its extra term `Nu_i/ω_c·der(T_s)/(T_s − T_wall)` is a derivative
  and vanishes at steady state, leaving exactly `Nu_Kornhauser_1994`.
- **Regularisation removed.** `Modelica.Fluid.Utilities.regPow(Re,b)` and the
  `smooth(5, …)` wrapper of `transition_factor` are replaced by the plain power
  and by the order-2 formula (rule 1 of `sources/thermocycle/README.md` §7).
  The Adair regime switch stays a smooth blend, as in the original.
- **Dead code removed.** `Adair1972.mo` computes `thetaCorr` from the
  `inletTDC` parameter in an `algorithm` section and never uses it, so the
  parameter has no effect on the result: the flag is dropped (no equation
  changes). `GnielinskiHeatTransfer`'s unused `xtra`/`K` comments and the
  commented-out alternatives of the `.mo` files are not transcribed.
- **`L` of the entry factor.** `GnielinskiHeatTransfer` adds a second equation
  for `surfaceAreas[i] = A_p + 2√(A_p·π)·L[i]` on top of the one of
  `PartialCylinderHeatTransfer` (with `position[i]`); the two together give
  `L[i] = position[i]`, so the demonstration passes `DL = bore/position`
  ("clearance length", source comment). The entry factor is kept in both
  Gnielinski/Irimescu functions, as in the original.
- **Angles.** The original works in rad (EES trigonometry is in degrees):
  `theta` stays in rad and `AdairSwirlVelocity` converts `2·theta` to degrees
  inside its `COS`; the transition intervals are written `π/2 ± 0.025π` =
  `deltaTheta = 0.05π` rad = 9° (source comment).
- **Case-insensitive names.** The first draft named the transition factor
  `t_A` and the Irimescu viscosity ratio `K_A`, which collide with the gas
  temperature `T_A` and the conductivity `k_A` in the case-insensitive EES
  symbol table (they were silently merged: *System square: No*, 86 equations /
  82 unknowns). They are now `tf_A`/`tf_B` and `kappa_A`/`kappa_B`.
- **Source defects checked** (`sources/thermocycle/README.md` §8): the
  copy-pasted reference of `Destoop1986.mo` (it cites Annand 1963 instead of
  Destoop 1986) is recorded in the function comment; no Destoop reference is
  identified in the library. None of the other listed defects (`Eps_t[N]`,
  `ORCNext`, the Therminol density, …) touches this row.
- **Level**: 86 equations → 1; largest block 1 → 0; functions present → 1;
  no multi-zone/discretised structure → 0; semi-empirical, crank-angle
  correlations → 1; no curated guesses → 0. Score 3 → **level 2**.

## Limitations and CoolSolve gaps

- These are the **simplified** versions of the papers, as the source says:
  Woschni without the combustion and scavenging terms (compression phase
  only), Annand without its radiation term, Irimescu with the piston speed as
  characteristic velocity instead of the turbulence-based velocity of the
  paper, Adair with the smooth blend of the library instead of the paper's
  if-clause. The validity ranges of the papers are not reproduced by the
  source and are not checked by the functions.
- `Nu_Destoop_1986` has no traceable reference (source defect above); the
  function quotes what the `.mo` file contains.
- The two demo states are illustrative; the numbers of the *Results* table are
  a check of the **equations**, not recommended design values. State B lies on
  the Adair branch boundary, where the swirl equation nearly vanishes.
- No gap is registered for this card: everything is plain EES (`FUNCTION`,
  `IF/THEN/ELSE`, `LN`, `LOG10`, `SQRT`, `COS`) and runs in CoolSolve
  v0.3.0@536d427 — `missing_features` is empty.
- **Open question** (not a gap): the branch factors of Adair eq. 15 could not
  be re-read from the OCR of the open-access paper; the translation follows
  the transcription in `Adair1972.mo` (factor 1 before/after the middle
  interval, ½ inside).

## Related models

- `CSL-0024` *single_cylinder_engine_weibe*: a single-cylinder engine that
  uses a constant wall coefficient (U_w = 500 W/(m²·K)) instead of one of
  these correlations — the natural place to plug a library function in.
- `CSL-0087` *internal_turbulent_nusselt*: the pipe-flow Nusselt library the
  Gnielinski/Irimescu equations of this model belong to.
- `CSL-0084` *orc_expander_pump_empirical_maps*: the other ThermoCycle
  function library of this batch (same source, same translation rules).
