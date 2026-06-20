import sympy as sp
from scipy import integrate
import numpy as np

CANDIDATE = 36

x = sp.Symbol('x')
curve = x**2 - 7*x + 10
line = -x + 10

# 교점 찾기
intersection_eq = sp.Eq(curve, line)
roots = sp.solve(intersection_eq, x)
roots.sort()

# 두 근이 0과 6인지 확인
assert roots == [0, 6], f"교점 오류: {roots}"

# 구간에서 직선이 위에 있는지 확인
test_x = 3
assert -test_x + 10 > test_x**2 - 7*test_x + 10, "함수 순서 오류"

# 넓이 계산
integrand = line - curve
area_symbolic = sp.integrate(integrand, (x, 0, 6))
area_value = float(area_symbolic)

# 검증
if abs(area_value - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: 계산 결과 {area_value}, 예상 {CANDIDATE}')