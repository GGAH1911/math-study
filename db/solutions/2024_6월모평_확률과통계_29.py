from sympy import symbols
import itertools

# 검은색 카드 위치 i, j에서 흰색 카드 배치
def verify_arrangement(i, j):
    # 조건 (나): j - i >= 3
    if j - i < 3:
        return False
    
    # 흰색 카드 위치 계산
    positions = sorted(set(range(1, 11)) - {i, j})
    # p[k-1]은 흰색 카드 k의 위치
    
    # 조건 (다): 3의 배수(3 또는 6)가 검은색 사이에 있어야 함
    p3 = positions[2]  # 카드 3의 위치
    p6 = positions[5]  # 카드 6의 위치
    
    # i < p3 < j 또는 i < p6 < j
    has_multiple_of_3 = (i < p3 < j) or (i < p6 < j)
    
    return has_multiple_of_3

# 모든 경우의 수 계산
count = 0
for i in range(1, 10):
    for j in range(i+1, 11):
        if verify_arrangement(i, j):
            count += 1

if count == 25:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')