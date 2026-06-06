import numpy as np
from scipy.integrate import quad

# 원래 함수들
def curve(x):
    return x**2 - 7*x + 10

def line(x):
    return -x + 10

# 교점 확인
x_intersect = [0, 6]
for x in x_intersect:
    assert abs(curve(x) - line(x)) < 1e-10, f'교점 {x}에서 불일치'

# 넓이 계산 (직선 - 곡선)
def integrand(x):
    return line(x) - curve(x)

area, _ = quad(integrand, 0, 6)
expected = 36

if abs(area - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {area} vs {expected}')