import math

# 직선 3x + y + 3 = 0
# 점과 직선 거리
def distance(x0, y0):
    return abs(3*x0 + y0 + 3) / math.sqrt(10)

# m 범위 확인
d2 = distance(0, 5)
count = 0
valid_m = []

for m in range(-10, 10):
    d1 = distance(m, -m)
    if d1 < d2:
        count += 1
        valid_m.append(m)

if count == 8 and valid_m == [-5, -4, -3, -2, -1, 0, 1, 2]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')