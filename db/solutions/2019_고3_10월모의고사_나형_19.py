"""2019 고3 10월모의고사 나형 19번 — 파라미터 솔버 (수동).
AB=2,BC=4,∠B=60° 삼각형. 마름모 D1BE1F1(F1 on CA) 내부 ∩ 부채꼴(중심B,반경 BE1,60°) 외부.
s=BE1=4/3. S1=마름모-부채꼴=s²sin60°-(1/6)πs²=8(3√3-π)/27. 다음삼각형 CE1F1 닮음비 2/3,넓이비 4/9.
lim=S1/(1-4/9)=(9/5)S1=8(3√3-π)/15. (답 ③)"""
import sympy as sp
def solve():
    s=sp.Rational(4,3)
    S1=s**2*sp.sin(sp.pi/3) - sp.Rational(1,6)*sp.pi*s**2
    lim=S1/(1-sp.Rational(4,9))
    return sp.simplify(lim)
CAND=sp.Rational(8,15)*(3*sp.sqrt(3)-sp.pi)    # 보기 ③
assert sp.simplify(solve()-CAND)==0, solve()
print('VERIFY_PASS')
