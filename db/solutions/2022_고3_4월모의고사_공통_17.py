import numpy as np
from scipy import integrate

# 원래 곡선: y = -x^2 + 4x - 4
def curve(x):
    return -x**2 + 4*x - 4

# 넓이 계산 (절댓값으로 음수 영역도 포함)
area, _ = integrate.quad(lambda x: -curve(x), 0, 2)
S = area
result = 12 * S

if abs(result - 32) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')