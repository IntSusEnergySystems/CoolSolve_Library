# domain_expansion — sources and domains beyond the current scope (B-23, open)

Working notes of the exploration opened by the maintainer on 2026-11-11:
*anything that requires a solver is a good idea — even better if it involves
substance properties — material strength and chemical reactions are examples*.
This is a **brainstorm + lead inventory**, not a triage: every accepted lead
becomes a `sources/<name>/inventory.csv` (29-column convention) and import
cards in a new roadmap batch. Nothing here is imported yet.

Clones used for this instalment (temporary, `/tmp/opencode`): `ees-examples`
(EES-Community, MIT), `cantera` (sparse, `samples/python`, BSD), `python-mechanics`
(MIT). All checked 2026-11-11.

## 1. Fit criteria (how a domain is judged)

1. **Equation-based**: the model is an implicit algebraic system (CoolSolve's
   core) or an ODE (`INTEGRAL`, dynamic kind). DAE-heavy / FEM / CFD sources do
   not fit.
2. **Solver value**: the model is *hard without a solver* (coupled, implicit,
   iterative) — not a closed-form formula.
3. **Substance properties**: uses thermophysical properties (ideal bonus; this
   is where CoolSolve + CoolProp shine).
4. **Language proximity**: EES files are native imports; Modelica/Python need
   translation (established, slower); spreadsheets/JS sims are usually poor fits.
5. **Licence**: MIT/BSD/Apache-2.0 direct; GPL only as *method reference*
   (equations as facts, no wholesale copying); textbook statements are always
   paraphrased + credited (existing library rules).

## 2. Domain map

### A. The EES ecosystem beyond thermodynamics — *the immediate lead*

