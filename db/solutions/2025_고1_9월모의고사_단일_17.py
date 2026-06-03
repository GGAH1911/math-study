import sympy as sp
x = sp.Symbol('x')
f = 3*x**2 + 6*x + 15
g = 12*x + 12

# 조건 (가) 검증
check1 = f.subs(x, 0) - g.subs(x, 0)
check2 = f.subs(x, 2) - g.subs(x, 2)
assert check1 == 3, f'f(0)-g(0) = {check1}, expected 3'
assert check2 == 3, f'f(2)-g(2) = {check2}, expected 3'

# 조건 (나) 검증
eq = f + g
roots = sp.solve(eq, x)
assert len(roots) == 1, f'Expected single root, got {roots}'
root = roots[0]
assert sp.simplify(eq.subs(x, root)) == 0

# 답 검증
ans = f.subs(x, 3)
assert ans == 60, f'f(3) = {ans}, expected 60'
print('VERIFY_PASS')