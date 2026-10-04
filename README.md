# CoolSolve Library

An open, curated library of **thermodynamic and energy-system models written in
the EES language**, documented, verified and ready to run in
[CoolSolve](https://github.com/CoolProp/CoolSolve) — the open-source,
EES-compatible equation solver built on [CoolProp](https://github.com/CoolProp/CoolProp).

> **Status:** the library is being bootstrapped. The methodology, structure and
> tooling are in place and the first model is in; models are added one by one
> following the [roadmap](roadmap.md). See [CATALOG.md](CATALOG.md) for the
> current content.

## Why this library

Decades of teaching and research in thermodynamics produced hundreds of
equation-based models — exercises, component models, cycles, research case
studies — scattered over personal folders, course websites and software
libraries, often redundant, in several languages and for proprietary tools.
This library gathers them in one place and makes them:

- **organised** — a flexible taxonomy (by physical system) with facets for the
  model kind, complexity level and CoolSolve status;
- **harmonised** — EES language, SI units (°C, Pa, J), English comments, a
  standard header and a standard README for every model;
- **verified** — each import is compared with the results of the original tool
  (e.g. the solution stored in the EES file) and every runnable model has a
  regression baseline;
- **attributed** — every model states its source, authors, link and license;
- **built into CoolSolve** — each CoolSolve build embeds the library as it is
  at compile time and serves it in an HTML model explorer, and any model can
  import the functions and procedures of a library model with
  `$INCLUDE library:<name>` (planned, see
  [CoolSolve support](https://github.com/CoolProp/CoolSolve/blob/main/docs/model_library_support.md)).

The library covers the whole range from introductory exercises to
research-grade models, and steady-state, dynamic, optimisation and
function-library models — each clearly labelled.

## Organisation

```
CoolSolve_Library/
├── models/                 one folder per model, organised by category (see below)
├── sources/                inventories of the source collections (the backlog)
├── docs/
│   ├── taxonomy.md         categories, kinds, complexity levels, status, naming rules
│   └── model_workflow.md   how models are triaged, imported, verified and documented
├── templates/model/        README, model.json and .eescode header templates
├── tools/
│   ├── build_index.py      validates the library, regenerates the index files
│   └── test_models.py      solves the models with CoolSolve, compares with baselines
├── taxonomy.json           declared categories (machine-readable)
├── library.csv             the model table: one row per model     (generated)
├── library.json            same, for the CoolSolve browser          (generated)
├── functions.csv           every FUNCTION/PROCEDURE of the library  (generated)
├── CATALOG.md              browsable catalogue                      (generated)
├── redirects.csv           old paths of moved/renamed models        (generated)
└── roadmap.md              work programme and progress log
```

Categories (taxonomy v0.2, see [docs/taxonomy.md](docs/taxonomy.md)):

```
models/
├── fundamentals/     properties · processes · combustion
├── heat_transfer/    conduction · convection · radiation · pressure_drop
├── components/       heat_exchangers · compressors · expanders_turbines · pumps_fans ·
│                     valves_nozzles_piping · boilers_burners · storage · instrumentation
├── cycles/           steam_power · organic_rankine · gas_turbines · engines ·
│                     refrigeration_heat_pumps · absorption_sorption
├── hvac/             psychrometrics · air_handling · cooling_towers
├── renewables/       solar_thermal · photovoltaics · geothermal_biomass
├── buildings/
└── energy_systems/   cogeneration · district_heating · economics
```

The taxonomy can evolve: models are identified by a permanent ID (`CSL-0001`),
never by their path, and all index files are regenerated from the folders, so
categories can be split, renamed or re-organised without breaking references.

## Reading the badges

Every model README starts with three badges:

| Complexity level | Kind | Status in CoolSolve |
|---|---|---|
| 🟢 **Level 1 · Introductory** — first courses, textbook exercises | ⚙️ **Steady-state** — algebraic, one operating point | ✅ **Verified** — runs and matches an independent reference |
| 🔵 **Level 2 · Intermediate** — complete cycles, components with correlations | ⏱️ **Dynamic** — time integration (`INTEGRAL`) | ☑️ **Runs** — runs, no independent reference |
| 🟠 **Level 3 · Advanced** — semi-empirical, multi-zone, off-design | 🎯 **Optimisation** — needs Min/Max (not yet in CoolSolve) | ⚠️ **Runs (modified)** — runs after documented simplifications |
| 🔴 **Level 4 · Research** — calibrated, large research models | 🧩 **Function library** — reusable functions/procedures | ⛔ **Blocked** — needs a missing CoolSolve feature · ❌ **Failing** · 📄 **Documented only** |

Levels 1–2 form the educational part of the library, levels 3–4 the
engineering and research part. The rating rubric is in
[docs/taxonomy.md §3](docs/taxonomy.md#3-level--complexity-rating).

## A model folder

Each model folder is a self-contained CoolSolve project:

| File | Content |
|---|---|
| `README.md` | Description, problem statement, model equations, how to run, results (tables and a diagram or plot), verification, source and attribution, conversion log, limitations |
| `model.json` | Metadata: ID, title, kind, level, status, fluids, tags, origin (source, authors, link, license), verification, CoolSolve gaps |
| `<name>.eescode` | The model in EES language, starting with a commented introduction and with English comments on the equations |
| `<name>.initials`, `coolsolve.conf`, `<name>-<table>.csv` | Guess values, solver settings, lookup tables (when needed) |
| `<name>.sol` | CoolSolve solution, also used as regression baseline |
| `figures/` | Thermodynamic diagram or plot made with CoolSolve, shown in the README |

Open `<name>.eescode` in the CoolSolve GUI (companion files are picked up
automatically) or run `coolsolve ./<name>.eescode`.

## The model table

[`library.csv`](library.csv) summarises the library, one row per model:
ID, name, title, category, kind, level, status, summary, fluids, tags, size
(equations, largest block), origin (type, source, path, authors, license, URL),
CoolSolve gaps, related models, CoolSolve version and date of verification,
path. It is generated by `tools/build_index.py` from the `model.json` files —
never edit it by hand. [`functions.csv`](functions.csv) lists every function
and procedure defined in the library (used to find reusable building blocks).

## Sources

| Source | Content | Inventory |
|---|---|---|
| ULiège thermodynamics collection (S. Quoilin) | 552 EES files (incl. archived copies), **341 distinct models** after de-duplication: teaching (applied thermodynamics, thermal machines, internal-combustion engines, HVAC) and research/reference models (ORC, heat pumps, components, ULiège model bank, Laborelec toolkit), 2002–2023 | [sources/thermo_models](sources/thermo_models/) |
| CoolSolve examples | 47 models of the CoolSolve test suite (they stay in CoolSolve and are classified here) — MIT | [sources/coolsolve_examples](sources/coolsolve_examples/) |
| [LaboThapPy](https://github.com/PyLaboThap/LaboThapPy) | 74 candidates: Python components, correlations and cycles of the ULiège/UCLouvain/UMONS thermodynamics labs — Apache-2.0 | [sources/labothappy](sources/labothappy/) |
| [TESPy](https://github.com/oemof/tespy) | 52 candidates: component equations, tutorials and validated example plants (CGAM, SEGS, sCO2…) — MIT | [sources/tespy](sources/tespy/) |

Source files are not copied into the library: each model references its
source by path, URL or library name, and credits the authors of the original
model (README and `model.json`). Models translated from other libraries are
published under the library license with full credits to the original
authors.

## Contributing

Read the [model workflow](docs/model_workflow.md) and pick a task from the
[roadmap](roadmap.md). Importing an EES file relies on the CoolSolve tools
`tools/ees_extract.py` and `tools/compare_solution.py`, documented in
[CoolSolve docs/ees_import.md](https://github.com/CoolProp/CoolSolve/blob/main/docs/ees_import.md).
Before committing, run:

```bash
python3 tools/build_index.py
python3 tools/test_models.py --coolsolve ../CoolSolve/build/coolsolve
```

CoolSolve aims to read native EES code: when a model needs a feature CoolSolve
lacks, the model keeps its EES syntax and the gap is reported in the
[CoolSolve gap register](https://github.com/CoolProp/CoolSolve/blob/main/docs/model_library_support.md).

## License

[MIT](LICENSE). Models translated or adapted from third-party sources credit
the authors of the original models in their README and `model.json`.

**Maintainer:** [Sylvain Quoilin](https://www.uliege.be/cms/c_9054334/en/directory?uid=U203754) —
[ISES Research Group](https://www.ises.uliege.be/), Université de Liège.
