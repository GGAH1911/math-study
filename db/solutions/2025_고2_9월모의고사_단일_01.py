from sympy import sympify, simplify
result = 2**3 * 4**(-1/2)
expected = 4
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')