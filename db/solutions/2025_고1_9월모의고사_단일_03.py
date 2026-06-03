from sympy import I, symbols, re, im
z = 1 + 3*I
z_conj = 1 - 3*I
result = (z + z_conj) * I
expected = 2*I
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')