# Scania DI09/DI16 marine diesel engines - data-handbook analysis

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0274`

Worked example from the ULiège course *Moteurs à combustion interne* (MCI,
Prof. Ph. Ngendakumana): instructor solution ("NGEN unit") of a diesel-engine
problem built on the 2013 Scania marine data handbook. One of four engines of
the handbook (DI09 070M 162 kW, DI09 072M 294 kW, DI16 073M 478 kW, DI16
079M 552 kW) is selected with a string variable; the model checks the
coherence of the handbook data (swept volume, compression ratio, mean piston
speed, torque, exhaust flow), computes the brake mean effective pressure, the
fuel flow and thermal efficiency from the specific consumption, the excess
air of the C12H26 combustion, the global thermal balance, the volumetric
efficiency at two reference states, the compressor pressure ratio and
isentropic efficiency across the intake filter, derates the engine to Lake
Victoria (1133 m, 30 °C, ISO 3046/1 reference D) and estimates the CO2
emissions per km at a ship speed of 25 knots. Published as an example.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas) |
| **Size** | 88 equations (largest block: 1, fully explicit) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/Examen/RESOLUTION_NGEN.EES` (TM-0224) |
| **Authors** | Ph. Ngendakumana, Rémi Dickes (ULiège) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (see verification field) |

## Problem statement (paraphrased)

From the 2013 Scania DI09/DI16 marine data handbook (general data and the
data sheets of four engines), for a selected engine: verify the coherence of
the handbook values (swept volume from bore/stroke/cylinders, mean piston
speed, torque/shaft power, exhaust flow); compute the clearance volume, the
brake mean effective pressure, the fuel mass flow from the specific
consumption, the thermal efficiency, the excess air (fuel assimilated to
C12H26), the residue of the global thermal balance (handbook heat flows:
engine cooling, charge-air cooler, exhaust, radiation), the volumetric
efficiency referred to the cylinder inlet and to standard atmosphere
(ISO 3046/1), and the isentropic efficiency of the turbocharger compressor
(intake filter pressure drop of 30 mbar, air 30 °C at inlet, handbook
temperatures across the charge-air cooler). The engine is then installed in
a boat on Lake Victoria (altitude 1133 m, ambient 30 °C): derate the shaft
power with the ISO 3046/1 reference-D law (m = 0.7, n = 1.2, mechanical
efficiency 0.85) and estimate the CO2 emissions in g/km at 25 knots.

## Model

- The four handbook data sets are held in `$IF MOTEUR$ = '1'..'4'`
  conditional-compilation branches; `MOTEUR$ = '3'` (DI16 073M, 478 kW) is
  the default run, the one stored in the EES file. Only the selected branch
  is compiled.
- All quantities follow from explicit design equations and balances; air is
  the ideal-gas `AIR` of EES/CoolProp. The excess air comes from the
  stoichiometric fuel-air ratio of C12H26, with `molarmass(C)`,
  `molarmass(H)`, `molarmass(O2)`, `molarmass(N2)` as in the original.
- The compressor isentropic efficiency uses absolute `Air` enthalpies and
  entropies of the property backend, **differences only** (`w_cp`, `w_s_cp`),
  so the backend reference state cancels.
- The derating law is the ISO 3046/1-type correction of CSL-0151:
  `K = (p_atm_x/p_atm_ref)^m·(T_a_ref/T_a_x)^n` with a site atmospheric
  pressure fitted as a quadratic in the altitude, and
  `alpha = K − 0.7·(1−K)·(1/eta_m − 1)`.
- Variable names are kept as in the original file, including the names
  containing `|` (`V|o_s`, `C|o_m`, `M|o_p`, `Tau|o`, `L|star`, `N|star`)
  and the accented `Rés`; they parse as such in CoolSolve.

## How to run

```bash
coolsolve ./scania_marine_diesel_handbook.eescode
```

