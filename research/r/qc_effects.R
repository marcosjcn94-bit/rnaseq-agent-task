suppressPackageStartupMessages(library(DESeq2))
suppressPackageStartupMessages(library(apeglm))
suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(jsonlite))
suppressPackageStartupMessages(library(digest))
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args) == 3L)
input <- args[[1]]; config_path <- args[[2]]; output <- args[[3]]
if (dir.exists(output) && length(list.files(output, all.files=TRUE, no..=TRUE)) > 0L) stop("output directory must be empty")
config <- fromJSON(config_path, simplifyVector=TRUE)
raw <- read.csv(file.path(input,"counts.csv"),row.names=1,check.names=FALSE)
metadata <- read.csv(file.path(input,"metadata.csv"),stringsAsFactors=FALSE)
stopifnot(!anyDuplicated(rownames(raw)),!anyDuplicated(colnames(raw)),
          !anyDuplicated(metadata$sample_id),setequal(colnames(raw),metadata$sample_id),
          all(is.finite(as.matrix(raw))),all(as.matrix(raw)>=0),all(as.matrix(raw)==floor(as.matrix(raw))))
raw <- raw[order(rownames(raw)),,drop=FALSE]
metadata <- metadata[match(colnames(raw),metadata$sample_id),,drop=FALSE]
rownames(metadata) <- metadata$sample_id
metadata$donor <- factor(metadata$donor,levels=sort(unique(metadata$donor)))
metadata$condition <- factor(metadata$condition,levels=c("control","treated"))
stopifnot(all(table(metadata$donor,metadata$condition)==1L))
keep <- rowSums(raw>=config$min_count)>=config$min_samples
counts <- as.matrix(raw[keep,,drop=FALSE]); storage.mode(counts) <- "integer"
base_info <- list()
captured_warnings <- character()
capture_warning <- function(w) {
  captured_warnings <<- unique(c(captured_warnings,conditionMessage(w)))
  invokeRestart("muffleWarning")
}
started <- proc.time()[["elapsed"]]
dds <- DESeqDataSetFromMatrix(countData=counts,colData=metadata,design=as.formula(config$design))
dds <- withCallingHandlers(DESeq(dds,fitType=config$fit_type,sfType=config$size_factors_fit_type,
                 minReplicatesForReplace=config$min_replicates,parallel=FALSE,quiet=TRUE),warning=capture_warning)
base_res <- results(dds,contrast=config$contrast,alpha=config$alpha,
                    independentFiltering=TRUE,cooksCutoff=TRUE)
base_table <- data.frame(gene_id=rownames(base_res),as.data.frame(base_res),check.names=FALSE)
coef_name <- resultsNames(dds)[grepl("condition_treated_vs_control",resultsNames(dds),fixed=TRUE)]
if(length(coef_name)!=1L) stop(paste("could not identify treated/control coefficient:",paste(resultsNames(dds),collapse=", ")))
shrunk <- lfcShrink(dds,coef=coef_name,type="apeglm",quiet=TRUE)
shrink_table <- data.frame(gene_id=rownames(shrunk),as.data.frame(shrunk),check.names=FALSE)
base_table$log2FoldChange_shrunk <- shrink_table$log2FoldChange[match(base_table$gene_id,shrink_table$gene_id)]
write.csv(base_table,file.path(tempdir(),"baseline-results.csv"),row.names=FALSE,na="")
rank_cor <- suppressWarnings(cor(abs(base_table$log2FoldChange),abs(base_table$log2FoldChange_shrunk),
                                 method="spearman",use="complete.obs"))

# VST is exploratory QC only; the inferential model above continues to use raw counts.
vsd <- vst(dds,blind=FALSE)
vst_matrix <- assay(vsd)
write.csv(data.frame(gene_id=rownames(vst_matrix),vst_matrix,check.names=FALSE),
          file.path(tempdir(),"vst.csv"),row.names=FALSE)
pca_base <- prcomp(t(log2(counts(dds,normalized=TRUE)+1)[order(matrixStats::rowVars(log2(counts(dds,normalized=TRUE)+1)),decreasing=TRUE)[seq_len(min(500,nrow(dds)))],]),center=TRUE,scale.=FALSE)
base_percent <- 100*pca_base$sdev^2/sum(pca_base$sdev^2)
base_pca <- data.frame(sample_id=rownames(pca_base$x),PC1=pca_base$x[,1],PC2=pca_base$x[,2],
                       PC1_percent=base_percent[1],PC2_percent=base_percent[2],
                       condition=metadata[rownames(pca_base$x),"condition"],donor=metadata[rownames(pca_base$x),"donor"],method="baseline_log2norm")
