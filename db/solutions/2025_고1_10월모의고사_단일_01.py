from sympy import symbols, expand

x, y = symbols('x y')
A = 2*x**2 + x*y - 2*y
B = x**2 + x*y + y
result = expand(A - B)
expected = x**2 - 3*y

if expand(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')