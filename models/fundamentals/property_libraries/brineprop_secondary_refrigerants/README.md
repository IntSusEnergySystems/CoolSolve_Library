# BrineProp: thermophysical properties of aqueous secondary refrigerants (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0079`

The **freezing point, density, specific heat, thermal conductivity and
dynamic viscosity** of eleven aqueous secondary refrigerants — glycols,
alcohols, ammonia and salt brines (`EG`, `PG`, `EA`, `MA`, `GL`, `NH3`,
`K2CO3`, `CaCl2`, `MgCl2`, `NaCl`, `KAc`) — as a function of the mass
concentration and the temperature, with the correlations of the **BrineProp**
library of the ULiège model bank (an 18-term polynomial in the deviations of
the concentration and the temperature from the mean values of the solution).
One line gives a model all of it:

```
$INCLUDE brineprop_secondary_refrigerants
```

- `rho = BrineProperty('Density', 'EG', 30, T)` — a **function in SI units**,
  for use in any equation (also solved for `T` or the concentration);
- `CALL BRINEPROP(...)` and `CALL BRINEPROP2(...)` — the two procedures of the
  EES library, with their signatures and output units, so that the EES models
  of the collection that call them run unchanged.

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | aqueous solutions EG, PG, EA, MA, GL, NH3, K2CO3, CaCl2, MgCl2, NaCl, KAc (secondary refrigerants; not CoolProp fluids) |
| **Size** | one function and two procedures (~50 lines); 41 equations in the demonstration program (largest block: 6, a `BRINEPROP2` call); two lookup tables, the solutions (11 rows) and the polynomial coefficients (198 × 5) |
| **Source** | ULiège Thermodynamics Laboratory — EES libraries `Brineprop.lib` (1997 edition according to its EES help file) and `Brineprop2.LIB`, with their binary coefficient tables `Brine1.lkt` and `Brine2.lkt` |
| **Authors** | TBD (ULiège Thermodynamics Laboratory; the EES help file of the library credits its 1997 edition and refers to IIR thermo-physical data, no personal name; the inventory attributes the library to the laboratory, J. Lebrun et al.) |
| **License** | MIT |
| **CoolSolve** | **verified** against EES stored solutions: 9 values of `BRINEPROP` (glycol run-around loop model of the same library) and `BRINEPROP2` (Vitocal heat pump model `CSL-0116`), ≤ 4.77e-10 |

## Problem statement

Give the thermophysical properties of an aqueous secondary refrigerant
(glycol, alcohol, brine) at a given mass concentration and temperature. Such
libraries replace a table lookup in the secondary-circuit models of HVAC and
heat-pump systems, where the brine side is treated as an incompressible fluid
whose ρ, c_p, k and μ are needed at each state.

## Model

| Routine | Use | Returns |
|---|---|---|
| `BrineProperty(Prop$, Fl$, Conc, Temp)` (FUNCTION) | `rho = BrineProperty('Density', 'EG', 30, T)` | the property `Prop$` in **SI units**: `'Freeze'` freezing point [°C], `'Density'` [kg/m³], `'SpecHeat'` [J/kg·K], `'ThermalC'` [W/m·K], `'DynVisc'` dynamic viscosity [Pa·s] |
| `BRINEPROP` (PROCEDURE) | `CALL BRINEPROP(Pr$, Fl$, Conc, Temp : output)` | one property, `Pr$` as above, in the units of the EES library: specific heat in **kJ/kg·K**, viscosity in **milliPa·s** |
| `BRINEPROP2` (PROCEDURE) | `CALL BRINEPROP2(Fl$, Conc, Temp : FreezingPt, Density, SpecHeat, ThermalConductivity, DynamicViscosity, Pr)` | the five properties and the Prandtl number, in the units of the EES library: specific heat in **kJ/kg·K**, viscosity in Pa·s |

