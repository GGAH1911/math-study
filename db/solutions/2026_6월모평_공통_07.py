import sympy as sp
x = sp.Symbol('x')
f_val = 2
f_prime_val = 1
g_prime_at_3 = 10*3 + f_val + 3*f_prime_val
if g_prime_at_3 == 35:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')