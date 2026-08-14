# a·cosθ + b·cos(π/2 − θ) = 0 이고 sinθ 의 부호가 주어졌을 때 cosθ 의 값을 고르는 문제.
#   여각 공식 cos(π/2 − θ) = sinθ  →  a·cosθ + b·sinθ = 0
#   sin²θ + cos²θ = 1 과 연립 → cosθ = ±b/√(a²+b²), 부호는 sinθ 조건이 결정.
#
# ★파라미터화 솔버(scripts/CLAUDE.md 규격): PARAMS 를 바꾸면 같은 유형의 새 문제와
#   검증된 답이 그대로 나온다. 원문제는 PARAMS 기본값으로 재현된다.
CANDIDATE = 4
import sympy as sp

PARAMS = dict(
    a=2,                 # cosθ 의 계수
    b=1,                 # cos(π/2 − θ) 의 계수
    sin_positive=0,      # sinθ 의 부호 조건: 0 → sinθ < 0, 1 → sinθ > 0
    choices=(-2*sp.sqrt(5)/5, -sp.sqrt(5)/5, sp.Integer(0), sp.sqrt(5)/5, 2*sp.sqrt(5)/5),
)


def cos_value(prm):
    """조건을 만족하는 cosθ 의 값(보기 번호가 아니라 실제 값)."""
    th = sp.Symbol('theta', real=True)
    # 여각 공식을 sympy 로 확인한 뒤 cos(π/2 − θ) 를 sinθ 로 바꾼다
    assert sp.simplify(sp.cos(sp.pi/2 - th) - sp.sin(th)) == 0
    c, s = sp.symbols('c s', real=True)
    sols = sp.solve([sp.Eq(prm['a']*c + prm['b']*s, 0), sp.Eq(s**2 + c**2, 1)],
                    [s, c], dict=True)
    want = 1 if prm['sin_positive'] else -1
    hits = []
    for sol in sols:
        sv, cv = sp.simplify(sol[s]), sp.simplify(sol[c])
        if not (sv.is_real and cv.is_real):
            continue
        if sp.sign(sv) == want:
            hits.append(sp.nsimplify(sp.radsimp(cv)))
    if len(hits) != 1:
        raise ValueError(f'부호 조건을 만족하는 cosθ 가 유일하지 않다: {hits}')
    return hits[0]


def solve(prm):
    """조건 → 정답 보기 번호. 계산한 값을 보기와 대조해 번호를 정한다."""
    v = cos_value(prm)
    for i, ch in enumerate(prm['choices'], 1):
        if sp.simplify(v - ch) == 0:
            return i
    raise ValueError(f'보기에 없는 값: {v}')


def make_choices(prm):
    """이 유형의 표준 보기 묶음 — 양의 근 크기 m 에 대해 (−2m, −m, 0, m, 2m).
    2m 이 1 을 넘으면 cosθ 의 범위 밖이라 바로 걸러지는 보기가 되므로
    (−m, −m/2, 0, m/2, m) 로 축소한다.
    변형문제를 만들 때 새 보기 목록을 뽑는 용도(solve 는 쓰지 않는다)."""
    m = sp.radsimp(abs(cos_value(prm)))
    ks = (-2, -1, 0, 1, 2) if 2*m <= 1 else (-1, sp.Rational(-1, 2), 0, sp.Rational(1, 2), 1)
    return tuple(sp.nsimplify(sp.radsimp(k*m)) for k in ks)


def statement(prm):
    def coef(x):
        return '' if x == 1 else ('-' if x == -1 else sp.latex(x))
    a, b = prm['a'], prm['b']
    cond = '\\sin\\theta > 0' if prm['sin_positive'] else '\\sin\\theta < 0'
    opts = '  '.join(f'({i}) ${sp.latex(ch)}$' for i, ch in enumerate(prm['choices'], 1))
    return (f'${coef(a)}\\cos\\theta + {coef(b)}\\cos\\left(\\frac{{\\pi}}{{2}}-\\theta\\right) = 0$ 이고 '
            f'${cond}$ 일 때, $\\cos\\theta$ 의 값은?\n  {opts}')


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
