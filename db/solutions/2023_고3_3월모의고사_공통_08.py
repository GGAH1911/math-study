import math

m = 6
x_p = m + 2
y_p = m - 1

# 곡선 위의 점인지 확인
y_on_curve = math.log(x_p + 8, 4) + m - 3

# 오차 범위 내에서 일치하는지 확인
if abs(y_p - y_on_curve) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')