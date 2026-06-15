from sympy import Rational, symbols, Eq, solve
PB = symbols('PB')
PA = Rational(1,3)
PAc = 1 - PA
PAB = PA*PB  # independence
sol = solve(Eq(PAc, 7*PAB), PB)
val = sol[0]
print('VERIFY_PASS' if val == Rational(2,7) else 'VERIFY_FAIL')