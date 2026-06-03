import sympy as sp
from sympy import sqrt

# 원래 문제 식
original_expr = sqrt(6) * sqrt(sp.Rational(1, 2)) + sqrt(3)
result = original_expr.simplify()

answer = 2 * sqrt(3)

if sp.simplify(result - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')