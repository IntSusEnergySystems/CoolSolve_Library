# ThermoCycle (Modelica) - source sweep for the CoolSolve_Library

Triage (not an audit) of the ThermoCycle Modelica library of the ULiège Thermodynamics Laboratory, to find the few steady-state models and correlations worth translating into the EES-compatible CoolSolve language. The machine-readable backlog is [`inventory.csv`](inventory.csv) (21 rows, `THC-001` ... `THC-021`, same columns as the LaboThapPy inventory).

| | |
|---|---|
| Repository | https://github.com/thermocycle/Thermocycle-library (`origin` of the local clone), site http://thermocycle.net |
| Local snapshot | `~/git/Thermocycle-library`, git repository, commit `b4f16c0b` (2019-03-20, "Removed enable annotation related to obsolete parameter..."), 265 commits from 2013-05-24 |
| Language / stack | Modelica 3.2.1, fluid properties through ExternalMedia and CoolProp (Dymola 2014/2015 era: ThermoCycle 1.x with CoolProp2Modelica, 2.x with ExternalMedia) |
| Size | 665 `.mo` files, 55 892 lines (`ThermoCycle/`: Components, Examples, Functions, Icons, Interfaces, Media, Obsolete, UsersGuide), a `Resources/Images` folder (19 entries), a Sphinx `docs/` (index, components, numerical methods, publications) |
| Tests / CI | none usable: test models are drivers with sources and ramps, no `assert`, no stored results, no data file (`find` shows no `.txt`, `.mat`, `.csv`); OpenModelica and Dymola are not installed here, so no Modelica run was possible |

## 1. License and attribution

> **Maintainer decision (task of 2026-10-05):** the library is MIT (ULiège Thermodynamics Laboratory, developed by the maintainer); `license_status = open:MIT` for every row. What matters is the credit to the authors of each original model.

* **Declared licenses are not uniform.** `LICENSE` is MIT, "Copyright (c) 2018 Thermodynamics Laboratory (University of Liège)", added on 2018-09-20 (commit `7aa9782`, S. Quoilin). `README.md`, `docs/index.rst`, `UsersGuide/Contacts.mo` and `UsersGuide/ModelicaLicense2.mo` still say "Modelica License 2". The `package.mo` files of `Components`, `Components/HeatFlow`, `Components/FluidFlow`, `Components/Units`, `Functions`, `Interfaces`, `Media`, `Icons`, `Obsolete` and `Examples` carry "Copyright (c) 2013-2014, Sylvain Quoilin and Adriano Desideri". The **reciprocating-machine package** states "Copyright (c) 2011-2013 Technical University of Denmark, DTU Mechanical Engineering ... Modelica License 2, main contributor Jorrit Wronski": it is the only third-party copyright found, and it concerns the kept candidate THC-005 (confirm with J. Wronski, or simply credit him as for any translated model).
* **Authors.** `README.md`: Bertrand Dechesne and Javier Vega (ULiège), Sylvain Quoilin (KU Leuven), Jorrit Wronski (DTU). `docs/index.rst`, `UsersGuide/Contacts.mo` and the example packages: S. Quoilin, A. Desideri, J. Wronski, I. Bell (ULiège). Git history (265 commits): A. Desideri 78, J. Wronski 100 (two identities), S. Quoilin 62 (two identities), `tbeu` 9, B. Dechesne 7, `ULg - Thermodynamics Laboratory` 2, one commit each for F. Ransy, J. Vega, L. Woolley, P. Harman, `dietmarw`, `thorade` and `queraltab` (author of the last commit). The `authors` column of the inventory comes from the git history of the files and the package headers; the maintainer completes it.
* **How to cite:** Quoilin, Desideri, Wronski, Bell and Lemort, "ThermoCycle: A Modelica library for the simulation of thermodynamic systems", Proc. 10th International Modelica Conference, 2014 (first item of `docs/publications.rst`), plus the scientific source of each model (listed in the inventory `notes`).
* **Third-party material inside the repo** (cite the original, check redistribution): Copeland compressor catalogue coefficients (`Functions/Compressors_EN12900`), thermal-oil property tables (`Media/Incompressible/IncompressibleTables`), the NREL receiver correlations and the Soltigua/Sopogy datasheet coefficients (`SolarAbsorber`), published correlations (Shah, Gungor-Winterton, Cooper, Yan et al., Annand, Woschni, Adair, Kornhauser, Irimescu).

**Credit block to reuse in the README of a translated model:**

