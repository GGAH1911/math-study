import sympy as sp

t = sp.Symbol('t')
v_t = -4*t + 5
x_t = sp.integrate(v_t, t) + 14

position_at_3 = x_t.subs(t, 3)
position_at_0 = x_t.subs(t, 0)

if position_at_3 == 11 and position_at_0 == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')