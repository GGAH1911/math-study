from sympy import symbols, expand
x, a, b = symbols('x a b')
lhs = a*(x+2)**2 + 1
rhs = 2*x**2 + b*x + 9
lhs_expanded = expand(lhs)
coeffs_lhs = [lhs_expanded.coeff(x, i) for i in range(3)]
coeffs_rhs = [rhs.coeff(x, i) for i in range(3)]
a_val, b_val = 2, 8
verify_lhs = expand(2*(x+2)**2 + 1)
verify_rhs = 2*x**2 + 8*x + 9
if expand(verify_lhs - verify_rhs) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')