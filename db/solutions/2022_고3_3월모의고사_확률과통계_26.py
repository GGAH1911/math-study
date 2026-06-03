from math import comb
A, P, B = (0, 0), (2, 3), (5, 0)
paths_AP = comb(2 + 3, 2)
paths_PB = comb(3 + 3, 3)
result = paths_AP * paths_PB
print('VERIFY_PASS' if result == 200 else f'VERIFY_FAIL: {result}')