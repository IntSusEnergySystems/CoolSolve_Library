# Maximum work from two air tanks at 900 K and 300 K

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ☑️ **Runs** &nbsp;|&nbsp; `CSL-0057`

Two rigid vessels, each holding 30 kg of air at 900 K and at 300 K, are coupled
by a heat engine that takes heat from the hot vessel, delivers it to the cold one
and produces work. The model asks for the **maximum** work this engine can
deliver, i.e. the reversible end state: an entropy balance on the *extended*
system (engine + both vessels) gives the common final temperature of the two
vessels, from which the work follows. A short, explicit exercise in the second
law on an ideal gas — the classical result is the geometric-mean temperature
$\sqrt{T_a T_b}$.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Air (ideal-gas substance: `cv(Air, T=…)` only) |
| **Size** | 13 equations, largest block 4 (the 4 unknowns `T_2`, `cv_air`, `DELTA_S_1`, `DELTA_S_2`) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition session 10 (exergy), exercise 3 (EES file `R10_E03_2022.EES`, session 2022-2023) |
| **Authors** | TBD (ULiège, course *Thermodynamique appliquée*; the session statement names the repetition assistants N. Paulus, A. Zeoli and V. Lemort) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs (see *Verification*: no independent numerical reference exists for this exercise) |

## Problem statement

Two vessels of constant volume are each filled with 30 kg of air, one at 900 K
and the other at 300 K. A heat engine is placed between the two vessels: it
takes heat from the first one, delivers it to the second one and produces work.
Determine the maximum work that can be delivered this way, and the final
temperatures of the two vessels.

## Model

The system is the **extended** system — the engine and both vessels — and the
work produced by the engine stays inside it. No mass and no work cross the
boundary of the extended system, so for a reversible process the total entropy
change is zero (`S2 - S1 = S_gen = 0`); the entropy change of the engine over one
cycle is zero. Each vessel being rigid (`p dv = 0`), the Gibbs relation gives
$T\,ds = du = c_v\,dT$, hence

$$\Delta S_1 = m_{air}\,c_{v,air}\,\ln\frac{T_{1a}}{T_2},\qquad
  \Delta S_2 = m_{air}\,c_{v,air}\,\ln\frac{T_{1b}}{T_2}$$

and the closure of the model is `DELTA_S_1 + DELTA_S_2 + DELTA_S_heat_engine = 0`
with `DELTA_S_heat_engine = 0`. Because both vessels contain the same mass of
air and the same constant `cv`, the balance reduces to
$T_2^2 = T_{1a}T_{1b}$: the final temperature is the **geometric mean** of the
two initial temperatures, whatever the value of `cv_air` — which is why the
maximum work does not depend on the heat capacity chosen.

The specific heat is taken constant and evaluated at the final temperature
`T_2`, "the temperature intermediate between the two vessels", as in the
original (which notes that the ambient temperature could be used instead without
really changing the results). The heat exchanged with each vessel and the work
are then

$$Q_{source} = m_{air}c_{v,air}(T_2-T_{1a}) < 0,\qquad
  Q_{sink} = m_{air}c_{v,air}(T_2-T_{1b}) > 0$$
$$W_{max} = -\big(|Q_{source}|-|Q_{sink}|\big),\qquad
  \eta_{max} = \frac{W_{max}}{Q_{source}}$$

