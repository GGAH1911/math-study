# 파라미터화 솔버 — 구간별 이차함수 |f(x)|=t 의 실근 개수 g(t)
#
# f(x) = (x-a)(x-c)          (a ≤ x ≤ r·a)          ← 원문제: c=4, r=3/2
#      = (x-a)(x-b)          (x < a  또는  x > r·a)   (a, b 는 양수)
# g(t) = |f(x)|=t 의 서로 다른 실근 개수.
#
# 구조(=수학):
#   b < a < c < r·a 이면 |f| 는  ①x<b 에서 무한대→0 으로 내려오는 왼쪽 팔
#   ②(b,a) 의 봉우리 A1=((a-b)/2)^2  ③(a,c) 의 봉우리 A2=((c-a)/2)^2
#   ④x=c 에서 x=r·a 까지 올라가는 가지(최고 J=f(ra^-)=(ra-a)(ra-c))
#   ⑤x=ra 에서 K=f(ra^+)=(ra-a)(ra-b) 로 위로 점프해 무한대로 가는 오른쪽 팔
#   로 이루어진다. 따라서 t→0+ 에서 g=1+2+2+1=6 (조건 (가)).
#   t 가 커지며 ②③④가 사라져 g=1 이 되려면 세 문턱이 한 점에서 겹쳐야 한다:
#        A1 = A2 = J = α      (⇒ b = 2a-c 이고 (ra-a)(ra-c) = ((c-a)/2)^2)
#   그 뒤 t=β=K 에서 오른쪽 팔이 생겨 1→2. 이것이 조건 (나)(불연속은 α, β 둘뿐,
#   lim_{t→α+}g = lim_{t→β-}g = 1)이다.
#   구한 a, b 로 f(0) = (0-a)(0-b) = ab 를 p+q√k 로 분해해 p²+q² 를 답한다.
CANDIDATE = 320

import sympy as sp

# 문제가 준 수치만 담는다 (a, b, α, β 는 solve 가 유도한다)
PARAMS = dict(
    c=4,        # 안쪽 조각 (x-a)(x-c) 의 상수 근
    r_num=3,    # 구간 [a, (r_num/r_den)·a] 의 배율 분자
    r_den=2,    # 같은 배율의 분모
)


# ── |f| 그래프의 실근 개수를 수치로 직접 센다 (조건 (가)(나) 확인용) ──────────────
def _quad_roots(p, q, v):
    """(x-p)(x-q) = v 의 실근."""
    disc = (p - q) ** 2 + 4 * v
    if disc < 0:
        return []
    s = disc ** 0.5
    return [((p + q) - s) / 2, ((p + q) + s) / 2]


def _g(t, a, b, c, r):
    """|f(x)| = t 의 서로 다른 실근 개수 (t > 0)."""
    hi = r * a
    out = []
    for v in (t, -t):
        for x in _quad_roots(a, b, v):          # 바깥 조각: x < a  또는  x > r·a
            if x < a - 1e-12 or x > hi + 1e-12:
                out.append(x)
        for x in _quad_roots(a, c, v):          # 안쪽 조각: a ≤ x ≤ r·a
            if a - 1e-12 <= x <= hi + 1e-12:
                out.append(x)
    out.sort()
    n = 0
    prev = None
    for x in out:
        if prev is None or abs(x - prev) > 1e-9 * max(1.0, abs(x)):
            n += 1
            prev = x
    return n


def _conditions_hold(a, b, c, r):
    """(가) t→0+ 에서 6, (나) 불연속 α, β 에서 6→1→2 인지 수치 확인."""
    a, b, c, r = float(a), float(b), float(c), float(r)
    alpha = ((c - a) / 2) ** 2
    beta = (r * a - a) * (r * a - b)
    if not (0 < alpha < beta):
        return False
    e = 1e-7 * max(1.0, alpha)
    return (_g(e, a, b, c, r) == 6            # (가) t→0+ 에서 6
            and _g(alpha + e, a, b, c, r) == 1  # (나) lim_{t→α+} = 1
            and _g(beta - e, a, b, c, r) == 1   # (나) lim_{t→β-} = 1
            and _g(beta + e, a, b, c, r) == 2)  # β 위에서는 오른쪽 팔이 살아나 2


def _split_surd(val):
    """유리수 p 와 q 로 val = p + q√k 분해."""
    val = sp.expand(sp.radsimp(sp.simplify(val)))
    sq = sorted((z for z in val.atoms(sp.Pow) if z.exp == sp.Rational(1, 2)), key=sp.default_sort_key)
    if not sq:
        return sp.simplify(val), sp.Integer(0)
    p, rest = val.as_independent(sq[0], as_Add=True)
    return sp.simplify(p), sp.simplify(rest / sq[0])


def solve(prm=None):
    prm = PARAMS if prm is None else prm
    c = sp.nsimplify(prm['c'])
    r = sp.nsimplify(prm['r_num']) / sp.nsimplify(prm['r_den'])
    a = sp.symbols('a', positive=True)

    b = 2 * a - c                                   # A1 = A2  ⇔  a-b = c-a
    peak = ((c - a) / 2) ** 2                       # 두 봉우리의 공통 높이 α
    jump = (r * a - a) * (r * a - c)                # J = f(r·a^-)

    found = []
    for s in sp.solve(sp.Eq(jump, peak), a):        # J = α (세 문턱이 겹칠 조건)
        s = sp.nsimplify(sp.simplify(s))
        if not s.is_real or not s.is_number or s <= 0:
            continue
        bv = sp.simplify(2 * s - c)
        # 모양 조건: 0 < b < a < c < r·a 이고 안쪽 봉우리 꼭짓점이 구간 안
        if not (bv.is_number and bv > 0 and bv < s and s < c and c < r * s and (s + c) / 2 <= r * s):
            continue
        if not _conditions_hold(s, bv, c, r):
            continue
        found.append((s, bv))
    if not found:
        raise ValueError('조건 (가)(나)를 만족하는 a, b 가 없다')

    a0, b0 = found[0]
    p, q = _split_surd(a0 * b0)                     # f(0) = (0-a)(0-b) = ab = p + q√k
    return sp.simplify(p ** 2 + q ** 2)


def statement(prm=None):
    prm = PARAMS if prm is None else prm
    r = sp.Rational(prm['r_num'], prm['r_den'])
    return (f"두 양수 a, b에 대하여 함수 f(x)는 f(x)=(x-a)(x-{sp.nsimplify(prm['c'])}) "
            f"({sp.latex(r)}a 이하 구간 a≤x≤{sp.latex(r)}a), f(x)=(x-a)(x-b) "
            f"(x<a 또는 x>{sp.latex(r)}a) 이다. 양의 실수 t에 대하여 방정식 |f(x)|=t의 "
            "서로 다른 실근의 개수를 g(t)라 하자. (가) lim_{t→0+}g(t)=6 "
            "(나) g(t)는 t=α, t=β(α≠β)에서만 불연속이고 lim_{t→α+}g(t)=lim_{t→β-}g(t)=1. "
            "f(0)=p+q√k일 때 p²+q²의 값을 구하시오.")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
