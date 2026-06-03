import sympy as sp
x = sp.Symbol('x')
f = 2*x**2 - x - 1

# 첫 번째 조건: lim x→∞ f(x)/x² = 2
lim1 = sp.limit(f/x**2, x, sp.oo)
assert lim1 == 2, f'First limit failed: {lim1}'

# 두 번째 조건: lim x→1 f(x)/(x-1) = 3
lim2 = sp.limit(f/(x-1), x, 1)
assert lim2 == 3, f'Second limit failed: {lim2}'

# 답 검증
result = f.subs(x, 3)
assert result == 14, f'f(3) = {result}'

print('VERIFY_PASS')