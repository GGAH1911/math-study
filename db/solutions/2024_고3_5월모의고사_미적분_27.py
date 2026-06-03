import sympy as sp

x_sym = sp.Symbol('x')
# 원래 함수
f = x_sym**3 + x_sym + 1
f_prime = sp.diff(f, x_sym)

# g(3): f(a)=3 의 실수 근
a = sp.Symbol('a')
roots = sp.solve(a**3 + a + 1 - 3, a)
real_roots = [r for r in roots if sp.im(r) == 0]
g3 = real_roots[0]  # should be 1

# g'(3) = 1/f'(g(3))
f_prime_at_g3 = f_prime.subs(x_sym, g3)
g_prime_3 = sp.Rational(1, 1) / f_prime_at_g3

# dy/dx at t=3
dx_dt = g_prime_3 + 1
dy_dt = g_prime_3 - 1
dy_dx = dy_dt / dx_dt

expected = sp.Rational(-3, 5)
if sp.simplify(dy_dx - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', float(dy_dx))