pca_vst <- prcomp(t(vst_matrix[order(matrixStats::rowVars(vst_matrix),decreasing=TRUE)[seq_len(min(500,nrow(vsd)))],]),center=TRUE,scale.=FALSE)
vst_percent <- 100*pca_vst$sdev^2/sum(pca_vst$sdev^2)
vst_pca <- data.frame(sample_id=rownames(pca_vst$x),PC1=pca_vst$x[,1],PC2=pca_vst$x[,2],
                      PC1_percent=vst_percent[1],PC2_percent=vst_percent[2],
                      condition=metadata[rownames(pca_vst$x),"condition"],donor=metadata[rownames(pca_vst$x),"donor"],method="vst_blind_false")
pca_data <- rbind(base_pca,vst_pca)
base_label <- sprintf("baseline_log2norm (PC1 %.1f%%, PC2 %.1f%%)",base_percent[1],base_percent[2])
vst_label <- sprintf("VST blind=FALSE (PC1 %.1f%%, PC2 %.1f%%)",vst_percent[1],vst_percent[2])
pca_data$method <- factor(pca_data$method,levels=c("baseline_log2norm","vst_blind_false"),labels=c(base_label,vst_label))
dist_matrix <- as.matrix(dist(t(vst_matrix)))
dist_data <- data.frame(sample_id=rep(rownames(dist_matrix),times=ncol(dist_matrix)),
                        sample_id_2=rep(colnames(dist_matrix),each=nrow(dist_matrix)),
                        distance=as.vector(dist_matrix))
means <- rowMeans(vst_matrix)
vars <- matrixStats::rowVars(vst_matrix)
mv_data <- data.frame(mean=means,variance=vars)
dir.create(output,recursive=TRUE,showWarnings=FALSE)
write.csv(base_table,file.path(output,"baseline_results_mle.csv"),row.names=FALSE,na="")
write.csv(shrink_table,file.path(output,"baseline_results_apeglm.csv"),row.names=FALSE,na="")
write.csv(pca_data,file.path(output,"pca_baseline_vs_vst.csv"),row.names=FALSE)
write.csv(dist_data,file.path(output,"sample_distances_vst.csv"),row.names=FALSE)
write.csv(mv_data,file.path(output,"mean_variance_vst.csv"),row.names=FALSE)
pdf(file.path(output,"pca_baseline_vs_vst.pdf"),width=10,height=5)
pca_plot <- ggplot(pca_data,aes(PC1,PC2,color=condition,shape=donor,label=sample_id))+geom_point(size=3)+geom_text(aes(hjust=ifelse(PC1<0,0,1)),vjust=-0.8,size=2.7,check_overlap=TRUE,show.legend=FALSE)+facet_wrap(~method,scales="free")+scale_x_continuous(expand=expansion(mult=0.12))+scale_y_continuous(expand=expansion(mult=0.12))+labs(x="PC1 score",y="PC2 score",color="Condition",shape="Donor")+theme_bw()
print(pca_plot)
dev.off()
png(file.path(output,"pca_baseline_vs_vst.png"),width=1600,height=800,res=160)
print(pca_plot)
dev.off()
pdf(file.path(output,"sample_distances_vst.pdf"),width=7,height=6)
dist_plot <- ggplot(dist_data,aes(sample_id,sample_id_2,fill=distance))+geom_tile()+scale_fill_viridis_c()+labs(x="Sample",y="Sample",fill="VST distance")+theme_bw()+theme(axis.text.x=element_text(angle=45,hjust=1))
print(dist_plot)
dev.off()
png(file.path(output,"sample_distances_vst.png"),width=1120,height=960,res=160)
print(dist_plot)
dev.off()
pdf(file.path(output,"mean_variance_vst.pdf"),width=7,height=5)
mv_plot <- ggplot(mv_data,aes(mean,variance))+geom_point(alpha=0.3,size=0.5)+scale_x_continuous(trans=scales::pseudo_log_trans(base=10))+scale_y_continuous(trans=scales::pseudo_log_trans(base=10))+labs(x="Mean VST expression (pseudo-log)",y="Variance across samples (pseudo-log)")+theme_bw()
print(mv_plot)
dev.off()
png(file.path(output,"mean_variance_vst.png"),width=1120,height=800,res=160)
print(mv_plot)
dev.off()

