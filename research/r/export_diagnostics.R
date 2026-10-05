suppressPackageStartupMessages(library(DESeq2))
suppressPackageStartupMessages(library(jsonlite))
suppressPackageStartupMessages(library(digest))
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args) == 3L)
input <- args[[1]]; config_path <- args[[2]]; output <- args[[3]]
if (dir.exists(output) && length(list.files(output, all.files=TRUE, no..=TRUE)) > 0L) stop("output directory must be empty")
config <- fromJSON(config_path, simplifyVector=TRUE)
counts <- read.csv(file.path(input, "counts.csv"), row.names=1, check.names=FALSE)
metadata <- read.csv(file.path(input, "metadata.csv"), stringsAsFactors=FALSE)
stopifnot(!anyDuplicated(rownames(counts)), !anyDuplicated(colnames(counts)),
          !anyDuplicated(metadata$sample_id), setequal(colnames(counts), metadata$sample_id),
          all(is.finite(as.matrix(counts))), all(as.matrix(counts) >= 0),
          all(as.matrix(counts) == floor(as.matrix(counts))))
counts <- counts[order(rownames(counts)), , drop=FALSE]
metadata <- metadata[match(colnames(counts), metadata$sample_id), , drop=FALSE]
rownames(metadata) <- metadata$sample_id
metadata$donor <- factor(metadata$donor, levels=sort(unique(metadata$donor)))
metadata$condition <- factor(metadata$condition, levels=c("control", "treated"))
stopifnot(all(table(metadata$donor, metadata$condition) == 1L))
keep <- rowSums(counts >= config$min_count) >= config$min_samples
counts <- as.matrix(counts[keep, , drop=FALSE]); storage.mode(counts) <- "integer"
dds <- DESeqDataSetFromMatrix(countData=counts, colData=metadata, design=as.formula(config$design))
started <- proc.time()[["elapsed"]]
captured_warnings <- character()
capture_warning <- function(w) {
  captured_warnings <<- unique(c(captured_warnings, conditionMessage(w)))
  invokeRestart("muffleWarning")
}
dds <- withCallingHandlers(DESeq(dds, fitType=config$fit_type, sfType=config$size_factors_fit_type,
             minReplicatesForReplace=config$min_replicates, parallel=FALSE, quiet=TRUE), warning=capture_warning)
res <- withCallingHandlers(results(dds, contrast=config$contrast, alpha=config$alpha,
               independentFiltering=config$independent_filter,
               cooksCutoff=config$cooks_filter), warning=capture_warning)
dir.create(output, recursive=TRUE, showWarnings=FALSE)
result_table <- data.frame(gene_id=rownames(res), as.data.frame(res), check.names=FALSE)
write.csv(result_table, file.path(output, "results.csv"), row.names=FALSE, na="")
write.csv(data.frame(gene_id=rownames(dds), counts(dds, normalized=TRUE), check.names=FALSE),
          file.path(output, "normalized_counts.csv"), row.names=FALSE, na="")
gene <- as.data.frame(mcols(dds))
gene$gene_id <- rownames(dds)
cooks <- assays(dds)[["cooks"]]
if (!is.null(cooks)) {
  colnames(cooks) <- paste0("cooks::", colnames(dds))
  gene <- cbind(gene, as.data.frame(cooks, check.names=FALSE))
}
write.csv(gene, file.path(output, "gene_diagnostics.csv"), row.names=FALSE, na="")
sf <- data.frame(sample_id=names(sizeFactors(dds)), size_factor=unname(sizeFactors(dds)))
write.csv(sf, file.path(output, "size_factors.csv"), row.names=FALSE, na="")
result_meta <- S4Vectors::metadata(res)
filter_threshold <- result_meta$filterThreshold
info <- list(
  stage="E2", design=config$design, contrast=as.list(config$contrast),
  warnings=as.list(captured_warnings),
  alpha=config$alpha, independent_filter=config$independent_filter,
  cooks_filter=config$cooks_filter, input_genes=nrow(read.csv(file.path(input,"counts.csv"),row.names=1,check.names=FALSE)),
  tested_genes=nrow(dds), significant=sum(res$padj < config$alpha, na.rm=TRUE),
  design_rank=qr(model.matrix(design(dds), colData(dds)))$rank,
  residual_degrees_of_freedom=nrow(colData(dds))-qr(model.matrix(design(dds),colData(dds)))$rank,
  size_factors=as.list(sizeFactors(dds)),
  dispersion_function=as.list(attr(dispersionFunction(dds), "coefficients")),
  dispersion_function_type=attr(dispersionFunction(dds), "fitType"),
  independent_filter_threshold=if(length(filter_threshold)) unname(filter_threshold[[1]]) else NULL,
  elapsed_seconds=proc.time()[["elapsed"]]-started,
  versions=list(R=R.version.string, DESeq2=as.character(packageVersion("DESeq2")),
                Bioconductor=as.character(BiocManager::version())),
  input_sha256=list(counts=digest(file=file.path(input,"counts.csv"),algo="sha256"),
                    metadata=digest(file=file.path(input,"metadata.csv"),algo="sha256")),
  config_sha256=digest(file=config_path,algo="sha256"),
  code_sha256=digest(file=normalizePath(file.path(dirname(config_path),"../r/export_diagnostics.R")),algo="sha256"),
  image_id=Sys.getenv("AIRWAY_IMAGE_ID", unset="not_provided"),
  peak_memory_bytes=as.numeric(gsub("[^0-9]", "", grep("VmHWM:", readLines("/proc/self/status"), value=TRUE))) * 1024,
  output_sha256=list(
    results=digest(file=file.path(output,"results.csv"),algo="sha256"),
    normalized_counts=digest(file=file.path(output,"normalized_counts.csv"),algo="sha256"),
    gene_diagnostics=digest(file=file.path(output,"gene_diagnostics.csv"),algo="sha256"),
    size_factors=digest(file=file.path(output,"size_factors.csv"),algo="sha256")
  ),
  status="complete"
)
write_json(info, file.path(output, "manifest.json"), pretty=TRUE, auto_unbox=TRUE, na="null")
cat("R diagnostic export completed:", nrow(dds), "genes;", sum(res$padj < config$alpha, na.rm=TRUE), "significant\n")
