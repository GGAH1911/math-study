CANDIDATE = 32

from sympy import symbols, Eq, solve, Rational

a1, d = symbols('a1 d')
eq1 = Eq(a1 + 2*d, 2)   # a3 = 2
eq2 = Eq(a1 + 6*d, 62)  # a7 = 62

sol = solve([eq1, eq2], [a1, d])
a1_val = sol[a1]
d_val = sol[d]

a5 = a1_val + 4*d_val

if a5 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {a5}, got {CANDIDATE}')
