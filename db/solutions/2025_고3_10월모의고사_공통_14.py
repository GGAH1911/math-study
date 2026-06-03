import numpy as np
from numpy import sin, cos, pi, sqrt

# Solve original constraints numerically: sin(beta)=3 sin(alpha), sqrt(5) sin(alpha+beta)=8 sin(alpha)
def f(alpha):
    beta = np.arcsin(3*np.sin(alpha))
    return sqrt(5)*sin(alpha+beta) - 8*sin(alpha)

lo, hi = 0.01, 0.3
for _ in range(200):
    mid = 0.5*(lo+hi)
    if f(mid)*f(lo) > 0: lo = mid
    else: hi = mid
alpha = 0.5*(lo+hi)
beta = np.arcsin(3*np.sin(alpha))

sa, sb = sin(alpha), sin(beta)
AE_given = sqrt(5); BC_given = 6.0
# Construct geometry from law of sines (using ORIGINAL conditions, not the derived area)
AD = AE_given * sin(alpha+beta) / sb
DE = AE_given * sa / sb
BD = BC_given * sin(beta-alpha) / sb
DC = BC_given * sa / sb

# Place coordinates: D origin, AC along x-axis, B in lower half-plane
A = np.array([-AD, 0.0])
C = np.array([ DC, 0.0])
D = np.array([0.0, 0.0])
B = np.array([-BD*cos(beta), -BD*sin(beta)])
E = np.array([-DE*cos(beta), -DE*sin(beta)])

def ang(P,Q,R):
    v1=P-Q; v2=R-Q
    return np.arccos(np.clip(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)),-1,1))

# Check ORIGINAL problem conditions
c_BC   = abs(np.linalg.norm(C-B) - 6.0) < 1e-9
c_AE   = abs(np.linalg.norm(E-A) - sqrt(5)) < 1e-9
c_AD43 = abs(np.linalg.norm(A-D)/np.linalg.norm(D-C) - 4.0/3.0) < 1e-9
c_ang  = abs(ang(D,A,E) - ang(D,B,C)) < 1e-9
c_sin  = abs(sin(ang(D,A,E))/sin(ang(E,D,A)) - 1.0/3.0) < 1e-9
t = np.dot(E-B, D-B)/np.dot(D-B, D-B)
perp = np.linalg.norm((E-B) - t*(D-B))
c_onBD = (0.0 <= t <= 1.0) and perp < 1e-9

# Circumradius of BCD from coordinates (independent of derivation)
def circumR(P1,P2,P3):
    a=np.linalg.norm(P2-P3); b=np.linalg.norm(P1-P3); c=np.linalg.norm(P1-P2)
    s=(a+b+c)/2.0
    A=sqrt(s*(s-a)*(s-b)*(s-c))
    return a*b*c/(4.0*A)

R = circumR(B,C,D)
area = pi * R*R
expected = 180.0*pi/11.0
c_area = abs(area - expected) < 1e-7

if all([c_BC, c_AE, c_AD43, c_ang, c_sin, c_onBD, c_area]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
