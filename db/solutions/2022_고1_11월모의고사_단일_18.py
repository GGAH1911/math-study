from sympy import symbols, expand, factor
x = symbols('x')
f = lambda x_val: x_val**3 - 3*x_val**2 - 6*x_val + 13
f_x_plus_3 = lambda x_val: (x_val+3)**3 - 3*(x_val+3)**2 - 6*(x_val+3) + 13
diff = lambda x_val: f_x_plus_3(x_val) - f(x_val)
print('f(2) =', f(2), '(should be -3)')
print('f(0) =', f(0))
diff_expr = expand(diff(x))
quotient = factor(diff_expr / ((x-1)*(x+2)))
print('f(x+3) - f(x) / [(x-1)(x+2)] =', quotient, '(should be constant 9)')
if f(2) == -3 and quotient == 9 and f(0) == 13:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')