import sympy as sp
from sympy import sqrt, simplify, Rational

S1 = (3 - sqrt(3)) / 3
scale_ratio = Rational(1, 12)
infinite_series = Rational(1, 5)
multiplier = 1 + infinite_series
limit = S1 * multiplier
result = simplify(limit)
print('VERIFY_PASS' if simplify(result - 2*(3-sqrt(3))/5) == 0 else 'VERIFY_FAIL')