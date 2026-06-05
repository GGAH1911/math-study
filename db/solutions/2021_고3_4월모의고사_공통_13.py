import numpy as np
from sympy import symbols, integrate, expand, simplify

x = symbols('x')
f = (x - 1) * (x - 4)

integral_0_to_1 = integrate(f, (x, 0, 1))
integral_0_to_4 = integrate(f, (x, 0, 4))
integral_1_to_4 = integrate(f, (x, 1, 4))

print('Integral 0 to 1:', float(integral_0_to_1))
print('Expected: 11/6 =', 11/6)
print('Match 1:', abs(float(integral_0_to_1) - 11/6) < 1e-10)

print('\nIntegral 0 to 4:', float(integral_0_to_4))
print('Expected: -8/3 =', -8/3)
print('Match 2:', abs(float(integral_0_to_4) - (-8/3)) < 1e-10)

print('\nIntegral 1 to 4:', float(integral_1_to_4))
print('Area (absolute value):', abs(float(integral_1_to_4)))
print('Expected answer: 4.5')

if abs(float(integral_0_to_1) - 11/6) < 1e-10 and abs(float(integral_0_to_4) - (-8/3)) < 1e-10 and abs(abs(float(integral_1_to_4)) - 4.5) < 1e-10:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')