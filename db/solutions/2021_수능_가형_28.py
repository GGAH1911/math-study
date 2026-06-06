from sympy import *
x_sym = symbols('x')
a_val, b_val = 0, 5
def g(t): return t**3 + t + 1
def f(x): return x * (x - b_val)**2
assert g(a_val) == 1
assert g(1) == 3
g_prime_1 = 4
f_expr = x_sym * (x_sym - b_val)**2
f_prime_at_1 = float(diff(f_expr, x_sym).subs(x_sym, 1))
h_prime_3 = f_prime_at_1 / g_prime_1
f8 = f(8)
print('VERIFY_PASS' if abs(h_prime_3 - 2) < 1e-9 and f8 == 72 else 'VERIFY_FAIL')