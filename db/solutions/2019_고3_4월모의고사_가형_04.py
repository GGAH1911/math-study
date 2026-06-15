from sympy import symbols, log, solve, Rational
a = symbols('a', positive=True)
expr = log(a, 2) + 2 - 1
sol = solve(expr, a)
assert len(sol) == 1 and sol[0] == Rational(1,2), f'Expected 1/2, got {sol}'
print('VERIFY_PASS')