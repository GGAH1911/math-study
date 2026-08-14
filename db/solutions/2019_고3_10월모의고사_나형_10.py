# 문제 10번 파라미터화
# ------------------------------------------------------------
# 원문제: 영역 S = {(x,y) : 2x - y >= 0, y > 0} 에서
#   직선 x=n 이 S와 만나는 점 중 y좌표가 정수인 점들의 (x좌표+y좌표) 합을 a_n 이라 할 때
#   a_10 - a_5 의 값은?  (선택지 ①300 ②305 ③310 ④315 ⑤320, 정답 ②)
#
# 수학 구조:
#   - 직선 x=n 위에서 0 < y <= c*n (c는 부등식 2x-y>=0의 계수 2) 인 정수 y 개수만큼
#     점 (n, y) 가 S에 속하고, 그 좌표합은 n+y.
#   - a_n = sum_{y=1}^{c*n} (n+y)  ... 계수 c, 대상 n 이 문제를 정하는 진짜 변수.
#   - 최종 물음은 a_{n1} - a_{n2} (원문제는 n1=10, n2=5).
#
# 파라미터화:
#   c   : 부등식 c*x - y >= 0 의 계수 (원문제 2)
#   n1  : 큰 쪽 직선의 x좌표 (원문제 10)
#   n2  : 작은 쪽 직선의 x좌표 (원문제 5)
#   base, step : 그 시험에서 실제로 배치된 5지선다 보기의 시작값/공차
#                (300,305,310,315,320 은 등차수열이며, 값(value)이 그 수열의
#                 몇 번째 항인지가 곧 정답 번호다 -> 보기는 값에서 독립적으로
#                 정해지고, 정답 번호는 실제로 값을 그 수열에서 '찾아서' 결정한다.)
#
# c, n1, n2 는 함께 바뀌면 값(value)과 정답 번호(solve)가 모두 실제로 달라진다.
# (한 개만 흔들면 정수 조건 - y좌표가 정수인 점 개수를 세는 구조 상 -
#  값이 우연히 보기 범위 안에 남아있기 어려우므로, 서로 묶어 흔드는 VARIANTS 로 검증한다.)

from sympy import symbols, summation, Integer

CANDIDATE = 2  # ★원문제 정답 (선택지 번호, 절대 변경 금지)

PARAMS = dict(c=2, n1=10, n2=5, base=300, step=5)

# 정수해가 자연스럽게 나오는(=보기 수열 안에 값이 들어오는) 조합들.
# 원문제와 다른 정답 번호를 내는 조합이 2개 이상 포함되어 있어야 함(4번 규칙 참고).
VARIANTS = [
    dict(c=2, n1=10, n2=5, base=300, step=5),   # 원문제: value=305 -> ②
    dict(c=2, n1=9, n2=2, base=300, step=5),    # value=315 -> ④ (원문제와 다름)
    dict(c=1, n1=23, n2=18, base=300, step=5),  # value=310 -> ③ (원문제와 다름)
]


def _a_n(c, n):
    """a_n = sum_{y=1}^{c*n} (n+y) 를 sympy 합으로 실제 계산."""
    c = Integer(c)
    n = Integer(n)
    upper = c * n
    if upper < 1 or upper != int(upper):
        raise ValueError(f"직선 x={n} 위에 조건을 만족하는 정수 y좌표가 존재하지 않습니다 (c*n={upper}).")
    y = symbols('y', integer=True)
    return int(summation(n + y, (y, 1, int(upper))))


def value(prm):
    """문제의 수학적 답: a_{n1} - a_{n2}."""
    c, n1, n2 = prm['c'], prm['n1'], prm['n2']
    if n1 == n2:
        raise ValueError("n1과 n2가 같으면 문제가 성립하지 않습니다.")
    return _a_n(c, n1) - _a_n(c, n2)


def choices(prm):
    """실제 시험에 배치된 5지선다 보기: base, base+step, ..., base+4*step (등차수열)."""
    base, step = prm['base'], prm['step']
    return [base + i * step for i in range(5)]


# 원문제 보기와 정확히 일치하는지 고정
assert choices(PARAMS) == [300, 305, 310, 315, 320]


def solve(prm):
    """value(prm)이 choices(prm) 중 몇 번째(1-based)인지 찾아 정답 번호로 반환."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f"값 {v}이 보기 {ch} 안에 없습니다 (성립하지 않는 조합).")
    return ch.index(v) + 1


def statement(prm):
    return (
        f"좌표평면에서 연립부등식 {{ {prm['c']}x - y >= 0, y > 0 }}이 나타내는 영역을 S라 하자. "
        f"자연수 n에 대하여 직선 x=n과 영역 S가 만나는 점 중 y좌표가 정수인 모든 점들의 "
        f"x좌표와 y좌표의 합을 a_n이라 하자. a_{{{prm['n1']}}} - a_{{{prm['n2']}}}의 값은?\n"
        f"보기: {', '.join(str(x) for x in choices(prm))}"
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    print('value =', value(PARAMS), 'choices =', choices(PARAMS), 'solve =', solve(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')

    # 파라미터 변화 확인 (2개 이상의 조합이 값과 정답 번호를 실제로 바꾼다)
    for prm in VARIANTS:
        v = value(prm)
        s = solve(prm)
        print(prm, '-> value=', v, 'answer_no=', s)

    diff_count = sum(1 for prm in VARIANTS[1:] if solve(prm) != CANDIDATE)
    assert diff_count >= 2, 'VARIANTS 중 원문제와 다른 답을 내는 조합이 2개 이상이어야 함'
