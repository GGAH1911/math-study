import sympy as sp
x = sp.Symbol('x')
a, b = -2, -5

# 첫 번째 방정식 검증
eq1 = x**3 + a*x**2 + b*x - 3*a
roots1 = sp.solve(eq1, x)
print(f'First equation roots: {roots1}')
assert all(r in [-2, 1, 3] for r in roots1), f'First equation check failed'
assert len(set(roots1)) == 3, 'Roots not distinct'
assert a in roots1, 'a not in roots'

# 두 번째 방정식 검증
eq2 = x**3 + b*x**2 - 2*a*x - 2*a*b
roots2 = sp.solve(eq2, x)
integer_roots = [r for r in roots2 if r.is_integer]
print(f'Second equation integer roots: {integer_roots}')
assert len(integer_roots) == 1, f'Expected 1 integer root, got {len(integer_roots)}'

print('VERIFY_PASS')