import sympy as sp

# ============================================================
# 원문제 (2019 고3 3월 모의고사 나형 17번, 정답 5)
#   자연수 k에 대하여 f(x) = | k/(2x) - 2 |  (x>0)
#   A: f(x)=0 인 점, P: 곡선 위의 점, Q: P에서 x축에 내린 수선의 발
#   <보기>
#     ㄱ. A = (k/4, 0) 이다.
#     ㄴ. P의 x좌표가 A의 x좌표보다 클 때, 선분 PQ의 길이는 2보다 작다.
#     ㄷ. P의 x좌표가 k일 때, 삼각형 AQP의 넓이가 자연수가 되도록 하는
#        k의 최솟값은 16이다.
#   ① ㄱ  ② ㄱㄴ  ③ ㄱㄷ  ④ ㄴㄷ  ⑤ ㄱㄴㄷ
#
# 수학 구조 분석
#   f(x) = | k/(a x) - b |  로 일반화하면 (원문제는 a=2, b=2)
#     - A = (k/(ab), 0)                       (ㄱ이 주장하는 좌표 공식)
#     - x > k/(ab) 에서 f(x) = b - k/(a x) 는 0에서 b로 단조 증가(수렴 X)
#       => sup PQ = b, 항상 PQ < b                (ㄴ이 주장하는 상계값)
#     - P의 x좌표를 m*k 라 하면 (원문제는 m=1)
#         f(P) = | 1/(a m) - b |  (k에 무관한 상수)
#         base = |m k - k/(ab)| = k*|m - 1/(ab)|
#         area = (1/2)*base*height = C*k   (C는 a,b,m 으로 정해지는 유리수 상수)
#         area가 자연수가 되는 최소 자연수 k = (C를 기약분수 p/q로 쓸 때의 q)
#       (ㄷ이 주장하는 최솟값)
#   즉 ㄱ,ㄴ,ㄷ 각각은 "실제로 계산된 값"과 "보기 문장이 주장하는 값"이
#   일치하는지를 따지는 참/거짓 명제이고, 정답은 참인 명제들의 조합이
#   보기 ①~⑤ 중 어느 것과 일치하는지로 결정된다.
# ============================================================

CANDIDATE = 5  # ★원문제 정답 (선지 번호) — 절대 바꾸지 않음

PARAMS = dict(
    a=sp.Integer(2),                 # f(x) = |k/(a x) - b| 의 분모 계수
    b=sp.Integer(2),                 # f(x) = |k/(a x) - b| 의 상수항
    m=sp.Integer(1),                 # P의 x좌표 = m*k
    claim_A_coef=sp.Rational(1, 4),  # ㄱ이 주장하는 A_x = claim_A_coef * k
    claim_bound=sp.Integer(2),       # ㄴ이 주장하는 PQ의 상계값
    claim_min_k=sp.Integer(16),      # ㄷ이 주장하는, 넓이를 자연수로 만드는 최소 k
)

# 원문제 보기 구성과 동일한 5개 선지 (참인 명제 조합)
CHOICE_LIST = [
    frozenset({'ㄱ'}),
    frozenset({'ㄱ', 'ㄴ'}),
    frozenset({'ㄱ', 'ㄷ'}),
    frozenset({'ㄴ', 'ㄷ'}),
    frozenset({'ㄱ', 'ㄴ', 'ㄷ'}),
]
assert CHOICE_LIST == [
    frozenset({'ㄱ'}), frozenset({'ㄱ', 'ㄴ'}), frozenset({'ㄱ', 'ㄷ'}),
    frozenset({'ㄴ', 'ㄷ'}), frozenset({'ㄱ', 'ㄴ', 'ㄷ'}),
], '원문제 보기 구성과 달라짐'


