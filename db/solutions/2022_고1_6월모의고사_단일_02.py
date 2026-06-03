import sympy as sp
x = sp.Symbol('x')
A = 4*x**2 + 2*x - 1
B = x**2 + x - 3
result = A - 2*B
expected = 2*x**2 + 5
if sp.simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')