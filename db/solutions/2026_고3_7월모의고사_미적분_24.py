# 유형: 함수방정식 f(g(x)) = h(x) 에서 연쇄법칙으로 f'(t) 구하기
#   g(x) = a x^3 + b x + c,  h(x) = const - amp*sin(freq*pi*x)
#   양변 미분: f'(g(x)) * g'(x) = h'(x)
#   g(x0) = t 인 x0 를 찾으면  f'(t) = h'(x0) / g'(x0)
# 원문제: g(x)=x^3+2x+2, h(x)=3-sin(pi x), t=5  ->  x0=1, f'(5)=pi/5 (보기 ②)
import sympy as sp

CANDIDATE = 2

PARAMS = dict(
    a=1,            # 안쪽 삼차항 계수
    b=2,            # 안쪽 일차항 계수
    c=2,            # 안쪽 상수항
    target=5,       # 도함수를 묻는 점 t  (f'(t))
    const=3,        # 우변 상수항
    amp=1,          # 우변 sin 앞 계수 (h = const - amp*sin(...))
    freq=1,         # sin 안의 pi 배수
    choices=[sp.pi/10, sp.pi/5, 3*sp.pi/10, 2*sp.pi/5, sp.pi/2],   # ①~⑤ 보기 값
)


def _inner_point(prm):
    """g(x) = target 을 만족하는 실수 x0 (a>0, b>0 이면 증가함수라 유일)."""
    x = sp.Symbol('x', real=True)
    poly = sp.Poly(prm['a']*x**3 + prm['b']*x + prm['c'] - prm['target'], x)
    reals = sp.real_roots(poly)
    if not reals:
        raise ValueError('g(x)=target 을 만족하는 실근이 없다')
    return x, sp.simplify(reals[0])


def answer_value(prm):
    """f'(target) 의 값 — 연쇄법칙 f'(g(x0))*g'(x0) = h'(x0)."""
    x, x0 = _inner_point(prm)
    g = prm['a']*x**3 + prm['b']*x + prm['c']
    h = prm['const'] - prm['amp']*sp.sin(prm['freq']*sp.pi*x)
    gp = sp.diff(g, x).subs(x, x0)
    if sp.simplify(gp) == 0:
        raise ValueError("g'(x0)=0 이라 f'(target) 이 정해지지 않는다")
    return sp.simplify(sp.diff(h, x).subs(x, x0) / gp)


def solve(prm):
    """보기 중 답의 번호를 돌려준다. (보기에 없는 값이면 값 자체를 돌려준다 — 변형문제 생성용)"""
    val = answer_value(prm)
    vn = complex(sp.N(val, 30)).real
    for i, ch in enumerate(prm.get('choices') or [], start=1):
        if abs(complex(sp.N(ch, 30)).real - vn) < 1e-18 or sp.simplify(val - ch) == 0:
            return i
    return sp.Float(vn, 15)


def statement(prm):
    """새 문제 문장."""
    x = sp.Symbol('x')
    g = sp.nsimplify(prm['a'])*x**3 + sp.nsimplify(prm['b'])*x + sp.nsimplify(prm['c'])
    h = sp.nsimplify(prm['const']) - sp.nsimplify(prm['amp'])*sp.sin(prm['freq']*sp.pi*x)
    opts = ' '.join(f'{n}{sp.latex(v)}' for n, v in
                    zip('①②③④⑤', prm.get('choices') or []))
    return (f"실수 전체의 집합에서 미분가능한 함수 f(x)가 모든 실수 x에 대하여 "
            f"f({sp.latex(g)}) = {sp.latex(h)} 를 만족시킬 때, "
            f"f'({prm['target']})의 값은? {opts}").strip()


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
