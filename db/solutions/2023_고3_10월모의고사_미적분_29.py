import sympy as sp
from sympy import sin, cos, limit, simplify, tan

theta = sp.Symbol('theta', positive=True, real=True)

# h = cot(theta/2) = 1/tan(theta/2)
h = 1/tan(theta/2)

# S(theta) = h/(1+h²)
S = h/(1 + h**2)

# Simplify to verify it equals (1/2)sin(theta)
S_simplified = simplify(S)
S_expected = sin(theta)/2

# Check if they're equal
verify_form = simplify(S_simplified - S_expected)

# Calculate the limit
limit_value = limit(S/theta, theta, 0, '+')

# Calculate 60 times the limit
result = 60 * limit_value

if verify_form == 0 and result == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')