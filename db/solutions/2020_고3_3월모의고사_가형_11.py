from itertools import combinations
from math import comb

# 방법 1: 직접 세기
count = 0
for white_pos in combinations(range(8), 2):
    # 흰 공이 이웃하지 않는지 확인
    if white_pos[1] - white_pos[0] <= 1:
        continue
    
    # 나머지 6개 위치 중 빨간 공 2개 배치
    remaining = [i for i in range(8) if i not in white_pos]
    for red_pos in combinations(remaining, 2):
        count += 1

# 방법 2: 이론적 계산
non_adjacent_white = sum(1 for w1, w2 in combinations(range(8), 2) if w2 - w1 > 1)
red_arrangements = comb(6, 2)
theoretical = non_adjacent_white * red_arrangements

if count == 315 and theoretical == 315:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')