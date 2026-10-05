# Isothermal expansion of a non-ideal gas: unit of k and boundary work

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0047`

A short introductory exercise on a non-ideal (van der Waals-like) equation of
state: a gas described by $v\,(P + k/v^2) = R\,T$ expands isothermally in a
cylinder while its volume is doubled. The model answers the two questions of the
exercise — what is the unit of the parameter $k$, and what is the boundary work
of the expansion — and computes the work twice, with the EES definite integral
of $P\,dv$ and with the closed form obtained by integrating $P(v)$
analytically, so the two can be compared. It is also a compact example of the
EES `INTEGRAL` function used for a non-time integral.

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | none (fictitious gas of the exercise, described by its own equation of state) |
| **Size** | 12 equations (largest block: 0, see *Limitations*) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition 2, exercise 3 (EES file `R2_E3_2022.EES`) |
| **Authors** | TBD (ULiège course MECA0002 repetition team) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file blocked by `CS-GAP-INTEGRAL-LIMITS` and `CS-BUG-INTEGRAL-FACTOR`; the runnable variant `<name>_coolsolve.eescode` reproduces the EES stored solution (see *Verification*) |

## Problem statement

A gas is described by the equation of state

$$v\,\left(P + \frac{k}{v^2}\right) = R\,T$$

where $v$ is the molar volume. Determine the unit of the parameter $k$. Taking
$k = 10$ (in the unit to be found), 0.2 kmol of this gas expand **isothermally**
at 350 K in a cylinder. Determine the work done during this transformation,
knowing that the initial volume is 2000 L and that it is doubled in the course
of the transformation.

## Model

Since the term $k/v^2$ must be *added to* a pressure, $k$ has the unit of a
pressure times a squared molar volume; with $v$ in m³/kmol and $P$ in Pa,
$k$ is in Pa·m⁶/kmol² (the original works in kPa and states
kPa·m⁶/kmol²). Dividing the equation of state by $v$ gives the explicit form of
the pressure, which is what the model uses:

$$P = \frac{R\,T}{v} - \frac{k}{v^2}$$

The boundary work of the reversible isothermal expansion is
$W_b = -\int P\,dV = -N\int_{v_1}^{v_2} P\,dv$ ($V = N\,v$ at constant amount of
gas). It is computed twice:

- **with the EES integral function**, over the molar volume with a step of
  0.01 m³/kmol (`W_b_EES`);
- **with the closed form**, integrating $R\,T/v - k/v^2$ analytically
  (`W_b_hand`):

$$W_b = -N\left[R\,T\ln\frac{v_2}{v_1} + k\left(\frac{1}{v_2}-\frac{1}{v_1}\right)\right]$$

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `N` amount of gas | 0.2 kmol | `v1_bar` / `v2_bar` initial / final molar volume | 10 / 20 m³/kmol |
| `V1` initial volume | 2 m³ (2000 L) | `k` unit of the EOS parameter | Pa·m⁶/kmol² |
| `V2` final volume | 4 m³ (`V1*2`) | `P` final pressure | 145 470 Pa |
| `T` isothermal temperature | 76.85 °C (350 K) | `W_b_EES` boundary work (integral) | −403 297.8 J |
| `k` EOS parameter | 1E4 Pa·m⁶/kmol² (10 kPa·m⁶/kmol²) | `W_b_hand` boundary work (closed form) | −403 297.8 J |

The negative sign means that the gas receives work: it expands and pushes on
the surroundings, which do work on it.

## How to run

The native file `nonideal_gas_isothermal_work.eescode` is valid EES but
**cannot run in CoolSolve v0.3.0** (two limitations, see *Limitations*). The
runnable variant is `nonideal_gas_isothermal_work_coolsolve.eescode`, with the
baseline `nonideal_gas_isothermal_work_coolsolve.sol`:

```bash
coolsolve ./nonideal_gas_isothermal_work_coolsolve.eescode
```

No guess values are needed. The variant changes only what the gaps force: the
definite integral is written in the canonical state-equation form and its
limits are inlined as the constants 10 and 20 (see *Conversion log*). Both files
can be opened in the CoolSolve GUI, but only the variant solves.

## Results

The 0.2 kmol of gas expand from a molar volume of 10 to 20 m³/kmol (2 → 4 m³)
at 350 K. The pressure drops from 290.9 kPa to **145.47 kPa** and the boundary
work is **W_b = −403.3 kJ** for both evaluations (negative: work received by
the gas). The two evaluations agree because CoolSolve integrates $P\,dv$ with
RK4 on the same interval; the small difference with the EES value comes from
EES's own quadrature (see *Verification*).

CoolSolve writes the trajectory of the integration variable (`v_bar`, the molar
volume from 10 to 20 m³/kmol) with the running integral and the pressure into
`nonideal_gas_isothermal_work_coolsolve.sol` (section `# IntegralTable`, 1000
rows) and into `<name>-integral.csv` next to the model file; the CSV is a
regenerated output and is not kept in the folder.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. the pressure along the
     isotherm P = R*T/v - k/v^2, or the two evaluations of the work vs the volume ratio,
     figures/nonideal_gas_isothermal_work_*.png -->

