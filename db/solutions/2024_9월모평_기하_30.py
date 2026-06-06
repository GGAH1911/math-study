import numpy as np
from scipy.optimize import minimize_scalar

# 좌표 설정
A = np.array([0, 0])
B = np.array([6, 0])
C = np.array([0, 6])
Q = np.array([2, -2*np.sqrt(3)])
M = (A + B) / 2

# 선분 AQ 위의 점 X: X = t*Q, t in [0,1]
def distance_squared(t):
    X = t * Q
    return np.sum((X - M)**2)

# 최솟값 찾기
result = minimize_scalar(distance_squared, bounds=(0, 1), method='bounded')
t_min = result.x
min_dist_sq = result.fun

# |XA + XB| = 2|XM|
m = 2 * np.sqrt(min_dist_sq)
m_squared = m**2

print(f"t_min = {t_min}")
print(f"|XM|_min^2 = {min_dist_sq}")
print(f"m^2 = {m_squared}")

if abs(m_squared - 27) < 0.0001:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")