from sympy import symbols, expand
x = symbols('x')
A = 3*x**2 - 5*x + 1
B = 2*x**2 + x + 3
result = expand(A - B)
expected = x**2 - 6*x - 2
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')