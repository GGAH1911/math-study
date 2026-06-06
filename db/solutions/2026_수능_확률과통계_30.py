import sympy as sp
from itertools import combinations

# 검증: 모든 가능한 배치를 직접 세기
count = 0

# Case 1: a=4, b=2, c=4
for i in range(1, 11):
    for j in range(i+2, 11):
        # 필수 0 위치
        zeros_required = set()
        if i > 1:
            zeros_required.add(i-1)
        if i < 10:
            zeros_required.add(i+1)
        if j > 1:
            zeros_required.add(j-1)
        if j < 10:
            zeros_required.add(j+1)
        
        num_required = len(zeros_required)
        if num_required > 4:
            continue
        
        # 남은 위치 중 추가 0 선택
        all_positions = set(range(1, 11))
        all_positions.discard(i)
        all_positions.discard(j)
        all_positions -= zeros_required
        
        additional_zeros_needed = 4 - num_required
        if additional_zeros_needed == 0:
            count += 1
        else:
            count += len(list(combinations(all_positions, additional_zeros_needed)))

# Case 2: a=6, b=1, c=3
for i in range(1, 11):
    zeros_required = set()
    if i > 1:
        zeros_required.add(i-1)
    if i < 10:
        zeros_required.add(i+1)
    
    num_required = len(zeros_required)
    all_positions = set(range(1, 11))
    all_positions.discard(i)
    all_positions -= zeros_required
    
    additional_zeros_needed = 3 - num_required
    count += len(list(combinations(all_positions, additional_zeros_needed)))

if count == 262:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')