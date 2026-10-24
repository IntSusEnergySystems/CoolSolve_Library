# Fuel injection in an atmospheric compression-ignition engine

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0277`

A 5-cylinder naturally aspirated compression-ignition (diesel) engine with a
3.2 L displacement captures a given air mass per cylinder (volumetric
efficiency on the ambient density). The fuel mass injected per cycle follows
from an equivalence ratio of 0.80 with dodecane (C12H26) as a stand-in for
the fuel, whose stoichiometric fuel-air ratio is computed from the molar
masses of C, H, O2 and N2. The injection window (-20° to 5° crank angle at
2400 rpm) gives the injected mass flow, and the injector outlet area and
diameter follow from the incompressible orifice equation at an injection
pressure differential of 1100 bar.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (O2, N2 through `Molarmass`) |
| **Size** | 29 equations, all explicit (largest block: 1) |
| **Source** | ULiège MCI — TP6, exercise 3, after Pulkrabek problems 5-9 and 5-10 (EES file `EX3_PNG_2019.EES`) |
| **Authors** | P. Ngendakumana (ULiège Thermotechnics) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — verified (see *Verification*) |

## Problem statement

A 5-cylinder naturally aspirated CI engine of 3.2 L total displacement runs
at 2400 rpm with a volumetric efficiency of 0.80 on ambient air (1 bar,
25 °C). Injection starts 20° before TDC and ends 5° after TDC. The fuel is
assimilated to dodecane C12H26 (density 850 kg/m³) and the equivalence ratio
is 0.80. The injection pressure differential across the injector is 110 MPa
and the discharge coefficient of the injector is 0.80. Determine the air and
fuel mass captured per cycle, the stoichiometric and actual fuel-air ratios,
the injection duration, the injected mass flow and the injector outlet
diameter.

## Model

- Air mass per cylinder: $m_a = \varepsilon_v\,\rho_a\,V_s$ with
  $\rho_a$ the ambient density and $V_s = V_{tot}/n_c$;
- fuel chemistry: $f_{st} = (m\,M_C + n\,M_H)/((m+n/4)(M_{O2} + 79/21\,M_{N2}))$
  for $\mathrm{C}_m\mathrm{H}_n$, $f = \phi\,f_{st}$, $m_f = f\,m_a$;
- injection timing: $\Theta = \Theta_f - \Theta_d$ crank-angle degrees,
  $\Delta\tau = \Theta/(360\,NT)$ with $NT$ the speed in rev/s;
- injector sizing (incompressible flow through the orifice, as in the
  original): $\dot m_f = C_d\,A\,\sqrt{2\,\rho_f\,\Delta p_f}$,
  $A = \pi\,d^2/4$.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `n_c` / `V_tot` | 5 / 3.2e-3 m³ | `rho_a` air density | 1.1688 kg/m³ |
| `epsilon_v` | 0.8 | `m_a` air mass per cycle | 0.5984 g |
| `p_atm` / `T_amb` | 1e5 Pa / 25 °C | `f_st` / `f` | 0.06702 / 0.05362 |
| `Theta_d` / `Theta_f` | -20 / 5 ° | `m_f` fuel per cycle | 32.09 mg |
| `RPM` | 2400 | `DELTATau` injection duration | 1.736 ms |
| `C_d` | 0.8 | `m_dot_f` injected flow | 0.01848 kg/s |
| `rho_f` / `DELTAp_f` | 850 kg/m³ / 110 MPa | `A` / `diam` | 5.342e-8 m² / 0.261 mm |
| `phi` | 0.8 | | |

## How to run

```bash
coolsolve ./fuel_injection_ci_engine.eescode
```

No special guesses needed (`.initials` from the EES stored solution).

## Results

The injector outlet diameter is 0.261 mm, a typical value for a diesel
injector hole; the air mass per cycle (0.60 g for 0.64 L at ambient
conditions) and the fuel-air ratio (0.0536, i.e. phi 0.8 against a
stoichiometric ratio of 0.067 for C12H26) are physically plausible.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. parametric sweep of the
     injector diameter diam vs the injection pressure differential DELTAp_f,
     figures/fuel_injection_ci_engine_sweep.png -->

## Verification

Compared with the EES stored solution of `EX3_PNG_2019.EES`
(`compare_solution.py --ees-units`; the reference stores T_amb and T_su in K,
converted to °C):

> 21 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
> CoolSolve: 9

At rtol=1e-6 the two differing variables are `rho_a` (3.20e-04) and
`m_dot_f`/`A` (3.08e-04), which inherit the air density difference: EES and
CoolProp use slightly different molar masses for ideal-gas Air. The nine
CoolSolve-only entries (`V_s`, `m_a`, `f`, `f_st`, `conv`, `DELTATau`,
`m_f`, `diam`, plus the constant `pi`) have no stored EES value; their
equations were checked by the solver (all 29 equations satisfied) and the
results are plausible (see *Results*).

## Source and attribution

Exercise solution by **P. Ngendakumana** (ULiège, Thermotechnics; identified
from the EES licence stamp of the file) for the MCI course, TP6 exercise 3.
The problem statement follows Pulkrabek, *Engineering Fundamentals of the
Internal Combustion Engine*, problems 5-9 and 5-10 (fuel injection in an
atmospheric CI engine).

Source file (EES 10.589, stored as RTF, comments in French), collection of
S. Quoilin:
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP6/EX3_PNG_2019.EES`
(inventory candidate `TM-0247`).

