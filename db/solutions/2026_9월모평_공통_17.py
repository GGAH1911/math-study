from sympy import symbols, integrate, diff
x = symbols('x')
f_prime_given = 3*x**2 + 2*x + 1
f_antiderivative = integrate(f_prime_given, x)
C = 3
f = f_antiderivative + C
f_at_1 = f.subs(x, 1)
f_at_2 = f.subs(x, 2)
f_prime_check = diff(f, x)
verify_derivative = (f_prime_check - f_prime_given).simplify()
verify_condition = f_at_1 == 6
if verify_condition and verify_derivative == 0 and f_at_2 == 17:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')