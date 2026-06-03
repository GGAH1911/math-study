from sympy import symbols, integrate, Rational
x = symbols('x')
f = x**2 + x
expr = 5*integrate(f, (x, 0, 1)) - integrate(5*x + f, (x, 0, 1))
result = expr
expected = Rational(5, 6)
print('VERIFY_PASS' if result == expected else f'VERIFY_FAIL: got {result}')