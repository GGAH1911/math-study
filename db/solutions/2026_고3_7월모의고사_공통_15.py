"""2026 고3 7월모의고사 공통 15 — 파라미터화 솔버 (유사문제 재생성용).

문제 구조
    f(x) = f3·x³ + f2·a·x² + b,      g(x) = g3·x³ + g2·a·x²
    h(x) = f(x) + |f(x) − g(x)|
    (가) h 는 x = x0 에서만 미분가능하지 않다.
    (나) h 는 x = xmax 에서 극대이고 x = α, β (α<β) 에서 극소이다.
    (다) h(α) − h(β) ≥ hgap
    이때 a+b 의 최댓값 M, 최솟값 m 에 대하여 M − m 의 값은?

수학 구조 (답을 박아 넣지 않고 실제로 푼다)
    p = f − g 라 두면  h = 2f − g (p>0 인 곳),  h = g (p<0 인 곳).
    · (가) ⇒ p(x0)=0 이어야 하므로 b 가 a 로 결정된다: b = −(f3−g3)·x0³ − (f2−g2)·a·x0².
      또한 p 의 **부호변화점이 x0 하나뿐**이어야 한다(짝수중근은 미분가능하므로 허용).
    · (나)(다) 는 주어진 a 마다 h 의 조각별 도함수 부호를 실제로 따져 극대·극소를
      전부 찾아 판정한다.
    · a+b 는 a 의 일차식이므로, 조건을 만족하는 a 의 하한·상한만 이분법으로 잡아내면
      M 과 m 이 그 두 끝에서 나온다. M − m 을 보기와 대조해 답 번호를 정한다.
"""
from sympy import Rational, nsimplify, sympify, simplify
import numpy as np

CANDIDATE = 1

PARAMS = dict(
    f3=Rational(1, 6),      # f(x) = f3·x³ + f2·a·x² + b
    f2=Rational(1, 2),
    g3=Rational(2, 3),      # g(x) = g3·x³ + g2·a·x²
    g2=Rational(1),
    x0=-1,                  # (가) 오직 이 점에서만 미분불가능
    xmax=0,                 # (나) 이 점에서 극대
    hgap=0,                 # (다) h(α) − h(β) ≥ hgap
    choices=[Rational(3, 2), Rational(9, 4), Rational(3), Rational(15, 4), Rational(9, 2)],
    a_lo=-20,               # a 탐색 구간
    a_hi=20,
)

# ───────────────────────── 다항식 유틸 (내림차순 계수) ─────────────────────────


def _val(c, x):
    v = 0.0
    for k in c:
        v = v * x + k
    return v


def _der(c):
    n = len(c) - 1
    return [c[i] * (n - i) for i in range(n)] or [0.0]


def _rroots(c):
    """실근 목록 (중근은 수치적으로 갈라져 여러 개로 나올 수 있음)."""
    c = list(c)
    while c and abs(c[0]) < 1e-14:
        c.pop(0)
    if len(c) < 2:
        return []
    if len(c) == 2:
        return [-c[1] / c[0]]
    if len(c) == 3:
        A, B, C = c
        d = B * B - 4 * A * C
        if d < 0:
            return []
        s = d ** 0.5
        return sorted([(-B - s) / (2 * A), (-B + s) / (2 * A)])
    return sorted(float(z.real) for z in np.roots(c) if abs(z.imag) <= 1e-9)


def _dedupe(xs, tol=1e-9):
    out = []
    for x in sorted(xs):
        if not out or x - out[-1] > tol:
            out.append(x)
    return out


# ───────────────────────── 주어진 a 에 대한 h 의 모형 ─────────────────────────