## Conversion log

- **2026-10-22 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MASS DEG PA K J` → temperatures converted by hand to °C:
  `T_amb = 25+273.15` (K) becomes `T_amb = 25` (°C); `T_su = T_amb` and the
  `density(Air,T=,P=)` call are unchanged (the physical state is the same).
  The `{$ID$}` licence stamp, `{$PX$}`/`{$ST$OFF}` display tags, the
  `$TABSTOPS` directive and the trailing NUL byte were removed; comments
  translated to English and the standard header added. `m = 12 ; n = 26`
  was split over two lines (one equation per line). Displayed-comment `!`
  prefixes became normal comments. No equation changed otherwise.
- **2026-10-22 — comparison with `CSL-0185`** (`diesel_injection_sizing`,
  MCI TP5 exercise 4, same collection): the two exercises share the
  air-mass/injection-timing skeleton (same n_c = 5, 3.2 L, 2400 rpm,
  -20°→5°, phi = 0.8), but the equations differ: this model computes
  `f_st` from the C12H26 composition (`Molarmass` of C, H, O2, N2) instead
  of taking a given `Afr_st`, and adds the injector sizing block
  (`C_d`, `rho_f`, `DELTAp_f` → `m_dot_f`, `A`, `diam`), while `CSL-0185`
  carries an unused intermittency factor. Imported as a separate model and
  linked, not merged.
- **Level**: 29 equations (< 50 → 0), largest block 1 (≤ 5 → 0), no
  functions/arrays (0), no multi-zone (0), no calibration/off-design (0), no
  curated guesses (0); score 0 → level 1.

## Limitations and CoolSolve gaps

- The fuel is an incompressible liquid of given density; no cavitation or
  compressibility effect in the injector hole (as in the original).
- The volumetric efficiency is a given constant; the model says nothing
  about the combustion itself.
- No CoolSolve gap blocks this model (`Molarmass` of the elements C and H is
  supported since the closure of `CS-GAP-MOLARMASS-ELEMENT`).

## Related models

- `CSL-0185` *diesel_injection_sizing*: same collection, MCI TP5 exercise 4 —
  shared engine/injection skeleton, but no injector sizing and a given
  stoichiometric air-fuel ratio (see *Conversion log*).
- `CSL-0221` *supercharged_engine_air_flow* and `CSL-0223`
  *turbocharged_engine_expander*: the two other exercises of the same MCI
  TP6 session (statements 1 and 2, supercharged air flow and turbocharger).
