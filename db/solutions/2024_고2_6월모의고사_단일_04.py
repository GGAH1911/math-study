import math
import numpy as np

# 주어진 방정식: 2*cos(x) + 1 = 0
# 우리의 답: x = 2π/3
x = 2 * math.pi / 3
result = 2 * math.cos(x) + 1

if abs(result) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')