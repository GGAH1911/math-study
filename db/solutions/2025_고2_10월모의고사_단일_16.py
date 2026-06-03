import sympy as sp
x = sp.Symbol('x')

f = x**2 - 5*x + 4
g = x**2 - 2*x + 1

# 조건 1: f(1) = 0
cond1 = f.subs(x, 1)
if cond1 != 0:
    print('VERIFY_FAIL')

# 조건 2: 극한이 0
limit_expr = (f.subs(x, x+3) * g) / (f**2)
limit_val = sp.limit(limit_expr, x, 1)
if limit_val != 0:
    print('VERIFY_FAIL')

# 답 검증
ans = f.subs(x, 5) + g.subs(x, 5)
if ans == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')