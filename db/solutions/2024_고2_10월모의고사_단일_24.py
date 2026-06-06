import sympy as sp
x = sp.Symbol('x')
f = 2*x**3 + 3*x**2 + 3*x

# 조건 1 검증
lim1 = sp.limit((f - 2*x**3) / x**2, x, sp.oo)
if lim1 == 3:
    cond1 = True
else:
    cond1 = False

# 조건 2 검증
lim2 = sp.limit(f / x, x, 0)
if lim2 == 3:
    cond2 = True
else:
    cond2 = False

# f(2) 계산
f_of_2 = f.subs(x, 2)

if cond1 and cond2 and f_of_2 == 34:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')