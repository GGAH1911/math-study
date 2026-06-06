from sympy import symbols, expand
x, y = symbols('x y')
A = x**2 - 2*x*y + y**2
B = 3*x*y - y**2
result = A + B
expected = x**2 + x*y
if expand(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')