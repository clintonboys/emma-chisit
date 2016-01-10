import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

A = np.array([1,np.nan, 3,5,1,2,5,2,4,1,2,np.nan,2,1,np.nan,2,np.nan,1,2])

plt.hist(A[~np.isnan(A)])
plt.show()