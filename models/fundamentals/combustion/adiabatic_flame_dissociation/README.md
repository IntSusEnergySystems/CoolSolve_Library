# Adiabatic flame temperature of CH4 or fuel oil with or without dissociation

🟠 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0150`

Adiabatic, constant-pressure combustion of CH4 or of a fuel oil (ultimate
analysis C = 86.9 %, H = 13.1 %) with excess air e ≥ 0. The adiabatic flame
temperature follows from the first law on the reaction, H_reactants =
H_products, either with complete-combustion products (CO2, H2O, O2, N2) or —
the interesting case — with the 14-species **chemical-equilibrium** mixture
(H2, O2, H2O, CO, CO2, OH, H, O, N2, N, NO, NO2, CH4, Ar) computed by the
built-in routine `CHEM_EQUIL`, so that dissociation at high temperature is
accounted for.

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | The 14 equilibrium species as ideal-gas fluids in property calls (CH4, O2, N2, CO2, H2O, CO, H2, Ar from CoolProp's ideal-gas equations of state; OH, H, O, N, NO, NO2 from the NASA-Glenn polynomials); their mole fractions come from `CHEM_EQUIL` |
| **Size** | 84 equations over the four `$IF` cases (78 for the shipped case, CH4 with dissociation; largest block: 45, the flame temperature with the equilibrium composition and the species enthalpies) |
| **Source** | ULiège — course MCI, TP1 exercises 3-4, 2016 (EES file `Ex_3-4_CH4-Fuel Oil_Tadiab with or without dissociation_2016.EES`) |
| **Authors** | P. Ngendakumana, R. Dickes (ULiège Thermotechnics; see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | verified; `coolsolve.conf` sets `enableEquationScaling = true` |

## Problem statement

Compute the adiabatic combustion temperature at 30 bar of CH4 (or of a fuel
oil entering at 15 °C with its LHV) burning with 20 % excess air, the air and
the fuel entering at 288 K, with and without dissociation of the products.
Switching the fuel and the dissociation option is done by commenting/uncommenting
two lines in the original file (`FUEL$`, `DISSOCIATION$`), whose `$IF`
directives select the corresponding equation blocks.

## Model

Reactants: `CmHn + (m+n/4)·(O2 + 79/21·N2)·(1+e)` — for CH4, m = 1 and n = 4;
for the fuel oil, m and n come from the ultimate analysis (kmol of C and H per
kg of fuel) and the fuel enthalpy from its LHV (42 855 kJ/kg) and specific
heat, with an empirical HHV/LHV check on the ultimate analysis (as in the
original). The enthalpy balance is written per kmol of CH4, or per kg of fuel
oil:

- **Without dissociation**: products `m CO2 + n/2 H2O + (m+n/4)·e·O2 +
  (m+n/4)·(79/21)·(1+e)·N2`; molar species enthalpies
  `MolarMass(X)·enthalpy(X, T=T)` [J/kmol] (DUPLICATE over the species) at the
  reference and flame temperatures; the ideal-gas enthalpies include the heat of
  formation, so the CH4 balance needs no heat of reaction.
- **With dissociation**: `CALL CHEM_EQUIL(P, T, A\O, C\O, H\O, N\O : x_H2 …
  x_Ar)` returns the equilibrium mole fractions from the element ratios, the
  pressure and the temperature (in the units of the model, Pa and °C);
  `Nprod = 14` species enthalpies again as property calls; the total product
  amount `ntot` follows from the H-atom balance
  `n = ntot·(2·x_H2 + 2·x_H2O + x_OH + x_H + 4·x_CH4)`.

The species names are not an array of strings but the rows of two lookup tables,
read with `LOOKUP$('Species14', i, 1)` (the 14 equilibrium species, in the order of
`x[i]`) and `LOOKUP$('Species4', i, 1)` (CO2, H2O, O2, N2, the order of `nkmol[i]`) in
the `DUPLICATE` loops: companion files `adiabatic_flame_dissociation-Species14.csv` and
`-Species4.csv`.

Unknowns of the shipped case (CH4, dissociation): `T_adiab` (from
`H_react = H_prod`) and `ntot`, solved in one block of 45 unknowns with the 14
mole fractions and the 14 species enthalpies at `T_adiab`.

## How to run

Open the model folder in CoolSolve (or `coolsolve adiabatic_flame_dissociation.eescode`)
and solve; select the case by commenting/uncommenting the `FUEL$` and
`DISSOCIATION$` lines. The `coolsolve.conf` of the folder sets
`enableEquationScaling = true`: the flame block holds enthalpies of 1E8 J/kmol
and an energy balance of 1E9 beside mole fractions down to 1E-20, and Newton's
steps must be solved on the equilibrated system to keep the directions of the
small equations (without it the block stops with *LineSearchFailed*). The guess
file `adiabatic_flame_dissociation.initials` holds the values of the EES file; the
model also solves from `T_adiab = 1775`, `ntot = 12.5`.

## Results (CoolSolve, shipped case)

CH4 with 20 % excess air at 30 bar, reactants at 288 K, with dissociation:

| Quantity | Value |
|---|---:|
| `T_adiab` adiabatic flame temperature | 1776.08 °C (2049.23 K) |
| `H_react` = `H_prod` | −78 344 kJ/kmol CH4 |
| `ntot` products | 12.433 kmol per kmol CH4 |
| `x_CO`, `x_NO`, `x_OH` | 1.66E-4, 3.19E-3, 9.75E-4 |

Without dissociation the same flame is at 1788.95 °C: dissociation lowers it by
12.9 K at 30 bar and 20 % excess air.

## Verification

**EES stored solution.** The last run stored in the source file is the fuel oil,
stoichiometric (e = 0), at 1 atm, with dissociation: its `CHEM_EQUIL` inputs are
P = 101.325 kPa, T = 2417.129 K, `C\O` = 0.3442947702 and `H\O` = 0.6228209192 (the
ratios of the oil at e = 0, which CoolSolve reproduces to 10 digits). The case was
solved in a scratch copy with `FUEL$ = 'Oil'`, `e = 0` and `P_comb = 101325` as the
only changes (9 iterations):

| Quantity | EES | CoolSolve | Difference |
|---|---:|---:|---:|
| `T_adiab` | 2417.129 K | 2412.01 K | −5.1 K (−0.21 %) |
| `ntot` [kmol/kg fuel] | 0.542859 | 0.542752 | −0.02 % |
| `x_H2O`, `x_N2`, `x_CO2` | 0.11292, 0.72655, 0.10892 | 0.11293, 0.72683, 0.10927 | +0.005 %, +0.04 %, +0.32 % |
| `x_CO`, `x_O2`, `x_H2` | 0.024481, 0.010549, 0.004335 | 0.024158, 0.010386, 0.004202 | −1.3 %, −1.5 %, −3.1 % |
| `x_OH`, `x_NO` | 0.005672, 0.004478 | 0.006019, 0.004184 | +6.1 %, −6.6 % |

EES's `Chem_Equil` uses older JANAF data, CoolSolve the NASA-Glenn data; at the same
temperature the major species agree within 0.4 % and OH, NO, NO2 differ by 4 to 10 %
(CoolSolve Language Reference, `CALL CHEM_EQUIL`). The records `H_react` =
−78 333.0 kJ/kmol, `P_comb` = 3000 kPa, `m` = 1 and `n` = 4 of the file belong to an
earlier CH4 run of this multi-case file and do not describe the stored run.

**Independent implementation.** The shipped CH4 flame computed with an independent
Python implementation (Gibbs-energy equilibrium of the 14 species and enthalpies from
the NASA-Glenn polynomials): 2048.2268 K. CoolSolve gives 2049.23 K, 1.0 K above:
the property calls use CoolProp's ideal-gas equations of state for 8 of the species
(with `CALL NASA` enthalpies instead of the property calls CoolSolve gives 2048.23 K).
Without dissociation, a hand balance with the NASA-Glenn data gives 1787.85 °C
against 1788.95 °C.

## Why dissociation does not cool the fuel-oil flame

The author's closing comment asks why the flame is cooler with dissociation for CH4
but not for the fuel oil. The two branches of the model write the energy balance
differently. For CH4 the products' enthalpies `H[i]` include the heats of formation,
so the chemical energy left in CO, H2, OH, NO… is charged to the products. For the
fuel oil the reactants carry the LHV — the heat of the *complete* combustion — and the
products are summed as sensible enthalpies `H[i] − H_ref[i]`: the formation enthalpies
cancel, the energy the dissociation absorbs is never subtracted, and the flame
temperature is that of complete combustion. CoolSolve reproduces it: at e = 0 and 1 atm
the oil flame is 2138.86 °C with dissociation and 2136.59 °C without; at 30 bar and
e = 0.2, 1858.06 °C and 1858.12 °C. Adding `Σ ntot·x[i]·Δh_f[i]` minus the formation
enthalpies of the complete-combustion products to `H_prod` would correct the oil
branch; the model keeps the equations of the original.

## Source and attribution

Exercise file of the ULiège course MCI, TP1 exercises 3-4 (2016), from the
`MCI_REMIDICKES` folder of the collection; the inventory attributes it to
**P. Ngendakumana** (the EES licence tag reads *"For use only by Philippe
Ngendakumana, ULG - Thermotechnics Unit, Liege, Belgium"* — a licence stamp,
which may differ from the author) and **R. Dickes** (the companion solution
files `Exo_1/2/3_resolution_RD.EES` of the same TP are initialled RD). To be
confirmed by the maintainer.

Source file (EES 10.589, stored as RTF, comments in English), collection of
S. Quoilin:
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP1_Ex_1-5/Ex_3-4_CH4-Fuel Oil_Tadiab with or without dissociation_2016.EES`
(inventory candidate `TM-0231`).

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MOLE DEG KPA K KJ`, RTF equations, no tables; converted by
  hand to SI-°C-Pa-J (ees_import.md §6):
  - `T_réf = 298.15 [K]` → `T_ref = 25 [°C]`; the variable is renamed
    `T_ref` (non-ASCII identifiers are avoided);
  - `P_comb = 30*Convert('bar','kPa')` → `P_comb = 30E5 [Pa]`;
  - `T_fuel = T_air = 288 [K]` → `14.85 [°C]`; `T_adiab` in °C, passed to
    `CHEM_EQUIL` as `T = T_adiab` with the pressure in Pa (CoolSolve's routine
    takes the units of the model; the original passes K and kPa);
    `T_adiab_K = T_adiab+273.15` is kept as an output;
  - **molar → mass basis**: the ideal-gas `Enthalpy` calls of the original
    (kJ/kmol in the MOLE unit system) become
    `molarmass(X)*enthalpy(X,T=…)` [J/kmol]; `LHV_f = 42855E3`, `c_f = 1885`;
    the empirical HHV/LHV correlations keep their kJ-based coefficients and
    feed a local `HHV_kJ`, converted to J only afterwards;
  - EES `NASA` procedure calls replaced by ideal-gas property calls, decision D12
    (`MolarMass(X)*enthalpy(X,T=…)` [J/kmol] at `T_ref` and `T_adiab`, in °C);
  - string array `Prod$[…]` replaced by the lookup tables
    `adiabatic_flame_dissociation-Species14.csv` and `-Species4.csv` and `LOOKUP$`,
    decision D14 (string arrays are not supported by CoolSolve);
  - everything else (the `$IF`/`$IFNOT` structure, the commented case lines,
    the `{T_adiab = 2000}` guess-update hint, `C%`/`H%`/`O%`/`S%` names,
    the `A\O`-style names, the `CHEM_EQUIL` call signature) is unchanged.
- **Solver configuration**: `coolsolve.conf` with `enableEquationScaling = true`
  (equilibrated Newton steps for the flame block, see *How to run*).
- **Level**: active-case equations 78 (score 1, 50–300) + largest block 45 (2) +
  arrays/DUPLICATE and procedure calls (1) + no multi-zone (0) + no
  calibration/dynamics (0) + tuned `coolsolve.conf` (1) = 5 → level 3 by the
  score, moved to level 2: a course exercise, whose large block is the
  equilibrium composition computed by one built-in routine.
- **Reference values**: the EES stored run (fuel oil, e = 0, 1 atm, see
  *Verification*); the CH4 records of the file are stale.

## Limitations

- The fuel-oil branch omits the energy absorbed by dissociation (see *Why
  dissociation does not cool the fuel-oil flame*); kept as in the original.
- `x_CH4` (~1E-20) is known to the absolute tolerance only in a block with terms
  of 1E9: it can come out as −1.4E-20 (warning W002); the other mole fractions are
  unaffected.
- The EES stored bounds of `T` (1000–3500 K) are not used (`CS-GAP-BOUNDS`); the
  guesses keep the solution in the physical branch.

## Related models

- `CSL-0046` *octane_combustion_400pct_air*: adiabatic flame temperature
  without dissociation (complete-combustion products only).
- `CSL-0005` *cpbar_combustion_products*: function library for the mean
  specific heat of CmHn combustion products, from the same ULiège
  combustion-course material.
- `CSL-0139` *combustion_chamber*: combustion chamber translated from TESPy;
  complete combustion only (the dissociation this model adds is not included
  there), species-resolved flue gas for an excess-air ratio lambda.
- Inventory neighbours of the same TP series (not yet imported): TM-0232 (NASA
  properties of CO2), TM-0234/TM-0235 (RD solution variants of exercises 1-3).
- `CSL-0264` *temperature_pressure_effects_dissociation*: TP1 exercise 2 of
  the same series, the same `CHEM_EQUIL` call used for the equilibrium
  composition only — no flame-temperature balance.
