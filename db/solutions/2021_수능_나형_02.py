from sympy import symbols, Eq, solve, Rational

a1 = Rational(1, 8)
r = symbols('r')

# a3/a2 = r = 2 조건
a2 = a1 * r
a3 = a1 * r**2
sol = solve(Eq(a3 / a2, 2), r)
r_val = sol[0]  # r = 2

a5 = a1 * r_val**4

# 검증
assert a3.subs(r, r_val) / a2.subs(r, r_val) == 2, 'ratio check failed'
assert a5 == 2, f'a5 expected 2, got {a5}'
print('VERIFY_PASS')