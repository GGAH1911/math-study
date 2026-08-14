# f(x)=3x^2+4 의 한 부정적분 F, F(0)+F(2)=14 → F(3)?
# 구조: F(x)=∫f dx + C 로 두고 조건식 F(p)+F(q)=S 로 적분상수 C 를 실제로 풀어 F(t) 를 구한다.
# 파라미터화: f 의 계수·조건에 쓰인 두 점(p,q)·조건값 S·구하는 점 t 를 바꾸면 새 문제가 된다.
CANDIDATE = 38
import sympy as sp

PARAMS = dict(
    c2=3,    # f(x) = c2*x^2 + c1*x + c0 의 이차항 계수
    c1=0,    #                            일차항 계수
    c0=4,    #                            상수항
    p=0,     # 조건 F(p) + F(q) = S 의 첫 번째 점
    q=2,     # 조건의 두 번째 점
    S=14,    # 조건값
    t=3,     # 구하는 함숫값의 점 F(t)
)


def solve(prm=PARAMS):
    x, C = sp.symbols('x C')
    f = prm['c2'] * x**2 + prm['c1'] * x + prm['c0']
    F = sp.integrate(f, x) + C                      # 부정적분 + 적분상수
    C0 = sp.solve(sp.Eq(F.subs(x, prm['p']) + F.subs(x, prm['q']), prm['S']), C)[0]
    return sp.nsimplify(sp.simplify(F.subs({x: prm['t'], C: C0})))


def statement(prm=PARAMS):
    x = sp.Symbol('x')
    f = sp.nsimplify(prm['c2']) * x**2 + sp.nsimplify(prm['c1']) * x + sp.nsimplify(prm['c0'])
    return (f"함수 f(x)={sp.latex(sp.expand(f))} 의 한 부정적분 F(x)에 대하여 "
            f"F({prm['p']})+F({prm['q']})={prm['S']} 일 때, F({prm['t']})의 값을 구하시오.")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
