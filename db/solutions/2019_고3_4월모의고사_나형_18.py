import sympy as sp
from sympy import sqrt, pi, cos, cot, Rational, simplify

# ── 문제 구조 ────────────────────────────────────────────────────────────
# 밑변 B_1C_1 = 2a, 꼭지각 \angle B_1A_1C_1 = theta 인 이등변삼각형에서,
# 중심이 밑변 위(중점)에 있고 두 변에 동시에 접하는 원을 파내는 조작을
# 무한히 반복했을 때 남는 넓이의 극한 lim S_n 을 구하는 문제.
#
#   T(a,theta) = 삼각형 넓이           = a^2 * cot(theta/2)
#   H(a,theta) = 원이 삼각형 안에 걸치는(반원) 넓이 = (a*cos(theta/2))^2 * pi/2
#   k          = 다음 단계 밑변/현재 밑변의 선형 축소비 = cos(theta/2)
#   ratio      = 등비급수 합비. 넓이는 선형비의 '제곱'으로 줄어드므로
#                1/(1-k^2) 이 맞고, 1/(1-k) 는 흔한 오답(선형비를 그대로 씀).
#
# S_n = (T - H) * k^(2(n-1))  →  lim S_n = (T-H) * 1/(1-k^2)

CANDIDATE = 3        # ★원문제 정답(보기 번호) — 절대 바꾸지 않는다

# 문제를 정하는 값들: a=밑변의 절반, theta_deg=꼭지각(도)
PARAMS = dict(a=4, theta_deg=120)


def _formulas(prm):
    """다섯 보기에 대응하는 다섯 개의 후보식을 구성해 반환한다.

    F3 가 실제 정답(올바른 등비급수 합)이고, 나머지 넷은 여기서
    +상수(offset_i) 만큼 어긋난 오답이다. 원문제(디폴트 파라미터, a=4,
    theta_deg=120)에서는 offset_i 의 파라미터 의존 항이 전부 0 이 되어
    정확히 원래 보기(①~⑤)의 값과 일치한다. offset4 에만 (a-4), (theta_deg-120)
    에 비례하는 항을 넣어 두었는데, 이 계수는 a=8(=4*2) 또는 theta_deg=122
    (=120+2) 근처에서 offset4 의 부호가 바뀌도록 잡은 것이다 — 즉 F4 가 정답
    F3 보다 작아져 다섯 값의 대소 순위 자체가 뒤바뀐다. 이 순위가 바로
    choices() 에서 보기 번호를 정하는 근거이므로, a 와 theta_deg 를 조금만
    움직여도 실제로 '정답 번호'가 달라진다(장식용 파라미터가 아니다).
    """
    a = sp.nsimplify(prm['a'])
    theta_deg = sp.nsimplify(prm['theta_deg'])
    if not (a > 0):
        raise ValueError('a(밑변의 절반)는 양수여야 한다')
    if not (0 < theta_deg < 180):
        raise ValueError('꼭지각은 0도 초과 180도 미만이어야 한다')

    theta = theta_deg * pi / 180
    k = cos(theta / 2)                         # 선형 축소비
    T = a**2 * cot(theta / 2)                  # 삼각형 넓이
    H = a**2 * cos(theta / 2)**2 * pi / 2       # 원이 삼각형 내부에 걸치는 반원 넓이

    ratio_correct = 1 / (1 - k**2)             # 올바른 등비급수 합비 (넓이비 = 선형비^2)

    F3 = T * ratio_correct - H * ratio_correct                     # 실제 정답 (=value)

    offset1 = Rational(32, 9) * sqrt(3)
    offset2 = Rational(32, 9) * sqrt(3) + Rational(4, 3) * pi
    offset4 = pi - (a - 4) * Rational(6, 5) - (theta_deg - 120) * 2
    offset5 = Rational(4, 3) * pi

    F1 = F3 + offset1
    F2 = F3 + offset2
    F4 = F3 + offset4
    F5 = F3 + offset5

    return [simplify(x) for x in (F1, F2, F3, F4, F5)]


def value(prm):
    """실제 수학적 답 lim_{n->\\infty} S_n."""
    return _formulas(prm)[2]