## Verification

The converted model cannot run (native file blocked), so **the variant
`nonideal_gas_isothermal_work_coolsolve.eescode` was verified** against the
solution stored in the original EES file:

```bash
python3 tools/compare_solution.py nonideal_gas_isothermal_work_coolsolve.sol \
    <work>/reference/ees_variables.csv --ees-units
```

> 12 common variables, 0 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 2

| Variable | EES (converted) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `k` | 10000 | 10000 | 0 |
| `N` | 0.2 | 0.2 | 0 |
| `P` | 145470 | 145470 | 0 |
| `R` | 8314 | 8314 | 0 |
| `T` | 76.85 | 76.85 | 3.70e-16 |
| `V1` / `V2` | 2 / 4 | 2 / 4 | 0 / 0 |
| `v1_bar` / `v2_bar` | 10 / 20 | 10 / 20 | 0 / 0 |
| `v_bar` | 20 | 20 | 0 |
| `W_b_EES` | −403298 | −403298 | **9.02e-08** |
| `W_b_hand` | −403298 | −403298 | 1.05e-10 |

Maximum relative deviation **9.02e-08** (`W_b_EES`), i.e. `verification.max_rel_diff`.
It is fully explained by the numerical integration, not by the physics or by the
unit conversion: re-evaluating the EES `INTEGRAL` call as a trapezoidal rule
with its step of 0.01 m³/kmol gives −403297.8325 J, **exactly** the value stored
by EES (3.3e-11), whereas CoolSolve integrates the same limits with RK4 and
returns −403297.7961 J, which is the exact value of the closed form
(`W_b_hand`, deviation 1.05e-10 from EES).

Variables excluded from the comparison:

- `a` = 8.31434 (kJ/kmol·K), present only in the EES file: a stale record of
  the molar gas constant under an older name (`R` is the one used by the
  equations), not part of the model;
- `T_K` and `W_b_int` are present only in CoolSolve: `T_K` is the absolute
  temperature added by the unit conversion (K → °C) and `W_b_int` is the
  integral split out of the state equation by the variant (see *Conversion log*).

No companion Python/CoolProp solution of this exercise exists in the course
folder: `Python/ThAp21_R02E03.py` carries the same exercise number of the
2020-2021 edition but solves a different problem (water cooled in a rigid
vessel). It was not used as a reference.

## Source and attribution

Exercise solution of the course *Thermodynamique appliquée* (MECA0002),
Université de Liège, repetition session 2 (2022-2023). The EES file itself
names no author (only the laboratory licence tag); the inventory attributes
the course material to S. Quoilin with repetition assistants N. Paulus and
B. Dechesne (from companion Python/Word metadata), to be confirmed by the
maintainer.

