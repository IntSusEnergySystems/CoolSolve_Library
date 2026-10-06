# thermo_models - sweep of the private EES model collection

Quick automated sweep (not an audit) of `~/Nextcloud/thermo_models/` (Prof. S. Quoilin; ULiège Thermodynamics Laboratory and teaching material) to produce a **backlog for the CoolSolve_Library**. Source folder untouched (read-only), nothing extracted to disk.

| file | role |
|---|---|
| `inventory.csv` | one row per model file, 29 columns (the 24 columns of the sweep + `ees_units`, `stored_solution`, `tables`, `decision`, `library_id`), UTF-8 |
| `sweep.py` | dependency-free, re-runnable extractor + duplicate grouping + heuristic classification (`python3 sweep.py --stats`, about 2 s) |
| `curation.csv` | manual curation layer applied by `sweep.py` (English title/description, category, kind, level, priority, licence, notes; one row per duplicate group or file, keyed by `path`). Delete it and the script falls back to raw comment titles and keyword heuristics |

> **Maintainer decisions (2026-10-04) — they supersede the licence triage of this sweep.**
> - Every file of this collection comes from the maintainer's laboratory and may be published
>   under the library license (MIT): `license_status` is `own` for all rows. The provenance
>   notes below are kept to **credit the authors** (find the author in the file; initials:
>   `SB` = Stéphane Bertagnolio, `VL` = Vincent Lemort; otherwise `TBD`, completed by the maintainer).
> - **Exams** are published as examples. An exam built on an exercise with a few values changed
>   is a `duplicate` of that exercise; the August 2022 resit questions (Q1–Q10) form one example
>   model. Student answers (June 2019 MCI exam) are excluded and their file names redacted.
> - Source files are not copied into the library: models reference them by path (`~/Nextcloud/thermo_models/...`).
> - Models in another unit system are converted **by hand** (CoolSolve `docs/ees_import.md` §6).

## 1. Scope and conventions

* **552 rows**: TM-0001..TM-0465 = every `.ees` (457), `.lib` (1) and `.lkt` (7) file on disk; TM-0466..TM-0552 = **87 extra rows for `.ees/.lib/.lkt` found only inside `.zip` archives** (read in memory; `path` = `<zip path>!/<member>`; mostly the Model data bank reference models and 2009-2010 exercise sets). A further 167 zip members with identical equations text (identical bytes for `.lkt`) to an already listed file were dropped; 45 macOS `._*` members ignored. The 3 `.rar`/`.7z` archives are not scanned (their EES members duplicate on-disk files).
* Reading rule: header byte 0 = version string length, uint32 at offset 16 = length of the Equations-window text (cp1252, 24 on-disk files stored as RTF, 1 file as UTF-16). The rest of the binary (parametric tables, plots, Diagram Window, unit settings) is **not** decoded: it is mostly memory dump. No `Minimize/Maximize` string exists in the binary part of any file (`MinMaxVar` is boilerplate), so optimisation hints come from comments only.
* `n_equations` = code lines containing `=` outside FUNCTION/PROCEDURE bodies (MODULE/SUBPROGRAM bodies count), DUPLICATE loops counted once; `n_lines` = lines of the equations text. `unit_hints`: bracket units found (most frequent first), `+273.15` = manual K/C conversion, `~T:C`, `~p:kPa`... = weak magnitude-based inference. No file contains a `$UnitSystem` setting in the text except 7 MCI files, so the EES unit system of most files is unknown (check before translating).
* **Duplicates**: exact = same normalised code (comments/spaces/case/locale removed); near = Jaccard >= 0.6 on normalised code lines; connected components. **118 duplicate groups** (`DG-xxxx`) cover 329 rows; 223 rows are singletons (`duplicate_group` empty). One representative per group (`is_representative=yes`, best documentation, then newest EES version/mtime; 341 representatives overall = number of distinct models); 64 non-representatives have identical equations (priority `skip`), the others are variants (`low`). Near misses (0.45-0.6) are listed in `notes` as "similar but not grouped".
* `doc_quality`: 0 none, 1 minimal (>= 8 comment words), 2 good (>= 60 words and >= 5 % of text, or >= 120 words), 3 excellent (>= 300 words and >= 15 %). `priority`: `wave1` (best first candidates), `high`, `medium`, `low` (redundant/trivial/variant), `skip` (identical copy, empty, scratch, student work). `license_status`: see section 2.
* Titles, descriptions, category/kind/level/priority were curated from a skim of titles, comments and code heads (not by running the models): treat them as a guide, not as validated facts. Language labels: fr / en / `en+fr` / none (no comments) / unknown.

