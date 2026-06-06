import numpy as np
from numpy.polynomial import polynomial as P

# k = 5, 6, 7에 대해 원래 사차방정식의 근 개수 확인
for k in [5, 6, 7]:
    # (2x^2 + kx)^2 + 10(2x^2 + kx) + 16 = 0
    # 전개: 4x^4 + 4kx^3 + k^2*x^2 + 20x^2 + 10kx + 16 = 0
    # 정렬: 4x^4 + 4kx^3 + (k^2 + 20)x^2 + 10kx + 16 = 0
    
    coeffs = [16, 10*k, k*k + 20, 4*k, 4]  # 낮은 차수부터
    roots = np.roots(coeffs[::-1])
    real_roots = roots[np.abs(roots.imag) < 1e-10].real
    unique_real_roots = len(np.unique(np.round(real_roots, 10)))
    
    # 검증: D1 > 0, D2 < 0
    D1 = k*k - 16
    D2 = k*k - 64
    condition = (D1 > 0) and (D2 < 0)
    
    if unique_real_roots != 2 or not condition:
        print(f'VERIFY_FAIL k={k}')
        exit()

print('VERIFY_PASS')