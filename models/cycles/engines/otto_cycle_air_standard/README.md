# Air-standard Otto cycle (ideal gas, variable specific heats)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0049`

The theoretical Otto cycle solved exactly as the original exercise does it:
air is an ideal gas whose specific heats depend on temperature, the ratio of
the specific heats γ is evaluated at the **mean temperature of each isentropic
transformation** and c_v is held **constant over each transformation**. The
model returns the four state points, the maximum pressure and temperature of
the cycle, the net work per unit mass, the thermal efficiency, and the work and
power of a multi-cylinder engine running at 4000 rpm. It is the simplest
library model of an air-standard cycle and a good reference for the
Laplace law, the closed-system first law and the recursive ("γ depends on T₂,
and T₂ depends on γ") solution of such exercises.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal-gas behaviour, `cp`/`cv`/`entropy` of `Air`) |
| **Size** | 45 equations (largest block: 3) |
| **Source** | ULiège, course *Thermodynamique appliquée* (MECA0002), session R5 (chapter 9 part 1, engines), exercise 1 — EES file `R05_E01_2022.EES` (`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R5/`) |
| **Authors** | TBD (ULiège course MECA0002; the session statement sheet `ThAp22_R05.docx` of the same folder lists the repetiteurs N. Paulus, A. Zeoli and V. Lemort; the EES file itself carries no author name, only the laboratory licence tag) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs and agrees with an independent Python/CoolProp solution of the same exercise to 2.1·10⁻¹¹ relative (42 variables), and with the meaningful part of the EES stored solution to 1.5·10⁻⁵ |

## Problem statement

An ideal Otto cycle receives **800 kJ of heat per kilogram of air** and has a
**compression ratio of 8**. At the beginning of the compression, the air is at
**100 kPa and 17 °C**. Determine:

- the maximum pressure and the maximum temperature of the cycle;
- the net work of the cycle;
- the thermal efficiency of the cycle;
- the total work per cycle and the power of a **1.6 L engine** performing this
  cycle with **4 cylinders at 4000 rpm**.

## Model

The four states are numbered as in the original: 1 = start of compression,
2 = end of compression, 3 = end of the constant-volume heat addition,
4 = end of the expansion.

- **Specific heats.** `gamma01` and `gamma34` are the ratios `cp/cv` evaluated
  at the mean temperature of the isentropic transformations 1‑2 and 3‑4;
  `cv12`, `cv23`, `cv34` and `cv41` are the values of `cv` at the mean
  temperature of each transformation, held constant over it (the original
  comments point out that this would not be judicious over large temperature
  variations). All these are `cp`/`cv` calls with a temperature argument only,
  i.e. they depend on temperature alone.
- **Ideal-gas law** at each state, `p = r_bis·T/v` with
  `r_bis = R#/molarmass(fluid$)` (287.047 J/(kg·K) for air). The law needs an
  **absolute temperature**: in the library unit system the state temperatures
  are in °C, so `+273.15` appears in the four equations of the law.
- **Laplace law** `p·v^gamma = constant` on the two isentropic transformations,
  coupled to `v[2] = v[1]/r_v` and `v[4] = v[1]` (the following transformation
  is isochoric).
- **First law for a closed system**, `w_ij + q_ij = cv_ij·(T[j] − T[i])`, on
  the four transformations, with `q_12 = q_34 = 0` (isentropic) and `q_23 = q`
  (the heat given in the statement); `w_23 = w_41 = 0` (isochoric).
- **Sign convention of the original**: `w` is the work **received** by the
  system, so `w_12 > 0` (compression) and `w_34 < 0` (the system produces
  work); `w_net_cycle` and `W_net` are therefore **negative** and the engine
  power comes out as −26.5 kW. The efficiency uses `abs(w_net_cycle/q)`. The
  original adds the two routes to the net work, `w_net_cycle` (sum of the
  works) and `w_net_cycle_bis = -(q_23 + q_41)` (heat added minus heat
  rejected), and notes that they are not exactly equal because γ, c_p and c_v
  are treated as constants.
- **Engine**: the mass admitted at each intake is `m = V_d/v[1]` (the total
  displacement over the specific volume at the intake state, i.e. the whole
  engine, not one cylinder), the work per cycle is `W_net = m·w_net_cycle`,
  and the power is `W_dot_net = W_net·n/2/60` (a four-stroke engine performs
  one cycle per two revolutions).
- **Post-processing**: the entropies `s[1..4]` at the four states are computed
  "for information", as in the original.

The recursive structure is the whole difficulty of this exercise: `gamma01`
depends on `T[2]`, and `T[2]` is only known through the Laplace law that uses
`gamma01`. CoolSolve solves the whole system simultaneously
(`coolsolve -d` reports *System square: Yes*, 45 equations / 45 variables);
with the shipped `.initials` it converges in 13 iterations.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `r_v` compression ratio | 8 | `p_max` maximum pressure | 4.325 MPa |
| `q` heat added per unit mass | 800 kJ/kg | `T_max` maximum temperature | 1295.6 °C |
| `p[1]` inlet pressure | 100 kPa | `w_net_cycle` net work per unit mass | −413.7 kJ/kg |
| `T[1]` inlet temperature | 17 °C | `w_net_cycle_bis` net work, heat route | −417.5 kJ/kg |
| `V_d` total displacement | 1.6 L | `eta_otto` thermal efficiency | 0.5172 |
| `n` engine speed | 4000 rpm | `W_net` work per cycle | −794.8 J |
| `fluid$` working fluid | Air | `W_dot_net` engine power | −26.49 kW |
| | | `m` admitted mass per cycle | 1.921·10⁻³ kg |

## How to run

Open `otto_cycle_air_standard.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./otto_cycle_air_standard.eescode
```

The `.initials` file is **needed**: the four `cp`/`cv` calls of the recursive
solution start from wild intermediate temperatures, and a cold start (no
`.initials`) makes CoolSolve fail the final verification of the `entropy()`
calls. The shipped guesses are the converged values, so the solve is
immediate and reproducible. No `coolsolve.conf`, no lookup table, no variant.

## Results

State points (per unit mass) and the indicators of the cycle:

| | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| `p[i]` [Pa] | 100 000 | 1.800·10⁶ | 4.325·10⁶ | 2.754·10⁵ |
| `T[i]` [°C] | 17.0 | 379.7 | 1295.6 | 525.9 |
| `v[i]` [m³/kg] | 0.83287 | 0.104109 | 0.104109 | 0.83287 |
| `s[i]` [J/(kg·K)] | 3856.9 | 3856.2 | 4607.3 | 4615.1 |

| Indicator | Value |
|---|---|
| `eta_otto` | 0.5172 |
| `w_net_cycle` / `w_net_cycle_bis` | −413 738 / −417 522 J/kg (0.91 % apart) |
| `gamma01` / `gamma34` | 1.3900 / 1.3244 |
| `cv12` / `cv23` / `cv34` / `cv41` | 737.2 / 873.5 / 885.0 / 751.5 J/(kg·K) |
| `m`, `W_net`, `W_dot_net` | 1.921·10⁻³ kg, −794.8 J, −26.49 kW |

The four checks of the exercise come out as follows:

- **maximum pressure and temperature** — `p_max` = 4.325 MPa,
  `T_max` = 1295.6 °C (i.e. 1568.7 K), both reached at state 3, at the end of
  the constant-volume heating;
- **net work** — 413.7 kJ per kg of air (positive magnitude; the model stores
  it negative, see the sign convention above);
- **thermal efficiency** — 51.7 %;
- **engine** — −794.8 J per cycle over the whole 1.6 L engine, i.e. −26.49 kW
  at 4000 rpm (6.62 kW per cylinder). The corresponding mean effective
  pressure, `W_net/V_d`, is 497 kPa.

Two physical remarks, both consequences of the closure chosen in the original
and confirmed here:

- the efficiency (51.7 %) is **below** the constant-γ value
  `1 − 1/r_v^(γ−1) = 1 − 1/8^0.4 = 56.5 %` (γ = 1.4), because c_v is treated as
  constant over a temperature range of 290 K to 1569 K while it actually rises
  from 718 to 931 J/(kg·K) (values of `cv(Air, T=…)` from the property
  backend);
- the two net-work routes differ by 0.91 % for the same reason, exactly as the
  original comment states.

The isentropic transformations are only *approximately* isentropic, because
γ is evaluated at a mean temperature: `s[2] − s[1]` = −0.67 J/(kg·K) and
`s[4] − s[3]` = +7.8 J/(kg·K), i.e. 1.7·10⁻⁴ and 1.7·10⁻³ of the entropy
level, which is the expected size of the mean-temperature approximation.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the charge is an
     ideal gas and CoolSolve has no ideal-gas diagram (CS-FEAT-DIAGRAM-IDEAL), so the
     figure of this model is a parametric sweep plot (roadmap decision D7), e.g. the
     thermal efficiency eta_otto and the maximum temperature T_max as functions of the
     compression ratio r_v, obtained with the Parametric tab of the GUI (values
     below checked by re-solving the model with r_v set to 4, 6, 8, 10, 12):
      r_v = 4     6     8     10    12
      eta_otto 0.386 0.467 0.517 0.553 0.581
      T_max   1172  1240  1296  1342  1382 °C
     saved as figures/otto_cycle_air_standard_rv.png  -->

## Verification

**Reference 1 — independent re-implementation (main reference).** The same
exercise was re-implemented in Python with CoolProp (`cp`, `cv`, `entropy` of
Air, and a fixed-point iteration on the recursive equations `T[2]`, `T[3]`,
`T[4]`), outside the library. `compare_solution.py` on the two result files
prints

```
42 common variables, 0 differ (rtol=1e-09); only in EES: 0; only in CoolSolve: 4
```

with `--rtol 1e-9 --all`: the **largest relative deviation is 2.11·10⁻¹¹** (on
`v[2]` and `v[3]`), everything else being equal to the printed digits. The
four variables only in CoolSolve are `fluid$`, its string copy in the `.sol`
file (`CS-BUG-SOL-STRING`), `R#` and `r` (the reference value 287 J/(kg·K) that
no equation uses). Both implementations use the same
property backend (CoolProp), so this checks the equations, the unit conversion
and the recursive solution, not the property data.

**Reference 2 — the stored EES solution (partial).** The source file was saved
**before a complete solution**: 25 of its 43 stored values are the placeholder
`1` (EES writes `1` for a variable that was never computed), and
`compare_solution.py … --ees-units --all` reports

```
44 common variables, 26 differ (rtol=0.001); only in EES: 3; only in CoolSolve: 2
```

(the three only in EES are `gamma`, `p` and `v`, leftovers of the EES
workspace; the two only in CoolSolve are `R#` and `r`.) Of the 26 differences:

- **18 variables carry a real stored value** and agree (18 lines marked *ok*):
  the inputs (`p[1]`, `T[1]`, `q`, `r`, `r_v`, `V_d`, `n`) and the zeros
  (`q_12`, `q_23`, `q_34`, `w_23`, `w_41`) identically, and `v[1]`, `v[2]`,
  `v[3]`, `v[4]`, `m`, `r_bis` to **1.51·10⁻⁵** relative (the molar mass of dry
  air: 28.966 kg/kmol in EES, 28.96546 kg/kmol in CoolProp). This is a real
  check of the specific gas constant, of the ideal-gas law and of the
  kPa → Pa conversion of the exercise data;
- **`s[1]` = 5672.12 vs 3856.91 J/(kg·K)** is a constant offset between the
  entropy reference states of the EES ideal-gas `Air` table and of CoolProp
  `Air` (a reference-state offset; the entropy *differences*,
  which are what the model uses, agree — see the isentropy check in *Results*);
- the other **25 variables** (`T[2]`, `T[3]`, `T[4]`, `p[2]`, `p[3]`, `p[4]`,
  `p_max`, `T_max`, `gamma01`, `gamma34`, `cv12`, `cv23`, `cv34`, `cv41`,
  `w_12`, `w_34`, `q_41`, `eta_otto`, `W_net`, `W_dot_net`,
  `w_net_cycle`, `w_net_cycle_bis`, `s[2]`, `s[3]`, `s[4]`) hold the EES
  placeholder `1`, so the comparison is meaningless for them: this is why the
  Python/CoolProp reference above is the primary one.

**CoolSolve solution check.** `coolsolve -d` reports *System square: Yes*,
SUCCESS in 13 iterations, and *ALL EQUATIONS SATISFIED* (45 checked, 0
violated, max |residual| 3.5·10⁻¹⁰, max relative error 1.1·10⁻¹⁵). The same
45 values are regenerated by `tools/test_models.py CSL-0049`.

## Source and attribution

ULiège, course *Thermodynamique appliquée* (MECA0002, Faculté des Sciences
Appliquées, Département d'Aérospatiale et de Mécanique, Laboratoire de
Thermodynamique), session R5 "exercices sur le chapitre 9 (partie 1) – moteurs
à combustion", exercise 1, 2022‑2023. The EES file is
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R5/R05_E01_2022.EES`
(inventory candidate `TM-0429`, duplicate group `DG-0102`); the session
statement sheet `ThAp22_R05.docx` of the same folder gives the text of the
three exercises of the session. No source file is copied into the library.

The course also ships a Python/CoolProp solution of the same exercise type in
an earlier session (`~/Nextcloud/thermo_models/thermodynamique appliquee/2018-2019/ThAp18_R04_OttoDiesel/`,
compression ratio 9 and 2600 kJ/kg — other data, other closure of γ, so it is
not a reference for this model; only its method was used to write the Python
reference of the *Verification* section).

## Conversion log

- **2026-10-05 — import (card C-52, candidate TM-0429)**: extracted with
  `CoolSolve/tools/ees_extract.py` (EES X10.836, 94 lines, 47 variables, no
  lookup and no parametric table, decimal comma converted by the tool, the
  `{$ID$…}` laboratory licence tag and the `{$PX$…}`/`{$ST$…}` display tags
  removed). Comments translated from French, standard header and section
  titles added, dead code and the GUI hint removed (see below). **Every
  equation of the original is kept**, including the two redundant routes to
  the net work and the `s[i]` post-processing.
- **2026-10-05 — unit conversion by hand** (the file is in
  `SI MASS DEG KPA K KJ`, [ees_import.md §6](https://github.com/CoolProp/CoolSolve/blob/main/docs/ees_import.md)):
  - `q = 800 [kJ/kg]` → `q = 800E3 [J/kg]`, `r = 0.287 [kJ/kg-K]` →
    `287 [J/(kg-K)]` (that `r` is not used by any equation of the original,
    which uses `r_bis = R#/molarmass(fluid$)`; it was kept, annotated);
  - `p[1] = 100 [kPa]` → `100E3 [Pa]`; all other pressures follow from the
    equations, in Pa;
  - `T[1] = 17 [K]+273.15 [K]` → `T[1] = 17 [C]`; the state temperatures are
    now in °C, so the **four ideal-gas-law equations carry `+273.15`**
    (`v[1] = r_bis*(T[1]+273.15)/p[1]` etc.), since the law needs an absolute
    temperature. Temperature differences (`T[j]-T[i]`) are unchanged;
  - the mean temperatures passed to `cp`/`cv` are unchanged, `(T[i]+T[j])/2`:
    a mean of two absolute temperatures in °C is the same value shifted to
    °C, and CoolSolve takes the temperature of a property call in °C;
  - `W_dot_net = W_net*n/2[rev]/(60[s/min])` → `W_net*n/2/60`: the unit
    annotations are dropped (n stays in rev/min), which is needed anyway
    because CoolSolve does not parse a unit annotation in the middle of a
    right-hand side (see *Limitations*); the result is in W;
  - `V_d = 1.6e-3 [m^3]` and `n = 4000 [rev/min]` need no conversion;
  - the `$UnitSystem` line was removed.
- **2026-10-05 — `molarmass(Air_ha)` → `molarmass(fluid$)`**: the original
  computes the specific gas constant of **air** as
  `r_bis = R#/molarmass(Air_ha)`, using the humid-air name for dry air. In the
  library the same quantity is written `R#/molarmass(fluid$)` with
  `fluid$ = 'Air'`, which follows the string variable of the model and gives
  the dry-air molar mass (287.047 J/(kg·K) against 287.043 in the EES stored
  solution, a 1.5·10⁻⁵ difference in the molar mass).
- **2026-10-05 — removed dead code**: the last line of the original (a note
  about the CTRL+Y key displaying the indexed variables in the Arrays window)
  and a standalone comment string ("négatif car fourni par le système") whose
  content is kept in the comments of `W_net` and of the sign convention in the
  header.
- **2026-10-05 — `.initials`**: the EES file has no usable guess values (every
  unknown is stored as 1), so the shipped `.initials` holds converged values
  (from the Python reference of the *Verification* section). Without them the
  model does not pass CoolSolve's final verification of the `entropy()` calls.
- **Level** (taxonomy.md §3): 45 equations (< 50 → 0); largest algebraic block
  3 (≤ 5 → 0); arrays used for the four states (`p[i]`, `T[i]`, `v[i]`,
  `s[i]`), no function or procedure (1); no multi-zone discretisation (0); no
  semi-empirical calibration, off-design or dynamics (0); curated guesses
  needed (1). Score 2 → **level 2**, consistent with the level of the
  inventory row.

## Limitations and CoolSolve gaps

- **No diagram, and no state-point arrays**: the charge is an ideal gas and
  CoolSolve has no ideal-gas diagram (`CS-FEAT-DIAGRAM-IDEAL`); the figure of
  this model is a parametric sweep (roadmap decision D7), see the placeholder
  in *Results*. The four states are nevertheless available as the `p[i]`,
  `T[i]`, `v[i]`, `s[i]` arrays of the model itself.
- **Unit annotations inside a right-hand side** are a parse error
  (`CS-GAP-UNIT-SUBEXPR`): the original's
  `W_dot_net = W_net*n/2[rev]/(60[s/min])` does not parse
  (*"Could not parse line"*, exit code 1). The line is rewritten in the
  unit conversion (§ above), which the registered workaround of that gap also
  prescribes, so the model is **not blocked** and no `_coolsolve` variant is
  needed.
- The entropy reference states differ between EES (ideal-gas `Air` table) and
  CoolProp (`Air`), as for every model computing absolute entropies
  of `Air` (a reference-state offset): only differences are meaningful, and the model's
  `s[i]` are "for information" post-processing anyway.
- CoolSolve prints a warning for every property call on the fluid `'Air'`
  ("*For moist air properties use AirH2O, not 'air'*"). It is a hint, not an
  error: the model wants dry air and its results are unaffected.
- Physical simplifications of the original, kept as they are: air as an ideal
  gas, c_v constant over each transformation, γ at the mean temperature, no
  dissociation, no heat transfer, no friction, no volumetric or mechanical
  loss, no volumetric efficiency (the mass admitted is exactly `V_d/v[1]`), and
  the engine power ignores the pumping work, the combustion pressure loss and
  the finite duration of the real Otto processes.

## Related models

- `CSL-0024` (*Single-cylinder engine with Weibe combustion*): the dynamic,
  crank-angle-resolved counterpart of this air-standard model — the same
  spark-ignition engine physics, but time-resolved and with a Weibe heat
  release instead of an ideal constant-volume heat addition.
- `CSL-0034` (*Full-power operating point of a 4-stroke gas engine*): the same
  engine family with real combustion products (`cpbar`) and cooling water;
  same course family, much richer closure.
- `CSL-0050` (*Land-based two-shaft gas turbine with intercooling,
  regeneration and reheat*): the gas-turbine cycle of the same course, walked
  through with the same station-by-station method (both on air as a perfect
  gas).
- `CSL-0059` *stirling_cycle_ideal_regenerator*: the other air-standard cycle
  of the same repetition (exercise 3), solved with the same method and the same
  temperature-dependent `cv` at a mean temperature, with an ideal regenerator
  and the work of the two isotherms also computed with an EES definite
  integral of `p dv`.
- The exercise session also contains the **Diesel** counterpart
  (`R05_E02_2022.EES`, inventory `TM-0430`/`TM-0433`, cut-off ratio 2,
  1.9 L engine), solved by the same method; it is a different exercise and is
  not in the library.