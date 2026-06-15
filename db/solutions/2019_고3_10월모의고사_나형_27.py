"""2019 고3 10월모의고사 나형 27번 — 파라미터 솔버 (수동).
최고차1 삼차 f. (가)lim_{x→0}(f(x)-3)/x=0 → f(0)=3, f'(0)=0. (나)y=f 와 y=-1 교점 2개.
f=x³+px²+3, f=-1 ↔ x³+px²+4=0 이 중근(2 distinct) → s³/2=4,s=2,p=-3.
f=x³-3x²+3, f(4)=19. (답 19)"""
import sympy as sp
def solve():
    x,p=sp.symbols('x p'); f=x**3+p*x**2+3
    # x³+px²+4=0 이 이중근 → 판별식0
    pv=[s for s in sp.solve(sp.discriminant(x**3+p*x**2+4,x),p) if s.is_real]
    # 교점 2개(이중근+단근) 되는 실수 p 선택: f(4) 가 정수
    for P in pv:
        fr=f.subs(p,P)
        roots=sp.solve(fr+1,x)
        if len([r for r in roots if r.is_real])>=1 and len(set(sp.solve(fr+1,x)))==2:
            return fr.subs(x,4)
    return None
assert solve()==19, solve()
print('VERIFY_PASS')