`Fl$` is the code of the solution, `Conc` its mass concentration [%] and `Temp`
its temperature [°C]; property names and codes are read in any case
(`'cacl2'`, `'specheat'`). `BRINEPROP` and `BRINEPROP2` are thin wrappers of
`BrineProperty`, so the three always agree; a new model calls `BrineProperty`.

`BrineProperty`:

1. finds the solution in the table `BrineSolutions` (`LOOKUP$ROW` on the
   column `Code`; an unknown code is an error that names it) and stops with
   `CALL ERROR` when `Conc` is outside the range `Conc_min` … `Conc_max` of
   the solution, or when the property name is not one of the five;
2. reads the 18 coefficients `c[k]` of the solution and the property from the
   table `BrineCoefficients` (row `18·(i−1) + k` for the solution in row `i`
   of `BrineSolutions`, one column per property);
3. with `x = Conc − Conc_mean` and `y = Temp − T_mean` (the mean values of the
   solution), evaluates
   `f = c[1] + c[2]y + c[3]y² + c[4]y³ + c[5]x + c[6]xy + c[7]xy² + c[8]xy³ + c[9]x² + c[10]x²y + c[11]x²y² + c[12]x²y³ + c[13]x³ + c[14]x³y + c[15]x³y² + c[16]x⁴ + c[17]x⁴y + c[18]x⁵`,
   which is the property in SI units, except for the viscosity, whose
   polynomial gives the logarithm of the viscosity in milliPa·s
   (`μ = exp(f)/1000` Pa·s).

Table `BrineSolutions` (`brineprop_secondary_refrigerants-BrineSolutions.csv`):

| `Code` | `Name` | `Conc_min` … `Conc_max` [%] | `Conc_mean` [%] | `T_mean` [°C] |
|---|---|---|---|---|
| EG | ethylene glycol | 0 – 56.1 | 38.1615 | 6.3333 |
| PG | propylene glycol | 15.2 – 57.0 | 42.7686 | 5.3571 |
| EA | ethyl alcohol | 11.1 – 60.1 | 38.925 | −4.9038 |
| MA | methyl alcohol | 7.8 – 44.3 | 32.9283 | −6.25 |
| GL | glycerol | 19.5 – 63.0 | 47.8467 | 7.0 |
| NH3 | ammonia | 7.8 – 23.6 | 17.9664 | −7.1429 |
| K2CO3 | potassium carbonate | 13.3 – 39.0 | 27.6708 | 4.1667 |
| CaCl2 | calcium chloride | 9.0 – 29.4 | 22.918 | 0.2459 |
| MgCl2 | magnesium chloride | 7.2 – 20.5 | 13.7 | 5.875 |
| NaCl | sodium chloride | 7.9 – 22.6 | 12.3539 | 9.2581 |
| KAc | potassium acetate | 11.0 – 41.0 | 30.9656 | 0.2459 |

The concentration ranges are those that the EES procedures test; the mean
values are the table `Brine2` of the EES library. The names are the usual
expansion of the codes: the EES help file of the library (`BRINEPROP.hlp`,
table *Limits*) names them *Ethylene Glycol*, *Propylene Glycol*, *Alcohol*,
*Methanol*, *Glycerol*, *Ammonia*, *Potassium Carbonate*, *Chloride*,
*Magne…*, *Soda* and *Acetate*, the three last ones only partly legible in
that compiled file. Table `BrineCoefficients`
(`brineprop_secondary_refrigerants-BrineCoefficients.csv`) is the table `Brine1`
of the EES library, its five columns named after the properties (`Freeze`,
`Density`, `SpecHeat`, `ThermalC`, `DynVisc`).

## How to run

```bash
coolsolve ./brineprop_secondary_refrigerants.eescode
```

`solve` in 30 iterations; the baseline is `brineprop_secondary_refrigerants.sol`
(regression-tested as `CSL-0079`). A model that uses the library writes
`$INCLUDE brineprop_secondary_refrigerants` (or `$INCLUDE CSL-0079`):
CoolSolve imports the three routines and the two tables, not the
demonstration program. The native files of `CSL-0072`, `CSL-0074`, `CSL-0078`,
`CSL-0116`, `CSL-0161`, `CSL-0162` and `CSL-0163` get them this way.

