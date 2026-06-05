import sympy as sp
x = sp.Symbol('x')
f = -3*x**3 + 12*x**2
g = lambda t: (12)*t

f_at_2 = f.subs(x, 2)
f_prime = sp.diff(f, x)
f_prime_at_2 = f_prime.subs(x, 2)

assert f_at_2 == 2*f_prime_at_2, f'f(2)={f_at_2}, 2f\'(2)={2*f_prime_at_2}'
assert abs(g(2) - f_at_2) < 1e-10, f'g(2)={g(2)}, f(2)={f_at_2}'
assert abs(f_prime_at_2 - 12) < 1e-10, f'f\'(2)={f_prime_at_2}'

integrand = -(-3*x*(x-2)**2)
area = sp.integrate(integrand, (x, 0, 2))
assert abs(float(area) - 4.0) < 1e-10, f'Area={area}'
print('VERIFY_PASS')