from sympy import symbols, solve, im, prod as sprod, sqrt, I, Rational

x, a = symbols('x a')
eq = x**4 + (3 - 2*a)*x**2 + a**2 - 3*a - 10

# Condition: -2 <= a < 5 for both real and complex roots

# Check ㄱ: a=1, product of real roots = -3
a1 = 1
roots1 = solve(eq.subs(a, a1), x)
real1 = [r for r in roots1 if im(r) == 0]
prod1 = 1
for r in real1:
    prod1 *= r
assert prod1 == -3, f'ㄱ failed: {prod1}'
print('ㄱ PASS: product of real roots =', prod1)

# Check ㄴ: product of real roots = -4 => a=2, product of complex roots = 3
a2 = 2
roots2 = solve(eq.subs(a, a2), x)
real2 = [r for r in roots2 if im(r) == 0]
comp2 = [r for r in roots2 if im(r) != 0]
prod_r2 = 1
for r in real2:
    prod_r2 *= r
prod_c2 = 1
for r in comp2:
    prod_c2 *= r
assert prod_r2 == -4, f'ㄴ real failed: {prod_r2}'
assert prod_c2 == 3, f'ㄴ complex failed: {prod_c2}'
print('ㄴ PASS: real product =', prod_r2, ', complex product =', prod_c2)

# Check ㄷ: a values giving integer roots, sum = -1
a_candidates = [-2, -1, 2]
for av in a_candidates:
    rts = solve(eq.subs(a, av), x)
    int_roots = [r for r in rts if im(r) == 0 and r == int(r)]
    assert len(int_roots) > 0, f'No integer roots for a={av}'
    print(f'a={av}: integer roots = {int_roots}')
assert sum(a_candidates) == -1, f'ㄷ sum failed: {sum(a_candidates)}'
print('ㄷ PASS: sum of a =', sum(a_candidates))

print('VERIFY_PASS')