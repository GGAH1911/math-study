from sympy import symbols, expand
x, y, z = symbols('x y z')
expr = (4*x - y - 3*z)**2
expanded = expand(expr)
coeff_yz = expanded.coeff(y*z)
print('VERIFY_PASS' if coeff_yz == 6 else 'VERIFY_FAIL')