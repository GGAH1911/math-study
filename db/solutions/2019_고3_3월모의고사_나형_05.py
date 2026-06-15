from sympy import Rational, summation, symbols, oo
n = symbols('n', positive=True, integer=True)
a1 = Rational(3)
r = Rational(1, 2)
term = a1 * r**(n-1)
S = summation(term, (n, 1, oo))
expected = 6
if S == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
