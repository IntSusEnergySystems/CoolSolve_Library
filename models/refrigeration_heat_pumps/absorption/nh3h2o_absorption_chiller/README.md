# Single-effect ammonia-water absorption chiller with rectifier

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0249`

The standard single-effect NH3-H2O absorption chiller at one operating point: absorber, solution pump, solution heat
exchanger, generator with a rectifier (dephlegmator), condenser, refrigerant heat exchanger, expansion valves and evaporator.
Ammonia is the refrigerant and water the absorbent. It is the first library model on the EES fluid `NH3H2O`, and shows how the
mixture is used: saturation states (`Q=0`, `Q=1`), flashes at given enthalpy (`P`, `X`, `H`), the composition of a saturated liquid
(`MassFraction`) and the state arrays of the thermodynamic diagrams.

| | |
|---|---|
| **Category** | Cycles and machines › Absorption and sorption |
| **Fluids** | `NH3H2O` (ammonia-water mixture, ammonia mass fraction `x`) |
| **Size** | 112 equations (largest block: 2) |
| **Source** | Written for the library; the cycle layout is the standard single-effect NH3-H2O cycle of the textbooks (see *Source and attribution*) |
| **Authors** | CoolSolve project (S. Quoilin, ISES, University of Liège); drafted with Claude (Anthropic) |
| **License** | MIT |
| **CoolSolve** | 0.3.0 (branch `feat/nh3h2o`) — verified (see verification field) |

## Problem statement

Size the operating point of a 10 kW chiller: evaporator inlet at -10 °C, condenser outlet at 40 °C, absorber outlet at 35 °C,
generator outlet at 120 °C, refrigerant rectified to 0.9995 mass fraction, effectiveness 0.7 for both heat exchangers. Find the
pressures, the compositions of the strong and weak solutions, the circulation ratio, the heat rates of all components and the COP.

## Model

- **Absorber outlet (1)**: saturated strong solution at the low pressure and at `T_abs`; its mass fraction `x[1]` comes from `MassFraction(NH3H2O, T, P, Q=0)`.
- **Pressures**: the high pressure is the bubble pressure of the refrigerant at `T_cd` (saturated liquid at the condenser outlet); the low
  pressure is the bubble pressure of the refrigerant at `T_ev`, the temperature at which the evaporation **starts**.
- **Pump (1→2)**: isentropic enthalpy rise (`P`, `X`, `S` flash) divided by `eta_pump`.
- **Solution heat exchanger (2→3, 4→5)**: effectiveness on the weak-solution side, `T[5] = T[4] - epsilon_SHX (T[4] - T[2])`; the strong solution leaves sub-cooled (checked: `q[3] = -0.001`).
- **Generator and rectifier**: mass and ammonia balances of the two together (strong solution in; refrigerant vapour 8 and weak solution 4 out) give the
  circulation ratio; the weak solution leaves saturated at `T_gen`. The vapour leaving the generator (7) is in equilibrium with it; the
  rectifier cools it to the dew point of the refrigerant (state 8, mass fraction `x_ref`), and its **reflux** (state 9) has the composition and
  temperature of the weak solution, so its flow follows from the mass and ammonia balances around the rectifier. `Q_dot_rect` is the heat it rejects.
- **Condenser (8→10)**, **refrigerant heat exchanger (10→11, 13→14)**: effectiveness on the liquid temperatures relative to the evaporator outlet
  temperature, `T[11] = T[10] - epsilon_RHX (T[10] - T[13])`; **refrigerant valve (11→12)** and **weak-solution valve (5→6)** are isenthalpic (both flash).
- **Evaporator (12→13)**: the evaporation of an ammonia-water refrigerant has a **large temperature glide** (the water accumulates in the liquid):
  at 2.9 bar the refrigerant of 0.9995 starts to boil at -10 °C, is 99 % evaporated at -8.8 °C and is dry only at +8.9 °C (0.998: +20.6 °C).
  The outlet is therefore given by its vapour quality `q_ev` (0.99), the rest being a water-rich liquid that goes to the absorber with the vapour.
- **Absorber**: heat rejected from the enthalpies of the two entering streams and the saturated strong solution leaving.
- **Check**: `E_check` closes the energy balance of the whole cycle (`Q_gen + Q_ev + W_pump - Q_abs - Q_cd - Q_rect`); it is a diagnostic, not an equation of the model.

Inputs: `Q_dot_ev`, `T_ev`, `T_cd`, `T_abs`, `T_gen` (°C), `x_ref`, `q_ev`, `epsilon_SHX`, `epsilon_RHX`, `eta_pump`.
Outputs: `P_low`, `P_high`, state arrays `P[i]`, `T[i]`, `x[i]`, `h[i]`, `s[i]` (i = 1 to 14, state 9 being the reflux), `q[i]` for the states that can be two-phase,
`m_dot[i]`, `Q_dot_gen`, `Q_dot_abs`, `Q_dot_cd`, `Q_dot_rect`, `Q_dot_SHX`, `W_dot_pump`, `f_circ`, `COP`.

## How to run

```bash
coolsolve nh3h2o_absorption_chiller.eescode
```

Default guesses are enough (6 iterations, about 2 s). Properties follow the EES fluid `NH3H2O`: CoolSolve evaluates the IAPWS Guideline G4-01 formulation,
whose results agree with EES (Ibrahim & Klein) within about 1 %, with another reference state for `h`, `s` and `u` (only differences matter in this model).
The model is valid while the weak solution is weaker than the strong one (`x[4] < x[1]`, i.e. `f_circ > 0`): below a generator temperature of about 96 °C
for these conditions the cycle cannot work and the equations give a negative circulation ratio.

## Results

Cooling capacity 10 kW; COP = Q_ev / Q_gen.

| Quantity | Value |
|---|---:|
| Evaporator / condenser pressure | 2.906 bar / 15.545 bar |
| Strong / weak solution mass fraction | 0.4172 / 0.3067 |
| Circulation ratio (kg strong solution per kg refrigerant) | 6.27 |
| Generator, absorber, condenser, rectifier heat | 22.02, 18.65, 9.24, 4.26 kW |
| Solution heat exchanger, pump | 11.95 kW, 129 W |
| **COP** | **0.454** |
| Closure of the energy balance (`E_check`) | -1.9e-11 W |

State points (`h` with the reference state of `NH3H2O`: compare differences):

| # | State | P [bar] | T [°C] | x [kg/kg] | h [kJ/kg] | Phase / quality |
|---|---|---:|---:|---:|---:|---|
| 1 | absorber outlet, saturated strong solution | 2.906 | 35.0 | 0.4172 | 53.8 | saturated liquid |
| 2 | after the pump | 15.545 | 35.3 | 0.4172 | 56.3 | sub-cooled liquid |
| 3 | strong solution after the solution heat exchanger | 15.545 | 84.9 | 0.4172 | 287.5 | sub-cooled liquid |
| 4 | generator outlet, saturated weak solution | 15.545 | 120.0 | 0.3067 | 437.0 | saturated liquid |
| 5 | weak solution after the solution heat exchanger | 15.545 | 60.7 | 0.3067 | 161.9 | sub-cooled liquid |
| 6 | after the weak-solution valve | 2.906 | 57.1 | 0.3067 | 161.9 | 0.011 |
| 7 | generator vapour (saturated, at T_gen) | 15.545 | 120.0 | 0.9034 | 1930.3 | saturated vapour |
| 8 | rectifier outlet, saturated refrigerant vapour | 15.545 | 46.1 | 0.9995 | 1654.2 | saturated vapour |
| 9 | reflux liquid (state of the weak solution) | 15.545 | 120.0 | 0.3067 | 437.0 | saturated liquid |
| 10 | condenser outlet, saturated liquid | 15.545 | 40.0 | 0.9995 | 533.2 | saturated liquid |
| 11 | liquid after the refrigerant heat exchanger | 15.545 | 5.8 | 0.9995 | 370.3 | sub-cooled liquid |
| 12 | after the refrigerant valve | 2.906 | -10.0 | 0.9995 | 370.3 | 0.057 |
| 13 | evaporator outlet (q = q_ev) | 2.906 | -8.8 | 0.9995 | 1583.4 | 0.990 |
| 14 | cold stream after the refrigerant heat exchanger | 2.906 | 54.8 | 0.9995 | 1746.3 | superheated vapour |

Effect of the generator temperature (other inputs unchanged; each run from the default guesses): COP 0.278 (100 °C, circulation ratio 30), 0.433 (110 °C), **0.454 (120 °C)**,
0.440 (130 °C), 0.409 (140 °C); the weak solution goes from 0.397 to 0.222 and the circulation ratio from 30 to 4.0.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve, saved in figures/, e.g.  ![P-h diagram of the cycle](figures/nh3h2o_absorption_chiller_ph.png)  + one-line caption -->

## Verification

There is no reference solution to compare with (the model is new and EES's own NH3H2O is another formulation), so the checks are internal and physical:
the mass and ammonia balances of the generator-rectifier and of the absorber hold by construction (the circulation ratio comes from them); the **energy balance of the whole
cycle closes to 2e-11 W** on 22 kW of heat (`E_check`), which tests all the enthalpy evaluations of the 14 states together; the two-phase states (6, 12, 13)
come out with qualities in [0, 1] and the single-phase ones are labelled sub-cooled/superheated by the property model. The COP of 0.45 and the circulation ratio of 6 are
plausible for a single-effect NH3-H2O chiller at these temperatures (thermal COPs of 0.4 to 0.6 are usually quoted for such cycles); the trend with the generator temperature has the expected maximum.
The property model itself is verified in CoolSolve against the verification tables of IAPWS G4-01 (`docs/nh3h2o_review.md` of CoolSolve).

## Source and attribution

Original model written for the CoolSolve Library by the CoolSolve project (S. Quoilin, ISES, University of Liège), drafted with Claude (Anthropic); licence MIT.
The cycle layout is the one of the standard single-effect NH3-H2O absorption chiller with rectifier, solution heat exchanger and refrigerant heat exchanger described in
textbooks, e.g. K. E. Herold, R. Radermacher, S. A. Klein, *Absorption Chillers and Heat Pumps*, CRC Press, 1996; the operating point and the simplifications
(reflux with the weak-solution state, effectivenesses on temperatures, evaporator outlet by quality) are choices of this model, not values taken from the book.
Properties: IAPWS Guideline G4-01 (2001), the formulation of R. Tillner-Roth and D. G. Friend, *J. Phys. Chem. Ref. Data* 27 (1998) 63, evaluated by CoolSolve (fluid `NH3H2O`).

## Conversion log
- **2026-10-18 — added**: written directly in EES syntax for CoolSolve (not a translation); state points as arrays for the diagrams; quality variables of the two-phase states; no `$UnitSystem`.
- **Level**: equations 112 (1) + largest block 2 (0) + arrays (1) + three or more coupled components (1) + no calibration/off-design (0) + default guesses suffice (0) = 3 → level 2.

## Limitations and CoolSolve gaps

- One operating point; no part load, no sizing of the exchangers; the rectifier is an equilibrium device with the reflux in the weak-solution state; the pump heat and the pressure drops are neglected; the water-rich liquid leaving the evaporator is not drained.
- Valid only for `x[4] < x[1]` (see *How to run*); the model does not stop when it is violated.
- The transport properties of `NH3H2O` (conductivity, viscosity, surface tension) are not implemented in CoolSolve; this model does not need them.
- No gap blocks the model.

## Related models

- `CSL-0043` (LiBr-water absorption chiller with a solution heat exchanger): the same cycle family with the other working pair (LiBr-H2O, no rectifier).
