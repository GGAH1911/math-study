from sympy import Matrix

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 두 벡터 a=(a1,a2), b=(b1,b2) 에 대해 k*a - l*b 의 모든 성분의 합을 구하는 문제.
# 답을 바꾸는 파라미터: a1,a2,b1,b2 (벡터 성분), k,l (선형결합 계수) — 모두
# value(prm) = k*(a1+a2) - l*(b1+b2) 계산에 실제로 쓰인다.
#
# 이 문제 유형(간단한 벡터 선형결합의 성분 합)은 보기가 항상 "1부터 5까지의
# 연속한 정수"로 고정되어 나오는 특수한 형태다(①1 ②2 ③3 ④4 ⑤5). 즉 보기 자체가
# 값을 따라 움직이는 창(window)이 아니라, 문제 유형이 강제하는 고정된 정수 범위다.
# 따라서 파라미터를 바꿔 계산된 값이 1~5 범위를 벗어나면 더 이상 "이 유형"의
# 문제로 성립하지 않으므로 예외를 던진다(규칙 6).

CANDIDATE = 3  # ★원문제 정답 (③)

PARAMS = dict(
    a1=1, a2=2,   # 벡터 a = (1, 2)
    b1=-2, b2=5,  # 벡터 b = (-2, 5)
    k=2, l=1,     # k*a - l*b
)


def value(prm):
    """k*a - l*b 의 모든 성분의 합을 sympy 로 실제 계산."""
    a = Matrix([prm['a1'], prm['a2']])
    b = Matrix([prm['b1'], prm['b2']])
    result = prm['k'] * a - prm['l'] * b
    return sum(result)


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기: 1부터 5까지의 연속 정수."""
    return (1, 2, 3, 4, 5)


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        # 값이 1~5 범위를 벗어나면 이 문제 유형으로 성립하지 않음
        raise ValueError(f"값 {v}이(가) 보기 범위 {ch}를 벗어남 — 문제로 성립하지 않음")
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    return (
        f"두 벡터 \\vec{{a}}=({prm['a1']}, {prm['a2']}), "
        f"\\vec{{b}}=({prm['b1']}, {prm['b2']})에 대하여 "
        f"벡터 {prm['k']}\\vec{{a}}{'+' if prm['l'] < 0 else '-'}"
        f"{abs(prm['l'])}\\vec{{b}}의 모든 성분의 합은?"
    )


# 원문제 보기가 정확히 ①1 ②2 ③3 ④4 ⑤5 인지 고정 검증
assert choices(PARAMS) == (1, 2, 3, 4, 5)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
