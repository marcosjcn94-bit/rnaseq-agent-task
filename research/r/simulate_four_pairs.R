args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 2L || length(args) > 3L) stop("usage: Rscript simulate_four_pairs.R diagnostics.csv output_dir [replicates]")
diagnostics_path <- args[[1]]; output_dir <- args[[2]]
nrep <- if (length(args) == 3L) as.integer(args[[3]]) else 200L
if (is.na(nrep) || nrep < 1L) stop("replicates must be positive")
suppressPackageStartupMessages(library(DESeq2))
dir.create(output_dir, recursive=TRUE, showWarnings=FALSE)
d <- read.csv(diagnostics_path)
ok <- is.finite(d$baseMean) & d$baseMean > 0 & is.finite(d$dispersion) & d$dispersion > 0
if (sum(ok) < 1000L) stop("fewer than 1000 usable empirical genes")
set.seed(20261005)
idx <- sample(which(ok), 1000L, replace=FALSE)
base <- d$baseMean[idx]; disp <- d$dispersion[idx]
donor_cols <- grep("^donor_",names(d),value=TRUE)
if (length(donor_cols) != 3L) stop("expected three fitted donor contrasts in E2 export")
donor_effects <- as.matrix(d[,donor_cols])/log(2)
if (any(!is.finite(donor_effects))) stop("nonfinite donor contrast estimate")
donor_effects <- cbind(0,donor_effects)
donor_centered <- donor_effects-rowMeans(donor_effects)
donor_sd <- sqrt(sum(donor_centered^2)/(nrow(donor_centered)*(ncol(donor_centered)-1)))
config <- expand.grid(de=c(0, .1), interaction=c(0, .5))
for (scenario in seq_len(nrow(config))) {
  frac <- config$de[scenario]; isd <- config$interaction[scenario]
  key <- sprintf("r-n4-de%s-int%s", frac, isd)
  path <- file.path(output_dir, paste0(key, ".csv"))
  rows <- if (file.exists(path)) read.csv(path, stringsAsFactors=FALSE) else data.frame()
  for (rep in seq_len(nrep)) {
    if (nrow(rows) >= rep) next
    seed <- 20261005 + 4000000 + as.integer(frac*100)*10000 + as.integer(isd*10)*1000 + rep
    set.seed(seed)
    truth <- rep(FALSE,1000L); truth[sample(1000L, round(1000*frac))] <- TRUE
    effect <- numeric(1000L); effect[truth] <- sample(c(-1,1),sum(truth),replace=TRUE)
    donor <- matrix(rnorm(4*1000,0,donor_sd),nrow=4)
    interaction <- matrix(rnorm(4*1000,0,isd),nrow=4)
    sf <- rlnorm(8,0,.16)
    y <- matrix(0L,nrow=1000,ncol=8)
    for (dd in 1:4) for (cc in 0:1) {
      j <- 2*(dd-1)+cc+1
      mu <- pmax(.05,2^(log2(pmax(base,.1))+donor[dd,]+cc*(effect+interaction[dd,])))*sf[j]
      y[,j] <- rnbinom(1000,size=1/pmax(disp,1e-6),mu=mu)
    }
    colnames(y) <- unlist(lapply(1:4,function(i)c(paste0("D",i,"_control"),paste0("D",i,"_treated"))))
    cd <- data.frame(donor=factor(rep(paste0("D",1:4),each=2)),condition=factor(rep(c("control","treated"),4),levels=c("control","treated")),row.names=colnames(y))
    ans <- tryCatch({
      dds <- DESeqDataSetFromMatrix(y,cd,~donor+condition)
      dds <- DESeq(dds,quiet=TRUE,minReplicatesForReplace=Inf)
      rr <- results(dds,contrast=c("condition","treated","control"),alpha=.05,independentFiltering=FALSE,cooksCutoff=FALSE)
      valid <- is.finite(rr$log2FoldChange) & is.finite(rr$lfcSE)
      rej <- !is.na(rr$padj) & rr$padj < .05
      nrej <- sum(rej[valid]); ntrue <- sum(truth[valid]); null <- !truth[valid]
      data.frame(engine="DESeq2",pairs=4,de_fraction=frac,interaction_sd=isd,replicate=rep,seed=seed,donor_effect_sd_log2=donor_sd,testable=sum(valid),failure="",
        fdp=sum(rej[valid]&!truth[valid])/max(nrej,1),power=if(ntrue)sum(rej[valid]&truth[valid])/ntrue else NA_real_,
        type1=if(any(null))sum(rej[valid]&null)/sum(null) else NA_real_,
        coverage=if(any(truth[valid]))mean(abs(rr$log2FoldChange[valid][truth[valid]]-effect[valid][truth[valid]])<=1.959963984540054*rr$lfcSE[valid][truth[valid]]) else NA_real_,
        rejections=nrej)
    },error=function(e) data.frame(engine="DESeq2",pairs=4,de_fraction=frac,interaction_sd=isd,replicate=rep,seed=seed,donor_effect_sd_log2=donor_sd,testable=0,failure=conditionMessage(e),fdp=NA,power=NA,type1=NA,coverage=NA,rejections=0))
    rows <- rbind(rows,ans); write.csv(rows,path,row.names=FALSE)
  }
}
