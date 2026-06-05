import sympy as sp
from sympy import limit, oo, symbols

x = symbols('x')

# 예시: g(x) = x, 2f(x) - 3g(x) = 1 조건 만족
g_x = x
f_x = (3*x + 1) / 2

# 조건 검증
cond1 = limit(2*f_x - 3*g_x, x, oo)
cond2 = limit(g_x, x, oo)

# 구하는 극한값
result = limit((4*f_x + g_x) / (3*f_x - g_x), x, oo)

if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')