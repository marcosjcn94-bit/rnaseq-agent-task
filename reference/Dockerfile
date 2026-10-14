# Keep the reference image aligned with the checked-in package lock.
FROM bioconductor/bioconductor_docker:RELEASE_3_22@sha256:e34177896c1579f66d48b756e4229b58237499183a089da084af72d7aba1d40a
COPY packages.lock.csv /tmp/packages.lock.csv
RUN Rscript -e 'options(repos = c(CRAN = "https://p3m.dev/cran/2026-10-07")); options(BioC_mirror = "https://p3m.dev/bioconductor/2026-04-09"); BiocManager::install(c("airway", "DESeq2"), ask=FALSE, update=FALSE, Ncpus=2)'
RUN Rscript -e 'lock <- read.csv("/tmp/packages.lock.csv"); current <- installed.packages(); stopifnot(all(lock$Package %in% rownames(current)), all(current[lock$Package, "Version"] == lock$Version))'
WORKDIR /work