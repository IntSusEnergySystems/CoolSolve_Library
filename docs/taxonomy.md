# Taxonomy and classification

Every model is classified along **one folder axis** (its category) and **four
facets** stored in its `model.json`:

| Axis / facet | Values | Stored in | Shown as |
|---|---|---|---|
| **Category** | folder tree below `models/` (declared in [`taxonomy.json`](../taxonomy.json)) | folder location | breadcrumb in README, `category` column |
| **Kind** | `steady`, `dynamic`, `optimization`, `function` | `kind` | ⚙️ ⏱️ 🎯 🧩 badge |
| **Level** (complexity) | 1 to 4 | `level` | 🟢 🔵 🟠 🔴 badge |
| **Status** (CoolSolve) | `verified`, `runs`, `modified`, `blocked`, `failing`, `stub` | `status` | ✅ ☑️ ⚠️ ⛔ ❌ 📄 badge |
| **Origin type** | `teaching`, `research`, `textbook`, `software_library`, `industry`, `coolsolve` | `origin.type` | README table |

Free-form `tags` and `fluids` complete the description. The facets are
exported to `library.csv` / `library.json`, so the CoolSolve library browser
can filter on any combination (e.g. *all verified level-1 heat-exchanger
models*). The README of each model starts with the three badges:

> 🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0001`

Badges are plain emoji + text (no external images), so they render offline in
the CoolSolve GUI and survive folder moves.

---

## 1. Categories (taxonomy v0.2)

```
models/
├── fundamentals/        properties · processes · combustion
├── heat_transfer/       conduction · convection · radiation · pressure_drop
├── components/          heat_exchangers · compressors · expanders_turbines · pumps_fans ·
│                        valves_nozzles_piping · boilers_burners · storage · instrumentation
├── cycles/              steam_power · organic_rankine · gas_turbines · engines ·
│                        refrigeration_heat_pumps · absorption_sorption
├── hvac/                psychrometrics · air_handling · cooling_towers
├── renewables/          solar_thermal · photovoltaics · geothermal_biomass
├── buildings/
└── energy_systems/      cogeneration · district_heating · economics
```

Descriptions of every category are in [`taxonomy.json`](../taxonomy.json)
(the file validated by `tools/build_index.py`). Rules:

- At most **two levels** of categories below `models/`; a category folder
  contains model folders only (a top category without children, such as
  `buildings/`, contains model folders directly).
- Classify by the **main object** of the model: a heat-pump cycle with a
  detailed compressor sub-model goes to `cycles/refrigeration_heat_pumps`; the
  compressor alone goes to `components/compressors`.
- **Function libraries** go with the physics they serve (`cpbar` →
  `fundamentals/combustion`, two-phase heat-transfer correlations →
  `heat_transfer/convection`).
- When a model fits two categories, choose the one a user would browse first
  and add the other as a tag.
- Sub-categories are created only when they hold models; split a category when
  it exceeds ~40 models (taxonomy review, roadmap Phase 6).
- Cross-cutting aspects are **tags**, not categories: `control` (on/off
  boilers, thermostatic valves, cooling ceilings), `parameter identification`
  (models identifying parameters from catalogue or test data), `exergy`,
  `part load`, `design`, `exercise`, `reference model`.

### From the inventory categories to the folders

The source inventories (`sources/*/inventory.csv`) use a flat `category_guess`;
the worker chooses the folder when importing:

| `category_guess` | Folder(s) |
|---|---|
| fundamentals | `fundamentals/processes` (first/second law, exergy, cycles of ideal gases in exercises) |
| properties | `fundamentals/properties` |
| heat_transfer | `heat_transfer/conduction`, `…/convection`, `…/radiation`, `…/pressure_drop` |
| heat_exchangers | `components/heat_exchangers` |
| compressors | `components/compressors` |
| expanders_turbines | `components/expanders_turbines` |
| pumps_fans | `components/pumps_fans` |
| valves_nozzles_piping | `components/valves_nozzles_piping`; flow metering → `components/instrumentation`; friction/pressure-drop correlations → `heat_transfer/pressure_drop` |
| storage | `components/storage` |
| combustion_boilers | equipment → `components/boilers_burners`; combustion chemistry and `cpbar`-type functions → `fundamentals/combustion` |
| engines | `cycles/engines` |
| power_cycles_vapour | water/steam → `cycles/steam_power`; organic fluids, transcritical CO2 → `cycles/organic_rankine` |
| power_cycles_gas | `cycles/gas_turbines` (incl. combined cycles, turbojets) |
| refrigeration_heat_pumps | `cycles/refrigeration_heat_pumps` |
| absorption_sorption | `cycles/absorption_sorption` |
| hvac_psychrometrics | `hvac/psychrometrics`, `hvac/air_handling`, `hvac/cooling_towers` |
| solar_renewables | `renewables/solar_thermal`, `renewables/photovoltaics`, `renewables/geothermal_biomass` (borefields) |
| cogeneration_energy_systems | `energy_systems/cogeneration`, `…/district_heating`, `…/economics` |
| buildings | `buildings` |
| misc | case by case; propose a taxonomy change (`T-TAXO`) if several models share a new topic |

## 2. Kind — steady, dynamic, optimisation, function

The kind separates models by the **type of mathematical problem**, which is
also what decides whether CoolSolve can run them:

| Kind | Badge | Definition | CoolSolve support |
|---|---|---|---|
| `steady` | ⚙️ **Steady-state** | Algebraic system for one operating point (parametric studies included) | Full |
| `dynamic` | ⏱️ **Dynamic** | Integration over time (or crank angle, length…) with `INTEGRAL` / `$IntegralTable`, or explicit time stepping with arrays | `INTEGRAL` supported with the limitations of the Language Reference §12.7 |
| `optimization` | 🎯 **Optimisation** | The purpose of the model needs a Min/Max search (design optimisation, parameter identification by minimisation) | Not available (`CS-GAP-OPTIM`); the model is shipped at the optimum found by EES (decision variables fixed) and runs as a steady model |
| `function` | 🧩 **Function library** | A set of `FUNCTION`/`PROCEDURE` definitions (typically from an EES `.lib` file) followed by a short demonstration program calling them with typical values | Full; import into other models planned (`CS-FEAT-IMPORT`) |

Each model has exactly one kind (its purpose). **Parameter-identification**
models are `steady` when the parameters are solved from as many measured points
as unknown parameters (square system), and `optimization` when they minimise
an error over many points; both get the tag `parameter identification`.
Dynamic and optimisation models
are additionally tracked as separate work streams in the roadmap (Phase 4) and
can be listed with the `kind` column of `library.csv`.

*Why not top-level folders per kind?* Users look for models by physical
system first (*storage tank*, *ORC*); kind folders would duplicate the whole
domain tree for a minority of models. The kind is therefore a mandatory facet
with its own badge, filter and roadmap track, rather than a folder level.

## 3. Level — complexity rating

| Level | Badge | Label | Typical audience | Typical content |
|---|---|---|---|---|
| 1 | 🟢 | **Introductory** | First thermodynamics courses | One process, component or simple cycle; textbook exercise; explicit equations |
| 2 | 🔵 | **Intermediate** | Applied thermodynamics, engineering courses | Complete cycle or component with correlations; small implicit loops; a few procedures |
| 3 | 🟠 | **Advanced** | Design studies, MSc theses, engineering practice | Semi-empirical, multi-zone or discretised models; off-design; large implicit blocks; careful guesses needed |
| 4 | 🔴 | **Research** | PhD work, publications | Calibrated multi-component systems; > ~1500 equations or heavy array discretisation; demanding numerics |

Levels 1–2 form the **educational** part of the library, levels 3–4 the
**engineering/research** part. To make the rating reproducible, compute a
score from the CoolSolve analysis (`coolsolve -d` → `report.md`) and the
model content:

| Criterion | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Equations (after analysis) | < 50 | 50–300 | 300–1500 | > 1500 |
| Largest algebraic block | ≤ 5 | 6–30 | > 30 | |
| Structure: functions/procedures, arrays/`DUPLICATE` | none | present | | |
| Structure: multi-zone / discretised / ≥ 3 coupled components | no | yes | | |
| Physics: semi-empirical calibration, off-design, part-load or dynamics | no | yes | | |
| Numerics: needs curated guesses, simplified-model bootstrap, *Try Harder* or a tuned `coolsolve.conf` | no | yes | | |

**Score → level:** 0–1 → 1; 2–3 → 2; 4–6 → 3; ≥ 7 → 4. The level may be moved
by ±1 when the pedagogical intent clearly differs (e.g. a long but trivial
exercise), with a one-line justification in the README conversion log.

Examples: the NTU exercise `exchangers1` (20 equations, explicit) scores 0 →
level 1; `condenser_3zones` (99 equations, block of 62, procedures, three
zones, needs good guesses) scores 1+2+1+1+0+1 = 6 → level 3.

## 4. Status — what CoolSolve can do with the model

| Status | Badge | Meaning | Required content |
|---|---|---|---|
| `verified` | ✅ **Verified** | Runs in CoolSolve and agrees with an independent reference (EES stored solution, parametric table, publication, other tool) within the tolerances of CoolSolve `docs/ees_import.md` §11 | Comparison in README, `.sol` baseline |
| `runs` | ☑️ **Runs** | Runs; no independent reference available (sanity checks only: balances, physical ranges) | `.sol` baseline |
| `modified` | ⚠️ **Runs (modified)** | Runs only after simplifications or changes of the original physics (documented); results not comparable 1:1 with the original | Changes and their impact in the conversion log |
| `blocked` | ⛔ **Blocked** | Cannot run because of missing CoolSolve features (`missing_features` lists the `CS-GAP-…` IDs); kept in native EES syntax | Gap IDs, reproducer in the CoolSolve gap register |
| `failing` | ❌ **Failing** | Should be supported but does not converge / errors; diagnosis in progress | Diagnosis notes (debug output, what was tried) |
| `stub` | 📄 **Documented only** | Folder and documentation only (source referenced in `model.json`); conversion not attempted yet (e.g. parked optimisation models) | README, `model.json` |

Typical transitions: `stub → runs/verified`, `failing → verified` after
debugging, `blocked → verified` when a CoolSolve gap is closed (roadmap task
*re-check blocked models*).

## 5. Identifiers, names and files

- **ID** `CSL-NNNN`: assigned once (next free ID printed by
  `tools/build_index.py`), never changed, never reused (removed models go to
  `retired.csv`). Cross-references (README "Related models", `related`,
  `supersedes`, CoolSolve `$INCLUDE 'library:…'`) use IDs, never paths.
- **Name** (= folder name = `name` field): English `snake_case`, descriptive,
  unique in the whole library, ≤ 50 characters, without level/status/kind
  information (e.g. `orc_recuperator_r245fa`, `scroll_compressor_semi_empirical`).
- **Files** (the folder is a CoolSolve project):

```
<name>/
├── README.md               documentation (template: templates/model/README.md)
├── model.json              metadata (template: templates/model/model.json)
├── <name>.eescode          the model (header: templates/model/header.eescode)
├── <name>.initials         guess values (when needed)
├── <name>.sol              CoolSolve solution = regression baseline (when the model runs)
├── <name>-<table>.csv      lookup tables (CoolSolve companion convention)
├── coolsolve.conf          solver configuration (when needed)
├── <name>_<variant>.eescode  optional variants (simplified, other fluid…), listed in the README
└── figures/                diagram or plot made in CoolSolve by the maintainer, shown in the README
```

Source files (`.ees`, `.lib`, `.py`…) and extraction data are **not** stored in
the library: `model.json` references the source by its path (with `~` for the
home directory), its URL or its name in an existing library, and the reference
results used for the verification are summarised in the README.

## 6. Changing the taxonomy without breaking anything

Paths are never the identity of a model: the ID is. Generated files
(`library.csv`, `library.json`, `functions.csv`, `CATALOG.md`,
`redirects.csv`) are rebuilt from the folders by `tools/build_index.py`.

- **Move a model** to another category: `git mv` the folder, add the old path
  to `previous_paths` in `model.json`, run `tools/build_index.py`.
- **Rename a model**: `git mv` the folder, rename the main file and its
  companions (`.initials`, `.sol`, `-<table>.csv`), update `name` and
  `main_file`, add the old path to `previous_paths`, rebuild.
- **Add, split or rename a category**: edit `taxonomy.json` (increase its
  `version`), move the folders as above, rebuild; record the change in the
  roadmap progress log.
- **Remove a model** (merged into another one, or withdrawn): delete the
  folder, add a line to `retired.csv` (`id,date,reason,replaced_by`).

Because CoolSolve resolves library models through `library.json` and
`redirects.csv`, and models reference each other by ID, none of these
operations breaks a link.
