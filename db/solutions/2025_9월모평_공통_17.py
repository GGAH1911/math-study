import sympy as sp
x = sp.Symbol('x')
f_prime = 6*x**2 + 2*x + 1
f = sp.integrate(f_prime, x) + 1
f_at_1 = f.subs(x, 1)
f_at_0 = f.subs(x, 0)
f_prime_check = sp.diff(f, x)
assert f_at_0 == 1, f'f(0) = {f_at_0}, expected 1'
assert f_prime_check == f_prime, f'f\'(x) mismatch'
result = f_at_1
assert result == 5, f'f(1) = {result}, expected 5'
print('VERIFY_PASS')