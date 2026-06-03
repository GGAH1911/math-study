from sympy import symbols, expand, Poly
x, y, a = symbols('x y a')
expr = expand((4*x - a*y + 2)**2)
a_val = -4
expr_sub = expand(expr.subs(a, a_val))
p = Poly(expr_sub, x, y)
coef_x2 = p.coeff_monomial(x**2)
coef_y = p.coeff_monomial(y)
print('VERIFY_PASS' if coef_x2 == coef_y else 'VERIFY_FAIL')