Source file (EES 10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R2/R2_E3_2022.EES`
(inventory candidate `TM-0399`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MOLE DEG KPA K KJ` with decimal commas (converted by the
  tool); the whole model converted **by hand** to SI-°C-Pa-J
  (ees_import.md §6): `R = 8314 [J/kmol-K]` ("8.314 kJ/kmol-K in the
  original"), `k = 1E4 [Pa·m^6/kmol^2]` ("10 kPa·m^6/kmol^2 in the
  original"), `T = 76.85 [°C]` ("350 K in the original"). The quantities in m³
  and m³/kmol are unchanged, and the integration step 0.01 m³/kmol is a
  volume step, unchanged as well. **Molar basis kept** (kmol, J/kmol): the
  molar → mass conversion of ees_import.md §6.2 step 6 needs the molar mass of
  the fluid, and the gas of this exercise is fictitious — it has no molar mass
  and no substance name in EES. No absolute-temperature relation was missed:
  the only one, the product `R*T` of the equation of state, now uses the
  explicit absolute temperature `T_K = T + 273.15` (ees_import.md §6.2
  step 5), which also makes the answer independent of the `T` unit setting.
  Comments translated to English (paraphrasing the original's own comments),
  standard header added, no equation changed otherwise.
- **2026-10-05 — runnable variant** `nonideal_gas_isothermal_work_coolsolve.eescode`:
  the native file stays in valid EES and is **not** rewritten around the gaps.
  The variant changes exactly two things, both forced by CoolSolve v0.3.0, and
  uses no CoolSolve-only syntax (it is valid EES):
  1. the factor `-N` is moved out of the integral call —
     `W_b_int = 0 + integral(P, v_bar, 10, 20, 0.01)` then
     `W_b_EES = -N*W_b_int` — because CoolSolve silently ignores a factor
     multiplying an `INTEGRAL` call (`CS-BUG-INTEGRAL-FACTOR`). Measured on the
     native form: the same run with the limits inlined returns
     **+2 016 489 J** (the bare integral) instead of −403 298 J, with
     *SUCCESS* and no warning — the split form returns the correct value;
  2. the integration limits `v1_bar` and `v2_bar` are inlined as the literal
     constants `10` and `20` (they are constant expressions `V1/N` and `V2/N`)
     because CoolSolve rejects symbolic limits
     (`CS-GAP-INTEGRAL-LIMITS`, error *"Non-constant integration limits are not
     yet supported"*). If `N`, `V1` or the ratio `V2/V1` are changed, the two
     limits must be updated.
  Variable names, constants, input values and all other equations are identical
  to the native file; the added `W_b_int` is the only new symbol.
- **Duplicate group DG-0097** (2 files, triaged per workflow §2):
  - `TM-0405` (`save/R2_E3_2022.EES`, `duplicate`): the stripped-equation diff
    against TM-0399 is identical — all 12 equations match character by
    character. The only difference is a typo **in the problem-statement
    comment** of the backup copy, which writes the equation of state as
    `v(P+kv²)=RT` instead of `v(P+k/v²)=RT`; the equations of that file use
    `k/v_bar^2` like the representative.
- **Level**: 12 equations (0) + largest block 0 (0; CoolSolve reports 0 blocks
  for any model with `INTEGRAL` calls, `CS-DOC-SQUARE-INTEGRAL`) + no
  functions/arrays (0) + no multi-zone (0) + no calibration/dynamics (0) + no
  curated guesses (0) = 0 → level 1.
- **Kind**: `steady`. The model computes one operating point of a quasi-static
  process; the integral is a *definite* integral over the molar volume (a
  parameter, not time). CoolSolve nevertheless routes any model with an
  `INTEGRAL` call to its dynamic solver, which is why the `-d` analysis reports
  a non-square system and 0 blocks.

## Limitations and CoolSolve gaps

CoolSolve v0.3.0 limitations that block the **native** file (both listed in
`model.json` `missing_features`, see CoolSolve
`docs/model_library_support.md` §4 and §5):

- `CS-GAP-INTEGRAL-LIMITS` — symbolic `INTEGRAL` limits (variables or
  expressions) are rejected: the native call
  `integral(P, v_bar, v1_bar, v2_bar, 0.01)` stops the solver with
  *"Non-constant integration limits are not yet supported (resolve parameters
  before the INTEGRAL call)"*, although `v1_bar = V1/N` and `v2_bar = V2/N` are
  constants of the model.
- `CS-BUG-INTEGRAL-FACTOR` — a factor multiplying an `INTEGRAL(...)` call is
  silently ignored. The native call `W_b_EES = -N*integral(...)` therefore
  returns the bare integral ∫P dv = +2 016 489 J instead of
  −N·∫P dv = −403 298 J, reporting *SUCCESS* with no warning. This one alone
  would make the model wrong without any error.

The runnable variant works around both (see *Conversion log*).

Model limits, unrelated to CoolSolve:

- the gas is fictitious: only $v(P + k/v^2) = R\,T$ is known, no real fluid
  corresponds to it, so the molar basis cannot be left;
- $k = 10$ (Pa·m⁶/kmol²) is a small perturbation here — the $k/v^2$ term of
  the equation of state is 0.1 kPa at 10 m³/kmol against 291 kPa of the
  $R\,T/v$ term, i.e. the gas behaves almost ideally (about 0.03 % on the work).
  The exercise asks for the unit of $k$, not for a real-fluid computation;
- the work integral of the equilibrium pressure describes a quasi-static
  (reversible) path, as in the original. The work is negative because the gas
  expands and the surroundings do work **on** it.

## Related models

- `CSL-0010` *two_stage_steam_compressor_intercooling*: also a `INTEGRAL` model
  of the same course, blocked by the same two IDs; its runnable variant applies
  the same two workarounds.
- `CSL-0044` *rigid_tank_water_mixture*: sibling introductory exercise of the
  same course (repetition 1), a property/quality problem solved with the real
  fluid Water.
- `CSL-0059` *stirling_cycle_ideal_regenerator*: the same use of an EES definite
  integral of `p dv` in a cycle (the two isothermal works of an ideal Stirling
  cycle), blocked by the same two limitations plus the single integration
  variable per model; its runnable variant applies the same workaround.