The engine takes 8.52 MJ from the hot vessel, gives 4.92 MJ to the cold one and
delivers the difference, 3.60 MJ.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_1a` initial temperature of the hot vessel | 626.85 °C (900 K) | `T_2` common final temperature | 246.465 °C (519.615 K) |
| `T_1b` initial temperature of the cold vessel | 26.85 °C (300 K) | **`W_max_delivered` maximum work** | **3.5995 MJ** |
| `m_air` air mass in each vessel | 30 kg | `Q_source`, `Q_sink` heat of the two vessels | −8.5164 MJ, +4.9170 MJ |
| | | `eta_max` ratio `W_max/Q_source` | 0.42265 |
| | | `DELTA_S_1` = −`DELTA_S_2` | ±12 298.4 J/K |
| | | `cv_air` at `T_2` | 746.3 J/(kg·K) |

## How to run

Open `two_tanks_max_work_air.eescode` in the CoolSolve GUI and press *Solve*, or
from a terminal:

```bash
coolsolve ./two_tanks_max_work_air.eescode
```

The single guess of `two_tanks_max_work_air.initials` (`T_2` = 246.465 °C, the
geometric mean of the two initial temperatures) is needed: from a cold start the
4-variable block `T_2`/`cv_air`/`DELTA_S_1`/`DELTA_S_2` gives up with
*MaxIterations* — from `T_2` = 1 °C the Newton iterations walk over more than
200 K, and the specific heat `cv(Air, T=T_2)` changes by about 20 J/(kg·K) over
that range (726.8 J/(kg·K) at 402.9 K, 746.3 J/(kg·K) at 519.6 K). No solver
settings and no runnable variant are needed. The dead variable `T_0`
of the original (298.15 K, used in none of its equations) was removed, so the
system is square: **13 equations, 13 unknowns, `System square: Yes`**.

## Results

| Variable | Value | Unit |
|---|---:|---|
| `T_2` final temperature of both vessels | 246.465 | °C (519.615 K) |
| `cv_air` specific heat of air at `T_2` | 746.30 | J/(kg·K) |
| `Q_source` heat taken from the hot vessel | −8 516 423 | J |
| `Q_sink` heat delivered to the cold vessel | 4 916 959 | J |
| `W_max` as written in the original (negative, see *Conversion log*) | −3 599 464 | J |
| **`W_max_delivered` maximum work delivered by the engine** | **3 599 464** | **J** |
| `eta_max` = `W_max`/`Q_source` | 0.422650 | – |
| `DELTA_S_1` / `DELTA_S_2` | +12 298.4 / −12 298.4 | J/K |

Both vessels end at **246.5 °C**, i.e. 219.6 K above the cold one and 380.4 K
below the hot one; this is well below the 326.85 °C (600 K) they would reach by
direct thermal exchange without an engine (`T2_bis = (T_1a+T_1b)/2`, discussed in
the original's own commentary and checked here) — the difference is the
temperature gap the engine exploits. Of the 8.52 MJ withdrawn from the hot
vessel, 4.92 MJ (58 %) ends up in the cold vessel and 3.60 MJ (42 %) is
delivered as work; `eta_max` = 0.42265 is exactly the Carnot ratio of the two
log-mean temperatures of the vessels, 1 − 399.80 K/692.48 K, as a reversible
engine between them must be.

No thermodynamic path is described by this model (two isolated end states on air,
no property state points), so its library figure is a parametric sweep (roadmap
decision D7, ideal-gas models have no diagram in CoolSolve).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep of
     T_2 and W_max_delivered vs T_1b (or vs m_air), figures/two_tanks_max_work_air_sweep.png -->

## Verification

**The solution stored by EES cannot be used as a reference.** The source file was
never solved after being saved: all 13 decoded variable records hold their EES
*initial* value (`1`, except `DELTA_S_heat_engine = 0` and the unused `T_0` =
298.15). `compare_solution.py … --ees-units` accordingly reports
*12 common variables, 8 differ (rtol=0.001)* with every reference value equal to
1 — the known behaviour of `CS-BUG-EXTRACT-STALE` (EES does not rewrite the
variable records at save). The course folder holds no Python/CoolProp solution
of exercise 3 (only of exercises 1 and 2, `old/ThAp21_R10E01.py`,
`old/ThAp21_R10E02.py`), and the session's PowerPoint (`R10_2021v1.pptx`) only
covers exercises 1 and 2. **The model is therefore shipped as `runs`, not
`verified`.**

**Check used instead: the closed-form solution of the same entropy balance**,
derived by hand and written as a reference CSV in the same format as an EES
variable list (`compare_solution.py` reads it unchanged):

$$T_2 = \sqrt{T_{1a}T_{1b}},\quad
  Q_{source} = -m_{air}c_v(T_{1a}-T_2),\quad
  W_{max} = m_{air}c_v\left(\sqrt{T_{1a}}-\sqrt{T_{1b}}\right)^{2}$$

**11 common variables, 0 differ (rtol=0.001)** — the largest deviation is the
solver's own maximum relative error, **1.04·10⁻¹⁵**:

| Variable | closed form | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `T_2` [°C] | 246.46524227066323 | 246.46524227066323 | < 1·10⁻¹⁵ |
| `Q_source` [J] | −8 516 422.921 | −8 516 422.921 | 9.2·10⁻¹⁶ |
| `Q_sink` [J] | 4 916 959.066 | 4 916 959.066 | 9.3·10⁻¹⁶ |
| `W_max` [J] | −3 599 463.855 | −3 599 463.855 | 1.3·10⁻¹⁵ |
| `eta_max` | 0.4226497308 | 0.4226497308 | 8.7·10⁻¹⁶ |
| `DELTA_S_1` [J/K] | 12 298.39877437 | 12 298.39877437 | 1.4·10⁻¹⁵ |
| `DELTA_S_2` [J/K] | −12 298.39877437 | −12 298.39877437 | 1.4·10⁻¹⁵ |

Two CoolSolve variables are excluded from the comparison, both named here:
`cv_air` is the property-backend value (it is not part of the closed form — it
is consistent, `cp(Air) − cv(Air)` = 287.4 J/(kg·K) at 519.6 K, i.e. the gas
constant of air 287.05 J/(kg·K) to 0.13 %), and `W_max_delivered` is the
post-processing output added by the import (equal to `-W_max`).

`eta_max` is a second, fully independent check: the ratio `W_max/Q_source`
computed by the model equals, to all printed digits, the Carnot ratio of the
log-mean temperatures of the two vessels, `1 − T_c,lm/T_h,lm` =
1 − 399.80/692.48 = 0.42264973, which contains neither the algebra of the model
nor its temperature shift.

## Source and attribution

Solution of repetition exercise 3 (session 10, on exergy) of the ULiège course
*Thermodynamique appliquée* (MECA0002); the exercise asks for the maximum work
obtainable from two air tanks coupled by a heat engine and for the final
temperatures. The EES file names no author (its `{$ID$}` tag is the laboratory's
student/staff licence, and the folder `R10` carries no initials); the session
statement of the course (`ThAp22_R10.docx`, exercise 3, session 2022-2023) lists
the repetition assistants N. Paulus, A. Zeoli and V. Lemort — to be confirmed by
the maintainer.

Source file (EES X10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R10/R10_E03_2022.EES`
(inventory candidate `TM-0390`, representative of the 2-file duplicate group
`DG-0094`; see *Decisions* below).

