import numpy as np

# 조건을 만족하는 구체적 벡터 생성
# |a|=|b|=sqrt(17), a·b=1
# a = (sqrt(17), 0)
# b: b·a=1, |b|=sqrt(17) → b_x = 1/sqrt(17), b_y = sqrt(17 - 1/17) = sqrt(288/17)
import math

ra = math.sqrt(17)
a = np.array([ra, 0.0])

bx = 1.0 / ra
by = math.sqrt(17 - bx**2)
b = np.array([bx, by])

# 검증
cond1 = abs(np.linalg.norm(a + b) - 6) < 1e-9
cond2 = abs(np.linalg.norm(2*a - b) - 9) < 1e-9
cond3 = abs(np.dot(a + b, a - b)) < 1e-9

# 넓이
area = 0.5 * abs(a[0]*b[1] - a[1]*b[0])
expected = 6 * math.sqrt(2)
cond4 = abs(area - expected) < 1e-9

if cond1 and cond2 and cond3 and cond4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL cond1={cond1} cond2={cond2} cond3={cond3} area={area:.6f} expected={expected:.6f}')
