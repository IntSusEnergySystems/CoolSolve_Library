# Gas engine with Rankine bottoming cycle (positive-displacement expander)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0261`

Steady-state model of a spark-ignition (gasoline) engine whose exhaust gas is
recovered in a boiler feeding a bottoming Rankine cycle on Water, with
positive-displacement (volumetric) expander and pump. It is exercise 8 of the
ULiège *Machines et systèmes thermiques* repetition session TP 12: the engine
part closes on the imposed shaft efficiency, the cycle part computes the steam
flow, the machine displacements and the Rankine and global efficiencies.

| | |
|---|---|
| **Category** | Energy systems › Cogeneration |
| **Fluids** | Air (engine charge and exhaust), Water (Rankine cycle) |
| **Size** | 127 equations (largest block: 32, the `cpbar`-combustion block) |
| **Source** | `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 12/MSTH-SB-R12-EX8.EES` (EES X7.458), candidate TM-0172 |
| **Authors** | ULiège MSTh course (J. Lebrun, V. Lemort, S. Bertagnolio; file signed SB) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution |

## Problem statement

A 4-stroke gasoline engine (displacement 1.3 L, 3000 rpm, shaft efficiency
0.35) runs on a fuel CH1.95 (LHV 44 MJ/kg, vaporised before combustion) and
gives 30 % of the fuel power `Q_dot_c` to a recovery boiler. The bottoming
Rankine cycle on Water has: a boiler at 7 bar / 250 °C with effectiveness 0.8
(no pressure loss), a positive-displacement expander at 6000 rpm (isentropic
efficiency 0.6, volumetric efficiency 1), a condenser at 80 °C and a
positive-displacement pump at 3000 rpm (isentropic efficiency 0.5, volumetric
efficiency 1). On the air side, the throttle loss is zero and the pressure
loss across the intake valves brings the charge to P_3 = 98 kPa (the valve
flow area is a result). Compute the engine states (1–8), the Rankine cycle
states (a–d), the steam flow, the expander and pump displacements, the Rankine
efficiency and the global efficiency `eta_global = (W_dot_u + W_dot_sh)/(Q_dot_c + W_dot_p)`.

## Model

* **Engine** (states 1–8, as in the original): ambient air throttled with zero
  loss (P_1 → P_2, T constant), then an isentropic path from state 2 to the
  valve-outlet pressure P_3 closed by the kinetic-energy balance
  `cp_23*(T_2 - T_3) = C_3^2/2` and the valve flow `V_dot_3 = C_3*A_soupapes`;
  the cylinder admission state (4) equals state 3 in pressure and state 2 in
  temperature, and the charge flow is fixed by the displaced volume flow
  `V_dot_4 = i*N*V_s` (i = 0.5, four-stroke); adiabatic combustion written as
  an energy balance bringing air and fuel to the reference temperature 25 °C
  and the products to the flame temperature T_6, the products being described
  by their **mean specific heat** `cpbar` of the ULiège combustion library
  (combustion assumed complete, `Q_dot_4 = 0`, as in the original); the
  expansion to T_7 follows from the shaft power
  `W_dot_sh = eta_m*M_dot_p*cp_p_67*(T_6 - T_7)` closed by
  `eta_sh = W_dot_sh/Q_dot_c = 0.35`; the pumping work `W_dot_pumping` is zero
  here (P_1 = P_4).
* **Rankine cycle** (states a–d on Water): saturated liquid at the condenser
  (a), pump with isentropic efficiency 0.5 (b), boiler to 250 °C (c) with the
  exhaust-gas side closed by `Q_dot_gw = M_dot_p*cp_p_78*(T_7 - T_8)` and the
  effectiveness relation `Q_dot_gw = epsilon_gw*C_dot_min_gw*(T_7 - T_b)` (the
  water side is the minimum capacitance rate), expander with isentropic
  efficiency 0.6 (d). The steam flow follows from `Q_dot_gw = 0.3*Q_dot_c`,
  the pump and expander displacements from their volumetric efficiencies.
* **`cpbar`**: the five-output `PROCEDURE` of the ULiège library
  `CombCmHn_SI_PNG2003_V2.LIB` (P. Ngendakumana, 2003), copied from library
  model CSL-0005 into a marked block at the top of the file (the original file
  does not contain the routine; `$INCLUDE` of library models is not available
  yet, `CS-GAP-INCLUDE`).

Main inputs and results (default run = the stored EES operating point):

| Variable | Meaning | Value |
|---|---|---|
| f | fuel-air ratio [-] | 0.0376 |
| T_6 / T_7 / T_8 | flame / exhaust / boiler-outlet temperature [°C] | 1343 / 862 / 464 |
| M_dot_steam | steam flow [kg/s] | 0.00691 |
| W_dot_sh / W_dot_exp / W_dot_p | shaft / expander / pump power [W] | 21 110 / 2 028 / 9.3 |
| V_s_exp / V_s_p | expander / pump displacement [m³] | 4.65e-5 / 2.85e-7 |
| eta_rankine | `W_dot_u/(Q_dot_gw + W_dot_p)` [-] | 0.112 |
| eta_global | `(W_dot_u + W_dot_sh)/(Q_dot_c + W_dot_p)` [-] | 0.384 |
| A_soupapes | intake-valve flow area [m²] | 4.30e-4 |

## How to run

```
coolsolve ./gas_engine_rankine_bottoming.eescode      # note the ./
```

One companion file is needed: `gas_engine_rankine_bottoming.initials` — guess
values taken from the EES stored solution. The flame temperature T_6 sits
inside the `cpbar` calls and the model does not converge from the CoolSolve
default guesses (block of 32 variables).

