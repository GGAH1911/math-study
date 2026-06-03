from sympy import *
x, a, b = symbols('x a b')
# 조건 1: 점근선 y=3 -> b=3
b_val = 3
# 조건 2: y절편 = 5 -> 2^a + b = 5
a_val = solve(2**a + b_val - 5, a)[0]
result = a_val + b_val
f = lambda xv: 2**(xv + a_val) + b_val
# 검증
asymptote_ok = abs(float(f(-1000)) - 3) < 1e-6
ycept_ok = abs(float(f(0)) - 5) < 1e-9
print('VERIFY_PASS' if (result == 4 and asymptote_ok and ycept_ok) else 'VERIFY_FAIL')