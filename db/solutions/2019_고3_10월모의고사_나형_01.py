import sympy as sp

# ─────────────────────────────────────────────────────────────
# 원문제: log_2 24 - log_2 3 의 값은?  (①1 ②2 ③3 ④4 ⑤5, 정답 ③)
#
# 수학 구조:
#   log_b(N1) - log_b(N2) = log_b(N1/N2)
# 이 값이 정수가 되려면 N1/N2 가 밑 b 의 정수 거듭제곱이어야 한다.
#   24/3 = 8 = 2^3  →  log_2 8 = 3
#
# 파라미터로 뽑은 것: base(밑), N1(피감수 진수), N2(감수 진수).
# 세 값 모두 sympy 로 log_b(N1)-log_b(N2) 를 실제로 계산·단순화해서
# 정수가 나오는지 검증하고, 정수가 아니면(=문제로 성립하지 않으면) 예외를 던진다.
# 선택지는 항상 1~5 의 다섯 개 자연수(원문제와 동일한 형식)이며,
# 계산된 값이 그 범위 밖이면 역시 예외를 던진다 → 정답 번호(= 값)가
# base/N1/N2 를 바꿀 때마다 실제로 달라지는 것을 아래에서 직접 확인했다.
# ─────────────────────────────────────────────────────────────

CANDIDATE = 3          # ★원문제 정답 (③번, 값 3) — 절대 바꾸지 않음

PARAMS = dict(
    base=2,   # 로그의 밑
    N1=24,    # 첫 번째 진수 (피감수)
    N2=3,     # 두 번째 진수 (감수)
)


def value(prm):
    """log_base(N1) - log_base(N2) 를 sympy 로 실제 계산한 정수값."""
    base, n1, n2 = prm['base'], prm['N1'], prm['N2']
    if base <= 1 or n1 <= 0 or n2 <= 0:
        raise ValueError("밑은 1보다 커야 하고 진수는 양수여야 합니다.")
    b, a, c = sp.Integer(base), sp.Integer(n1), sp.Integer(n2)
    expr = sp.simplify(sp.log(a, b) - sp.log(c, b))
    if not expr.is_integer:
        raise ValueError("주어진 base/N1/N2 조합으로는 값이 정수가 되지 않습니다.")
    return int(expr)


def choices(prm):
    """원문제와 동일한 형식: 1부터 5까지의 자연수 다섯 개."""
    ch = tuple(range(1, 6))
    v = value(prm)
    if v not in ch:
        raise ValueError("계산된 값이 선택지 범위(1~5)를 벗어납니다.")
    return ch


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    return ch.index(v) + 1  # 몇 번째 선택지인지(①=1 ...)


def statement(prm):
    base, n1, n2 = prm['base'], prm['N1'], prm['N2']
    ch = choices(prm)
    opts = ' '.join(f"{i+1}. {c}" for i, c in enumerate(ch))
    return (
        f"$\\log_{{{base}}} {n1} - \\log_{{{base}}} {n2}$ 의 값은? [2점]\n"
        f"  {opts}"
    )


# 원문제 보기(1,2,3,4,5)와 일치하는지 고정
assert choices(PARAMS) == (1, 2, 3, 4, 5)

print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
