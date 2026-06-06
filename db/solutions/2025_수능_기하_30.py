import numpy as np
from scipy.optimize import minimize_scalar

def compute_dot_product(theta):
    # 도형 S 위의 점 P
    P = np.array([2 + 2*np.cos(theta), 2*np.sin(theta)])
    
    # 조건 2에서 Q의 위치
    Q = np.array([2.5 + 0.5*np.cos(theta), 2 + 0.5*np.sin(theta)])
    
    # 벡터들
    AC = np.array([4, -4])
    AQ = Q - np.array([0, 4])
    
    # 내적
    return np.dot(AC, AQ)

# 최댓값과 최솟값 구하기
thetas = np.linspace(0, 2*np.pi, 1000)
values = [compute_dot_product(t) for t in thetas]

M = max(values)
m = min(values)

product = M * m

# 검증: 이론값과 비교
theory_M = 18 + 2*np.sqrt(2)
theory_m = 18 - 2*np.sqrt(2)
theory_product = 316

if abs(product - theory_product) < 0.01:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')