fold_tables <- list(); fold_manifests <- list()
for(donor in levels(metadata$donor)) {
  sample_keep <- metadata$donor != donor
  fold_meta <- droplevels(metadata[sample_keep,,drop=FALSE])
  fold_counts <- counts[,sample_keep,drop=FALSE]
  stopifnot(nlevels(fold_meta$donor)==3L,all(table(fold_meta$donor,fold_meta$condition)==1L))
  fold_dds <- DESeqDataSetFromMatrix(countData=fold_counts,colData=fold_meta,design=as.formula(config$design))
  warnings_before <- captured_warnings
  fold_dds <- withCallingHandlers(DESeq(fold_dds,fitType=config$fit_type,sfType=config$size_factors_fit_type,
                    minReplicatesForReplace=config$min_replicates,parallel=FALSE,quiet=TRUE),warning=capture_warning)
  fold_res <- results(fold_dds,contrast=config$contrast,alpha=config$alpha,
                      independentFiltering=TRUE,cooksCutoff=TRUE)
  fold_table <- data.frame(gene_id=rownames(fold_res),as.data.frame(fold_res),check.names=FALSE)
  fold_table$excluded_donor <- donor
  fold_table$status <- ifelse(is.finite(fold_table$log2FoldChange)&is.finite(fold_table$lfcSE),"estimable","not_estimable")
  fold_table$ci95_low <- fold_table$log2FoldChange-1.96*fold_table$lfcSE
  fold_table$ci95_high <- fold_table$log2FoldChange+1.96*fold_table$lfcSE
  fold_tables[[donor]] <- fold_table
  design_matrix <- model.matrix(design(fold_dds),colData(fold_dds))
  fold_manifests[[donor]] <- list(excluded_donor=donor,samples=colnames(fold_counts),pairs=nlevels(fold_meta$donor),
                                  design_rank=qr(design_matrix)$rank,residual_df=nrow(design_matrix)-qr(design_matrix)$rank,
                                  warnings=as.list(setdiff(captured_warnings,warnings_before)))
}
fold_all <- do.call(rbind,fold_tables)
write.csv(fold_all,file.path(output,"fold_results.csv"),row.names=FALSE,na="")
elapsed <- proc.time()[["elapsed"]]-started
files <- list.files(output,full.names=TRUE)
hashes <- lapply(files,function(path)digest(file=path,algo="sha256")); names(hashes)<-basename(files)
vm <- grep("VmHWM:",readLines("/proc/self/status"),value=TRUE)
peak_bytes <- as.numeric(gsub("[^0-9]","",vm))*1024
info <- list(run_id=basename(output),stage="E3",status="complete",design=config$design,contrast=as.list(config$contrast),
             input_sha256=list(counts=digest(file=file.path(input,"counts.csv"),algo="sha256"),metadata=digest(file=file.path(input,"metadata.csv"),algo="sha256")),
             config_sha256=digest(file=config_path,algo="sha256"),code_sha256=digest(file=normalizePath(file.path(dirname(config_path),"../r/qc_effects.R")),algo="sha256"),
             image_id=Sys.getenv("AIRWAY_IMAGE_ID",unset="not_provided"),
             versions=list(R=R.version.string,Bioconductor=as.character(BiocManager::version()),DESeq2=as.character(packageVersion("DESeq2")),
                           limma=as.character(packageVersion("limma")),apeglm=as.character(packageVersion("apeglm"))),
             universe=list(fixed_baseline_genes=nrow(counts),folds=length(fold_tables)),
             options=list(vst_blind=FALSE,shrinkage="apeglm",inferential_counts="raw",fold_universe="fixed_baseline"),
             residual_degrees_of_freedom=3,warnings=as.list(captured_warnings),folds=fold_manifests,
             shrinkage=list(coefficient=coef_name,spearman_abs_effect_rank=unname(rank_cor)),elapsed_seconds=elapsed,
             peak_memory_bytes=peak_bytes,output_sha256=hashes)
write_json(info,file.path(output,"manifest.json"),pretty=TRUE,auto_unbox=TRUE,na="null")
cat("E3 R completed:",nrow(counts),"genes;",length(fold_tables),"folds; VST blind=FALSE; apeglm coefficient",coef_name,"\n")
