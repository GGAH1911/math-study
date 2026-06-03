from sympy import symbols, expand
x, y = symbols('x y')
A = 2*x**2 + 3*y**2 - 2
B = x**2 - y**2
result = A - B
expected = x**2 + 4*y**2 - 2
if expand(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')