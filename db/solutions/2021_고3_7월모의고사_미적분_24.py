import numpy as np
from sympy import *

x = symbols('x')
integrand = 2*cos(2*x)*sin(2*x)**2
result = integrate(integrand, (x, 0, pi/4))
print('Integral result:', result)
print('Simplified:', simplify(result))
print('Float value:', float(result))
if abs(float(result) - 1/3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')