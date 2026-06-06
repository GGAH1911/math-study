import numpy as np
A = np.array([-4, 0, 0])
B = np.array([4, 0, 0])
C = np.array([3, np.sqrt(7), 0])
D = np.array([-7/4, 3*np.sqrt(7)/4, 3])
H = np.array([-7/4, 3*np.sqrt(7)/4, 0])
O = np.array([0, 0, 0])
assert np.allclose(np.linalg.norm(A), 4)
assert np.allclose(np.linalg.norm(D), 4)
assert np.allclose(np.linalg.norm(B - A), 8)
assert np.allclose(np.linalg.norm(C - B), 2*np.sqrt(2))
assert np.allclose(np.dot(C, D), 0)
AD = D - A
OH = H - O
assert np.allclose(np.dot(AD, OH), 0)
AH = H - A
cross_AD_AH = np.cross(AD, AH)
area = 0.5 * np.linalg.norm(cross_AD_AH)
OD = D - O
OC = C - O
norm_doc = np.cross(OD, OC)
cos_theta = np.abs(np.dot(cross_AD_AH, norm_doc)) / (np.linalg.norm(cross_AD_AH) * np.linalg.norm(norm_doc))
S = area * cos_theta
result = 8 * S
if np.isclose(result, 27):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')