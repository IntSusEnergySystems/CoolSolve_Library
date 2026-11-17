# Coated temperature sensor in an oscillating ambient

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0358`

A small spherical sensor coated with a thin layer of lower conductivity sits in
an ambient whose temperature oscillates as a sine around a mean (a reactor
environment). The sensor is lumped (its Biot number is 0.0018 &lt;&lt; 1) and the
coating is represented by a conduction resistance in series with the convection
resistance; the analytical response of the resulting first-order system gives
the sensor temperature at a given time, started from an initial temperature.
The model computes the coating/convective resistances, the sensor capacitance
and time constant, and the sensor and ambient temperatures at `t`.

| | |
|---|---|
| **Category** | Heat transfer › Conduction, fins and radiation |
| **Fluids** | none (solid sensor) |
| **Size** | 24 equations, all explicit (largest block: 1) |
| **Source** | Nellis & Klein, *Heat Transfer*, Cambridge University Press, 2009, example 3.1-2 (EES example of F-Chart Software) |
| **Authors** | G.F. Nellis and S.A. Klein (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0 — runs; verified against the EES stored solution (see *Verification*) |

## Problem statement

A temperature sensor (sphere, D = 1 mm, k_s = 50 W/m-K, c_s = 150 J/kg-K,
rho_s = 16 000 kg/m³) is coated with a layer 100 micron thick of conductivity
k_c = 0.2 W/m-K and exposed to convection (h_bar = 500 W/m²-K) in an ambient
whose temperature oscillates as T_infinity = T_infinity_bar + DT_infinity sin(2 pi f t)
with a mean of 320 °C, an amplitude of 50 K and f = 0.5 Hz. The sensor starts
at 260 °C. What is the sensor temperature at t = 10 s?

## Model

Resistances (as in the original): convection on the outer coating surface
`R_conv = 1/(h_bar 4 pi (D/2+th_c)^2)`, conduction through the spherical coating
`R_cond_c = (1/(D/2) − 1/(D/2+th_c))/(4 pi k_c)`, internal conduction of the
sensor `R_cond_int = L_c/(k_s A_s)` with `L_c = V/A_s`. The Biot number
`Bi = R_cond_int/(R_conv + R_cond_c)` = 0.0018 justifies the lumped treatment.
Sensor capacitance `C = V rho_s c_s` and time constant `tau = (R_conv + R_cond_c) C`
= 0.722 s. The analytical response (solution from Maple, as in the original) is

$$Temp = e^{-t/\tau} C_1 + \frac{T_{\infty,bar} + 4 T_{\infty,bar} f^2 \pi^2 \tau^2 - 2 DT_\infty \cos(2\pi f t) f \pi \tau + DT_\infty \sin(2\pi f t)}{1 + 4 f^2 \pi^2 \tau^2}$$

with the integration constant `C_1` fixed by the initial condition
`Temp(0) = T_ini`. The response is linear: the same formula holds in °C, which
is why the K → °C conversion of the original leaves the equations unchanged.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_infinity_bar` mean ambient | 320 °C | `Temp` sensor temperature at `t` | 323.138 °C |
| `T_ini` initial temperature | 260 °C | `T_infinity` ambient at `t` | 345.201 °C |
| `DT_infinity` amplitude | 50 K | `tau` time constant | 0.7222 s |
| `f` frequency | 3.141592654 rad/s (0.5 Hz) | `Bi` Biot number | 0.001846 |
| `t` evaluation time | 10 s | `C_1` integration constant | −56.51 °C |
| `D`, `th_c` geometry | 1 mm, 100 micron | `R_conv`, `R_cond_c`, `R_cond_int` | 442.10, 132.63, 1.061 K/W |

## How to run

```bash
coolsolve ./coated_sensor_oscillating.eescode
```

All equations are explicit; no guesses needed. Change `t` to evaluate the
response at another time.

## Niche

The only library models of a transient temperature response in this category
are `CSL-0349` (1-D transient fin, discretised, `INTEGRAL`) and `CSL-0353`
(bent-beam actuator, blocked native file, six-node `INTEGRAL`). This model is
the closed-form counterpart: a lumped sensor with a coating resistance in a
sinusoidally varying ambient, no integration needed. The sinusoidal-sensor
chapter of the same book also contains the discretised mounting-rod sensor
with self-heating (inventory row `EEX-383`, not yet imported).

## Results