## Results

Demonstration program (after the routines), regression case of the baseline
(`brineprop_secondary_refrigerants.sol`):

Case 1 — `BRINEPROP`, propylene glycol 50 % at 65 °C, the example block that
followed `END` in `Brineprop.lib`:

| Quantity | Value |
|---|---:|
| `T_freeze_1` [°C] | −33.0940254 |
| `rho_brine_1` [kg/m³] | 1006.87140 |
| `c_p_brine_1_kJ` [kJ/kg·K] | 3.70784870 |
| `k_brine_1` [W/m·K] | 0.380096893 |
| `mu_brine_1_mPa_s` [milliPa·s] | 1.35132125 |

Case 2 — `BRINEPROP`, ethylene glycol 25 % at 6.324036551 °C, the temperature
stored by the glycol run-around loop reference model of the same library
(inventory `TM-0476`), used for the verification below:

| Quantity | Value |
|---|---:|
| `T_freeze_2` [°C] | −10.9597832 |
| `rho_brine_2` [kg/m³] | 1036.22875 |
| `c_p_brine_2` [J/kg·K] (`c_p_brine_2_kJ` = 3.80535085) | 3805.35085 |
| `k_brine_2` [W/m·K] | 0.472382728 |
| `mu_brine_2` [Pa·s] (`mu_brine_2_mPa_s` = 2.94346083) | 0.00294346083 |

Case 3 — `BRINEPROP2`, ethylene glycol 30 % at −5 °C, the call of the Vitocal
300-G heat pump model (`CSL-0116`), used for the verification below:

| Quantity | Value |
|---|---:|
| `T_freeze_3` [°C] | −14.5981734 |
| `rho_brine_3` [kg/m³] | 1046.80069 |
| `c_p_brine_3_kJ` [kJ/kg·K] | 3.66057833 |
| `k_brine_3` [W/m·K] | 0.441521131 |
| `mu_brine_3` [Pa·s] | 0.00530539650 |
| `Pr_brine_3` [-] | 43.9861607 |

Case 4 — `BRINEPROP2`, calcium chloride 25 % at −4 °C, the example call that
followed `END` in `Brineprop2.LIB`, with its solution name in mixed case
(`'Cacl2'`):

| Quantity | Value |
|---|---:|
| `T_freeze_4` [°C] | −28.8933886 |
| `rho_brine_4` [kg/m³] | 1238.99040 |
| `c_p_brine_4_kJ` [kJ/kg·K] | 2.85300501 |
| `k_brine_4` [W/m·K] | 0.533827706 |
| `mu_brine_4` [Pa·s] | 0.00460410006 |
| `Pr_brine_4` [-] | 24.6062922 |

Case 5 — `BrineProperty` in equations (SI units) at the state of case 2: the
values of case 2 in SI units (`T_freeze_5` −10.9597832 °C, `rho_brine_5`
1036.22875 kg/m³, `c_p_brine_5` 3805.35085 J/kg·K, `k_brine_5`
0.472382728 W/m·K, `mu_brine_5` 0.00294346083 Pa·s).

<!-- FIGURE (maintainer, docs/model_workflow.md §7): e.g. density and specific heat
     of EG 25 % and PG 50 % versus temperature (−20…80 °C) as a parametric sweep. -->
## Verification

Status **verified** (native file): the nine properties that independent EES
references hold — three of `BRINEPROP`, six of `BRINEPROP2` — agree to
4.77e-10, well inside the tolerance. Comparison with
`tools/compare_solution.py` (default rtol = 0.001) against one reference CSV
holding both: `9 common variables, 0 differ (rtol=0.001)`, maximum relative
difference 4.77e-10 (`rho_brine_2`).

