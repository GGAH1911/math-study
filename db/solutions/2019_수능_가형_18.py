import sympy as sp
from sympy import sin, cos, tan, limit, symbols, simplify

theta = symbols('theta', real=True, positive=True)

# S(theta)
S = theta / (2 * (1 + sin(theta))**2)

# T(theta)
T = sin(theta) * (1 + sin(theta) - cos(theta)) / (2 * cos(theta) * (1 + sin(theta)))

# [S(theta)]^2 / T(theta)
ratio = (S**2) / T
result = limit(ratio, theta, 0, '+')

print(f'Limit: {result}')
if result == sp.Rational(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')