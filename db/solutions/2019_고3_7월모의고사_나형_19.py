"""2019 고3 7월모의고사 나형 19번 — 파라미터 솔버 (수동).
정삼각형(변3) 1:2 내분 → A2B2C2(변√3, 닮음비 1/√3, 넓이비 1/3). R1=지름 B2C1 반원(아래쪽) 내부
∩ 지름 B2C2 반원(아래쪽) 외부. S_n 은 공비 1/3 등비급수 → lim=S1·3/2.
수치적분으로 S1 계산 → lim = (12π+9√3)/32 (보기 ④)."""
import numpy as np
def lim_area(side=3.0):
    B1=np.array([0,0.]); C1=np.array([side,0.]); A1=np.array([side/2, side*np.sqrt(3)/2])
    B2=(2/3)*B1+(1/3)*C1; C2=(2/3)*C1+(1/3)*A1
    OG=(B2+C1)/2; rG=np.linalg.norm(C1-B2)/2
    OS=(B2+C2)/2; rS=np.linalg.norm(C2-B2)/2
    xs=np.linspace(-0.2,side+0.4,2600); ys=np.linspace(-2.0,2.2,2600)
    X,Y=np.meshgrid(xs,ys); cell=(xs[1]-xs[0])*(ys[1]-ys[0])
    inbig=((X-OG[0])**2+(Y-OG[1])**2<=rG**2)
    insml=((X-OS[0])**2+(Y-OS[1])**2<=rS**2)
    dG=C1-B2; nG=np.array([-dG[1],dG[0]]); sG=(X-B2[0])*nG[0]+(Y-B2[1])*nG[1]  # 아래쪽 반원
    dS=C2-B2; nS=np.array([-dS[1],dS[0]]); sS=(X-B2[0])*nS[0]+(Y-B2[1])*nS[1]
    R1=inbig&(sG<=0)&(~(insml&(sS<=0)))
    S1=R1.sum()*cell
    return 1.5*S1                       # Σ 공비 1/3 → S1/(1-1/3)
CAND=(12*np.pi+9*np.sqrt(3))/32         # 보기 ④
assert abs(lim_area()-CAND)<2e-3, (lim_area(),CAND)
print('VERIFY_PASS')
