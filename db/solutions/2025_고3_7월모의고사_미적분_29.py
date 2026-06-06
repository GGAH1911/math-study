import sympy as sp
a1 = 24
r = -sp.Rational(1, 2)
result = a1 / (1 - r)
if result == 16:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {result}')