* Columns added after the sweep (filled when the CoolSolve repository is next to the library): `ees_units` = unit system decoded from the binary (`SI MASS DEG PA C J` for 288 of 540 EES files; 248 use kPa/kJ and/or K; `+decimal-comma` for 230 files written with the European number format), `stored_solution` = variables with a value stored by EES / variables decoded (the EES reference for verification), `tables` = embedded lookup/parametric tables; `decision` and `library_id` = workflow columns (see `docs/model_workflow.md` §2), preserved when `sweep.py` is re-run.
* **`tables` and `stored_solution` come from a heuristic binary decoder and can be wrong.** Known false positives: TM-0413 (`parametric:table1(761x2)` is not the 18 001-row integral table, which was recovered from the plot objects of the file) and TM-0326/TM-0263 (the former `74x2` was a mis-decoded pair of string-keyed lookup tables, hand-decoded as `activite` 7x2 and `veture` 6x2: CoolSolve `CS-BUG-EXTRACT-LOOKUP-STRING`; the cells were corrected). Before relying on a decoded table, check it against the EES file (row/column counts and values used by the equations, plot objects, or a hand decoding) and say in the model README how it was verified (`docs/model_workflow.md` §3, step 1).

## 2. Sub-folders: origin, authors (licence notes superseded, see the box at the top)

| Sub-folder | rows | on disk + in zip | unique reps | reps by level 1/2/3/4 | licence own/unclear/needs-perm. | priority wave1/high/medium/low/skip |
|---|---|---|---|---|---|---|
| `Model data bank` | 40 | 13 + 27 | 31 | 12/16/3/0 | 1/39/0 | 13/7/10/7/3 |
| `modeles` | 67 | 63 + 4 | 42 | 17/16/8/1 | 9/22/36 | 9/7/18/27/6 |
| `machines et systemes thermiques` | 183 | 180 + 3 | 92 | 50/42/0/0 | 0/183/0 | 1/7/38/121/16 |
| `MCI_REMIDICKES` | 71 | 70 + 1 | 48 | 26/21/1/0 | 0/0/71 | 0/3/15/8/45 |
| `thermo_kuleuven` | 30 | 30 + 0 | 27 | 26/1/0/0 | 0/0/30 | 0/0/10/20/0 |
| `thermodynamique appliquee` | 161 | 109 + 52 | 101 | 77/24/0/0 | 109/52/0 | 15/13/41/68/24 |

