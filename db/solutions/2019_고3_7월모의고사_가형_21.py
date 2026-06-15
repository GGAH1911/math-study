import sympy as sp
from sympy import sin, cos, asin, diff, sqrt, simplify

t = sp.Symbol('t', real=True, positive=True)

# g(t) = arcsin(t) - t/sqrt(1-t^2)
g = asin(t) - t/sqrt(1 - t**2)

# 미분
g_prime = diff(g, t)
g_prime_simplified = simplify(g_prime)

# t = 2*sqrt(2)/3에서 계산
t_val = 2*sqrt(2)/3
result = g_prime_simplified.subs(t, t_val)
result_value = float(result)

# 검증
if abs(result_value - (-24)) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result_value}')