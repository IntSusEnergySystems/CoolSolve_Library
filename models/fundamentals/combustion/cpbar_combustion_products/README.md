# cpbar: mean specific heat of CmHn combustion products (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0005`

Three EES routines returning the properties of the combustion products of a
hydrocarbon fuel CmHn burnt in simplified air (79 % N₂ / 21 % O₂): the mean
specific heat `c_bar_p` between two temperatures (PROCEDURE `cpbar`, which
also returns the unburned-CO losses of incomplete combustion), the ratio of
specific heats (FUNCTION `gamma`) and the molar mass of the products (FUNCTION
`mmprod`). This is the ULiège combustion library that the boiler, engine and
gas-turbine models of the collection call implicitly; it is kept in native EES
syntax with the original names and signatures so that those models (and the
future `$INCLUDE library:cpbar_combustion_products`) can use it unchanged.

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | ideal-gas species CO₂, CO, H₂O, N₂, O₂ |
| **Size** | 30 equations after analysis (largest block: 5); 3 routines of 45–70 lines |
| **Source** | ULiège Thermodynamics Laboratory — EES library `CombCmHn_SI_PNG2003_V2.LIB` (2003); also the CoolSolve example `cpbar.eescode` (CSX-013) |
| **Authors** | P. Ngendakumana (ULiège Thermodynamics Laboratory, 2003) |
| **License** | MIT |
| **CoolSolve** | 0.3.0+fix/library-gaps@fbdb6a7 — **verified** against the EES stored solution (≤ 0.22 %). Needs the CoolSolve fixes of the branch `fix/library-gaps` (merged in CoolSolve `main` on 2026-10-05; `CS-BUG-IF-IGNORED`, `CS-BUG-MOLARMASS`, `CS-BUG-SINGLE-INPUT-PAIR`, `CS-GAP-FORMATION-ENTHALPY`, `CS-GAP-UNITSYSTEM-FUNC`): CoolSolve v0.3.0 runs the file but its results are wrong |

## Problem statement

For a fuel CₘHₙ burnt with a fuel-air ratio f (kg of fuel per kg of air;
f = 0 means pure air), compute between two temperatures T_p1 and T_p2:

- `c_bar_p`, the mass-basis mean specific heat of the (dry + water) products
  [J/kg·K], from the ideal-gas enthalpies of CO₂, CO, H₂O, N₂, O₂ weighted by
  the equilibrium composition of complete or incomplete combustion;
- in incomplete combustion (air deficiency, negative excess air): `Q_4`, the
  losses in unburned CO [J/kg of fuel], `x`, the fraction of the C atoms
  oxidized to CO₂, `e_min`, the minimum excess air for x > 0, and the actual
  (negative) excess air `e`;
- `gamma` = c̄_p/(c̄_p − R_u/MM) and the products molar mass `MM` [kg/kmol].

Assumptions: simplified air, no O₂ in the flue gas of incomplete combustion,
all H oxidized to H₂O, stoichiometric air `parfuel = m + n/4` kmol O₂/kmol
fuel, fuel molar mass `MM_f = 12·m + n`.

## Model

| Routines | Signature | Returns |
|---|---|---|
| `cpbar` (PROCEDURE) | `CALL cpbar(m, n, f, T_p1, T_p2 : c_bar_p, Q_4, x, e_min, e)` | mean c̄_p [J/kg·K] of the products of CₘHₙ between T_p1 and T_p2 [°C]; with incomplete combustion also Q_4 [J/kg fuel], x [−], e_min and e [−] |
| `gamma` (FUNCTION) | `gamma(m, n, f, T_p1, T_p2)` | ratio of specific heats of the same products [−] |
| `mmprod` (FUNCTION) | `mmprod(m, n, f)` | molar mass of the products [kg/kmol] |