```text
This CoolSolve model is a translation (EES-compatible language, equation-oriented) of
<model/correlation name> from the ThermoCycle Modelica library, file <path>, commit b4f16c0b.
ThermoCycle - https://github.com/thermocycle/Thermocycle-library
Copyright (c) 2018 Thermodynamics Laboratory (University of Liege), MIT License.
Original authors: S. Quoilin, A. Desideri, J. Wronski, I. Bell (see the git history of the file).
Changes: translated from Modelica to CoolSolve; der() terms set to zero (steady state);
<other changes>. Scientific basis: <original reference>.
```

## 2. What the repository contains

ThermoCycle is a library for the **dynamic** modelling of thermal systems (ORC, heat pumps, solar fields), built on finite-volume flow cells and moving-boundary cells; its own README says so. What it holds, by top-level package:

* `Components/FluidFlow`: 1D flow cells and pipes (`Flow1Dim`, `Cell1Dim`, incompressible and constant-cp variants), sources, sinks, sensors.
* `Components/HeatFlow`: heat-transfer correlation models for the cells (single-phase and two-phase, in `HeatTransfer`), metal walls, solar absorber models with their geometry records, sources and sensors.
* `Components/Units`: heat exchangers (`Hx1D` family, `CrossHX`, `BoilerSystem`, `MBeva`, the `MB_HX` moving-boundary package), tanks and thermocline storage, solar fields, pumps, expanders, compressors, steam turbine, valves and pressure drops, reciprocating machines, controllers.
* `Functions`: empirical machine maps (hermetic and open-drive scroll expander, single-screw expander, pumps, EN12900 compressors, test-rig pressure drops), numerical smoothing functions, enumerations.
* `Examples`: step-by-step ORC (R245fa) and heat-pump (R407c) cycles, plants, test drivers. `Media`: ExternalMedia/CoolProp wrappers and thermal-oil tables. `Interfaces`, `Icons`, `UsersGuide`, `Obsolete`.

What it does **not** contain: no void-fraction or two-phase pressure-drop correlation (the moving-boundary functions `Theta` and `Gamma` are coefficients of the dynamic cell balances), no steady-state cycle example (all 26 example models assemble dynamic components with time ramps), no steady storage sizing model.

## 3. Sweep method

1. `find` on `*.mo`: 665 files, each holding one class (two packages hold several: `ScrollCompressor.mo`, `HeatStorageWaterHeater.mo`). A throwaway script (not kept: the rules of step 2 reproduce the counts) stripped the comments and extracted per file the class kind (model, function, record, connector, package, type, block), `partial`, the number of `der(` calls, `extends`, `parameter`, `when`, `algorithm` and the line count.
2. The files were assigned to families by **path rules, applied in this order**: kept candidates (listed files); `package.mo`; `Media` (wrappers) and `Icons`, `Interfaces`, `Functions/Enumerations`, `UsersGuide`; `Obsolete`; `Examples/Simulations`; test harnesses (`Examples/Test*`, `*/Tests/*`, `*/TestCases/*`, reciprocating `Examples`); sources, sinks, sensors; control systems; numerical helpers (`Functions` smoothing and start-value functions); partial classes; correlation wrappers and couplers; then by component family (pipes and walls, heat exchangers, moving-boundary, tanks, solar fields, reciprocating machines); the remaining steady components were classified one by one. Every file lands in exactly one family (665 of 665).
3. **Dynamic** means: contains `der()`, or instantiates a dynamic component (`Flow1Dim`, `Cell1Dim`, `MetalWall`, `Tank`, `Drum_pL`, moving-boundary cells), or is an example driven by time (`experiment(StopTime...)`, ramps). The `steadystate_*` parameters of the heat exchangers only set `der = 0` at initialisation, so such models stay dynamic (maintainer rule: exclude every dynamic model). Models whose only dynamic terms are a thermal mass or a rotor inertia (`SolAbsForristal`, the Lemort machines) are treated as steady with `der = 0`.
4. All files of the kept candidates, all the steady components of `Units` (`Expander`, `Pump`, `Compressor`, `SteamTurbine`, `Nozzle`, valves, `DP`, `Pdrop`, `Semi_isothermal_HeatExchanger`, `ScrollCompressor`, `ExpanderOpendriveDetailed`, `Compressor_EN12900`), the heat-transfer correlations, the reciprocating heat-transfer files, the media tables and the example plants (structure) were read; the dynamic families were judged by structure (instantiated components, `der()` counts) and by their documentation, not line by line.
5. **Overlap check** against `library.csv`, `functions.csv` and the four inventories (title, description and notes of every row, searched by keyword), and a check of the incompressible-fluid list of CoolProp 8.0.0. The polynomial maps of `THC-003` were re-evaluated in Python to check their ranges. No Modelica model was run.

