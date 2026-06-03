from sympy import symbols, Rational, solve
a1, r3 = symbols('a1 r3', real=True, positive=True)
eq1 = a1 * (1 + r3 + r3**2) - 3
eq2 = a1 * r3 * (1 + r3 + r3**2) - 6
sol = solve([eq1, eq2], [a1, r3])
r3_val = sol[0][1]
a1_val = sol[0][0]
a10 = a1_val * r3_val**3
if a10 == Rational(24, 7):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')