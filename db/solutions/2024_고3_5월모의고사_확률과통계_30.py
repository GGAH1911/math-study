from itertools import permutations

def solve(n_divisions=6, num_flags=7, sum_limit=12):
    """
    원판에 num_flags개의 깃발을 배치하는 경우의 수.
    
    점: 중심 1개 + 둘레 n_divisions개 (총 n_divisions+1 = num_flags개)
    깃발: 1~num_flags
    정삼각형: 중심 + 둘레의 인접한 두 점 (총 n_divisions개)
    조건: 각 정삼각형의 합 ≤ sum_limit
    회전 동치: 같은 것으로 봄
    
    Parameters:
    - n_divisions: 둘레의 등분 수 (기본값: 6)
    - num_flags: 깃발의 개수 (기본값: 7)
    - sum_limit: 정삼각형 합의 제한값 (기본값: 12)
    
    Returns:
    - 조건을 만족하는 배치의 수
    """
    
    total = 0
    
    # 중심에 놓인 깃발 c를 선택
    for c in range(1, num_flags + 1):
        M = sum_limit - c  # 둘레의 인접쌍 합 제한
        
        # 둘레에 배치할 깃발 (c 제외)
        perimeter_flags = [f for f in range(1, num_flags + 1) if f != c]
        
        # 회전 제거: 가장 큰 수를 P_1에 고정
        largest = max(perimeter_flags)
        remaining = [f for f in perimeter_flags if f != largest]
        
        # remaining의 모든 순열에 대해 유효성 확인
        valid_count = 0
        
        for perm in permutations(remaining):
            # 둘레 배치: [largest, perm[0], ..., perm[n_divisions-2]]
            perimeter = [largest] + list(perm)
            
            # 모든 인접쌍의 합이 M 이하인지 확인
            valid = True
            for i in range(n_divisions):
                if perimeter[i] + perimeter[(i + 1) % n_divisions] > M:
                    valid = False
                    break
            
            if valid:
                valid_count += 1
        
        total += valid_count
    
    return total


CANDIDATE = 40

if solve() == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')