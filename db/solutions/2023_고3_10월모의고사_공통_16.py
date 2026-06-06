import math

def verify(x):
    # 정의역 확인
    if x <= 2 or x <= -6:
        return False
    
    # 원래 방정식: log_2(x-2) = 1 + log_4(x+6)
    # log_2 밑: 2
    # log_4 밑: 4
    
    lhs = math.log2(x - 2)
    rhs = 1 + math.log(x + 6, 4)
    
    # 부동소수점 오차 고려
    return abs(lhs - rhs) < 1e-10

x_answer = 10
if verify(x_answer):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')