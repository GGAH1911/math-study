"""2026 고3 7월 모의고사 기하 26번 — 타원의 정의 + 접선의 두 절편

원문제: 두 점 F(c,0), F′(-c,0)(c>0)을 초점으로 하는 타원 x²/48 + y²/(4b²) = 1 위의
  제1사분면 위의 점 P(6, b)에서의 접선이 x축, y축과 만나는 점을 각각 A, B라 하자.
  PF + PF′ = AB 일 때, b²×c 의 값은?   ① 20 ② 24 ③ 28 ④ 32 ⑤ 36

수학 구조(파라미터화):
  타원  x²/A + y²/(m·b²) = 1,  제1사분면의 점 P(px, b)
    P 가 타원 위  →  px²/A + b²/(m b²) = 1  →  px²/A = 1 - 1/m  →  px = √(A(m-1)/m)
      (그래서 px 는 파라미터가 아니라 A, m 에서 유도되는 값이다. 원문제: A=48, m=4 → px=6)
    P 에서의 접선  px·x/A + b·y/(m b²) = 1  →  x/(A/px) + y/(m b) = 1
      ⇒ A(A/px, 0),  B(0, m b),  AB = √((A/px)² + (m b)²)
    타원의 정의    PF + PF′ = 장축의 길이 = 2√A
    조건 2√A = AB 로 b² 이 정해지고,  c² = A - m b²  (초점이 x축 위)
    답 = b² × c 를 보기 값들과 대조해 보기 번호를 고른다.

  A, m 을 바꾸면 b², c 가 함께 바뀌어 같은 유형의 새 문제가 나오고,
  ch_start / ch_step / n_choices 로 보기 ①~⑤ 를 만든다(정답 번호는 solve 가 계산).
"""
import sympy as sp

CANDIDATE = 4

PARAMS = dict(
    A=48,          # 타원 x²/A + y²/(m b²) = 1 의 x² 분모 (장축쪽)
    m=4,           # y² 분모에 붙은 b² 의 계수 (원문제의 "4b²")
    ch_start=20,   # 보기 ① 의 값
    ch_step=4,     # 보기 사이의 간격 → 20, 24, 28, 32, 36
    n_choices=5,
)


def choices_of(prm):
    """보기 ①~⑤ 의 값 목록."""
    s, d = sp.nsimplify(prm['ch_start']), sp.nsimplify(prm['ch_step'])
    return [sp.nsimplify(s + i * d) for i in range(int(prm['n_choices']))]


def geometry(prm):
    """조건으로부터 (px, b², c) 를 실제로 푼다. 성립 불가능한 설정이면 None."""
    A, m = sp.nsimplify(prm['A']), sp.nsimplify(prm['m'])
    if A <= 0 or m <= 1:
        return None                                   # px² = A(m-1)/m > 0 이어야 한다
    b, x, y = sp.symbols('b x y', positive=True)

    px = sp.sqrt(sp.simplify(A * (m - 1) / m))        # P(px, b) 가 타원 위라는 조건
    tangent = sp.Eq(px * x / A + b * y / (m * b**2), 1)   # P 에서의 접선
    ax = sp.solve(tangent.subs(y, 0), x)[0]           # x절편 → A(ax, 0)
    by = sp.solve(tangent.subs(x, 0), y)[0]           # y절편 → B(0, by)
    AB = sp.sqrt(ax**2 + by**2)

    # 타원의 정의: PF + PF′ = 장축의 길이 = 2√A. 이것이 AB 와 같다.
    sols = [s for s in sp.solve(sp.Eq(2 * sp.sqrt(A), AB), b) if s.is_real and s > 0]
    if not sols:
        return None                                   # b > 0 인 해가 없다 = 문제가 성립 안 함
    b2 = sp.simplify(sols[0]**2)
    c2 = sp.simplify(A - m * b2)                      # 초점이 x축 위 (A > m b²)
    if not c2.is_real or c2 <= 0:
        return None
    return sp.simplify(px), b2, sp.sqrt(c2)


def value(prm):
    """문제가 묻는 값 b² × c."""
    g = geometry(prm)
    return None if g is None else sp.simplify(g[1] * g[2])


def solve(prm=None):
    """조건 → 답(보기 번호). 보기 중에 해당 값이 없으면 0."""
    prm = PARAMS if prm is None else prm
    val = value(prm)
    if val is None:
        return 0
    for i, v in enumerate(choices_of(prm), start=1):
        if sp.simplify(v - val) == 0:
            return i
    return 0


def statement(prm=None):
    """파라미터로부터 새 문제 문장을 만든다."""
    prm = PARAMS if prm is None else prm
    g = geometry(prm)
    if g is None:
        return '(주어진 파라미터로는 문제가 성립하지 않습니다)'
    px = g[0]
    A, m = sp.nsimplify(prm['A']), sp.nsimplify(prm['m'])
    coef = '' if m == 1 else sp.latex(m)
    marks = '①②③④⑤⑥⑦⑧⑨'
    opts = ' '.join(f'{marks[i]} ${sp.latex(v)}$'
                    for i, v in enumerate(choices_of(prm)))
    return (
        f"두 점 $F(c,0)$, $F'(-c,0)$ $(c>0)$ 을 초점으로 하는 타원 "
        f"$\\dfrac{{x^2}}{{{sp.latex(A)}}}+\\dfrac{{y^2}}{{{coef}b^2}}=1$ 위에 있는 "
        f"제1사분면 위의 점 $P({sp.latex(px)},\\,b)$ 에서의 접선이 $x$축, $y$축과 만나는 점을 "
        f"각각 $A$, $B$ 라 하자. $\\overline{{PF}}+\\overline{{PF'}}=\\overline{{AB}}$ 일 때, "
        f"$b^2\\times c$ 의 값은?\n{opts}"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
