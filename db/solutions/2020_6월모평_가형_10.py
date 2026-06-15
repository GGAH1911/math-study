from sympy import *
x = symbols('x')
integrand = x**3 * ln(x)
result = integrate(integrand, (x, 1, E))
answer = (3*E**4 + 1)/16
if simplify(result - answer) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')