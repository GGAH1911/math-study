from sympy import symbols, solve, simplify

a1, d = symbols('a1 d', real=True)

eq1 = a1 + 2*d - 1
eq2 = 8*a1 + 160*d - 48

sol = solve([eq1, eq2], [a1, d])
a1_val = sol[a1]
d_val = sol[d]

a39 = a1_val + 38*d_val
a39_simplified = simplify(a39)

if a39_simplified == 11:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')