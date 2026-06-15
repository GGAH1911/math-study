from sympy import *
x = symbols('x')
result = integrate(exp(x + 3), (x, 0, ln(3)))
answer_value = 2 * E**3
if simplify(result - answer_value) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')