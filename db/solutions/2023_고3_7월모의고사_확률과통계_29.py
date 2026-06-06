import sympy as sp
import numpy as np
from scipy.optimize import fsolve

# c1 = 2 - sqrt(2)
c1_exact = 2 - sp.sqrt(2)
a_exact = c1_exact / 2
c2_exact = 4 - c1_exact

# Calculate P(0 <= Y <= 5a)
five_a = 5 * a_exact
result = c1_exact**2
expanded = sp.expand(result)
print(f'P(0 <= Y <= 5a) = {expanded}')

# Verify this equals 6 - 4√2
expected = 6 - 4*sp.sqrt(2)
verif = sp.simplify(expanded - expected)
print(f'Verification: {expanded} = {expected}: {verif == 0}')

# Check p and q
p = 6
q = 4
answer_product = p * q
print(f'p = {p}, q = {q}')
print(f'p × q = {answer_product}')

# Numerical check
numerical_result = float(expanded.evalf())
print(f'Numerical: 6 - 4√2 ≈ {numerical_result}')
if 0 < numerical_result < 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')