The three branches (complete combustion with excess air, incomplete
combustion with air deficiency, pure air for f = 0) are selected by `IF (f>0)`
and `IF (f>f_st)` statements. Units: SI, mass basis, °C, Pa, J — the routines
guard this with `UNITSYSTEM()`/`CALL ERROR` checks, which are kept as in the
EES original (CoolSolve's unit system is fixed to SI-°C-Pa-J, so they never fire).

## How to run
Open `cpbar_combustion_products.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./cpbar_combustion_products.eescode
```

The demonstration program after the definitions calls `cpbar`, `gamma` and
`mmprod` on the fuel oil (m = 86/12, n = 14, M = 100 kg/kmol) and temperatures
(25 °C → 200 °C) of the original EES test file, for the complete-combustion
(f = 0.05), incomplete-combustion (f = 0.07 and 0.08) and pure-air (f = 0)
regimes; it is the regression baseline (`cpbar_combustion_products.sol`). It
solves in 6 iterations; the routines are used by other models through a copy of
their definitions until `$INCLUDE library:cpbar_combustion_products` is available.
## Results
Reference results are the stored solution of the companion EES test file
(`CombCmHn_SI_PNG2003_V2_test.EES`, EES 7.966, candidate TM-0254; fuel oil
CₘHₙ with m = 86/12, n = 14, 25 °C → 200 °C):

| Quantity | Case | EES reference | CoolSolve | Deviation |
|---|---|---:|---:|---:|
| `c_bar_p` [J/kg·K] | incomplete combustion, f = 0.07 | 1090.60 | 1093.02 | 0.22 % |
| `Q_4` [J/kmol fuel] | idem | 1.51725e8 | 1.51794e8 | 0.05 % |
| `x` [−] | idem | 0.925188 | 0.925155 | 0.004 % |
| `e_min` [−] | idem | −0.3359375 | −0.3359375 | exact |
| `e` [−] | idem | −0.025132 | −0.025143 | 0.05 % |
| `gamma` [−] | pure air | 1.394538 | 1.393607 | 0.07 % |
| `MM_prod` [kg/kmol] | pure air | 28.85006 | 28.85040 | 0.001 % |

Cases of the demonstration program without EES reference (checked against an
independent computation, see *Verification*):

| Quantity | Case | CoolSolve | Independent | Deviation |
|---|---|---:|---:|---:|
| `c_bar_p` [J/kg·K] | complete combustion, f = 0.05 (e = 0.365) | 1072.33 | 1071.06 | 0.12 % |
| `c_bar_p` [J/kg·K] | pure air (`Q_4 = 0`, `x = 1`, `e_min = e = 0`) | 1020.32 | 1019.36 | 0.09 % |
| `gamma` [−] | complete combustion, f = 0.05 | 1.36769 | 1.36829 | 0.04 % |
| `gamma` [−] | incomplete combustion, f = 0.08 | 1.36724 | 1.36779 | 0.04 % |
| `MM_prod` [kg/kmol] | complete combustion, f = 0.05 | 28.8396 | 28.8396 | exact |

`Q_4` is the heat of reaction of the unburned CO (b kmol of CO per kmol of fuel
times the lower heating value of CO, 282 990 kJ/kmol).

<!-- FIGURE (added by the maintainer if the model becomes runnable, docs/model_workflow.md §7):
     e.g. c_bar_p of the fuel-oil products vs the fuel-air ratio across the three regimes. -->
## Verification
Status **verified**: the three regimes agree with the EES stored solution and
with an independent computation within the expected EES-vs-CoolProp
ideal-gas tolerance (≤ 0.5 %, `ees_import.md` §11); largest deviation 0.22 %
(`c_bar_p`, incomplete combustion).

1. **EES reference.** The companion test file (TM-0254) stores the solution of
   its last run: the incomplete-combustion `cpbar` call (f = 0.07) and the
   pure-air `gamma`/`mmprod` calls, all for 25 °C → 200 °C (first table of
   *Results*; extracted with `tools/ees_extract.py` of the CoolSolve
   repository; compared with `tools/compare_solution.py`, names mapped to the
   demonstration program). The 7 values agree within 0.22 %.
2. **Independent computation** (work folder, deleted): the same equations
   re-written in Python with CoolProp's *ideal-gas* enthalpy (h − h_residual,
   pressure-independent) and molar masses, no CoolSolve code. It checks the
   regimes that the EES file does not store: complete combustion (f = 0.05),
   pure-air `cpbar`, incomplete combustion with f = 0.08 (second table of
   *Results*: ≤ 0.12 %). It is also 0.10 % from the EES `c_bar_p`, i.e. the
   CoolSolve value is ≈ 0.1 % higher than a perfectly ideal gas because
   CoolSolve evaluates the temperature-only enthalpies at an internal pressure
   (101 325 Pa; 100 Pa for H₂O), so the real-gas effect of CO₂ at 1 atm is
   included.
