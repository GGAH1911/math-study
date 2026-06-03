import numpy as np

# 원: x^2 + y^2 = 8, 중심 O(0,0), 반지름 r = sqrt(8)
# 점 A(5, 5)
# 원 위의 점 P는 P = (2*sqrt(2)*cos(t), 2*sqrt(2)*sin(t))

r = np.sqrt(8)
Ax, Ay = 5, 5

# AP의 최솟값: OA - r
OA = np.sqrt(Ax**2 + Ay**2)
min_AP = OA - r

# 수치 검증: t를 촘촘히 샘플링해서 실제 최솟값 확인
t_vals = np.linspace(0, 2*np.pi, 1_000_000)
Px = r * np.cos(t_vals)
Py = r * np.sin(t_vals)
dists = np.sqrt((Px - Ax)**2 + (Py - Ay)**2)
numerical_min = dists.min()

expected = 3 * np.sqrt(2)

if abs(min_AP - expected) < 1e-9 and abs(numerical_min - expected) < 1e-5:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: analytical={min_AP}, numerical={numerical_min}, expected={expected}')
