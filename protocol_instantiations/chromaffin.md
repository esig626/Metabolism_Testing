# Source-Grounded Protocol Instantiation: SDH-b Chromaffin Study

## Source and citation convention

The source is Vera-Sigüenza et al., *A Mathematical Exploration of SDH-b Loss
in Chromaffin Cells*, *Bulletin of Mathematical Biology* 87:53 (2025), supplied
as `sources/pdfs/sdhb_chromaffin_2025.pdf` (`CHR`). Citations use PDF page
numbers, which the article itself labels “Page X of 36.” The recurring “53” is
the article number, not a page number. Supplementary files referenced in the
article are not included in the supplied PDF.

This record does not infer independence from the presence of multiple clones or
from a mean curve. Cells, metabolites, fragments, isotopologues, ions, and fitted
fluxes are not biological replicates.

## Biological classes and contrasts

| Field | Source-grounded instantiation |
|---|---|
| Cell identity | Previously characterised immortalised mouse chromaffin cells (imCC). `[CHR p. 3, Introduction and §2.1]` |
| Principal biological contrast | Wild type, reported as SDH-b+/+, versus SDH-b-deficient/knockout, reported as SDH-b−/− or K.O. `[CHR p. 3, §2.1; p. 15, §4]` |
| Knockout clones | SDH-b−/− clones CL6 and CL8 are named; the manuscript refers generically to their SDH-b+/+ counterparts without naming WT clones. Whether CL6 and CL8 were analysed separately, pooled, averaged, or used in every tracing assay is **UNKNOWN — NOT REPORTED**. `[CHR p. 3, §2.1]` |
| Tracer/control contrast | Glucose and glutamine supplied in unlabelled form or as ^13C6-glucose and ^13C5-glutamine. The experimental results and MFA explicitly compare WT and K.O. after uniformly labelled ^13C6-glucose. `[CHR p. 4, §2.4; pp. 15–18, §4 and Figures 6–7]` |
| Tracer-arm layout | Whether glucose and glutamine tracers were separate arms, simultaneous dual-labelled conditions, or another arrangement is **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.4]` |
| Other experimental perturbations | No wet-lab drug or environmental perturbation is reported for these tracing cultures. The 30% oxygen-flux reduction is a model simulation, not an experimental culture condition. `[CHR p. 21, Figure 10]` |
| Unreported identity fields | **UNKNOWN — NOT REPORTED:** parental WT line identity; number of WT clones; exact clone-to-condition assignment; passage; authentication; mycoplasma status. `[CHR p. 3, §2.1]` |

## Culture and exposure

| Field | Source-grounded instantiation |
|---|---|
| Architecture | Plated, well-based monocultures are implied by “each well,” confluence, aspiration, washing, and scraping. Plate format, well size, surface area, and culture volume are **UNKNOWN — NOT REPORTED**. No experimental co-culture or subcellular fractionation is reported. `[CHR pp. 3–4, §§2.3–2.4]` |
| Maintenance medium | DMEM with 10% FBS and 1 mM pyruvate; chemicals, DMEM, and FBS were from Sigma-Aldrich unless stated otherwise. `[CHR p. 3, §2.1]` |
| Tracing medium | 11 mM glucose and 2 mM glutamine supplied in unlabelled or labelled form. Whether this was a complete DMEM exchange, whether FBS was present or dialysed, and all other tracing-medium constituents are **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.4]` |
| Culture temperature and CO2 | **UNKNOWN — NOT REPORTED.** The reported −20°C chloroform, 45°C drying, and 60°C derivatisation temperatures are processing conditions, not culture-incubator conditions. `[CHR p. 4, §§2.4–2.5]` |
| Tracer identities and concentrations | ^13C6-glucose at 11 mM and ^13C5-glutamine at 2 mM; CK Isotopes. The Results explicitly call the ^13C6-glucose uniformly labelled but do not use that wording for ^13C5-glutamine. Isotopic enrichment/purity and catalogue numbers are **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.4; p. 15, §4]` |
| Seeding number | **UNKNOWN — NOT REPORTED** for tracing. The 1 × 10^6 trypsinised cells in §2.2 belong to the total-protein assay and are not a tracer seeding count. `[CHR p. 3, §2.2; p. 4, §2.4]` |
| Confluence target | Cells were plated to be 70% confluent after 48 h. Initial density, measured confluence, and assessment method are **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.4]` |
| Labelling duration | A terminal sample was collected after 48 h. Growth was also monitored over 48 h. Figures 8–9 describe enrichment “over time,” but the experimental sampling schedule behind those curves is **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.4; pp. 15–16, §4.1; pp. 19–20, §4.2 and Figures 8–9]` |

## Biological fractions and sample preparation

The source-grounded physical branching is:

`culture/well [WT or K.O.] → {100 µL spent-medium aliquot, cell-associated polar extract}`.

These are sibling fractions of a culture, not independent biological replicates.

| Stage | Source-grounded instantiation |
|---|---|
| Extracellular measurements | The section is headed “Glucose, Lactate and Sodium Measurements”; it says collected-supernatant levels were measured with a Contour XT glucometer, without an analyte-specific device/procedure mapping. Calibration and the sodium procedure are **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.3]` |
| Tracing harvest | After 48 h, 100 µL medium was removed for extraction/analysis. The next sentence reports pelleting cells “as described above,” but later sentences aspirate remaining medium and scrape cells from the wells; the referent and lineage of the pelleted material are therefore ambiguous. Speed, duration, rotor, and temperature are **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.4]` |
| Wash and quench | Empty wells were washed twice with ice-cold saline; 500 µL methanol was added; cells were scraped into a cold tube. The manuscript does not call this a quench and does not report delay-to-methanol or methanol temperature. `[CHR p. 4, §2.4]` |
| Biphasic extraction | Added 500 µL ice-cold water containing D6-glutaric acid at 1 µg/mL (CDN Isotopes D-5227), then 500 µL chloroform pre-chilled to −20°C; shook on ice for 15 min; centrifuged; transferred the polar phase; dried by centrifugation at 45°C. `[CHR p. 4, §2.4]` |
| Medium extraction | Whether the 100 µL medium aliquot underwent the same biphasic extraction is **UNKNOWN — NOT REPORTED**. Phase-recovery volumes, centrifugation conditions, and storage are also **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.4]` |
| Auxiliary protein assay | 1 × 10^6 trypsinised cells were PBS-washed, lysed in 60 µL RIPA for 30 min, and cleared supernatant assayed by BCA. The paper does not establish that these were the same wells as the tracing assay. `[CHR p. 3, §2.2]` |
| Cell counting | Cells were suspended in 200 µL trypsin plus 400 µL PBS; 10 µL was loaded into a Fast Read 102 counting chamber; five grid squares and dilution factor 60 were used. `[CHR p. 3, §2.2]` |

