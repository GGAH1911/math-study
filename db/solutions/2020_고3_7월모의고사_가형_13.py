import math
from sympy import symbols, solve, sqrt, simplify

# 두 함수 정의
def f(x):
    return 2**x + 1

def g(x):
    return 2**(x+1)

# 문제 조건으로부터 구한 a, b
a, b = 1, -1

# 점 A, B 좌표
A = (a, f(a))
B = (b, g(b))

# 중점이 P(0, 2)인지 확인
midpoint_x = (A[0] + B[0]) / 2
midpoint_y = (A[1] + B[1]) / 2

assert midpoint_x == 0, f"중점 x좌표 오류: {midpoint_x}"
assert midpoint_y == 2, f"중점 y좌표 오류: {midpoint_y}"

# AB의 길이 계산
dist_squared = (A[0] - B[0])**2 + (A[1] - B[1])**2
dist = math.sqrt(dist_squared)

# 예상값: 2√2 ≈ 2.828427...
expected = 2 * math.sqrt(2)

if abs(dist - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {dist} != {expected}')