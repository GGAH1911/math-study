import numpy as np
C = np.array([0,0,0],dtype=float)
B = np.array([3,0,0],dtype=float)
D = np.array([0,3,0],dtype=float)
assert abs(np.linalg.norm(B-C)-3)<1e-9
assert abs(np.linalg.norm(D-C)-3)<1e-9
assert abs(np.dot(B-C,D-C))<1e-9,'BCD not 90'
H = B + (1/3)*(D-B)
assert abs(np.linalg.norm(H-B)/np.linalg.norm(D-H)-0.5)<1e-9,'H not 1:2'
h = np.sqrt(15)
A = np.array([2,1,h],dtype=float)
AH = H-A
assert abs(np.dot(AH,B-C))<1e-9
assert abs(np.dot(AH,D-C))<1e-9,'AH not perp to plane'
area_ABC = 0.5*np.linalg.norm(np.cross(B-A,C-A))
assert abs(area_ABC-6)<1e-9,f'area ABC={area_ABC}'
HA=A-H; HC=C-H
area_AHC=0.5*np.linalg.norm(np.cross(HA,HC))
expected=5*np.sqrt(3)/2
print('VERIFY_PASS' if abs(area_AHC-expected)<1e-9 else f'VERIFY_FAIL: {area_AHC} vs {expected}')