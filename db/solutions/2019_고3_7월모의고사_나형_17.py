import sympy as sp

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 공차가 자연수인 등차수열 {a_n} 과 공비가 자연수인 등비수열 {b_n} 이
# 인덱스 p 에서 같은 값 C 를 갖는다(a_p = b_p = C).
#   a_1 = C - (p-1)d,  b_1 = C / r^(p-1)
# 조건 (가) a_{p+gap1} = b_{p+gap1} 을 풀면
#   C + gap1*d = C*r^gap1  =>  d = C*(r^gap1 - 1) / gap1
# 조건 (나) L < a_{p+gap2} < U (a_{p+gap2} = C + gap2*d) 를 만족하는
# 자연수 r 이 유일하게 정해지고, 그때
#   a_{p+gap1} + b_{p+gap1+1} = C*r^gap1 + C*r^(gap1+1) = C*r^gap1*(1+r)
# 이 실제 정답 값이며, 이 값이 보기(선택지) 중 몇 번째인지가 최종 정답이다.
# 원문제는 p=6, C=9, gap1=1(조건 가: a7=b7), gap2=5(조건 나: a11),
# L=94, U=109 인 경우로, r=3, d=18 이 유일해이고 값은 9*3*4=108(⑤번).
#
# ★답을 바꾸는 파라미터는 C(공통값), L,U(부등식 범위) 등이지만, 이들은
#   "조건 (가)(나)를 만족하는 자연수 r 이 유일하게 존재해야 한다"는 정수해
#   조건으로 서로 묶여 있다(예: C 만 바꾸면 L,U 범위 밖으로 r 후보가 사라지거나
#   여러 개가 남아 문제가 깨진다). 따라서 규칙 5 에 따라 실제로 성립하는
#   (C, L, U) 조합을 VARIANTS 로 여러 개 제시해 답이 실제로 달라짐을 증명한다.

CANDIDATE = 5  # ★원문제 정답 (⑤ 108 → 선택지 번호 5)

PARAMS = dict(
    p=6,       # 두 수열이 같은 값 C 를 갖는 인덱스 (a_p = b_p = C)
    C=9,       # a_p = b_p = C
    gap1=1,    # 조건 (가): a_{p+gap1} = b_{p+gap1}  (원문제: a_7 = b_7)
    gap2=5,    # 조건 (나)가 적용되는 인덱스 오프셋 a_{p+gap2}  (원문제: a_11)
    L=94,      # 조건 (나) 하한
    U=109,     # 조건 (나) 상한
    R_MAX=60,  # 자연수 r 탐색 상한 (닫힌식 대신 유한 탐색; 40초 제한 내 충분히 작음)
)

# 원문제의 고정 보기(선택지): 96,99,102,105,108 (공차 3인 등차수열, 정답이 마지막 항)
CHOICES_WINDOW = (96, 99, 102, 105, 108)


def _find_r(prm):
    """조건 (가)(나)를 모두 만족하는 자연수 r(과 그때의 자연수 공차 d)을 찾는다.
    유일해가 아니면(문제로 성립하지 않으면) 예외를 던진다."""
    p, C, gap1, gap2, L, U, R_MAX = (
        prm['p'], prm['C'], prm['gap1'], prm['gap2'], prm['L'], prm['U'], prm['R_MAX'])
    sols = []
    for r in range(1, R_MAX + 1):
        # 조건 (가) a_{p+gap1}=b_{p+gap1} 을 풀면 d = C*(r^gap1 - 1)/gap1
        d = sp.Rational(C, gap1) * (r ** gap1 - 1)
        if not d.is_integer or d <= 0:
            continue  # 공차 d는 자연수(양의 정수)여야 함
        a_tail = C + gap2 * d  # a_{p+gap2}
        if L < a_tail < U:     # 조건 (나)
            sols.append((r, sp.Integer(d)))
    if len(sols) != 1:
        raise ValueError(f'조건을 만족하는 자연수 r 이 유일하지 않음(해 {len(sols)}개): {sols}')
    return sols[0]


def value(prm):
    """a_{p+gap1} + b_{p+gap1+1} 을 sympy 로 실제 계산."""
    r, d = _find_r(prm)
    C, gap1 = prm['C'], prm['gap1']
    a_val = C + gap1 * d          # a_{p+gap1} (조건 (가)에 의해 b_{p+gap1} 과 같은 값)
    b_val = C * r ** (gap1 + 1)   # b_{p+gap1+1} = b_p * r^(gap1+1)
    return sp.nsimplify(a_val + b_val)


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기: 96부터 3씩 커지는 5개 정수."""
    return CHOICES_WINDOW


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        # 값이 고정 보기 범위를 벗어나면 이 문제 유형으로 성립하지 않음
        raise ValueError(f'값 {v}이(가) 보기 {ch}를 벗어남 — 문제로 성립하지 않음')
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    p, C, gap1, gap2, L, U = (prm['p'], prm['C'], prm['gap1'], prm['gap2'], prm['L'], prm['U'])
    return (
        f"공차가 자연수인 등차수열 {{a_n}}과 공비가 자연수인 등비수열 {{b_n}}이 "
        f"a_{p}=b_{p}={C} 이고, 다음 조건을 만족시킨다.\n"
        f"(가) a_{p+gap1}=b_{p+gap1}\n"
        f"(나) {L}<a_{p+gap2}<{U}\n"
        f"a_{p+gap1}+b_{p+gap1+1}의 값은?\n"
        f"① {CHOICES_WINDOW[0]} ② {CHOICES_WINDOW[1]} ③ {CHOICES_WINDOW[2]} "
        f"④ {CHOICES_WINDOW[3]} ⑤ {CHOICES_WINDOW[4]}"
    )


# 원문제 보기가 정확히 ①96 ②99 ③102 ④105 ⑤108 인지 고정 검증
assert choices(PARAMS) == (96, 99, 102, 105, 108)

# 조건 (가)(나)를 만족하는 자연수 r 이 유일하게 존재하도록 (C, L, U) 를 묶어
# 실제로 성립하는 조합들. 서로 다른 조합이 서로 다른 보기 번호를 정답으로 만든다.
VARIANTS = [
    dict(C=16),                # r=2, d=16 → 값 96  → 보기 ①
    dict(C=17),                # r=2, d=17 → 값 102 → 보기 ③
    dict(C=8, L=50, U=100),    # r=3, d=8  → 값 96  → 보기 ①
]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