1. **EES reference of `BRINEPROP`.** A `.lib` file stores no solution of its
   own, so the reference is the stored solution of the *glycol run-around
   loop* reference model of the same library,
   `GLYCOLRECOVERYLOOP_RefSim_EES_Model_SB080116.EES` (EES 7.888, inventory
   `TM-0476`), which calls `BRINEPROP` for ethylene glycol 25 % at
   `t_gw_m` = 6.324036551 °C and stores the three results (`rho_gw`,
   `c_p_gw`, `mu_gw`). Extracted with `tools/ees_extract.py`; the three
   values, converted to the units of the model, form the reference CSV:

   | Variable | EES | CoolSolve | rel. diff |
   |---|---:|---:|---:|
   | `c_p_brine_2` [J/kg·K] | 3805.35 | 3805.35 | 7.88e-13 |
   | `mu_brine_2` [Pa·s] | 0.00294346 | 0.00294346 | 7.34e-11 |
   | `rho_brine_2` [kg/m³] | 1036.23 | 1036.23 | 4.77e-10 |

   The reference file holds only the three properties the glycol model
   stores, so the other variables of cases 1 and 2 have **no** EES reference
   and are not part of the figure.
2. **EES reference of `BRINEPROP2`.** The stored solution of the Vitocal
   300-G heat pump model of the collection
   (`HeatPump_Vitocal 300G -110_CGSQ1112288.EES`, library model `CSL-0116`),
   which calls `CALL BRINEPROP2('EG',30,-5:FreezingPt,Density,SpecHeat,
   ThermalConductivity,DynamicViscosity, Pr)` and stores the six outputs
   (extracted with `tools/ees_extract.py`; renamed to the variables of case 3,
   same units):

   | Variable | EES | CoolSolve | rel. diff |
   |---|---:|---:|---:|
   | `T_freeze_3` [°C] | −14.5982 | −14.5982 | 1.77e-10 |
   | `rho_brine_3` [kg/m³] | 1046.8 | 1046.8 | 3.59e-10 |
   | `c_p_brine_3_kJ` [kJ/kg·K] | 3.66058 | 3.66058 | 1.11e-10 |
   | `k_brine_3` [W/m·K] | 0.441521 | 0.441521 | 1.59e-11 |
   | `mu_brine_3` [Pa·s] | 0.0053054 | 0.0053054 | 6.03e-12 |
   | `Pr_brine_3` [-] | 43.9862 | 43.9862 | 6.59e-12 |

   Another EES value, outside the figure because it is not an output of this
   model: the plate heat exchanger file of `CSL-0161` keeps
   `T_freezing` = −10.95876809 °C from an earlier run of its EG branch
   (`BRINEPROP2` for EG 25 % at 25 °C), which `CSL-0161` reproduces to 6e-11.
   Cases 4 and 5 have no EES reference. No variable of the references was
   excluded.
3. **Rewrite against the EES procedures.** The routines of this model are a
   rewrite of the EES procedures (see *Conversion log*, 2026-11-05). Before the
   rewrite the model shipped the EES `BRINEPROP` and `BRINEPROP2` as copied
   from the libraries; the rewritten model gives the same values for the 32
   variables of cases 1 to 4 (relative difference 0.0), `BRINEPROP` and
   `BRINEPROP2` of the EES text agreed to 5.7e-11 on the five properties of
   all 11 solutions, and every model of the library that calls them
   reproduces its baseline with the rewrite (`CSL-0072`, `CSL-0078`,
   `CSL-0161`, `CSL-0162`, `CSL-0163`: ≤ 1.4e-8).
4. **Lookup tables.** `Brine1.lkt` and `Brine2.lkt` (EES 4.631 binary lookup
   files) were **decoded by hand** from the EES layout documented in
   `ees_import.md` §13 (per column: a short-string name in a 31-byte field,
   then *nrows* 10-byte values; the values are 80-bit extended floats written
   as a 64-bit little-endian significand followed by a 16-bit little-endian
   exponent whose bit 15 is the sign). The decode reproduces the EES stored
   values above to 4.8e-10, and it was made independently for `CSL-0072`,
   which shipped the same two tables: both decodes agree to the last printed
   digit (max. absolute difference 0.0). The CSV values are written with full
   round-trip precision (17 significant digits): the 18-term polynomial
   cancels, and the 5-digit rounding of an EES CSV export shifts the results by
   up to 1.4e-5 (viscosity).
