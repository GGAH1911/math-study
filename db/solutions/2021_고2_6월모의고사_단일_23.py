import math

# 원래 문제: log_3(x-2) = 1
x = 5

# 진수 조건 확인
if x - 2 <= 0:
    print('VERIFY_FAIL')
else:
    # 좌변 계산
    lhs = math.log(x - 2) / math.log(3)
    
    # 우변
    rhs = 1
    
    # 검증
    if abs(lhs - rhs) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')