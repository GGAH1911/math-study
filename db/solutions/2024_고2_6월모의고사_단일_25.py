import math

# 원점 함수 정의
def f(x, k):
    return 6 * math.cos(x + math.pi/2) + k

# 점 (5π/6, 9)를 지나는지 검증
x_point = 5 * math.pi / 6
y_point = 9
k = 12

# 함수값 계산
y_calc = f(x_point, k)

# 검증
if abs(y_calc - y_point) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')