def _model(prm, a):
    """a 하나를 고정했을 때 p = f−g, 그리고 h 의 두 조각(2f−g, g) 계수."""
    A = float(prm['f3'] - prm['g3'])
    B = float(prm['f2'] - prm['g2'])
    x0 = float(prm['x0'])
    b = -(A * x0 ** 3 + B * a * x0 ** 2)                       # (가): p(x0) = 0
    p = [A, B * a, 0.0, b]
    hp = [float(2 * prm['f3'] - prm['g3']),                    # p > 0 : h = 2f − g
          float(2 * prm['f2'] - prm['g2']) * a, 0.0, 2 * b]
    hn = [float(prm['g3']), float(prm['g2']) * a, 0.0, 0.0]    # p < 0 : h = g
    return p, hp, hn


def _sign_changes(p):
    """p 의 부호가 실제로 바뀌는 점 = |p| 가 꺾이는 점 = h 의 미분불가능점."""
    rs = _dedupe(_rroots(p))
    out = []
    for i, r in enumerate(rs):
        gap = min([abs(r - o) for o in rs if o is not r] or [1.0])
        d = min(1e-7, gap / 4) if gap < 1.0 else 1e-7
        if _val(p, r - d) * _val(p, r + d) < 0:
            out.append(r)
    return out


def _extrema(prm, a):
    """h 의 극대점·극소점 (조각별 도함수 부호변화로 판정)."""
    p, hp, hn = _model(prm, a)
    dhp, dhn = _der(hp), _der(hn)
    pts = _dedupe(_rroots(p) + _rroots(dhp) + _rroots(dhn))
    if not pts:
        return [], [], None
    hprime = lambda x: _val(dhp, x) if _val(p, x) > 0 else _val(dhn, x)
    hvalue = lambda x: _val(hp, x) if _val(p, x) > 0 else _val(hn, x)
    xs = [pts[0] - 1.0] + [(pts[i] + pts[i + 1]) / 2 for i in range(len(pts) - 1)] + [pts[-1] + 1.0]
    sg = [1 if hprime(x) > 0 else (-1 if hprime(x) < 0 else 0) for x in xs]
    mx = [pts[i] for i in range(len(pts)) if sg[i] > 0 > sg[i + 1]]
    mn = [pts[i] for i in range(len(pts)) if sg[i] < 0 < sg[i + 1]]
    return mx, mn, hvalue


def _ok(prm, a):
    """a 가 (가)(나)(다) 를 모두 만족하는가."""
    x0, xmax = float(prm['x0']), float(prm['xmax'])
    p, _, _ = _model(prm, a)
    ch = _sign_changes(p)
    if len(ch) != 1 or abs(ch[0] - x0) > 1e-6:              # (가) x0 에서만 미분불가능
        return False
    mx, mn, hv = _extrema(prm, a)
    if len(mx) != 1 or abs(mx[0] - xmax) > 1e-6:           # (나) 극대는 xmax 한 곳
        return False
    if len(mn) != 2:                                       # (나) 극소는 두 곳
        return False
    return hv(mn[0]) - hv(mn[1]) >= float(prm['hgap']) - 1e-12   # (다)


# ───────────────────────── 조건을 만족하는 a 의 범위 ─────────────────────────


def _boundary(prm, inside, outside):
    for _ in range(40):
        mid = (inside + outside) / 2
        if _ok(prm, mid):
            inside = mid
        else:
            outside = mid
    return (inside + outside) / 2


def _snap(x):
    """이분법으로 얻은 끝점을 가까운 유리수로 되돌린다(없으면 근사 유리수)."""
    for den in (1, 2, 3, 4, 6, 8, 12, 16, 24, 100, 1000):
        r = Rational(x).limit_denominator(den)
        if abs(float(r) - x) < 1e-7:
            return r
    return Rational(x).limit_denominator(10 ** 7)


def _a_range(prm):
    lo, hi, step = float(prm['a_lo']), float(prm['a_hi']), 0.02
    n = int((hi - lo) / step)
    grid = [lo + (k + 0.5) * step for k in range(n)]        # 격자점이 특이점에 딱 걸리지 않게 반칸 이동
    good = [x for x in grid if _ok(prm, x)]
    if not good:
        raise ValueError('조건을 만족하는 a 가 없다 (문제가 성립하지 않음)')
    a_min = _boundary(prm, good[0], good[0] - step)
    a_max = _boundary(prm, good[-1], good[-1] + step)
    return _snap(a_min), _snap(a_max)


