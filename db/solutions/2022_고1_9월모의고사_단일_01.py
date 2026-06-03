from sympy import symbols, expand, simplify
x, y = symbols('x y')
A = x**2 - 2*x*y + y**2
B = x**2 + 2*x*y + y**2
result = A + B
expected = 2*x**2 + 2*y**2
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')