import math

# 원래 함수: y = 3*sin(x + pi) + k
# 점 (pi/6, 5/2)을 지남

x_point = math.pi / 6
y_point = 5 / 2
k = 4  # 우리가 구한 답

# 함수값 계산
y_calculated = 3 * math.sin(x_point + math.pi) + k

# 검증
if abs(y_calculated - y_point) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')