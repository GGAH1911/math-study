import numpy as np
t = 3.5
discriminant = t**2 - 4
u1, u2 = (t - np.sqrt(discriminant))/2, (t + np.sqrt(discriminant))/2
x1, x2 = np.log2(u1), np.log2(u2)
assert np.isclose(x1 + x2, 0), 'x1+x2 should be 0'
y1, y2 = 2**x1, 2**x2
assert np.isclose(2**x1 + 2**(-x1), t), 'x1 satisfies equation'
assert np.isclose(2**x2 + 2**(-x2), t), 'x2 satisfies equation'
A, B, C, D, O = np.array([x1,y1]), np.array([x2,y2]), np.array([0,1]), np.array([0,t-1]), np.array([0,0])
CD = np.abs(D[1]-C[1])
assert np.isclose(CD, t-2), 'CD check'
AC = np.linalg.norm(A-C)
DB = np.linalg.norm(B-D)
assert np.isclose(AC, DB), 'AC=DB check'
area_AOB = 0.5*np.abs(np.cross(A, B))
area_ABD = 0.5*np.abs(np.cross(B-A, D-A))
ratio = area_ABD/area_AOB
assert np.isclose(ratio, (t-2)/t), 'Area ratio check'
print('VERIFY_PASS')