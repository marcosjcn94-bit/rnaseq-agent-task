suppressPackageStartupMessages(library(airway))
suppressPackageStartupMessages(library(SummarizedExperiment))
args <- commandArgs(trailingOnly=TRUE)
out <- if (length(args)) args[1] else "/out"
dir.create(out, recursive=TRUE, showWarnings=FALSE)
data("airway", package="airway")
expected <- c("SRR1039508","SRR1039509","SRR1039512","SRR1039513","SRR1039516","SRR1039517","SRR1039520","SRR1039521")
stopifnot(identical(colnames(airway), expected), ncol(airway)==8L)
raw <- assay(airway)
md <- as.data.frame(colData(airway))
stopifnot(all(md$albut=="untrt"), length(unique(md$cell))==4L, all(raw>=0), all(raw==floor(raw)))
metadata <- data.frame(sample_id=colnames(raw), donor=as.character(md$cell),
 condition=ifelse(md$dex=="trt","treated","control"))
stopifnot(all(table(metadata$donor,metadata$condition)==1L))
write.csv(data.frame(gene_id=rownames(raw),raw,check.names=FALSE),
 file.path(out,"counts.csv"),row.names=FALSE,quote=FALSE)
write.csv(metadata,file.path(out,"metadata.csv"),row.names=FALSE,quote=FALSE)
rd <- as.data.frame(rowData(airway))
symbol_field <- if ("gene_name" %in% names(rd)) "gene_name" else if ("symbol" %in% names(rd)) "symbol" else NULL
symbols <- if (is.null(symbol_field)) rep(NA_character_, nrow(raw)) else as.character(rd[[symbol_field]])
write.csv(data.frame(gene_id=rownames(raw),symbol=symbols),file.path(out,"annotation.csv"),row.names=FALSE)
sources <- c("https://bioconductor.org/packages/airway",
 "https://bioconductor.org/packages/release/data/experiment/vignettes/airway/inst/doc/airway.html",
 "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52778")
files <- lapply(c("counts.csv","metadata.csv","annotation.csv"),function(name) {
 path <- file.path(out,name)
 list(path=name, bytes=unname(file.info(path)$size),sha256=digest::digest(file=path,algo="sha256"))
})
names(files) <- c("counts.csv","metadata.csv","annotation.csv")
manifest <- list(schema_version=1, acquired_at=format(Sys.time(),tz="UTC",usetz=TRUE),
 source="Bioconductor airway object, assay counts", count_type="raw_fragment_counts",
 dataset="GSE52778", subset="4 donors x control/treated; no albuterol",
 genes=nrow(raw), samples=ncol(raw), sample_ids=expected, urls=sources,
 airway_version=as.character(packageVersion("airway")),
 r_version=R.version.string, bioconductor_version=as.character(BiocManager::version()),
 annotation=metadata(rowRanges(airway)), files=files,
 mapping=list(donor="cell",condition=list(untrt="control",trt="treated")),
 package_license=packageDescription("airway")$License)
jsonlite::write_json(manifest,file.path(out,"manifest.json"),pretty=TRUE,auto_unbox=TRUE,na="null")
capture.output(sessionInfo(),file=file.path(out,"acquisition_session.txt"))
cat("Exported",nrow(raw),"genes and",ncol(raw),"samples\n")
