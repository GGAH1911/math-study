from sympy import symbols, expand, Poly

x = symbols('x')
expr = (x + 4) * (2*x**2 - 3*x + 1)
expanded = expand(expr)
poly = Poly(expanded, x)
coeffs = poly.all_coeffs()
x2_coeff = poly.nth(2)

if x2_coeff == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')