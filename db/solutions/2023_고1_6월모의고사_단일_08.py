from sympy import I, simplify, expand
x = 1 - 2*I
y = 1 + 2*I
result = x**3*y + x*y**3 - x**2 - y**2
result = simplify(result)
if result == -24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')