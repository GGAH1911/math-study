from sympy import symbols, series

CANDIDATE = 1  # ★원문제 정답 = 보기 ①

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# "같은 종류의 상자 k개에 같은 종류의 공 n개를 남김없이 나누어 담을 때,
#  빈 상자가 없도록 담는 경우의 수"는 n을 정확히 k개의 양의 정수로
# 분할(partition)하는 방법의 수 p(n, k)와 같다.
#   생성함수: p(n,k) = [x^n] x^k / ((1-x)(1-x^2)...(1-x^k))
# 이 계수를 sympy series로 실제로 추출해서 계산한다(하드코딩 아님).
#
# 답을 바꾸는 파라미터: total(공의 개수 n), boxes(상자의 개수 k).
# 다만 이 특정 원문제(n=8,k=3)는 p(n,k)가 k=3 근방에서 국소 최댓값(peak)이라
# k 하나만 +1,+2,*2 식으로 흔들면 값이 보기 범위(5~9) 밖으로 나가거나 그대로다
# (n,k가 서로 얽혀 있어 "하나만 못 흔드는" 경우 — 규칙 5). 그래서 VARIANTS로
# n과 k를 함께 바꾼 성립하는 조합을 제시해 파라미터가 실제로 답을 바꾼다는
# 것을 보인다.

PARAMS = dict(
    total=8,   # 공의 개수 n
    boxes=3,   # 상자의 개수 k
)

# 보기는 "정답, 정답+1, 정답+2, 정답+3, 정답+4"의 연속한 다섯 정수로 고정 출제된
# 문제 유형이다(①5 ②6 ③7 ④8 ⑤9). 계산된 값이 이 범위를 벗어나면 이 유형의
# 문제로 성립하지 않으므로 예외를 던진다(규칙 6).
_FIXED_CHOICES = (5, 6, 7, 8, 9)

_x = symbols('x')


def value(prm):
    """n = prm['total']개의 공을 정확히 k = prm['boxes']개의 양의 정수로
    분할하는 방법의 수 p(n,k)를, 생성함수의 x^n 계수로 sympy가 실제로 계산."""
    n, k = prm['total'], prm['boxes']
    if k <= 0 or n < k:
        raise ValueError(f"n={n}개를 양수 k={k}개로 분할할 수 없음")
    gf = _x ** k
    denom = 1
    for i in range(1, k + 1):
        denom *= (1 - _x ** i)
    gf = gf / denom
    ser = series(gf, _x, 0, n + 1).removeO()
    return int(ser.coeff(_x, n))


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기(연속한 정수 5개)."""
    return _FIXED_CHOICES


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"값 {v}이(가) 보기 범위 {ch}를 벗어남 — 문제로 성립하지 않음")
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    return (
        f"같은 종류의 상자 {prm['boxes']}개에 같은 종류의 야구공 {prm['total']}개를 "
        f"남김없이 나누어 담을 때, 빈 상자가 없도록 담는 경우의 수는?"
    )


# n,k가 서로 얽혀 하나만 흔들면 깨지는 경우이므로 VARIANTS로 성립하는 조합을 제시.
# 아래 두 조합 모두 예외 없이 풀리고, 원문제(보기 ①)와 다른 답을 낸다.
VARIANTS = [
    dict(total=9),            # p(9,3) = 7 → 보기 ③
    dict(total=9, boxes=4),   # p(9,4) = 6 → 보기 ②
    dict(total=10),           # p(10,3) = 8 → 보기 ④
]

assert choices(PARAMS) == (5, 6, 7, 8, 9)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
