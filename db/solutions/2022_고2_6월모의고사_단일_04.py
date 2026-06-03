import math

# 주어진 조건
x = 5 * math.pi / 4

# 범위 확인
lower = math.pi / 2
upper = 3 * math.pi / 2
in_range = lower < x < upper

# 방정식 검증
tan_x = math.tan(x)
is_solution = abs(tan_x - 1.0) < 1e-10

if in_range and is_solution:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')