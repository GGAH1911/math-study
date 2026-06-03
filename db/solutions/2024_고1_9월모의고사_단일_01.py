from sympy import symbols, expand
x, y = symbols('x y')
A = x**2 + 3*x*y + 2*y**2
B = 2*x**2 - 3*x*y - y**2
result = A + B
expected = 3*x**2 + y**2
if expand(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')