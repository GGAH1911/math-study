from sympy import *
x = symbols('x')
integral = integrate(sqrt(1 + 3*x), (x, 0, 1))
answer = Rational(14, 9)
if simplify(integral - answer) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: integral={integral}, answer={answer}')