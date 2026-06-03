from itertools import permutations

# 원탁 배치 (회전 중복 제거를 위해 A를 위치 0에 고정)
# A=0, B=1, C=2, 나머지=3,4,5,6

count_total = 0
count_neighbor = 0

# A를 위치 0에 고정, 나머지 6명을 위치 1~6에 배치
for perm in permutations(range(1, 7)):
    count_total += 1
    # perm = (위치1, 위치2, ..., 위치6)
    # 위치 0은 A, 위치 1~6은 perm 원소들
    arrangement = [0] + list(perm)
    
    # A(위치 0)의 이웃 확인
    # 원탁이므로 위치 0의 이웃은 위치 1과 위치 6
    left_neighbor = arrangement[6]
    right_neighbor = arrangement[1]
    
    # B=1 또는 C=2가 A의 이웃인지 확인
    if left_neighbor in [1, 2] or right_neighbor in [1, 2]:
        count_neighbor += 1

probability = count_neighbor / count_total
expected = 3/5

if abs(probability - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')