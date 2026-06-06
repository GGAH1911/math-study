import math

x = 6

# 정의역 확인
if x - 1 <= 0 or 13 + 2*x <= 0:
    print('VERIFY_FAIL')
else:
    # 좌변
    lhs = math.log2(x - 1)
    
    # 우변
    rhs = math.log(13 + 2*x, 4)
    
    # 비교 (부동소수점 오차 고려)
    if abs(lhs - rhs) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')