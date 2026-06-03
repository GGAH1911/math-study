from math import comb
total = comb(8, 4)
favorable = comb(4, 2) * comb(4, 2) + comb(4, 3) * comb(4, 1) + comb(4, 4) * comb(4, 0)
result = favorable / total
if abs(result - 53/70) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')