FROM bioconductor/bioconductor_docker:RELEASE_3_22
RUN Rscript -e 'BiocManager::install(c("airway", "DESeq2"), ask=FALSE, update=FALSE, Ncpus=2)'
WORKDIR /work
