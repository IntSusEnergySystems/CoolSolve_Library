# Fuel-oil boiler modelled with the mean specific heat of the flue gases (cpbar)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0006`

A fuel-oil heating boiler represented as a combustor followed by two heat
exchangers: the flue gases enter the gas side at the adiabatic flame
temperature, transfer heat to the water circuit through a gas-to-water
exchanger (ε-NTU method), and the water loses heat to the environment
(envelope losses). The combustion products are described by their **mean
specific heat** `c_bar_p` between the reference temperature (25 °C) and the
relevant gas temperature, computed by the `cpbar` routine of the ULiège
combustion library (CSL-0005) — the function-library import pattern of the
library: the procedure is copied in a block
`{--- Library functions copied from CSL-0005 ---}` until
`$INCLUDE library:…` exists (`CS-FEAT-IMPORT`).

| | |
|---|---|
| **Category** | Components › Boilers and burners |
| **Fluids** | ideal-gas species CO₂, H₂O, N₂, O₂; Air (air c_p) |
| **Size** | 49 equations (largest block: 13), incl. the copied 113-line `cpbar` procedure |
| **Source** | CoolSolve example `boiler_cpbar.eescode` (CSX-004, S. Quoilin), derived from the EES reference model *Classical fuel-oil heating boiler with ON/OFF control* (TM-0492, J. Lebrun & S. Bertagnolio, ULiège model bank, 2008) |
| **Authors** | S. Quoilin (CoolSolve example); J. Lebrun, S. Bertagnolio (EES reference model); P. Ngendakumana (`cpbar` library) |
| **License** | MIT |
| **CoolSolve** | 0.3.0+fix/library-gaps@fbdb6a7 — **verified** against the EES stored solution (42 variables, ≤ 0.08 %). Needs the CoolSolve fixes of the branch `fix/library-gaps` (merged in CoolSolve `main` on 2026-10-05; `CS-BUG-IF-IGNORED`, `CS-BUG-MOLARMASS`, `CS-BUG-SINGLE-INPUT-PAIR`): CoolSolve v0.3.0 fails on the `cpbar` calls (SingularJacobian) |

## Problem statement

A boiler is characterised by AU₁ = 34 W/K (gas-to-water overall heat
transfer coefficient), AU₂ = 7 W/K (water-to-envelope) and burns a fuel oil
(86.9 % C, 13.1 % H, LHV = 43 MJ/kg, c_f = 1.8 kJ/kg·K) at 0.6 g/s with a
fuel-air ratio f = 0.062. Air, fuel and environment are at 20 °C. Determine
the boiler efficiency when supplied with water at 60 °C and 0.28 kg/s.
(Statement of the CoolSolve example CSX-004.)

## Model

1. **Combustor**: the equivalent fuel CmHn (m = 1, n = y_h·12/y_c = 1.809) and
   the energy balance
   ṁ_f·LHV + ṁ_a·c_p,a·(T_a,su − T_ref) + ṁ_f·c_f·(T_f,su − T_ref) =
   ṁ_p·c̄_p·(T_p,ad − T_ref), with c̄_p = `cpbar(m,n,f,25,T_p,ad)` (mean
   specific heat of the products between 25 °C and the adiabatic flame
   temperature), ṁ_a = ṁ_f/f, ṁ_p = ṁ_a + ṁ_f.
2. **Gas-to-water exchanger** (ε-NTU, counterflow): gas inlet T_gas,su =
   T_p,ad, heat capacity rate Ċ_p = ṁ_p·`cpbar(m,n,f,T_gas,su,T_gas_ex)`,
   NTU₁ = AU₁/Ċ_min, effectiveness ε₁(NTU₁, ω₁) → Q̇₁ and the intermediate
   water temperature T_w,ex_1.
3. **Envelope loss**: pure-water exchanger to the environment, ε₂ =
   1 − exp(−NTU₂) → Q̇₂ and the outlet temperature T_w,ex.
4. **Efficiency**: η = (Q̇₁ − Q̇₂)/(ṁ_f·LHV).

