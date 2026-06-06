import numpy as np
from math import sqrt

alpha = 3 - 2*sqrt(3)/3
beta = -1 - 2*sqrt(3)/3

result = alpha**2 + beta**2
print(f'α = {alpha:.6f}')
print(f'β = {beta:.6f}')
print(f'α² + β² = {result:.6f}')
print(f'Nearest integer: {round(result)}')

if 7.5 < result < 8.5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')