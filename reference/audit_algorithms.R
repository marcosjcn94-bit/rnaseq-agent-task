suppressPackageStartupMessages(library(DESeq2))
cat(paste(deparse(DESeq2:::estimateDispersionsPriorVar),collapse="\n"),"\n")
