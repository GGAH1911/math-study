import sympy as sp
x = sp.Symbol('x')
P = x**3 - 3*x**2 + x + 5

# 조건 (가) 검증: P(x)=0의 근
roots = sp.solve(P, x)
real_roots = [r for r in roots if r.is_real]
complex_roots = [r for r in roots if not r.is_real]

assert len(real_roots) == 1 and len(complex_roots) == 2, 'Real/complex root count mismatch'
assert abs(complex_roots[0] * complex_roots[1] - 5) < 1e-9, 'Complex root product should be 5'

# 조건 (나) 검증: P(3x-1)=0의 근
P_sub = P.subs(x, 3*x - 1)
roots_sub = sp.solve(P_sub, x)
zero_root = [r for r in roots_sub if r == 0]
complex_roots_sub = [r for r in roots_sub if r != 0]

assert len(zero_root) == 1, 'Should have root at x=0'
assert len(complex_roots_sub) == 2, 'Should have 2 complex roots'
complex_sum = sum(complex_roots_sub)
assert abs(complex_sum - 2) < 1e-9, f'Complex root sum should be 2, got {complex_sum}'

print('VERIFY_PASS')