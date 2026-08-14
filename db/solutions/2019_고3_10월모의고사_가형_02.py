from sympy import symbols, ln, limit, Integer

# ─────────────────────────────────────────────────────────────
# 원문제: lim_{x->0} ln(1+8x) / (2x) 의 값은? (선택지 ①1 ②2 ③3 ④4 ⑤5, 정답 ④=4)
#
# 수학 구조: lim_{x->0} ln(1+ax)/(bx) 는 0/0 꼴이므로 로피탈 정리(또는
#   ln(1+u)~u, u->0 근사)를 적용하면 lim_{x->0} (a/(1+ax)) / b = a/b 로 수렴한다.
#   즉 이 문제의 답은 오직 계수비 a/b 로 결정된다 (a, b 가 답을 바꾸는 파라미터).
#   선택지는 시작값 start 부터 5개의 연속 정수 (원문제는 start=1 -> 1,2,3,4,5)이며,
#   정답 a/b 가 이 5개 중 어디에 위치하는지가 "몇 번(①~⑤)"인 CANDIDATE 를 결정한다
#   (start 역시 답(선택 번호)을 바꾸는 파라미터).
# ─────────────────────────────────────────────────────────────

CANDIDATE = 4  # ★원문제 정답: ④번 (값 4)

PARAMS = dict(
    a=8,      # ln(1+ax) 의 계수
    b=2,      # 분모 bx 의 계수
    start=1,  # 선택지 시작값 (선택지 = start, start+1, ..., start+4)
)


def value(prm):
    """lim_{x->0} ln(1+ax)/(bx) 를 sympy 로 실제 계산한 극한값 (=a/b)."""
    x = symbols('x')
    a, b = prm['a'], prm['b']
    if b == 0:
        raise ValueError("b는 0이 될 수 없습니다.")
    expr = ln(1 + a * x) / (b * x)
    v = limit(expr, x, 0)
    return v


def choices(prm):
    """선택지 5개: start 부터 시작하는 연속 정수 (①~⑤에 대응)."""
    s = prm['start']
    return [s + i for i in range(5)]


def solve(prm):
    """정답 선택지 번호(1~5)를 반환. 극한값이 보기 중에 없으면 예외를 던진다."""
    v = value(prm)
    if v.is_Integer is not True and not (v == Integer(round(float(v)))):
        raise ValueError(f"극한값 {v} 이 정수가 아니어서 이 보기 형식의 문제로 성립하지 않습니다.")
    v_int = int(v)
    ch = choices(prm)
    if v_int not in ch:
        raise ValueError(f"극한값 {v_int} 이 보기 {ch} 안에 없습니다.")
    return ch.index(v_int) + 1


def statement(prm):
    a, b = prm['a'], prm['b']
    ch = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f"{c}{n}" for c, n in zip(circled, ch))
    return (
        f"$\\lim_{{x \\to 0}} \\frac{{\\ln(1+{a}x)}}{{{b}x}}$ 의 값은? [2점]\n  {opts}"
    )


# ── 원문제 보기 재현 확인 ──
assert choices(PARAMS) == [1, 2, 3, 4, 5]

# ── 파라미터가 실제로 답을 바꾸는지 확인 (문서화용, 정답 재현에는 영향 없음) ──
_variant_b = solve(dict(a=6, b=2, start=1))     # a/b=3 -> 선택지 [1,2,3,4,5] 중 3번째
_variant_start = solve(dict(a=8, b=2, start=2))  # 값 4, 선택지 [2,3,4,5,6] 중 3번째
assert _variant_b != CANDIDATE
assert _variant_start != CANDIDATE

print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
