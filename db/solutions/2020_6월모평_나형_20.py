import sympy as sp
x = sp.Symbol('x')
# n=2 경우 검증
f = 4*x**2 + 10*x**3
n = 2
# 조건 2
lim2 = sp.limit(f/x**n, x, 0)
assert lim2 == 4, f'Condition 2 failed: {lim2}'
# 조건 1
num = f - 4*x**3 + 3*x**2
denom = x**(n+1) + 1
lim1 = sp.limit(num/denom, x, sp.oo)
assert lim1 == 6, f'Condition 1 failed: {lim1}'
f_1 = f.subs(x, 1)
assert f_1 == 14, f'f(1) calculation failed: {f_1}'
print('VERIFY_PASS')