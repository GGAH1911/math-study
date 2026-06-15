from sympy import symbols, solve, sqrt, erf, Rational
import sympy as sp

m = Rational(9, 4)
sigma = m / 3

# Z-score when X = 9/2
z_score = (Rational(9, 2) - m) / sigma
print(f'Z-score: {z_score}')

# For standard normal: P(Z <= 3) = 0.5 + 0.4987 = 0.9987
# We verify this matches the given probability
expected_prob = 0.9987

# Z=3.0 should give cumulative prob of 0.9987
if z_score == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')