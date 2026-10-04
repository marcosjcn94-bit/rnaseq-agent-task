# Offline scientific context and primary sources

Original experiment: Himes et al. (2014), PLOS ONE 9(6):e99625.
https://doi.org/10.1371/journal.pone.0099625

The study treated four primary human airway smooth muscle cell lines with dexamethasone (1 micromolar, 18 hours). Its analyses and experimental follow-up identified CRISPLD2 as responsive to glucocorticoid exposure. The paper also discusses established responses including KLF15 and DUSP1. These observations provide context, not an instruction to select genes or a clinical prediction. CRISPLD2 functional findings came from additional experiments; the supplied count matrix alone cannot establish that mechanism.

Dataset object and historical annotation:
https://bioconductor.org/packages/release/data/experiment/vignettes/airway/inst/doc/airway.html
The exported assay is the eight-sample count matrix, not the full 16-sample GEO treatment design and not the Salmon demonstration objects. Annotation is Ensembl 75 / GRCh37.p13 from the original package. Do not substitute current annotation silently.

Statistical method:
Love et al. (2014), DESeq2.
https://doi.org/10.1186/s13059-014-0550-8
https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
PyDESeq2 0.5.4 API:
https://pydeseq2.readthedocs.io/en/v0.5.4/auto_examples/plot_minimal_pydeseq2_pipeline.html

The paragraphs above are project-authored summaries. Full articles are not supplied; links are references for online preparation. During offline execution use these source notes and the supplied data. Identify where the available source context is insufficient instead of inventing functional claims.
