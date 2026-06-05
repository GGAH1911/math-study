import numpy as np
A = np.array([0,0,0], dtype=float)
B = np.array([6,0,0], dtype=float)
phi1 = np.radians(60)
D = A + 6*np.array([0, np.cos(phi1), np.sin(phi1)])
C = B + 6*np.array([0, np.cos(phi1), np.sin(phi1)])
phi2 = np.radians(30)
F = A + 12*np.array([0, np.cos(phi2), np.sin(phi2)])
E = B + 12*np.array([0, np.cos(phi2), np.sin(phi2)])
H = np.array([F[0], F[1], 0.0])
AB2 = B[:2]-A[:2]; AD2 = D[:2]-A[:2]
proj_alpha = abs(AB2[0]*AD2[1]-AB2[1]*AD2[0])
assert abs(proj_alpha-18)<1e-6, f'proj alpha={proj_alpha}'
assert abs(np.linalg.norm(F-A)-12)<1e-9
assert abs(np.dot(F-A, B-A))<1e-9
assert abs(np.linalg.norm(F-H)-6)<1e-9
n_ABEF = np.cross(B-A, F-A); n_ABEF/=np.linalg.norm(n_ABEF)
n_ABCD = np.cross(B-A, D-A); n_ABCD/=np.linalg.norm(n_ABCD)
cos_ang = abs(np.dot(n_ABCD, n_ABEF))
area = 36*cos_ang
AD=D-A; AFv=F-A
cos_DAF=np.dot(AD,AFv)/(np.linalg.norm(AD)*np.linalg.norm(AFv))
angle_DAF=np.arccos(cos_DAF)
assert 0<angle_DAF<np.pi/2
if abs(area-18*np.sqrt(3))<1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {area}')