3. **Why the earlier status was *blocked*.** Under CoolSolve v0.3.0 the same
   file solved but gave wrong values (`c_bar_p` 1020.3 instead of 1090.6,
   `x` = 2900, `gamma` < 0, `MM_prod` 0.0289 instead of 28.85 …). Five
   CoolSolve defects, now fixed in the branch `fix/library-gaps` (registered
   in the CoolSolve gap register with their reproducers):
   - `CS-BUG-IF-IGNORED`: the conditions of the `IF … THEN … ELSE` statements
     were ignored — every branch executed, later assignments overrode earlier
     ones, and the pure-air `cpbar` call failed (division by m = 0 in an
     untaken branch);
   - `CS-BUG-MOLARMASS`: `molarmass()` returned kg/mol instead of the EES kg/kmol;
   - `CS-BUG-SINGLE-INPUT-PAIR`: `enthalpy(X,T=T_p1) − enthalpy(X,T=T_p2)` in one
     expression evaluated inconsistently between the solve and the verification
     (internal pressure clamped to 1000 Pa);
   - `CS-GAP-FORMATION-ENTHALPY`: ideal-gas enthalpies lacked the heats of
     formation, so `Q_4` (unburned-CO losses) was wrong (`LHV_CO` = −5.5 instead
     of 283.0 MJ/kmol);
   - `CS-GAP-UNITSYSTEM-FUNC`: `UNITSYSTEM()` and `CALL ERROR` were unknown, the
     unit-system guards had to be commented out.
   With these fixes the file solves **as written in EES**: the guards and the
   pure-air `cpbar` call are restored, and no equation was changed.
## Source and attribution

Function library written by **P. Ngendakumana** (ULiège Thermodynamics
Laboratory) in 2003, as identified by the "PNG 2003" in the file name and the
inventory of S. Quoilin's `thermo_models` collection; it has been distributed
and used in the lab's teaching and research EES setups since (loaded
automatically from the EES `USERLIB` folder). The CoolSolve example
`cpbar.eescode` (CSX-013, S. Quoilin) is an earlier conversion of the same
file with the same defects; this library model supersedes it.

Source file (plain-text EES library, comments in French):
`~/Nextcloud/thermo_models/Model data bank/EES_Functions/cpbar/COMBCMHN_PNG_2003/CombCmHn_SI_PNG2003_V2.LIB`
(inventory candidate `TM-0253`; companion test file `CombCmHn_SI_PNG2003_V2_test.EES`
= `TM-0254`).

## Conversion log

- **2026-10-04 — import** (`T-FUNC`, card C-04): the `.LIB` (Windows-1252,
  CRLF, `{$DS.}` header tag, trailing NUL byte) was converted to UTF-8/LF;
  unit system already SI-°C-Pa-J on mass basis, no conversion needed; the
  EES help tags `{$CPBAR}`, `{$GAMMA}`, `{$MMPROD}` became plain comment
  blocks; the French inline comments were translated to English; the
  `UNITSYSTEM()`/`CALL ERROR` guards were kept but commented out (CoolSolve
  supported neither; `CS-GAP-UNITSYSTEM-FUNC` — restored by the re-check
  below). **No equation was changed**: the routines are byte-faithful to the
  original apart from the comment edits above.
- **2026-10-04 — demonstration program**: written after the definitions, in
  the pattern of the CoolSolve example `cpbar.eescode` (CSX-013) and of the
  original test file TM-0254: the same fuel oil and temperatures, one call
  per regime with distinct output names (`_c`, `_i`, `_a`). The pure-air
  `cpbar` call was kept commented (it crashed CoolSolve,
  `CS-BUG-IF-IGNORED` — restored by the re-check below); the pure-air inputs
  are used by the `gamma` and `mmprod` calls. The original test file commented the alternative cases too
  (EES cannot overload output names), so this is a documentation choice, not
  a physics change.
- The CoolSolve example `cpbar.eescode` (CSX-013) is superseded by this model
  in the library; it remains in the CoolSolve repository as a test case.
