# ees_library - the F-Chart EES example library (new source, triaged 2026-11-11)

`~/Nextcloud/thermo_models/EES_library/` (added by the maintainer) is the set of
**example files shipped with EES** (F-Chart Software / S. A. Klein): 124 files —
122 EES files (121 `.ees`/`.EES` + 1 `.lkt`) and 2 non-EES companions
(`EESDDE.xls`, `Excel_ws1.xlsx`, used by the Excel/DDE demos, not inventoried).
The `$ID$` stamps inside the files are EES *licence* stamps of whoever saved them
last (mostly S. A. Klein; a few third-party stamps and two cracked-EES stamps) —
not authorship statements: the examples are © F-Chart Software.

| file | role |
|---|---|
| [`inventory.csv`](inventory.csv) | one row per EES file (122 rows, `EEL-001`…`EEL-122`, same 29 columns as `sources/thermo_models`), decisions and priorities of the 2026-11-11 triage |
| [`curation.csv`](curation.csv) | the manual triage layer (one row per file, keyed by path), applied by the sweep |
| [`make_inventory.py`](make_inventory.py) | re-runnable builder: runs `sources/thermo_models/sweep.py` on the source folder (read-only), applies `curation.csv`, renumbers the ids to `EEL-nnn`, preserves the workflow columns of an existing `inventory.csv` |

Refresh: `python3 make_inventory.py` (about 2 s; needs no network and does not
touch the source folder).

## 1. Licence — largely resolved by the official MIT mirror (2026-11-11)

All files are **© F-Chart Software** (authors S. A. Klein and co-workers), the
example set distributed with EES. `license_status = fchart-mit` for every row.
**Finding of 2026-11-11:** F-Chart publishes the same examples under **MIT** in
its official GitHub organisation — [EES-Community/ees-examples]
(https://github.com/EES-Community/ees-examples) (clone 5c703d0, 2026-03-01;
`LICENSE` "Copyright (c) 2026 ees-examples contributors", MIT; plain-text `.ees`
files, each with a download link to `fchartsoftware.com/ees/examples/…`).
113 of the 121 local files match a repo file by (normalised) name — the local
binary versions carry the stored EES solution, the repo versions are plain text
(fewer binary artefacts; text comparison of the few RTF-stored locals was not
byte-exact). Only
`Animation`, `MakePlot`, `Link_Return`, `Excel_ees`, `psych` (→ `psych_calculator`),
`2-D Conduction (1)`, `Indicated power (1)`, `Regen_minmax (1)` lack an exact-name
match). Pending the maintainer's confirmation, imports can therefore reference
the MIT repo path *and* the local binary original (stored solution!), and be
published under MIT with credit "© F-Chart Software / S. A. Klein, MIT via
EES-Community/ees-examples".

**The MIT repo also contains 366 files that are NOT in the local folder** (479
tracked plain-text `.ees`, 113 matched → 366 repo-only; 331 *distinct* by
normalised name — about 35 are intra-repo duplicate variants, mostly
trailing-underscore copies such as `example_3.5-2_…_revisited.ees` and
`…_revisited_.ees`). Breakdown of the 366: `Case_Study` 299 (the Nellis &
Klein *Heat Transfer* (2009) / *Introduction to Heat Transfer* textbook
examples `example_*`, served from `examples_heat_transfer_2009`, and the
Herold/Radermacher/Klein *Absorption Chillers and Heat Pumps* (CRC 2015)
examples `ex*`), `uncategorized` 29 (real models: `brayton_cycle`,
`recompression_cycle`, `refrigerator_captube/evapcond`, `pump_curve`,
radiation/fin exam models…), `Properties` 2 (`iceproperties`, `psych_calculator`),
`Statics` 2 (`$Vector2D` equilibrium, Gray/Costanzo/Witt/Plesha 2023) and 34
further feature/plot demos (expected discard, like their local counterparts).
That sweep is a separate task (roadmap B-22, card C-519); statements remain
copyrighted by the books (paraphrase + credit, as for `thermo_kuleuven`).

