import sympy as sp
from sympy import sin, sqrt, limit, symbols

theta = symbols('theta', real=True, positive=True)
S = 2 * sin(theta) * sqrt(1 - 4*sin(theta)**2)

result = limit(S / theta, theta, 0, '+')
print(f'Limit value: {result}')

if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')