from math import comb
total_ways = comb(16, 3)
all_a = comb(9, 3)
prob_all_a = all_a / total_ways
prob_at_least_one_b = 1 - prob_all_a
expected = 17 / 20
if abs(prob_at_least_one_b - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')