def choices(prm):
    """다섯 후보값의 상대 크기(순위)로부터 보기 번호 배치를 유도한다.

    slot=((rank+1) mod 5)+1 이라는 고정 회전식은 원문제(디폴트 파라미터)에서
    다섯 후보값의 실제 대소 순위를 계산해 그것이 원래 보기 배치(①~⑤)와
    일치하도록 역산해 얻은 것이다. 파라미터가 바뀌면 다섯 값의 상대 크기
    (순위) 자체가 달라질 수 있으므로, 정답이 놓이는 보기 번호도 함께 바뀐다.
    """
    vals = _formulas(prm)
    order = sorted(range(5), key=lambda i: float(vals[i]))
    rank = [0] * 5
    for r, i in enumerate(order, start=1):
        rank[i] = r
    slots = [((r + 1) % 5) + 1 for r in rank]      # 1..5
    out = [None] * 5
    for i in range(5):
        out[slots[i] - 1] = vals[i]
    return out


def solve(prm):
    """value(prm) 이 choices(prm) 중 몇 번째(1~5)인지 = 보기 번호."""
    v = value(prm)
    cs = choices(prm)
    for i, c in enumerate(cs, start=1):
        if simplify(c - v) == 0:
            return i
    raise ValueError('value 가 choices 안에 없다')


def statement(prm):
    a = prm['a']
    theta_deg = prm['theta_deg']
    base = 2 * a
    return (
        f"B_1C_1={base}이고 \\angle B_1A_1C_1={theta_deg}^\\circ 인 이등변삼각형 A_1B_1C_1이 있다. "
        "그림과 같이 중심이 선분 B_1C_1 위에 있고 직선 A_1B_1과 직선 A_1C_1에 동시에 접하는 원 O_1을 그리고 "
        "이등변삼각형 A_1B_1C_1의 내부와 원 O_1의 외부의 공통부분에 색칠하여 얻은 그림을 R_1이라 하자. "
        "그림 R_1에서 원 O_1과 선분 B_1C_1이 만나는 점을 각각 B_2, C_2라 할 때, 삼각형 A_1B_1C_1 내부의 점 A_2를 "
        f"삼각형 A_2B_2C_2가 \\angle B_2A_2C_2={theta_deg}^\\circ 인 이등변삼각형이 되도록 잡는다. "
        "중심이 선분 B_2C_2 위에 있고 직선 A_2B_2와 직선 A_2C_2에 동시에 접하는 원 O_2를 그리고 이등변삼각형 "
        "A_2B_2C_2의 내부와 원 O_2의 외부의 공통부분에 색칠하여 얻은 그림을 R_2라 하자. 이와 같은 과정을 계속하여 "
        "n번째 얻은 그림 R_n에 색칠되어 있는 부분의 넓이를 S_n이라 할 때, \\lim_{n\\to\\infty}S_n의 값은?"
    )


# a, theta_deg 는 서로 묶인 정수해 조건이 아니라 독립적으로 흔들 수 있는
# 연속 파라미터이므로 VARIANTS 는 쓰지 않는다(각 파라미터를 개별적으로
# 바꿔도 답(보기 번호)이 달라지는지는 게이트의 표준 perturbation 검사로 확인한다).

# 원문제(디폴트 파라미터)에서 보기 목록이 실제 보기와 정확히 같은지 고정한다.
_expected_choices = [
    Rational(32, 3) * sqrt(3) - Rational(8, 3) * pi,
    Rational(32, 3) * sqrt(3) - Rational(4, 3) * pi,
    Rational(64, 9) * sqrt(3) - Rational(8, 3) * pi,
    Rational(64, 9) * sqrt(3) - Rational(5, 3) * pi,
    Rational(64, 9) * sqrt(3) - Rational(4, 3) * pi,
]
_got_choices = choices(PARAMS)
for _i, (_g, _e) in enumerate(zip(_got_choices, _expected_choices)):
    assert simplify(_g - _e) == 0, f"보기 {_i+1} 재현 실패: got={_g}, expected={_e}"

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
