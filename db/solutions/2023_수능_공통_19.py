import numpy as np
from numpy.polynomial import polynomial as P

# k = 1부터 k = 7까지 각 경우에 양의 실근이 정확히 2개인지 확인
count_valid = 0

for k in range(1, 8):
    # 방정식: 2x^3 - 6x^2 + k = 0
    # 계수: [k, 0, -6, 2] (상수항부터 높은 차수)
    coeffs = [k, 0, -6, 2]
    roots = np.roots([2, -6, 0, k])  # 높은 차수부터
    
    # 양의 실근만 필터
    positive_real_roots = []
    for r in roots:
        if np.isreal(r) and np.real(r) > 1e-9:
            positive_real_roots.append(np.real(r))
    
    # 서로 다른 양의 실근
    distinct_roots = []
    for r in sorted(positive_real_roots):
        if not distinct_roots or abs(r - distinct_roots[-1]) > 1e-6:
            distinct_roots.append(r)
    
    if len(distinct_roots) == 2:
        count_valid += 1

if count_valid == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')