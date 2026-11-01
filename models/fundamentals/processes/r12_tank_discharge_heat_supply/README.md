# R12 tank discharge with heat supply (uniform-state open system)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0320`

A rigid 25 L tank holds refrigerant 12 (R12) at 25 °C as a liquid–vapour mixture. A valve is opened and vapour leaves through a nozzle while heat is supplied to keep the tank at 25 °C, until only saturated vapour is left. The model gives the mass that has left the tank and the heat that had to be supplied, from the **first law of the unsteady uniform-state control volume** (tank, valve and nozzle together, kinetic energy at the nozzle exit included). It is a short explicit exercise on the energy balance of a variable-mass open system.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | R12 (real fluid: saturated liquid and vapour at 25 °C, superheated vapour at the nozzle exit) |
| **Size** | 21 equations (largest block: 1, all explicit) |
| **Source** | ULiège course *Thermodynamique appliquée* (THD), exercise 5.72 of the course textbook (EES file `THD10_R03_E5.EES`) |
| **Authors** | TBD (ULiège, THD course exercise sets, folder `THD10_R03`; the file names no author) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — runs; verified against the EES stored solution (see *Verification*) |

## Problem statement

A 25 L tank contains R12, initially 90 % liquid and 10 % vapour by volume at 25 °C. The valve is opened and refrigerant vapour escapes through a nozzle at 100 kPa and −20 °C, with a velocity of 180 m/s. During the process heat is supplied to the tank so that the R12 inside stays at 25 °C. Compute (a) the total mass that has left when the tank holds only saturated vapour, and (b) the heat supplied to the tank during the process. (Statement paraphrased from the French original.)

## Model

- **Initial state**: liquid and vapour masses from their volumes and the saturated specific volumes at 25 °C, $m_{l,i}=V_{l}/v_{l}$, $m_{v,i}=V_{v}/v_{v}$; total mass $m_{tot}$ and initial quality $x_i=m_{v,i}/m_{tot}$.
- **Final state**: the tank is full of saturated vapour at 25 °C, $m_{v,f}=V_t/v_v$; the mass that left is $m_{ej}=m_{tot}-m_{v,f}$.
- **First law** for the control volume tank + valve + nozzle (uniform state in the tank, no work, no inlet, negligible mass in the piping, no kinetic or potential energy inside the tank or at the exit elevation, as stated in the original):

$$Q = m_{v,f}\,u_f - m_{tot}\,u_i + m_{ej}\left(h_{out} + \tfrac{c_{out}^2}{2}\right)$$

with $u_f$ the internal energy of saturated vapour at 25 °C, $u_i$ that of the initial mixture (quality $x_i$, 25 °C) and $h_{out}$ the enthalpy at the nozzle exit (100 kPa, −20 °C: superheated vapour, the saturation pressure at −20 °C being 150.7 kPa).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `Vol_t` tank volume | 25 L | `m_ej` mass that left the tank | 28.670 kg |
| `f_v_l_i`, `f_v_v_i` initial volume fractions | 0.9, 0.1 | **`Q` heat supplied** | **4036.96 kJ** |
| `T_i` tank temperature | 25 °C | `x_i` initial quality | 0.003112 |
| `p_out_n`, `T_out_n` nozzle exit state | 100 kPa, −20 °C | `m_tot`, `m_v_f` initial / final mass | 29.590 kg, 0.9207 kg |
| `c_out_n` nozzle exit velocity | 180 m/s | | |

## How to run

```bash
coolsolve ./r12_tank_discharge_heat_supply.eescode
```

All 21 equations are explicit (21 blocks of size 1): no guess values, no `.initials`, no `coolsolve.conf`.

## Results

