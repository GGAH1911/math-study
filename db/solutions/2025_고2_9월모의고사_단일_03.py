from sympy import symbols, Eq, solve
a1 = symbols('a1')
d = 5
# a_n = a1 + (n-1)*d
a3 = a1 + 2*d
sol = solve(Eq(a1 + a3, 16), a1)
assert len(sol) == 1
a1_val = sol[0]
a4 = a1_val + 3*d
print('VERIFY_PASS' if a4 == 18 else 'VERIFY_FAIL')