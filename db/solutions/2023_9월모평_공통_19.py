import numpy as np
from numpy.polynomial import polynomial as P

# 원래 방정식: 3x^4 - 4x^3 - 12x^2 + k = 0
# k = 1, 2, 3, 4에서 각각 4개의 실근을 가지는지 확인

count_valid = 0
for k in range(1, 5):
    # 계수: 3x^4 - 4x^3 - 12x^2 + 0x + k
    coeffs = [k, 0, -12, -4, 3]  # 낮은 차수부터
    roots = np.roots(coeffs[::-1])  # 높은 차수부터
    
    # 실근 개수 확인
    real_roots = roots[np.abs(roots.imag) < 1e-10].real
    distinct_roots = len(np.unique(np.round(real_roots, 8)))
    
    if distinct_roots == 4:
        count_valid += 1

# k=5, k=6에서는 4개 실근이 아닌지 확인
for k in [5, 6, 32]:
    coeffs = [k, 0, -12, -4, 3]
    roots = np.roots(coeffs[::-1])
    real_roots = roots[np.abs(roots.imag) < 1e-10].real
    distinct_roots = len(np.unique(np.round(real_roots, 8)))
    if distinct_roots != 4:
        count_valid += 1

if count_valid >= 7:  # 4개(k=1,2,3,4) + 3개(k=5,6,32 확인)
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')