## Decisions on the duplicate group (inventory `DG-0094`)

The group is one exercise in two files (the same file, loose and inside an
archive). The two extractions were compared after stripping the comments and the
blank lines: 24 non-empty lines each, of which the 12 equations, and the equations
are identical.

| Row | File | Equations | Decision |
|---|---|---|---|
| `TM-0390` | `2022-2023/R10/R10_E03_2022.EES` | representative (12 equations) | `added` → `CSL-0057` |
| `TM-0545` | `2022-2023/R10/R10.zip!/R10_E03_2022.EES` | identical to `TM-0390` | `duplicate` of `CSL-0057` |

The two files differ by one character in the last explanatory comment of the
original ("la machine motrice importe **peu**" against "… importe **peut**",
13 199 against 13 200 bytes), not in any equation.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): EES
  X10.836, 13 variable records (the *unsolved* initial values described in
  *Verification*), no lookup or parametric table, no external function (only the
  built-in `abs`, `cv` and `ln`); `{$ID$}`, `{$PX$96}` and `{$ST$ON}` tags
  removed, no NUL byte (the equations are stored as plain text, so
  `CS-BUG-EXTRACT-NUL` does not apply).
- **Unit system** `SI MASS DEG KPA K KJ` converted **by hand** to
  `SI MASS DEG PA C J`. The only quantity that changes is the temperature:
  `T_1a = 626.85 [C]` (900 K) and `T_1b = 26.85 [C]` (300 K), original values
  kept in the comments. The masses were already in kg; the specific heat, the
  entropies and the energies change unit by ×1000 (kJ → J) *implicitly*, since
  the single property call `cv(Air, T=T_2)` returns J/(kg·K) in CoolSolve and
  every other equation is homogeneous in the converted quantities — no
  conversion factor had to be written anywhere. The `$UnitSystem` directive was
  deleted. No pressure appears in the model.
