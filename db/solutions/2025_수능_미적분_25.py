import sympy as sp
from sympy import symbols, sqrt, limit, oo

n = symbols('n', positive=True, integer=True)

# 주어진 조건: lim (na_n)/(n^2+3) = 1 을 만족하는 a_n
# a_n = n + 3/n (주요 항)
a_n = n + 3/n

# 조건 검증
condition = limit((n * a_n) / (n**2 + 3), n, oo)
assert condition == 1, f"Condition check failed: {condition}"

# 구하는 극한: lim (sqrt(a_n^2 + n) - a_n)
expr = sqrt(a_n**2 + n) - a_n
result = limit(expr, n, oo)

if result == sp.Rational(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')