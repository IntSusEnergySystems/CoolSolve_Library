# Helium bottle pushing liquid oxygen at constant pressure (rocket exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0283`

A teaching exercise of the ULiège thermodynamics course: in a rocket, a helium
bottle pushes liquid oxygen (LOX) towards the engine pump at a constant
pressure of 100 kPa. The model computes the isobaric boundary work done by the
helium while the LOX tank empties, and sizes the helium bottle from the two
helium states (initial fill at 20 °C / 14 MPa, final state at −75 °C / 100 kPa
filling bottle + empty tank).

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Helium (`He`, ideal-gas substance) |
| **Size** | 18 equations, largest block 3 |
| **Source** | ULiège — course MECA0002, exercise R2 E5 (2022-2023), EES file `R2_E5_2022.EES` |
| **Authors** | TBD — the file names nobody; the inventory records the course MECA0002 (companion metadata credits S. Quoilin, repetition assistants N. Paulus, B. Dechesne) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

(translated from the French of the source file) In a rocket, a helium bottle
keeps the liquid oxygen (1142 kg/m³) feeding the engine pump at a constant
pressure of 100 kPa. The initial conditions are given in figure 4.16 of the
textbook (the figure is not part of the file; every datum used is written in
the equation window). After the tank has been emptied, the bottle as well as
the tank are filled with helium at −75 °C and 100 kPa.

- a) Compute the work done by the helium during this process.
- b) Determine the volume the helium bottle must have.

## Model

Data: $\rho_{LOX} = 1142$ kg/m³, $m_{LOX} = 5000$ kg, delivery pressure
$p_{LOX} = 100$ kPa (the data line `p_alim` = 100 kPa is unused, as in the
original), initial helium state $T_{he,i} = 20$ °C, $p_{he,i} = 14$ MPa, final
helium state $T_{he,f} = -75$ °C, $p_{he,f} = 100$ kPa.

- a) The LOX tank volume is $V_{tank} = m_{LOX}/\rho_{LOX}$. The helium pushes
  the LOX at constant pressure towards the pump: the process is isobaric, so
  the boundary work is the (constant) pressure times the volume change of the
  helium, $\Delta V = V_{tank}$ because the tank goes from completely full to
  completely empty: $W = -p_{LOX}\,\Delta V$ (negative: done *by* the system,
  as in the original comment).
- b) At the final state the helium fills bottle + empty tank at −75 °C and
  100 kPa: $V_{total} = V_{ballon} + V_{tank}$, $m_{he} = V_{total}/v_{he,f}$
  with $v_{he,f}$ = `Volume(He,T=T_he_f,P=p_he_f)`. At the initial state all
  the helium is in the bottle: $v_{he,i}$ at 20 °C / 14 MPa,
  $V_{ballon} = m_{he}\,v_{he,i}$.

| Inputs | Value | Outputs | CoolSolve value |
|---|---|---|---|
| `m_LOX` LOX mass | 5000 kg | `W` boundary work | −437.83 kJ |
| `rho_LOX` LOX density | 1142 kg/m³ | `Vol_tank` LOX tank volume | 4.37828 m³ |
| `p_LOX` / `p_alim` supply pressure | 100 kPa (unused) | `m_he` helium mass | 1.07502 kg |
| `p_he_i` / `T_he_i` initial helium | 14 MPa / 20 °C | `Vol_ballon` bottle volume | 0.0498952 m³ |
| `p_he_f` / `T_he_f` final helium | 100 kPa / −75 °C | `Vol_total` final volume | 4.42818 m³ |

## How to run

Open `helium_bottle_lox_displacement.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./helium_bottle_lox_displacement.eescode
```

No `.initials` are needed (18 equations, 18 variables, square, solved in 2
iterations). There are no variants.

## Results

