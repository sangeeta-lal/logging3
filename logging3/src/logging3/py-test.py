import numpy as np
import lda
import lda.datasets

X = lda.datasets.load_reuters()
print("type(X): {}".format(type(X)))
print("shape: {}\n".format(X.shape))


print " X=", X