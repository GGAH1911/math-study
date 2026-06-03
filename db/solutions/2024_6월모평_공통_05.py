from sympy import symbols, diff, simplify
x = symbols('x')
f_val_1 = 2
f_prime_1 = 3
g_prime_1 = 3 * (1)**2 * f_val_1 + (1**3 + 1) * f_prime_1
result = g_prime_1
if result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')