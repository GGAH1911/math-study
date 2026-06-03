import math

a = math.sqrt(3)

# 원점 O=(0,0) 검사
y1_at_0 = a**0 - 1
y2_at_0 = math.log(0+1, a)

# 점 P=(2,2) 검사 (두 곡선 모두 통과해야)
y1_at_2 = a**2 - 1                # (sqrt(3))^2 - 1 = 2
y2_at_2 = math.log(2+1, a)       # log_sqrt3(3) = 2

# 삼각형 OHP 넓이: O=(0,0), H=(2,0), P=(2,2)
area = 0.5 * abs(2) * abs(2)

eps = 1e-9
if (abs(y1_at_0) < eps and abs(y2_at_0) < eps and
    abs(y1_at_2 - 2.0) < eps and abs(y2_at_2 - 2.0) < eps and
    abs(area - 2.0) < eps):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'y1(0)={y1_at_0}, y2(0)={y2_at_0}')
    print(f'y1(2)={y1_at_2}, y2(2)={y2_at_2}')
    print(f'area={area}')