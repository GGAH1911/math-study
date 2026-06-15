import math
import numpy as np
from scipy.optimize import fsolve

# 함수 정의
def f(x):
    return np.tan(x / 4)

# 주기 검증: T = 4π
T = 4 * math.pi

# 여러 x 값에서 f(x) == f(x+T) 확인
test_points = [0.1, 0.5, 1.0, 1.5, 2.0]
verified = True

for x in test_points:
    # tan의 단절점 주의
    if abs(np.cos(x/4)) < 1e-10 or abs(np.cos((x+T)/4)) < 1e-10:
        continue
    val1 = f(x)
    val2 = f(x + T)
    if not np.isclose(val1, val2, atol=1e-9):
        verified = False
        break

if verified:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')