"""2019 고3 7월모의고사 가형 30번 — 파라미터 솔버 (수동).
사차 f, 극대 x=a>0. g=(1-cosπx)/f (f≠0), 7π²/128 (f=0). g 미분가능.
(가)g'(0)g'(2a)≠0 → 0이 f의 근(이중) 강제. (나)g 극값 at a → a 정수. g(1)=2/7→f(1)=7.
이중근 0,s(짝수정수), 극대 a=s/2 정수, 극한값 k s²=64/7, f(1)=k(1-s)²=7 → |1-s|/s=7/8 → s=8,a=4,k=1/7.
f=(1/7)x²(x-8)². g(-1)=2/f(-1)=2/(81/7)=14/81 → p+q=81+14=95."""
import sympy as sp
def solve():
    x=sp.symbols('x'); k,s=sp.symbols('k s',positive=True)
    # k s²=64/7,  k(1-s)²=7  (s>1)
    sol=sp.solve([k*s**2-sp.Rational(64,7), k*(1-s)**2-7],[k,s],dict=True)
    s0=[t for t in sol if t[s]>1][0]
    f=s0[k]*x**2*(x-s0[s])**2
    g_m1=(1-sp.cos(-sp.pi))/f.subs(x,-1)        # 1-cos(-π)=2
    q,p=sp.fraction(sp.nsimplify(g_m1))
    assert sp.gcd(p,q)==1
    return int(p+q)
assert solve()==95, solve()
print('VERIFY_PASS')
