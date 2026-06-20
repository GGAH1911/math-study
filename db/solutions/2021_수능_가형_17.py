import numpy as np
from scipy.special import comb

# k는 binomial distribution B(15, 1/3)
# 각 k에 대해 X = k + 12
# E(X) = sum of (k+12) * P(k)

n = 15
p = 1/3
q = 2/3

expected_X = 0
for k in range(16):
    prob_k = comb(n, k, exact=True) * (p**k) * (q**(n-k))
    x_value = k + 12
    expected_X += x_value * prob_k

print(f'E(X) = {expected_X}')
if abs(expected_X - 17) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')