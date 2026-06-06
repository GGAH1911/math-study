from itertools import combinations

# 공 정의: 인덱스 0-3은 흰공(1,2,3,4), 인덱스 4-7은 검은공(3,4,5,6)
white_nums = [1, 2, 3, 4]
black_nums = [3, 4, 5, 6]

# 모든 4개 조합
all_combos = list(combinations(range(8), 4))

# 조건 A: (흰3, 검3) 또는 (흰4, 검4) 모두 포함
# 흰3은 인덱스 2, 검3은 인덱스 4
# 흰4는 인덱스 3, 검4는 인덱스 5
condition_a = []
for combo in all_combos:
    has_3_pair = (2 in combo and 4 in combo)
    has_4_pair = (3 in combo and 5 in combo)
    if has_3_pair or has_4_pair:
        condition_a.append(combo)

# 조건 A 내에서 검은공이 2개인 경우
black_indices = {4, 5, 6, 7}
black_2 = []
for combo in condition_a:
    black_count = sum(1 for i in combo if i in black_indices)
    if black_count == 2:
        black_2.append(combo)

print(f'|A| = {len(condition_a)}')
print(f'|A ∩ (검은공 2개)| = {len(black_2)}')
print(f'확률 = {len(black_2)}/{len(condition_a)}')

from math import gcd
g = gcd(len(black_2), len(condition_a))
q = len(black_2) // g
p = len(condition_a) // g
print(f'기약분수 = {q}/{p}')
print(f'p + q = {p + q}')

if p + q == 46:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')