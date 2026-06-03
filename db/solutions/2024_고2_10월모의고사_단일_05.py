import sympy as sp
from sympy import symbols, limit, oo, simplify

x = symbols('x', real=True, positive=True)

# 왼쪽 경계 극한
left_limit = limit(x * (3 / (2*x + 1)), x, oo)

# 오른쪽 경계 극한
right_limit = limit(x * (3 / (2*x - 1)), x, oo)

# 두 극한이 같은지 확인
if left_limit == right_limit == sp.Rational(3, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')