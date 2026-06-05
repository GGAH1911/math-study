from math import factorial
from itertools import permutations

# 원래 카드 생성
cards = [1, 2, 3, 3, 4, 4, 4]

# 모든 고유한 순열 생성
def unique_permutations(elements):
    if len(elements) == 1:
        return [elements]
    unique_perms = []
    for i, val in enumerate(elements):
        if elements[:i].count(val) == 0:
            for perm in unique_permutations(elements[:i] + elements[i+1:]):
                unique_perms.append([val] + perm)
    return unique_perms

all_perms = unique_permutations(cards)

# 1과 2 사이에 2장 이상 있는 경우 세기
count = 0
for perm in all_perms:
    idx_1 = perm.index(1)
    idx_2 = perm.index(2)
    distance = abs(idx_1 - idx_2) - 1
    if distance >= 2:
        count += 1

if count == 200:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')