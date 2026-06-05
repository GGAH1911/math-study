from sympy import *
t = symbols('t', real=True, positive=True)
OP2 = t**4 - 7*t**2 + 16
PA2 = t**4 - 7*t**2 + 12
S = 8*sqrt(PA2)/OP2
T = 2*PA2**Rational(3,2)/OP2
ratio = simplify(T/S - PA2/4)
assert ratio == 0, 'ratio mismatch'
lim1 = limit(T/((t-2)*S), t, 2, '+')
lim2 = limit(T/((t**4-2)*S), t, oo)
result = lim1 + lim2
if result == Rational(5,4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)
