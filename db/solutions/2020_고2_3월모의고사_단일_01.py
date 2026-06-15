from sympy import symbols, expand
x, y = symbols('x y')
A = 2*x**2 - 3*x*y
B = x**2 - 4*x*y - y**2
result = expand(A - B)
expected = x**2 + x*y + y**2
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')