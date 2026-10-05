# Centrifugal compressor design and similarity (air)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0069`

A centrifugal turbocompressor is designed for its best-performance point: the
flow factor φ and the enthalpy factor ψ of that point are given, and the model
returns the impeller diameter, the rotation speed, the blade tip speed and the
inlet area that realise them. The second file of the model
(`..._methane.eescode`) applies the same two similarity factors to a
compressor of the same type compressing methane, as the exercise asks.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air (main file), Methane (variant) |
| **Size** | 15 equations (largest block: 1), per file |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 4 (2004-10-12), exercise 4 (EES file `MSTH_041012_exercice_6.EES`, continuation `..._exercice_6_suite.EES`) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory, course *Machines et systèmes thermiques*, repetition of 2004-10-12, exercise 4; individual author not identified) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — main file and variant verified against the EES stored solutions (see *Verification*) |

## Problem statement

A centrifugal turbocompressor has been designed to reach its best performance
under the following nominal conditions:

- working fluid: dry clean air;
- suction pressure and temperature: 1 bar and 20 °C;
- discharge pressure: 2.5 bar;
- flow rate: 6000 m³/h;
- flow factor: φ = 0.3;
- enthalpy factor: ψ = 1.4.

Determine:

- the optimal impeller diameter and rotation speed;
- the diameter and the rotation speed of a compressor of the same type
  compressing 12000 m³/h of methane from 2 bar, 20 °C to 3 bar.

## Model

The two factors of the best-performance point close the two similarity
relations that fix the size and the speed of the machine; the isentropic
enthalpy rise that appears in ψ comes from the fluid alone, so it is known
before the geometry is:

- flow factor: $\phi = \dot V_{su}/(U\,A)$ — the volume flow divided by the
  product of the blade tip speed and the inlet area (dimensionless);
- enthalpy factor: $\psi = \Delta h_s/(U^2/2)$ — the isentropic enthalpy rise
  divided by half the square of the blade tip speed (dimensionless);
- blade tip speed and inlet area: $U = \pi D N$, $A = \pi D^2/4$ with
  $N$ in rev/s and `rpm = 60·N`;
- isentropic enthalpy rise: $\Delta h_s = h_{ex,s} - h_{su}$ with
  $h_{su} = h(\text{Air},T_{su})$, $s_{su} = s(\text{Air},T_{su},P_{su})$ and
  $h_{ex,s} = h(\text{Air},s_{su},P_{ex})$.

Each factor appears twice — once as an input of the nominal point, once as the
relation that closes the geometry — so the system is square and CoolSolve
splits the 15 equations into 15 blocks of one equation.

| Inputs | Value | Outputs (air) | Value |
|---|---|---|---|
| `p_su` / `t_su` | 1 bar / 20 °C | `D` impeller diameter | 0.1412 m |
| `p_ex` discharge pressure | 2.5 bar | `N` rotation speed | 799.9 rev/s |
| `V_dot_su` flow rate | 6000 m³/h | `rpm` rotation speed | 47 996 rev/min |
| `phi` flow factor | 0.3 | `U` blade tip speed | 354.8 m/s |
| `psi` enthalpy factor | 1.4 | `A` inlet area | 0.01566 m² |

## How to run

Open `centrifugal_compressor_design_similarity.eescode` in the CoolSolve GUI
and press *Solve*, or from a terminal:

```bash
coolsolve ./centrifugal_compressor_design_similarity.eescode
```

**The `.initials` file is required.** With the default guesses (1 for every
unknown) the Newton solver of the default pipeline diverges in the block that
computes the inlet area and stops with *SingularJacobian*; with the stored EES
solution as initial values the model converges in 4 iterations (see
*Limitations and CoolSolve gaps*). Adding `TrustRegion` to the solver pipeline
(`coolsolve.conf` with `solverPipeline = Newton, TrustRegion`) also converges
without any initial value.

The methane variant is run the same way and has its own `.initials`:

```bash
coolsolve ./centrifugal_compressor_design_similarity_methane.eescode
```

## Results

Main file (air, 1 → 2.5 bar, 6000 m³/h):

| Quantity | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `D` [m] | 0.141204 | 0.141193 | 7.6e-05 |
| `N` [rev/s] | 799.745 | 799.927 | 2.3e-04 |
| `rpm` [rev/min] | 47 984.7 | 47 995.6 | 2.3e-04 |
| `U` [m/s] | 354.770 | 354.824 | 1.5e-04 |
| `A` [m²] | 0.0156596 | 0.0156572 | 1.5e-04 |
| `DELTAh_s` [J/kg] | 88 103.2 | 88 130.0 | 3.0e-04 |
| `h_su`, `h_exs` [J/kg], `s_su` [J/kg·K] | — | — | constant reference-state offset (see *Verification*) |

Variant (methane, 2 → 3 bar, 12 000 m³/h):

