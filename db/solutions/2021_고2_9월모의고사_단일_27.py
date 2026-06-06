import math

def verify():
    # 원래 부등식: log|x-1| + log(x+2) <= 1
    candidates = [-1, 0, 2, 3]
    all_pass = True
    
    for x in candidates:
        # 정의역 확인
        if x <= -2 or x == 1:
            print(f'x={x}: VERIFY_FAIL (정의역 외)')
            all_pass = False
            continue
        
        # 부등식 검증
        lhs = math.log10(abs(x - 1)) + math.log10(x + 2)
        rhs = 1.0
        
        if lhs <= rhs + 1e-9:  # 부동소수점 오차 허용
            print(f'x={x}: {lhs:.6f} <= {rhs} ✓')
        else:
            print(f'x={x}: {lhs:.6f} > {rhs} ✗')
            all_pass = False
    
    # 정수해의 합
    total = sum(candidates)
    print(f'정수해의 합: {total}')
    
    if all_pass and total == 4:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()