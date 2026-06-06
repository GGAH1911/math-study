from sympy import symbols, expand
x, y = symbols('x y')
expr = (x + 2*y)**3
expanded = expand(expr)
coeff = expanded.coeff(x*y**2)
result = 'VERIFY_PASS' if coeff == 12 else 'VERIFY_FAIL'
print(result)