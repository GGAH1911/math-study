from sympy import symbols, solve, Eq
a1, d = symbols('a1 d')
eq1 = Eq(a1 + d, 6)
eq2 = Eq(2*a1 + 8*d, 36)
sol = solve([eq1, eq2], [a1, d])
a1_val, d_val = sol[a1], sol[d]
a10 = a1_val + 9*d_val
print('VERIFY_PASS' if a10 == 38 else 'VERIFY_FAIL')