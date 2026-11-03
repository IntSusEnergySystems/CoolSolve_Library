# Air compression: single-stage vs two-stage, isentropic vs polytropic model

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0270`

Compressing air from 70 °C and 2 bar to 10 bar along three paths — single-stage
with a 60 % isentropic efficiency, two stages of 60 % separated by an
intermediate pressure of 5 bar, and a single-stage polytropic model with an
efficiency of 60 % — and comparing the outlet temperatures and the specific
works on the T-s diagram. A bonus equation gives the isentropic efficiency
equivalent to the polytropic path.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air (ideal gas) |
| **Size** | 60 equations, largest block 2 (46 in the original + 14 diagram state points) |
| **Source** | ULiège — course *Thermodynamique appliquée* (THD10), session R05, exercise 2 (EES file `THD10_R05_E2.EES`, 2010) |
| **Authors** | TBD (no author named in the file; the course was maintained by S. Bertagnolio and S. Borguet) |
| **License** | MIT |
| **CoolSolve** | v0.4.0@9768373 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Air enters a compressor at 70 °C and 2 bar and must be compressed to a
discharge pressure of 10 bar. Compare, on a T-s diagram, the following
evolutions (statement of the original exercise, translated):

- a) compression with an isentropic efficiency of 60 %;
- b) two-stage compression (intermediate pressure 5 bar) in which each stage
  has an isentropic efficiency of 60 %;
- c) compression with a polytropic efficiency of 60 %.

## Model

Air is the EES ideal-gas substance `Air`; all states are evaluated with the
property functions `enthalpy`, `entropy`, `temperature`, `cp`, `cv`.

- **a) single stage, isentropic efficiency** — by definition of the isentropic
  efficiency of a work-consuming component,
  $\eta_{is} = (h_{s,is} - h_e)/(h_s - h_e)$, with $h_{s,is}$ from
  $(s_e, p_s)$; $w_{1et} = h_s - h_e$.
- **b) two stages** — stage 1: $\eta_{is,2et} = (h_{int,is} - h_e)/(h_{int} - h_e)$
  with $h_{int,is}$ from $(s_e, p_{int})$; stage 2 takes the exit state of
  stage 1, $(p_{int}, T_{int})$, and $\eta_{is,2et} = (h_{s,is,2et} - h_{int})/(h_{s,2et} - h_{int})$;
  $w_{2et} = h_{s,2et} - h_e$.
- **c) polytropic model** —
  $\eta_p \ln(T_{s,p}/T_e) = \frac{\gamma-1}{\gamma}\ln(p_{s,pol}/p_e)$ with
  $\gamma = c_p/c_v$ evaluated at the mean temperature $(T_e + T_{s,p})/2$
  (the original writes `+273` for the K conversion); $w_p = h_{s,p} - h_e$.
- **bonus** — the isentropic efficiency equivalent to the polytropic path,
  $\eta_{is,2} = \left(\pi_c^{(\gamma-1)/\gamma}-1\right)/\left(\pi_c^{\eta_p^{-1}(\gamma-1)/\gamma}-1\right)$,
  with $\pi_c = p_{s,pol}/p_e$.

As in the original, the second stage of (b) is fed by the discharge of the
first stage: the file contains **no intercooling heat rejection** at the
intermediate pressure (the two stages are simply arranged in series, which
raises the work — see *Results*). The original comment explains that the
polytropic model spreads the irreversibilities along the process, which is why
its final temperature is the highest.

| Inputs | Value | Main outputs | Value (CoolSolve) |
|---|---|---|---|
| `T_e` inlet temperature | 70 °C | `T_s` outlet (a) | 394.2 °C |
| `p_e` / `p_s` inlet / discharge pressure | 0.2 / 1 MPa | `w_1et` work (a) | 335.0 kJ/kg |
| `p_int` intermediate pressure | 0.5 MPa | `T_s_2et` outlet (b) | 416.5 °C |
| `eta_is` / `eta_is_2et` | 0.6 / 0.6 | `w_2et` work (b) | 358.9 kJ/kg |
| `eta_p` polytropic efficiency | 0.6 | `T_s_p` outlet (c) | 448.7 °C |
| | | `w_p` work (c) | 393.5 kJ/kg |
| | | `eta_is2` equivalent isentropic efficiency | 0.5095 |

## How to run

Open `air_compressor_staging_comparison.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./air_compressor_staging_comparison.eescode
```

The `.initials` file (the EES stored solution converted to SI-°C-Pa-J) is
needed: from the default guesses the solver diverges on `h_s`, whose equation
is a ratio of unknown enthalpy differences.

## Results

| Path | Outlet temperature [°C] | Specific work [J/kg] |
|---|---:|---:|
| (a) single stage, $\eta_{is}$ = 0.6 | 394.2 | 334 966 |
| (b) two stages, $\eta_{is}$ = 0.6 each | 416.5 | 358 886 |
| (c) single stage, $\eta_p$ = 0.6 (polytropic) | 448.7 | 393 484 |

Without an intercooling heat rejection, splitting the pressure ratio in two
does not save work: it costs 7.1 % more than the single-stage compression
(358 886 vs 334 966 J/kg), because the second stage compresses gas already
heated by the first. The polytropic path gives the highest outlet temperature
and 17.5 % more work than (a). The equivalent isentropic efficiency of the
polytropic path, $\eta_{is2} = 0.5095$, is indeed lower than the polytropic
efficiency 0.6, as the original comments state.

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` of the three paths (`a`, `b`, `c`)
are the state points for the T-s / h-s diagrams (CoolSolve *Diagram* tab,
*Overlay array path*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the three
     compression paths, figures/air_compressor_staging_comparison_ts.png -->

## Verification

The model was compared with the solution stored in the original EES file
(`compare_solution.py`, 45 common variables, rtol = 0.001, EES values
converted by hand from kPa/kJ to Pa/J with `--ees-units`):

- **temperatures and works** agree within **2.10e-03** (`T_int` = `T_b[2]`,
  239.03 °C in EES vs 238.53 °C in CoolSolve); the works differ by
  6.3e-04 (`w_1et`, below the tool's rtol), 1.28e-03 (`w_2et`) and 1.65e-03
  (`w_p`). These deviations come from the air specific-heat functions of
  EES 8.4 vs the CoolProp ideal gas, not from the import;
- **excluded from that maximum** (reference-state offsets of the ideal gas,
  not errors of the model): the absolute enthalpies (`h_e` … `h_s_p`, offset
  +1.259e5 J/kg at the inlet, EES 343.8 kJ/kg vs CoolSolve 469.8 kJ/kg) and
  the absolute entropies (`s_e` … `s_s_p`, offset −1.815e3 J/kg-K). Enthalpy
  *differences* (the works) and entropy *differences* are unaffected;
- **only in the EES reference**: `cp`, `cv`, `R`, `p[1]`, `p[2]`, `T_s[1]`,
  `T_s[2]`, `s_s[1]`, `s_s[2]` — dead variables left in the file: no equation
  of the equations window uses them (the extracted window is square with 46
  variables without them). Their values belong to the argon exercise
  `THD10_R05_E1` of the same session, which stores the same names (`R` =
  0.20812 kJ/kg-K, the argon gas constant; E1 stores `p[1]` = 100 kPa and
  `p[2]` = 600 kPa, the same as the leftovers here);
- the 15 variables "only in CoolSolve" are the 14 state-point equations added
  for the diagrams (`P_a`/`h_a`/`P_b`/`h_b`/`P_c`/`h_c`), which copy existing
  variables and do not change the results, and the string `fluid$` (the
  extractor decodes numeric variables only).

## Source and attribution

Solution of exercise 2 of session R05 of the ULiège course *Thermodynamique
appliquée* (THD10, 2010), by an author who is not named in the file (the
course was maintained by **Stéphane Bertagnolio** and **Sébastien Borguet**;
the `$ID$` stamp only shows the laboratory student/staff EES licence). Source
file (EES 8.423, comments in French, unit system `SI MASS DEG KPA C KJ`),
collection of S. Quoilin, inventory candidate `TM-0516`:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R05.zip!/THD10_R05_E2.EES`

## Conversion log

- **2026-10-22 — import** (`tools/ees_extract.py`, CoolSolve repository):
  the zip member was extracted to the work folder first (the tool reads plain
  paths); unit system `SI MASS DEG KPA C KJ` converted **by hand** to
  SI-°C-Pa-J: `p_e`, `p_s`, `p_int`, `p_s_pol` × 1000 (200 → 200E3 Pa, 1000 →
  1000E3 Pa, 500 → 500E3 Pa, 1000 → 1000E3 Pa), all other inputs are
  dimensionless and all other quantities are property outputs; the guesses of
  the `.initials` (pressures, specific enthalpies/entropies/works) were
  converted the same way. The `$UnitSystem` directive was removed, the EES
  licence tag dropped by the extractor, comments translated to English and the
  standard header added. No equation was changed; `+273` in the polytropic
  equation is kept as in the original (a 0.15 K rounding of the K offset).
- **2026-10-22 — diagram support**: block of 14 post-processing equations
  (`P_a[i]`, `h_a[i]`, `P_b[i]`, `h_b[i]`, `P_c[i]`, `h_c[i]`, complementing
  the original `T_a`/`s_a`… arrays) added at the end of the model for the
  CoolSolve diagrams; the results of the model are unchanged.
- **Level**: equations 60 → 1 point, largest block ≤ 5 → 0, arrays present → 1,
  no multi-zone/off-design/custom numerics → 0; score 2 → level 2
  (docs/taxonomy.md §3).

## Limitations and CoolSolve gaps

- No CoolSolve gap blocks the file: it solves natively (`System square`,
  60 equations, all satisfied).
- Physics: as in the original, the two-stage path has **no intercooling**
  between the stages (the intermediate state is the discharge of stage 1);
  stage pressure drops, kinetic energies and the drive efficiency are
  neglected; $\gamma$ is evaluated once, at the mean temperature of the
  polytropic path.

## Related models

- `CSL-0010` *two_stage_steam_compressor_intercooling*: the same staging
  question (two stages, intermediate pressure) on steam, with the
  intercooling heat rejection that this file does not contain and with the
  optimal intermediate pressure as the result.
- `CSL-0237` *air_isentropic_compression_cp*: isentropic compression of the
  same air, comparing a constant $c_p$ model with the property functions used
  here.
- `CSL-0285` *argon_piston_compression*: exercise 1 of the same THD10 session
  — closed-system (piston-cylinder) reversible compression of argon along the
  isentropic, isothermal and polytropic paths.