**`ees-examples-raw.zip` (33.6 MB, repo root) — the raw originals.** 488
members: **280 `.eez`** (EES zip-wrapped binary files — the *stored solutions*,
parametric/lookup tables, plots and diagram windows) + 176 `.ees` + 10 nested
zips. The inner paths give the provenance of each example
(`D:\EES_stuff\Examples\Heat Transfer (2021)\Chapter 8\…`,
`C:\Temp\Heat Transfer Examples\Chapter 7\…`), i.e. which book edition and
chapter it comes from. The plain-text `.ees` files carry no stored solution, so
**the `.eez` set is the verification reference for the repo-only models** and
the source of their companion lookup tables (extract with
CoolSolve `tools/ees_extract.py` after unzipping the wrapper).

## 2. Triage rules (2026-11-11)

Following the maintainer's guidance — *"many of the models there are macros or
features that we don't want to support in CoolSolve, they can be discarded"* —
every file was read (equations text extracted from the binary; 3 735 code lines
in total) and classified:

| decision | rows | content |
|---|---:|---|
| `todo` | 38 | real physical models worth importing (table §4) |
| `discarded` | 79 | EES **feature demos**: language directives (`$IF`, `$EXPORT`, `$Constant`…), plotting, regression/curve-fit, uncertainty propagation, optimisation-method tests on toy problems, Excel/DDE/macro demos, **diagram-window GUI demos**, **animations** (engines, compressor, beer bubbles, projectile…) — features CoolSolve does not want to support |
| `duplicate` | 4 | intra-collection exact copies (`2-D Conduction (1)`, `Regen_minmax (1)`, `Indicated power (1)`) and one same-physics variant (`Difeqn2`) |
| `merged` | 1 | `compressorMap.lkt`, the lookup-table companion of `compressorMap.EES` |

Priorities of the 38 `todo` rows: 5 `high`, 13 `medium`, 20 `low` (the `low`
rows are mostly *duplicate-likely* of existing library models — the F-Chart
reference version of a cycle the library already has; they are kept `todo` for
the maintainer to decide *merge / duplicate / import*, see §4).

## 3. Diagram windows

Many examples have an **advanced Diagram window** (inputs with units, drop-down
substance selection, sliders, animated schematic, even the problem statement).
Per the maintainer's rule these are **still import candidates**, with a clear
note in the model README and `model.json` that *the Diagram window is not
imported and remains a gap in CoolSolve*. Detection here is textual (the file
mentions its Diagram window, `$IFNOT DiagramWindow`, animation objects); it was
confirmed file by file during the triage and must be re-checked at import time.
A `diagram-window: yes` note marks the affected `todo` rows. A dedicated gap
(`CS-GAP-DIAGRAM-WINDOW`, see roadmap B-22) will be proposed in the CoolSolve
register so the models can reference it.

## 4. Import candidates (maintainer review table)

38 rows `todo`, by priority then id. "Gap" lists the CoolSolve gaps that will
block the native file (from the register of 2026-11-08; **new** = to register).
"Dup?" = duplicate-likely of the library model(s) given — compare before
importing.

