from math import comb

# 전체: a+b+c+d=12, a,b,c,d>=0
total = comb(15, 3)

# a=2인 경우: b+c+d=10, b,c,d>=0
case_a2 = comb(12, 2)

# a+b+c=10인 경우: d=2, a+b+c=10, a,b,c>=0
case_abc10 = comb(12, 2)

# a=2 AND a+b+c=10: b+c=8, d=2
case_both = comb(9, 1)

# 포함-배제
violating = case_a2 + case_abc10 - case_both
valid = total - violating

# 검증
assert total == 455, f'Total should be 455, got {total}'
assert case_a2 == 66, f'case_a2 should be 66, got {case_a2}'
assert case_abc10 == 66, f'case_abc10 should be 66, got {case_abc10}'
assert case_both == 9, f'case_both should be 9, got {case_both}'
assert violating == 123, f'Violating should be 123, got {violating}'
assert valid == 332, f'Valid should be 332, got {valid}'

print('VERIFY_PASS')