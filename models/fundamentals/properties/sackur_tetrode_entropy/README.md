# Sackur-Tetrode absolute entropy of helium

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0365`

Absolute molar entropy of a monatomic ideal gas (helium at 1 atm and 300 K)
computed from the Sackur-Tetrode equation of statistical mechanics and checked
against the absolute entropy of the EES/NASA ideal-gas database: the two values
agree within 1e-6 relative. Textbook example 15.5-1 of Klein & Nellis,
*Thermodynamics* (2011) — a verification curiosity with no system model.

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | He (ideal gas) |
| **Size** | 8 equations, all explicit (largest block: 1) |
| **Source** | Klein & Nellis, *Thermodynamics*, Cambridge University Press, 2011, example 15.5-1 ([EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/example_15.5-1.ees)) |
| **Authors** | S. A. Klein and G. F. Nellis (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0 — verified analytically and against the published helium entropy (the EES stored solution is stale; see *Verification*) |

## Problem statement

Calculate the absolute entropy of helium at 300 K and 1 atm from the
Sackur-Tetrode equation of statistical mechanics,

> s̄ = R·[ ln( k·T·(2π·m·k·T/h²)^(3/2) / P ) + 5/2 ],

with m = MW/N_A the mass of one particle, and check the value against the
absolute entropy of the EES/NASA ideal-gas database.

## Model

All equations are explicit, kept as in the original:

- inputs: `G$ = 'He'`, `T = 26.85 °C` (300 K in the original), `P = 101325 Pa`
  (1 atm in the original);
- `MW = MolarMass(G$)`, `m = MW/(NA#*1000)` (mass of one particle);
- `T_K = T + 273.15` (the Sackur-Tetrode equation needs absolute temperature);
- `s_bar = R#*(ln(k#*T_K*(2*pi*m*k#*T_K/(h#^2))^(3/2)/P)+5/2)`;
- `s_bar_EES = MolarMass(G$)*Entropy(G$,T=T,P=P)`.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| G$ | 'He' | MW | 4.002602 kg/kmol |
| T | 26.85 °C (300 K in the original) | m | 6.64648e-27 kg |
| P | 101325 Pa (1 atm in the original) | **s_bar** (Sackur-Tetrode) | **126171.99 J/kmol-K** |
| | | **s_bar_EES** (EES/NASA database) | **126172.11 J/kmol-K** |

## How to run

```bash
coolsolve ./sackur_tetrode_entropy.eescode
```

No `.initials` needed: all 8 equations are explicit assignments (0
iterations, system square). No `coolsolve.conf`, no variants.

## Results

`s_bar = 126171.99 J/kmol-K (126.172 J/mol-K)` and
`s_bar_EES = 126172.11 J/kmol-K (126.172 J/mol-K)`: the Sackur-Tetrode value
and the EES/NASA database agree within 0.12 J/kmol-K, i.e. 9.6e-7 relative —
the statistical-mechanics result reproduces the tabulated absolute entropy of
helium.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
     figures/sackur_tetrode_entropy_sweep.png + one-line caption -->

## Verification

**Reference used: analytical recomputation and the published JANAF/NIST
entropy of helium.** The solution stored in the source file is **stale** for
the equations as saved: the extractor warns "Stored solution may be STALE"
(the stored `T` record is 1000 K while the saved equation fixes
`T = 300 [K]`). The stored `s_bar`/`s_bar_EES` records (151195.2668 /
151299.1457 J/kmol-K) correspond to that T = 1000 K run, not to the 300 K of
the file as saved, so the shipped baseline is the 300 K run and it is verified
against independent references:

- **Analytical** (`s_bar`): the CoolSolve value 126171.992162 J/kmol-K equals
  a recomputation of the same formula in Python (same constants) to
  2.6e-13 relative.
- **Publication** (`s_bar_EES`): the JANAF/NIST absolute entropy of helium,
  S°(298.15 K, 1 bar) = 126.150 J/mol-K, adjusted exactly with cp = 5/2·R
  (monatomic ideal gas) to 300 K and 1 atm gives 126169.13 J/kmol-K — the
  CoolSolve `s_bar_EES = 126172.113` J/kmol-K agrees to **2.4e-5 relative**
  (the residual is the tabulated-data vs equation-of-state difference, within
  the 1e-4 expected for the EES third-law scale, `ees_import.md` §11).
- **Internal agreement**: `s_bar_EES − s_bar = 0.1209 J/kmol-K` (9.6e-7
  relative) — the example's own check.

The stored records themselves were re-checked at their own run point: a
work-folder re-run at T = 1000 K (726.85 °C) reproduces the stored solution
with `compare_solution.py --ees-units`:

> 6 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 7

with actual relative differences of 1.8e-5 on `s_bar`, 6.7e-4 on `s_bar_EES`
(small EES/CoolProp ideal-gas helium data differences) and 4.7e-6 on `m`
(molar-mass last digits). The seven only-in-CoolSolve variables are the
built-in constants (`pi`, `R#`, `k#`, `h#`, `NA#`) plus `T_K` and `G$`. That
check run was made in the temporary work folder only (the shipped `.sol` is
the 300 K baseline).

## Source and attribution

Example 15.5-1 of **S. A. Klein and G. F. Nellis**, *Thermodynamics*,
Cambridge University Press, 2011, distributed as an EES example by F-Chart
Software. The plain-text mirror of the file is published under MIT by
[EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/example_15.5-1.ees)
(inventory candidate `EEX-160`); the binary `.eez` companion with the stored
solution is `ees-examples-raw/Case_Study/example_15.5-1.eez` of the same
repository (original download page in the file header:
https://fchartsoftware.com/ees/examples/examples_thermodynamics_2011/chapter%2015/example%2015.5-1.eez ;
licence tag `{$ID$ … S.A. Klein, F-Chart Software}`: licence holder, not
authorship).

## Conversion log

- **2026-11-15 — import** (`tools/ees_extract.py` on the inner `.EES` of the
  `.eez` companion): EES X11.915, unit system `SI MOLE RAD PA K J`. Manual
  conversion to CoolSolve's SI-°C-Pa-J mass basis (card C-519):
  `T = 26.85 [°C]` (300 K in the original) and the added absolute-temperature
  helper `T_K = T + 273.15` used inside the Sackur-Tetrode equation;
  `P = 101325 [Pa]` (1 atm in the original; the `Convert(atm,Pa)` call is not
  transcribed, per card decision). Molar-to-mass basis: the original
  `m = MW/NA#` relies on EES's molar unit system, where `NA#` is per kmol and
  the stored record is the particle mass in kg (6.6464e-27 kg); CoolSolve's
  `NA#` is fixed at 6.02214076e23 1/mol, so the transcription is
  `m = MW/(NA#*1000)` in kg (same quantity, no physics change). The original
  entropies are molar (EES `Entropy` returns J/kmol-K in the molar system);
  CoolSolve's `entropy()` is per kg, so `s_bar_EES = MolarMass(G$)*Entropy(...)`
  keeps J/kmol-K, the basis of `s_bar` (`R#` = 8314.462618 J/kmol-K).
  `Entropy` receives `T` in °C (CoolSolve convention) while the Sackur-Tetrode
  equation uses `T_K`. Per card decision: the commented-out `G$='Ar'`
  alternative is dropped (helium kept), and the `$ifnot ParametricTable …
  $else $ShowWindow Plot` guard is not transcribed (GUI directive; the
  equations window kept `T = 300 [K]` as its branch). Display directive
  `$TabStops` removed; `{$ID$}`, `{$PX$}`, `{$ST$}` tags removed by the
  extractor. No lookup or parametric tables; comments kept (already English).
  No `.initials`: all equations explicit (0 iterations, system square).
- **Level**: 8 equations → 0; largest block 1 → 0; no functions/arrays → 0;
  not multi-zone → 0; no semi-empirical/off-design physics → 0; no curated
  guesses → 0. Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- Physical validity (as in the original): ideal monatomic gas, classical
  limit — the Sackur-Tetrode equation ignores quantum degeneracy (fine for He
  at 300 K) and internal degrees of freedom.
- No CoolSolve gap: `NA#`, `k#`, `h#`, `R#` are built-in constants and
  `MolarMass`, `Entropy`, `ln` are built-in functions (`missing_features`
  empty).

## Related models

None (`related` empty): the other models of `fundamentals/properties` concern
macroscopic property calls (real vs ideal gas, two-phase states) and none uses
statistical mechanics.
