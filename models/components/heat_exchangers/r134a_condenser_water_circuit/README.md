# R134a condenser rejecting heat into a water circuit (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0173`

An R134a condenser rejects heat into a cooling-water circuit. The refrigerant
flow and the heat to reject are given, the exchanger loses heat to the
ambient, and the refrigerant side has a pressure drop. The model computes the
minimum water mass flow that keeps the water temperature rise at 3 °C, and
the R134a outlet temperature. Teaching exercise, ULiège MECA0002,
thermodynamique appliquée, 2022-2023, repetition R3 exercise 11.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R134a (water is a constant specific heat) |
| **Size** | 25 equations (largest block: 1) |
| **Source** | thermo_models, file `R3_E11_2022_échangeur.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@b3c0d78 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A heat exchanger rejects heat from refrigerant R134a into a water circuit.
The refrigerant mass flow is 0.5 kg/s and the heat to reject is 15 kW. The
source describes the inlet as superheated vapour “de 80 °C” at 350 kPa. The
equation window implements that as the saturation temperature at the inlet
pressure plus 80 °C (stored inlet temperature 85.008 °C), and that equation
is kept. The exchanger loses 1200 W to the ambient. Cooling water enters at
1 bar and 20 °C. The refrigerant pressure drop is 0.1 bar; the water-side
pressure drop is neglected. Find the minimum cooling-water flow so that the
water temperature does not rise by more than 3 °C, and the R134a outlet
temperature.

## Model

Heat rates follow the source sign: negative when the refrigerant loses heat.
The part lost to the ambient is not rejected into the water. R134a properties
are real-fluid calls. Water is closed with a constant specific heat, as in
the source, which assumes no latent exchange between 20 °C and at most 23 °C.

- \(T_\mathrm{in} = T_\mathrm{sat}(p_\mathrm{in}) + 80\)
- \(p_\mathrm{out} = p_\mathrm{in} - \Delta p\)
- \(\dot Q_\mathrm{R134a} = \dot m_\mathrm{R134a}\,(h_\mathrm{out} - h_\mathrm{in})\)
- \(\dot Q_\mathrm{eau} = \dot Q_\mathrm{R134a} - \dot Q_\mathrm{loss}\)
- \(-\dot Q_\mathrm{eau} = \dot m_\mathrm{eau,min}\,c_p\,\Delta T_\mathrm{max}\)

| Input | Value |
|---|---|
| `Q_dot_R134a` | −15000 W (−15 kW in the source) |
| `Q_dot_loss` | −1200 W (−1.2 kW in the source) |
| `p_in_R134a` | 350 kPa (350×10³ Pa) |
| `DELTA_p_R134a` | 10 kPa, written `0.1e2` kPa (0.1 bar) in the source |
| `T_in_eau` | 20 °C |
| `m_dot_R134a` | 0.5 kg/s |
| `DELTAT_max` | 3 °C |
| `cp_eau` | 4184 J/(kg·K) (4.184 kJ/(kg·°C) in the source) |
| `p_eau` | 100 kPa (1 bar in the source) |

`T_in_eau` and `p_eau` are assigned and then unused in the balances, as in
the source. The source says the water pressure, being close to atmospheric,
supports the usual constant specific heat. The system is square without any
value taken from the stored solution (17 equations, 17 variables). The stored
unknowns are guesses in `.initials`.

The eight equations `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 inlet, i = 2
outlet) are post-processing for the CoolSolve diagram. They do not change
the seventeen physical results.

## How to run

```bash
coolsolve ./r134a_condenser_water_circuit.eescode
```

CoolSolve reports 4 iterations with the shipped `.initials` and 4 iterations
without them. Two blocks of size 1 are solved by a one-dimensional Newton
method, two iterations each: `h_out_R134a`, because the first-law equation
does not isolate it, and `m_dot_eau_min`, for the same reason on the water
balance. The other blocks are direct evaluations. No `coolsolve.conf`.

The `.initials` file is the EES stored solution converted to Pa and J.
Enthalpies stay on the EES reference state.

## Results

