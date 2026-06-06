# 원래 점
x0, y0 = 2, -1
# a=2, b=4일 때 검증
a, b = 2, 4
# 평행이동: (x0+a, y0+5)
x_new = x0 + a
y_new = y0 + 5
# (4, b)와 비교
if x_new == 4 and y_new == b:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')