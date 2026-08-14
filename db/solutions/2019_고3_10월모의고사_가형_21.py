"""2019 고3 10월모의고사 가형 21번 — 파라미터화 솔버.

곡선 y=(x-n)e^{c x} (c는 지수의 계수, 원문제는 c=1 즉 e^x) 위에서, 점 (a,0)으로부터
그은 접선의 접점 t는  0-(t-n)e^{ct} = ((t-n)c+1) e^{ct} (a-t)  를 만족한다.
양변을 e^{ct}(≠0)로 나누면 t에 대한 이차식이 되고, 그 판별식

    D = c(a-n)(c(a-n)+4)

의 부호로 접선 개수 f(a,n) (2/1/0)이 정해진다. 이 판별식은 diff/expand/Poly.discriminant를
통해 sympy로 직접 유도한다(원문제는 c=1인 경우로 D=(a-n)(a-n+4)와 일치).

파라미터로 뽑은 수학 구조:
  - c        : 지수 e^{cx}의 계수. 판별식의 '+4' 항이 '+4/c'로 스케일되어, 그 값이 정수인지
               여부에 따라 <보기> ㄴ(항상 거짓이라는 주장)의 진위가 바뀐다.
  - a1, n1   : <보기> ㄱ이 검사하는 "a=a1일 때 f(n1)=1이다"의 (a1, n1).
  - L, U, S  : <보기> ㄷ의 조건 "sum_{n=L}^{U} f(n) = S".
  - da_claim : <보기> ㄷ이 그 조건을 만족한다고 주장하는 정수 a들의 집합.
  - a_search : 정수 a를 탐색하는 반경(문제의 '모든 정수 a'를 유한 구간으로 근사).
"""
import sympy as sp

CANDIDATE = 3  # 원문제 정답 ③ (ㄱ, ㄷ)

PARAMS = dict(
    c=1,                    # e^{c x}의 계수. 원문제는 c=1 (곡선 y=(x-n)e^x)
    a1=0, n1=4,              # ㄱ: "a=a1일 때 f(n1)=1이다"
    L=1, U=5, S=5,            # ㄷ: "sum_{n=L}^{U} f(n) = S"
    da_claim=(-1, 3),         # ㄷ이 주장하는 그 a들의 집합
    a_search=60,              # 정수 a 탐색 반경
)


def _discriminant_expr():
    """점(a,0)에서 y=(x-n)e^{cx}에 그은 접선의 접점 방정식을 세우고 판별식을 유도한다."""
    t, a, n, c = sp.symbols('t a n c')
    f_t = (t - n) * sp.exp(c * t)
    fp_t = sp.diff(f_t, t)
    eq = sp.expand((0 - (f_t + fp_t * (a - t))) / sp.exp(c * t))  # e^{ct}로 나눠 다항식화
    poly = sp.Poly(eq, t)
    return sp.factor(poly.discriminant())  # c*(a-n)*(c*(a-n)+4) 형태


_A, _N, _C = sp.symbols('a n c')
_DISC = _discriminant_expr()


def _f_count(a, n, c):
    """점 (a,0)에서 곡선 y=(x-n)e^{cx}에 그은 접선의 개수 f(a,n)."""
    val = sp.nsimplify(_DISC.subs({_A: a, _N: n, _C: c}))
    if val > 0:
        return 2
    elif val == 0:
        return 1
    else:
        return 0


