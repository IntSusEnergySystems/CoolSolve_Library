# Entropy change of water in an insulated rigid tank (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0243`

A closed rigid tank holds 2 kg of a saturated liquid–vapour mixture of water
at 100 kPa. Three quarters of the mass is liquid. The final state is
saturated vapour at the same specific volume, and the model computes the
entropy change of the water. Teaching exercise Cengel 7-34 from the KU Leuven
`thermo_kuleuven` collection.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water |
| **Size** | 16 equations (largest block: 1) |
| **Source** | thermo_models, file `07-34.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@4ded1eb — verified against the EES stored solution (see *Verification*) |

## Problem statement

The file name and the inventory identify the problem as Cengel 7-34, the
entropy change of water in an insulated rigid tank. The equation window
itself has no problem text.

It gives a mass of 2 kg, a pressure written as `100e3` Pa, a liquid mass
written as `2 * 3/4` kg and a vapour mass written as `2 * 1/4` kg. The
quality is the vapour mass divided by the total mass. The temperature is the
saturation temperature at that pressure. The initial state is fixed by that
quality and pressure. The final quality is 1, and the final specific volume
equals the initial specific volume. The entropy change is the mass times the
change of specific entropy, from the water properties, as written.

## Model

One closed tank, with an initial state and a final state, as written in the
equation window. There is no flow. `v_2 = v_1` keeps the specific volume.
The entropy change, as in the original, is

\[
\Delta S = m(s_2 - s_1)
\]

The fluid token in the file is `water`. CoolSolve accepts it. The hint
"Did you mean Water" did not print, so the token stays `water`. `T_sat`,
`volume`, `intenergy`, `enthalpy` and `entropy` stay as written. The initial
calls use the pair `(x, p)`. The final calls use the pair `(x, v)`. There is
no `quality()` call, and no `P=` argument is added.

`x = m_v/m` and `x_2 = 1` stay. `m = 2`, `m_l = 2 * 3/4` and `m_v = 2 * 1/4`
stay. `m_l` is not used in a later equation. It stays, because it is an
equation of the window. The window uses `p` only. The converted window is
square, so no second spelling was introduced and no stored unknown was added.

Two named states of one tank do not get diagram-state arrays. The figure
placeholder is left empty. The diagram-window RTF is empty.

| Input | Value |
|---|---|
| `m` | 2 kg |
| `p` | `100e3` Pa |
| `m_l` | `2 * 3/4` kg |
| `m_v` | `2 * 1/4` kg |

Those four assignments are already equations. The system is square without
any further assignment (16 equations, 16 variables).

## How to run

```bash
coolsolve ./water_tank_entropy_change.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. There is no `abs()`, so the
guesses do not select a root. The `.initials` file is the EES stored
solution with no value rescaled. There is no `coolsolve.conf` and no
runnable variant.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `DELTAS` [J/K] | 8096.122997 | 8097.535034 | 1.74e-04 |
| `T` [°C] | 99.60592890 | 99.6324495 | 2.66e-04 |
| `s_1` [J/kg-K] | 2816.780817 | 2816.768591 | 4.34e-06 |
| `s_2` [J/kg-K] | 6864.842315 | 6865.536107 | 1.01e-04 |
| `h_1` [J/kg] | 981864.8525 | 981920.3301 | 5.65e-05 |
| `h_2` [J/kg] | 2742199.490 | 2742674.975 | 1.73e-04 |
| `u_1` [J/kg] | 939438.4243 | 939484.1577 | 4.87e-05 |
| `u_2` [J/kg] | 2556234.658 | 2556682.532 | 1.75e-04 |
| `v_1`, `v_2` [m³/kg] | 0.4242642816 | 0.4243617231 | 2.30e-04 |

`m`, `m_l`, `m_v`, `p`, `x` and `x_2` match. The tool prints `DELTAS` as
8096.12 against 8097.54, `T` as 99.6059 against 99.6324, `s_1` as 2816.78
against 2816.77 and `s_2` as 6864.84 against 6865.54.

