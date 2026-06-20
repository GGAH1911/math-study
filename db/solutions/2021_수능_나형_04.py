import numpy as np
from scipy.optimize import minimize_scalar

# 함수 정의: f(x) = 4*cos(x) + 3
def f(x):
    return 4 * np.cos(x) + 3

# 최댓값 구하기: -f(x)의 최솟값 = f(x)의 최댓값
result = minimize_scalar(lambda x: -f(x), bounds=(0, 2*np.pi), method='bounded')
max_value = -result.fun

# 해석적 검증: cos(x) = 1일 때 최댓값
max_analytical = 4 * 1 + 3

# 검증
if np.isclose(max_value, 7) and np.isclose(max_analytical, 7):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')