## 4. Summary counts

| | Files | Share |
|---|---:|---:|
| **Total `.mo` files** | **665** | |
| Infrastructure excluded (packages 95, icons 35, connectors and converters 18, media wrappers 67, enumerations 8, users guide 2, partial classes 19, sources, sinks and sensors 28, controllers 7, smoothing and start-value helpers 11, correlation wrappers and couplers 20, **test harnesses 131**) | 441 | 66 % |
| **Dynamic excluded** (finite-volume flow and heat exchangers 26, moving-boundary 38, tanks and storage 10, solar fields 6, reciprocating machines 17, example plants 26) | 123 | 18 % |
| Obsolete excluded (21 old dynamic models, 3 old sources, 2 old absorbers, 1 old expander) | 27 | 4 % |
| Steady but already covered or trivial (Lemort/Winandy machines 2, Stodola turbine 1, real-fluid nozzle 1, single-phase and plate correlations 6, valves, lumped pressure drops, constant-efficiency machines, e-NTU wall exchanger, constant-cp cells 12) | 22 | 3 % |
| **Candidates kept** (5 cards: THC-001 to THC-005) | 38 | 6 % |
| Kept at low priority, to merge into other cards (THC-006 EN12900 data 9, THC-007 oil tables 5) | 14 | 2 % |

**Candidates by `category_guess`** (inventory rows with `decision = todo`, 7 rows): `solar_renewables` 2 (14 files), `heat_transfer` 2 (11 files), `expanders_turbines` 1 (13 files), `compressors` 1 (9 files), `properties` 1 (5 files). By priority: wave1 1, high 1, medium 2, low 3. By kind: 1 steady, 6 function. The 14 other rows are summary rows (`discarded`, priority `skip`): 5 steady-covered and 9 dynamic or infrastructure families; for a summary row `n_lines` is the total over the files of the family, for a candidate it is the main file.

## 5. Selection rationale

* **Excluded by rule:** every dynamic model; connectors, interfaces, partial and base classes, icons, media wrappers, packages, enumerations; test harnesses and examples that assemble dynamic components; obsolete versions. That is 591 of the 665 files; ThermoCycle is a dynamic library and almost nothing steady is left once the infrastructure is removed.
* **Excluded because already covered:** the Winandy scroll compressor and the Quoilin open-drive scroll expander are `CSL-0007` and `CSL-0037` (and LTP-002/LTP-005); the Stodola turbine is TSP-003; the isentropic nozzle is TM-0002; the Gnielinski, Dittus-Boelter, Martin, Muley-Manglik and Yan correlations are LTP-034/LTP-035/TM-0319 (the same published correlations); `RLMTD` is the regularised LMTD already listed as TSP-029; valves, `DP` and constant-efficiency machines are textbook blocks.
* **Kept** because they bring something the library and the other inventories do not have:
  * **Solar thermal** (`renewables/solar_thermal` is empty and `thermo_models` has no collector): the first-principles Forristal/NREL receiver model in steady form (THC-001) and the empirical NREL Schott PTR70 / Sopogy / Soltigua loss and efficiency correlations (THC-002), which complement LTP-020/LTP-050 (Dickes-Lemort-Quoilin form).
  * **ORC machine maps** (THC-003): empirical isentropic efficiency and filling-factor maps for three volumetric expander technologies and the pump curves of the ULiège rigs, a map-based alternative to the semi-empirical `CSL-0037`.
  * **Heat-transfer correlations**: Shah 1982 flow boiling (in LaboThapPy only as a simplified inline block of the skipped legacy script LTP-054, not in the LTP-034 function library) with Gungor-Winterton and Cooper (THC-004), and the in-cylinder correlations for engines and compressors (THC-005; `CSL-0024` uses a constant coefficient).
  * **Data to merge, not cards:** six Copeland EN12900 coefficient sets (THC-006, into the TSP-006 card) and five oil tables of which only Mobiltherm and Therminol SP are absent from CoolProp (THC-007).
* **Reference results are scarce:** ThermoCycle stores none. Verification has to come from the original papers and reports (NREL/TP-550-34169 for the Forristal model, the NREL PTR70 heat-loss test, Shah 1982, Gungor and Winterton 1987, the ThermoCycle/ULiège publications), from an independent Python implementation with CoolProp, and from energy-balance closure. Each row says which.

## 6. Recommended cards