- **The two logarithms needed absolute temperatures** (ees_import.md §6,
  step 5): a ratio of temperatures is *not* invariant under the K → °C shift.
  Writing the relations literally as `ln(T_1a/T_2)` with °C values converges to
  a spurious root of the model, `T_2` = 129.734 °C instead of 246.465 °C (the
  shift changes `T_1a·T_1b ≠ (T_1a−273.15)(T_1b−273.15)`), with `W_max`
  negative. The equations therefore read
  `ln((T_1a+273.15)/(T_2+273.15))` and `ln((T_1b+273.15)/(T_2+273.15))`, i.e.
  the absolute temperature is written explicitly once, as the conversion
  procedure prescribes; the physics of the original is untouched.
- **Comments translated** to English, paraphrasing the French original (its
  entropy-balance note, its Gibbs-relation derivation, its note on the choice of
  the temperature at which `cv` is evaluated, its note that the two vessels are
  stabilised at `T_2`, and its long complementary explanation of `T2_bis`,
  which is kept as display comments at the end of the file). Section titles in
  the `"!…"` display form, standard header added.
- **Variable names kept** as in the original (`T_1a`, `T_1b`, `m_air`,
  `DELTA_S_1`, `DELTA_S_2`, `DELTA_S_heat_engine`, `cv_air`, `Q_source`,
  `Q_sink`, `W_max`, `eta_max`). Two changes:
  - `T_0` (298.15 K in the stored solution) appears in **none** of the
    equations of the original — dead code, removed: with
    it the model is not square in CoolSolve (13 records for 12 equations), without
    it 13 equations for 13 unknowns;
  - `W_max_delivered = abs(Q_source)-abs(Q_sink)` added as a post-processing
    output, because the sign convention of the original's
    `W_max = -(abs(Q_source)-abs(Q_sink))` yields a *negative* value for a work
    the engine *delivers*: the magnitude, 3.5995 MJ, is the physical maximum
    work and is what the results table above reports. The equation of the
    original is kept unchanged, so `W_max` = −3.5995 MJ as EES would compute it,
    and `eta_max` = `W_max`/`Q_source` = +0.42265 stays positive because both
    terms are negative. All other results are unaffected by the added line.
- **No state-point arrays added**: the model describes two isolated end states of
  air and no thermodynamic path, so there is nothing to overlay on a diagram
  (figure = parametric sweep, as for the other ideal-gas models).
- **Level**: equations 13 (< 50 → 0), largest algebraic block 4 (≤ 5 → 0),
  structure: no function, procedure or array (0), no multi-zone or
  discretisation and fewer than three coupled components (0), no semi-empirical,
  off-design or dynamic physics (0), one curated guess in
  `<model>.initials` needed to converge (1) → score 1 → level 1.

## Limitations and CoolSolve gaps

- The model is the original's: constant `cv` of air (evaluated at the final
  temperature), one common final temperature for the two vessels (the engine
  works between the two *bodies*, not between two fixed reservoirs), a
  reversible transformation and no losses (pressure drop, heat leak, engine
  irreversibility). The maximum work is therefore a bound, not a machine
  design.
- The results scale linearly with `cv_air`, i.e. with the property backend's
  ideal-gas model for air (`CV` of CoolProp's `Air`); `T_2` and `eta_max` do not
  depend on it.
- No CoolSolve gap blocks this model. `CV(Air, T=…)` (ideal gas, temperature
  only), `abs` and `ln` are supported; the `cv()` call emits two cosmetic hints
  during the iterations (a moist-air reminder and a "looks like a temperature
  in K" hint on intermediate Newton values), which do not affect the solution.
- `CS-GAP-UNITSYSTEM` applies to the original (`KPA K KJ` is read but ignored by
  CoolSolve); the manual conversion removes it, so it is not blocking.

## Related models

- `CSL-0045` *steam_turbine_exergy_balance*: same course and same session 10
  (exergy), on an open system — the reversible-work and second-law-efficiency
  counterpart of this exercise on a turbine.
- `CSL-0048` *two_tanks_connected_valve_r12*: two vessels again, on a real fluid
  in the two-phase dome, same course and import route.
- `CSL-0044` *rigid_tank_water_mixture*: rigid-vessel thermodynamics on a
  real fluid.
- `CSL-0003` *methane_tank_evaporation*: mass and phase change in a rigid tank,
  same course family.