import sympy as sp
from sympy import symbols, integrate, Abs

t = symbols('t', real=True)
v = -3*t**2 + 6*t
s = integrate(v, t)

a_val = 3
s0 = s.subs(t, 0)
s2 = s.subs(t, 2)
s6 = s.subs(t, 2*a_val)

distance = Abs(s2 - s0) + Abs(s6 - s2)

if distance == 116:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')