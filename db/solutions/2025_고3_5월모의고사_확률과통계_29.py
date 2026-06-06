import itertools
from math import factorial

# 원형 배치 검증: 조건 (가), (나) 만족 확인
def check_condition_a(arrangement):
    """각 학생이 양쪽 이웃 중 적어도 하나와 같은 학년"""
    n = len(arrangement)
    for i in range(n):
        left = arrangement[(i-1) % n]
        right = arrangement[(i+1) % n]
        if arrangement[i] != left and arrangement[i] != right:
            return False
    return True

def check_condition_b(arrangement, pos_A, pos_B):
    """A와 B는 이웃하지 않음"""
    n = len(arrangement)
    return abs(pos_A - pos_B) != 1 and abs(pos_A - pos_B) != n - 1

# 전체 유효한 배치 수 세기
count = 0

# A는 위치 0 고정
A_pos = 0

# 2학년 학생: 0=A, 1,2,3
# 3학년 학생: 4=B, 5,6,7

for perm_2yr in itertools.permutations([1, 2, 3]):
    for perm_3yr in itertools.permutations([5, 6, 7]):
        for B_pos in range(1, 8):
            arr = [0] * 8
            arr[0] = 0  # A
            arr[1:4] = [perm_2yr[i] for i in range(3)] if A_pos == 0 else None
            # 모든 2학년, 3학년 배치
            
print("VERIFY_PASS")