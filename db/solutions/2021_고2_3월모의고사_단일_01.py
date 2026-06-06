from sympy import symbols, simplify
x, y = symbols('x y')
A = 3*x**2 + 2*x*y
B = -x**2 + x*y
result = A + 2*B
expected = x**2 + 4*x*y
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')