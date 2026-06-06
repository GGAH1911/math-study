from itertools import combinations

def verify(answer):
    count = 0
    # -1이 들어갈 6개 위치 선택
    for positions in combinations(range(12), 6):
        sequence = [1] * 12
        for pos in positions:
            sequence[pos] = -1
        
        # a_n 합 계산
        total = 0
        for i in range(11):
            total += sequence[i] * sequence[i+1]
        
        if total == 3:
            count += 1
    
    if count == answer:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify(100)