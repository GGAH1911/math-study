from sympy import symbols, expand
x = symbols('x')
k = 4
expr = 9*x**2 + 12*x + k
square_form = (3*x + 2)**2
if expand(expr) == expand(square_form):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')