import numpy as np

# 원래 조건 재현
D = np.array([0.0, 0.0, 0.0])
A = np.array([3.0, 0.0, 0.0])
B = np.array([0.0, 2.0, 0.0])
C = np.array([0.0, 0.0, 2*np.sqrt(3)])

# 조건 검증
assert abs(np.linalg.norm(A-D) - 3) < 1e-10, 'AD'
assert abs(np.linalg.norm(B-D) - 2) < 1e-10, 'DB'
assert abs(np.linalg.norm(C-D) - 2*np.sqrt(3)) < 1e-10, 'DC'
cos_ADB = np.dot(A-D, B-D)/(np.linalg.norm(A-D)*np.linalg.norm(B-D))
cos_ADC = np.dot(A-D, C-D)/(np.linalg.norm(A-D)*np.linalg.norm(C-D))
cos_BDC = np.dot(B-D, C-D)/(np.linalg.norm(B-D)*np.linalg.norm(C-D))
assert abs(cos_ADB) < 1e-10, 'angle ADB'
assert abs(cos_ADC) < 1e-10, 'angle ADC'
assert abs(cos_BDC) < 1e-10, 'angle BDC'

# t=1/4에서 AP+DP
t_opt = 1/4
P_opt = (1-t_opt)*B + t_opt*C
val_opt = np.linalg.norm(P_opt - A) + np.linalg.norm(P_opt - D)

# 수치 최솟값 (전탐색)
t_scan = np.linspace(0, 1, 100000)
P_scan = np.outer(1-t_scan, B) + np.outer(t_scan, C)
AP_scan = np.linalg.norm(P_scan - A, axis=1)
DP_scan = np.linalg.norm(P_scan - D, axis=1)
min_scan = np.min(AP_scan + DP_scan)

expected = 3*np.sqrt(3)

if abs(val_opt - expected) < 1e-8 and abs(min_scan - expected) < 1e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'val_opt={val_opt}, expected={expected}, scan_min={min_scan}')
