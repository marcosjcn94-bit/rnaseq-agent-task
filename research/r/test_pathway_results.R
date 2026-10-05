args<-commandArgs(trailingOnly=TRUE);stopifnot(length(args)==1L)
camera<-read.csv(file.path(args[[1]],"camera_all_terms.csv"),stringsAsFactors=FALSE)
ora<-read.csv(file.path(args[[1]],"ora_deseq2_baseline.csv"),stringsAsFactors=FALSE)
ora_noif<-read.csv(file.path(args[[1]],"ora_common_universe_no_if.csv"),stringsAsFactors=FALSE)
goseq<-read.csv(file.path(args[[1]],"goseq_sensitivities.csv"),stringsAsFactors=FALSE)
curves<-read.csv(file.path(args[[1]],"selection_probability_curves.csv"),stringsAsFactors=FALSE)
stopifnot(nrow(camera)>0L,!anyDuplicated(camera[c("term_id","analysis","correlation")]),
  all(camera$n_genes>=15 & camera$n_genes<=500),all(camera$p_value>=0 & camera$p_value<=1),
  setequal(unique(camera$analysis),c("full","drop_N052611","drop_N061011","drop_N080611","drop_N61311")),
  setequal(unique(camera$correlation),c("estimated","fixed")))
for(g in split(camera,interaction(camera$analysis,camera$correlation,drop=TRUE)))
  stopifnot(isTRUE(all.equal(g$fdr,p.adjust(g$p_value,"BH"),tolerance=1e-12)))
for(tab in list(ora,ora_noif)) stopifnot(nrow(tab)>0L,!anyDuplicated(tab$term_id),all(tab$p_value>=0 & tab$p_value<=1),
  isTRUE(all.equal(tab$fdr,p.adjust(tab$p_value,"BH"),tolerance=1e-12)))
stopifnot(setequal(unique(goseq$analysis),c("exon_union_length","mean_normalized_expression")),
  !anyDuplicated(goseq[c("category","analysis")]),all(goseq$numInCat>=15 & goseq$numInCat<=500),
  all(goseq$over_represented_pvalue>=0 & goseq$over_represented_pvalue<=1),
  all(goseq$under_represented_pvalue>=0 & goseq$under_represented_pvalue<=1),
  !anyDuplicated(curves[c("gene_id","analysis")]),setequal(unique(curves$analysis),unique(goseq$analysis)))
for(g in split(goseq,goseq$analysis))
  stopifnot(isTRUE(all.equal(g$fdr_over,p.adjust(g$over_represented_pvalue,"BH"),tolerance=1e-12)),
            isTRUE(all.equal(g$fdr_under,p.adjust(g$under_represented_pvalue,"BH"),tolerance=1e-12)))
cat("GOseq p-values clipped for numerical roundoff:",sum(goseq$over_p_clipped)+sum(goseq$under_p_clipped),"\n")
cat("pathway result checks passed:",nrow(camera),"CAMERA,",nrow(ora),"ORA,",nrow(goseq),"GOseq rows\n")