| Quantity | Symbol | CoolSolve | EES stored |
|---|---|---:|---:|
| LOX tank volume | `Vol_tank` | 4.37828 m³ | 4.37828 m³ |
| Volume change of the helium | `DELTAV` | 4.37828 m³ | 4.37828 m³ |
| Boundary work | `W` | −437.83 kJ | not stored (−p·ΔV = −437.83 kJ) |
| He specific volume, final (−75 °C, 100 kPa) | `v_he_f` | 4.11914 m³/kg | 4.115614605 m³/kg |
| He specific volume, initial (20 °C, 14 MPa) | `v_he_i` | 0.0464131 m³/kg | 0.04349130967 m³/kg |
| Helium mass | `m_he` | 1.07502 kg | 1.075184466 kg |
| Final total volume | `Vol_total` | 4.42818 m³ | 4.425044893 m³ |
| Helium bottle volume | `Vol_ballon` | 0.0498952 m³ | 0.04676118058 m³ |

`W = -100e3 Pa × 4.3782837 m³ = -437828 J` (one-liner: 100 × 4.37828 = 437.83
kJ). The EES stored values close the same algebra: with the stored
`v_he_i`/`v_he_f`, `Vol_tank/(1 - v_he_i/v_he_f)` = 4.425044893 = stored
`Vol_total`, and `Vol_total/v_he_f`·`v_he_i` = 0.04676118058 = stored
`Vol_ballon`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot, e.g. helium
     bottle volume Vol_ballon vs initial fill pressure p_he_i, figures/helium_bottle_lox_displacement_sweep.png -->

## Verification

**Reference.** The stored solution of the card's own file `R2_E5_2022.EES`
(TM-0401) covers part (a) only: `Vol_total`, `Vol_ballon` and `m_he` are still
at the default guess 1 (the file was saved before part (b) was solved), and it
has no `W`. The complete stored solution of the **same equations** is the one
of the 2017 version of the exercise, `R2_E1_borguet.EES` (TM-0359; the
equations are identical except that the temperatures are written
`20 [°C]`/`-75 [°C]` instead of `20[K]+273.15`). Part (a) values of TM-0401
were cross-checked and are identical (`DELTAV` 4.378283713, `v_he_f`
4.115614605, `v_he_i` 0.04349130967).

**Comparison 1 — vs TM-0359 stored solution**, `compare_solution.py --ees-units`
(reference converted kPa → Pa, K → °C):

```
17 common variables, 2 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 1
Only in EES reference: P
```

Maximum relative difference **6.30e-02 on `v_he_i`** (EES 0.0434913, CoolSolve
0.0464131); `Vol_ballon` 6.28e-02; then `v_he_f` 8.56e-04, `Vol_total`
7.08e-04, `m_he` 1.49e-04, part (a) (`DELTAV`, `Vol_tank`, `Vol_f`) 4.91e-11,
the data lines 0. Excluded variables: **`W`** exists only in CoolSolve (the EES
stored solution has no `W`); **`P`** (value 1, empty units) exists only in the
EES reference — a stale variable-information record of a variable the equation
window does not define.

Cause of the deviation, the registered gap **`CS-GAP-IDEAL-GAS-MODEL`**: EES
evaluates its ideal-gas `He` as exactly ideal (the stored values give
Z = pv/RT = 0.99988 with the standard molar mass, i.e. EES's gas constant for
He differs by 1.2e-4), while CoolSolve with the input pair (T, P) returns the
CoolProp real-fluid state: Z = 1.067 at 14 MPa (6.3 % higher `v` than the EES
stored value), Z = 1.00074 at 1 bar (8.6e-4 higher `v`). Part (a) and the
ideal-gas algebra are unaffected. The gap
does not block the file (`missing_features` empty); this model is cited as
evidence in that register row.

**Comparison 2 — vs TM-0401 stored solution** (`compare_solution.py --ees-units`):

```
17 common variables, 4 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 1
```

