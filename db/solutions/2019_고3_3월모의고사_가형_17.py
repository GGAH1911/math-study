import sympy as sp
from sympy import sqrt, ln, integrate, symbols, exp, simplify

x = symbols('x', real=True, positive=True)
e_val = exp(1)

# 점 P의 좌표
x0 = sqrt(e_val)
y0 = sp.Rational(1, 2)

# 함수들
f = x**2 / (2*e_val)
g = ln(x)

# 넓이 계산
area1 = integrate(f, (x, 0, x0))
area2 = integrate(g, (x, 1, x0))
total_area = area1 - area2

# 단순화
result = simplify(total_area)
expected = (2*sqrt(e_val) - 3) / 3

if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')