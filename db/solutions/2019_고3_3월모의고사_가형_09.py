from itertools import permutations

# 1학년 2명(0,1), 2학년 2명(2,3), 3학년 1명(4)
students = [0, 1, 2, 3, 4]
count = 0
valid_arrangements = []

# 원형 배열이므로 0번 위치를 고정 (학생 4를 고정)
for perm in permutations([0, 1, 2, 3]):
    arrangement = [perm[0], perm[1], perm[2], perm[3], 4]
    # 학생 0과 1이 이웃하는지 확인
    pos_0 = arrangement.index(0)
    pos_1 = arrangement.index(1)
    
    # 원형이므로 거리가 1 또는 4인 경우가 이웃
    distance = min(abs(pos_0 - pos_1), 5 - abs(pos_0 - pos_1))
    
    if distance == 1:
        count += 1
        valid_arrangements.append(arrangement)

if count == 12:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count} instead of 12')