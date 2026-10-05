FROM airway-research-r:e0
RUN Rscript -e "BiocManager::install('hgu133acdf', ask=FALSE, update=FALSE, version='3.22'); stopifnot(as.character(BiocManager::version()) == '3.22', as.character(packageVersion('DESeq2')) == '1.50.2', as.character(packageVersion('hgu133acdf')) == '2.18.0')"