No guess values needed (fully explicit system, largest block 1). To analyse
another engine of the handbook, set `MOTEUR$` to `'1'`, `'2'` or `'4'`.

## Results (default run: DI16 073M - 478 kW)

| Quantity | Model | Handbook / check |
|---|---:|---:|
| Swept volume `V_s` | 0.016353 m³ | 16.4e-3 m³ (handbook, −0.3 % apart) |
| Clearance fraction `RapVc` | 5.75 % | 1/17.4 |
| Mean piston speed `C_m` | 7.70 m/s | 7.7 m/s |
| Brake mean effective pressure | 19.23 bar | plausible for a marine diesel |
| Shaft power from torque | 393.0 kW | 393 kW |
| Torque `tau` | 2501.9 Nm | 2502 Nm |
| Fuel flow `M_dot_f` | 0.02282 kg/s | 209 g/kWh |
| Thermal efficiency `eta` | 40.3 % | plausible |
| Excess air `e` | 0.518 | plausible for a supercharged diesel |
| Balance residue `Tol` | 1.52 % | handbook data rounding |
| Exhaust flow `M_dot_p` | 0.5395 kg/s | 0.533 kg/s (+1.2 %) |
| Volumetric efficiency `epsilon_v` (cylinder inlet) | 0.949 | plausible |
| `epsilon_v_bis` (standard atmosphere) | 2.16 | > 1: supercharged |
| Compressor pressure ratio `r_p_cp` | 2.577 | 2.5 + filter |
| Compressor isentropic efficiency `epsilon_s_cp` | 0.697 | plausible |
| Derating factor `K` | 0.899 | 1133 m, 30 °C |
| Derated shaft power `W_dot_sh_x` | −348.5 kW | −11.3 % |
| CO2 emissions `Em_CO2` | 5500 g/km | 25 knots; original gave 1.53 g/km (corrected, see log) |

The two normalised-speed forms `N|star` and `N|star_bis` give the same value
(5541), as intended by the original.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![Derated power vs altitude](figures/scania_marine_diesel_handbook_derating.png)  + one-line caption -->

## Verification

Reference: the solution stored in the EES file (79 variables), compared with
`tools/compare_solution.py`:

```
74 common variables, 10 differ (rtol=0.001); only in EES: 5; only in CoolSolve: 15
Only in EES reference: a, m, P, param, T
```

- The 5 EES-only names (`a`, `m`, `P`, `param`, `T`) are stale stored
  variables of the original file that no equation uses.
- The 15 variables that the EES file does not store are the string
  variables, the built-in `pi`, and 12 handbook data/intermediate values
  (`csp`, `C|o_m`, `V|o_s`, `M|o_p`, `Tau|o`, `L|star`, `N|star`,
  `N|star_bis`, `DELTAP_bar_e`, `M_dot_f`, `V_c`, `Rés`); they follow from
  the same equations as the compared variables.
- 6 of the 10 differences are the documented absolute `Air` enthalpy/entropy
  reference-state offsets of the property backends (EES − CoolSolve =
  +125.9 kJ/kg on `h`, +1815.15 J/kg-K on `s`; CoolSolve
  docs/ees_import.md §11), and 3 more are the derived differences
  `w_cp` (1.05e-3), `w_s_cp` (2.23e-3) and `epsilon_s_cp` (1.18e-3), within
  the ≤ 0.5 % property tolerance. The isentropic temperature
  `T_a_ex_s_cp` agrees.
- `v_bateau` and `Em_CO2` differ by the documented ×3600 correction of a
  genuine unit error of the original (conversion log): the EES stored values
  (46.3 "km/s", 1.528 g/km) carry the same slip.
- All other common variables agree exactly (input data and explicit
  algebra) or within 8.3e-4 (`T_a_ex_s_cp` 8.3e-4, `rho_a_amb` 3.2e-4,
  `epsilon_v`, `epsilon_v_bis`: ideal-gas property backend differences).
  The maximum printed relative difference is 3.18e-01, on the absolute
  `s_a_su_cp` (reference-state offset).