| Quantity | CoolSolve | EES stored, converted |
|---|---:|---:|
| `m_dot_eau_min` | 1.09943 kg/s | 1.09943 kg/s |
| `T_out_R134a` | 53.1701 °C | 53.1491 °C |
| `T_in_R134a` | 85.0281 °C | 85.0081 °C |
| `T_sat_R134a` | 5.02807 °C | 5.00814 °C |
| `Q_dot_R134a` | −15000 W | −15000 W |
| `Q_dot_loss` | −1200 W | −1200 W |
| `Q_dot_eau_ref` | −13800 W | −13800 W |
| `p_in_R134a` | 350000 Pa | 350000 Pa |
| `p_out_R134a` | 340000 Pa | 340000 Pa |
| `DELTA_p_R134a` | 10000 Pa | 10000 Pa |
| `h_in_R134a` | 475615 J/kg | 327449 J/kg |
| `h_out_R134a` | 445615 J/kg | 297449 J/kg |
| `cp_eau` | 4184 J/(kg·K) | 4184 J/(kg·K) |

`m_dot_eau_min`, the three heat rates and the pressures are printed at the
digits of `compare_solution.py`. The enthalpy drop is −30000 J/kg on both
sides, which is \(\dot Q_\mathrm{R134a}/\dot m_\mathrm{R134a}\). The water
balance closes as \(13800/(4184 \times 3) = 1.099426386\) kg/s.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R3_E11_2022_échangeur.EES` (EES X10.836, 17 stored variables):

> 17 common variables, 4 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8

The four differences, quoted as the tool prints them:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `cp_eau` | 4.184 | 4184 | 9.99e-01 |
| `h_in_R134a` | 327449 | 475615 | 3.12e-01 |
| `h_out_R134a` | 297449 | 445615 | 3.32e-01 |
| `T_sat_R134a` | 5.00814 | 5.02807 | 3.96e-03 |

Maximum relative difference over all common variables: **9.99e-01** (`cp_eau`).

`cp_eau` is not a physical mismatch. EES stored the unit as `KJ/(kg-C)`.
`--ees-units` scales a numerator that contains `kJ`, and the match is
case-sensitive, so `KJ` was left as 4.184. The model value 4184 J/(kg·K) is
4.184 × 1000. The relative difference 9.99e-01 is that factor of 1000.

`h_in_R134a` and `h_out_R134a` are absolute enthalpies. The offset is the
same on both:

| Variable | EES (J/kg) | CoolSolve (J/kg) | CoolSolve − EES |
|---|---:|---:|---:|
| `h_in_R134a` | 327449.0731 | 475615.2913 | 148166.218 |
| `h_out_R134a` | 297449.0731 | 445615.2913 | 148166.218 |

EES sets \(h = 0\) and \(s = 0\) for saturated liquid R134a at −40 °C. The
same state in this CoolSolve binary is \(h = 148144.046\) J/kg and
\(s = 795.610\) J/kg·K. EES stored no entropy, so there is no entropy offset
to compare. The enthalpy offset exceeds 148144.046 J/kg by 22.172 J/kg at
this superheated state. The two states share one offset: the drop is
−30000 J/kg in EES and in CoolSolve.

`T_sat_R134a` is 0.01993 °C higher here (5.02807 °C against 5.00814 °C).
The relative difference is 3.96e-03 because the temperature is only 5 °C.
Saturation pressure at the EES temperature 5.008144556 °C is 349758 Pa
against the imposed 350000 Pa (relative 6.92e-04). The same 0.0199 °C shift
is in `T_in_R134a` (relative 2.34e-04, under rtol). `T_out_R134a` differs by
0.0210 °C (relative 3.96e-04, under rtol).

The other common variables stay under rtol = 0.001 (`--all`):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `m_dot_eau_min` | 1.09943 | 1.09943 | 2.12e-10 |
| `T_out_R134a` | 53.1491 | 53.1701 | 3.96e-04 |
| `T_in_R134a` | 85.0081 | 85.0281 | 2.34e-04 |
| `Q_dot_R134a` | −15000 | −15000 | 0.00e+00 |
| `Q_dot_loss` | −1200 | −1200 | 0.00e+00 |
| `Q_dot_eau_ref` | −13800 | −13800 | 0.00e+00 |
| `p_in_R134a`, `p_out_R134a` | 350000, 340000 | 350000, 340000 | 0.00e+00 |
| `DELTA_p_R134a` | 10000 | 10000 | 0.00e+00 |
| `p_eau` | 100000 | 100000 | 0.00e+00 |
| `m_dot_R134a` | 0.5 | 0.5 | 0.00e+00 |
| `DELTAT_max` | 3 | 3 | 0.00e+00 |
| `T_in_eau` | 20 | 20 | 0.00e+00 |

The eight names only in the CoolSolve solution are the diagram arrays
`P[1]`, `h[1]`, `T[1]`, `s[1]`, `P[2]`, `h[2]`, `T[2]`, `s[2]`. A solve of
the seventeen original equations and a solve of this file give the same
seventeen variables (relative difference 0).

## Source and attribution

The EES file names no person. The inventory names S. Quoilin for the course,
so the author is S. Quoilin. Course: ULiège MECA0002, thermodynamique
appliquée, 2022-2023, repetition R3 exercise 11. The `{$ID$}` tag is the
licence of the Laboratoire de Thermodynamique, University of Liège, not an
author. Assistant names that appear only in companion metadata are not added.
Source file:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R3/R3_E11_2022_échangeur.EES`
(EES X10.836, inventory row TM-0410). The comments in the source are French.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X10.836, unit
  system `SI MASS DEG KPA C KJ`, 17 variables, no tables). The equation window
  is plain text; the extractor rewrote decimal commas and argument semicolons
  (`0,5` → `0.5`). `$UnitSystem` was deleted. No `$Export`, `concat$` or
  `EESFILEDIR$` lines. No Diagram-window input had to be restored: the system
  is square (17 equations, 17 variables). Comments were translated into
  English. Variable names are unchanged. The inlet temperature stays
  `T_sat_R134a + 80`, which is what the stored solution uses (85.008 °C), not
  a fixed 80 °C.
