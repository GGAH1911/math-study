from math import comb
k = 1
coeff = comb(5, k) * (3**k)
print(f'{coeff}')
assert coeff == 15, f'Expected 15, got {coeff}'
print('VERIFY_PASS')