# 문제: 함수 y = log_base(x) + offset 의 그래프가 점 (a, y0)을 지날 때 a의 값은? (객관식)
#
# 수학 구조:
#   y0 = log_base(a) + offset  ->  a = base^(y0 - offset)
#
# 보기 구조 (원문제): 1/16, 1/8, 1/4, 1/2, 1  =  base^(-4), base^(-3), ..., base^(0)
#   즉 밑이 base인 지수들을 exp_min 부터 num_choices개, 1씩 증가시키며 오름차순으로 나열.
#   답이 그 목록의 몇 번째(1-based)에 오는지가 정답 번호.
#
# 파라미터로 뽑은 것:
#   base       : 로그의 밑
#   offset     : y = log_base(x) + offset 의 상수항
#   y0         : 점의 y좌표 (원문제는 1)
#   exp_min    : 보기 목록에 나오는 지수의 최솟값 (원문제는 -4, 즉 1/16부터 시작)
#   num_choices: 보기 개수 (원문제는 5)
#
# offset, y0, exp_min 을 각각 바꾸면 정답 번호(보기 몇 번인지)가 실제로 달라짐을 아래에서 확인.

from sympy import symbols, log, Eq, solve as sympy_solve, Rational

CANDIDATE = 4  # ★원문제 정답 (④ 1/2)

PARAMS = dict(
    base=2,
    offset=2,
    y0=1,
    exp_min=-4,
    num_choices=5,
)


def value(prm):
    """y0 = log_base(a) + offset 을 sympy로 실제로 풀어 a를 구한다."""
    a = symbols('a', positive=True)
    eq = Eq(log(a, prm['base']) + prm['offset'], prm['y0'])
    sol = sympy_solve(eq, a)
    if len(sol) != 1:
        raise ValueError(f"해가 유일하지 않습니다: {sol}")
    return sol[0]


def choices(prm):
    """value에서 유도: base의 exp_min부터 num_choices개 연속 지수를 오름차순으로 나열."""
    base = Rational(prm['base'])
    exp_min = prm['exp_min']
    n = prm['num_choices']
    return [base ** e for e in range(exp_min, exp_min + n)]


def solve(prm):
    v = value(prm)
    cs = choices(prm)
    if v not in cs:
        raise ValueError(f"값 {v} 이(가) 보기 목록 {cs} 안에 없어 문제가 성립하지 않습니다.")
    return cs.index(v) + 1  # 1-based 보기 번호


def statement(prm):
    base = prm['base']
    offset = prm['offset']
    y0 = prm['y0']
    cs = choices(prm)
    labels = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧'][:len(cs)]
    choice_str = '  '.join(f'{lab} {c}' for lab, c in zip(labels, cs))
    return (
        f"함수 y = log_{base}(x) + {offset} 의 그래프가 점 (a, {y0})을 지날 때, "
        f"a의 값은?\n{choice_str}"
    )


# 원문제 보기가 실제로 재현되는지 고정
assert choices(PARAMS) == [Rational(1, 16), Rational(1, 8), Rational(1, 4), Rational(1, 2), 1]
assert value(PARAMS) == Rational(1, 2)

print(statement(PARAMS))
print('answer:', solve(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
