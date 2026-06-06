import math

# 원래 방정식: log_{1/2}(x+3) = -4
# 답: x = 13
x = 13

# 좌변 계산
arg = x + 3
if arg <= 0:
    print('VERIFY_FAIL')
else:
    lhs = math.log(arg, 0.5)  # log_{1/2}(arg)
    expected_rhs = -4
    
    # 부동소수점 오차를 고려한 비교
    if abs(lhs - expected_rhs) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')