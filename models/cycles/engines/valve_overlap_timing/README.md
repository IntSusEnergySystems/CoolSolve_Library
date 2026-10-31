# Valve overlap from crank-angle valve timing

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0276`

Teaching exercise (ULiège MCI, TP5, exercise 2): the inlet and exhaust valve
opening/closing crank angles of a four-stroke engine are given at rated
regime and at idle (TDC at 0° of crank angle, counterclockwise rotation, as
in the original). The valve overlap angle is the angle between the exhaust
valve closing and the inlet valve opening, i.e. the period around the
exhaust TDC during which both valves are open; it is also converted to a
duration in seconds through the engine speed.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | none |
| **Size** | 16 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP5/Ex_2_Croisement des soupapes_PNG.EES` (EES X10.393) |
| **Authors** | Philippe Ngendakumana (ULiège Thermotechnics) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (14 common variables, 0 differ) |

## Problem statement

Croisement des soupapes (valve overlap): with TDC at 0° of crank angle and a
counterclockwise rotation direction, the file gives the inlet valve opening
(IVO, before TDC), inlet valve closing (IVC), exhaust valve opening (EVO)
and exhaust valve closing (EVC, after TDC) of an engine at rated regime
(3500 1/min) and at idle (900 1/min). Compute the valve overlap angles and
the corresponding overlap durations.

## Model

For each regime (index 1 = rated, 2 = idle), as in the original:

\[
N = Rpm/60 \;[\mathrm{1/s}], \qquad
VO = EVC - IVO \;[\mathrm{deg\ CA}], \qquad
\Delta t = VO/(360\,N) \;[\mathrm{s}]
\]

The original writes IVC = 57+180 and EVO = −52+180 (rated regime) and
IVC = 18+180, EVO = −21+180 (idle): the arithmetic is kept as in the source.

## How to run

```bash
coolsolve ./valve_overlap_timing.eescode
```

All equations are explicit: no guesses, no `.initials`, no `coolsolve.conf`.

## Results

| Quantity | Rated regime (1) | Idle (2) |
|---|---:|---:|
| Overlap angle VO [deg CA] | 53 | 20 |
| Engine speed N [1/s] | 58.3333 | 15 |
| Overlap duration DELTAt [s] | 2.5238e-03 | 3.7037e-03 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Compared with the EES stored solution of the source file
(`ees_extract.py` decoded 14 variables): `compare_solution.py` reports
**14 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
CoolSolve: 2**. The two CoolSolve-only names are `DELTAt_1` and `DELTAt_2`,
which EES had not stored; they recompute by hand to 53/21000 = 2.5238e-03 s
and 20/5400 = 3.7037e-03 s. The model is pure explicit algebra, so all
common variables agree exactly.

## Source and attribution

Source: `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP5/Ex_2_Croisement
des soupapes_PNG.EES`, ULiège MCI course, TP5 exercise 2. File name suffix
`_PNG` and the EES licence stamp identify Philippe Ngendakumana (ULiège
Thermotechnics) as author; the source inventory also lists R. Dickes
(collector of the MCI file set).

## Conversion log

- **2026-10-31 — import**: extracted with `tools/ees_extract.py` (RTF equations
  converted to text, EES tags `{$ID$…}`, `{$PX$96}`, `{$ST$OFF}` removed, NUL
  byte removed). Unit system of the original `$UnitSystem SI MASS DEG KPA C
  KJ`: the model contains no pressure, energy or temperature quantity (only
  crank angles in degrees, engine speeds and durations), so the kPa→Pa and
  kJ→J conversions change no value; the `$UnitSystem` line is deleted.
  French comments translated to English.
- **2026-10-31 — comment correction**: the original comments label `N_1`,
  `N_2` ("Rpm/60") as "tours/min" while the value is in revolutions per
  second (EES stored units: tours/s); the library comments say [1/s].
  Equations and results unchanged.
- **Level**: 16 equations (0), largest block 1 (0), no functions/arrays (0),
  single trivial system (0), no calibration/off-design (0), no guesses (0)
  → score 0 → level 1.

## Niche

Nearest library models: `CSL-0178` `intake_valve_sizing` (same MCI TP5,
exercise 1 — sizes the intake valve area, bore and mean piston speed, no
crank-angle timing), and the TP5 injection exercises `CSL-0185`
`diesel_injection_sizing` / `CSL-0206` `gasoline_double_injection`
(injection crank angles, but for fuel injection duration and masses). No
library model computed the valve overlap from crank-angle valve timing
before; this one adds the exhaust/intake valve-event bookkeeping around the
TDC and its conversion to a duration.

## Limitations and CoolSolve gaps

None: explicit algebra only; no CoolSolve gap concerns this model.

## Related models

- `CSL-0178` (`intake_valve_sizing`): same source TP5, exercise 1 — intake
  valve area sizing instead of valve timing.
- `CSL-0185` (`diesel_injection_sizing`), `CSL-0206`
  (`gasoline_double_injection`): same course TP5, crank angles converted to
  durations for fuel injection.
