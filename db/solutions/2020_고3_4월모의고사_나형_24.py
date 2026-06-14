CANDIDATE = 22
from sympy import symbols, Eq, solve, Rational

d = symbols('d')
a1 = 6
a4 = a1 + 3*d
a10 = a1 + 9*d

# 원래 조건: 2*a4 = a10
sol = solve(Eq(2*a4, a10), d)
d_val = sol[0]

a9 = a1 + 8*d_val

if a9 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
