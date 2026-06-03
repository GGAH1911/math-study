import sympy as sp
x = sp.Symbol('x')
A = 3*x**2 + 2*x - 1
B = -x**2 + x + 3
answer_expr = 2*x**2 + 3*x + 2
result = sp.expand(A + B)
if sp.simplify(result - answer_expr) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')