def _ab(prm, a):
    """a+b — (가) 로 b 가 a 에 의해 정해지므로 a 의 일차식."""
    A, B, x0 = prm['f3'] - prm['g3'], prm['f2'] - prm['g2'], sympify(prm['x0'])
    return a + (-(A * x0 ** 3 + B * a * x0 ** 2))


def solve_value(prm=None):
    """M − m 의 값."""
    prm = dict(PARAMS if prm is None else prm)
    a_min, a_max = _a_range(prm)
    vals = [_ab(prm, a_min), _ab(prm, a_max)]
    return simplify(max(vals) - min(vals))


def solve(prm=None):
    """조건 → 답. 객관식이므로 계산값을 보기와 대조해 **보기 번호**를 돌려준다.
    (보기 밖의 값이 나오는 변형 문제라면 값 자체를 돌려준다 — statement() 가 보기를 새로 만든다.)"""
    prm = dict(PARAMS if prm is None else prm)
    val = solve_value(prm)
    for i, c in enumerate(prm.get('choices') or [], 1):
        if simplify(sympify(c) - val) == 0:
            return i
    return val


# ───────────────────────── 유사문제 문장 생성 ─────────────────────────


def _opts(prm, val):
    ch = [sympify(c) for c in (prm.get('choices') or [])]
    if any(simplify(c - val) == 0 for c in ch):
        return ch
    d = abs(val) / 4 if val != 0 else Rational(3, 4)
    return sorted({val + k * d for k in (-2, -1, 0, 1, 2)})


def _c(v, tail):
    """계수를 문장용으로: 1 은 생략, 분수는 \\frac 으로."""
    v = sympify(v)
    if v == 1:
        return tail
    if v == -1:
        return '-' + tail
    s = f'\\frac{{{v.p}}}{{{v.q}}}' if getattr(v, 'q', 1) != 1 else str(v)
    return s + tail


def statement(prm=None):
    """파라미터로 정해지는 새 문제 문장 + 보기 + 정답 번호."""
    prm = dict(PARAMS if prm is None else prm)
    val = solve_value(prm)
    opts = _opts(prm, val)
    num = [i for i, c in enumerate(opts, 1) if simplify(c - val) == 0][0]
    cond = '' if prm['hgap'] == 0 else f" − {prm['hgap']}"
    txt = (f"두 실수 a, b에 대하여 두 함수\n"
           f"  f(x) = {_c(prm['f3'], 'x^3')} + {_c(prm['f2'], 'ax^2')} + b,   "
           f"g(x) = {_c(prm['g3'], 'x^3')} + {_c(prm['g2'], 'ax^2')}\n"
           f"이 있다. 함수 h(x)를 h(x) = f(x) + |f(x) − g(x)| 라 할 때, h(x)는 다음 조건을 만족시킨다.\n"
           f"  (가) 함수 h(x)는 x = {prm['x0']} 에서만 미분가능하지 않다.\n"
           f"  (나) 함수 h(x)는 x = {prm['xmax']} 에서 극대이고 x = α, x = β (α<β)에서 극소이다.\n"
           f"h(α) ≥ h(β){cond} 일 때, a+b의 최댓값을 M, 최솟값을 m이라 하자. M − m의 값은?\n"
           f"  보기: " + ", ".join(f"{i}) {c}" for i, c in enumerate(opts, 1)))
    return {'text': txt, 'choices': opts, 'answer_no': num, 'answer_value': val}


if __name__ == '__main__':
    got = solve(PARAMS)
    print(f'M - m = {solve_value(PARAMS)}  → 보기 {got}번 (CANDIDATE={CANDIDATE})')
    print('VERIFY_PASS' if got == CANDIDATE else 'VERIFY_FAIL')