| id | file | model | category / kind / level | pri | diagram | gap | dup? |
|---|---|---|---|---|---|---|---|
| EEL-025 | `Blasius.EES` | Blasius flat-plate boundary layer (ODE, shooting) | heat_transfer/external_convection · dynamic · L2 | high | – | – | – |
| EEL-029 | `ChemEq.EES` | combustion equilibrium, law of mass action (octane, 120 % air) | fundamentals/combustion · steady · L2 | high | – | NASA species | – |
| EEL-069 | `LaGrange.EES` | same equilibrium, Lagrange multipliers | fundamentals/combustion · steady · L3 | high | – | NASA species | – |
| EEL-110 | `Supermkt.ees` | supermarket cooling system with bypass (CAEE 1993) | refrigeration_heat_pumps/refrigeration_systems · steady · L2 | high | yes | – | – |
| EEL-121 | `von Karman.EES` | von Karman viscous pump (3 coupled ODE, White 2005) | heat_transfer/external_convection · dynamic · L3 | high | – | – | – |
| EEL-009 | `2-D Conduction.EES` | 2-D steady conduction field, square plate | heat_transfer/conduction_radiation · steady · L2 | med | – | – | – |
| EEL-026 | `capvst.ees` | R134a heat pump with effectiveness HXs (α/β) | refrigeration_heat_pumps/heat_pump_cycles · steady · L2 | med | – | – (decimal comma, kPa/kJ) | – |
| EEL-030 | `ChemEq_converge.EES` | equilibrium, 11 species, staged convergence | fundamentals/combustion · steady · L3 | med | – | NASA species | – |
| EEL-058 | `gas spring.EES` | ball oscillating on a gas column (real gas) | fundamentals/piston_cylinders · dynamic · L2 | med | yes | – (animation out) | – |
| EEL-068 | `janaf.ees` | equilibrium with JANAF/NASA species data | fundamentals/combustion · steady · L2 | med | – | NASA species + ext. proc. | – |
| EEL-076 | `Maxpower.ees` | Carnot engine at maximum power (Curzon-Ahlborn) | fundamentals/second_law · optimization · L2 | med | yes | Min/Max | – |
| EEL-077 | `min_G.EES` | equilibrium by direct Gibbs minimisation | fundamentals/combustion · optimization · L3 | med | – | NASA species + Min/Max | – |
| EEL-092 | `psych.EES` | psychrometric calculator, any two properties | hvac/psychrometrics · function · L2 | med | yes | string `$IF` (substance/pair) | – |
| EEL-094 | `Rankine.ees` | regenerative Rankine, optimum extraction pressure | power_cycles/steam_advanced · optimization · L2 | med | yes | Min/Max; English units | – |
| EEL-104 | `Solid-Liquid_Props.EES` | EES solid-property library (k_, rho_, …) | fundamentals/properties · function · L1 | med | – | **new**: solid props | – |
| EEL-106 | `spring.EES` | spring-loaded piston + He, damped oscillation | fundamentals/piston_cylinders · dynamic · L2 | med | yes | – (animation out) | ~CSL-0210 |
| EEL-107 | `Steam_flow vectors.EES` | impulse-turbine velocity triangles, complex numbers | machines/turbomachine_design · steady · L3 | med | yes | **new**: `$Complex` | – |
| EEL-117 | `Transient Conduction…Plane Wall.EES` | 1-D transient conduction: series vs numerical | heat_transfer/conduction_radiation · dynamic · L2 | med | – | – | – |
| EEL-014 | `Absorp.ees` | NH3-H2O absorption cycle, external DLL | refrigeration_heat_pumps/absorption · steady · L3 | low | – | ext. procedure | CSL-0249 |
| EEL-015 | `adiabatic_combustion.EES` | octane flame temperature, guess-value lesson | fundamentals/combustion · steady · L1 | low | – | NASA species | CSL-0046 |
| EEL-024 | `Blackbody.EES` | blackbody band fraction (Planck integral) | heat_transfer/conduction_radiation · function · L1 | low | yes | – | ~CSL-0107 |
| EEL-034 | `compressorMap.EES` | compressor map, 2-D scattered interpolation (+ .lkt) | machines/compressor_maps · function · L2 | low | – | CS-GAP-INTERP2D | CSL-0035 |
| EEL-036 | `Convect.ees` | flat-plate convection exercise | heat_transfer/external_convection · steady · L1 | low | – | – | ht rows |
| EEL-049 | `Difeqn1.ees` | lumped-capacitance cooling (ODE) | fundamentals/tanks_vessels · dynamic · L1 | low | – | – | – |
| EEL-057 | `Flamet.ees` | CH4 flame temperature, JANAF | fundamentals/combustion · steady · L1 | low | – | NASA species | CSL-0150/46 |
| EEL-059 | `Gas Turbine System.EES` | simple gas turbine (English units) | power_cycles/gas_turbine_design · steady · L1 | low | yes | – (convert units) | CSL-0204 family |
| EEL-063 | `Heatex.ees` | counterflow HX, ε from LMTD | heat_exchangers/methods · steady · L1 | low | – | – | CSL-0002/0090 |
| EEL-080 | `moody.ees` | Churchill friction factor (function) | heat_transfer/pressure_drop · function · L1 | low | – | – | CSL-0018/0130 |
| EEL-083 | `nozzle.EES` | C-D nozzle, area-Mach, guess chaining | components/nozzles_ejectors · steady · L2 | low | – | – | CSL-0310 |
| EEL-091 | `Property_Calculator.EES` | multi-fluid any-two-property calculator | fundamentals/property_libraries · function · L2 | low | yes | string `$IF` | GUI calculator |
| EEL-095 | `Refrig.ees` | R134a vapour-compression cycle | refrigeration_heat_pumps/refrigeration_cycles · steady · L1 | low | – | – | CSL-0001 |
| EEL-096 | `Refrig_pro.EES` | same, diagram-driven | refrigeration_heat_pumps/refrigeration_cycles · steady · L1 | low | yes | – | CSL-0001 |
| EEL-097 | `Regen.ees` | regenerative Rankine, 2 FWH (English units) | power_cycles/steam_advanced · steady · L2 | low | – | – (convert units) | steam_advanced |
| EEL-099 | `Regen_minmax.EES` | same + FWH pressures optimised | power_cycles/steam_advanced · optimization · L2 | low | – | Min/Max | Regen.ees |
| EEL-101 | `runaround_HX.EES` | run-around loop, convergence lesson | heat_exchangers/methods · steady · L2 | low | yes | – | CSL-0162 |
| EEL-105 | `sonic_v.EES` | speed of sound by entropy perturbation (function) | fundamentals/property_libraries · function · L1 | low | – | `UnitSystem()` (check) | – |
| EEL-108 | `SteamCyc.ees` | reheat Rankine (Çengel 9.26) | power_cycles/steam_basic · steady · L1 | low | yes | – | steam_basic family |
| EEL-115 | `Throttle.EES` | R134a throttle with KE (`$IFNOT DiagramWindow`) | components/piping_valves · steady · L1 | low | yes | – | valve exercises |

