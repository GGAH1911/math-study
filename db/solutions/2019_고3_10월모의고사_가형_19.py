"""2019 고3 10월모의고사 가형 19번 — 파라미터 솔버 (수동).
모서리1 정사면체 ABCD. M=중점 AB, N=CD 3:1 내분(CN:ND=3:1). P(AC 위) MP+PN 최소,
Q(AD 위) MQ+QN 최소. 삼각형 MPQ 의 평면 BCD 정사영 넓이. (답 ② √3/15)
반사 최소 → AP:PC=2:3, AQ:QD=2:1. 정사영=xy성분 삼각형 넓이 = √3/15."""
import numpy as np
from scipy.optimize import minimize_scalar
def solve():
    B=np.array([0,0,0.]); C=np.array([1,0,0.]); Dp=np.array([0.5,np.sqrt(3)/2,0])
    A=np.array([0.5,np.sqrt(3)/6,np.sqrt(6)/3])
    M=(A+B)/2; N=C+0.75*(Dp-C)
    def Pmin(X):
        f=lambda t:np.linalg.norm(M-(A+t*(X-A)))+np.linalg.norm(N-(A+t*(X-A)))
        return A+minimize_scalar(f,bounds=(0,1),method='bounded').x*(X-A)
    P=Pmin(C); Q=Pmin(Dp)
    m,p,q=M[:2],P[:2],Q[:2]
    return 0.5*abs((p[0]-m[0])*(q[1]-m[1])-(q[0]-m[0])*(p[1]-m[1]))
assert abs(solve()-np.sqrt(3)/15)<1e-5, solve()
print('VERIFY_PASS')
