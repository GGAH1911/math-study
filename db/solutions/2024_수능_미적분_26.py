from sympy import *
x = symbols('x')
A = (1 - 2*x) * cos(x)
V = integrate(A, (x, Rational(3,4)*pi, Rational(5,4)*pi))
V_s = simplify(V)
expected = 2*sqrt(2)*pi - sqrt(2)
if simplify(V_s - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('Computed:', V_s)
    print('Expected:', expected)