## Derivatisation and GC-MS

### Derivatisation

The dried polar extracts were treated with 2% methoxamine in pyridine (40 µL,
or 20 µL for undefined “primary samples,” 1 h at 60°C), followed by
N-(tert-butyl-dimethylsilyl)-N-methyl-trifluoroacetamide with 1%
tert-butyldimethyl-chlorosilane (60 µL, or 30 µL for “primary samples,” 1 h at
60°C). Samples were transferred to glass vials. “Primary samples,” reaction-batch
structure, and sample order within a derivatisation batch are
**UNKNOWN — NOT REPORTED**.
`[CHR p. 4, §2.5]`

### Instrument and acquisition

| Field | Reported method |
|---|---|
| Platform | Agilent 8890 GC with Agilent 5977B MSD. `[CHR p. 4, §2.5]` |
| Injection | 1 µL, splitless; helium at 1 mL/min. `[CHR p. 4, §2.5]` |
| Oven program | 100°C for 1 min; ramp to 160°C at 10°C/min; to 200°C at 5°C/min; to 320°C at 10°C/min; hold 5 min. `[CHR p. 4, §2.5]` |
| Detection | Scan mode. Column, inlet temperature, ionisation mode, source/quadrupole temperatures, scan range, detector settings, and raw-file schema are **UNKNOWN — NOT REPORTED**. `[CHR p. 4, §2.5]` |
| LC workflows | No LC-MS or LC-QTOF workflow is reported in this manuscript. `[CHR pp. 3–5, §§2.1–2.7]` |

### Processing and normalisation

- MassHunter was used for real-time data-quality assessment, followed by `.CDF`
  conversion and in-house MATLAB analysis; GraphPad Prism 9 and MATLAB were
  used for graphs/statistics. `[CHR p. 4, §2.6]`
- Manual integration, integration boundaries, baseline/deconvolution rules,
  metabolite-identification criteria, retention matching, fragment selection,
  drift correction, and processing versions are **UNKNOWN — NOT REPORTED**.
  `[CHR p. 4, §2.6]`
- Total ion counts for each metabolite were normalised to D6-glutaric acid.
  `[CHR p. 4, §2.5]` This is abundance/internal-standard normalisation; it does
  not specify how a MID was corrected or closed.
- Cell-count normalisation of GC-MS metabolite abundances or MIDs and protein
  normalisation of tracing data are **UNKNOWN — NOT REPORTED**. Cell-number
  changes do enter the extracellular glucose/lactate rate calculation.
  `[CHR pp. 3–4, §2.2; p. 16, §4.1, Eq. 4]`
- Natural-abundance correction, derivative-atom correction, tracer-impurity
  correction, correction matrix, software/version, and correction ordering are
  **UNKNOWN — NOT REPORTED**. `[CHR pp. 4–5, §§2.5–2.7]`

## Measured metabolites and isotope observations