- **2026-10-04 — status `blocked`**: see *Verification* (superseded by the
  re-check below).
- **2026-10-05 — re-check (`T-RECHECK`) with CoolSolve `0.3.0+fix/library-gaps@fbdb6a7`**:
  the five registered CoolSolve defects are fixed, so the workarounds of the
  import were removed: the `UNITSYSTEM()`/`CALL ERROR` guards of `cpbar` and
  `gamma` are active again (as in the EES `.LIB`) and the pure-air `cpbar` call
  of the demonstration program is restored. `cpbar_combustion_products.sol` is
  the regression baseline. Status `blocked` → `verified`. No equation of the
  routines changed since the import.
- **Level 2** although the raw score is 1 (30 equations, largest block 5,
  procedures/functions present): kept in line with the inventory guess and
  with the level-2/3 boiler, engine and gas-turbine models that call these
  routines (three-branch combustion logic, 9 outputs).

## Limitations and CoolSolve gaps
- **Needs CoolSolve with the fixes of the branch `fix/library-gaps`**
  (CoolSolve > v0.3.0; merged in `main` on 2026-10-05): the file also *runs* under v0.3.0 but gives wrong
  results (see *Verification*). Closed gaps: `CS-BUG-IF-IGNORED`,
  `CS-BUG-MOLARMASS`, `CS-BUG-SINGLE-INPUT-PAIR`, `CS-GAP-FORMATION-ENTHALPY`,
  `CS-GAP-UNITSYSTEM-FUNC`; none is left in `missing_features`.
- `CS-GAP-INCLUDE` / `CS-FEAT-IMPORT`: models that call these routines copy
  their definitions until `$INCLUDE library:cpbar_combustion_products` exists.
- Accuracy: the ideal-gas enthalpies of CoolProp differ from those of EES by
  ≈ 0.1–0.2 % on c̄_p (the internal pressure of CoolSolve's temperature-only
  property calls adds the real-gas effect of CO₂ at 1 atm).
- Physics: simplified air (79/21 molar), no dissociation, no O₂ in the flue
  gas of incomplete combustion, `MM_f = 12·m + n` (H = 1 kg/kmol), enthalpy
  differences on the *ideal-gas* tables of the five species; `Q_4` is the heat
  of reaction per kmol of fuel (J/kmol), although the original comments call it
  J/kg of fuel.
## Related models
- `CSL-0087` *internal_turbulent_nusselt*: the other `ht`-translation
  function library of the library (same layout: functions + demonstration
  program), here for heat transfer rather than for combustion properties.
- `CSL-0006` *boiler_mean_specific_heat*: first user — its `cpbar`
  procedure is a copy of this one, in a block marked
  `{--- Library functions copied from CSL-0005 ---}`, until `$INCLUDE library:…`
  (`CS-FEAT-IMPORT`) is available.
- `CSL-0011` *two_shaft_gas_turbine_compressor_map*: calls `cpbar` and `gamma`
  (copied in its runnable variants).
- `CSL-0046` *octane_combustion_400pct_air*: combustion exercise of the same
  course (species formation enthalpies and ideal-gas enthalpies, no `cpbar`).
- Engine models of the collection also call `cpbar`/`gamma`.
- `CSL-0050` *gas_turbine_two_shaft_intercooled_regenerative*: gas turbine of the
  same course, combustion chamber of the air assumed unchanged (no `cpbar`).
- `CSL-0058` *diesel_engine_excess_air_exhaust_analysis*: exhaust-gas analysis
  of a diesel engine (real-fluid product enthalpies, no `cpbar`).
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.
- `CSL-0149` *gas_engine_complete_model*: complete gas engine (maximum-power
  point with recovery circuits), `cpbar` for the products between 25 °C and the
  flame temperature and between `t_6` and `t_7`.
- `CSL-0150` *adiabatic_flame_dissociation*: adiabatic flame temperature of
  CH4 or fuel oil with chemical-equilibrium dissociation (EES built-in
  `Chem_Equil`, native file blocked), same combustion-course material.
- `CSL-0166` *boiler_modulating_burner_refsim*: its cpbar procedure is copied into this model (modulating-burner RefSim model, 2008 model bank).
