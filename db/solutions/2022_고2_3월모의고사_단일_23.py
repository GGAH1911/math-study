# 점 (5, 4)를 직선 y=x에 대해 대칭이동
x1, y1 = 5, 4
# y=x 대칭: (x, y) -> (y, x)
x2, y2 = y1, x1
assert x2 == 4 and y2 == 5, f'Symmetry failed: got ({x2}, {y2})'

# y축 방향으로 1만큼 평행이동
x3, y3 = x2, y2 + 1
assert x3 == 4 and y3 == 6, f'Translation failed: got ({x3}, {y3})'

# ab의 값
ab = x3 * y3
assert ab == 24, f'Product failed: {ab}'

print('VERIFY_PASS')