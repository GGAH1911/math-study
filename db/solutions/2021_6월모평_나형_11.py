import math

# 원점, 점 1, 점 2의 좌표
pt0 = (0, 0)
pt1 = (2, math.log(2, 4))  # log_4(2) = 1/2
a_candidate = 2
pt2 = (4, math.log(a_candidate, 2))  # log_2(2) = 1

# 원점과 pt1을 지나는 직선의 기울기
m = pt1[1] / pt1[0]

# pt2가 직선 위에 있는지 확인
y_on_line = m * pt2[0]

# 검증
if math.isclose(pt2[1], y_on_line) and math.isclose(pt1[1], m * pt1[0]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')