| Observation | Evidence boundary |
|---|---|
| Extracellular | Glucose, lactate, and sodium are named in the measurement section; glucose consumption and lactate production rates are used downstream. `[CHR p. 4, §2.3; pp. 15–16, §4.1 and Figure 5]` |
| Explicit ^13C6-glucose MID panel | Lactate, citrate, succinate, malate, fumarate, and aspartate; Figure 6 labels m+0, m+1, m+2, etc. and compares experimental and simulated MIDs for WT and K.O. `[CHR pp. 16–17, §4.1 and Figure 6]` |
| Enrichment curves | Pyruvate enrichment/model fit in Figure 8; citrate and fumarate enrichment/model fits in Figure 9. `[CHR pp. 19–20, §4.2 and Figures 8–9]` |
| Other measured metabolites | The paper says enrichment simulations were repeated for “all measured metabolites,” but the supplied PDF gives no further exhaustive list. `[CHR p. 21, §4.2]` |
| Raw ion counts | The article says metabolite concentrations were derived from raw ion counts and points to Supplementary Data. The supplementary files are not supplied, so availability, row structure, and provenance are **UNKNOWN — NOT REPORTED IN THE SUPPLIED SOURCE**. `[CHR p. 19, §4.2]` |
| Missing measurement definition | **UNKNOWN — NOT REPORTED:** exact ions and GC-MS fragments; formulas and derivative atom counts; carbon atom maps; complete isotopologue ranges; censoring/missing rules; replicate-level MID values. `[CHR pp. 4–5 and 15–20, analytical/MFA methods and results]` |

## Replication and QC

- Biological replicate count, technical injection count, separate-well count,
  experiment-day count, culture-batch count, preparation replicates, and pooling
  are **UNKNOWN — NOT REPORTED**. `[CHR pp. 3–5, methods; pp. 15–20,
  experimental integration]`
- Figure 8 calls its output a “mean enrichment curve” but gives no `n`, averaging
  unit, or independence statement. `[CHR p. 20, Figure 8]`
- CL6 and CL8 are named clones, not a reported replicate count. Their observation
  lineage is **UNKNOWN — NOT REPORTED**. `[CHR p. 3, §2.1]`
- Reported QC comprises MassHunter real-time data-quality analysis before `.CDF`
  conversion. The MFA stage reports sum-of-squared-residual assessment, parameter
  confidence intervals, and identifiability evaluation; these are downstream fit
  diagnostics, not instrument QC. `[CHR p. 4, §2.6; p. 17, Figure 6 and text]`
- Blanks, pooled QCs, calibration series, retention-index standards, carryover
  checks, drift checks, repeated injections, acceptance thresholds, and exclusion
  rules are **UNKNOWN — NOT REPORTED**. `[CHR pp. 4–5, §§2.5–2.7]`

## Downstream MFA and kinetic modelling

The study used ^13C-MFA in the MATLAB INCA routine to partially quantify and
parameterise metabolic fluxes from MS MIDs; Figure 7 presents WT and K.O.
central-carbon flux maps. Growth and extracellular glucose/lactate rates are
reported nearby, but the manuscript does not explicitly state that they constrained
the INCA fit. `[CHR p. 5, §2.7; pp. 15–18, §4 and Figures 5–7]`

The text notes that INCA supports steady-state and isotopically non-stationary MFA
but does not identify which mode was used. Exact MFA network, atom maps, fragment
definitions, bounds, error law, confidence level, multistart/convergence procedure,
and steady-state criterion are **UNKNOWN — NOT REPORTED**. `[CHR p. 5, §2.7;
p. 17, Figure 6 and text]`

A later kinetic stage sets normalised enrichment with Vmax initially equal to 1 and
uses MATLAB Levenberg–Marquardt optimisation to refine parameters from
enrichment, concentration, and MFA-flux information. This mathematical
normalisation is distinct from analytical internal-standard normalisation and from
MID unit-sum closure. `[CHR p. 19, §4.2]`

The MFA fluxes and kinetic-model states are downstream fitted quantities, not
primary observations.

## Defensible experimental hierarchy

`stage-specific batch (UNKNOWN — NOT REPORTED) → culture/well [WT or named K.O. clone] → physical sibling fraction {medium aliquot, cell-associated material} → fraction-to-analytical-path mapping (UNKNOWN — NOT REPORTED) → extraction/derivatisation → injection (repeat structure UNKNOWN — NOT REPORTED) → metabolite/derivative → GC-MS fragment (UNKNOWN — NOT REPORTED) → MID/isotopologue → raw ion counts/integrated area → joint culture-indexed profile → downstream MFA/kinetic fit`

The primary sampling unit cannot be identified precisely because clone assignment,
well replication, experiment days, and batch structure are
**UNKNOWN — NOT REPORTED**. The cell and medium fractions share a parent culture.
The physical branching is reported, but the source does not map the six-metabolite
MID panel to medium, cells, or both. Metabolites and
fragments are feature dimensions, MID components are compositionally coupled, ions
are measurement depth, and fitted fluxes are estimators; none supplies biological
replication. `[CHR pp. 3–5]`
