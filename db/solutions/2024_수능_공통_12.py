from sympy import *
x = symbols('x')
f = Rational(1,9)*x*(x-6)*(x-9)
t = Rational(3)
f_t = f.subs(x, t)
area1 = integrate(f, (x, 0, t))
u = symbols('u')
area2 = integrate(-u + f_t, (u, 0, f_t))
total = area1 + area2
fp = diff(f, x)
fp_t = fp.subs(x, t)
cond1 = Eq(fp_t, -1)
cond2 = Eq(total, Rational(129,4))
if cond1 and cond2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
