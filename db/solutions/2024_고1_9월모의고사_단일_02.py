from sympy import symbols, I, re, im
z = 1 - 2*I
z_conj = 1 + 2*I
result = z + z_conj
print('VERIFY_PASS' if result == 2 else 'VERIFY_FAIL')