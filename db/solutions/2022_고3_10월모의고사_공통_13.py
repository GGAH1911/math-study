import numpy as np
from numpy.linalg import norm

B = np.array([0.0, 0.0])
C = np.array([3*np.sqrt(3), 0.0])
A = np.array([np.sqrt(3), 1.0])

# 원래 문제 조건 검증
assert abs(norm(A-B) - 2) < 1e-10, 'AB=2 fail'
assert abs(norm(B-C) - 3*np.sqrt(3)) < 1e-10, 'BC=3√3 fail'
assert abs(norm(C-A) - np.sqrt(13)) < 1e-10, 'CA=√13 fail'

D = np.array([2*np.sqrt(3), 0.0])
assert abs(norm(A-D) - 2) < 1e-10, 'AD=2 fail'
assert D[0] < C[0] and D[0] > B[0], 'D not on BC fail'

def circumcircle(P1, P2, P3):
    ax,ay=P1; bx,by=P2; cx,cy=P3
    Dv = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    ux = ((ax**2+ay**2)*(by-cy)+(bx**2+by**2)*(cy-ay)+(cx**2+cy**2)*(ay-by))/Dv
    uy = ((ax**2+ay**2)*(cx-bx)+(bx**2+by**2)*(ax-cx)+(cx**2+cy**2)*(bx-ax))/Dv
    center = np.array([ux, uy])
    return center, norm(P1-center)

ctr, R = circumcircle(A, B, D)
assert abs(R - 2) < 1e-9, f'R={R}, expected 2'

AC = C - A
v = A - ctr
s_E = -2*np.dot(v, AC)/np.dot(AC, AC)
assert 0 < s_E < 1, f's_E={s_E} not in (0,1)'
E = A + s_E * AC
assert abs(norm(E-ctr) - R) < 1e-9, 'E not on circumcircle'

# ABDE 사각형이 원에 내접하는지 확인
for P in [A, B, D, E]:
    assert abs(norm(P-ctr) - R) < 1e-9, f'{P} not on circle'

# (가), (나), (다) 계산
p = (norm(A-B)**2 + norm(B-C)**2 - norm(C-A)**2) / (2*norm(A-B)*norm(B-C))  # cos(∠ABC)
q = R  # 외접원 반지름
r = norm(D-E)  # DE

pqr = p * q * r
expected = 6*np.sqrt(13)/13

if abs(pqr - expected) < 1e-8:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: p*q*r={pqr:.10f}, expected={expected:.10f}')
