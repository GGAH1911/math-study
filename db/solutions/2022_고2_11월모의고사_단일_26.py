import sympy as sp
from fractions import Fraction

# Verify the general term formula
def S_n(n):
    return Fraction(n, 2*n + 1)

# Calculate a_n for n=1 to 6
a = {}
for n in range(1, 7):
    if n == 1:
        a[n] = S_n(1)
    else:
        a[n] = S_n(n) - S_n(n-1)

# Verify a_n = 1/[(2n+1)(2n-1)] and compute 1/a_n
sum_inv_a = Fraction(0)
for k in range(1, 7):
    inv_a_k = 1 / a[k]
    # Also verify formula 1/a_k = 4k^2 - 1
    formula_result = 4*k**2 - 1
    assert abs(float(inv_a_k) - formula_result) < 1e-10, f'Mismatch at k={k}'
    sum_inv_a += inv_a_k

if int(sum_inv_a) == 358:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')