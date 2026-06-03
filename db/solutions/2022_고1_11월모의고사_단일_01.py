from sympy import symbols, simplify
x, y = symbols('x y')
A = x**2 + 2*x*y - 1
B = -2*x**2 + x*y + 1
result = A + B
expected = -x**2 + 3*x*y
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')