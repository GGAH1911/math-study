# 2026 고3 7월 미적분 26번 — 파라미터화 솔버
#   곡선 y=base^x 가 두 직선 y=t, y=t+gap 과 만나는 점 P, Q 의 x좌표 차가 f(t).
#   base^x=t  →  x=log_base(t),   base^x=t+gap  →  x=log_base(t+gap)
#   f(t) = (ln(t+gap) - ln t)/ln(base)
#   구하는 값 = ∫_lo^hi f(t)/t^power dt  (부분적분)
# 보기 중 그 값과 같은 것의 번호가 답이다.
import sympy as sp

CANDIDATE = 1

PARAMS = dict(
    base=sp.E,                       # 곡선 y = base^x
    gap=2,                           # 두 직선 y=t, y=t+gap 의 간격
    power=2,                         # 피적분함수 f(t)/t^power 의 분모 차수
    lo=sp.Rational(2, 3),            # 적분 아래끝
    hi=2,                            # 적분 위끝
    choices=[                        # 보기 ①~⑤ (원문제 그대로, 오름차순)
        -1 + 3 * sp.log(2),
        -1 + 4 * sp.log(2),
        4 * sp.log(2),
        1 + 3 * sp.log(2),
        1 + 4 * sp.log(2),
    ],
)


def value(prm):
    """정적분 ∫_lo^hi f(t)/t^power dt 의 정확한 값."""
    t = sp.symbols('t', positive=True)
    f = (sp.log(t + prm['gap']) - sp.log(t)) / sp.log(prm['base'])   # 두 교점의 x좌표 차
    val = sp.integrate(f / t ** prm['power'], (t, prm['lo'], prm['hi']))
    return sp.expand_log(sp.simplify(val), force=True)


def make_choices(v):
    """값 v 에 대한 5지선다 보기(오름차순) 자동 생성 — 상수항·로그계수를 ±1 흔든 오답."""
    ve = sp.expand_log(sp.simplify(v), force=True)
    terms = sp.Add.make_args(ve)
    rat = sum([x for x in terms if not x.has(sp.log)], sp.Integer(0))
    logpart = sp.simplify(ve - rat)
    c, k = logpart.as_coeff_Mul()
    if k.func is sp.log and k.args[0].is_Integer:      # log(64) → 6·log(2) 로 펴서 계수를 흔든다
        fac = sp.factorint(int(k.args[0]))
        if len(fac) == 1:
            p0, e0 = next(iter(fac.items()))
            c, k = c * e0, sp.log(p0)
    if k.func is sp.log:
        c2 = c - 1 if c - 1 != 0 else c + 2        # 로그계수 0(=로그항 소멸)은 오답으로 부적절
        cand = [ve, rat + 1 + logpart, rat - 1 + logpart,
                rat + (c + 1) * k, rat + c2 * k]
    else:
        cand = [ve, ve + 1, ve - 1, ve + 2, ve - 2]
    out = []
    for x in cand:
        x = sp.simplify(x)
        if not any(sp.simplify(x - y) == 0 for y in out):
            out.append(x)
    return sorted(out, key=lambda x: float(x))


def solve(prm):
    """조건 → 정답 보기번호. 보기에 없으면 0(보기를 함께 새로 만들어야 하는 변형)."""
    v = value(prm)
    ch = prm.get('choices') or make_choices(v)
    for i, c in enumerate(ch, 1):
        if sp.simplify(sp.nsimplify(v) - sp.nsimplify(c)) == 0:
            return i
    return 0


def statement(prm):
    """새 문제 문장(보기 자동 생성)."""
    v = value(prm)
    ch = prm.get('choices') or make_choices(v)
    b = '' if prm['base'] == sp.E else sp.latex(prm['base'])
    curve = 'e^{x}' if prm['base'] == sp.E else f'{b}^{{x}}'
    body = (f"양수 $t$에 대하여 곡선 $y={curve}$과 두 직선 $y=t$, $y=t+{sp.latex(prm['gap'])}$가 "
            f"만나는 점을 각각 P, Q라 할 때, 두 점 P, Q의 $x$좌표의 차를 $f(t)$라 하자. "
            f"$\\displaystyle\\int_{{{sp.latex(prm['lo'])}}}^{{{sp.latex(prm['hi'])}}}"
            f"\\dfrac{{f(t)}}{{t^{{{sp.latex(prm['power'])}}}}}\\,dt$의 값은?")
    marks = '①②③④⑤'
    opts = ' '.join(f'{marks[i]} ${sp.latex(c)}$' for i, c in enumerate(ch))
    return f"{body}\n{opts}\n(답: {marks[solve(prm) - 1]}  값 = {sp.latex(v)})"


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