| Variable | Value | Unit |
|---|---:|---|
| `v_l_i` specific volume, saturated liquid at 25 °C | 7.6276·10⁻⁴ | m³/kg |
| `v_v_i` specific volume, saturated vapour at 25 °C | 2.7153·10⁻² | m³/kg |
| `m_l_i`, `m_v_i` initial liquid / vapour mass | 29.498, 0.09207 | kg |
| `m_tot` initial total mass | 29.590 | kg |
| `x_i` initial quality | 3.1115·10⁻³ | – |
| `m_v_f` final mass | 0.92070 | kg |
| **`m_ej` mass that left the tank** | **28.670** | kg |
| `h_out_n`, `u_f`, `u_i` (CoolProp reference state) | 344.64, 345.70, 223.94 | kJ/kg |
| **`Q` heat supplied** | **4036.96** | kJ |

97 % of the initial mass leaves the tank (almost all of it liquid that evaporates in the tank before it leaves as vapour, hence the large heat input). The heat splits as 3.46 MJ (`m_ej (h_out - u_i)`, 85.7 %), 112 kJ (`m_v_f (u_f - u_i)`, 2.8 %) and 464 kJ for the kinetic energy of the jet (`m_ej c²/2`, 11.5 %); the three terms add up to `Q`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep of Q vs c_out_n or T_i, figures/r12_tank_discharge_heat_supply_sweep.png -->

## Verification

Compared with the solution stored by EES in the source file (`compare_solution.py … --ees-units`, `rtol=1e-3`): **21 common variables, 8 differ (rtol=0.001); only in EES: 1 (`P`)**. Largest relative differences, as printed:

| Variable | EES (converted) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `h_out_n` [J/kg] | 179978 | 344643 | 4.78e-01 |
| `u_f` [J/kg] | 180222 | 345703 | 4.79e-01 |
| `u_i` [J/kg] | 59570.1 | 223943 | 7.34e-01 |
| `v_v_i` [m³/kg] | 0.0268663 | 0.0271532 | 1.06e-02 |
| `m_v_f`, `m_v_i`, `x_i` | 0.930535, 0.0930535, 0.00314488 | 0.920702, 0.0920702, 0.00311151 | 1.06e-02 |
| `Q` [J] | 4.02723e+06 | 4.03696e+06 | 2.41e-03 |
| `m_ej` [kg] | 28.6583 | 28.6695 | 3.9e-04 (within `rtol`) |

The maximum over all common variables is 7.34·10⁻¹ (`u_i`); excluding the three energy variables `h_out_n`, `u_f`, `u_i` it is 1.06·10⁻² (`v_v_i`). Two explained causes:

1. **Reference state** (`h_out_n`, `u_f`, `u_i`): EES and CoolProp use different zero points for the enthalpy and internal energy of R12 (the CoolSolve value of the saturated-liquid enthalpy at −40 °C is 163 857 J/kg; the EES value is not stored). The offsets of the three variables are 164 665, 165 480 and 164 373 J/kg, i.e. a common shift of about 164.5 kJ/kg plus ±0.8 kJ/kg of equation-of-state differences. The heat `Q` is independent of the reference state, because the masses of the balance satisfy $m_{v,f}-m_{tot}+m_{ej}=0$: adding 10⁵ J/kg to `u_f`, `u_i` and `h_out_n` leaves `Q` unchanged (checked: 4.036958182·10⁶ J before and after).
2. **Saturated vapour density** (`v_v_i`, +1.06 % in CoolProp with respect to EES, as in `CSL-0048`): it changes the vapour masses and the quality (same relative amount), and hence `Q` by 2.4·10⁻³; the saturated-liquid volume agrees to 8·10⁻⁵ (not listed, below `rtol`).

**Transcription check.** Substituting the EES values of `v_l_i`, `v_v_i`, `u_f`, `u_i` and `h_out_n` for the five property calls (scratch run in the work folder, not kept) reproduces the stored EES solution: *21 common variables, 4 differ (rtol=1e-12)*, largest relative difference 2.09·10⁻¹⁰ (`m_ej`), `Q` to 9.4·10⁻¹². The equations are therefore transcribed exactly and the differences above are property-backend differences. 25 °C is 14 K below the critical temperature of R12 (39.4 °C), where a few % is expected between EES and CoolProp (ees_import.md §11).

