from sympy import symbols, diff

CANDIDATE = 6

t, a = symbols('t a')
x = t**3 - 3*t**2 + a*t
v = diff(x, t)

v_at_3 = v.subs([(t, 3), (a, CANDIDATE)])

if v_at_3 == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')