| Quantity | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `D` [m] | 0.216003 | 0.216001 | 6.5e-06 |
| `N` [rev/s] | 446.828 | 446.836 | 1.9e-05 |
| `rpm` [rev/min] | 26 809.7 | 26 810.2 | 1.9e-05 |
| `U` [m/s] | 303.214 | 303.218 | 1.3e-05 |
| `A` [m²] | 0.0366445 | 0.0366440 | 1.3e-05 |
| `DELTAh_s` [J/kg] | 64 357.1 | 64 358.8 | 2.6e-05 |
| `h_su`, `h_exs` [J/kg], `s_su` [J/kg·K] | — | — | constant reference-state offset (see *Verification*) |

The methane compressor of the same type is larger (0.216 m against 0.141 m) and
slower (26 810 against 47 996 rev/min). With the two factors unchanged,
`U = √(2 Δh_s/ψ)` fixes a lower tip speed — methane is compressed from 2 to
3 bar instead of air from 1 to 2.5 bar, so its isentropic enthalpy rise is
smaller (64.4 against 88.1 kJ/kg) — and `A = V̇_su/(φ·U)` then grows with the
volume flow (2.0 times larger). The original notes of its own ideal-gas
approximation that "it changes very little": its stored ideal-gas run gives
D = 0.2158 m and 26 872 rev/min against 0.2160 m and 26 810 rev/min with the
real-gas properties kept here.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     e.g. D and rpm as functions of the flow factor phi at fixed psi, saved in figures/.
     Air is an ideal-gas substance here, which has no CoolSolve diagram
     (CS-FEAT-DIAGRAM-IDEAL), so the figure is a sweep plot. -->

## Verification

1. **Main file vs EES.** The original equations were solved unchanged and
   compared with the solution stored by EES 7.210 in
   `MSTH_041012_exercice_6.EES` (`tools/compare_solution.py`, `rtol=0.001`):
   *"15 common variables, 3 differ (rtol=0.001)"*. The 12 comparable
   variables agree, the largest relative deviation being **3.04e-04**
   (`DELTAh_s`, 88 130 vs 88 103 J/kg: EES 7 and CoolProp `Air` properties),
   inside the 0.1–0.5 % expected for a different equation of state (CoolSolve
   `docs/ees_import.md` §11). The three remaining variables are the absolute
   enthalpies and the absolute entropy, shifted by a constant reference-state
   offset (EES 7 `Air` versus CoolProp `Air`, as already documented for
   `CSL-0023` and `CSL-0035`):

   | Quantity | EES | CoolSolve | offset |
   |---|---:|---:|---:|
   | `h_su` | 293 534.34 J/kg | 419 404.92 J/kg | +125.87 kJ/kg |
   | `h_exs` | 381 637.54 J/kg | 507 534.89 J/kg | +125.90 kJ/kg |
   | `s_su` | 5 682.13 J/kg·K | 3 867.26 J/kg·K | −1 814.87 J/kg·K |

   The energy difference is what the model uses and it agrees
   (`DELTAh_s`, 3.0e-04); the geometry follows from it (`U = √(2 Δh_s/ψ)`),
   which is why `D`, `A`, `N` and `rpm` agree to 2.3e-04.
2. **Methane variant vs EES.** Same procedure with the solution stored in
   `MSTH_041012_exercice_6_suite.EES`: *"15 common variables, 3 differ
   (rtol=0.001)"*, the 12 comparable variables agreeing with a largest
   relative deviation of **2.58e-05** (`DELTAh_s`). `h_su`, `h_exs` and `s_su`
   carry the real-methane reference-state offset (+910.94 kJ/kg on `h`,
   +6 676.88 J/kg·K on `s`); the difference `DELTAh_s` again agrees.
3. **Arithmetic of the results** recomputed from the model equations:
   `U = π·D·N = 354.824 m/s`, `φ = V̇_su/(U·A) = 0.3000`,
   `ψ = Δh_s/(U²/2) = 1.4000` (main file), and the same two factors for the
   variant (303.218 m/s, 0.3000, 1.4000).

## Source and attribution

Exercise of the ULiège course *Machines et systèmes thermiques* (repetition 4
of 2004-10-12, exercise 4). The EES licence tag names the ULiège
Thermodynamics Laboratory (its exercise-2 files carry the J. Lebrun lab
licence), which identifies the laboratory but not the individual author;
none is named in the files.

