from sympy import symbols, expand

x = symbols('x')
expr = (x**2 - 1/x)**2 * (x - 2)**5
expanded = expand(expr)
coeff = expanded.coeff(x, 1)

if coeff == 104:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')