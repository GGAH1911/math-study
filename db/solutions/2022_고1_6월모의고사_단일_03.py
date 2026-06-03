from sympy import symbols, Rational
x = symbols('x')
P = x**3 + x**2 + x + 1
result = P.subs(x, Rational(1, 2))
expected = Rational(15, 8)
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')