Suggested reading of the table: the five `high` rows are models with **no
library counterpart**; the combustion block (EEL-015/029/030/057/068/069/077) is
a coherent **chemical-reactions set** (four methods for the same equilibrium
problem — mass action, Lagrange, direct Gibbs, NASA data — plus two flame-
temperature exercises) and anchors the domain expansion discussed in the roadmap
(B-23); the `low`/dup rows are mostly F-Chart reference versions of models the
library already has — candidates for `merged`/`duplicate` rather than new models.

## 5. What the discarded files demonstrate (for the record)

Feature coverage of the 79 `discarded` rows, should CoolSolve ever want test
material: string `$IF` directives, `$IMPORT`/`$EXPORT`, `$SAVETABLE`,
`$REFERENCE`, `$Warnings`, `$Constant`, `$DOLAST`, `$TabStops`, `$Trace`,
`$INCLUDE`, array range notation, modules/subprograms, complex mode, matrix
operations, `CONVERT`/unit checking, 3-D/polar/error-bar plotting, curve fitting
and linear regression, uncertainty propagation, genetic optimisation, macro
files and DDE/Excel links, diagram-window controls (sliders, check boxes, radio
groups, child windows, links, animated graphics) and eight animation models.
The two non-inventoried files (`EESDDE.xls`, `Excel_ws1.xlsx`) belong to the
Excel demos.
