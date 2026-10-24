# Adiabatic flame temperature of CH4 or fuel oil with or without dissociation

🟠 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0150`

Adiabatic, constant-pressure combustion of CH4 or of a fuel oil (ultimate
analysis C = 86.9 %, H = 13.1 %) with excess air e ≥ 0. The adiabatic flame
temperature follows from the first law on the reaction, H_reactants =
H_products, either with complete-combustion products (CO2, H2O, O2, N2) or —
the interesting case — with the 14-species **chemical-equilibrium** mixture
(H2, O2, H2O, CO, CO2, OH, H, O, N2, N, NO, NO2, CH4, Ar) computed by the
built-in EES routine `Chem_Equil`, so that dissociation at high temperature
is accounted for.

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | The 14 equilibrium species as ideal-gas fluids in property calls: CH4, O2, N2, CO2, H2O, CO, H2, Ar (registered in CoolSolve) and OH, H, O, N, NO, NO2 (not registered); their mole fractions come from `Chem_Equil` |
| **Size** | 84 equations over the four `$IF` cases (≈ 51 for the stored run; largest block: 2) |
| **Source** | ULiège — course MCI, TP1 exercises 3-4, 2016 (EES file `Ex_3-4_CH4-Fuel Oil_Tadiab with or without dissociation_2016.EES`) |
| **Authors** | P. Ngendakumana, R. Dickes (ULiège Thermotechnics; see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | native file **blocked** by `CS-GAP-CHEM-EQUIL` and `CS-GAP-FLUIDS-NASA-SPECIES`; no runnable variant (see *Why no runnable variant*) |

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
original). The enthalpy balance is written per kmol of fuel:

- **Without dissociation**: products `m CO2 + n/2 H2O + (m+n/4)·e·O2 +
  (m+n/4)·(79/21)·(1+e)·N2`; molar species enthalpies
  `MolarMass(X)·enthalpy(X, T=T)` [J/kmol] (DUPLICATE over the species) at the
  reference and flame temperatures; the ideal-gas enthalpies include the heat of
  formation, so the balance needs no heat of reaction.
- **With dissociation**: `CALL CHEM_EQUIL(P, T, A\O, C\O, H\O, N\O : x_H2 …
  x_Ar)` returns the equilibrium mole fractions from the element ratios and
  the pressure; `Nprod = 14` species enthalpies again as property calls; the
  total product amount `ntot` follows from the H-atom balance
  `n = ntot·(2·x_H2 + 2·x_H2O + x_OH + x_H + 4·x_CH4)`.

The species names are not an array of strings but the rows of two lookup tables,
read with `LOOKUP$('Species14', i, 1)` (the 14 equilibrium species, in the order of
`x[i]`) and `LOOKUP$('Species4', i, 1)` (CO2, H2O, O2, N2, the order of `nkmol[i]`) in
the `DUPLICATE` loops: companion files `adiabatic_flame_dissociation-Species14.csv` and
`-Species4.csv`.

Unknowns of the stored run (CH4, dissociation): `T_adiab` (from
`H_react = H_prod`) and `ntot`; the 14 mole fractions are procedure outputs.

## How to run

The file is valid EES: open it in EES and select the case by
commenting/uncommenting the `FUEL$` and `DISSOCIATION$` lines. In CoolSolve
it does **not** run: `CALL CHEM_EQUIL` is an unknown procedure
(`CS-GAP-CHEM-EQUIL`) and six of the fourteen species (OH, H, O, N, NO, NO2) are no
CoolSolve fluids (`CS-GAP-FLUIDS-NASA-SPECIES`). The file as shipped is square (78
equations); the `$IF`/`$IFNOT` directives are resolved (with the file as shipped,
`FUEL$ = 'CH4'` and `DISSOCIATION$ = 'YES'`, the `'Oil'` lines are removed). With
`DISSOCIATION$ = 'NO'` the file runs (see *Verification*).

## Results (EES stored solution)

The source file stores its last run — CH4, `DISSOCIATION$ = 'YES'`, e = 0.2,
30 bar, reactants at 288 K. 26 of the 28 stored variables carry values (`CO`
and `NO` are cleared); the Oil-case records (`MM_f`, `LHV_f`, `c_f`, `H_rf`,
`H_ra`, `HHV`, `LHV_f_bis`) belong to the alternative fuel case of this
multi-case file and are stale for the last run.

| Quantity | EES stored value |
|---|---:|
| `T_adiab` adiabatic flame temperature | 2417.129 K (2143.98 °C) |
| `H_react` = `H_prod` | −78 333.0 kJ/kmol fuel |
| `P_comb` combustion pressure | 3000 kPa |
| `ntot` products | 0.542859 kmol (see caveat below) |
| `m`, `n` of the fuel | 1, 4 (CH4) |

Caveat (flagged, not resolvable without EES): the stored `ntot` = 0.54286
kmol is inconsistent with the file's own H-atom balance for the same run —
with mole fractions summing to 1, `ntot = 4/(2·x_H2 + 2·x_H2O + x_OH + x_H +
4·x_CH4)` cannot be smaller than 2 kmol per kmol CH4. The stored record set
appears to mix runs (as the Oil-case records do), or the equations changed
after the last solve; the author's concluding comment itself says he was
looking for an error: *"near stoichiometric conditions the adiabatic
temperature should be lower with dissociation than without; this is the case
with CH4, but not with fuel oil. Why? I have not found the error in my
equations!"* (translated; kept in the model file).

## Verification

**Partial, in a scratch copy.** The file as shipped does not run in CoolSolve
(status `blocked`, no runnable variant, see below). The no-dissociation case (CH4,
`DISSOCIATION$ = 'NO'`, e = 0.2, reactants at 288 K), solved in a scratch copy in which
only that line of the file was changed (27 equations, 6 iterations; the species names
are read from `Species4` with `LOOKUP$`), gives `T_adiab` = 1788.7 °C
(2061.8 K) and `H_react` = `H_prod` = −78 351 kJ/kmol fuel. An independent hand
balance (Python; sensible enthalpies from the NASA-Glenn polynomials of `thermo.inp`, formation
enthalpies −74 600, −393 510 and −241 826 kJ/kmol for CH4, CO2 and H2O vapour as in
CoolSolve) gives 1787.85 °C and −78 344 kJ/kmol, i.e. 0.8 K (CoolProp's ideal-gas specific
heats) and 0.01 % apart. The molar enthalpy rise of
the species from 25 °C to 2127 °C agrees with JANAF within 0.11 % (N2, O2, CO2, H2O,
CO, H2).

The EES stored solution above (dissociation, `H_react` = −78 333.0 kJ/kmol fuel) is the
verification reference for a future re-check when the blocking gaps are closed. Its
reactant side is 0.02 % less negative than the scratch value (0.34 % with the rounded
JANAF formation enthalpy of CH4, −74 850, that CoolSolve used before taking the NASA-Glenn
data of the EES ideal gases); the 18 kJ/kmol difference is of the size of the R = 8.314
scaling of the EES enthalpies (6e-5) and of CoolProp's specific heats.

## Why no runnable variant

A faithful transcription of the stored operating point (dissociation ON) is
not possible: it would require re-implementing the 14-species Gibbs-energy
equilibrium solver inside the model, and six of the fourteen equilibrium
species (H, O, OH, N, NO, NO2) are not registered as CoolSolve fluids at all
(`CS-GAP-FLUIDS-NASA-SPECIES`).
A no-dissociation variant would answer a different question than the stored
reference (and has no stored EES values to verify against). The model is
therefore shipped blocked, like `CSL-0081`, without a `_coolsolve` variant.

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
  - `T_fuel = T_air = 288 [K]` → `14.85 [°C]`; `T_adiab` in °C with
    `T_adiab_K = T_adiab+273.15` passed to the `Chem_Equil` call (its data are
    defined in K);
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
- **Blocked in CoolSolve** (native file kept in valid EES): `CALL CHEM_EQUIL` →
  *"Unknown procedure: CHEM_EQUIL"* (`CS-GAP-CHEM-EQUIL`), `enthalpy(OH, …)` and the
  five other species → *"Unknown fluid"* (`CS-GAP-FLUIDS-NASA-SPECIES`). The EES stored bounds
  of `T` (1000–3500 K) also keep EES in the physical branch (`CS-GAP-BOUNDS`); not
  blocking.

- **No runnable variant**: see the section above.
- **Level**: active-case equations ≈ 51 (score 1, 50–300) + largest block 2
  (0) + arrays/DUPLICATE and procedure calls (1) + no multi-zone (0) + no
  calibration/dynamics (0) + no curated guesses needed by the equations
  themselves (0) = 2 → level 2 by the score; consistent with the inventory
  guess (2). The topic (chemical-equilibrium combustion) is advanced
  applied-thermodynamics material.
- **Reference values**: `T_adiab` 2417.129 K and `H_react = H_prod`
  −78 333.0 kJ/kmol quoted from the stored solution; `ntot` flagged as
  inconsistent (see *Results*).

## Related models

- `CSL-0046` *octane_combustion_400pct_air*: adiabatic flame temperature
  without dissociation (complete-combustion products only), verified runnable
  variant.
- `CSL-0005` *cpbar_combustion_products*: function library for the mean
  specific heat of CmHn combustion products, from the same ULiège
  combustion-course material.
- `CSL-0139` *combustion_chamber*: combustion chamber translated from TESPy;
  complete combustion only (the dissociation this model adds is not included
  there), species-resolved flue gas for an excess-air ratio lambda.
- Inventory neighbours of the same TP series (not yet imported): TM-0230
  (T&P effects on dissociation, `Chem_Equil`), TM-0232 (NASA properties of
  CO2), TM-0234/TM-0235 (RD solution variants of exercises 1-3).
- `CSL-0264` *temperature_pressure_effects_dissociation*: TP1 exercise 2 of
  the same series (imported from TM-0230), the same `CHEM_EQUIL` call used
  for the equilibrium composition only — no flame-temperature balance.