- **2026-10-15 — units**: every converted value, by hand.
  - `Q_dot_R134a`: −15 kW → −15000 W (`-15e3`)
  - `Q_dot_loss`: −1.2 kW → −1200 W (`-1.2e3`)
  - `p_in_R134a`: 350 kPa → 350000 Pa (`350e3`)
  - `DELTA_p_R134a`: `0.1e2` kPa = 10 kPa → 10000 Pa (`10e3`)
  - `p_eau`: `1e2` kPa = 100 kPa → 100000 Pa (`100e3`)
  - `cp_eau`: 4.184 kJ/(kg·°C) → 4184 J/(kg·K) (`4.184e3`)
  - `.initials`: `Q_dot_R134a` −15 → −15000; `Q_dot_loss` −1.2 → −1200;
    `Q_dot_eau_ref` −13.8 → −13800; `p_eau` 100 → 100000; `p_in_R134a` 350 →
    350000; `DELTA_p_R134a` 10 → 10000; `p_out_R134a` 340 → 340000;
    `h_in_R134a` 327.4490731 → 327449.0731; `h_out_R134a` 297.4490731 →
    297449.0731; `cp_eau` 4.184 → 4184. Temperatures, `m_dot_R134a`,
    `m_dot_eau_min` and `DELTAT_max` unchanged.
  - Balances were not rewritten: kW with kJ/kg, and kW with kJ/(kg·°C), scale
    together. Property calls had no extra factor. No hidden gas constant or
    latent-heat coefficient. The only unit-bearing constant is `cp_eau`.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1, 2. `s[1]` is `entropy(R134a, T=T[1], P=P[1])` and `s[2]` is
  `entropy(R134a, h=h[2], P=P[2])`. The seventeen original variables are
  unchanged (relative difference 0).
- **Level**: equations 25 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; converges with and
  without guesses, no `coolsolve.conf` → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The first law has no work term and neglects kinetic and potential energy, as
in the source. The water side uses a constant specific heat rather than
`Water` properties. `T_in_eau` and `p_eau` do not enter the balances. The
refrigerant pressure drop is imposed. No CoolSolve gap blocks the file.

## Related models

None in `related`. CSL-0171 is a different condenser exercise (Cengel 6-54:
heat rejection and the heat-pump COP, no water circuit). The equations are
not the same, so this file is not a variant of that model.