The solved entropy change equals `m * (s_2 - s_1)`: 8096.122996953 J/K.
The stored entropies give the same check: `2 * (6865.536107 - 2816.768591)`
is 8097.535032 J/K, and the stored `DELTAS` is 8097.535034 J/K.

`h_1` is 55.48 J/kg below the stored value, `h_2` is 475.48 J/kg below,
`u_1` is 45.73 J/kg below and `u_2` is 447.87 J/kg below. Those differences
are the Water property formulation. They sit inside the band of tens to
about 1100 J/kg, and every relative difference is inside rtol 0.001.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `07-34.EES` (EES X9.920, 16 variables),
compared with `compare_solution.py` without `--ees-units`. The tool's
summary line is:

`16 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The default listing prints no difference row. With every common variable
listed, the printed relative differences are `T` 2.66e-04, `v_1` and `v_2`
2.30e-04, `u_2` 1.75e-04, `DELTAS` 1.74e-04, `h_2` 1.73e-04, `s_2` 1.01e-04,
`h_1` 5.65e-05, `u_1` 4.87e-05 and `s_1` 4.34e-06. `m`, `m_l`, `m_v`, `p`,
`x` and `x_2` print 0.00e+00.

The maximum relative difference over all 16 common variables, as printed by
the tool, is 2.66e-04, on `T`.

The equations are the original ones. `DELTAS` is consistent with
`s_2 - s_1` on both the CoolSolve solution and the stored solution. The
enthalpy and internal-energy offsets are property residuals, so the model
stays verified.

`intenergy()` prints: `v=0.424264 m³/kg is unusually large. If this is density in kg/m³, use D=2.3570 instead of V/VOLUME.`
The solved `v_1` is the specific volume from `volume(water, x=x, p=p)`. It
prints 2.30e-04 against the stored 0.4243617231 m³/kg. The final calls keep
`v=v_2`. The solution file labels `v_1` and `v_2` as `kg/m^3`. The value is
the specific volume, and the calls are unchanged.

All 16 equations are satisfied (max residual 0).

## Source and attribution

The equation window names nobody. The EES licence tag is the J. Lebrun
laboratory licence (University of Liège) and is not the author. The inventory
authors column names S. Quoilin for this KU Leuven course file, so the
authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/07-34.EES`.

Candidate TM-0342. No duplicate group. Teaching exercise, not an exam.
EES X9.920. The diagram-window RTF is empty.

## Conversion log

- **2026-10-16 — import**: `ees_extract.py` on `07-34.EES` (EES X9.920, plain text, 16 variables, no tables, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, already pascal, Celsius and joule. No number was rescaled: `p = 100e3` stays, and `m = 2`, `m_l = 2 * 3/4` and `m_v = 2 * 1/4` stay. `$UnitSystem` was deleted. The source equation text and the extraction contain no `$TABSTOPS` and no `$Export`. `$Export` is not a missing feature and not a variant. The licence tag was not copied. With `$UnitSystem` removed, the window is square: 16 equations, 16 variables, largest block 1. No stored unknown was added. No diagram-state array was added. CoolSolve accepts the token `water`. The hint "Did you mean Water" did not print, so the token was not changed to `Water`. `T_sat(water,p=p)` stays. `volume`, `intenergy`, `enthalpy` and `entropy` keep the pairs `(x, p)` and `(x, v)`. No `P=` argument was added. The window uses `p` only. The converted window is square, so no second spelling was introduced. Binary mtime 2026-10-16 00:39:38 +0200, CoolSolve 0.3.0, checkout commit `4ded1eb`.
- **Level**: equations 16 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one tank with two named states, not three coupled components → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with `.initials` and 0 without → 0. Score 0 → level 1. No ±1 shift.

## Limitations and CoolSolve gaps

The window computes the entropy change of the water between the two states
it defines. It does not compute a heat transfer.

Water enthalpy and internal energy differ from the stored solution by 55.48
to 475.48 J/kg. That residual is inside rtol 0.001, and `DELTAS` stays
consistent with `s_2 - s_1`.

`intenergy()` warns that `v = 0.424264` m³/kg looks large. The argument is
the specific volume of the mixture. The call keeps `v`.

No CoolSolve gap. `missing_features` is empty.

## Related models

`related` is empty.
