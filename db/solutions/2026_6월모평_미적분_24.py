import numpy as np
from sympy import *

x, y = symbols('x y', real=True)

# 원래 곡선 방정식
F = 3*x + y + cos(x*y) - 2

# 점 (0,1) 검증
assert F.subs([(x,0),(y,1)]) == 0, 'Point not on curve'

# 음함수 미분: dy/dx = -F_x / F_y
F_x = diff(F, x)
F_y = diff(F, y)
slope = (-F_x / F_y).subs([(x,0),(y,1)])
assert slope == -3, f'Expected slope -3, got {slope}'

# 접선: y = -3x + 1, x절편 = 1/3
tangent = lambda xv: -3*xv + 1
x_intercept = Rational(1, 3)
assert tangent(x_intercept) == 0, 'x-intercept wrong'

print('VERIFY_PASS')
