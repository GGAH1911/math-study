from sympy import symbols, diff
t, k = symbols('t k', real=True)
x = k*t**3 - 6*t**2 + t
v = diff(x, t)
a = diff(v, t)
# k=2일 때 조건 확인
v_at_k_2 = v.subs([(t, 2), (k, 2)])
if abs(v_at_k_2 - 1) < 1e-10:
    a_at_4 = a.subs([(t, 4), (k, 2)])
    if abs(a_at_4 - 36) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')