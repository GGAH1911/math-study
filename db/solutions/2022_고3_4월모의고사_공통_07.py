from sympy import symbols, diff, limit, simplify
x = symbols('x')
f_3 = 2
f_prime_3 = 1
p = -6
q = 11
g = x**2 + p*x + q
g_3 = g.subs(x, 3)
g_prime = diff(g, x)
g_prime_3 = g_prime.subs(x, 3)
verify_limit_numerator = f_prime_3 - g_prime_3
if g_3 == f_3 and g_prime_3 == 0 and verify_limit_numerator == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')