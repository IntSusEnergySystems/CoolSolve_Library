# Transient response of a bent-beam electrothermal actuator

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0353`

A Joule-heated bent-beam actuator (V-beam between two anchors) is discretised
into N = 6 nodes along one side of the beam. Each node has a transient energy
balance — conduction from its neighbours, uniform Joule generation from the
applied current, convection to the air — integrated from the initial
temperature over 25 ms. The elongation of the beam by thermal expansion moves
the apex sideways; the resulting displacement is compared with the analytical
fin solution of example 1.7-1 of the same book (shipped with the model as
`T_an[i]`).

| | |
|---|---|
| **Category** | Heat transfer › Conduction, fins and radiation |
| **Fluids** | none (solid conduction, Joule generation, surface convection) |
| **Size** | 63 equations (largest block: 0 — integral model, reduced program) |
| **Source** | Nellis & Klein, *Heat Transfer*, Cambridge University Press, 2009, example 3.8-1 ([EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/example_3.8-1_transient_response_of_a_bent-beam_actuator.ees)) |
| **Authors** | G. F. Nellis and S. A. Klein (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0 — native file blocked by `CS-GAP-INTEGRAL-DUPLICATE`, `CS-GAP-LINE-CONTINUATION`, `CS-GAP-INDEX-VAR`; the runnable variant is verified (see *Verification*) |

## Problem statement

A bent-beam actuator made of silicon (k = 80 W/m-K, rho = 2300 kg/m³,
c = 700 J/kg-K, electrical resistivity 1e-5 ohm-m, CTE 3.5e-6 1/K) has its
anchors 1 mm apart, each half-beam inclined at theta = 0.5 rad; the beam is
10 micron wide and 5 micron thick. A current of 0.010 A heats it by Joule
generation; it convects to air at 20 °C with h_bar = 100 W/m²-K and starts
uniformly at 20 °C. Compute the temperature of six equally spaced nodes along
one half-beam after t_sim = 0.025 s and the displacement of the apex; compare
the profile with the analytical fin solution (uniform generation).

## Model

- Geometry: half-beam length L = L_a/(2·cos(theta)), node positions
  s[i] = L·(i−1)/(N−1), spacing DELTAs = L/(N−1); also the lumped and
  diffusive time constants of the beam.
- Node 1 (pillar) stays at T_a; interior nodes i = 2…N−1 (`DUPLICATE`):
  dTdt[i] = k·(T[i−1]+T[i+1]−2·T[i])/(DELTAs²·rho·c) + rho_e·I²/(w²·th²·rho·c)
  + 2·(w+th)·h_bar·(T_infinity−T[i])/(w·th·rho·c); apex node N: half the
  conduction coefficient (one neighbour).
- Temperatures: T[i] = T_ini + Integral(dTdt[i], time, 0, t_sim), recorded
  every 0.5 ms in `$IntegralTable` (kept as
  `bent_beam_actuator_coolsolve-integral.csv`).
- Displacement: elongation DELTAL = Σ CTE·(T[i]−T_ini)·DELTAs (half-weighted
  apex node), then DELTAy = sqrt((L+DELTAL)²−(L_a/2)²) − sqrt(L²−(L_a/2)²).
- Analytical fin solution of example 1.7-1: constants C_1, C_2 from the two
  boundary conditions, T_an[i] = T_infinity + C_1·exp(m_an·s[i]) +
  C_2·exp(−m_an·s[i]) + gvol·A_c/(h_bar·per).

Temperatures are in °C. The original file stored kelvin; every temperature
here is that value minus 273.15. The energy balances use only temperature
differences, so the rates and the apex displacement are unchanged.

| Inputs | Value | Outputs (final, t = 25 ms) | Value |
|---|---|---|---|
| L_a / w / th | 1 mm / 10 / 5 micron | T[2] … T[6] | 288.4 … 756.1 °C |
| theta | 0.5 rad | DELTAy_micron | 2.023 micron |
| Current | 0.010 A | T_an[6] (analytical steady state) | 756.6 °C |
| T_a = T_ini = T_infinity | 20 °C | tau_lumped / tau_diff | 26.8 ms / 6.5 ms |
| h_bar / k / rho_e / CTE / c / rho | 100 W/m²-K / 80 W/m-K / 1e-5 ohm-m / 3.5e-6 1/K / 700 J/kg-K / 2300 kg/m³ | | |
| N / t_sim | 6 / 0.025 s | | |

The beam heats monotonically towards the analytical steady-state profile
(apex 756.1 °C vs 756.6 °C at 25 ms); the pillar node stays at 20 °C and
the profile is monotonically increasing towards the apex — as in the original.

## How to run

The native file `bent_beam_actuator.eescode` keeps the original EES text
(`Integral` inside a `DUPLICATE` loop, `&` line continuations, array elements
indexed by the variable `N` outside loops); CoolSolve cannot parse it (three
gaps, see *Limitations and CoolSolve gaps*). Run the runnable variant instead:

```bash
coolsolve ./bent_beam_actuator_coolsolve.eescode
```

No `.initials` needed: it converges from the default guesses (SUCCESS, all
equations satisfied). The variant is regression-tested as
`CSL-0353:coolsolve` against its `.sol` baseline; every solve also rewrites
the `-integral.csv` trajectory table.

## Results

| Quantity | Numerical (t = 25 ms) | Analytical (steady) |
|---|---:|---:|
| T[2] / T[4] / T[6] [°C] | 288.4 / 640.3 / 756.1 | 288.6 / 640.8 / 756.6 |
| DELTAy_micron [micron] | 2.023 | — |

Trajectory (every 0.5 ms, `bent_beam_actuator_coolsolve-integral.csv`): all
nodes start at 20 °C, T[1] stays there; the apex reaches 142 °C at 0.5 ms
and 756.1 °C at 25 ms — the thermal time constant of the beam
(tau_lumped = 26.8 ms) sets the approach to the steady state.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of T[i] and T_an[i] vs time
     (Integral tab, from bent_beam_actuator_coolsolve-integral.csv),
     figures/bent_beam_actuator_transient.png + one-line caption -->

## Verification

The verification concerns the **runnable variant** (the native file does not
parse in CoolSolve). Reference: the solution stored in the binary example
`ees-examples-raw/uncategorized/example_3.8-1_transient_response_of_a_bent-beam_actuator.eez`,
extracted with `tools/ees_extract.py` (EES X11.911, 70 decoded records;
warning "stored solution may be STALE" on the loop index `i` only, stored as
inf).

`compare_solution.py bent_beam_actuator_coolsolve.sol reference/ees_variables.csv`:

```
| dTdt[2] | 3.242 | 3.27168 | 9.07e-03 | **DIFF** |
| dTdt[3] | 6.16665 | 6.2231 | 9.07e-03 | **DIFF** |
| dTdt[4] | 8.48767 | 8.56536 | 9.07e-03 | **DIFF** |
| dTdt[5] | 9.97786 | 10.0692 | 9.07e-03 | **DIFF** |
| dTdt[6] | 10.4913 | 10.5874 | 9.07e-03 | **DIFF** |

