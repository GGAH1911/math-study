from sympy import symbols, expand
x = symbols('x')
A = 2*x**2 + x + 3
B = x**2 + x + 2
result = A - B
expected = x**2 + 1
if expand(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')