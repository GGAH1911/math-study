import sympy as sp
x, a = sp.symbols('x a', real=True)
f = 2*x**3 - 9*x**2 + a*x + 5
f_prime = sp.diff(f, x)
eq_at_1 = f_prime.subs(x, 1)
a_val = sp.solve(eq_at_1, a)[0]
f_prime_concrete = f_prime.subs(a, a_val)
crit_points = sp.solve(f_prime_concrete, x)
f_double_prime = sp.diff(f_prime_concrete, x)
test_1 = f_double_prime.subs(x, 1)
test_b = f_double_prime.subs(x, 2)
result = a_val + 2 if a_val == 12 and test_1 < 0 and test_b > 0 else -1
print('VERIFY_PASS' if result == 14 else 'VERIFY_FAIL')