The EES file stores an extra variable `P = 1`, which no equation uses (the "only in EES" entry); it is not reproduced.

## Source and attribution

Exercise 5.72 of the textbook used in the ULiège course *Thermodynamique appliquée* (THD), solved in EES with the first law of the open system in uniform flow written out term by term in the comments. The file belongs to the `THD10` exercise sets of the course (folder `THD10_R03`, kept in the `2017-2018` folder of the collection); the collection notes name S. Bertagnolio and S. Borguet for these sets, but the file carries no initials and the EES `{$ID$}` tag is the laboratory's student/staff licence: authors TBD, to be confirmed by the maintainer.

Source file (EES X8.423, comments in French, SI MASS DEG KPA C KJ): `~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R03/THD10_R03_E5.EES` (inventory candidate `TM-0369`).

## Niche

Nearest models: `CSL-0048` (two rigid R12 tanks connected by a valve), `CSL-0003` (methane tank evaporation) and `CSL-0230` (rigid vessel, heat removed at constant volume). `CSL-0048` and `CSL-0003` only carry mass and volume balances (no energy equation); `CSL-0230` has an energy balance for a closed system of fixed mass. This model adds the **unsteady uniform-state open-system first law**: a variable-mass control volume with heat supply, an outflow with enthalpy and kinetic energy (`m_ej (h + c²/2)`), initial and final internal energies, on a real fluid crossing the dome (liquid–vapour mixture inside, superheated vapour outside). Same fluid and same initial state as `CSL-0048`, but another balance and another result (heat, not quality).

## Conversion log

- **2026-10-31 — import** (`tools/ees_extract.py`): EES X8.423, 22 variable records (the stored solution), no table, no function other than the property calls `volume`, `intenergy`, `enthalpy`; `{$ID$}` tag removed; the French comments were not copied (the long comment block that explains the first law term by term is summarised in the header and in *Model*); the file uses the European number format (`0,9`, `;` as argument separator), converted by the extractor to the dot convention, which is a display convention of EES and changes no value.
- **Unit system** `SI MASS DEG KPA C KJ` converted **by hand** to `SI MASS DEG PA C J`: `p_out_n = 100E3 [Pa]` (100 kPa in the original); the energies `u_f`, `u_i`, `h_out_n` and `Q` are now in J/kg and J, so the kinetic-energy term of the original, `c_out_n^2/2000` (kJ/kg), becomes `c_out_n^2/2` (J/kg); temperatures (°C), volumes, masses and velocity were already in the target units. Everything else is unchanged.
- **Other changes**: comments translated and shortened; the unit annotation `[°C]` of the original becomes `[C]`; the original's lower-case `p=` argument kept as written. No equation was added or removed; the original order is kept (the property equations `u_f`, `u_i`, `h_out_n` come after `Q`, which EES and CoolSolve do not mind).
- **Level**: 21 equations (< 50, 0), largest block 1 (0), no function or array (0), no multi-zone or discretisation (0), no calibration or dynamics (0; the "dynamic" process is solved as a single initial-final balance), no curated guesses (0) → score 0 → level 1.

## Limitations and CoolSolve gaps

- The model assumes what the statement says: uniform and constant tank temperature (25 °C), negligible mass in the valve and nozzle, no velocity or elevation terms inside the tank, constant nozzle exit state. The intermediate evolution of the process (mass flow, heat rate as functions of time) is not modelled: only the initial and final states are needed.
- The heat and the mass that left scale with the saturated properties of R12 at 25 °C; the ~1 % difference between the EES and CoolProp saturated vapour volumes sets the accuracy of the comparison.
- No CoolSolve gap blocks this model.

## Related models

- `CSL-0048` (*two rigid R12 tanks connected by a valve*): same fluid, same temperature and initial volume fractions; mass and volume balances only, no energy balance.
- `CSL-0003` (*evaporation of liquid methane in a tank*): evaporation in a tank with outflow, mass balance only.
