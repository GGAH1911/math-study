from itertools import combinations
from fractions import Fraction

# 공 정의: (색, 번호)
white_balls = [(1, 1), (1, 2)]  # 흰 공: 1번, 2번
black_balls = [(2, 1), (2, 2), (2, 2), (2, 2)]  # 검은 공: 1번, 2번(3개)
all_balls = white_balls + black_balls

# 3개 선택의 모든 경우
all_combinations = list(combinations(range(6), 3))
total_cases = len(all_combinations)  # 20

# 사건 A: 흰 공 1개, 검은 공 2개
A_count = 0
for indices in all_combinations:
    white_count = sum(1 for i in indices if all_balls[i][0] == 1)
    black_count = sum(1 for i in indices if all_balls[i][0] == 2)
    if white_count == 1 and black_count == 2:
        A_count += 1

# 사건 B: 곱이 8
B_count = 0
for indices in all_combinations:
    product = 1
    for i in indices:
        product *= all_balls[i][1]
    if product == 8:
        B_count += 1

# 사건 A∩B
AB_count = 0
for indices in all_combinations:
    white_count = sum(1 for i in indices if all_balls[i][0] == 1)
    black_count = sum(1 for i in indices if all_balls[i][0] == 2)
    product = 1
    for i in indices:
        product *= all_balls[i][1]
    if white_count == 1 and black_count == 2 and product == 8:
        AB_count += 1

prob = Fraction(A_count + B_count - AB_count, total_cases)
if prob == Fraction(13, 20):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')