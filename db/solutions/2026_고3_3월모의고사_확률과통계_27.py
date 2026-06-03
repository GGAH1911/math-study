from itertools import combinations

U = {-4, -2, -1, 1, 2, 4}
count = 0

# 모든 부분집합 쌍 (A, B) 생성
for mask_a in range(2**6):
    for mask_b in range(2**6):
        A = {list(U)[i] for i in range(6) if mask_a & (1 << i)}
        B = {list(U)[i] for i in range(6) if mask_b & (1 << i)}
        
        intersection = A & B
        
        # 조건 (가): n(A ∩ B) ≥ 2
        if len(intersection) < 2:
            continue
        
        # 조건 (나): A ∩ B의 모든 원소 합 = 0
        if sum(intersection) != 0:
            continue
        
        count += 1

if count == 271:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')