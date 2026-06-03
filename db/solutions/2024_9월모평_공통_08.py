import sympy as sp
x = sp.Symbol('x')
f = 2*x**3 - 3*x**2 + 4
f_prime = sp.diff(f, x)
f_1_value = 3
verify_derivative = f_prime - (6*x**2 - 2*f_1_value*x)
verify_f_0 = f.subs(x, 0) - 4
verify_f_1 = f.subs(x, 1) - f_1_value
verify_f_2 = f.subs(x, 2)
if verify_derivative == 0 and verify_f_0 == 0 and verify_f_1 == 0 and verify_f_2 == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')