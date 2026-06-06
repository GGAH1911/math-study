from sympy import symbols, expand
x, y = symbols('x y')
k = 2
expr_original = x**2 + k*x*y - 3*y**2 + x + 11*y - 6
expr_factored = (x + 3*y - 2)*(x - y + 3)
result = expand(expr_factored) - expr_original
if result == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')