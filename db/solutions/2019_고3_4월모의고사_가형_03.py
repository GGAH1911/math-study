import sympy as sp

# ---- 문제의 수학 구조 ----
# 타원 표준형: x^2/a_squared + y^2/b_squared = 1
#   - a_squared, b_squared 중 더 큰 쪽이 (반)장축 방향을 결정한다.
#   - 장축의 길이 = 2 * sqrt(max(a_squared, b_squared))
# 보기(선택지)는 공차 choice_step, 첫 항 choice_start인 등차수열 n_choices개로 제시된다.
#   원문제: x^2/16 + y^2/7 = 1  ->  장축 길이 = 2*sqrt(16) = 8
#   보기: ①4 ②6 ③8 ④10 ⑤12  (start=4, step=2) 중 8은 ③번째 -> 정답 3

CANDIDATE = 3  # ★원문제의 정답: 보기 번호 ③ (값 8이 세 번째 보기)

PARAMS = dict(
    a_squared=16,    # x^2 항의 분모 (a^2)
    b_squared=7,     # y^2 항의 분모 (b^2)
    choice_start=4,  # 첫 번째 보기 값
    choice_step=2,   # 보기 간 공차
    n_choices=5,     # 보기 개수
)


def value(prm):
    """타원 x^2/A + y^2/B = 1 의 장축의 길이(수학적 답)를 sympy로 구한다."""
    A = sp.Integer(prm['a_squared'])
    B = sp.Integer(prm['b_squared'])
    if A <= 0 or B <= 0:
        raise ValueError("a^2, b^2 은 양수여야 타원이 정의됩니다.")
    if A == B:
        raise ValueError("a^2 = b^2 이면 원이 되어 장축이 정의되지 않습니다.")
    semi_major_sq = sp.Max(A, B)          # 더 큰 분모가 (반)장축의 제곱
    semi_major = sp.sqrt(semi_major_sq)
    if not semi_major.is_integer:
        raise ValueError("반장축 길이가 정수가 아니어서(무리수) 정수형 보기를 구성할 수 없습니다.")
    return 2 * semi_major                 # 장축의 길이 = 2 * 반장축


def choices(prm):
    """수학적 답(value)에서 유도되는 것이 아니라, 문제의 보기 형식(등차수열)을 그대로 생성.
    실제 값이 이 목록 안에 있는지는 solve에서 검증한다."""
    start = sp.Integer(prm['choice_start'])
    step = sp.Integer(prm['choice_step'])
    n = prm['n_choices']
    return [start + i * step for i in range(n)]


def solve(prm):
    v = value(prm)
    opts = choices(prm)
    if v not in opts:
        raise ValueError(f"정답 {v} 이(가) 보기 {opts} 안에 없어 문제가 성립하지 않습니다.")
    return opts.index(v) + 1  # 보기 번호 (1-based, ①=1)


def statement(prm):
    A, B = prm['a_squared'], prm['b_squared']
    opts = choices(prm)
    circled = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧']
    opt_str = ' '.join(f"{circled[i]} {o}" for i, o in enumerate(opts))
    return f"타원 x^2/{A} + y^2/{B} = 1의 장축의 길이는? {opt_str}"


# 보기 목록이 원문제의 보기(4,6,8,10,12)와 일치하는지 고정
assert choices(PARAMS) == [4, 6, 8, 10, 12]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
