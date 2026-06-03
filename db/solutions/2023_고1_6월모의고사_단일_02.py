from sympy import symbols, expand
x = symbols('x')
A = 2*x**2 - 4*x + 3
B = -x**2 + 9*x + 6
result = expand(A + B)
expected = x**2 + 5*x + 9
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')