import sympy as sp
from scipy.integrate import quad
import numpy as np

CANDIDATE = 14

# 함수 정의
def f(x):
    return (1/3) * x * (4 - x)

def g(x):
    return abs(x - 1) - 1

# 교점 확인
assert abs(f(0) - g(0)) < 1e-10, "x=0에서 교점 아님"
assert abs(f(3) - g(3)) < 1e-10, "x=3에서 교점 아님"

# 구간별 적분
def integrand1(x):
    return f(x) - (-x)  # 0 <= x < 1

def integrand2(x):
    return f(x) - (x - 2)  # 1 <= x <= 3

S1, _ = quad(integrand1, 0, 1)
S2, _ = quad(integrand2, 1, 3)
S = S1 + S2

# 4S 계산
four_S = 4 * S

# 검증
if abs(four_S - CANDIDATE) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: 4S={four_S}, CANDIDATE={CANDIDATE}')