The `cpbar` PROCEDURE (complete/incomplete combustion and pure-air branches
selected by `IF (f>0)` and `IF (f>f_st)`) is copied verbatim from CSL-0005.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `AU_1`, `AU_2` | 34, 7 W/K | `T_p_ad` adiabatic flame temp. | 1974.5 °C |
| `y_c` / `y_h` | 0.869 / 0.131 | `cp_p` (25 °C → T_p_ad) | 1285.0 J/kg·K |
| `LHV`, `c_f` | 43 MJ/kg, 1800 J/kg·K | `cp_p_hex` (T_gas_ex → T_p_ad) | 1307.0 J/kg·K |
| `M_dot_f`, `f` | 6·10⁻⁴ kg/s, 0.062 | `T_gas_ex` flue gas exit | 215.2 °C |
| `T_a_su`, `T_f_su`, `T_env` | 20, 20, 20 °C | `Q_dot_u` useful power | 23.21 kW |
| `T_w_su`, `M_dot_w` | 60 °C, 0.28 kg/s | `eta` boiler efficiency | 0.8997 |

## How to run
Open `boiler_mean_specific_heat.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./boiler_mean_specific_heat.eescode
```

The file `boiler_mean_specific_heat.initials` (guess values, as stored by EES
for the reference model) is picked up automatically: the unknown flame
temperature sits inside the `cpbar` calls, where the mean specific heat
`c̄_p = Δh/ΔT` tends to 0/0 when the temperature is close to the reference
temperature (25 °C), and Newton does not converge from the default guesses.
With the guesses the model solves in 10 iterations
(`boiler_mean_specific_heat.sol` is the regression baseline).

The variant `boiler_mean_specific_heat_onoff.eescode` (same boiler with on/off
burner control, parameters of the identified model, mean specific heats fixed
to 1300 J/kg·K as in the CoolSolve example CSX-005) runs without guesses:
θ = 0.514, η = 0.884, mean efficiency η_set = 0.875 for a set point of 80 °C
with water supplied at 70 °C — it reproduces the stored solution of the example
(48/48 variables identical); `boiler_mean_specific_heat_onoff.sol` is its regression
baseline (tested as `CSL-0006:onoff`).
## Results
Values at the shipped inputs (f = 0.062, complete combustion with excess air,
e = 0.116), as computed by `boiler_mean_specific_heat.eescode`:

| Quantity | c̄_p-based (this model) | constant c̄_p = 1300 (example CSX-004) |
|---|---:|---:|
| `T_p_ad` [°C] | 1974.5 | 1952.0 |
| `T_gas_ex` [°C] | 215.2 | 211.3 |
| `Q_dot_u` [W] | 23 212 | 22 840 |
| `eta` [−] | 0.8997 | 0.8853 |

The constant-c̄_p column is the CoolSolve example CSX-004 (`cp_p = cp_p_hex =
1300 J/kg·K` instead of the two `cpbar` calls). The flue-gas mean specific
heats are 1285.0 J/kg·K (25 °C → `T_p_ad`) and 1307.0 J/kg·K (`T_gas_ex` →
`T_p_ad`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7):
     e.g. boiler efficiency vs the fuel-air ratio (parametric sweep plot). -->
## Verification
Status **verified**: with the inputs of the stored EES run, this model
reproduces **all 42 EES variables that it has in common within 0.08 %**
(EES-vs-CoolProp ideal-gas tables), and the shipped-input results were
cross-checked with an independent computation.

1. **Reference data.** The EES original of the physics, TM-0492 (*Classical
   fuel-oil heating boiler with ON/OFF control*, J. Lebrun & S. Bertagnolio,
   2008), stores the solution of its last run (62 variables): the same
   cpbar-based combustor + ε-NTU boiler at f = 0.06, ṁ_f = 0.0013 kg/s,
   AU_gw = 83 W/K, AU_wenv = 12 W/K, all temperatures 25 °C, water 2150 l/h
   (0.5972 kg/s) supplied at 70 °C, c_w = 4187 J/kg·K. Extracted with
   `tools/ees_extract.py` (unit system already SI-°C-Pa-J).
2. **Comparison** (work copy of this model with the inputs of that run, EES
   guess values, `tools/compare_solution.py` with the variable names mapped;
   42 of the 62 EES variables have a counterpart here — the others belong to
   the ON/OFF regulation, the auxiliaries and the results logging, not
   imported). Main results:

   | Quantity (EES name → this model) | EES | CoolSolve | rel. diff. |
   |---|---:|---:|---:|
   | `t_adiab` → `T_p_ad` [°C] | 1930.49 | 1929.06 | 0.07 % |
   | `c_p_p` → `cp_p` [J/kg·K] | 1277.34 | 1278.30 | 0.08 % |
   | `c_p_g` → `cp_p_hex` [J/kg·K] | 1296.26 | 1297.12 | 0.07 % |
   | `t_g_ex` → `T_gas_ex` [°C] | 187.05 | 187.18 | 0.07 % |
   | `epsilon_gw` → `epsilon_1` [−] | 0.93709 | 0.93697 | 0.01 % |
   | `Q_dot_gw` → `Q_dot_1` [W] | 51 903.5 | 51 891.7 | 0.02 % |
   | `t_w_ex_ON` → `T_w_ex` [°C] | 90.442 | 90.437 | 0.005 % |
   | `eta_ON` → `eta` [−] | 0.91442 | 0.91421 | 0.02 % |

   Largest deviation 0.076 % (`cp_p`); the inputs, `n`, `x_1`, `x_2`,
   `M_dot_a`, `M_dot_p` and `NTU_2` agree to 1e-4 or better. The differences
   are the ideal-gas tables of CO₂/H₂O/N₂/O₂ (EES vs CoolProp), the shipped
   file uses c_w = 4186 where EES uses 4187.
