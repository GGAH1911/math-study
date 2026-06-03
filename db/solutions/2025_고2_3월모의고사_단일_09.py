from sympy import symbols, solve, simplify
a = 9
# 원의 중심
center_x, center_y = -3, -5
# 변환 후 직선: y = -ax - 4a + 4
line_y = -a * center_x - 4*a + 4
# 원의 중심이 직선 위에 있는지 확인
if abs(line_y - center_y) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')