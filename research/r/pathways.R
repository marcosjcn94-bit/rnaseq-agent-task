suppressPackageStartupMessages({
  library(edgeR); library(limma); library(DESeq2); library(goseq)
  library(jsonlite); library(digest)
})
source("research/r/pathway_utils.R")
args <- commandArgs(trailingOnly=TRUE); stopifnot(length(args)==4L)
input <- args[[1]]; ann_dir <- args[[2]]; config_path <- args[[3]]; out <- args[[4]]
if (dir.exists(out) && length(list.files(out, all.files=TRUE, no..=TRUE))) stop("output must be empty")
dir.create(out, recursive=TRUE, showWarnings=FALSE)
cfg <- fromJSON(config_path, simplifyVector=TRUE)
counts <- as.matrix(read.csv(file.path(input,"counts.csv"),row.names=1,check.names=FALSE))
storage.mode(counts) <- "integer"
meta <- read.csv(file.path(input,"metadata.csv"),stringsAsFactors=FALSE)
counts <- counts[order(rownames(counts)),,drop=FALSE]
meta <- meta[match(colnames(counts),meta$sample_id),,drop=FALSE]
stopifnot(!anyNA(meta$sample_id),!anyDuplicated(rownames(counts)),all(table(meta$donor,meta$condition)==1L))
meta$donor <- factor(meta$donor); meta$condition <- factor(meta$condition,levels=c("control","treated"))
mapping <- read.csv(file.path(ann_dir,"ensembl_entrez_unique.csv"),stringsAsFactors=FALSE)
membership <- read.csv(file.path(ann_dir,"go_bp_ancestral_membership.csv"),stringsAsFactors=FALSE)
base_keep <- rowSums(counts>=cfg$min_count)>=cfg$min_samples
base_ids <- rownames(counts)[base_keep]
idmap <- mapping[match(base_ids,mapping$ensembl),,drop=FALSE]
idmap <- idmap[!is.na(idmap$entrez),,drop=FALSE]
go <- split(as.character(membership$entrez),as.character(membership$go_id))
mapped_entrez <- unique(as.character(idmap$entrez))
go_ids <- names(go)
member_entrez <- as.character(membership$entrez)
member_entrez_index <- match(member_entrez,mapped_entrez)
member_term_index <- match(as.character(membership$go_id),go_ids)
stopifnot(!anyNA(member_entrez_index),!anyNA(member_term_index))
term_names <- unique(membership[c("go_id","TERM")]); term_names <- setNames(term_names$TERM,term_names$go_id)
sets_for <- function(ids, min_size=cfg$min_set_size, max_size=cfg$max_set_size) {
  ids <- unique(as.character(ids)); mapped <- unique(as.character(idmap$entrez[match(ids,idmap$ensembl)]))
  mapped <- mapped[!is.na(mapped)]; valid <- logical(length(mapped_entrez))
  valid[match(mapped,mapped_entrez)] <- TRUE
  present <- valid[member_entrez_index]
  counts <- tabulate(member_term_index[present],nbins=length(go_ids))
  selected_terms <- which(counts>=min_size & counts<=max_size)
  rows <- present & member_term_index %in% selected_terms
  split(member_entrez[rows],as.character(membership$go_id[rows]))
}
run_camera <- function(samples, label) {
  y0 <- counts[base_ids,samples,drop=FALSE]
  m <- droplevels(meta[match(samples,meta$sample_id),,drop=FALSE]); rownames(m)<-m$sample_id
  design <- model.matrix(as.formula(cfg$design),m)
  if (qr(design)$rank<ncol(design)) stop(paste("rank deficient",label))
  y <- DGEList(y0); keep <- filterByExpr(y,design=design); y <- calcNormFactors(y[keep,,keep.lib.sizes=FALSE])
  v <- voom(y,design,plot=FALSE); coef <- which(colnames(design)=="conditiontreated"); stopifnot(length(coef)==1L)
  idx <- sets_for(rownames(v$E)); if (!length(idx)) stop("no eligible GO terms")
  convert <- lapply(idx,function(ids) match(idmap$ensembl[match(ids,idmap$entrez)],rownames(v$E)))
  convert <- lapply(convert,function(x) sort(unique(x[!is.na(x)])))
  names(convert)<-names(idx); valid <- lengths(convert)>=cfg$min_set_size
  idx<-convert[valid]; if(!length(idx)) stop("no eligible CAMERA terms after intersection")
  rows <- list(); correlations <- list(estimated=NA_real_,fixed=cfg$camera_fixed_cor_sensitivity)
  for (tag in names(correlations)) {
    fit <- camera(v,index=idx,design=design,contrast=coef,
         use.ranks=TRUE,inter.gene.cor=unname(correlations[[tag]]),allow.neg.cor=FALSE)
    term_id <- names(idx); aligned_names <- unname(term_names[term_id])
    lengths_out <- c(length(term_id),length(aligned_names),length(fit$NGenes),length(fit$Direction),length(fit$PValue))
    if(any(lengths_out!=nrow(fit))) stop(paste("CAMERA output shape mismatch",paste(lengths_out,collapse=","),"rows",nrow(fit)))
    tab <- data.frame(term_id=term_id,term_name=aligned_names,
      n_genes=fit$NGenes,direction=fit$Direction,p_value=fit$PValue,
      fdr=p.adjust(fit$PValue,method="BH"),analysis=label,correlation=tag,stringsAsFactors=FALSE)
    rows[[tag]]<-tab
  }
  do.call(rbind,rows)
}
sample_sets <- c(list(full=colnames(counts)),
  setNames(lapply(cfg$fold_donors,function(d) meta$sample_id[meta$donor!=d]),paste0("drop_",cfg$fold_donors)))
