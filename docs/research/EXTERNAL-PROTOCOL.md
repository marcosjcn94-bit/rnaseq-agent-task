# E5 — GSE13168 external dataset audit

Status is `insufficient_metadata`. Work stopped before inference.

## Frozen selection

The planned GPL96 contrast used three paired GFP basal/Flu comparisons (GSM332914/332925, GSM332915/332926, GSM332916/332927). The prespecified endpoints were log fold change (LFC) and 95% confidence intervals for CRISPLD2, DUSP1, and KLF15. Global concordance and CAMERA were exploratory. The comparison allowed different effect sizes and carried no novelty claim.

| Donor in record | Basal | Flu |
|---|---|---|
| 2 | GSM332914 | GSM332925 |
| 3 | GSM332915 | GSM332926 |
| 4 | GSM332916 | GSM332927 |

## Audit and decision

The audit downloaded the series SOFT and MINiML records and six CEL files from the GEO/NCBI FTP site. Hashes and the allowlisted extraction are in `.artifacts/research/E5/extracted/`. The records confirm the six GSM accessions, GPL96, and the pairs identified by `donorN` in the titles. The protocols describe pretreatment with 10 nM fluticasone for 30 minutes and collection after 8 hours of stimulation. The selected sample records, including their “basal” and “Flu” titles, leave the exact stimulus or cytokine assignment unresolved.

The pre-inference decision was `insufficient_metadata`. The intended comparison could combine different stimuli, so model fitting stopped. The CEL files were retained without RMA processing. The RMA image was built in preparation. The design differs from AIRWAY, which used 1 µM dexamethasone for 18 hours and RNA-seq.

The numerical donor identifier supports pairing within GSE13168. The relationship between these anonymized donors and the AIRWAY cohort remains `unknown`.

Primary sources are [GEO GSE13168](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE13168) and [Himes et al. (2014)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0099625). Before revising the contrast, obtain a sample-level table that resolves stimulus and treatment or select a cohort with complete metadata.
