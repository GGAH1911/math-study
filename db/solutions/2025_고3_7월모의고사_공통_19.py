import sympy as sp
x = sp.Symbol('x')
f = x**4 - 8*x**2 + 10
f_at_2 = f.subs(x, 2)
f_at_0 = f.subs(x, 0)
f_prime = sp.diff(f, x)
f_prime_at_2 = f_prime.subs(x, 2)
f_prime_at_0 = f_prime.subs(x, 0)
f_double_prime = sp.diff(f_prime, x)
f_double_prime_at_0 = f_double_prime.subs(x, 0)
f_double_prime_at_2 = f_double_prime.subs(x, 2)
verify = (f_at_2 == -6 and f_prime_at_2 == 0 and f_prime_at_0 == 0 and f_double_prime_at_0 < 0 and f_double_prime_at_2 > 0)
print('VERIFY_PASS' if verify else 'VERIFY_FAIL')