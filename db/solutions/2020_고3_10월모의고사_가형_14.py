import numpy as np
from scipy import integrate
from sympy import *

CANDIDATE = -1

# 정적분 계산: ∫₀^π (x/π)sin(x) dx
x = symbols('x')
integrand = (x / pi) * sin(x)
result = integrate(integrand, (x, 0, pi))

# 극한값: -∫₀^π (x/π)sin(x) dx
limit_value = -float(result)

if abs(limit_value - CANDIDATE) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')