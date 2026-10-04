FROM bioconductor/bioconductor_docker:RELEASE_3_22@sha256:e34177896c1579f66d48b756e4229b58237499183a089da084af72d7aba1d40a
RUN Rscript -e 'BiocManager::install(c("airway", "DESeq2"), ask=FALSE, update=FALSE, Ncpus=2)'
COPY packages.lock.csv /tmp/packages.lock.csv
RUN Rscript -e 'lock <- read.csv("/tmp/packages.lock.csv"); current <- installed.packages(); stopifnot(all(lock$Package %in% rownames(current)), all(current[lock$Package, "Version"] == lock$Version))'
WORKDIR /work
