# Helium balloon buoyancy and acceleration (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0241`

A spherical helium balloon has a diameter of 10 m. The air density is given,
the helium density is one seventh of that density, and the mass is written
as 70×2 kg. The model computes the buoyancy force, the total mass and the
upward acceleration. Teaching exercise Cengel 1-101 from the KU Leuven
`thermo_kuleuven` collection.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | none |
| **Size** | 10 equations (largest block: 1) |
| **Source** | thermo_models, file `01-101.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7d66c3b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The file name and the inventory identify the problem as Cengel 1-101. The
equation window itself has no problem text. It gives a diameter of 10 m, an
air density of 1.16 kg/m³, a helium density equal to one seventh of the air
density, a mass written as `70 * 2` kg and a gravitational acceleration of
9.81 m/s².

The buoyancy force is the weight of the displaced air. The balloon volume is
the volume of a sphere. The total mass is the given mass plus the helium
mass. The last equation is Newton's second law for the acceleration, as
written: the buoyancy force minus the total weight equals the total mass
times the acceleration.

The window does not compute a maximum load. No stored unknown was added.

## Model

One balloon, as written in the equation window. There is no fluid call and
no cycle, so no diagram-state array is added. The figure placeholder is left
empty.

\[
\rho_{\mathrm{he}} = \rho_{\mathrm{air}}/7, \quad
V_{\mathrm{balloon}} = \frac{4}{3}\pi r^{3}, \quad
r = d/2
\]

\[
F_b = \rho_{\mathrm{air}}\, g\, V_{\mathrm{balloon}}, \quad
m_{\mathrm{tot}} = m + \rho_{\mathrm{he}} V_{\mathrm{balloon}}
\]

\[
F_b - m_{\mathrm{tot}} g = m_{\mathrm{tot}} a
\]

| Input | Value |
|---|---|
| `rho_air` | 1.16 kg/m³ |
| `d` | 10 m |
| `m` | `70 * 2` kg |
| `g` | 9.81 m/s² |

Those four assignments are already equations. `g = 9.81` is the equation.
The line `g = g#` is a comment in the window and stays a comment. The
built-in `g#` is not used.

The window writes `pi` in the sphere volume. CoolSolve accepts `pi` as the
built-in constant. The converted window is square (10 equations, 10
variables), so the spelling stays. It was not rewritten as `PI`.

`rho_he = rho_air/7` stays. The model does not call `density(Helium)` or
any other property function. The window gives the density ratio.

The diagram-window RTF is empty. No stored unknown was added.

## How to run

```bash
coolsolve ./helium_balloon_buoyancy.eescode
```

CoolSolve reports 2 iterations with the shipped `.initials` and 2 iterations
without them. There is no `abs()`, so the guesses do not select a root. The
`.initials` file is the EES stored solution with no value rescaled. There is
no `coolsolve.conf` and no runnable variant.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `a` [m/s²] | 16.46509153865 | 16.46509154 | 8.20e-11 |
| `F_b` [N] | 5958.344626798 | 5958.344627 | 3.39e-11 |
| `m_tot` [kg] | 226.7677970991 | 226.7677971 | 3.97e-12 |
| `rho_he` [kg/m³] | 0.1657142857143 | 0.1657142857 | 8.63e-11 |

`a` is 16.46509153865 m/s² in CoolSolve and 16.46509154 m/s² in the stored
solution. `F_b` is 5958.344626798 N against 5958.344627 N. `m_tot` is
226.7677970991 kg against 226.7677971 kg.

The maximum relative difference over the common variables is on `rho_he`,
and it is the rounding of the stored value `1.16/7`. `rho_air`, `d`, `m`,
`g` and `r` match. `V_balloon` prints 3.25e-12.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `01-101.EES` (EES X9.920, 10 variables),
compared with `compare_solution.py` without `--ees-units`. The tool's
summary line is:

`10 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1`

The one name only in CoolSolve is `pi`, the built-in constant in
`V_balloon = 4/3 * pi * r^3`. It is written into the solution. It is not an
extra unknown: the statistics are 10 equations and 10 variables, and the
system is square.

The maximum relative difference over all common variables, as printed by the
tool with every common variable listed, is **8.63e-11** on `rho_he`
(unrounded 8.629e-11). Nothing is above rtol 0.001.

## Source and attribution

The equation window names nobody. The EES licence tag is the J. Lebrun
laboratory licence (University of Liège) and is not the author. The inventory
authors column names S. Quoilin for this KU Leuven course file, so the
authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/01-101.EES`.

Candidate TM-0327. No duplicate group. Teaching exercise, not an exam.
EES X9.920. The only words in the equation window are the comment `or:` and
`g = g#`. The diagram-window RTF is empty.

## Conversion log

- **2026-10-16 — import**: `ees_extract.py` on `01-101.EES` (EES X9.920, plain text, 10 variables, no tables, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, already pascal, Celsius and joule. No number was rescaled: `rho_air = 1.16`, `d = 10`, `m = 70 * 2` and `g = 9.81` stay. `$UnitSystem` was deleted. The file contains no `$TABSTOPS` and no `$Export`. `$Export` is not a missing feature and not a variant. The licence tag was not copied. With `$UnitSystem` removed, the window is square: 10 equations, 10 variables, largest block 1. No diagram input and no stored unknown was turned into an equation. The diagram-window RTF is empty. No diagram-state array was added.
- **g#**: the window has `g = 9.81` and, as a comment, `g = g#`. The comment stays a comment. 9.81 was not replaced by the built-in `g#`.
- **pi**: the window writes `pi` in `V_balloon = 4/3 * pi * r^3`. CoolSolve treats that spelling as the built-in constant. The converted window is square, so `pi` was not rewritten as `PI`.
- **Density**: `rho_he = rho_air/7` stays. There is no call to `density(Helium)` or to any property function.
- **Level**: equations 10 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one balloon, not discretised → 0; no calibration, off-design or dynamics → 0; converges from the default guess (2 iterations without `.initials`, 2 with the stored solution) → 0. Score 0 → level 1. No ±1 shift.

## Limitations and CoolSolve gaps

The densities and `g` are the numbers written in the window. The helium
density is the ratio `rho_air/7`, not a property call. The model computes
the acceleration for the given mass. It does not solve for a maximum load.

No CoolSolve gap is listed. There is no variant.

## Related models

- `CSL-0283` *helium_bottle_lox_displacement*: same substance (helium) in a
  level-1 exercise of this category — buoyancy of a balloon here, an isobaric
  gas-pressurization sizing exercise there.