At `t` = 10 s: the ambient is at 345.2 °C (25.2 °C above the mean, i.e.
sin(2 pi f t) = 0.504), the sensor follows at 323.138 °C, lagging and
attenuated by its 0.722 s time constant (tau * f * 2 pi = 2.27). The initial
transient has decayed (exp(−t/tau) = 9.7e-7), so the sensor is in the periodic
regime.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): sensor and ambient temperature vs time (Parametric sweep over t or Integral),
     figures/coated_sensor_oscillating_time.png -->

## Verification

Compared with the **stored solution of the original EES file** (single solve at
t = 10 s, `.eez` raw file, `ees_variables.csv` with `--ees-units`):

```
Converted EES reference values: T_infinity_bar (K->C), Temp (K->C), T_ini (K->C), T_infinity (K->C)

| Variable | EES | CoolSolve | rel. diff | |
|---|---:|---:|---:|---|

24 common variables, 0 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 1
Only in EES reference: T_C, T_infinity_C
```

At a tolerance of 1e-12 the largest relative difference is **3.35e-09** (on
`T_infinity`). `T_C`/`T_infinity_C` exist only in the reference because the °C
aliases were dropped in the conversion (they equal `Temp`/`T_infinity`: EES
stores 323.1377038 and 345.2010963 °C); the extra CoolSolve entry is the
built-in `pi`. The time of the stored solution (t = 10 s) is the evaluation
time of the model, so no closed-form hand check was needed.

## Source and attribution

Example 3.1-2 of **G.F. Nellis and S.A. Klein**, *Heat Transfer*, Cambridge
University Press, 2009 (chapter 3), as an EES example of F-Chart Software
(MIT example set). The raw binary file is published at
`https://fchartsoftware.com/ees/examples/examples_heat_transfer_2009/chapter%203/example%203.1-2%20temperature%20sensor.eez`
(EES X11.911; a plain-text MIT mirror is in the EES-Community/ees-examples
collection, inventory row `EEX-017`).

## Conversion log

- **2026-11-15 — import** (`tools/ees_extract.py` on the binary `.EES` of the
  `.eez`): unit system `SI MASS RAD PA K J` → converted by hand to SI-°C-Pa-J.
  - `T_infinity_bar` 593.15 K → `320 [°C]`, `T_ini` 533.15 K → `260 [°C]`;
    `DT_infinity` stays 50 K (temperature difference).
  - `f`: the stored value 3.141592654 rad/s is used (0.5 Hz converted by EES's
    `Convert(Hz,rad/s)`); `D` 1 mm → `0.001 [m]`; `th_c` 100 micron →
    `100e-6 [m]`. No `Convert`/`ConvertTemp` call is kept.
  - RAD → degrees: each trigonometric argument of the stored solution is
    multiplied by `180/pi` (`Cos`/`Sin(2 pi f t*180/pi)`).
  - Temperatures in K → °C: the response is linear, the formula is unchanged;
    the °C aliases `T_C`/`T_infinity_C` (`ConvertTemp(K,C,…)`) were dropped —
    they equal `Temp`/`T_infinity`. `C_1` is unchanged by the shift (it is a
    difference of temperatures); its stored value is reproduced exactly.
  - The `$if ParametricTable='Table 1'` guard and `$endif` were dropped and the
    solution kept: the block is the only solution of the file (no parametric
    table is stored; the table conditions are false in a CoolSolve solve), and
    EES's stored solution was computed with it active, at **t = 10 s** (the
    stored time; used as input, not guessed).
  - The equation continued with `&` was joined into one line
    (`CS-GAP-LINE-CONTINUATION`); no change of the equation itself.
  - The `$if ParametricTable='Attenuation'` block (`phi`, `Att`, undefined
    `ftau`) was dropped as in the task card: it belongs to another run of the
    example (period/frequency product of a different quantity) and is not part
    of the stored solution.
- **Level**: 24 equations (< 50 → 0), largest block 1 (≤ 5 → 0), no
  functions/arrays (0), not discretised (0), dynamics as closed form (1), no
  curated guesses (0) → score 1 → **level 1** (the inventory guessed level 2 /
  dynamic: the physics is transient but the model is an explicit evaluation at
  a given time, hence kind `steady`).

## Limitations and CoolSolve gaps

- The lumped-sensor assumption holds only for `Bi << 1` (here 0.0018); the
  coating conduction resistance is exact for a spherical shell.
- No CoolSolve gap blocks this model (`missing_features` is empty).

## Related models

None (`related` is empty; the transient-response neighbours are named in the
*Niche* section above).