camera <- do.call(rbind,lapply(names(sample_sets),function(label) run_camera(sample_sets[[label]],label)))
write.csv(camera,file.path(out,"camera_all_terms.csv"),row.names=FALSE,na="")

# ORA uses the frozen DESeq2 baseline results and the same eligible mapped universe.
de <- read.csv(file.path(dirname(ann_dir),"..","E2","r-baseline","results.csv"),stringsAsFactors=FALSE)
if (!all(c("gene_id","padj") %in% names(de))) stop("E2 DESeq2 results unavailable or malformed")
ora_universe <- intersect(intersect(base_ids,idmap$ensembl),de$gene_id[!is.na(de$padj)])
de_ids <- intersect(de$gene_id[!is.na(de$padj)&de$padj<cfg$alpha],ora_universe)
ora_sets <- sets_for(ora_universe); ora <- lapply(names(ora_sets),function(t) {
  gs <- intersect(ora_sets[[t]],idmap$entrez[match(ora_universe,idmap$ensembl)])
  sig <- intersect(gs,idmap$entrez[match(de_ids,idmap$ensembl)])
  data.frame(term_id=t,term_name=unname(term_names[t]),set_size=length(gs),selected=length(sig),
    p_value=phyper(length(sig)-1,length(gs),length(unique(idmap$entrez[match(ora_universe,idmap$ensembl)]))-length(gs),
                   length(unique(idmap$entrez[match(de_ids,idmap$ensembl)])),lower.tail=FALSE))
})
ora <- do.call(rbind,ora); ora$fdr<-p.adjust(ora$p_value,"BH"); write.csv(ora,file.path(out,"ora_deseq2_baseline.csv"),row.names=FALSE)
# Separate common-universe sensitivity using the E2 independent-filter-off result.
de_noif <- read.csv(file.path(dirname(ann_dir),"..","E2","r-if-off","results.csv"),stringsAsFactors=FALSE)
u_noif <- intersect(intersect(base_ids,idmap$ensembl),de_noif$gene_id[!is.na(de_noif$padj)])
sig_noif <- intersect(de_noif$gene_id[!is.na(de_noif$padj)&de_noif$padj<cfg$alpha],u_noif)
sets_noif <- sets_for(u_noif)
ora_noif <- lapply(names(sets_noif),function(t) {
  gs <- intersect(sets_noif[[t]],idmap$entrez[match(u_noif,idmap$ensembl)])
  sig <- intersect(gs,idmap$entrez[match(sig_noif,idmap$ensembl)])
  n_all <- length(unique(idmap$entrez[match(u_noif,idmap$ensembl)])); n_sig <- length(unique(idmap$entrez[match(sig_noif,idmap$ensembl)]))
  data.frame(term_id=t,term_name=unname(term_names[t]),set_size=length(gs),selected=length(sig),
    p_value=phyper(length(sig)-1,length(gs),n_all-length(gs),n_sig,lower.tail=FALSE))
})
ora_noif <- do.call(rbind,ora_noif); ora_noif$fdr<-p.adjust(ora_noif$p_value,"BH")
ora_noif$analysis<-"independent_filter_off"; write.csv(ora_noif,file.path(out,"ora_common_universe_no_if.csv"),row.names=FALSE)

