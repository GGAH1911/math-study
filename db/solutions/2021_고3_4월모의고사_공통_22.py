from sympy import symbols, expand, solve, factor
import numpy as np

# a = -1.5인 경우 확인
a = -1.5
x = symbols('x')
f = 3*x + a
g = x**3 + 2*a*x**2 + a**2*x - 8 - 8*a - 2*a**2
h = f * g

# 조건 (가): h(-0.5) = 0, h'(-0.5) = 0 확인
c = -a/3
h_at_c = h.subs(x, c)
print(f'h({c}) = {float(h_at_c)}')  # 0이어야 함

from sympy import diff
h_prime = diff(h, x)
h_prime_at_c = h_prime.subs(x, c)
print(f"h'({c}) = {float(h_prime_at_c)}")  # 0이어야 함

# a = -1.5일 때 h(-1) 계산
a_val = -1.5
h_expr = 3*(x - 0.5)**3*(x - 2)
h_at_minus1 = h_expr.subs(x, -1)
print(f'h(-1) = {h_at_minus1}')
print(f'h(-1) as fraction = {float(h_at_minus1)}')
print(f'243/8 = {243/8}')

if abs(float(h_at_minus1) - 243/8) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')