import sympy as sp
x, m = sp.symbols('x m')
f = -sp.Rational(1, 3) * x**3 + 2 * x**2 + m * x + 1
f_prime = sp.diff(f, x)
m_value = -3
f_prime_at_3 = f_prime.subs([(x, 3), (m, m_value)])
f_double_prime = sp.diff(f_prime, x)
f_double_prime_at_3 = f_double_prime.subs(x, 3)
print('f\'(3) =', f_prime_at_3)
print('f\"(3) =', f_double_prime_at_3)
if f_prime_at_3 == 0 and f_double_prime_at_3 < 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')