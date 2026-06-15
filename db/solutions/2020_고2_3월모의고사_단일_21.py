from sympy import symbols, diff, simplify, Rational
t = symbols('t', real=True, positive=True)
A = 6*t - 7*t**2 - 1
dA_dt = diff(A, t)
t_crit = -dA_dt.coeff(t, 1) / dA_dt.coeff(t, 0)
M = A.subs(t, Rational(3, 7))
a = Rational(1, 2)
result = a + M
print('VERIFY_PASS' if result == Rational(11, 14) else 'VERIFY_FAIL')