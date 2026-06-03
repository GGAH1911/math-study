import sympy as sp
x, a = sp.symbols('x a')
f = x**3 - x + 2
fp = sp.diff(f, x)
# 접선의 y절편 = f(a) - f'(a)*a, 이것이 4여야 함
eq = (f - fp*x).subs(x, a) - 4
roots = sp.solve(eq, a)
assert roots, 'no roots found'
results = []
for a_val in roots:
    slope = fp.subs(x, a_val)
    y_int = f.subs(x, a_val) - slope*a_val
    x_int = sp.solve(slope*x + y_int, x)
    results.extend(x_int)
answer = sp.Integer(-2)
if answer in results:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
