from sympy import symbols, integrate, solve, Rational
a = symbols('a', positive=True, real=True)
left = integrate(4*a**2 - 3*a, (a, 0, a))
right = integrate(a**2 + a, (a, 0, a))
eq = left - right
sol = solve(eq, a)
if sol and sol[0] == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')