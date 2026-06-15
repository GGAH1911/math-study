"""2019 고3 10월모의고사 가형 26번 — 파라미터 솔버 (수동).
모비율 p 신뢰도95% CI [0.0706,0.1294]. 중심 p̂=0.1=m/n, 오차 1.96√(p̂q̂/n)=0.0294.
→ √(0.09/n)=0.015 → n=400, m=0.1·400=40 → m+n=440. (답 440)"""
from fractions import Fraction as F
def solve(lo, hi, z):
    phat=F(lo+hi,2); margin=F(hi-lo,2)
    # z√(p̂q̂/n)=margin → n=z²p̂q̂/margin²
    n=z*z*phat*(1-phat)/(margin*margin)
    m=phat*n
    return int(m+n)
assert solve(F(706,10000),F(1294,10000),F(196,100))==440
print('VERIFY_PASS')
