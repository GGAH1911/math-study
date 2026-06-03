import numpy as np

def build(theta):
    A=np.array([-1.0,0.0]); B=np.array([1.0,0.0]); O=np.array([0.0,0.0])
    # P: 반원 위, angle OAP = theta
    # P = A + r*(cos theta, sin theta), 원 위 조건으로 r=2cos theta
    r=2*np.cos(theta)
    P=A+r*np.array([np.cos(theta),np.sin(theta)])
    # 원래 방정식 확인
    assert abs(P[0]**2+P[1]**2-1)<1e-12, 'P not on circle'
    # Q: 직선 OP와 직선 x=1 교점
    # OP 방향 = P/|P|. param: t*P/|P|. x=1 -> t = 1/(P[0]/|P|) = |P|/P[0]
    Q=np.array([1.0, P[1]/P[0]])
    # 검증: Q-O와 P-O 평행
    assert abs(Q[0]*P[1]-Q[1]*P[0])<1e-10
    # 각 OQB의 이등분선: 단위벡터 합
    u_QO=(O-Q)/np.linalg.norm(O-Q)
    u_QB=(B-Q)/np.linalg.norm(B-Q)
    bis=u_QO+u_QB
    # 직선 AP와 교점 R
    dirAP=np.array([np.cos(theta),np.sin(theta)])
    M=np.column_stack([dirAP,-bis])
    rhs=Q-A
    s=np.linalg.solve(M,rhs)
    R=A+s[0]*dirAP
    # R이 이등분선 위에 있는지 다시 검증
    R_chk=Q+s[1]*bis
    assert np.allclose(R,R_chk,atol=1e-10)
    return A,P,Q,R

def tri_area(P1,P2,P3):
    return 0.5*abs((P2[0]-P1[0])*(P3[1]-P1[1])-(P2[1]-P1[1])*(P3[0]-P1[0]))

def ratio(theta):
    A,P,Q,R=build(theta)
    O=np.array([0.0,0.0])
    f=tri_area(O,A,P)
    g=tri_area(P,Q,R)
    return g/(theta**4*f)

vals=[ratio(t) for t in [1e-2,1e-3,1e-4,1e-5]]
# 극한 -> 2
if all(abs(v-2)<5e-2 for v in vals) and abs(vals[-1]-2)<1e-3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', vals)
