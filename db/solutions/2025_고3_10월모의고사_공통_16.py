import math

def verify(x):
    # 정의역 확인
    if x <= 2:
        return 'VERIFY_FAIL'
    
    # 좌변: log_4(x+2) + log_4(2)
    left = math.log(x+2, 4) + math.log(2, 4)
    
    # 우변: log_2(x-2)
    right = math.log(x-2, 2)
    
    # 같은지 확인 (부동소수점 오차 허용)
    if abs(left - right) < 1e-9:
        return 'VERIFY_PASS'
    else:
        return 'VERIFY_FAIL'

x = 6
print(verify(x))