## Results

The table above is the default run (the stored EES operating point); it is the
regression baseline `gas_engine_rankine_bottoming.sol`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![T-s diagram of the bottoming Rankine cycle](figures/gas_engine_rankine_bottoming_ts.png)  + one-line caption -->

## Verification

Reference: the EES stored solution of `MSTH-SB-R12-EX8.EES` (99 variables with
a stored value), compared with
`python3 ../CoolSolve/tools/compare_solution.py gas_engine_rankine_bottoming.sol reference/ees_variables.csv`:

> 99 common variables, 5 differ (rtol=0.001)

The 5 variables above the tolerance, all explained:

* `s_2` (EES 5678.35, CoolSolve 3863.47 J/kg-K, 3.20e-01): constant entropy
  reference-state offset of Air (EES ideal-gas Air vs the CoolProp pseudo-pure
  Air). It cancels in the isentropic inversion `T_3 = TEMPERATURE(Air, s=s_2, P=P_3)`:
  T_3 (4.9e-4), v_3 and V_dot_3 (6e-5) agree.
* `cp_p_67` (1.7e-3) and `cp_p_78` (1.3e-3): the `cpbar` mean specific heats
  are enthalpy differences of the ideal-gas species CO2/CO/H2O/N2, which
  differ slightly between the EES and CoolProp data (same deviation class as
  CSL-0034). `C_3` (1.3e-3) and `A_soupapes` (1.3e-3) follow the air-side
  property slopes the same way.
* All 94 other common variables agree to ≤ 9.7e-4 (largest: `C_dot_p_gw`
  9.7e-4; all the exercise results — powers, flows, efficiencies, cycle
  enthalpies — to ≤ 5.1e-4).

`verification.max_rel_diff` (0.32) is the `s_2` reference offset, not a model
deviation; on physically derived results the model agrees within the
real-fluid/ideal-gas tolerance of the import guide (§11).

## Source and attribution

* Source: `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 12/MSTH-SB-R12-EX8.EES`
  (ULiège Thermodynamics Laboratory, MSTh repetition TP 12, exercise 8; EES
  X7.458; licence stamp `{$ID$ #202: Laboratoire de Thermodynamique, U. de Liege}`).
* Authors: the file header signs `MSTh - SB - R12 - Exercice 8` (S.
  Bertagnolio); the inventory credits the MSTh course (J. Lebrun, V. Lemort,
  S. Bertagnolio).
* **`cpbar`**: P. Ngendakumana, *CombCmHn_SI_PNG2003_V2.LIB* (ULiège
  combustion library, 2003), copied from library model CSL-0005.

## Conversion log

- **2026-10-22 — import**: `ees_extract.py` (103 variables, no lookup or
  parametric table); unit system already `SI MASS DEG PA C J` — no conversion;
  comments translated from French, standard header added.
- **2026-10-22 — `cpbar`**: the original calls the library routine in *function
  position* (`cp_p_56 = cpbar(m_f,n_f,f,T_ref,T_6)`, three call sites) without
  containing its code. The library ships it as a five-output `PROCEDURE`,
  which EES calls with `CALL`, so the three call sites were transcribed as
  `CALL cpbar(m_f,n_f,f,T_p1,T_p2:cp_p_xx,Q_4_xx,x_xx,e_min_xx,e_xx)` — valid
  EES, no equation changed (same transcription as CSL-0006 and CSL-0034); the
  body is copied verbatim from CSL-0005, and the four unused outputs are named
  `Q_4_56`…`e_78` to avoid clashing with the exercise variables.
- **2026-10-22 — dead code removed**: the commented-out provisional values
  (`cp_p_56=1300`, `cp_p_67=1300`, `cp_p_78=1300`), the commented alternative
  `W_dot_sh` definition (`W_dot_in`, `W_dot_m = 2*PI*N*T_m`) and
  `eta_in_actif` — four variables (W_dot_in, W_dot_m, T_m, eta_in_actif) that
  EES still carried in its variable list without a stored value.
- **2026-10-22 — post-processing added**: state-point arrays `P[i]`, `h[i]`,
  `T[i]`, `s[i]` (i = 1..4 for the Rankine states a–d) for the CoolSolve
  diagram overlay; no effect on the results (checked: unchanged `.sol`
  values).
- **Level**: equations 127 → 1; largest block 32 (> 30) → 2; procedures → 1;
  four coupled components (engine, boiler, expander/pump, condenser) → 1; no
  off-design/semi-empirical physics → 0; needs the shipped guesses → 1.
  Score 6 → level 3 (the inventory guessed level 2; the multi-component
  structure and the implicit `cpbar` block put it at the lower boundary of
  level 3).

## Limitations and CoolSolve gaps

* Combustion is assumed complete and the products are described by a mean
  specific heat over the temperature interval (as in the original); no
  dissociation, `HV_CO` unused.
* The shaft efficiency is imposed (`eta_sh = W_dot_sh/Q_dot_c = 0.35`), so the
  expansion closes on it rather than on a machine model.
* No CoolSolve gap blocks this model (`missing_features` empty).

## Related models

* **CSL-0005** `cpbar_combustion_products`: the `cpbar` routine (function
  library) copied into this model.
* **CSL-0034** `gas_engine_full_power_cpbar`: the same engine sub-model family
  (intake valves, `cpbar` combustion, MSTh repetition exercises); there the
  intake pressure is solved from an imposed power, here the expansion closes
  on the imposed shaft efficiency and the exhaust gas drives a Rankine cycle.
