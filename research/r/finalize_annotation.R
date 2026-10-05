suppressPackageStartupMessages({library(jsonlite);library(digest);library(org.Hs.eg.db);library(GO.db);library(airway)})
args<-commandArgs(trailingOnly=TRUE);stopifnot(length(args)==3L)
source_dir<-args[[1]];out<-args[[2]];ids_file<-args[[3]]
if(dir.exists(out)&&length(list.files(out,all.files=TRUE,no..=TRUE)))stop("output must be empty")
dir.create(out,recursive=TRUE,showWarnings=FALSE)
for(f in c("ensembl_entrez_raw.csv","ensembl_entrez_unique.csv","airway_exon_union_lengths.csv"))
  stopifnot(file.copy(file.path(source_dir,f),file.path(out,f)))
go<-read.csv(file.path(source_dir,"go_bp_ancestral_membership.csv"),check.names=FALSE,stringsAsFactors=FALSE)
stopifnot(ncol(go)==5L,all(go[[4]]%in%c("BP","CC","MF")))
membership<-unique(data.frame(go_id=go[[1]][go[[4]]=="BP"],entrez=go[[2]][go[[4]]=="BP"],TERM=go[[5]][go[[4]]=="BP"]))
membership<-membership[order(membership$go_id,membership$entrez),]
write.csv(membership,file.path(out,"go_bp_ancestral_membership.csv"),row.names=FALSE)
files<-list.files(out,full.names=TRUE)
hashes<-setNames(vapply(files,function(f)digest(file=f,algo="sha256"),character(1)),basename(files))
raw<-read.csv(file.path(out,"ensembl_entrez_raw.csv"),stringsAsFactors=FALSE)
unique_map<-read.csv(file.path(out,"ensembl_entrez_unique.csv"),stringsAsFactors=FALSE)
ids<-read.csv(ids_file,stringsAsFactors=FALSE)$gene_id
manifest<-list(stage="E4-annotation",source_attempt="annotation-attempt1; GOALL evidence/ontology columns explicitly normalized",
  created_utc=format(Sys.time(),tz="UTC",usetz=TRUE),input_gene_ids=length(unique(ids)),
  raw_mapping_rows=nrow(raw),uniquely_mapped_ensembl=nrow(unique_map),
  versions=list(org.Hs.eg.db=as.character(packageVersion("org.Hs.eg.db")),GO.db=as.character(packageVersion("GO.db")),airway=as.character(packageVersion("airway"))),
  GO_collection="GO Biological Process; GOALL ancestral membership; deduplicated gene-term pairs",
  input_sha256=digest(file=ids_file,algo="sha256"),files_sha256=as.list(hashes))
write_json(manifest,file.path(out,"manifest.json"),auto_unbox=TRUE,pretty=TRUE)