The thermal balance closes at 1.52 % of the fuel input (handbook data
rounding), and the derating and CO2 results were checked for plausibility
(−11.3 % power at 1133 m/30 °C; ≈ 254 kg CO2/h over 46.3 km/h ≈ 5.5 kg/km).

## Source and attribution

Source file:
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/Examen/RESOLUTION_NGEN.EES`
(TM-0224, EES 10.589, RTF). Instructor solution of the MCI exam of June 2017
(the file's export block names `Examen_Juin_2017/SCANIA
DI09-DI16_Examen_2016-2017`), from the "NGEN" unit of Prof. Ph. Ngendakumana
(Thermotechnics Unit, ULiège); EES licence stamp R. Dickes. Published as an
example per the maintainer decisions in `sources/thermo_models/README.md`
(exam statements paraphrased, no student data). Library version by the
CoolSolve Library workers (MIT).

## Conversion log

- **2026-10-22 — import**: extracted with
  `CoolSolve/tools/ees_extract.py` (RTF equations converted to text, licence
  and display tags removed, one NUL byte deleted at end of file). Unit
  system of the file already `SI MASS DEG PA C J`: no unit conversion. The
  `$UnitSystem` and `$TABSTOPS` directives were deleted (CoolSolve is
  SI-°C-Pa-J). Comments translated from French; section titles kept. The
  statement `parm = 12 ; parn = 26` was split over two lines (one equation
  per line, no change of meaning). The dead export block commented out at
  the end of the original (`Filename$ = 'D:\…'`, `$Export …`, a hard-coded
  Windows path) was removed. Variable names, equations and values unchanged.
- **2026-10-22 — correction of a genuine error (CO2 section)**: the original
  computes `v_bateau = 25*1.852` and annotates it km/s (its own comment says
  "conversion des nœuds en km/s"), but 25 knots = 46.3 km/**h** = 0.012861
  km/s; dividing by the km/h value understates `Em_CO2` by a factor 3600
  (1.53 g/km, i.e. ~35× better than a passenger car for 35× the power). The
  import divides by 3600 (`v_bateau = 25*1.852/3600`); impact: `Em_CO2`
  1.53 → 5500.28 g/km, no other variable affected. The EES stored solution
  carries the same slip (`v_bateau` = 46.3 annotated km/s, `Em_CO2` =
  1.528 g/km), so these two variables are intentionally different in the
  verification comparison.
- **Level**: score of docs/taxonomy.md §3 — equations 88 (1), largest block
  1 (0), no functions/arrays (0), no multi-zone structure (0), semi-empirical
  ISO 3046-type derating law (1), no curated guesses (0) → score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The handbook heat flows (`Q_dot_water`, `Q_dot_air`, `Q_dot_exhaust`,
  `Q_dot_rad`) are inputs of the balance, not computed; the balance residue
  (1.52 %) only shows their mutual coherence.
- The derating law ignores the coolant-temperature exponent
  (`param_q` unused, as in the original) and humidity (`param_a = 0`).
- No CoolSolve gap blocks this model (`$IF` conditional compilation with a
  string constant and `molarmass` of the elements C/H are supported).

## Related models

- `CSL-0273` *engine_data_coherence_derating*: the other instructor solution
  ("RD") of the same MCI exam problem, for the DI09 072M engine. Different
  equations (only 4 common lines) and scope: it adds coherence checks the
  NGEN solution has not (charge-air cooler duty from the measured ΔT and cp,
  power from torque, exhaust flow) and does not have the four-engine
  `$IF` selection, the filter pressure drop, the ISO-ambient volumetric
  efficiency nor the normalised-speed checks.
- `CSL-0151` *engine_derating_iso3046*: the same ISO 3046/1 derating law
  (same `alpha` equation) as a standalone model.
