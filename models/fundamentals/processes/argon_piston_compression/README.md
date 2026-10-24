# Argon compression in a piston-cylinder: adiabatic, isothermal, polytropic

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0285`

A closed-system teaching exercise: 0.2 kg of argon at 100 kPa and 300 K are
compressed reversibly to 600 kPa in a piston-cylinder. The boundary work is
computed for three reversible paths — adiabatic (isentropic), isothermal and
polytropic with n = 1.3 — and each path is closed with a first-law heat
check. The three paths are drawn as T-s points. Argon is treated as an ideal
gas (as in the original).

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Ar |
| **Size** | 39 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (THD10), session R05, exercise 1 (2010), EES file `THD10_R05_E1.EES` (inside `THD10_R05.zip`) |
| **Authors** | TBD (ULiège THD10 course solution; S. Bertagnolio and S. Borguet named for the course in the collection, no author in the file) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A cylinder closed by a piston contains 0.2 kg of argon at 100 kPa and 300 K.
The gas is compressed to 600 kPa in a reversible evolution. Compute the work
required if the evolution is: (a) adiabatic, (b) isothermal, (c) polytropic
with exponent n = 1.3.

## Model

Ideal gas, closed system, reversible paths (mass constant):

- (a) isentropic: $p\,T^{\gamma/(\gamma-1)} = c$, $W_s = m\,c_v\,(T_{f,s} - T_i)$,
  with $c_p$, $c_v$ taken from the argon property functions at the initial
  state and $\gamma = c_p/c_v$;
- (b) isothermal: $p\,v = c$, $W_t = m\,R\,T_i\,\ln(v_i/v_{f,t})$;
- (c) polytropic: $p\,v^n = c$, $W_p = \frac{m}{n-1} R\,(T_{f,p} - T_i)$;
- heat by the first law for each path: $Q = m\,c_v\,\Delta T - W$
  (gives $Q_s = 0$ for the adiabatic path and $Q_t = -W_t$ for the
  isothermal path).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `m` mass of argon | 0.2 kg | `W_s` / `W_t` / `W_p` boundary work | 19 708 / 22 374 / 21 315 J |
| `T_i` initial temperature | 26.85 °C (300 K) | `T_f_s` / `T_f_t` / `T_f_p` final temperature | 342.3 / 26.85 / 180.5 °C |
| `p_i` / `p_f` pressures | 100 / 600 kPa | `Q_s` / `Q_t` / `Q_p` heat | 0 / −22 374 / −11 717 J |
| `n` polytropic exponent | 1.3 | `gamma` | 1.6695 |

The work increases from the isentropic to the polytropic and the isothermal
path, and the heat extracted grows in the same order (comments of the
original): the isothermal compression removes as much heat as the work
supplied, the polytropic path (n = 1.3) organises a partial cooling
representative of a positive-displacement compressor.

The arrays `T_s[i]`/`s_s[i]`, `T_t[i]`/`s_t[i]`, `T_p[i]`/`s_p[i]` (i = 1
initial, 2 final state of each path) hold the T-s points of the three
evolutions (post-processing, no effect on the results).

## How to run

```bash
coolsolve ./argon_piston_compression.eescode
```

No guesses needed (all-explicit system, largest block 1).

## Results

| Path | W [J] (EES) | W [J] (CoolSolve) | Q [J] (EES) | Q [J] (CoolSolve) | T_f [°C] (EES) | T_f [°C] (CoolSolve) |
|---|---:|---:|---:|---:|---:|---:|
| a) adiabatic (isentropic) | 19 625 | 19 708 | 0 | 0 | 341.15 | 342.29 |
| b) isothermal | 22 374 | 22 374 | −22 374 | −22 374 | 26.85 | 26.85 |
| c) polytropic n = 1.3 | 21 315 | 21 315 | −11 723 | −11 717 | 180.47 | 180.47 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the three compression paths,
     figures/argon_piston_compression_ts.png -->

## Verification

EES stored solution of `THD10_R05_E1.EES` (EES 8.423, 42 stored variables),
compared with `tools/compare_solution.py --ees-units` (rtol=0.001): 38
common variables, 13 differ, maximum relative difference 5.56e-03.

- The four display temperatures `T_s[1]`, `T_t[1]`, `T_t[2]`, `T_p[1]`
  (5.56e-03, i.e. 0.15 K) differ because the original converted K to °C with
  −273 and the library uses the exact −273.15.
- Excluding these display values, the maximum is 4.21e-03 on `W_s` (3.32e-03
  on `T_f_s`): the argon `cp` of CoolProp (521.5 J/kg-K) differs from the
  ideal-gas `cp` of EES 8.4 (520.3 J/kg-K), which propagates through
  `gamma` (1.6695 vs 1.6667) into the isentropic path; the isothermal and
  polytropic works depend only on `R` and agree to 6e-09.
- Four variables of the EES file (`w`, `T_1`, `p[1]`, `p[2]`) are stale data
  of an earlier version, not defined by its current equations; they are not
  part of the model.
- Absolute entropies `s_s`, `s_t`, `s_p` (EES ideal-gas third-law reference
  vs CoolProp real-fluid Ar) agree within 1.64e-03 here; they are
  post-processing points only.

## Source and attribution

Exercise solution of the ULiège course *Thermodynamique appliquée* (THD10),
session R05, exercise 1 (2010). The file names no author (EES licence stamp
of the ULiège Thermodynamics Laboratory); the collection names S.
Bertagnolio and S. Borguet for the course → authors left to the maintainer
(`TBD`).

Source file (EES 8.423, comments in French):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R05.zip!/THD10_R05_E1.EES`
(inventory candidate `TM-0515`).

