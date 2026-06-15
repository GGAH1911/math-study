"""2019 고3 10월모의고사 가형 29번 — 파라미터 솔버 (수동).
A(-1,0,6),B(2,-√3,0),C(3,0,0). |AP|=2, |CQ|=2√3, BC·CQ=6. max|PQ|. (답 12)
P: 구(A,2). Q: 구(C,2√3)∩평면(BC·CQ=6) = 원(중심 C+3·BĈ, r=√3). max|PQ|=2+max|AQ|=2+10=12."""
import sympy as sp
def solve():
    A=sp.Matrix([-1,0,6]); B=sp.Matrix([2,-sp.sqrt(3),0]); C=sp.Matrix([3,0,0])
    BC=C-B; ub=BC/BC.norm()
    rCQ=2*sp.sqrt(3)
    cos=sp.Rational(6,1)/(BC.norm()*rCQ)      # BC·CQ=|BC||CQ|cosθ=6
    d=rCQ*cos                                  # 축방향 거리
    Oc=C+d*ub; rc=rCQ*sp.sqrt(1-cos**2)        # 원 중심·반지름
    AO=A-Oc
    h=AO.dot(ub)                               # 원 평면 수직성분
    rho=sp.sqrt(AO.dot(AO)-h**2)               # 평면내 성분
    maxAQ=sp.sqrt(h**2+(rho+rc)**2)
    return sp.simplify(2+maxAQ)
assert solve()==12, solve()
print('VERIFY_PASS')
