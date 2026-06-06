import sympy as sp
from sympy import integrate, symbols, sqrt, Piecewise

x = symbols('x', real=True)

# Define f(x) piecewise
f = Piecewise(
    (x**2 + 1, (x >= 0) & (x < 1)),
    (3*x - 1, (x >= 1) & (x <= 2))
)

# Compute the integral
integral_result = integrate(f, (x, 0, 2))

# Check if it equals 29/6
expected = sp.Rational(29, 6)

if integral_result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')