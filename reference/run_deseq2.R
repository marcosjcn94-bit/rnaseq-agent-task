suppressPackageStartupMessages(library(DESeq2))
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==3)
input <- args[1]; out <- args[2]; config <- jsonlite::read_json(args[3],simplifyVector=TRUE)
if (dir.exists(out) && length(list.files(out,all.files=TRUE,no..=TRUE))>0) stop("output directory must be empty")
counts <- read.csv(file.path(input,"counts.csv"),row.names=1,check.names=FALSE)
meta <- read.csv(file.path(input,"metadata.csv"),stringsAsFactors=FALSE)
stopifnot(ncol(counts)==8L, all(counts>=0), all(as.matrix(counts)==floor(as.matrix(counts))),
 !anyDuplicated(rownames(counts)),!anyDuplicated(meta$sample_id),
 setequal(colnames(counts),meta$sample_id))
counts <- counts[order(rownames(counts)),sort(colnames(counts))]
meta <- meta[match(colnames(counts),meta$sample_id),]
rownames(meta) <- meta$sample_id
meta$donor <- factor(meta$donor,levels=sort(unique(meta$donor)))
meta$condition <- factor(meta$condition,levels=c("control","treated"))
stopifnot(all(table(meta$donor,meta$condition)==1L))
keep <- rowSums(counts>=config$min_count)>=config$min_samples
stopifnot(any(keep))
counts <- as.matrix(counts[keep,,drop=FALSE])
storage.mode(counts) <- "integer"
dds <- DESeqDataSetFromMatrix(countData=counts,colData=meta,design=as.formula(config$design))
started <- proc.time()[["elapsed"]]
dds <- DESeq(dds,fitType=config$fit_type,sfType=config$size_factors_fit_type,
 minReplicatesForReplace=config$min_replicates,parallel=FALSE,quiet=TRUE)
res <- results(dds,contrast=config$contrast,alpha=config$alpha,
 independentFiltering=config$independent_filter,cooksCutoff=config$cooks_filter)
dir.create(out,recursive=TRUE,showWarnings=FALSE)
write.csv(data.frame(gene_id=rownames(res),as.data.frame(res),check.names=FALSE),
 file.path(out,"differential_expression.csv"),row.names=FALSE,na="")
write.csv(data.frame(gene_id=rownames(dds),counts(dds,normalized=TRUE),check.names=FALSE),
 file.path(out,"normalized_counts.csv"),row.names=FALSE)
packages <- as.data.frame(installed.packages()[,c("Package","Version")])
write.csv(packages,file.path(out,"packages.csv"),row.names=FALSE)
jsonlite::write_json(list(design=config$design,contrast=config$contrast,parameters=config,
 input_hashes=list(counts=digest::digest(file=file.path(input,"counts.csv"),algo="sha256"),metadata=digest::digest(file=file.path(input,"metadata.csv"),algo="sha256")),
 config_hash=digest::digest(file=args[3],algo="sha256"),
 result_hash=digest::digest(file=file.path(out,"differential_expression.csv"),algo="sha256"),
 docker_image_id=Sys.getenv("RNASEQ_IMAGE_ID"),
 genes_input=length(keep),genes_tested=sum(keep),significant=sum(res$padj<.05,na.rm=TRUE),
 elapsed_seconds=proc.time()[["elapsed"]]-started,
 DESeq2_version=as.character(packageVersion("DESeq2")),R_version=R.version.string,
 size_factors=as.list(sizeFactors(dds)),
 effective_fit=attr(dispersionFunction(dds),"fitType")),
 file.path(out,"manifest.json"),pretty=TRUE,auto_unbox=TRUE,na="null")
capture.output(sessionInfo(),file=file.path(out,"sessionInfo.txt"))
cat("R reference completed:",sum(keep),"genes\n")