5. **Independent computation** (scratch folders, deleted): Python
   transcriptions of the procedures (same tables, same polynomial, no
   CoolSolve code) give the same values as the model for the demonstration
   cases and the 5 properties of all 11 solutions, reproduce the six EES
   values of item 2 (≤ 3.6e-10) and the `T_freezing` of `CSL-0161` (5.9e-11).

## Source and attribution

Function library of the **Thermodynamics Laboratory of the University of Liège**
(Faculté des Sciences Appliquées), distributed with the EES setups of the
laboratory as compiled EES libraries loaded from the `USERLIB` folder
(`Brineprop.lib`, `Brineprop2.LIB`, help files `BRINEPROP.hlp` and
`BrineProp2.chm`, coefficient tables `Brine1.lkt` / `Brine2.lkt`). No personal
author is named in the library: the EES help file credits the 1997 edition of
the library and refers to IIR thermo-physical data, and the inventory of
S. Quoilin's collection attributes it to the laboratory (J. Lebrun et al.);
the author is therefore left `TBD` for the maintainer. The lab disclaimer of
the collection (freely distributed, may not be sold, cite the origin) applies.

Source files (compiled EES libraries, Windows-1252, the equation text is plain
text inside the binary), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/AHU_Components/Recovery_Systems/GLYCOLRECOVERYLOOP_REFSIM_EES_MODEL_SB080116.zip!/UserLib/BrineProp/Brineprop.lib`
(EES 7.793, inventory candidate `TM-0479`) with the tables `Brine1.lkt` and
`Brine2.lkt` (EES 4.631) of the same folder, and the EES 9.513 edition of
`Brineprop2.LIB`, `~/Nextcloud/thermo_models/Brineprop2.LIB`; the sibling
`Brineprop2.LIB` of the archive above (EES 7.793, 2006, inventory candidate
`TM-0480`) is its earlier edition, without the `UpperCase$` of the solution
name. Other copies of `Brineprop.lib` in the collection (those that the
`CSL-0072` and `CSL-0078` files carried) differ only in the wording of the
range-check messages and in the number of surplus `ENDIF`s.

## Conversion log

- **2026-10-05 — import** (`T-FUNC`, roadmap card C-84): the `.lib` is a
  *compiled* EES library, not plain text; its equation text was recovered from
  the binary (Windows-1252, NUL bytes and the compiled code section removed),
  the `{$DS.}`-like stamp `$SB1-X7.793` was dropped. Unit system already
  SI-°C-Pa-J on mass basis → **no unit conversion**. The procedure was copied
  unchanged except for the dead code that followed `END` and for its string
  array of unit labels, shipped as a lookup table `Units` (both superseded by
  the rewrite of 2026-11-05).
- **2026-10-05 — demonstration program**: written after the procedure
  definition (workflow §4), in the pattern of the example block of the
  library: case 1 is that example (PG, 50 %, `T_g_avg`), case 2 is the state
  stored by the glycol run-around loop model of the same library (EG, 25 %,
  6.324036551 °C) so that the verification has an EES reference. Two
  conversions are written explicitly for the comparison with that stored
  solution (`c_p_brine_2 = c_p_brine_2_kJ*1000`, `mu_brine_2 =
  mu_brine_2_mPa_s/1000`), which is how the glycol model itself calls the
  library (`… : c_p_gw/1000`, `… : mu_gw*1000`).
- **2026-10-05 — `T_g_avg` = 65**: the example block of the library writes
  `T_g_avg=65 [K]`, but the temperature argument of `BRINEPROP` is in degrees
  Celsius (the help file: *"temperature in °C"*; the coefficient tables are
  centred on °C, see `T_mean`). 65 K = −208.15 °C is below the freezing point
  of every one of the eleven solutions (the highest freezing point the
  correlation returns over the whole validity domain is 0.03 °C), so the
  demonstration uses `T_brine_1 = 65 [C]` and says so in a comment.
- **2026-10-05 — lookup tables**: decoded by hand from the binary `.lkt` files
  (see *Verification* item 4) and shipped as companion CSVs.
- **Level 2** although the raw score is 4 (440 equations when the ten
  demonstration calls are flattened, largest block 1, procedure present,
  semi-empirical correlation): the equation count comes entirely from the ten
  repetitions of the same 18-term polynomial, not from model depth — the
  library routine itself is one polynomial and two table reads. Kept in line
  with the inventory guess and with the level-2 function library `CSL-0005`
  (`cpbar_combustion_products`).
- **2026-11-05 — `BRINEPROP2` added and the library rewritten** (`TM-0480`,
  `merged` into this model since its triage; maintainer request: one library,
  as simple and correct as possible for the user, not bound to the original
  formulation). The EES text of the two procedures repeated the same work
  (22 range checks, an 11-branch solution ladder, the coefficient loop and the
  polynomial, written twice), carried surplus `ENDIF`s that EES ignores and
  CoolSolve reports in every model that includes the library (`P008`), mixed
  up the limits in its error messages (*"smaller than 60.1 %. Try setting the lower
  limit"*), reused the loop counter `Pr` for the Prandtl number in
  `BRINEPROP2`, and needed a string array of unit labels that fed no equation.
  The model now has:
  - one function `BrineProperty(Prop$, Fl$, Conc, Temp)`, in SI units, that
    does the work once: the solution is a row of the table `BrineSolutions`
    (code, name, concentration range and the mean values of the old table
    `Brine2`), found with `LOOKUP$ROW`; the coefficients are the table
    `BrineCoefficients` (the old `Brine1`, its columns named after the
    properties); one `CALL ERROR` per check, with the value in the message;
  - `BRINEPROP` and `BRINEPROP2` as wrappers of it, with the signatures and
    the output units of the EES library (specific heat in kJ/kg·K, viscosity
    in milliPa·s and Pa·s), so that the EES models that call them only need
    the `$INCLUDE` line;
  - the tables `Brine1`, `Brine2` and `Units` replaced by `BrineSolutions` and
    `BrineCoefficients` (same values); the models that carried their own copy
    of `BRINEPROP` and of the tables (`CSL-0072`, two files, and `CSL-0078`)
    include this model instead.

  Demonstration cases 3 and 4 (`BRINEPROP2`) and 5 (`BrineProperty`) are
  added. The results do not change (*Verification* item 3); the `.sol` is
  regenerated for the new variables (cases 1 and 2 move by at most 2.2e-10
  from the baseline of 2026-10-18, a tighter solver convergence:
  `c_p_brine_2` now agrees with EES to 7.9e-13 instead of 2.2e-10). The level
  stays 2.

## CoolProp incompressible solutions: the alternative for new models

CoolProp's incompressible library carries the **same eleven aqueous
solutions, from the same source**: the `M…` fluids of CoolProp are the
correlations of Å. Melinder for the IIR (*Properties of Secondary Working
Fluids for Indirect Systems*, 2010), with the same 18-term polynomial in the
deviations from a mean concentration and temperature, the same five
properties and the logarithm of the viscosity (CoolProp,
`dev/incompressible_liquids/CPIncomp/MelinderFluids.py`). The coefficients and
the mean values differ from those of BrineProp, which is most likely an
earlier edition of the same IIR correlations (its help file credits the 1997
edition and IIR data). A new model can use them **with the standard property
functions, no `$INCLUDE` and no table**: the concentration in mass % as the
second argument (or `C=`), the temperature alone (the EES form, evaluated at
101325 Pa) or with a pressure, results in SI units.

```
rho  = density(EG, 30, T=T)        "kg/m^3"
c_p  = cp(EG, 30, T=T)             "J/kg-K"
k    = conductivity(EG, 30, T=T)   "W/m-K"
mu   = viscosity(EG, 30, T=T)      "Pa-s"
Pr   = prandtl(EG, 30, T=T)        "-"
```

| BrineProp | CoolProp | CoolSolve name | CoolProp range |
|---|---|---|---|
| `EG` | `MEG` | `EG`, `EthyleneGlycol`, `MEG` | 0–60 % |
| `PG` | `MPG` | `PG`, `PropyleneGlycol`, `MPG` | 0–60 % |
| `EA` | `MEA` | `EthanolSolution`, `MEA` | 0–60 % |
| `MA` | `MMA` | `Methanol`, `MMA` | 0–60 % |
| `GL` | `MGL` | `Glycerol`, `MGL` | 0–60 % |
| `CaCl2` | `MCA` | `CaCl2`, `MCA` | 0–30 % |
| `NaCl` | `MNA` | `NaCl`, `MNA` | 0–23 % |
| `NH3` | `MAM` | — (not registered) | 0–30 % |
| `K2CO3` | `MKC` | — (not registered) | 0–40 % |
| `MgCl2` | `MMG` | — (not registered) | 0–30 % |
| `KAc` | `MKA` | — (not registered) | 0–45 % |

**Agreement** (2026-11-05, scratch comparison, deleted: the BrineProp
polynomial of this model against the Melinder 2010 polynomial of CoolProp,
whose evaluation was first checked against CoolSolve's CoolProp calls to
2.8e-7; 5 concentrations over the range common to both × 8 temperatures from
2 K above the freezing point to 40 °C, 30 °C for ammonia):

- at typical operating points (the middle of the concentration range, 0 to
  20 °C) the two agree within 0.25 % on the density, 0.45 % on the
  conductivity, 0.65 % on the specific heat (2.5 % for `PG`, 1.3 % for `MA`)
  and 2.6 % on the viscosity (6.6 % for `NH3`); over the whole concentration
  range the freezing points agree within 0.08 K (`EG`) to 1.8 K (`PG`);
- at the edges of the range, where one of the two fits extrapolates, the
  deviations grow: up to 16 % on the specific heat (`EA` at 60 % and −43 °C,
  `MA` 10 %, `PG` 4 %, the others below 1 %) and up to 20–33 % on the
  viscosity (`MA`, `EA` at their lowest concentration and 40 °C, `MgCl2`
  near its freezing point), 2–13 % for the other solutions;
- at the three EES stored points of ethylene glycol used in this model and in
  `CSL-0072` (EG 25 % at 6.3 °C and 25 °C, EG 30 % at −5 °C), CoolProp gives a
  density lower by 0.05–0.08 %, a specific heat lower by 0.5–0.8 %, a
  conductivity lower by 0.1 % and a viscosity lower by 0.2–1.0 % than EES and
  BrineProp, and the freezing point within 0.02 K. A model that switches to
  CoolProp therefore no longer reproduces its EES stored solution exactly.

**Speed** (CoolSolve 0.4.0, `-d` profiling, `profiling.md`): on a small
model (50 temperatures of EG 30 %, one property each) a block evaluation
costs 0.022 ms with an arithmetic equation, 0.024 ms with
`density(EG, 30, T=T)` (the CoolProp call itself: 1.1 µs) and 0.091 ms with
`BrineProperty('Density', 'EG', 30, T)`: a CoolProp call costs about 2 µs, a
`BrineProperty` call about 70 µs (an interpreted function: a `LOOKUP$ROW`, 18
`LOOKUP`s and the polynomial with its derivatives), some 35 times more. In a
large model both are hidden today by a cost of CoolSolve itself that grows
with the size of the model (about 1 ms per block evaluation at 3200
variables, `CS-BUG-BLOCK-EVAL-SCALING` in the CoolSolve register).

**Behaviour**: CoolProp refuses a temperature below the freezing point of
the solution (an error naming the call), while the BrineProp polynomial
extrapolates silently. CoolSolve also accepts the concentration as an
unknown of the model with CoolProp (`rho = density(EG, C, T=20)` with
`rho = 1040` solves for `C`).

**What BrineProp is still needed for**:

1. the EES models of the collection that call `BRINEPROP` or `BRINEPROP2`
   (`CSL-0072`, `CSL-0074`, `CSL-0078`, `CSL-0116`, `CSL-0161`, `CSL-0162`,
   `CSL-0163`): with this library they reproduce their EES stored solutions;
2. the **freezing point**: CoolProp has it (`T_freeze` of an incompressible
   solution) but CoolSolve does not evaluate `FREEZINGPT` yet;
3. ammonia, potassium carbonate, magnesium chloride and potassium acetate:
   CoolProp has them (`MAM`, `MKC`, `MMG`, `MKA`) but CoolSolve does not
   register them yet (*Unknown fluid*).

For a new model on one of the seven registered solutions, the CoolProp
property functions are the simpler and faster choice.

## Limitations

Physics and accuracy: the correlations are those of the laboratory (1997), with
IIR thermo-physical data; they are empirical polynomials valid only inside the
concentration ranges of the table above, and no uncertainty is given. The
property is a function of concentration and temperature only — pressure has no
influence (the brines are treated as incompressible by the calling models).
The 11 solutions are not CoolProp fluids: no EES property call is involved.
The temperature is not checked: outside the range of the data of a solution
(above its boiling point, below its freezing point) the polynomial
extrapolates.

## Related models

- `CSL-0072` *centrifugal_brine_pump_refsim* — brine pump of the same model
  bank (density and specific heat of EG 25 %, `$INCLUDE` line in its two
  files); its EES reference values for EG 25 % at 25 °C
  (ρ = 1030.000008 kg/m³, c_p = 3852.099981 J/kg·K) are reproduced by the
  tables of this model to 2.9e-09 and 6.2e-09 relative.
- `CSL-0074` *cooling_coil_refsim* — cooling coil of the same model bank that
  calls `BRINEPROP` for the brine side (`$INCLUDE` line in its native file).
- `CSL-0078` *brine_to_water_heat_pump_refsim* — brine evaporator of the same
  model bank; density and specific heat of a 25 % propylene glycol solution
  (`$INCLUDE` line in its native file).
- `CSL-0087` *internal_turbulent_nusselt*: the other translated function
  library (from `ht`), the third kind of function library of the library next to
  this one and `CSL-0005`.
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.
- `CSL-0113` *condenser_3_zones_plate_correlations*: plate condenser whose
  `prop_htf` procedure carries a glycol polynomial for the secondary fluid;
  this library is the more complete property source for the same fluids.
- `CSL-0114` *evaporator_3_zones_plate_correlations*: three-zone plate evaporator whose `prop_htf` procedure carries the same glycol polynomial for the secondary fluid.
- `CSL-0116` *heat_pump_vitocal_300g*: brine-to-water heat pump whose
  evaporator calls `BRINEPROP2` for EG 30 % at −5 °C (`$INCLUDE` line in its
  native file); its EES stored solution is the reference of `BRINEPROP2`
  (demonstration case 3).
- `CSL-0121` *heat_transfer_fluid_properties*: companion function library for the pure
  heat-transfer fluids (monoethylene glycol, Therminol VP-1/66, thermal oil); the two
  libraries cover the secondary fluids of the library between them.
- `CSL-0161` *plate_hx_thermal_resistances*: single-phase plate heat exchanger
  (Martin) whose native file calls `BRINEPROP2` on its ethylene-glycol branch
  (`$INCLUDE` line); its stored run is the water branch.
- `CSL-0162` *glycol_runaround_recovery_loop*: model of the same model bank
  calling `BRINEPROP` the same way ('SPECHEAT'/'DENSITY'/'DYNVISC' on EG 25 %;
  `$INCLUDE` line in its native file).
- `CSL-0163` *cooling_coil_paramid*: calls this library's `BRINEPROP`
  procedure for the ethylene-glycol properties of the identified coil
  (`$INCLUDE` line in its native file).
