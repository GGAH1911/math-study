from math import comb

total = comb(10, 4)
not_multiple_of_5 = comb(8, 4)
multiple_of_5 = total - not_multiple_of_5

probability = multiple_of_5 / total
expected = 2 / 3

if abs(probability - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')