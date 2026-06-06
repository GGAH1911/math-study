import sympy as sp
k = sp.Rational(3, 5)
f_k = 3 * (1 - k)
g_k = 3 * (k + 1)
result = f_k * g_k
expected = sp.Rational(144, 25)
if result == expected:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {result} != {expected}')