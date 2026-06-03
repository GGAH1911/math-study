import numpy as np
z = 1 - 1j
z_conj = 1 + 1j
frac_term = (1/z - 1/z_conj)
rhs = (z - 1) * 1j
for n in [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]:
    lhs = frac_term ** n
    if abs(lhs - rhs) < 1e-10:
        pass
    else:
        print('VERIFY_FAIL')
        exit()
print('VERIFY_PASS')