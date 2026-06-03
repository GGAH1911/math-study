from sympy import sqrt, simplify, symbols
x = (4 - sqrt(7)) / 3
result = 3*x**3 - 5*x**2 + 4*x + 7
result_simplified = simplify(result)
expected = 16 - 3*sqrt(7)
if simplify(result_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')