unique_bimap <- function(map) {
  map <- unique(map[complete.cases(map), , drop=FALSE])
  left <- table(map[[1]]); right <- table(map[[2]])
  out <- map[left[map[[1]]] == 1L & right[map[[2]]] == 1L, , drop=FALSE]
  rownames(out) <- NULL
  out
}

eligible_sets <- function(sets, universe, min_size=15L, max_size=500L) {
  universe <- unique(as.character(universe))
  sets <- lapply(sets,function(x) intersect(unique(as.character(x)),universe))
  sets[lengths(sets)>=min_size & lengths(sets)<=max_size]
}

ora_pvalue <- function(set, selected, universe) {
  universe <- unique(as.character(universe)); set <- intersect(unique(as.character(set)),universe)
  selected <- intersect(unique(as.character(selected)),universe)
  if (!length(set) || !length(selected)) return(1)
  phyper(length(intersect(set,selected))-1L,length(set),length(universe)-length(set),length(selected),lower.tail=FALSE)
}
