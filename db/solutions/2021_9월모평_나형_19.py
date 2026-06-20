from itertools import combinations

# 1부터 6까지의 수
cards = list(range(1, 7))

# 두 장을 선택하는 모든 경우
pairs = list(combinations(cards, 2))

# 각 쌍에서 작은 수, 큰 수
pairs_sorted = [(min(p), max(p)) for p in pairs]

count_total = 0
count_intersect = 0

for a1, a2 in pairs_sorted:
    for b1, b2 in pairs_sorted:
        count_total += 1
        # A ∩ B ≠ ∅ 조건: max(a1, b1) ≤ min(a2, b2)
        if max(a1, b1) <= min(a2, b2):
            count_intersect += 1

prob = count_intersect / count_total
expected = 13 / 15

if abs(prob - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {prob} != {expected}')