3. **Independent computation** at the shipped inputs (work folder, deleted):
   the combustor balance re-written in Python/CoolProp with ideal-gas
   enthalpies gives `T_p_ad` 1974.46 °C and `c_p_p` 1285.02 J/kg·K against
   1974.48 °C and 1285.01 J/kg·K from CoolSolve. Note that single-input
   `enthalpy(H2O,T=…)` follows a vapour path in both EES and CoolSolve — a
   1-atm computation would cross the saturation dome and give a different c̄_p.
4. **Constant-c̄_p variant**: the shipped equations with `cp_p = cp_p_hex =
   1300 J/kg·K` are exactly the CoolSolve example CSX-004 (η = 0.8853), and
   `boiler_mean_specific_heat_onoff.eescode` reproduces the stored solution
   of CSX-005 (48/48 variables identical, also with the fixed CoolSolve) — the
   ε-NTU and regulation parts of the model are verified by construction.
5. **Why the earlier status was *blocked*.** Under CoolSolve v0.3.0 the copied
   `cpbar` procedure hit three defects, now fixed in the branch
   `fix/library-gaps` (reproducers in the CoolSolve gap register):
   `CS-BUG-IF-IGNORED` (every branch of the procedure executed),
   `CS-BUG-MOLARMASS` (`molarmass()` in kg/mol instead of kg/kmol) and
   `CS-BUG-SINGLE-INPUT-PAIR` (`enthalpy(X,T=T1) − enthalpy(X,T=T2)` evaluated
   inconsistently) — the solve ended in a `SingularJacobian`.
## Source and attribution