| # | ID | Candidate | Why it is new | Difficulty | Reference data |
|---|---|---|---|---|---|
| 1 | THC-001 | Forristal receiver (1D radial balance, steady) | first-principles collector loss, EES heritage, empty solar category | medium | NREL/TP-550-34169, PTR70 heat-loss test, energy balance |
| 2 | THC-002 | PT receiver and collector loss correlations (PTR70 x3, Sopogy, Soltigua) | measured-data fits, one family with LTP-050/LTP-020 | easy | NREL PTR70 report, datasheets, cross-check with THC-001 |
| 3 | THC-003 | ORC expander and pump empirical maps | map-based machines with filling factor, three technologies | easy | Python re-evaluation, thesis and paper of the docs |
| 4 | THC-004 | Shah 1982 + Gungor-Winterton + Cooper | Shah is absent from LTP-034; do after LTP-034/035 | easy-medium | original papers, Python and CoolProp |
| 5 | THC-005 | In-cylinder HTC correlations | no in-cylinder correlation in the library | easy | original papers, Python |

## 7. Translation guidelines specific to ThermoCycle

1. **Steady state = `der(x) = 0`.** Drop `initial equation`, `steadystate_*`, `cardinality`, `inStream`, flow-reversal branches, `homotopy`, `noEvent` and `smooth`. The regularisation functions (`regPow`, `regSquare`, `regRoot`, `transition_factor`, `weightingfactor`) exist for the dynamic solver: use plain powers, and keep a smooth blend only where a regime switch would stall the Newton iteration (Shah, Adair, Re-dependent constants of Forristal).
2. **Properties:** `Medium.setState_ph/ps/pT`, `density`, `specificEnthalpy`, `dynamicViscosity`, `thermalConductivity`, `prandtlNumber`, `setBubbleState/setDewState` become EES property calls with (P, H), (P, S), (P, T) or (P, x) pairs (decision D11: no (T, H) pair). ExternalMedia options such as `|calc_transport=1` disappear.
3. **Units and conventions:** SI throughout, but temperatures in K in the radiation and free-molecular terms (`T^4`, `T_g_t`, mean free path) and `Eps_t(T - 273.15)`; angles in rad (CoolSolve trigonometry is in degrees); Forristal vacuum pressure through mmHg; screw maps use p in bar and speed in rpm inside the polynomials; EN12900 in degF and lbm/h; N_rot in Hz in the machine models and rpm in the maps; HL correlations use T in degC.
4. **Arrays** (`[N]` cells of the absorber) become `DUPLICATE` loops; the Forristal receiver is first translated as one cell at a given tube temperature.
5. **Clamps** (`min`, `max` of the maps and of the Reynolds regimes) are non-smooth: keep them, or replace by range checks documented in the README.
6. Fluid names for the EES translation: `R245fa`, `R134a`, `R407C`, `Water`; the Modelica test fluids are R245fa, R134a, R407c, water (R718) and air.

## 8. Check before trusting a file (found during the sweep)

* `SolAbsForristal.mo`: radiation term uses `Eps_t[N]` instead of `Eps_t[i]`; the Re-dependent `C`, `m` are non-smooth `if` chains of strict inequalities that fall through to the last branch at exactly Re = 40 and Re = 1000; the optical parameters have no default.
* `Geometry/Schott_SopoNova/SopoNova.mo` and `Schott_2008_PTR70_Hydrogen.mo` hold identical coefficients; `Geometry/Soltigua/BaseGeometry.mo` has `A_3 = -2-6.94444444E-07`; `AbsSoltigua.mo` seems to count the 0.64 W/(m2 K) loss twice.
* `Functions/Enumerations/ExpTypes.mo` has no `ORCNext` value, yet `Examples/Simulations/step_by_step/ORC_245fa/step9.mo` (and probably the other steps) use it: the step-by-step examples are stale.
* `TwoPhaseCorrelations/GungorWinterton1987.mo` names its reference anchor `Shah1982`; `Reciprocating/HeatTransfer/Destoop1986.mo` cites Annand 1963 (copy-paste of the reference).
* `Media/Incompressible/IncompressibleTables/Therminol66`: cp(20 degC) = 1008.4 is a density value; `FlueGas.mo`: density column is 1/1287... under a "kg/m3" comment (it is kg/L).
* The polynomial maps of `Functions` have no documented validity range: the hermetic-scroll `epsilon_s` is -1.6 at rho = 10 kg/m3 and pressure ratio 2 before its clamp.
* Licensing is not uniform (see section 1).
