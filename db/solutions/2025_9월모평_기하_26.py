import sympy as sp
import numpy as np

n = sp.Symbol('n', positive=True, integer=True)

# 접선 방정식: x - ny + n^2 = 0
# 원의 중심 (1, 0)에서 접선까지의 거리
dist = sp.sqrt(1 + n**2)

# 조건: dist <= 6
# sqrt(1 + n^2) <= 6
# 1 + n^2 <= 36
# n^2 <= 35

count = 0
for n_val in range(1, 10):
    if n_val**2 <= 35:
        count += 1
        # 검증: 점 (n^2, 2n)이 포물선 위에 있는지 확인
        x, y = n_val**2, 2*n_val
        assert y**2 == 4*x, f"Point ({x}, {y}) not on parabola"
        
        # 거리 검증
        dist_val = np.sqrt(1 + n_val**2)
        assert dist_val <= 6, f"n={n_val} fails distance check"

if count == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')