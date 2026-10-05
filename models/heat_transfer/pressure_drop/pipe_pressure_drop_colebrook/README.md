# Pipe pressure drop with the Colebrook-White friction factor

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0018`

Friction pressure drop of n-pentane flowing in a straight horizontal pipe,
with the Darcy friction factor solved from the implicit Colebrook-White
equation and checked against an explicit approximation. A textbook-level
single-pipe calculation (level 1), useful as a reference for pipe sizing
and for the Colebrook function backlog (roadmap P1.9).

| | |
|---|---|
| **Category** | Heat transfer › Pressure drop |
| **Fluids** | n-Pentane |
| **Size** | 26 equations (largest block: 1) |
| **Source** | ULiège Thermodynamics Laboratory (V. Lemort, 2006), curated as the CoolSolve example `pressuredrop.eescode` |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory), S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs; import verified against EES (see *Verification*) |

## Problem statement

n-Pentane flows at 80 g/s in a straight horizontal pipe of 16 mm inner
diameter and 10 m length (absolute roughness 1.5 µm). Compute the Darcy
friction factor — from the implicit Colebrook-White equation and from an
explicit approximation — the linear pressure gradient, the total friction
pressure drop (in Pa and bar) and the dynamic pressure. Two operating
points are given: superheated vapour at 1 bar (saturation + 10 K, active)
and at 10 bar (saturation + 50 K, in comments).

## Model

- Saturation temperature at the pipe pressure: `T_sat = T_sat(n-pentane, P)`;
  operating temperature `T = T_sat + 10` (1 bar case).
- Friction factor from the implicit Colebrook-White equation, solved
  together with the Reynolds number:
  `1/sqrt(f) = -2·log10(eps/(3.7·D) + 2.51/(Re·sqrt(f)))`;
  `f_vlad` is the explicit approximation of the same relation, as in the
  original.
- `deltaP_lin = f/D·rho·U²/2`, `DELTAP = deltaP_lin·L`,
  `P_dyn = rho·U²/2`, with `U` from the volume flow rate and the pipe
  cross-section, and `Re = D·U/nu`.

| Inputs | Value | Outputs (1 bar case) | Value |
|---|---|---|---|
| `D_i` inner diameter | 0.016 m | `f` Colebrook friction factor | 0.01349 |
| `epsilon` roughness | 1.5 µm | `f_vlad` explicit friction factor | 0.01336 |
| `M_dot` flow rate | 0.08 kg/s | `Re` Reynolds number | 891 900 |
| `L` pipe length | 10 m | `DELTAP` total pressure drop | 2.357 bar |
| `P` / `T` | 1 bar / 45.7 °C | `P_dyn` dynamic pressure | 27 951 Pa |

## How to run

Open `pipe_pressure_drop_colebrook.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./pipe_pressure_drop_colebrook.eescode
```

No `.initials` file is needed (converges from default guesses in
106 iterations). For the 10 bar operating point, swap the two commented
equation blocks under *"n-pentane operating point"* (as in the original):
P = 10 bar, T = T_sat + 50 gives DELTAP = 0.308 bar at U = 17.8 m/s
(sanity-checked only, no EES reference stored for this point).

## Results

1 bar case (superheated n-pentane vapour, T = T_sat + 10 K):

| Quantity | EES | CoolSolve | rel. diff. |
|---|---:|---:|---:|
| `T_sat` [°C] | 35.488 | 35.674 | 0.52 % |
| `Re` [-] | 841 154 | 891 900 | 5.7 % |
| `f` (Colebrook) [-] | 0.013566 | 0.013491 | 0.56 % |
| `f_vlad` (explicit) [-] | 0.013436 | 0.013365 | 0.53 % |
| `deltaP_lin` [Pa/m] | 23 685 | 23 567 | 0.50 % |
| `DELTAP` [Pa] | 236 849 | 235 671 | 0.50 % |
| `DELTAP_vlad` [Pa] | 234 577 | 233 472 | 0.47 % |
| `P_dyn` [Pa] | 27 934 | 27 951 | 0.06 % |

The explicit formula agrees with the implicit Colebrook factor within
1 % in both tools. All 11 remaining variables (pressures, geometry, flow
rate, density, velocity, ratios) agree within 0.1 %.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot,
      e.g. DELTAP vs M_dot from the CoolSolve parametric tab -->

## Verification

**Faithful import vs EES.** The equations were solved unchanged and
compared with the solution stored in the original EES file
(`EES_ok/pressuredrop.EES`, EES 9.920; the ULiège original
`perte de charge VL060830.EES`, EES 7.458, holds byte-identical equations
with stored values within 0.05 % of the EES 9.920 ones):

```bash
python3 ../CoolSolve/tools/compare_solution.py pipe_pressure_drop_colebrook.sol reference/ees_variables.csv
# 25 common variables, 14 differ (rtol=0.001)
```

The deviations come from the fluid-property formulations, not from the
model equations: at 1 bar superheated n-pentane vapour, CoolProp gives a
dynamic viscosity 5.7 % lower than EES (7.14 vs 7.57 µPa·s) and a
saturation temperature 0.19 K higher (35.67 vs 35.49 °C). These propagate
into `Re` (5.7 %) and, damped by the logarithmic friction law, into `f`
(0.56 %) and the engineering results `DELTAP` (≤ 0.50 %). Transport
properties of this vintage differ between EES and CoolProp by a few
percent; the model itself is verified.

## Source and attribution

Original EES model by **Vincent Lemort** (ULiège Thermodynamics
Laboratory), identified from the file name `perte de charge VL060830.EES`
(VL = Vincent Lemort, dated 2006-08-30); the EES licence tag names the
ULiège laboratory licence, not the author. Curated in English as the
CoolSolve example by **S. Quoilin**.

Source files (references only, not copied into the library):
`~/Nextcloud/thermo_models/modeles/perte de charge VL060830.EES`
(inventory candidate `TM-0315`) and
`~/git/CoolSolve/examples/pressuredrop.eescode`
(inventory candidate `CSX-035`; the EES original re-saved as
`CoolSolve/misc/EES_ok.zip:EES_ok/pressuredrop.EES`, EES 9.920, whose
stored solution is the verification reference).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): unit system already
  SI-C-Pa-J (no conversion needed); licence and display tags removed;
  full stored solution present (26 variables, no warnings). The EES
  original, its EES 9.920 re-save and the CoolSolve example hold
  byte-identical equations; only the comments differ (French in the EES
  files, English in the example).
- **2026-10-05 — curation**: standard header added; French comments
  translated to English (same wording as the CoolSolve example);
  `$UnitSystem` line deleted per library convention; equations, variable
  names (including `f_vlad` for the explicit factor and the commented-out
  `{'R123'}` alternative fluid) and both operating-point blocks kept as in
  the original. No `.initials` file: the model converges from default
  guesses. Results unchanged by curation (same `.sol` as the raw
  extraction up to solver tolerance).
- Level scored 0 (26 equations, largest block 1, no user functions,
  arrays or multi-zone structure, no curated guesses) → level 1.

## Limitations and CoolSolve gaps

- No CoolSolve gap blocks this model. Verification deviations (viscosity
  5.7 %, saturation temperature +0.19 K for n-pentane vapour) are
  EES-vs-CoolProp property-formulation differences, documented above.
- The Laborelec pipe models (`TM-0309`, `TM-0312`) call an external EES
  `colebrook` procedure and add fittings lookup tables, insulation and
  heat gain: a different level of detail (level 3 system models), left
  for separate cards including the P1.9 Colebrook function model.
- The 10 bar operating point has no stored EES reference (the original
  file was last solved at 1 bar); its CoolSolve result is sanity-checked
  only.

## Related models

None yet in the library. See the CoolSolve example
`pressuredrop.eescode` (same model, kept in CoolSolve as a test case).