## Conversion log

- **2026-10-23 — import** (`tools/ees_extract.py`): unit system
  `SI MASS DEG KPA C KJ` with decimal commas (converted to dots by the tool)
  → converted by hand to SI-°C-Pa-J: `p_i = 100E3 [Pa]` (100 kPa),
  `p_f = 600E3 [Pa]` (600 kPa), `R_u = 8314 [J/kmol-K]`
  (8.314 kJ/kmol-K). The original stored temperatures in K and passed
  `T-273` to the property calls: the converted model stores temperatures in
  °C (`T_i = 26.85 [°C]`, 300 K in the original) and uses the absolute
  temperature `(T+273.15)` in the ideal-gas law and in the isentropic and
  polytropic p-T relations (pressures and works in Pa and J). Comments
  translated to English, standard header added, the long physical discussion
  of the original moved to this README (§ *Results*). The stale variables
  `w`, `T_1`, `p[1]`, `p[2]` of the EES file are not part of its equations
  and are not imported.
- **2026-10-23 — no correction of the original**: the equations were already
  consistent (Q_s = 0 and Q_t = −W_t are recovered exactly).
- **Level**: equations 39 (< 50) = 0; largest block 1 (≤ 5) = 0; structure 0;
  multi-zone 0; semi-empirical/off-design 0; curated guesses 0 → score 0,
  level 1 (matches the inventory guess).

## Niche

Nearest library models:

- `CSL-0237` *air_isentropic_compression_cp* (fundamentals/processes): also a
  closed-system ideal-gas compression, but only the isentropic path, and its
  point is constant vs variable `cp` (air, Cengel exercise); no isothermal or
  polytropic path, no first-law heat check, no T-s points.
- `CSL-0270` *air_compressor_staging_comparison* (components/compressors):
  same THD10 session, but an open-system steady compressor with isentropic
  and polytropic *efficiencies* and staging — different system and purpose.
- `piston_cylinder_spring_water`, `piston_cylinder_stops_air`:
  piston-cylinder closed systems, but with spring/stops mechanics on
  water/air, not the comparison of reversible ideal paths.

This model adds the three reversible paths (isentropic/isothermal/polytropic)
of a closed system on a monatomic gas (Ar, γ = 5/3), with the first-law heat
of each path and the T-s points — the textbook baseline of compression work.

## Limitations and CoolSolve gaps

- Argon is ideal-gas in EES ('AR') and a real-fluid substance in CoolProp
  ('Ar'): at 1–6 bar, 300–615 K the difference is a few ‰ on `cp` (see
  *Verification*), no CoolSolve gap involved.
- No CoolSolve gap blocks this model.

## Related models

- `CSL-0237` *air_isentropic_compression_cp*: closed-system isentropic
  compression of air, constant vs variable specific heats.
- `CSL-0270` *air_compressor_staging_comparison*: exercise 2 of the same
  THD10 session — single- vs two-stage compression with isentropic/polytropic
  efficiencies (open system).
