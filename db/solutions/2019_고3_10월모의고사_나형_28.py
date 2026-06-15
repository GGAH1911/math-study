"""2019 고3 10월모의고사 나형 28번 — 파라미터 솔버 (수동).
점심 한식K 60%, 양식W 40%. W→W 25%, K→K 30% (즉 K→W 70%, W→W 25%).
P(저녁W)=0.4·0.25+0.6·0.70=0.52. P(K∩저녁W)=0.6·0.70=0.42.
P(점심K|저녁W)=0.42/0.52=21/26 → p+q=47. (답 47)"""
from fractions import Fraction as F
def solve(pK, WW, KK):
    pW=1-pK
    dinW = pW*WW + pK*(1-KK)
    KandW = pK*(1-KK)
    r=KandW/dinW
    return r.denominator + r.numerator
assert solve(F(6,10),F(25,100),F(30,100))==47
print('VERIFY_PASS')