Maximum **9.50e-01 on `Vol_ballon`** (the unsolved EES placeholder 1 against
0.0498952), then `Vol_total` 7.74e-01 and `m_he` 6.98e-02 (same placeholders),
`v_he_i` 6.30e-02 (the ideal-vs-real difference above). Every variable TM-0401
actually solved for part (a) agrees (0 to 4.91e-11).

## Source and attribution

Exercise of the ULiège course **MECA0002** (2022-2023 session R2, exercise
E5), collection of S. Quoilin. The equation window names no author; the
inventory records the course author S. Quoilin and the repetition assistants
N. Paulus and B. Dechesne from the companion file metadata of the collection
(author field `TBD` pending confirmation).

Source file (EES X10.836, comments in French, decimal commas):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R2/R2_E5_2022.EES`
(inventory candidate `TM-0401`, duplicate group `DG-0080`).

## Conversion log

- **2026-10-23 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MASS DEG KPA K KJ` converted by hand (D5): every pressure
  kPa → Pa (100 → `100E3`, 14000 → `14E6`); `T_he_i = 20[K]+273.15 [K]` →
  `20 [°C]` and `T_he_f = -75[K]+273.15 [K]` → `-75 [°C]` (same values,
  293.15 K and 198.15 K); `W = -P_LOX*DELTAV` now carries Pa·m³ = J (was kJ).
  `$UnitSystem` directive and the EES licence/display tags removed, comments
  translated to English, standard header added; `P_LOX` written as `p_LOX`
  (one variable in case-insensitive EES; both spellings occur in the original).
  No (T,H) call (D11), no MODULE/SUBPROGRAM (D10), no tables — nothing else was
  rewritten.
- **2026-10-23 — verification reference**: TM-0401's stored solution is
  incomplete for part (b) (see *Verification*); the stored solution of TM-0359,
  same equations, is used as the complete EES reference.
- **Level**: score of taxonomy.md §3 = 0 (18 equations < 50 → 0; largest block
  3 ≤ 5 → 0; no user functions/procedures/arrays → 0; no multi-zone → 0; no
  semi-empirical/dynamic content → 0; no curated guesses → 0) → level 1.

## Limitations and CoolSolve gaps

- `CS-GAP-IDEAL-GAS-MODEL` (registered, **not blocking**): with (T, P) inputs
  CoolSolve returns the real-fluid helium state where EES gives the ideal gas;
  `v_he_i` and hence `Vol_ballon`/`m_he`/`Vol_total` deviate from the EES
  stored solution by 6.3e-02 / 6.3e-02 / 1.5e-04 / 7.1e-04 (see
  *Verification*). Not in `missing_features` — the native file runs as written.
- `p_alim` is a given that feeds no equation, as in the original.
- Figure 4.16 of the statement is not part of the file; all data used are
  written explicitly in the equation window.

## Niche

Nearest models of the library compared by equations, fluids and topology:

- `CSL-0241` *helium_balloon_buoyancy* — same substance (helium), same level
  and category (level-1 exercise in fundamentals/processes), but a
  buoyancy/Newton's-second-law exercise with given densities and no property
  call, no work, no sizing.
- `CSL-0176` *piston_cylinder_water_constant_pressure* — constant-pressure
  closed-system exercise, but on water (two-phase real fluid) computing
  heating/volume change; no gas-pressurization sizing.
- `CSL-0047` *nonideal_gas_isothermal_work* — gas boundary work at property
  level (non-ideal gas), no system topology.

This model adds the specific rocket **pressurization topology**: a high-pressure
gas bottle displacing a liquid at constant pressure, sizing the bottle volume
from the two gas states — computed with the ideal-gas substance `He` and
verified against an EES stored solution (18 variables). None of the nearest
models computes a pressurant's isobaric displacement work or bottle sizing.

## Related models

- `CSL-0241` *helium_balloon_buoyancy*: same substance and same level-1
  exercise setting, other physics (buoyancy).
- `CSL-0176` *piston_cylinder_water_constant_pressure*: same constant-pressure
  closed-system process, other fluid and other question (heating a two-phase
  water charge).