Source files (EES 7.210, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/MSTH_041012_exercice_6.EES`
(inventory candidate `TM-0057`) and, for the methane variant,
`.../MSTH_041012_exercice_6_suite.EES` (`TM-0058`). No EES original of this
example exists in CoolSolve `misc/EES_ok.zip`. The CoolSolve example
(`examples/simple_centrifugal_compressor.eescode`, `CSX-043`) is kept in the
CoolSolve repository as a test case.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): the
  unit system was already `SI MASS DEG PA C J`, no conversion needed; the EES
  licence tag was removed; no lookup or parametric table, no external
  function, no warning in the extraction report. Comments translated to
  English (flow factor / enthalpy factor, as in the original French *facteur
  de débit* / *facteur d'enthalpie*), the standard header added, SI units
  added to the trailing comments, and the embedded EES *"Solution:"*
  printout removed (the stored values are in the *Results* and *Verification*
  tables). **No equation was changed.**
- **2026-10-05 — `.initials`**: the stored EES solution, with the absolute
  enthalpies and the entropy put on the CoolProp `Air` reference state (same
  convention as `CSL-0023`, so that the guesses stay consistent with the
  values the model itself computes). Every other guess is the EES stored
  value. The raw EES guesses also converge here (10 iterations, verified),
  because every enthalpy call of the model is explicit; the same treatment is
  applied to the variant's `.initials`.
- **2026-10-05 — methane variant.** The exercise is split by the original into
  two files (*exercice 6* and *exercice 6_suite*); the second one is shipped
  as `centrifugal_compressor_design_similarity_methane.eescode`, with its own
  `.initials` and `.sol` (regression-tested as `CSL-0069:methane`). It is the
  same equation set with the methane nominal point; the real fluid
  (`methane` in EES, an EES *real* substance) is the approximation the original
  leaves active, and its ideal-gas lines (`CH4`, an EES *ideal-gas* substance)
  stay commented out, as in the original. No equation of the original was
  changed and no CoolSolve-only syntax is used.
- **2026-10-05 — differences vs the CoolSolve example** (`CSX-043`, kept in
  CoolSolve): the 15 equations are **identical** to the EES original
  (checked line by line after stripping comments and blanks); only the header
  comment differs (the example adds a `SOLVER NOTE`, see below). The library
  model follows the EES original, and drops the *Solution* printout of the
  example. The example's `SOLVER NOTE` states that "the default solver
  configuration includes TrustRegion and will converge": the shipped
  `examples/coolsolve.conf` does not change the solver pipeline (its default
  is `Newton`), so a CLI run and the example test report fail (see *Limitations
  and CoolSolve gaps*).
- **Level 2** (taxonomy.md §3): 15 equations (0) + largest block 1 (0) + no
  function, procedure or array (0) + single component (0) + similarity
  factors imposed on a nominal point, semi-empirical design closure (1) +
  curated guesses required (1) = 2 → Intermediate.

## Limitations and CoolSolve gaps

- No registered CoolSolve gap blocks this model (`missing_features` is empty);
  no runnable `_coolsolve` variant is needed and none is shipped.
- Very coarse model (as the original itself states): the machine is sized
  from two similarity factors, nothing else is imposed, and no off-design
  behaviour, geometry or slip is represented. Air and methane are treated as
  compressible ideal gases (`Air`) or as real gases (`methane`); the original
  shows that the choice changes the result by ~0.2 %.
- The `enthalpy(): fluid 'Air'` hint (suggesting `AirH2O` for moist air) is
  spurious here: dry-air ideal-gas properties are intended.
- **Solver diagnosis of the failure of the CoolSolve example** (reproduced on
  the unmodified example, debug folder): the system is square (15 equations,
  15 unknowns, 15 blocks of 1). With the default guesses, the Newton1D block
  that solves `phi = V_dot_su/(U*A)` for `A` starts at `A` = 1, its first step
  (`ΔA` = 62.9, from `A = 1`) throws `A` far on the negative side, and the
  sequence diverges towards −∞; `∂F/∂A = V̇_su/(U·A²)` then underflows to zero
  and the block reports *SingularJacobian* (a diverged 1-D block, not a
  genuinely singular one). The same file converges from the same guesses when
  `TrustRegion` is added to the solver pipeline, and converges with the stored
  EES values as initial guesses with Newton alone (4 iterations, the state
  shipped here). The root cause is a too distant default guess, so the
  `.initials` file is the fix; the step taken in the failing block is worth a
  look, but no register row was added for it here: the CoolSolve behaviour is
  reproduced, yet nothing shows that EES converges from the same guesses, so it
  is listed as an unverified suggestion in
  `~/Nextcloud/llm/csl-coolsolve-pending.md` rather than in the register.

## Related models

- `CSL-0023` *centrifugal_turbocompressor_performance*: same component, same
  course and repetition, but off-design performance at constant isentropic
  efficiencies (flow rate, power) instead of a design by similarity factors.
- `CSL-0035` *centrifugal_compressor_lookup_map*: same component and same
  repetition, characterised by a measured performance map.
- `thermo_models` `TM-0059` / `TM-0060` (`MSTH_041012_exercice_7*.EES`):
  optimal-regime laws applied to another compressor of the same session.
- CoolSolve example `simple_centrifugal_compressor.eescode` (`CSX-043`):
  same exercise, kept in CoolSolve as a test case.