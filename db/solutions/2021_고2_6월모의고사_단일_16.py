import numpy as np

a = 4 * np.sqrt(2)
k = 8  # 임의의 k > 1

# 좌표 계산
log_2_k = np.log2(k)
log_a_k = np.log(k) / np.log(a)

A = np.array([k, log_2_k])
B = np.array([k, log_a_k])
C_x = 2 ** log_a_k
C = np.array([C_x, log_a_k])
D = np.array([1, 0])

# 삼각형 넓이 (좌표로 계산)
def tri_area(p1, p2, p3):
    return 0.5 * abs((p2[0]-p1[0])*(p3[1]-p1[1]) - (p3[0]-p1[0])*(p2[1]-p1[1]))

area_ACB = tri_area(A, C, B)
area_BCD = tri_area(B, C, D)
ratio = area_ACB / area_BCD

if abs(ratio - 1.5) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')