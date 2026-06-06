# 직접 세기로 검증
# 6명을 0~5로 표시: A=0, B=1, C=2, D=3, E=4, F=5
from itertools import permutations

def is_neighbor(perm, i, j):
    """원탁에서 i와 j가 이웃하는지 확인"""
    pos_i = perm.index(i)
    pos_j = perm.index(j)
    return abs(pos_i - pos_j) == 1 or abs(pos_i - pos_j) == 5

# 회전을 제거한 대표원소만 세기
# 0번(A)을 항상 0번 위치에 고정
count = 0
for perm in permutations(range(1, 6)):
    full_perm = (0,) + perm  # A를 0번 위치에 고정
    
    # 조건 (가): A(0)과 B(1)이 이웃
    if not is_neighbor(full_perm, 0, 1):
        continue
    
    # 조건 (나): B(1)과 C(2)가 이웃하지 않음
    if is_neighbor(full_perm, 1, 2):
        continue
    
    count += 1

if count == 36:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}, expected 36')