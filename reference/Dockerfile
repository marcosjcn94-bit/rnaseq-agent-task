FROM bioconductor/bioconductor_docker:RELEASE_3_22@sha256:e34177896c1579f66d48b756e4229b58237499183a089da084af72d7aba1d40a
RUN Rscript -e 'BiocManager::install(c("airway", "DESeq2"), ask=FALSE, update=FALSE, Ncpus=2)'
RUN Rscript -e 'lock <- installed.packages()[, c("Package", "Version")]; write.csv(lock, "/tmp/packages.lock.csv", row.names = FALSE, quote = FALSE)'
RUN Rscript -e 'lock <- read.csv("/tmp/packages.lock.csv", stringsAsFactors = FALSE); current <- installed.packages(); stopifnot(all(lock$Package %in% rownames(current)), all(current[lock$Package, "Version"] == lock$Version))'
WORKDIR /work