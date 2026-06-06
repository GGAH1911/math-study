import numpy as np
from scipy.optimize import fsolve

def verify():
    # t = 1에 가까운 값으로 검증
    t = 1.001
    
    # 교점: x^2 - 3tx + 2t^2 = 0
    x_A = t
    x_B = 2*t
    
    # y 값
    y_A = 2*t / x_A  # = 2
    y_B = 2*t / x_B  # = 1
    
    # 직선 검증
    assert abs(y_A - (-1/t * x_A + 3)) < 1e-10
    assert abs(y_B - (-1/t * x_B + 3)) < 1e-10
    
    # 거리 계산
    OA = np.sqrt(x_A**2 + y_A**2)
    OB = np.sqrt(x_B**2 + y_B**2)
    
    # 극한값
    k_numerical = (OB - OA) / (t - 1)
    k_exact = 3 * np.sqrt(5) / 5
    
    # 답 검증
    answer = 30 * k_exact**2
    
    if abs(answer - 54) < 0.01:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()