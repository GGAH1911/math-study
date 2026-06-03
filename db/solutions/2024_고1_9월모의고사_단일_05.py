import sympy as sp
k = 1
# 원래 직선: y = kx + 1
# 평행이동된 직선: y = kx - k - 1
# 점 (3, 1)을 지나는지 확인
x_val, y_val = 3, 1
y_on_line = k * x_val - k - 1
if y_on_line == y_val:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')