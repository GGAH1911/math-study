from sympy import symbols, expand
x = symbols('x')
A = x**2 - x + 1
B = -x**2 + 2*x
result = A + B
result_simplified = expand(result)
expected = x + 1
if expand(result_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')