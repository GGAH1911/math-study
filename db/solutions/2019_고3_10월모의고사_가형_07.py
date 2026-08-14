import sympy as sp

# ─────────────────────────────────────────────────────────────────
# 문제의 수학 구조
#   점 P(x, y):  x = A*t + sin(b*t),  y = C - cos(b*t)
#   시각 t = t0 에서의 속력 = sqrt(x'(t0)^2 + y'(t0)^2)
#           = sqrt((A + b*cos(b*t0))^2 + (b*sin(b*t0))^2)
#
# 파라미터로 뽑은 것:
#   A  : x(t)에서 t의 계수 (원문제 2)
#   b  : sin/cos 안의 각속도 계수 (원문제 1)
#   t0 : 속력을 구하는 시각 (원문제 pi/3)
#   C  : y(t)의 상수항(원문제 1) — 미분에서 사라지므로 답에 영향 없음, 문장 생성용으로만 사용
#
# A, t0 을 바꾸면 v^2 = (A + b*cos(b*t0))^2 + (b*sin(b*t0))^2 이 바뀌고,
# 그 값이 보기 5개(연속 정수의 제곱근) 중 어느 자리에 오는지도 함께 바뀐다.
# ─────────────────────────────────────────────────────────────────

PARAMS = dict(A=2, b=1, t0=sp.pi / 3, C=1)


def value(prm):
    """시각 t0 에서의 속력(수학적 답 값)을 sympy 로 실제 미분해 구한다."""
    t = sp.symbols('t')
    A, b, t0, C = prm['A'], prm['b'], prm['t0'], prm['C']
    x = A * t + sp.sin(b * t)
    y = C - sp.cos(b * t)
    dx = sp.diff(x, t).subs(t, t0)
    dy = sp.diff(y, t).subs(t, t0)
    speed = sp.sqrt(sp.simplify(dx ** 2 + dy ** 2))
    speed = sp.simplify(speed)
    if speed.has(sp.zoo, sp.nan, sp.oo) or not speed.is_real:
        raise ValueError(f'유효하지 않은 속력: {speed}')
    return speed


def choices(prm):
    """값 v = sqrt(n) (n: 양의 정수) 을 중심으로 '연속된 정수 5개의 제곱근' 보기를 값에서 유도한다.

    n 이 정수가 아니면(문제가 성립하지 않으면) 예외를 던진다.
    정답이 보기 중 몇 번째(1~5)에 오는지는 n 자체의 잔여값(n-3 mod 5)으로 정해져,
    n(=A,t0 에 의해 결정)이 바뀌면 정답 위치도 함께 바뀐다.
    원문제(n=7)에서는 이 규칙이 정확히 '정답이 다섯 번째'가 되도록 맞춰져 있다.
    """
    v = value(prm)
    n = sp.simplify(v ** 2)
    n = sp.nsimplify(n)
    if not n.is_integer or n <= 0:
        raise ValueError(f'보기를 구성할 수 없는 값: n={n}')
    n = int(n)
    r = (n - 3) % 5          # 정답이 놓일 자리(0~4, 아래에서부터)
    if n - r <= 0:
        raise ValueError(f'보기 하한이 0 이하가 됨: n={n}, r={r}')
    offsets = list(range(-r, 5 - r))
    vals = sorted((sp.sqrt(n + o) for o in offsets), key=lambda z: sp.N(z))
    return vals


def solve(prm):
    """조건 → 보기 번호(1~5)."""
    v = value(prm)
    ch = choices(prm)
    for i, c in enumerate(ch, start=1):
        if sp.simplify(c - v) == 0:
            return i
    raise ValueError('구한 값이 보기 목록에 없음')


CANDIDATE = 5

# 원문제 보기(①~⑤) 재현 확인: sqrt(3), 2, sqrt(5), sqrt(6), sqrt(7)
assert choices(PARAMS) == [sp.sqrt(3), 2, sp.sqrt(5), sp.sqrt(6), sp.sqrt(7)], choices(PARAMS)


def statement(prm):
    A, b, t0, C = prm['A'], prm['b'], prm['t0'], prm['C']
    bt = 't' if b == 1 else f'{b}t'
    return (
        f"좌표평면 위를 움직이는 점 P의 시각 t에서의 위치 (x, y)가\n"
        f"        x = {A}t + \\sin({bt}),   y = {C} - \\cos({bt})\n"
        f"이다. 시각 t = {sp.latex(t0)} 에서 점 P의 속력은?"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
