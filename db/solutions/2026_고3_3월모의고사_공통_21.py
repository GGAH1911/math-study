import sympy as sp
x = sp.Symbol('x')
f = x**3 - 4*x
assert f.subs(x, 0) == 0
assert sp.Poly(f, x).LC() == 1
t = sp.Symbol('t')
integral = sp.integrate(t**3 - 4*t, (t, 0, 2))
g_2 = 2 * integral
assert g_2 == -8
f_4 = f.subs(x, 4)
assert f_4 == 48
print('VERIFY_PASS')