from itertools import product

# 주사위 눈: 1~6
dice_values = range(1, 7)
all_outcomes = list(product(dice_values, repeat=2))

# 조건을 만족하는 경우
satisfying = []
for a, b in all_outcomes:
    if abs(a - 3) + abs(b - 3) == 2 or a == b:
        satisfying.append((a, b))

# 답 검증
probability = len(satisfying) / len(all_outcomes)
expected = 1/3

if abs(probability - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')