# GOseq length sensitivity from the airway package's exon union lengths.
lengths <- read.csv(file.path(ann_dir,"airway_exon_union_lengths.csv"),stringsAsFactors=FALSE)
entrez_by_ens <- setNames(as.character(idmap$entrez),idmap$ensembl)
go_entrez <- unique(as.character(idmap$entrez[match(ora_universe,idmap$ensembl)]))
membership_subset <- membership[as.character(membership$entrez)%in%go_entrez,c("go_id","entrez"),drop=FALSE]
go_by_entrez <- split(as.character(membership_subset$go_id),as.character(membership_subset$entrez))
gene2cat <- lapply(unname(entrez_by_ens[ora_universe]),function(e) {
  categories <- go_by_entrez[[e]]; if(is.null(categories)) character() else unique(categories)
})
names(gene2cat)<-ora_universe
len <- setNames(lengths$exon_union_bp,lengths$ensembl)
goseq_universe <- ora_universe[ora_universe %in% names(len) & !is.na(len[ora_universe])]
length_bias <- len[goseq_universe]
eligible_goseq_terms <- names(sets_for(goseq_universe))
gene2cat_len <- lapply(gene2cat[goseq_universe],function(x)intersect(x,eligible_goseq_terms))
de_ids_len <- intersect(de_ids,goseq_universe)
expr <- read.csv(file.path(dirname(ann_dir),"..","E2","r-baseline","normalized_counts.csv"),check.names=FALSE)
expr_mean <- setNames(rowMeans(as.matrix(expr[,-1,drop=FALSE])),expr[[1]])[goseq_universe]
run_goseq <- function(bias,label) {
  ids <- names(bias); b <- unname(bias); names(b)<-ids
  selected <- setNames(as.integer(ids%in%de_ids_len),ids)
  pwf <- nullp(selected,bias.data=b,plot.fit=FALSE)
  fit <- goseq(pwf,gene2cat=gene2cat_len,use_genes_without_cat=TRUE,method="Wallenius")
  fit$over_p_raw<-fit$over_represented_pvalue;fit$under_p_raw<-fit$under_represented_pvalue
  fit$over_represented_pvalue<-pmin(1,pmax(0,fit$over_p_raw));fit$under_represented_pvalue<-pmin(1,pmax(0,fit$under_p_raw))
  fit$over_p_clipped<-fit$over_p_raw!=fit$over_represented_pvalue;fit$under_p_clipped<-fit$under_p_raw!=fit$under_represented_pvalue
  fit$analysis<-label;fit$fdr_over<-p.adjust(fit$over_represented_pvalue,"BH")
  fit$fdr_under<-p.adjust(fit$under_represented_pvalue,"BH")
  list(result=fit,curve=data.frame(gene_id=rownames(pwf),bias=pwf$bias,pwf=pwf$pwf,selected=pwf$DEgenes,analysis=label))
}
goseq_len<-run_goseq(length_bias,"exon_union_length")
goseq_expr<-run_goseq(expr_mean,"mean_normalized_expression")
goseq_tab<-rbind(goseq_len$result,goseq_expr$result)
write.csv(goseq_tab,file.path(out,"goseq_sensitivities.csv"),row.names=FALSE,na="")
write.csv(rbind(goseq_len$curve,goseq_expr$curve),file.path(out,"selection_probability_curves.csv"),row.names=FALSE)
write.csv(data.frame(gene_id=goseq_universe,length_bp=length_bias,mean_normalized_expression=expr_mean,
                     selected=goseq_universe%in%de_ids),file.path(out,"selection_bias_data.csv"),row.names=FALSE)
out_files<-list.files(out,full.names=TRUE)
out_hashes<-setNames(vapply(out_files,function(f)digest(file=f,algo="sha256"),character(1)),basename(out_files))
manifest<-list(stage="E4",created_utc=format(Sys.time(),tz="UTC",usetz=TRUE),
  config_sha256=digest(cfg,algo="sha256"),annotation_manifest=fromJSON(file.path(ann_dir,"manifest.json")),
  code_sha256=digest(file="research/r/pathways.R",algo="sha256"),files_sha256=as.list(out_hashes),
  base_tested_genes=length(base_ids),unique_mapped_genes=length(ora_universe),
  camera_terms=nrow(camera),ora_terms=nrow(ora),goseq_terms=nrow(goseq_tab),
  versions=sapply(c("edgeR","limma","DESeq2","goseq"),function(p)as.character(packageVersion(p))),
  input_hashes=list(counts=digest(file=file.path(input,"counts.csv"),algo="sha256"),metadata=digest(file=file.path(input,"metadata.csv"),algo="sha256")))
write_json(manifest,file.path(out,"manifest.json"),auto_unbox=TRUE,pretty=TRUE)