The single largest finding of this exploration is that **F-Chart's official MIT
mirror ([EES-Community/ees-examples](https://github.com/EES-Community/ees-examples),
clone `5c703d0` of 2026-03-01) contains 366 files that are not in the local
`EES_library` folder** (331 distinct by normalised name — ≈35 are intra-repo
trailing-underscore duplicate variants), **plus `ees-examples-raw.zip` (33.6 MB):
280 `.eez` binary originals with the stored solutions, companion tables and
book/chapter provenance paths** — the verification reference for the repo-only
models (see [sources/ees_library/README.md](../ees_library/README.md) §1):

| block | content | count | notes |
|---|---|---:|---|
| `Case_Study/example_*` | Nellis & Klein, *Heat Transfer* (Cambridge 2009) / *Introduction to Heat Transfer* textbook examples: conduction, fins, transient, external/internal/free convection, boiling, heat exchangers, mass transfer + cooling coils, radiation (view factors, shields, enclosures), cryogenics (LOX dewar, superconductor quench) | ~240 | plain-text `.ees`, book headers in each file, `$UnitSystem SI MASS RAD PA K J`; statements © Cambridge (paraphrase); fills the library's thin `heat_transfer` categories with a coherent, graduated set |
| `Case_Study/ex*` | Herold, Radermacher & Klein, *Absorption Chillers and Heat Pumps* 2nd ed (CRC 2015): H2O/LiBr and NH3/H2O cycles, double-effect, two-stage with precooling | ~30 | `refrigeration_heat_pumps/absorption` has only 2 models today; CoolSolve has `nh3h2o` built in and `CS-GAP-LIBR-PK` pending |
| `Case_Study/*` (misc) | `ansi540` (AHRI 540-2004 compressor polynomials — pairs with CSL-0136 EN12900), `gas_turbine_engine_2`, `recompression_cycle` (sCO2!), `refrigerator_captube/evapcond`, `compact_hx`, `crossflow_hx`, `air_preheater`, `enthalpy_exchanger`, `humidifier_simulation`, `oil_cooler_simulation`, `pump_curve`, `freezing`, `lumped_system`, … | ~25 | several have no library counterpart |
| `uncategorized/` (real models) | `brayton_cycle`, exam models (radiation, fins), plot/cycle extras | ~20 | triage needed |
| `Properties/` | `iceproperties` (!), `psych_calculator` | 2 | ice properties tie into the CoolSolve solid-phase design study |
| `Statics/` | 2 equilibrium problems from Gray, Costanzo, Witt & Plesha, *Statics and Dynamics* (McGraw-Hill 2023) using `$Vector2D` / `VectorAssignPolar` | 2 | **mechanics domain in EES**; blocked by an unregistered vector gap — needs a CoolSolve decision before this domain can grow |
| feature/plot demo folders | more variants of the discarded EES_library rows (`Plots`, `Diagram_Window`, `Directives`, `Macros`, `Units`, `Advanced`, `Curve_Fit`, `Lookup_Tables`, `Integral`, `Formatted_Equations_Window`) | ~34 | triage as discard |

Also on fchartsoftware.com (add-on property libraries, model-relevant rather
than importable): `chem_equil` (the CHEM_EQUIL external procedure, C-H-O-N-Ar
equilibrium), LiBrH2O (Yuan & Herred 2005), **seawater properties** (Lienhard,
MIT — matches the solid/TEOS-10 design study), **RocketProps** (rocket
propellant properties), VoltTC (thermocouple ITS-90), SETP5 solar library
(Duffie & Beckman 5th ed — solar!), ACHP problem-file zips (same as the book
block above), plus the "books using EES" list (Klein & Nellis thermodynamics
textbook; Mitchell & Braun HVAC; Barron & Nellis cryogenics). These are
CoolSolve *feature* leads (property back-ends) more than library models.

**First step (proposed card C-519):** sweep `ees-examples` into
`sources/ees_examples/` (same pattern as `ees_library`), triage the 366 new
files (331 distinct). Biggest single addition available to the library, and it
is MIT. Verification material: `ees-examples-raw.zip` (280 `.eez` stored
solutions + provenance).

### B. Chemical reactions, combustion and process engineering — *strong fit; species data are in CoolSolve 0.5*

| collection | licence | content | verdict |
|---|---|---|---|
| [Cantera](https://github.com/Cantera/cantera) `samples/python` (70 scripts: kinetics, reactors, onedim flames, thermo, transport) | BSD | shock tubes, PSR/CSTR/PFR networks, ignition delay, adiabatic flames, SOFC, Li-ion battery deg., diamond CVD | species thermochemistry is in CoolSolve 0.5 (`OH`, `NO`, `CHEM_EQUIL`, heating values). What remains is the translation: ODE balances and Arrhenius rates, not a missing species table. Pick 5-8 showcase models (ignition delay, PSR, PFR, equilibrium, SOFC) |
| EES `ChemEq` four-method set (B-22) | MIT | mass action / Lagrange / Gibbs-min / JANAF on octane-air | in-batch already; species properties are available (`CS-GAP-FLUIDS-NASA-SPECIES` closed in 0.5) |
| [pycse](https://github.com/jkitchin/pycse) (J. Kitchin, CMU; ~300 solved ChE problems: material & energy balances, reactors, VLE, units, fitting) | **GPL-3.0** | excellent problem bank, exactly the right level | GPL blocks copying; use as *ideas* only (equations of physical laws are not copyrightable, but do not mirror structure/wording); better: ask Kitchin (or verify) whether examples may be relicensed |
| [LearnChemE](https://github.com/LearnChemE) (CU Boulder) | site CC-BY-NC-SA-ish | interactive JS sims, Mathematica | poor fit (not equation models); skip |
| APMonitor examples (apmonitor.com wiki, J. Hedengren) | to verify | CSTR/distillation/HX/kinetics in APMonitor syntax | syntax is EES-like (equation-based); check licence + whether models are original or from textbooks (Fogler etc.) before any use |
| NASA CEA (Fortran) / RocketCEA (Python wrapper) | US government work / wrapper licence to verify | rocket combustion equilibrium + nozzle performance | see domain D; CEA is the reference *oracle* for chemical-equilibrium models |

Chemical-reaction models the library could still add (species data are in
CoolSolve 0.5): equilibrium composition by the other three methods (B-22),
ignition delay (H2/O2, n-heptane), PSR/CSTR extinction curves, PFR with heat
loss, SOFC Nernst + voltage (Cantera `sofc.py`), Li-ion battery
(single-particle ODE). Adiabatic flames with dissociation are already in
(`CSL-0150`, `CSL-0264`).

### C. Material strength / mechanics of materials — *fit is real but sources are thin; mostly authored models*

Few equation-solver collections exist; solids are taught with closed forms and
FEM. What was found:

| lead | licence | content | verdict |
|---|---|---|---|
| `ees-examples/Statics` (2 files) | MIT (files) | cable-bar equilibrium via `$Vector2D` | seed of an EES mechanics set; needs vector support (new gap) or manual component equations |
| [python-mechanics](https://github.com/TomLXXVI/python-mechanics) (T. Christiaens) | MIT | beam/shaft stress & deflection library, examples from Hibbeler 10th ed SI | use as **verification oracle for authored models**; Hibbeler statements © Pearson (paraphrase or renumber) |
| MIT OCW 3.11 (Roylance) | CC BY-NC-SA | 1990s `.exe` modules, no EES | reference only, skip |
| MIT OCW 2.60J tools (O. Labban) | "used with permission" + CC BY-NC-SA | EES intro PDFs (no .ees published) | skip |

Authored-model candidates (equation systems where a solver genuinely helps,
several involve substance properties — solid props gap `k_/rho_/c_/E_/nu_`
interacts here): statically indeterminate beam/bar assemblies; thick-walled
pressure vessel + thermal stress; combined-loading Mohr circle at a point;
Euler/inelastic buckling of columns with imperfections; bolted/flanged joint
preload + thermal; composite laminate CLT (matrix system, E + alpha vs T);
fatigue (Goodman) sizing; spring-mass-damper + gas spring (already coming via
EEL-058/106). Recommend: **author 5-8 showcase models** (new category
`solids_mechanics/` in taxonomy v0.4), verify vs python-mechanics / textbook
numbers; decide the solid-property-function gap together with the CoolSolve
solid-phase design study.

### D. Propulsion and compressible flow — *excellent solver+properties fit*

Rocket/airbreathing cycle analysis is implicit (equilibrium combustion, choked
nozzles, matches) and property-driven (combustion gases). Leads: NASA CEA
(oracle), RocketCEA (Python wrapper), K. Niemeyer's rocket-propulsion course
notes (CEA via Cantera, open notes), library nozzles CSL-0310/0325 as starting
points. Authored set: ideal rocket cycle (chamber equilibrium T, c*, Cf, Isp vs
expansion ratio), nozzle with real-gas properties, isentropic ramjet/scramjet
segment, tank blowdown (already adjacent to gas spring). Gated on NASA species
for equilibrium; real-fluid nozzle parts run today.

### E. Other domains screened (short verdicts)

- **Hydraulics/pipe networks** (Hardy-Cross as an implicit system, pump-system
  operating points): small authored set possible; overlaps `pressure_drop`.
- **Psychrometric/HVAC systems**: already a library strength; ees-examples adds
  Mitchell&Braun-style content.
- **Electrical circuits** (MNA DC/AC steady state): pure solver, no substance
  properties; possible later showcase, low priority.
- **ASCEND** (equation-based modelling environment, GPL): its model library
  (flash, chem eng) is a *method* reference only (GPL).
- **Modelica libraries** (Buildings, PowerSystems): DAE-oriented, dynamic;
  translation effort high — same verdict as ThermoCycle (only few steady models
  kept).
- **FEHT** (F-Chart's FEM heat-transfer sibling): FEM, out of CoolSolve scope.

## 3. Candidate collections (summary table for the maintainer)

| # | collection | domain | licence | size | fit | proposed first step |
|---|---|---|---|---|---|---|
| 1 | EES-Community/ees-examples (repo-only files) | heat transfer, absorption, mechanics, properties | **MIT** | 366 files | native EES | **C-519 sweep + triage (recommended first)** |
| 2 | F-Chart add-on property libraries (chem_equil, seawater, RocketProps, SETP5, VoltTC) | properties | varies, free downloads | ~5 libs | CoolSolve *feature* leads | hand to CoolSolve gap/feature discussion |
| 3 | Cantera `samples/python` | reactions, reactors, flames | BSD | 70 scripts | translation, gap-gated | park until NASA-species gap closes; then pick 5-8 |
| 4 | NASA CEA / RocketCEA | propulsion equilibrium | public domain (US gov)/wrapper | wrapper | oracle + authored models | authored rocket-cycle set (domain D) |
| 5 | python-mechanics | solids (oracle) | MIT | lib + Hibbeler examples | oracle only | authored solids_mechanics set (domain C) |
| 6 | pycse | ChE problem bank | GPL-3.0 | ~300 | ideas only | optionally ask author about relicense |
| 7 | APMonitor wiki examples | ChE processes | verify | ~100s | syntax-near | verify licence & provenance before anything |
| 8 | MIT OCW 2.60J / 3.11 | thermo/MoM | NC-SA | PDFs/exe | poor | skip |
| 9 | LearnChemE | ChE | NC | JS sims | poor | skip |
| 10 | ASCEND models | ChE/thermo | GPL | lib | reference only | skip |

## 4. Recommended actions (for the maintainer)

1. **Approve C-519** (ees-examples sweep): the largest, best-licensed,
   nearest-language addition available; fills `heat_transfer` and `absorption`
   with textbook-grade graduated sets (with the standard paraphrase rule).
2. **CoolSolve 0.5** closed `CS-GAP-FLUIDS-NASA-SPECIES`, `CS-GAP-NASA`,
   `CS-GAP-CHEM-EQUIL` and `CS-GAP-HEATING-VALUE`. Still open for these
   domains: diagram window (import policy), `$Vector2D` (mechanics),
   solid-property functions (materials, `docs/solid_phase_properties.md`).
3. **Decide the authored-models policy**: domains C and D are mostly *authored*
   models with open-source oracles (python-mechanics, CEA/RocketCEA) rather
   than translations — a new model *kind* of work for the library (the workflow
   covers translations only today).
4. Domain pick for the next batch after B-22: chemistry (in-batch already) →
   heat-transfer textbook set (C-519) → propulsion (authored) → solids (authored).