def value(prm):
    """ㄱ, ㄴ, ㄷ 각각의 참/거짓을 sympy로 실제 계산하여, 참인 명제 라벨 집합을 반환."""
    a, b, m = sp.nsimplify(prm['a']), sp.nsimplify(prm['b']), sp.nsimplify(prm['m'])
    if a <= 0 or b <= 0 or m <= 0:
        raise ValueError('a, b, m 은 모두 양수여야 함')

    k = sp.symbols('k', positive=True)

    # ---- ㄱ: A의 x좌표 공식 ----
    x_A = k / (a * b)                       # f(x)=0 <=> k/(a x)=b <=> x=k/(ab)
    actual_A_coef = sp.nsimplify(sp.simplify(x_A / k))
    stmt_1 = (actual_A_coef == sp.nsimplify(prm['claim_A_coef']))

    # ---- ㄴ: x > x_A 구간에서 f(x) = b - k/(a x) 는 (0, b)에서 단조증가, sup=b ----
    x = sp.symbols('x', positive=True)
    f_expr = b - k / (a * x)                # x > x_A 구간에서의 f(x) (증가함수)
    # 단조 증가성 확인 (도함수 > 0)
    deriv = sp.diff(f_expr, x)
    if not sp.simplify(deriv) > 0:
        raise ValueError('x > x_A 구간에서 f(x)가 증가함수가 아님 (구조 가정 위반)')
    actual_bound = b                        # x -> 무한대 극한값 (도달하지 않는 상한)
    stmt_2 = bool(sp.nsimplify(prm['claim_bound']) >= actual_bound)

    # ---- ㄷ: P의 x좌표 = m*k 일 때 삼각형 AQP의 넓이 = C*k, 자연수 되는 최소 k ----
    height = sp.Abs(1 / (a * m) - b)        # f(mk) = |k/(a*m*k) - b| = |1/(am) - b|
    base_coef = sp.Abs(m - 1 / (a * b))     # |m*k - k/(ab)| = k * base_coef
    C = sp.nsimplify(sp.Rational(1, 2) * base_coef * height)
    if C == 0:
        raise ValueError('넓이가 항상 0이 되어 최솟값 조건이 성립하지 않음')
    p, q = sp.fraction(sp.nsimplify(C))     # 기약분수 p/q
    if p <= 0 or q <= 0:
        raise ValueError('넓이 계수가 올바른 양의 유리수가 아님')
    minimal_k = q                           # area = C*k 가 자연수가 되는 최소 자연수 k
    stmt_3 = (minimal_k == sp.nsimplify(prm['claim_min_k']))

    labels = set()
    if stmt_1:
        labels.add('ㄱ')
    if stmt_2:
        labels.add('ㄴ')
    if stmt_3:
        labels.add('ㄷ')
    return frozenset(labels)


def choices(prm):
    """원문제와 동일한 5개 선지 (참인 명제 조합 목록). 값 자체(어떤 조합이 참인지)에서
    유도되는 것이 아니라 이 유형(<보기> 참/거짓 선택형) 고유의 고정 선지 구성이며,
    원문제 보기와 동일함을 위의 assert로 고정해 두었다."""
    return CHOICE_LIST


def solve(prm):
    v = value(prm)
    if v not in choices(prm):
        raise ValueError(f'참인 명제 조합 {v} 는 주어진 선지에 존재하지 않음')
    return choices(prm).index(v) + 1  # 1-based 선지 번호


def statement(prm):
    a, b, m = prm['a'], prm['b'], prm['m']
    ca, cbnd, cmin = prm['claim_A_coef'], prm['claim_bound'], prm['claim_min_k']
    return (
        f"자연수 k에 대하여 함수 f(x) = | k/({a}x) - {b} | (x>0) 의 그래프와 "
        f"x축의 교점을 A, 곡선 y=f(x) 위의 점 P에서 x축에 내린 수선의 발을 Q라 하자. "
        f"<보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
        f"<보기>\n"
        f"ㄱ. 점 A의 좌표는 ({sp.nsimplify(ca)}*k, 0) 이다.\n"
        f"ㄴ. 점 P의 x좌표가 점 A의 x좌표보다 클 때, 선분 PQ의 길이는 {cbnd}보다 작다.\n"
        f"ㄷ. 점 P의 x좌표가 {m}*k일 때, 삼각형 AQP의 넓이가 자연수가 되도록 하는 "
        f"k의 최솟값은 {cmin}이다.\n"
        f"① ㄱ  ② ㄱ, ㄴ  ③ ㄱ, ㄷ  ④ ㄴ, ㄷ  ⑤ ㄱ, ㄴ, ㄷ"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
