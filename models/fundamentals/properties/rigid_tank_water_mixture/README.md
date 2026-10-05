# Rigid tank with a liquid-vapour water mixture

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0044`

A classic introductory exercise on saturation properties: a rigid vessel
contains water as a liquid-vapour equilibrium mixture at a given pressure.
The quality follows from the average specific volume, and from it the masses
and volumes of the two phases.

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | Water |
| **Size** | 12 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition 1, exercise 1 (EES file `R1_E1_2022.EES`) |
| **Authors** | TBD (ULiège course MECA0002 repetition team) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A rigid vessel of 1 m³ contains 4 kg of water as a liquid-vapour mixture in
equilibrium at a pressure of 6 bar. Determine:

a. the masses of liquid and vapour;
b. the volumes occupied by the liquid and by the vapour.

## Model

The tank volume and mass are shared between the two phases:

$$V = V_v + V_l, \qquad m = m_v + m_l$$

The link between mass and volume is the specific volume, read from the
saturation tables of Water: the average specific volume $v = V/m$ gives the
quality $x$, hence $m_v = x\,m$; the liquid volume is $V_l = v_l\,m_l$ with
$v_l$ and $v_v$ the saturated-liquid and saturated-vapour specific volumes at
$p$. The saturation temperature is reported for information.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `Vol` tank volume | 1 m³ | `x` quality | 0.7915 |
| `m` mass of water | 4 kg | `m_v` / `m_l` vapour / liquid mass | 3.166 / 0.834 kg |
| `p` pressure | 600 kPa | `Vol_v` / `Vol_l` vapour / liquid volume | 0.9991 / 0.000918 m³ |
| | | `v_v` / `v_l` sat. vapour / liquid sp. volume | 0.3156 / 0.001101 m³/kg |
| | | `T` saturation temperature | 158.83 °C |

## How to run

Open `rigid_tank_water_mixture.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./rigid_tank_water_mixture.eescode
```

No guess values needed (all equations explicit).

## Results

Water at 600 kPa: `T` = 158.83 °C, `v_avg` = 0.25 m³/kg, quality `x` = 0.7915:
3.166 kg of vapour occupying 0.9991 m³ (99.9 % of the tank) and 0.834 kg of
liquid at the bottom (0.918 l).

CoolSolve emits a *QUALITY()* warning ("v=0.25 m³/kg is unusually large. If
this is density in kg/m³, use D=4.0000"): it misreads the average specific
volume of a large-vessel mixture for a mistaken density input. The value is
correct (V/m) and the result matches EES.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. quality or phase volumes vs pressure,
     figures/rigid_tank_water_mixture_*.png -->

## Verification

1. **EES stored solution.** The converted model was solved with CoolSolve and
   compared with the solution stored in the original EES file
   (`compare_solution.py rigid_tank_water_mixture.sol reference/ees_variables.csv
   --ees-units`, conversion of the kPa/K reference by the tool):

   > 12 common variables, 0 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 0

   The EES file additionally stores a variable `V` = 1 (no units): a stale
   record of the tank volume under an older name, not part of the equations;
   it was ignored.
2. **Companion CoolProp solution.** The course provides a Python/CoolProp
   solution of the same exercise (`Python/ThAp21_R01E01.py` next to the EES
   file, referenced, not copied). Its printed results, computed from the
   verified model output, are: m_l = 0.8 kg, m_v = 3.2 kg (1 decimal), V_l =
   0.92 l, V_v = 999.08 l, T = 158.83 °C — consistent with the table above
   (the script was not run; CoolProp is not installed in this environment).

## Source and attribution

Exercise solution of the course *Thermodynamique appliquée* (MECA0002),
Université de Liège, repetition session 1 (2022-2023). The EES file itself
names no author (only the laboratory licence tag); the inventory attributes
the course material to S. Quoilin with repetition assistants N. Paulus and
B. Dechesne (from companion Python/Word metadata), to be confirmed by the
maintainer.

Source file (EES 10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R1/R1_E1_2022.EES`
(inventory candidate `TM-0378`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MASS DEG KPA K KJ` with decimal commas (converted by the
  tool); converted by hand to SI-°C-Pa-J (ees_import.md §6): `p = 600E3 [Pa]`
  ("600 kPa in the original"); `T` now returns °C (EES returned K, 431.98 K →
  158.83 °C). No energy terms, no absolute-temperature relations, no other
  unit-dependent constant in the model. Comments translated to English,
  standard header added, no equation changed otherwise.
- **Duplicate group DG-0088** (4 files, triaged per workflow §2):
  - `TM-0383` (`save/R1_E1_2022.EES`, `duplicate`): stripped-equation diff
    identical to TM-0378 (backup copy).
  - `TM-0540` (`R1-solutions.zip!/R1_E1_2022.EES`, `duplicate`): same
    equations with the variables renamed (`v_avg`→`v_tp`, `x`→`x_tp`).
  - `TM-0506` (`THD10_R01.zip!/THD10_R01/SBorguet/R1_E1_borguet.EES`, 2017
    version by S. Borguet, `merged`): same exercise and values, solved
    differently (`Vol_v = v_v*m_v` kept, quality from `x = m_v/m`), plus an
    extra question *c*: "down to which pressure should the tank be expanded
    so that all the water is vapour?" — i.e. the pressure at which the
    saturated-vapour specific volume equals 0.25 m³/kg. Computed with the
    same property backend for the record: **p = 767.5 kPa** (saturation
    temperature 168.7 °C). Not part of the model file.
- **Level**: 12 equations (0) + largest block 1 (0) + no functions/arrays (0)
  + no multi-zone (0) + no calibration/dynamics (0) + no curated guesses (0)
  = 0 → level 1.

## Limitations and CoolSolve gaps

- None. The spurious `QUALITY()` warning on `v=0.25` is informational only
  (see *Results*); the result is correct and matches EES.

## Related models

- `CSL-0003` *methane_tank_evaporation*: sibling exercise of the same
  repetition session (R1, exercise 3): liquid methane evaporating in a tank.
- `CSL-0047` *nonideal_gas_isothermal_work*: sibling introductory exercise of
  the same course (repetition 2, exercise 3): isothermal expansion of a gas
  described by its own equation of state, boundary work with an EES integral.
- `CSL-0048` *two_tanks_connected_valve_r12*: sibling exercise of the same
  repetition session (R1, exercise 4): two rigid tanks connected by a valve,
  change of the quality of R12.
- `CSL-0057` *two_tanks_max_work_air*: the two-rigid-vessel problem of the
  same course, solved as a reversible maximum-work (exergy) balance on ideal-gas
  air.
