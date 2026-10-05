args<-commandArgs(trailingOnly=TRUE);stopifnot(length(args)==3L)
ids<-unique(read.csv(args[[1]],stringsAsFactors=FALSE)$gene_id)
raw<-unique(read.csv(file.path(args[[2]],"ensembl_entrez_raw.csv"),stringsAsFactors=FALSE))
keep<-read.csv(file.path(args[[2]],"ensembl_entrez_unique.csv"),stringsAsFactors=FALSE)
by_ens<-table(raw$ensembl);by_entrez<-table(raw$entrez)
mapped<-intersect(ids,unique(raw$ensembl));uni<-intersect(ids,keep$ensembl)
cat("tested",length(ids),"raw-mapped",length(mapped),"unmapped",length(setdiff(ids,mapped)),
  "unambiguous",length(uni),"excluded-after-ambiguity",length(setdiff(mapped,uni)),"\n")
cat("Ensembl with multiple Entrez",sum(by_ens>1),"Entrez with multiple Ensembl",sum(by_entrez>1),"\n")
go<-read.csv(file.path(args[[2]],"go_bp_ancestral_membership.csv"),stringsAsFactors=FALSE)
len<-read.csv(file.path(args[[2]],"airway_exon_union_lengths.csv"),stringsAsFactors=FALSE)
tested_for_goseq<-read.csv(file.path(args[[3]],"selection_bias_data.csv"),stringsAsFactors=FALSE)$gene_id
cat("GO rows",nrow(go),"terms",length(unique(go$go_id)),"unique maps without exon length",
  sum(!keep$ensembl%in%len$ensembl),"unique maps outside GOseq universe",sum(!keep$ensembl%in%tested_for_goseq),"\n")
