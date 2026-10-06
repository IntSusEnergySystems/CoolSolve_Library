# Supercritical CO2 ORC with polynomial compressor and turbine performance maps

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ☑️ **Runs** &nbsp;|&nbsp; `CSL-0038`

Closed CO2 (R744) vapour power cycle of the supercritical/transcritical ORC
family: water-cooled cooler, compressor, recuperator, solar air-CO2 heater,
turbine and three pipes with pressure and temperature losses. The compressor
and the turbine are described by the **polynomial fits of their performance
maps** (mass flow and enthalpy rise as coordinates, efficiency and speed as
outputs) instead of a physical correlation, and the machine speed is imposed,
so that the maps close the cycle: the CO2 mass flow rate and the turbine exhaust
pressure are results of the system. Useful for a first sizing of a supercritical
CO2 power cycle and as a template for map-based turbomachinery in EES/CoolSolve.

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R744 (CO2, real gas, CoolProp properties); Water (cooling water) |
| **Size** | 144 equations (largest block: 28) |
| **Source** | CoolSolve example [`examples/orc_co2.eescode`](https://github.com/CoolProp/CoolSolve/blob/main/examples/orc_co2.eescode) (ULiège Thermodynamics Laboratory, MIT); **no EES original of this model is known** (see *Verification*) |
| **Authors** | S. Quoilin (ULiège Thermodynamics Laboratory) — probable, to be confirmed by the maintainer (the file carries no author tag) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; reproduces the stored solution of the example to 1.5·10⁻⁷ (no independent reference available) |

## Problem statement

A closed CO2 cycle operating above the critical pressure of CO2
(7.377 MPa) is driven by a compressor and a turbine whose performance maps are
given as polynomials:

- compressor: $\eta_s$ and the speed are polynomial functions of two map
  coordinates, the mass flow `md` and the isentropic enthalpy rise `Dh`
  (coefficients `p00…p50` for $\eta_s$, `k00…k02` for the speed);
- turbine: same structure with the enthalpy-rise coordinate `Dh_turb`
  (coefficients `t00…t03` for the speed, `e00…e05` for $\eta_t$).

Both machines run at the **imposed speed of 75 000 rpm**. Because the speed is
the same variable in the two maps, the maps impose the compressor mass flow
rate `m_dot` and the turbine exhaust pressure `P[7]` (hence the compressor
discharge pressure `P_ex`): they are unknowns of the algebraic system, together
with the CO2 temperature `T[3]` after the recuperator and the conductance `AU`
of the cooler.

Heat is supplied by a solar air-CO2 heater (`DELTAT_sun` = 150 K on the CO2
side, constant air flow rate) and rejected to cooling water in a
counterflow cooler (`DELTAT_cool` = 25 K drop on the CO2 side, water at 15 °C).

## Model

State points of the loop (SI, °C / Pa / J, fluid R744):

| | component | equations |
|---|---|---|
| 9 → 1 | cooler (CO2-water, counterflow) | `P[1]=P[9]`, `T[9]-T[1]=DELTAT_cool`, ε-NTU model of the water side, `Q_dot_cool` from both the CO2 energy balance and the effectiveness model (the second definition closes the cooler and gives `AU`) |
| 1 → 2 | compressor | `s_is=s[1]`, `P_ex=P[2]`, `h_is=h(s_is,P_ex)`, $\eta_s=(h_{is}-h_1)/(h_2-h_1)$, `h[2]=h(h[2],P[2])`, and the map $\eta_s=f_{p}(md,Dh)$ + speed map $RPM=g_k(md,Dh)=75\,000$ |
| 2 → 3, 8 → 9 | recuperator (CO2-CO2, counterflow) | no pressure loss, `h[3]-h[2]=h[8]-h[9]` (heat given by the hot side = heat received by the cold side) |
| 3 → 4, 5 → 6, 7 → 8 | pipes | `P_next = xsi*P` with `xsi` = 0.97, temperature loss `DELTAT_loss` = 2 K (**see the sign inconsistency in the conversion log**) |
| 4 → 5 | solar heater (air-CO2) | constant CO2 pressure, `T[5]-T[4]=DELTAT_sun` |
| 6 → 7 | turbine | `h_is_t=h(P[7],s[6])`, $\eta_t=(h_6-h_7)/(h_6-h_{is,t})$, and the map $\eta_t=f_e(md,Dh_{turb})$ + speed map $RPM=g_t(md,Dh_{turb})=75\,000$ |
| — | closure | dummy state 10 = state 1 |

The map coordinates are built with the conversion constants of the original
(`Dh = DELTAh/1055.056*0.45359237`, `md = m_dot/0.45359237`); their physical
units are not documented in the original and are kept unchanged.

A post-processing block at the end of the file gives the net power, the heat of
the solar heater, the net heat received through the pipes, the cycle
efficiency and the energy balance of the cycle; it does not change any other
result. The state points are stored in the arrays `P[i]`, `h[i]`, `T[i]`,
`s[i]` (i = 1…10) and can be drawn directly with the *Overlay array path*
option of the CoolSolve *Diagram* tab (P-h diagram: X = `h`, Y = `P`,
*Close loop* ticked).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `p_su` CO2 supply pressure | 7.687 MPa | `m_dot` CO2 mass flow | 2.270 kg/s |
| `T_su` CO2 supply temperature | 32.22 °C | `W_dot` compressor power | 23.42 kW |
| `RPM` speed of both machines | 75 000 rpm | `W_dot_t` turbine power | 117.5 kW |
| `DELTAT_sun` heater temperature rise | 150 K | `W_dot_net` net power | 94.08 kW |
| `DELTAT_cool` cooler temperature drop | 25 K | `eta_cycle` cycle efficiency | 22.1 % |
| `DELTAT_loss[3]`, `[5]`, `[7]` pipe losses | 2 K | `Q_dot_cool` cooling power | 332.2 kW |
| `xsi` pipe pressure-loss factor | 0.97 | `Q_dot_sun` heat of the heater | 419.1 kW |
| `m_dot_H2O` cooling-water flow | 3 kg/s | `eta_s` / `eta_t` isentropic efficiencies | 0.624 / 0.882 |
| `T_H2O_in` cooling-water inlet temperature | 15 °C | `r_p` compressor pressure ratio | 1.515 |
| polynomial coefficients | 21 + 6 + 10 + 21 | `epsilon` cooler effectiveness / `AU` | 0.626 / 562.4 W/K |

## How to run

```bash
coolsolve ./orc_co2_polynomial_maps.eescode
```

The file **`orc_co2_polynomial_maps.initials` is required**: without it the
largest algebraic block (28 variables, the heater-expander-recuperator part)
is singular and the solve fails (`SingularJacobian`, block 77). This is the
behaviour announced in the header of the original example ("this model requires
the .initials file for reliable convergence"); the shipped initials hold a
converged solution of the model and are used as guesses. No variant and no
`coolsolve.conf` are needed.

## Results

| State | Description | P [MPa] | T [°C] | h [kJ/kg] | s [kJ/(kg·K)] |
|---:|---|---:|---:|---:|---:|
| 1 | cooler outlet / compressor supply | 7.688 | 32.22 | 310.9 | 1.3618 |
| 2 | compressor exhaust | 11.648 | 45.80 | 321.3 | 1.3740 |
| 3 | recuperator cold-side outlet | 11.648 | 542.50 | 1032.4 | 2.8423 |
| 4 | solar heater inlet | 11.299 | 540.50 | 1030.3 | 2.8456 |
| 5 | solar heater outlet | 11.299 | 690.50 | 1215.0 | 3.0538 |
| 6 | turbine inlet | 10.960 | 692.50 | 1217.6 | 3.0624 |
| 7 | turbine exhaust | 7.925 | 649.43 | 1165.9 | 3.0700 |
| 8 | recuperator hot-side inlet | 7.688 | 651.43 | 1168.5 | 3.0786 |
| 9 | cooler inlet | 7.688 | 57.22 | 457.3 | 1.8321 |

Powers: 23.42 kW absorbed by the compressor, 117.5 kW produced by the turbine,
**94.08 kW net**; 332.2 kW rejected in the cooler, 419.1 kW received from the
solar heater and 7.13 kW net through the pipes; cycle efficiency 22.1 %.
The mass flow rate (2.270 kg/s) and the turbine exhaust pressure (7.93 MPa) are
the outcomes of the speed constraint of the maps, and the pressure ratio stays
close to 1.5 because the imposed speed is far from the optimum of the map at
this enthalpy rise.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of
     the cycle, saved as figures/orc_co2_polynomial_maps_ph.png
     (Diagram tab, fluid R744, "Array overlay" with P[i] and h[i], "Close loop") -->

## Verification

**No independent reference exists for this model.** It is a CoolSolve example
whose original `.EES` file is not in `CoolSolve/misc/EES_ok.zip` (the archive
holds `orc_simple`, `orc_complex`, `orc_extraction`, `orc_r245fa`,
`orc_ammonia` and `orc_solar_complex`, none of them on CO2), and the ULiège
collection (`~/Nextcloud/thermo_models`, inventoried in
`~/git/CoolSolve_Library/sources/thermo_models/inventory.csv`) contains no
transcritical/supercritical CO2 exercise. The status is therefore *runs* (not
*verified*) and the checks are:

1. **Reproduction of the stored solution of the example.** The file
   `examples/orc_co2.initials` of the CoolSolve repository holds a converged
   solution of the example (it agrees with the example's own `.sol` to 8
   digits). `compare_solution.py` on it prints
   *"140 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
   CoolSolve: 5"* — the five extra variables are the post-processing outputs of
   the library model. Run with `--rtol 1e-12`, the largest relative deviation is
   **1.48·10⁻⁷ on `NTU`** (12-digit round-off in the stored values).
   This is a regression check against the same tool, not a verification against
   an independent implementation. The enthalpy and entropy values carry
   CoolProp's reference state for R744 (no EES reference to compare with).
2. **Energy balance of the cycle.** The post-processing variable `balance`
   (`Q_dot_sun + Q_dot_pipe + W_dot - Q_dot_cool - W_dot_t`) closes to
   −5.4·10⁻¹⁰ W, i.e. 1.3·10⁻¹⁵ of the 426 kW exchanged.
3. **Physical ranges.** $\eta_s$ = 0.624, $\eta_t$ = 0.882 and the cooler
   effectiveness 0.626 lie in (0, 1); all pressures (7.69 to 11.65 MPa) are
   above the critical pressure of CO2 (7.377 MPa), so the working fluid is
   supercritical at every state point and crosses no phase boundary; the
   recuperator heats the cold side (T[3] > T[2]) with the exhaust gas
   (T[8] = 651 °C > T[9] = 57 °C).

## Source and attribution

- Model file: `~/git/CoolSolve/examples/orc_co2.eescode` (CoolSolve examples,
  MIT), with its guesses `~/git/CoolSolve/examples/orc_co2.initials`; the
  example stays in the CoolSolve repository (inventory row `CSX-028`, decision
  `added` → `CSL-0038`).
- No EES original is known (see *Verification*), so the file is imported from
  the example itself; no unit conversion was needed (the file is already in
  SI-°C-Pa-J, without a `$UnitSystem` directive).
- Authors: the file carries no author tag. The CoolSolve examples inventory
  lists "S. Quoilin / ULiège Thermodynamics Laboratory (CoolSolve examples)" as
  the source of `examples/orc_co2.eescode`; to be confirmed by the maintainer.

## Conversion log

- **2026-10-05 — import**: from `~/git/CoolSolve/examples/orc_co2.eescode`
  (CoolSolve example, already in SI-°C-Pa-J: nothing to convert, no
  `$UnitSystem` directive). Standard header added; section titles renamed with
  the `"!…"` display form and the two identical `"Power"` titles split into
  `!Compressor power` and `!Turbine power`; comments translated to English from
  the French of the original ("isentropique", "pertes de charges",
  "Apport solaire (air-C02)", "calcul du cp moyen", "DETLAT de 25K") and every
  dimensional quantity given its SI unit in the trailing comment. The commented
  `m_dot=2` of the example was *not* restored: the mass flow rate is an unknown
  of the system (the maps impose the speed), and the commented `P_ex=140E5` is
  replaced by a note that the discharge pressure comes from the maps. Results
  unchanged (140/140 variables of the example reproduced).
- **2026-10-05 — dead code removed** (no effect on the results): the
  `parameter Real gamma`, `parameter Real gamma_inlet` declarations and the
  commented block `{gamma …}` (`v[1]`, `v[2]`, `cp[1..2]`, `cv[1..2]`,
  `gamma[1..2]`, the polytropic relation `P[1]*v[1]^gamma=P[2]*v[2]^gamma`),
  the commented alternative closure `{T[3]-T[2]=T[8]-T[9]}` of the recuperator,
  the commented alternative pipe losses `{DELTAT_loss[3]=15;}`,
  `{DELTAT_loss[5]=10}`, `{DELTAT_loss[7]=3}`, the commented guesses
  `{md=8, Dh=4.1}` and the commented cooler area `{AU=4200}`. The equation
  `eta_t=(h[6]-h[7])/(h[6]-h_is_t);` lost its redundant final `;`, which
  CoolSolve accepts in a comment (see *Limitations*).
- **2026-10-05 — sign inconsistency of the pipe model kept as in the original**:
  the pipe 3-4 **cools** the CO2 (`T[4]=T[3]-DELTAT_loss[3]`, −2126 J/kg) while
  the pipes 5-6 and 7-8 **heat** it (`T[6]-T[5]=DELTAT_loss[5]`,
  `T[8]-T[7]=DELTAT_loss[7]`, +2660 and +2608 J/kg). This is most probably a
  sign typo of the original, but it is not corrected here: there is no
  independent reference against which the impact could be checked. The net heat
  received by the CO2 through the pipes is therefore +7.13 kW (`Q_dot_pipe`),
  the cycle efficiency is computed as `W_dot_net/(Q_dot_sun+Q_dot_pipe)` and the
  energy balance closes with that term. Correcting the two signs would cool the
  CO2 instead of heating it and change all the results of the map-constrained
  system (the mass flow rate and the pressures are unknowns).
- **2026-10-05 — post-processing block added**: `W_dot_net`, `Q_dot_sun`,
  `Q_dot_pipe`, `eta_cycle` and `balance` (energy balance, must be 0). The state
  points were already stored in the arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` of the
  original, so no diagram block had to be added; the closing comment lists the
  state numbering for the *Diagram* tab. No other result changes.
- **Level**: 144 equations → 1; largest algebraic block 28 → 1; arrays → 1;
  more than three coupled components (cooler, compressor, two recuperator
  sides, heater, turbine, three pipes) → 1; semi-empirical (fitted) component
  maps → 1; curated guesses required (`.initials`) → 1. Score 6 → level 3.

## Limitations and CoolSolve gaps

- No registered CoolSolve gap blocks this model (`missing_features` is empty);
  it runs natively in CoolSolve v0.3.0.
- The `.initials` file is required (no guess → singular Jacobian); this is a
  property of the model (largest block of 28 variables), not of CoolSolve.
- The polynomial maps are *fitted* correlations: their validity range is the
  range of the data they were fitted on, which is not documented in the
  original. Outside it, the coefficients (which reach 5th order) can give
  efficiencies outside (0, 1).
- The physical meaning/units of the two map coordinates (`md`, `Dh`) are not
  documented in the original; only the numerical conversion constants are kept.
- Unregistered CoolSolve observation (no EES-file evidence, so not registered as
  a gap): a `"comment"` placed **after** a `;`-terminated equation on the same
  line is a parse error ("Could not parse segment: …"), because the line is
  split on `;` before the comment is stripped. `a = 1;  "x"` fails while
  `a = 1  "x"` and `a = 1;` both parse. The optional `;` was simply dropped in
  the library file.

## Related models

- `CSL-0019` *Simple ORC with imposed component performance (R245fa)*: same
  screening purpose (state points, net power, cycle efficiency) with an
  imposed-effectiveness subcritical R245fa cycle.
- `CSL-0036` *ORC with two-stage expander and intermediate extraction (R134a)*:
  another vapour power cycle with a component model more detailed than a map.
- `CSL-0084` *orc_expander_pump_empirical_maps*: same map approach for
  volumetric expanders and pumps, other fluid (R245fa) and other maps.- `CSL-0104` *supercritical_internal_nu*: the near-supercritical internal
  convection correlations (function library) for the parts of the CO2 heat
  exchangers that cross the pseudo-critical point of R744; this model uses
  polynomial maps instead.