* **`Model data bank/`** - copy of Jean Lebrun's *Banque de modèles de simulation* (ULiège Thermodynamics Laboratory, 2007-2008; concept note `Presentation_banque_modeles_JL070710.doc`, catalogue `modeles/listing_database_models.xls`). Not downloaded from a third party: the 28 `index.php` are generic directory-listing scripts of the lab web server (www.labothap.ulg.ac.be), i.e. a mirror of the lab site. HVAC/energy component "RefSim" (reference simulation) and "ParamID" (parameter identification) models with control-panel inputs/outputs, by V. Lemort, S. Bertagnolio, J. Lebrun, V. Teodorese, A. Rodríguez, C. Da Silva, C. Cuevas (Univ. de Concepción, 3-zone condenser), S. Quoilin; PDFs labelled "IEA A43 PR2 Axx" are the matching reports. 33 rows (24 here, the rest copies in `modeles/`) carry the disclaimer *"freely distributed and may not be sold; cite the origin"* (attribution required, resale forbidden: not a standard open-source licence -> `unclear`). Two third-party PDFs (Pilavachi et al., HeatSET 2007; IBGE) are copyrighted and not models. Only 13 files are on disk (12 `.ees` + the `cpbar` `.lib`): the other 27 rows come from its 27 zip files (the 3 `.exe` runtimes are ignored). Top documentation quality of the whole collection.
* **`modeles/`** - working copy/superset of the model bank plus related lab models: `LABORELEC_2002` (F. Trebilcock, Dec 2002, reviewers J. Lebrun and E. Winandy: toolkit for Laborelec, polynomial compressor/pump/fan models, pressure drop, evaporative condenser/cooling towers, with Word reports, Excel catalogue data and 6 `.lkt`; client work -> `needs-permission`); `JL/new` (J. Lebrun, Feb 2008, reciprocating/screw/scroll compressor reference models, zipped); Quoilin's models (ORC 2009/2012, expander 2008, discretised HX, plate HX and thermal comfort with Bertagnolio/Lebrun); V. Lemort's inverter heat pump (2007, 560 equations) and pipe pressure drop (2006); PV model (author not identified); economic evaluation (S. Bertagnolio). `simple_ORC_model SQ120220` carries an explicit free-use-with-credit statement.
* **`machines et systemes thermiques/`** (MSTh, course MECA0006) - ULiège course (lecture notes by J. Lebrun 2005, J. Lebrun and V. Lemort 2007; course code MECA0006 per the `Labo cp` files), 13 exercise sessions (TP01-TP13, 2004-2006) with EES solutions by V. Lemort (`VL`, statement in the comments), S. Bertagnolio (`SB`), J. Lebrun (revision files `JL051223`), unidentified `JD`, and one S. Quoilin file. French, level 1-2, semi-empirical component models (compressors, turbomachines, coils, cooling towers, boilers, engines, gas turbines, refrigeration, LiBr absorption). Extremely redundant: 92 distinct models for 183 files. Colleagues' teaching material -> `unclear`.
* **`MCI_REMIDICKES/`** - "Moteurs à combustion interne" (ULiège) of Prof. Ph. Ngendakumana (Thermotechnics Unit; file tag `PNG`, EES licence #3804) with assistant Rémi Dickes (`RD`), 2016-2019: TP1-TP7 (combustion/dissociation, ISO 3046 derating, engine parameters, turbocharging, valves, injection, emissions), 2 labs (engine test bench; 68 `.asc` cylinder-pressure vs crank-angle traces), June 2019 exam (**21 student submissions** + teacher solutions) and student lab reports. The student files contain personal data (names in file names): excluded and redacted; the teacher solutions (`TM-0223`, `TM-0224`) are publishable as examples. Uses EES built-in `NASA`/`Chem_Equil` procedures and an external `HSCmHnPRODCOMB` library.
* **`thermo_kuleuven/`** - KU Leuven thermodynamics course 2018-2020 (slides chapters 1-10, textbook PDF of Çengel & Boles 8th ed. = copyrighted) with 30 terse EES solutions of textbook problems named by chapter-problem number (`07-34.EES`); EES stamp user "Sylvain" on the ULiège licence, i.e. written by S. Quoilin as lecturer. English, level 1. Statements/numbers come from the textbook and the course belongs to KU Leuven -> `needs-permission`.
* **`thermodynamique appliquee/`** - ULiège course MECA0002 *Thermodynamique appliquée*: `2022-2023` (R1-R12 repetition solutions, very well documented, French) and `Aout 2022` (resit-exam solutions Q1-Q10 on an ORC + heat-pump system) -> `own` (per companion Python/Word metadata the repetitions were prepared with assistants N. Paulus and B. Dechesne: confirm); `2017-2018` mostly holds 2009-2010 THD exercise sets by S. Bertagnolio and S. Borguet (zipped; plus two 2017 files) -> `unclear`. Statements follow the French edition of Çengel (copyrighted text: paraphrase before publishing). Non-EES material: 326 Python scripts (CoolProp + `fsolve`, useful as **independent reference results** for validation), exams (janv. 2020/2021, août 2021), course PDFs and the textbook + solution manual (no EES inside).

## 3. Statistics (552 rows, 341 unique representatives)

| category_guess | rows | unique reps |
|---|---|---|
| engines | 95 | 51 |
| compressors | 73 | 41 |
| refrigeration_heat_pumps | 72 | 52 |
| fundamentals | 63 | 40 |
| hvac_psychrometrics | 57 | 39 |
| combustion_boilers | 33 | 18 |
| power_cycles_gas | 33 | 17 |
| power_cycles_vapour | 26 | 18 |
| expanders_turbines | 20 | 13 |
| valves_nozzles_piping | 16 | 13 |
| pumps_fans | 11 | 9 |
| absorption_sorption | 10 | 2 |
| heat_exchangers | 10 | 4 |
| buildings | 8 | 6 |
| cogeneration_energy_systems | 7 | 5 |
| properties | 7 | 5 |
| storage | 5 | 3 |
| solar_renewables | 3 | 2 |
| heat_transfer | 2 | 2 |
| misc | 1 | 1 |

| kind_guess | rows | unique reps |
|---|---|---|
| steady | 529 | 323 |
| dynamic | 6 | 4 |
| optimization | 4 | 4 |
| function | 3 | 2 |
| unknown | 10 | 8 |

| level_guess | rows | unique reps |
|---|---|---|
| 1 | 296 | 208 |
| 2 | 233 | 120 |
| 3 | 22 | 12 |
| 4 | 1 | 1 |

| priority | rows | unique reps |
|---|---|---|
| wave1 | 38 | 38 |
| high | 37 | 36 |
| medium | 132 | 127 |
| low | 251 | 110 |
| skip | 94 | 30 |

| license_status | rows | unique reps |
|---|---|---|
| own | 552 | 341 |

| doc_quality | rows | unique reps |
|---|---|---|
| 3 | 177 | 106 |
| 2 | 189 | 120 |
| 1 | 155 | 89 |
| 0 | 31 | 26 |

| language | rows | unique reps |
|---|---|---|
| fr | 395 | 228 |
| en | 124 | 88 |
| none | 16 | 14 |
| unknown | 13 | 9 |
| en+fr | 4 | 2 |

Distribution of main-body equations over `.ees` rows: median 34, 4 models above 200 (max 560); 106 representatives have excellent documentation. 37 rows are `high`.

## 4. Wave 1 - recommended first candidates (38)

Selection: representative, documented, one per distinct topic, mix of simple smoke tests and richer models. (The licence column shows the sweep's original triage; all rows are now `own`, see the box at the top.)

| id | title | category | lvl | licence | why |
|---|---|---|---|---|---|
| TM-0165 | LiBr-H2O absorption chiller cycle (MSTh R11 Ex1-4) | absorption_sorption | 1 | unclear | only sorption-cycle family (LiBr-H2O); needs LiBr-H2O properties that CoolProp lacks - good gap probe |
| TM-0251 | Centrifugal fan reference simulation model (dimensionless pressure/flow/power factors) | pumps_fans | 1 | unclear | 19 equations, excellent docs; dimensionless fan model, pairs with ParamID model TM-0485 |
| TM-0253 | cpbar: mean specific heat of CmHn combustion products and incomplete-combustion losses... | combustion_boilers | 2 | unclear | function library (PROCEDURE/FUNCTION) needed by 3 boiler models; tests user-function support |
| TM-0255 | ISO 5167 orifice plate (diaphragm) flow-rate calculation procedure | valves_nozzles_piping | 2 | unclear | standard (ISO 5167) flow-metering with PROCEDURE/MODULE/CALL and FluidProp property calls |
| TM-0266 | Three-zone condenser parametric model: counterflow, crossflow and combined flow (R134a,... | heat_exchangers | 3 | unclear | level-3 heat exchanger, 3 flow configurations, procedures, 6 copies; external author (Cuevas) |
| TM-0270 | Economic evaluation of energy-saving investments: NPV and simple payback | cogeneration_energy_systems | 2 | unclear | distinct topic (NPV/IRR economics): arrays with i-1 indexing, no fluid properties |
| TM-0272 | Simple scroll expander model as an EES MODULE: supply pressure drop and cooling, isentr... | expanders_turbines | 3 | own | own; EES MODULE for a scroll expander - building block for ORC cycles |
| TM-0314 | Low-temperature ORC (R134a) with detailed components and heat-exchanger volumes (void-f... | power_cycles_vapour | 3 | unclear | level-3 complete low-T ORC with exchanger volumes/void-fraction charge (296 eq) |
| TM-0316 | Photovoltaic module single-diode model: I-V curve from module database | solar_renewables | 2 | needs-perm. | only PV model: lookup of module data, DUPLICATE I-V curve, ConvertTemp; copy stamped with U. Wisconsin SEL licence -> clear origin first |
| TM-0319 | Single-phase plate heat exchanger thermal-resistance model (Martin correlation) | heat_transfer | 2 | own | own; small PROCEDURE-based plate-HX correlation (Martin), well documented |
| TM-0321 | Air-to-air glycol run-around heat-recovery loop (epsilon-NTU coils, Braun hypothesis, p... | hvac_psychrometrics | 3 | unclear | documented HVAC run-around heat-recovery loop; 3 versions; needs BrineProp lib |
| TM-0324 | Simple ORC model for screening: R245fa cycle with hot-air source (Quoilin thesis) | power_cycles_vapour | 2 | own | own; explicit free-use-with-citation statement; ORC screening model tied to thesis |
| TM-0326 | Thermal comfort model: Fanger PMV-PPD | buildings | 2 | own | distinct buildings/comfort topic (Fanger PMV-PPD), own, lookups + arrays |
| TM-0378 | Rigid tank with liquid-vapour water mixture: liquid and vapour masses and volumes (exer... | fundamentals | 1 | own | simplest property-call exercise (level 1) - ideal first smoke test |
| TM-0389 | Steam turbine exergy balance: exergy destruction (3 MPa, 450 C, 8 kg/s) | fundamentals | 1 | own | compact exergy balance of a steam turbine, own, well documented |
| TM-0393 | Combustion of octane with 400% theoretical air: product composition, heat transfer and... | combustion_boilers | 1 | own | combustion stoichiometry and adiabatic flame temperature; excess-air parametric study |
| TM-0399 | Non-ideal gas v(P+k/v^2)=RT: unit of k and isothermal expansion work using EES integral | properties | 1 | own | user-defined equation of state + numerical integration (INTEGRAL) - solver feature probe |
| TM-0413 | Domestic hot-water storage tank (500 L): dynamic energy balance with tap draw, losses a... | storage | 1 | own | only own dynamic example (INTEGRAL/IntegralTable time integration of a tank) |
| TM-0422 | Two-stage compression of superheated steam: optimal intermediate pressure and isotherma... | compressors | 1 | own | two-stage compression with integral work and optimal intermediate pressure |
| TM-0429 | Air-standard Otto cycle: pressures, temperatures, net work, efficiency and engine power | engines | 2 | own | air-standard engine cycle with recursive cp(T); also holds the Diesel sister exercise |
| TM-0441 | Land-based two-shaft gas turbine: LP-turbine shaft power and overall efficiency | power_cycles_gas | 2 | own | two-shaft gas turbine, 93 eq, documented; parametric variants |
| TM-0442 | Ideal turbojet at 260 m/s: diffuser, compressor, combustor, turbine, nozzle | power_cycles_gas | 1 | own | jet-propulsion cycle: ideal turbojet with exhaust velocity and propulsion efficiency |
| TM-0443 | Rankine cycle of a 60 MW steam plant (70 bar, 500 C): flows, efficiency and condenser c... | power_cycles_vapour | 2 | own | baseline Rankine plant, 857 comment words |
| TM-0444 | Rankine cycle with steam extraction at 14 bar to an open feedwater heater (deaerator) | power_cycles_vapour | 2 | own | Rankine with extraction/open feedwater heater; builds on TM-0443; 5-file family |
| TM-0446 | Combined gas-steam cycle: Brayton topping cycle with heat-recovery Rankine bottoming | power_cycles_gas | 2 | own | gas-steam combined cycle (Brayton + HRSG + Rankine) |
| TM-0448 | R134a vapour-compression refrigeration cycle with subcooling and superheating: COP and... | refrigeration_heat_pumps | 1 | own | baseline R134a vapour-compression cycle (subcooling/superheat, ARRAYS) |
| TM-0449 | R410A heat pump: refrigerant flow, overall COP, evaporator air flow and isentropic effi... | refrigeration_heat_pumps | 2 | own | air-source R410A heat pump with air-side flow and compressor efficiency |
| TM-0451 | Moist air in a 5 m x 5 m x 3 m room: humidity ratio, dew point and water mass | hvac_psychrometrics | 1 | own | moist-air property calls (AirH2O vs Air_ha), dew point, water mass |
| TM-0471 | Cooling coil reference simulation model (RefSim): dry and wet regimes, one zone | hvac_psychrometrics | 2 | unclear | reference wet/dry cooling-coil model, Merkel/Braun theory, excellent docs |
| TM-0475 | Adiabatic humidifier simplified model (humidification effectiveness) | hvac_psychrometrics | 1 | unclear | 15 equations; adiabatic humidifier effectiveness model |
| TM-0481 | Scroll compressor reference model (Winandy et al.): heating-up, internal leakage, inter... | compressors | 2 | unclear | widely cited semi-empirical scroll compressor (Winandy et al.), 107 eq |
| TM-0487 | Centrifugal brine pump simulation model (RefSim) | pumps_fans | 1 | unclear | 16 equations; pump + hydraulic network reference model |
| TM-0488 | Air-cooled water chiller reference model: rotary compressors in cascade, condenser fan... | refrigeration_heat_pumps | 2 | unclear | system-level air-cooled chiller reference model (cascade compressors, fan control) |
| TM-0489 | Direct-contact cooling tower reference model | hvac_psychrometrics | 2 | unclear | direct-contact cooling tower reference model (wet-coil theory) |
| TM-0490 | Vertical ground-loop heat exchanger (borefield) model with heat pump: g-function superp... | solar_renewables | 3 | unclear | dynamic multi-year borefield model with PROCEDURE/FUNCTION, IntegralTable |
| TM-0492 | Classical fuel-oil heating boiler with ON/OFF control: simulation reference model | combustion_boilers | 2 | unclear | fuel-oil boiler with on/off control; uses cpbar library |
| TM-0494 | Condensing boiler reference model: five-step combustion, dry and wet gas-water exchange... | combustion_boilers | 3 | unclear | level-3 condensing boiler: SUBPROGRAM/FUNCTION/PROCEDURE, 2158 comment words |
| TM-0495 | Brine-to-water heat pump reference model: scroll compressor, brine evaporator, water co... | refrigeration_heat_pumps | 2 | unclear | ground-source heat pump: scroll compressor + brine evaporator + condenser |

## 5. Notable special cases

* **Lookup tables (.lkt)**: TM-0225, TM-0298, TM-0299, TM-0308, TM-0310, TM-0311, TM-0313, TM-0477, TM-0478 (binary; pipe fittings/pipe data, cooling-tower and condenser catalogue data, brine data, one student data set). 24 representatives also use `LOOKUP`/`INTERPOLATE`; some tables live *inside* the `.ees` (e.g. `PVModules`, `Tprofile`) and are not extractable from the text: they are decoded from the binary by CoolSolve `tools/ees_extract.py` (column `tables`). Standalone `.lkt` files are not decoded yet.
* **Function libraries**: TM-0253, TM-0479, TM-0480 (`cpbar` combustion-product cp; `BrineProp`/`BrineProp2` brine properties, compiled-style `.lib`). Models needing them say so in `notes` (`cpbar`: TM-0491/0492/0493; `BrineProp`: TM-0319/0321/0470/0471/0486/0487/0495). 23 representatives define FUNCTION/PROCEDURE/MODULE/SUBPROGRAM.
* **Dynamic models** (`INTEGRAL`/`$IntegralTable` over time): TM-0095, TM-0104, TM-0413, TM-0490 (storage tanks, borefield). `INTEGRAL()` is also used for plain work integrals in TM-0399/0420/0422/0431 (steady).
* **Optimisation / identification hints**: TM-0268, TM-0290, TM-0293, TM-0295 (error minimisation to identify exchanger resistances; `optim` summary table in TM-0268). Many "PARAMID" models are parameter *identification* by solving at measured points (steady). Parametric tables are used instead of optimisers elsewhere.
* **Very large models**: TM-0268, TM-0274, TM-0314, TM-0494 (TM-0274 is the only level-4: 560 equations, 57 FUNCTIONs, 2 SUBPROGRAMs).
* **External/EES-specific dependencies**: REFPROP (TM-0268), FluidProp/StanMix (TM-0255/0256/0323), EES built-ins `NASA`, `Chem_Equil` (MCI TP1, no CoolProp equivalent), `$INCLUDE` of unavailable libraries (TM-0240, TM-0494), Diagram-Window/control-panel models (TM-0297, 0300 keep part of their equations in `{$DS.}` `.TXT` snippet files listed in `companion_files`; TM-0321 and the other model-bank panel models use the control panel), pipe procedures calling `Colebrook` (not defined in the file; EES library procedure). Water-glycol/LiBr/NH3-H2O mixtures need non-CoolProp property work.
* **Stored differently**: 24 on-disk RTF files, 1 UTF-16 file (TM-0419), 2 near-identical files saved as `~` EES backups.

## 6. Taxonomy gaps and suggestions

* No home for **economics/NPV** (TM-0270/0271 sit in `cogeneration_energy_systems`), **flow metering/instrumentation** (ISO 5167 in `valves_nozzles_piping`), **thermochemistry/chemical equilibrium** (MCI TP1 in `combustion_boilers`), **ground-source/geothermal** (borefield in `solar_renewables`), **evaporative cooling equipment** (cooling towers/evaporative condensers in `hvac_psychrometrics`), **controls/regulation** (cooling ceiling, boiler on/off, thermostatic valve), **terminal units** (radiator, cooling ceiling in `buildings`).
* `kind_guess` has no value for **parameter identification/calibration** (PARAMID, catalogue-data fits): proposed tag `calibration`; `dynamic` also covers quasi-steady parametric time series only when INTEGRAL is used.
* `fundamentals` (40 representatives) mixes closed-system first-law, exergy, Carnot and property-evaluation exercises; `engines` is large mainly because of the MCI course. Poorly covered: `heat_transfer` (only the plate-HX correlation model TM-0319/0496: no fin/conduction/convection exercises), solar/renewables (PV + borefield), absorption (LiBr only), buildings (6, mostly terminal units and Carnot house exercises), storage (3 distinct), valves/nozzles/piping (13, mostly standards and pressure-drop procedures).

## 7. Caveats and next steps

* Licences: superseded by the maintainer decision (box at the top): all rows `own`, published under MIT with credits to the authors listed in the provenance notes.
* Student exam submissions (MCI exam, June 2019; 42 rows) are classified by a rule of `sweep.py` (`PERSONAL_DIRS`) and their **file names are redacted** in `inventory.csv` (`[redacted TM-xxxx]`); `curation.csv` contains no personal data. Keep it that way when adding curation rows.
* Several teaching files embed textbook statements (Çengel/Boles; Pulkrabek in MCI): paraphrase and keep only data/solution structure.
* Candidate ids are **stable** (since 2026-10-06): when `inventory.csv` exists, a path already inventoried keeps its TM id (personal files: the k-th file of a folder keeps the k-th redacted id), a zip member dropped as a copy of a new disk file passes its id to that file, and new files get the next free ids (appended at the end). Duplicate groups keep their DG id (a new group gets the next free DG id) and their representative. Rows already in the inventory are kept as they are (workers' notes and decisions included); only a duplicate-group change is recorded in `notes`. Blank runs in paths are collapsed when matching. `curation.csv` is keyed by path (not by id). If the tree changes, check the warnings printed for unknown keys and lost ids. First incremental run: 2026-10-06 (+50 rows TM-0553…TM-0602, see B-10 in the roadmap).

## 8. 2026-10-06 additions (TM-0553…TM-0602)

Triage of the 50 rows the re-run of `sweep.py` appended for the folders `procedures EES/`
(32 rows), `Steady-state models/` (10), `optim/` (4) and `solar/` (4). Every row was compared
by its **equations** (comments and blanks stripped, `tools/ees_extract.py` output in
`work/triage/`, deleted afterwards) with the rows of its duplicate group, with the earlier
copies of the same files (`Model data bank/`, `modeles/`) and with the 80 library models
(`library.csv`, `functions.csv`). No model folder is created by this card.

### Counts

| Decision | Rows | Members |
|---|---:|---|
| `todo` (worth importing) | 22 | TM-0554, 0558, 0559, 0560, 0563, 0564, 0565, 0566, 0569, 0570, 0571, 0574, 0575, 0579, 0581, 0582, 0585, 0587, 0588, 0589, 0593, 0596 |
| `duplicate` | 18 | TM-0555, 0556 (of TM-0268), 0561 (of TM-0496), 0562 (of TM-0563), 0576/0577/0578 (of TM-0255/0256/0257 → CSL-0075), 0583, 0584 (of TM-0585), 0590, 0592 (of TM-0316/0317), 0594 (of TM-0564), 0595 (of TM-0569), 0598 (of TM-0275), 0599 (of TM-0272 → CSL-0037), 0600 (of TM-0314), 0601 (of TM-0319), 0602 (of TM-0324 → CSL-0019) |
| `discarded` | 8 | TM-0553, 0567, 0568, 0586 (binary `.lkt` lookup tables, not models), 0557 (generic statistics helper on the lab data), 0572 (trivial moist-air density, covered by CoolProp `AirH2O`), 0573 (throat `SUBPROGRAM` fragment, superseded by CSL-0037 / TM-0593), 0580 (LMTD experiment file: the alternatives are noted as non-working in the file) |
| `merged` | 1 | TM-0597 → CSL-0037 |
| `parked` | 1 | TM-0591 (SETP library, third party) |

Per folder: `procedures EES/` (32) 18 `todo`, 7 `duplicate`, 7 `discarded`;
`Steady-state models/` (10) 2 `todo`, 7 `duplicate`, 1 `merged`; `optim/` (4) 1 `todo`,
2 `duplicate`, 1 `discarded`; `solar/` (4) 1 `todo`, 2 `duplicate`, 1 `parked`.

### Proposed cards (roadmap §6, B-10)

```
[ ] C-122 T-FUNC   TM-0585,TM-0496                       → components/heat_exchangers/plate_hx_correlations   — plate-HX correlations: 10 procedures (bogaerts, han, hsieh, kumar, kuo, martin, muley, thonon, wanniarachchi, yan); verification: TM-0585 stored solution + ht HT-005/HT-010 Python values
[ ] C-123 T-FUNC   TM-0564,TM-0569,TM-0579,TM-0566,TM-0571 → components/heat_exchangers/three_zone_hx_procedures — 7 procedures (hx_cd, hx_ev, lmtd, single_phase_HX, EV, CD, evaporator2); verification: stored demo cases of TM-0564/TM-0569 (energy balance) + ht HT-004 epsilon-NTU
[ ] C-124 T-IMPORT TM-0563                               → components/heat_exchangers/condenser_3_zones_plate_correlations — three-zone plate condenser, Thonon/Kuo, R123+glycol (REFPROP variant TM-0562 described); verification: EES stored solution
[ ] C-125 T-IMPORT TM-0570 (auto-size variant TM-0582)   → components/heat_exchangers/evaporator_3_zones_plate_correlations — three-zone plate evaporator, Thonon/Hsieh, R245fa+glycol+oil; verification: EES stored solution + TM-0582 parametric table
[ ] C-126 T-IMPORT TM-0575                               → components/heat_exchangers/hx_fem_evaporator_discretised — discretised hxfem evaporator, the smoothed revision of TM-0275; verification: EES stored solution
[ ] C-127 T-IMPORT TM-0596                               → cycles/refrigeration_heat_pumps/heat_pump_vitocal_300g — scroll compressor + two plate HXs, glycol/water (needs CSL-0079 and the expander of TM-0597/CSL-0037); verification: EES stored solution
[ ] C-128 T-IMPORT TM-0565                               → components/expanders_turbines/double_stage_scroll_expander — two-stage hermetic scroll expander (Lemort/Quoilin/Pire correlations, MODULE); verification: EES stored solution
[ ] C-129 T-IMPORT TM-0593                               → components/valves_nozzles_piping/air_nozzle_ejector — air ejector with choked primary nozzle and entrainment; verification: EES stored solution
[ ] C-130 T-IMPORT TM-0589                               → renewables/solar_thermal/solar_geometry_sun_path — solar geometry (declination, hour angle, altitude, azimuth, sunrise); verification: EES stored solution
[ ] C-131 T-IMPORT TM-0588                               → components/valves_nozzles_piping/ball_valve_authority — equivalent opening diameter and valve authority from the ball angle; verification: EES stored solution + Idel'cik Memento p.339
[ ] C-132 T-FUNC   TM-0574                               → fundamentals/properties/heat_transfer_fluid_properties — prop_htf: MEG, Therminol VP-1/66, oil (companion of CSL-0079); verification: HEDH HTF-VP1 data sheet values
[ ] C-133 T-FUNC   TM-0558,TM-0559,TM-0587,TM-0581         → components/instrumentation/nozzle_discharge_coefficients — ASHRAE 41.2 / ISO R859 (4 nozzles), ISO 5167 long radius, admission procedure, range checker; verification: shared ISO 5167 part vs CSL-0075 + ASHRAE 41.2 tables
[ ] C-134 T-FUNC   TM-0560                               → components/compressors/copeland_catalogue_correlation — third-order ARI/Copeland polynomial for ZH38K4E-TFD (W, M coefficients + Vs in five 242x2 tables); verification: EES stored solution
[ ] C-135 T-IMPORT TM-0554                               → heat_transfer/pressure_drop/plate_hx_pressure_drop_identification — plate-HX pressure drops identified with REFPROP mixtures (likely blocked); verification: EES stored solution
```

### Notes for the import cards

* **Function names must be unique in the library** (workflow §4.4). `warning_error`
  (CSL-0075), `fluidprop` (CSL-0075), `single_phase_HX`, `lmtd`, `hx_cd`, `hx_ev`, `thonon`,
  `kuo`, `hsieh`, `martin`, `prop_htf`, `copeland` are already used by other models or by
  copied library blocks: rename them per file (`warning_error_ashrae`, `lmtd_xi1000`, …) or
  prefix them with the file name.
* **C-122 overlaps the `ht` batch** (cards C-105/HT-010 plate-HX correlations, C-107
  two-phase). The lab file adds Thonon, Kuo-Lie-Hsieh-Lin, Han, Wanniarachchi, Yan and
  Bogaerts, which `ht` does not have; the Martin, Kumar and Muley-Manglik formulas are
  common. Decide whether the lab procedures are merged into the `ht` plate-HX file or kept
  as a lab function model (the two libraries then coexist).
* **C-123** contains a genuine bug of TM-0566 (`cp_cf = specheat(hf$,…)` — the cold-fluid
  capacity is taken on the hot fluid) and three procedures with no demonstration program
  (the stored solution could not be decoded, EES X8.198 layout): write the main program and
  verify against a CoolProp recomputation.
* **C-127** needs `BrineProp` (CSL-0079, blocked), the `Expander` procedure of TM-0597
  (merged into CSL-0037 → copy the block, `CS-FEAT-IMPORT`) and the external `ev` lookup
  tables (`TM-0567`, `TM-0568`, which are data files of the models, not models themselves).
* **C-130** calls the EES built-in `nDay_(month, day)`; if CoolSolve has no equivalent,
  replace it by an explicit day-number expression (log it in the conversion log).
* **C-126 is the preferred revision of TM-0275** (whose copy TM-0598 is an exact duplicate):
  it smooths the three U-value transitions over `width = 0.1` of the length, which the file
  itself names as the fix for the non-convergence problems, and its demo case is the
  validated R245fa/air_ha one. When C-126 is done, TM-0275 should become a duplicate.

### Open questions for the maintainer

1. **TM-0591 (`solar/SETP.LIB`) is parked**: the file is the SETP library (Duffie &
   Beckman, *Solar Engineering of Thermal Processes*) with renamed functions
   (`EqnTime_`, `AveDay_`, `CheckTemp_`, …), 69 procedures in 2724 lines of commercial code
   distributed with the textbook — the licence does not allow publication under MIT.
   Confirm, or ask the author of the derived file for permission.
2. **PV models (TM-0316/0317 = TM-0590/0592)**: the two copies of `PV_model.EES` /
   `TandS_Imput_IV_Model_Output_RsAdjust.EES` are identical, and one of them carries the
   *Solar Energy Laboratory, University of Wisconsin* licence stamp, so the origin is
   third party. Nothing new in the 2026-10-06 copies; the licence question of TM-0316 is
   still open (kept `todo`, no card proposed here).
3. **`optim/R245fa SQ101129` (TM-0555, TM-0556)** are byte-equivalent to TM-0268 apart from
   `;`/`,` separators in `$COMMON`; the three REFPROP-based ORC rows (TM-0268, TM-0555,
   TM-0556) remain one candidate. Importing it means a `blocked` model (`CALL EES_REFPROP`).
4. **TM-0574 (`prop_htf`)** overlaps CSL-0079 (brines, `blocked`): do we want two
   secondary-fluid property models, or should the Therminol/oil correlations be added to
   CSL-0079?
5. **Authors**: the `procedures EES/`, `optim/` and `Steady-state models/` files carry the
   *J. Lebrun lab* licence stamp only; `TBD (<ULiège, J. Lebrun laboratory>)` would have to
   be completed by the maintainer (TM-0565/TM-0575/TM-0561/TM-0574 name S. Quoilin in the
   file or are signed `SQ`).
6. **`identification pressure drops` (TM-0554)** is kept `todo` but ranked last: it needs
   REFPROP mixtures (`R245fa+R134a`) that CoolProp cannot provide, so an import would be a
   `blocked` model with no faithful runnable variant.
