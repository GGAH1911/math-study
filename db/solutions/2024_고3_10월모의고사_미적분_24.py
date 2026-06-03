from sympy import integrate, cos, pi, symbols, sqrt, Rational, simplify
x = symbols('x')
val = integrate(cos(pi/3 - x), (x, 0, pi/3))
candidate = sqrt(3)/2
print('VERIFY_PASS' if simplify(val - candidate) == 0 else 'VERIFY_FAIL')