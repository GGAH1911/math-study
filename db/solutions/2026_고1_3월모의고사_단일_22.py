# 직선: y = 2x + b에서 b = 3
# 점 (1, 5)가 직선 y = 2x + 3 위에 있는지 확인
x, y = 1, 5
m = 2
b = 3
result = y - (m * x + b)
if abs(result) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')