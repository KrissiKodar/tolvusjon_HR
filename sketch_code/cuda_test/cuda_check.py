import numpy as np
import matplotlib.pyplot as plt

# array with random numbers
A = np.random.rand(3,3)

# find eigenvalues and eigenvectors
ei_val, ei_vec = np.linalg.eig(A)

print('eigenvalues: ', ei_val)
print('eigenvectors: ', ei_vec)
