from math import comb, gcd

CANDIDATE = 46

# 전체 공: 흰(1,2,3,4), 검은(3,4,5,6)
white_balls = [1, 2, 3, 4]
black_balls = [3, 4, 5, 6]

# 모든 4개 조합 생성
from itertools import combinations

all_balls = [(i, 'W') for i in white_balls] + [(i, 'B') for i in black_balls]
all_combos = list(combinations(range(8), 4))

# 같은 숫자가 있는 경우와 검은 공이 2개인 경우를 세기
same_number_count = 0
same_and_2black_count = 0

for combo in all_combos:
    numbers = [all_balls[i][0] for i in combo]
    ball_types = [all_balls[i][1] for i in combo]
    black_count = sum(1 for t in ball_types if t == 'B')
    
    # 같은 숫자가 있는지 확인
    has_duplicate = len(numbers) != len(set(numbers))
    
    if has_duplicate:
        same_number_count += 1
        if black_count == 2:
            same_and_2black_count += 1

# 조건부 확률 = same_and_2black_count / same_number_count
if same_number_count > 0:
    # 기약분수로 표현
    from math import gcd
    g = gcd(same_and_2black_count, same_number_count)
    q = same_and_2black_count // g
    p = same_number_count // g
    answer = p + q
    
    if answer == CANDIDATE:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')