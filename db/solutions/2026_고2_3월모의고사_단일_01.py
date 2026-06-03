from sympy import symbols, expand
x = symbols('x')
A = 2*x**2 + 3*x - 1
B = -x**2 - 2*x + 3
result = expand(A + B)
expected = x**2 + x + 2
if expand(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')