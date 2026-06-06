from itertools import product

def count_valid_functions():
    count = 0
    # 모든 가능한 함수 f: {1,2,3,4,5} -> {1,2,3,4,5}
    # 함수는 튜플 (f(1), f(2), f(3), f(4), f(5))로 표현
    for f_tuple in product(range(1, 6), repeat=5):
        f = {i+1: f_tuple[i] for i in range(5)}
        
        # 조건 (가): 비감소 함수
        is_non_decreasing = all(f[i] <= f[i+1] for i in range(1, 5))
        if not is_non_decreasing:
            continue
        
        # 조건 (나): f(2) ≠ 1
        if f[2] == 1:
            continue
        
        # 조건 (나): f(4) × f(5) < 20
        if f[4] * f[5] >= 20:
            continue
        
        count += 1
    
    return count

result = count_valid_functions()
if result == 45:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')