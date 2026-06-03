import sympy as sp
x, k = sp.symbols('x k', real=True)
f = x**3 - (k/2)*x**2 + x + 1
f_prime = sp.diff(f, x)

# 검증 조건들
cond1 = sp.Eq(f.subs(x, 0), 1)
cond2 = sp.Eq(f.subs(x, 2), 1)
cond3 = sp.Eq(f_prime, 3*x**2 - k*x + 1)

# 조건 3은 정의상 자동 만족
sol = sp.solve([cond1, cond2], [k])
k_val = sol[k]

if k_val == 5:
    f_actual = x**3 - (5/2)*x**2 + x + 1
    if float(f_actual.subs(x, 0)) == 1 and float(f_actual.subs(x, 2)) == 1:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')