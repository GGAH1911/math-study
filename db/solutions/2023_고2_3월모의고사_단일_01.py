from sympy import symbols, expand
x = symbols('x')
A = x**3 + 2*x**2
B = 2*x**3 - x**2 - 1
result = A + B
expected = 3*x**3 + x**2 - 1
if expand(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')