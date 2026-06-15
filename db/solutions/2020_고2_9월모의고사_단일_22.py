import sympy as sp
# 3^4 × 9^{-1} ?
CANDIDATE = 9
print('VERIFY_PASS' if 3**4 * sp.Rational(1,9) == CANDIDATE else 'VERIFY_FAIL')