The CoolSolve example `boiler_cpbar.eescode` (CSX-004, S. Quoilin / ULiège
Thermodynamics Laboratory) is the direct base of this import; it is a
simplified version (cpbar disabled, exercise statement) of the EES reference
model *CLASSICAL_ONOFF_BOILER_SIMULATION_REFERENCE_EES_MODEL_SBJL080212.EES*
(TM-0492) by **Jean Lebrun and Stéphane Bertagnolio** (ULiège Thermodynamics
Laboratory, model bank, 2008-01-10; ASHRAE TC4.7 HVAC1 Toolkit lineage; the
file carries the lab disclaimer "freely distributed, may not be sold, cite
the origin"). The `cpbar` procedure is by **P. Ngendakumana** (ULiège, 2003),
imported as CSL-0005.

Sources (never copied into the library):
`~/git/CoolSolve/examples/boiler_cpbar.eescode` and
`~/git/CoolSolve/examples/boiler_cpbar2.eescode` (CSX-004/CSX-005);
`~/Nextcloud/thermo_models/Model data bank/Heat_and_Cool_Production_Systems/Heat_Production_by_Combustion/CLASSICAL_ONOFF_BOILER_SIMULATION_REFERENCE_MODEL_SBJL080212.zip`
(TM-0492, with its `UserLib` copies of the combustion library).

## Conversion log

- **2026-10-05 — import** (`T-IMPORT`, card C-05): base = CoolSolve example
  CSX-004 (unit system SI-°C-Pa-J, comments already in English); standard
  header added and the section comments made explicit (no equation changed).
  The two `cpbar` calls that the example had replaced by constants
  (`//cp_p=cpbar(m,n,f,T_p_ad,T_ref){1300}`) were **restored** in their
  original EES form `CALL cpbar(m,n,f,T1,T2 : c_p_p,Q_41,x_1,e_min_1,e_1)`
  (as in TM-0492: EES loaded the routine implicitly from its `USERLIB`),
  and the `cpbar` PROCEDURE was **copied verbatim from CSL-0005** in a
  `{--- Library functions copied from CSL-0005 ---}` block — the library
  pattern until `$INCLUDE library:…` (`CS-FEAT-IMPORT`, `CS-GAP-INCLUDE`).
  Output names `Q_41, x_1, e_min_1, e_1` / `Q_42, x_2, e_min_2, e_2` follow
  TM-0492.
- **2026-10-05 — status `blocked`**: SingularJacobian with the copied
  procedure (`CS-BUG-IF-IGNORED`, `CS-BUG-MOLARMASS`,
  `CS-BUG-SINGLE-INPUT-PAIR`); superseded by the re-check below.
- **2026-10-05 — on/off variant**: `boiler_mean_specific_heat_onoff.eescode`
  imported from the CoolSolve example CSX-005 (S. Quoilin): header added,
  the commented-out alternative inputs and the trailing variable dump of the
  example removed; the equations are unchanged (c̄_p kept at the constants of
  the example, which is what makes the variant runnable). Verified against
  the stored solution of the example (48/48 identical).
- **2026-10-05 — variant baseline (C-14 review)**: `boiler_mean_specific_heat_onoff.sol`
  added so that `tools/test_models.py` tests the variant (`CSL-0006:onoff`).
- **Not imported** from TM-0492 (documented decision): the `WRITERESULTS`
  procedure that logs the results into an external lookup table
  (`Lookup_Results`, an `.lkt` file not shipped in the zip — output logging,
  not physics; also `lookup()` table writes), the auxiliaries correlation
  with the degenerate 5-argument intrinsic `IF(Q_dot_u_n,35000,100,0,0)`
  (CoolSolve has the 3-argument `if` only; in the EES run the term evaluated
  to 0), and the ON/OFF regulation is covered by the runnable variant
  instead. These would require CoolSolve features that are not needed to
  represent the boiler physics; none of them affects the computed results
  used for the verification.
- **2026-10-05 — re-check (`T-RECHECK`) with CoolSolve `0.3.0+fix/library-gaps@fbdb6a7`**:
  the three registered CoolSolve defects are fixed. The copied `cpbar`
  procedure is the verbatim copy of CSL-0005 with its `UNITSYSTEM()`/`CALL
  ERROR` guards active (as in the EES `.LIB`; `CS-GAP-UNITSYSTEM-FUNC`, closed);
  `boiler_mean_specific_heat.initials` added (guess values from the converged
  solution, equivalent to the guesses EES stores); `boiler_mean_specific_heat.sol`
  is the regression baseline. Status `blocked` → `verified`. No equation of the
  boiler changed since the import.
- **Level 2** (score 2: 49 equations, largest block 13, procedure present —
  in line with the inventory guess and the level-2 ε-NTU boiler exercises).

## Limitations and CoolSolve gaps
- **Needs CoolSolve with the fixes of the branch `fix/library-gaps`**
  (CoolSolve > v0.3.0; merged in `main` on 2026-10-05). Closed gaps: `CS-BUG-IF-IGNORED`, `CS-BUG-MOLARMASS`,
  `CS-BUG-SINGLE-INPUT-PAIR` (and `CS-GAP-UNITSYSTEM-FUNC` for the guards of the
  copied routine); none is left in `missing_features`.
- **Convergence needs the shipped guess values**: from the default guesses the
  Newton iteration of the `cpbar` block stalls (the mean specific heat is 0/0
  at the reference temperature); the full solver pipeline of CoolSolve
  (`solverPipeline = Newton, TrustRegion, LevenbergMarquardt, …`) reaches a
  point that does not pass the final verification. Keep `.initials` next to the
  model.
- `CS-GAP-FORMATION-ENTHALPY` (closed): affected only the `Q_41`/`Q_42` outputs
  of the copied routine (unburned-CO losses, zero here since the combustion is
  complete).
- `CS-GAP-INCLUDE`/`CS-FEAT-IMPORT`: the copy of the procedure is the
  registered workaround; replace it by `$INCLUDE library:cpbar_combustion_products`
  once CoolSolve supports it (`T-MERGE` batch of the roadmap).
- Physics: simplified air (79/21 molar), no dissociation, the flue gas is
  cooled from the adiabatic flame temperature (no furnace/section split),
  constant water c_p, ε-NTU exchanger with constant AU.
## Related models
- `CSL-0005` *cpbar_combustion_products*: the function library this model
  calls; its `cpbar` procedure is copied in the block marked as such (and
  its README lists this model as first user).
- The gas-turbine and engine models of the collection (e.g. card C-10,
  *two-shaft gas turbine*) call the same library (`cpbar`, `gamma`).
- `CSL-0166` *boiler_modulating_burner_refsim*: the classical ON/OFF boiler of the same model bank (modulating-burner RefSim model, 2008 model bank).
