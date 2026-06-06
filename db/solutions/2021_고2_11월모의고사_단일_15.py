import sympy as sp
a = 3
f_1 = a - 2
g_1 = 2 - a
f_prime_1 = 4
g_prime_1 = a
result = f_prime_1 * g_1 + f_1 * g_prime_1
if result == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')