from itertools import combinations

# 모든 가능한 (a1, a2), (b1, b2) 쌍
cards = list(range(1, 7))
pairs = list(combinations(cards, 2))

# A ∩ B ≠ ∅인 경우를 계산
count_nonempty = 0
total = 0

for (a1, a2) in pairs:
    for (b1, b2) in pairs:
        total += 1
        # A ∩ B ≠ ∅ ⟺ a1 ≤ b2 AND b1 ≤ a2
        if a1 <= b2 and b1 <= a2:
            count_nonempty += 1

prob = count_nonempty / total
expected = 13 / 15

if abs(prob - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {prob}, expected {expected}')