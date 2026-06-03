import numpy as np
from cmath import exp, pi

# z = -2i
z = -2j
z_conj = 2j

# 우변 계산
rhs = (z - z_conj) * 1j / 4
print(f'RHS = {rhs}')

# 좌변 계산 (n = 8, 16, ..., 96)
base = (1 - 1j) / np.sqrt(2)
valid_count = 0
for m in range(1, 13):
    n = 8 * m
    lhs = base ** n
    if abs(lhs - 1) < 1e-9:
        valid_count += 1
        print(f'n = {n}: {lhs:.10f} ✓')
    else:
        print(f'n = {n}: FAIL')

if valid_count == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')