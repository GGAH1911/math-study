from sympy import symbols, expand, solve, Poly

x, a = symbols('x a', real=True)
eq = x**3 + 5*x**2 + (a-6)*x - a

# 검증 a = -7
a_val = -7
eq_a7 = eq.subs(a, a_val)
roots_a7 = solve(eq_a7, x)
print('a=-7:', sorted(set(roots_a7)), 'count:', len(set(roots_a7)))
assert len(set(roots_a7)) == 2, f'a=-7: 서로 다른 실근이 2개가 아님'

# 검증 a = 9
a_val = 9
eq_a9 = eq.subs(a, a_val)
roots_a9 = solve(eq_a9, x)
print('a=9:', sorted(set(roots_a9)), 'count:', len(set(roots_a9)))
assert len(set(roots_a9)) == 2, f'a=9: 서로 다른 실근이 2개가 아님'

# 합이 2인지 확인
sum_a = -7 + 9
assert sum_a == 2, f'합이 2가 아님: {sum_a}'
print('VERIFY_PASS')