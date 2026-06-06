from sympy import symbols, expand
x, a = symbols('x a')
expr = (x + a)**3 + x*(x - 4)
expanded = expand(expr)
coeff_x2 = expanded.coeff(x, 2)
a_val = 3
coeff_check = coeff_x2.subs(a, a_val)
if coeff_check == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')