def solve(prm):
    c = sp.Rational(prm['c'])
    if c == 0:
        raise ValueError("c=0이면 곡선이 e^{0}=1이 되어 문제가 성립하지 않습니다.")
    shift = sp.Rational(4, c)  # 판별식의 이론적 폭 → 탐색창 크기 산정에 사용
    win = int(sp.ceiling(sp.Abs(shift))) + 5

    def f(a, n):
        return _f_count(a, n, c)

    # ㄱ: a=a1일 때 f(n1)=1 인가
    g = f(prm['a1'], prm['n1']) == 1

    # ㄴ: f(n)=1인 정수 n의 개수가 1인 정수 a가 존재하는가 (전칭 명제를 유한 구간에서 확인)
    def count_eq1(a):
        return sum(1 for n in range(a - win, a + win + 1) if f(a, n) == 1)
    nu = any(count_eq1(a) == 1 for a in range(-prm['a_search'], prm['a_search'] + 1))

    # ㄷ: sum_{n=L}^{U} f(a,n) = S 를 만족하는 정수 a의 집합이 da_claim과 일치하는가
    def total(a):
        return sum(f(a, n) for n in range(prm['L'], prm['U'] + 1))
    da_set = set(a for a in range(-prm['a_search'], prm['a_search'] + 1) if total(a) == prm['S'])
    da = da_set == set(prm['da_claim'])

    # 실제 수능 보기 형식(①~⑤)에 등장하는 5개 조합만 유효한 문제로 인정
    choice = {
        (1, 0, 0): 1,  # ① ㄱ
        (1, 1, 0): 2,  # ② ㄱ,ㄴ
        (1, 0, 1): 3,  # ③ ㄱ,ㄷ
        (0, 1, 1): 4,  # ④ ㄴ,ㄷ
        (1, 1, 1): 5,  # ⑤ ㄱ,ㄴ,ㄷ
    }
    key = (int(g), int(nu), int(da))
    if key not in choice:
        raise ValueError(
            f"이 파라미터 조합의 진리값 {key}(ㄱ,ㄴ,ㄷ)은 보기 ①~⑤ 어디에도 해당하지 않아 "
            "문제로 성립하지 않습니다."
        )
    return choice[key]


# c(=지수 계수)는 a1,n1과 묶여 있어야 유효한 문제가 된다(ㄱ이 성립하려면 D(a1,n1,c)=0이어야 함).
# 아래 VARIANTS는 서로 다른 파라미터를 흔들어 CANDIDATE(3)와 다른 답을 내는 예시들이다.
VARIANTS = [
    dict(PARAMS, da_claim=(0, 3)),                     # ㄷ의 주장(a값 집합)만 바꿔 거짓으로 만듦 → ①
    dict(PARAMS, c=3, a1=0, n1=0),                      # 곡선을 y=(x-n)e^{3x}로 일반화 → ②
]


def statement(prm):
    c = prm['c']
    curve = "y=(x-n)e^x" if sp.Rational(c) == 1 else f"y=(x-n)e^{{{c}x}}"
    claim = ' 또는 '.join(str(x) for x in prm['da_claim'])
    return (
        f"정수 n에 대하여 점 (a, 0)에서 곡선 {curve}에 그은 접선의 개수를 f(n)이라 하자. "
        "<보기>에서 옳은 것만을 있는 대로 고른 것은?\n"
        f"ㄱ. a={prm['a1']}일 때, f({prm['n1']})=1이다.\n"
        "ㄴ. f(n)=1인 정수 n의 개수가 1인 정수 a가 존재한다.\n"
        f"ㄷ. sum_{{n={prm['L']}}}^{{{prm['U']}}} f(n)={prm['S']}를 만족시키는 정수 a의 값은 "
        f"{claim}이다.\n"
        "① ㄱ ② ㄱ,ㄴ ③ ㄱ,ㄷ ④ ㄴ,ㄷ ⑤ ㄱ,ㄴ,ㄷ"
    )


assert solve(VARIANTS[0]) != CANDIDATE, "da_claim을 바꿔도 답이 그대로면 파라미터가 죽은 것"
assert solve(VARIANTS[1]) != CANDIDATE, "c(지수 계수)를 바꿔도 답이 그대로면 파라미터가 죽은 것"
assert solve(VARIANTS[0]) != solve(VARIANTS[1]), "두 변형이 같은 답을 내면 서로 다른 문제임을 못 보임"

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
