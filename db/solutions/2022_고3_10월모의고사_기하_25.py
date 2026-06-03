import numpy as np
A = np.array([0., 0.])
B = np.array([2., 0.])
C = np.array([2., 4*np.sqrt(2)])
D = np.array([0., 4*np.sqrt(2)])
AB = np.linalg.norm(B - A)
BD = np.linalg.norm(D - B)
BA_BC = np.linalg.norm((A - B) - (C - B))
AD = np.linalg.norm(D - A)
AB_CD_sum = np.linalg.norm((B - A) + (D - C))
cond1a = np.isclose(AB, 2)
cond1b = np.isclose(AB_CD_sum, 0)
cond2a = np.isclose(BD, 6)
cond2b = np.isclose(BA_BC, 6)
ans_check = np.isclose(AD, 4*np.sqrt(2))
if cond1a and cond1b and cond2a and cond2b and ans_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')