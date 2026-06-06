from sympy import symbols, diff, solve, simplify
a = symbols('a', real=True, positive=True)
f = (1/2) * (2 - a) * (3*a + 3)
s_a = simplify(f)
ds_da = diff(s_a, a)
critical = solve(ds_da, a)
if critical:
    a_opt = critical[0]
    s_max = s_a.subs(a, a_opt)
    print('Critical point:', a_opt)
    print('Maximum value:', s_max)
    print('Decimal:', float(s_max))
    if abs(float(s_max) - 27/8) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')