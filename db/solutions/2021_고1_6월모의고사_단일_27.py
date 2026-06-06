import numpy as np
from cmath import exp, pi

n = 24
term1 = (np.sqrt(2) / (1 + 1j)) ** n
term2 = ((np.sqrt(3) + 1j) / 2) ** n
result = term1 + term2

if abs(result - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')