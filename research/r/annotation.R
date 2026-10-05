suppressPackageStartupMessages({
  library(AnnotationDbi); library(org.Hs.eg.db); library(GO.db)
  library(airway); library(GenomicRanges); library(digest); library(jsonlite)
})
source("research/r/pathway_utils.R")

freeze_annotation <- function(gene_ids) {
  selected <- AnnotationDbi::select(org.Hs.eg.db, keys=unique(gene_ids),
                                    keytype="ENSEMBL", columns="ENTREZID")
  raw <- unique(data.frame(ensembl=selected$ENSEMBL,entrez=selected$ENTREZID))
  mapping <- unique_bimap(raw)
  go_selected <- AnnotationDbi::select(org.Hs.eg.db, keys=unique(mapping$entrez),
                                  keytype="ENTREZID", columns="GOALL")
  go_raw <- unique(data.frame(entrez=go_selected$ENTREZID,go_id=go_selected$GOALL,
                              ontology=go_selected$ONTOLOGYALL))
  go_raw <- go_raw[complete.cases(go_raw)&go_raw$ontology=="BP",]
  terms <- AnnotationDbi::select(GO.db, keys=unique(go_raw$go_id),
                                 keytype="GOID", columns=c("TERM", "ONTOLOGY"))
  terms <- unique(terms[terms$ONTOLOGY == "BP" & !is.na(terms$TERM), ])
  term_table <- unique(data.frame(go_id=terms$GOID,TERM=terms$TERM))
  membership <- unique(merge(go_raw[,c("go_id","entrez")],term_table,by="go_id"))
  membership <- membership[,c("go_id","entrez","TERM")]
  data("airway", package="airway")
  gene_exons <- rowRanges(airway)[intersect(gene_ids,names(rowRanges(airway)))]
  length_table <- data.frame(ensembl=names(gene_exons),
    exon_union_bp=vapply(gene_exons, function(x) sum(width(reduce(x))), numeric(1)))
  list(mapping=mapping, membership=membership, lengths=length_table,
       raw_mapping=raw, versions=c(org.Hs.eg.db=as.character(packageVersion("org.Hs.eg.db")),
          GO.db=as.character(packageVersion("GO.db")), airway=as.character(packageVersion("airway"))))
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly=TRUE); stopifnot(length(args) == 2L)
  ids <- read.csv(args[1], stringsAsFactors=FALSE)$gene_id
  out <- args[2]; if (dir.exists(out) && length(list.files(out, all.files=TRUE, no..=TRUE))) stop("output must be empty")
  dir.create(out, recursive=TRUE, showWarnings=FALSE)
  frozen <- freeze_annotation(ids)
  write.csv(frozen$mapping, file.path(out,"ensembl_entrez_unique.csv"), row.names=FALSE)
  write.csv(frozen$raw_mapping, file.path(out,"ensembl_entrez_raw.csv"), row.names=FALSE)
  write.csv(frozen$membership, file.path(out,"go_bp_ancestral_membership.csv"), row.names=FALSE)
  write.csv(frozen$lengths, file.path(out,"airway_exon_union_lengths.csv"), row.names=FALSE)
  files <- list.files(out, full.names=TRUE)
  manifest <- list(versions=frozen$versions, GO_collection="GO Biological Process; GOALL ancestral membership",
    created_utc=format(Sys.time(), tz="UTC", usetz=TRUE), files=setNames(vapply(files, digest::digest, character(1), algo="sha256", file=TRUE), basename(files)))
  write_json(manifest, file.path(out,"manifest.json"), auto_unbox=TRUE, pretty=TRUE)
}
