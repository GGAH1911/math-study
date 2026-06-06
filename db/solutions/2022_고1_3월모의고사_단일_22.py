# 원래 함수: y = 3x + a, 점 (-3, 2)를 지남
x_point, y_point = -3, 2
# 함수식에 대입
a = 11
y_calculated = 3 * x_point + a
if y_calculated == y_point:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')