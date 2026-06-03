import sympy as sp
import numpy as np

x = sp.Symbol('x')
# 원래 문제의 단면 넓이: (2/sqrt(x))^2 = 4/x
# 부피 적분: int_1^4 4/x dx
integral = sp.integrate(4/x, (x, 1, 4))
target = 8 * sp.ln(2)

if sp.simplify(integral - target) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')