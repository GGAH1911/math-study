import sympy as sp
from sympy import symbols, limit, expand

x = symbols('x', real=True)

# f(x)의 1 < x < 2 구간 정의
f = -2*(x - 1)**2 + 3

# a + b = -1인 경우를 검증 (예: a=0, b=-1)
a, b = 0, -1
poly = x**2 + a*x + b  # x^2 - 1 = (x-1)(x+1)

# 곱
product = expand(poly * f)

# 우극한 (x → 1+)
lim_right = limit(product, x, 1, '+')

# 좌극한 (x → 1-에서 (x^2 + ax + b) * 1)
lim_left = (1 + a + b) * 1

# 함수값
func_val = (1 + a + b) * 1

# 검증
if lim_right == lim_left == func_val == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')