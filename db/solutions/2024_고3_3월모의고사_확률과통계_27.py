from itertools import combinations

# A가 들어갈 3개 상자: 홀수 개수가 홀수(1개 또는 3개)인 경우만
odd_boxes = {1, 3, 5, 7}
even_boxes = {2, 4, 6}

count = 0

# A의 위치 선택 (합이 홀수인 경우만)
for a_positions in combinations(range(1, 8), 3):
    a_set = set(a_positions)
    odd_count = len(a_set & odd_boxes)
    
    # 홀수가 1개 또는 3개인 경우만
    if odd_count in [1, 3]:
        # 나머지 4개 상자
        remaining = [i for i in range(1, 8) if i not in a_set]
        
        # B의 위치 선택 (2개)
        for b_positions in combinations(remaining, 2):
            # C, D의 위치 선택
            cd_positions = [i for i in remaining if i not in b_positions]
            # C: 2가지, D: 1가지
            count += 2  # C,D 배치 방법

if count == 192:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')