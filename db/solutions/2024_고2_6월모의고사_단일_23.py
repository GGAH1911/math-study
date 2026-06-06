import math

# 문제의 원래 방정식: log_4(x-1) = 3
x = 65

# 원래 방정식에 대입하여 검증
lhs = math.log(x - 1, 4)  # log_4(x-1)
rhs = 3

# 양변이 같은지 확인 (부동소수점 오차 허용)
if abs(lhs - rhs) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')