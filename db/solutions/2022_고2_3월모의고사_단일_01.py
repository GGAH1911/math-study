from sympy import symbols, expand
x, y = symbols('x y')
A = 3*x**2 - 2*x*y + y**2
B = x**2 + x*y - y**2
result = expand(A - B)
expected = 2*x**2 - 3*x*y + 2*y**2
if expand(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')