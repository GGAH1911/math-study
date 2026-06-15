import math

# 범위: pi/2 <= x <= pi
# 방정식: sin(x) = 1/2

CANDIDATE = 5 * math.pi / 6

# 조건 1: 범위 확인
in_range = (math.pi / 2 <= CANDIDATE <= math.pi)

# 조건 2: 방정식 만족 확인
lhs = math.sin(CANDIDATE)
rhs = 0.5

if in_range and math.isclose(lhs, rhs, abs_tol=1e-10):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: in_range={in_range}, sin(5pi/6)={lhs}, expected={rhs}')
