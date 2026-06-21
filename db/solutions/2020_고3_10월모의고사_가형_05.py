from sympy import symbols, expand, Rational
x, a = symbols('x a')
expr = (2*x + a/x)**7
expanded = expand(expr)
coeff_x3 = expanded.coeff(x, 3)
a_val = Rational(1, 4)
coeff_check = coeff_x3.subs(a, a_val)
if coeff_check == 42:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')