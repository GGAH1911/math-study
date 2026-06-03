import sympy as sp
x = sp.Symbol('x')
A = x**2 - 2*x + 1
B = 2*x**2 + 2*x - 2
result = A + B
expected = 3*x**2 - 1
if sp.simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')