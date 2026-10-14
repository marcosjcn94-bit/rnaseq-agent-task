# Keep this install on the same package snapshots as the locked reference image.
FROM rnaseq-reference:dev
ARG BIOC_VERSION=3.22
RUN Rscript -e "stopifnot(as.character(BiocManager::version()) == '${BIOC_VERSION}'); options(repos = c(CRAN = 'https://p3m.dev/cran/2026-10-07')); options(BioC_mirror = 'https://p3m.dev/bioconductor/2026-04-09'); BiocManager::install(c('limma','edgeR','goseq','AnnotationDbi','org.Hs.eg.db','apeglm','affy'), ask=FALSE, update=FALSE, version='${BIOC_VERSION}')" \
    && Rscript -e "p <- installed.packages(); write.csv(data.frame(Package=rownames(p),Version=p[, 'Version']), '/tmp/research-packages.csv', row.names=FALSE)"
COPY research/r-packages.lock.csv /tmp/research-packages.lock.csv
RUN Rscript -e "expected <- read.csv('/tmp/research-packages.lock.csv'); actual <- installed.packages(); actual <- data.frame(Package=rownames(actual), Version=actual[, 'Version']); expected <- expected[order(expected[['Package']]), ]; actual <- actual[order(actual[['Package']]), ]; rownames(expected) <- NULL; rownames(actual) <- NULL; stopifnot(identical(expected, actual))"
WORKDIR /research
CMD ["Rscript", "-e", "stopifnot(as.character(BiocManager::version()) == '3.22', as.character(packageVersion('DESeq2')) == '1.50.2')"]