import inspect
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
print("PyDESeq2 dispersion prior:")
print(inspect.getsource(DeseqDataSet.fit_dispersion_prior))
print("PyDESeq2 independent filtering:")
print(inspect.getsource(DeseqStats._independent_filtering))