64 common variables, 5 differ (rtol=0.001); only in EES: 6; only in CoolSolve: 1
```

- All **stored temperatures** agree: max relative difference 2.3e-7 on T[2]
  (integration tolerance of the two tools). The **apex displacement**
  DELTAy_micron agrees to 3.0e-7 (2.022660272 µm in EES, 2.022659663 µm in
  CoolSolve) — the verified criterion of the task card.
- The five **dTdt** rates differ by 9.07e-03 relative, an artefact of
  cancellation, not a model difference: the equation sums the conduction term
  (≈ −2.38e5 K/s) and the Joule term (≈ +2.48e5 K/s) which nearly cancel.
  Recomputing each side's dTdt from its own stored temperatures reproduces
  its stored rate (EES 3.2416 ≈ stored 3.242; CoolSolve 3.2715 ≈ .sol
  3.27168): the 2e-7 difference of the temperatures is amplified by ~4e4.
- Only in EES: the five variables of the dead commented block
  (`C_node`, `R_cond_node`, `R_conv_node`, `R_node`, `tau_node` — stored
  records without equations) and the loop index `i` (inf, suspect).
  Only in CoolSolve: `pi`.

## Source and attribution

Example 3.8-1 of **G. F. Nellis and S. A. Klein**, *Heat Transfer*,
Cambridge University Press, 2009, distributed as an EES example by F-Chart
Software. The plain-text mirror of the file is published under MIT by
[EES-Community/ees-examples](https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/example_3.8-1_transient_response_of_a_bent-beam_actuator.ees)
(commit 5c703d0, file
`uncategorized/example_3.8-1_transient_response_of_a_bent-beam_actuator.ees`,
also the inventory candidate `EEX-019`); the binary `.eez` with the stored
solution is
`ees-examples-raw/uncategorized/example_3.8-1_transient_response_of_a_bent-beam_actuator.eez`
of the same repository (licence tag `{$ID$ … S.A. Klein, F-Chart Software}`:
licence holder, not authorship).

## Conversion log

- **2026-11-15 — import** (`tools/ees_extract.py` on the `.eez`, the inner
  EES X11.911 file): unit system `SI MASS RAD PA K J`. Temperatures are
  stored in °C (each original kelvin value minus 273.15); the balances use
  only differences, so the rates and the displacement are unchanged. Trigonometry
  in the variant is in degrees. The `Convert` calls other than `micron` are
  kept; the three `ConvertTemp(C,K,…)` calls are replaced by 20 °C.
  Comments kept (already English); the `[-]` unit annotation of `N = 6`
  dropped (library rule); display directives `$Tabstops` and `$UnitSystem`
  removed (CoolSolve fixes the unit system; the RAD setting of the original
  is documented in the headers); `{$ID$}`, `{$PX$}`, `{$ST$}` tags removed by
  the extractor. No lookup or parametric tables; no `.initials` needed.
- **2026-11-15 — native file blocked** by three registered CoolSolve gaps
  (each with a minimal reproducer in the gap register): the six
  `T[i] = T_ini + Integral(dTdt[i], …)` equations are inside a `DUPLICATE`
  loop (`CS-GAP-INTEGRAL-DUPLICATE`), two equations are continued with `&`
  (`CS-GAP-LINE-CONTINUATION`), and `dTdt[N]`/`T[N]` index arrays by the
  variable `N` outside loops (`CS-GAP-INDEX-VAR`).
- **2026-11-15 — runnable variant** `bent_beam_actuator_coolsolve.eescode`,
  changes forced by CoolSolve, physics and variable names unchanged (valid
  EES, no CoolSolve-only syntax): the integral loop written out one equation
  per node, `T[1]`…`T[6]` (`CS-GAP-INTEGRAL-DUPLICATE`); the two `&`-continued
  equations joined into single lines (`CS-GAP-LINE-CONTINUATION`); the
  variable index written literally, `dTdt[6]`, `T[6]` (`CS-GAP-INDEX-VAR`;
  N = 6). Unit-system repairs, results unchanged: the trigonometric argument
  scaled to degrees `Cos(theta*180/pi)` (the original ran with RAD);
  `Convert(micron,·)` hand-converted (`w = 1e-05`, `th = 5e-06`,
  `DELTAy_micron = DELTAy*1e6`) because `micron` is not a unit CoolSolve
  knows (an omission of its unit table, not registered: no card for it);
  `current`/`Deltas` unified to `Current`/`DELTAs` (EES names are
  case-insensitive, CoolSolve keeps one name). The `$IntegralTable` column
  range `T[1..N]` written as `T[1..6]` with the same literal index. Solved
  with CoolSolve 0.4.0: SUCCESS.
- **Level**: 63 equations → 1; largest algebraic block 0 (integral model,
  reduced program) → 0; `DUPLICATE`/arrays → 1; 6-node discretisation → 1;
  dynamics → 1; curated guesses: no → 0. Score 4 → **level 3**.

## Limitations and CoolSolve gaps

- `CS-GAP-INTEGRAL-DUPLICATE`: `INTEGRAL` calls inside a `DUPLICATE` loop are
  rejected; the native file keeps the loop, the variant writes the six
  equations one by one.
- `CS-GAP-LINE-CONTINUATION`: equations continued with `&` do not parse
  (native file has two); the variant joins them.
- `CS-GAP-INDEX-VAR`: an array element indexed by a main-program variable set
  to a constant (`T[N]`, `dTdt[N]`) becomes an extra unknown; the variant
  writes the literal index 6.
- `Convert(micron, …)` is a parse error in CoolSolve ("unknown unit
  'micron'", valid EES unit name): hand-converted in the variant. Not
  registered (no card for it, decision of task C-519).
- Steady properties, 1-D fin discretisation, constant h_bar and radiation
  neglected — as in the original.

## Related models

None: the category holds a resistance/shape-factor library (`CSL-0106`
*conduction_resistances_and_shapes*), a 2-D steady plate (`CSL-0341`
*conduction_2d_square_plate*), a transient plane wall (`CSL-0340`
*transient_conduction_plane_wall*) and the 50-node steady fuel sphere
(`CSL-0348` *fuel_element_sphere*, imported from the same book with the same
line-continuation and index gaps). None models an electrothermal actuator.
