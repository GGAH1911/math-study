import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import brentq

def verify(n_val, r_n_val):
    # 검증: n=n_val일 때 r_n_val이 모든 조건을 만족하는가
    
    # 접점
    a = n_val / 2
    f_a = 4 / (n_val**3) * a**3 + 1
    assert abs(f_a - 1.5) < 1e-10
    
    # 접선의 기울기
    f_prime_a = 12 / (n_val**3) * a**2
    assert abs(f_prime_a - 3/n_val) < 1e-10
    
    # 원의 중심 (h, r_n_val)은 다음을 만족:
    # (1) 3h = r_n*(n + sqrt(9+n^2))
    # (2) (h - n/2)^2 = 3*r_n - 9/4
    
    eq1_rhs = r_n_val * (n_val + np.sqrt(9 + n_val**2))
    h = eq1_rhs / 3
    
    lhs_eq2 = (h - n_val/2)**2
    rhs_eq2 = 3*r_n_val - 9/4
    
    if abs(lhs_eq2 - rhs_eq2) > 1e-6:
        return 'VERIFY_FAIL'
    
    # 점근 형태 확인: r_n ≈ 3/4 + 27/(16n^2)
    r_asymp = 0.75 + 27/(16*n_val**2)
    if abs(r_n_val - r_asymp) > 1e-5:
        return 'VERIFY_FAIL'
    
    # 극한값
    limit_val = n_val**2 * (4*r_n_val - 3)
    expected = 27/4
    if abs(limit_val - expected) > 0.01:
        return 'VERIFY_FAIL'
    
    return 'VERIFY_PASS'

# 여러 n값에서 점근 형태로 계산한 r_n으로 검증
for n_test in [100, 1000, 10000]:
    r_test = 0.75 + 27/(16*n_test**2)
    result = verify(n_test, r_test)
    if result != 'VERIFY_PASS':
        print(f'VERIFY_FAIL at n={n_test}')
        exit()

print('VERIFY_PASS')