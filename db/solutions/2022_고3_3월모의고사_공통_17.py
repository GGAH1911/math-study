import sympy as sp
from scipy import integrate
import numpy as np

x = sp.Symbol('x')

# 첫 번째 적분: ∫_{-3}^{2} (2x³ + 6|x|) dx
# x < 0일 때 |x| = -x, x >= 0일 때 |x| = x
f1_neg = 2*x**3 - 6*x  # x in [-3, 0)
f1_pos = 2*x**3 + 6*x  # x in [0, 2]

integral1_neg = sp.integrate(f1_neg, (x, -3, 0))
integral1_pos = sp.integrate(f1_pos, (x, 0, 2))
integral1_total = integral1_neg + integral1_pos

# 두 번째 적분: ∫_{-3}^{-2} (2x³ - 6x) dx
f2 = 2*x**3 - 6*x
integral2 = sp.integrate(f2, (x, -3, -2))

# 최종 답
result = integral1_total - integral2

if result == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')