from sympy import symbols, expand
x, y = symbols('x y')
A = 2*x**2 + x*y + y**2
B = x**2 + 2*x*y - y**2
result = A + B
answer_form = 3*x**2 + 3*x*y
if expand(result - answer_form) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')