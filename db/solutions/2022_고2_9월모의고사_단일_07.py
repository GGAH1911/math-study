import math

# 주어진 조건
theta = math.pi / 6  # 중심각
l = math.pi  # 호의 길이

# 반지름 구하기: l = r * theta
r = l / theta
assert abs(r - 6) < 1e-10, f'반지름 계산 오류: {r}'

# 부채꼴 넓이: S = (1/2) * r^2 * theta
S = 0.5 * r**2 * theta
answer_value = 3 * math.pi

if abs(S - answer_value) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')