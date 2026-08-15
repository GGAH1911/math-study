import sympy as sp

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# "y = sqrt(x-p) + a 를 x축으로 b, y축으로 c 만큼 평행이동하면 y = sqrt(x-q) 와
# 일치한다. a+b 의 값은?" 형태의 무리함수 평행이동 문제.
#
# 평행이동 결과: y - c = sqrt((x-b) - p) + a  →  y = sqrt(x-b-p) + (a+c)
# 이것이 y = sqrt(x-q) 와 항등이 되려면
#   (근호 내부 x 의 계수 비교) -b - p + q = 0   →  b = q - p
#   (상수항 비교)              a + c = 0        →  a = -c
# 답은 a+b = (q-p) - c. p, q, c 세 값 모두 답을 바꾸는 독립 파라미터다.
#
# 원문제는 p=1, q=4, c=-1 인 경우로, a=1, b=3, a+b=4.
# 이 문제유형은 "①1 ②2 ③3 ④4 ⑤5" 처럼 답이 1~5 사이의 정수이면 보기가
# 그대로 1,2,3,4,5 로 나오는 고정 보기창(window) 구조다 — 계수를 바꿔도
# 계산값이 1~5 안에 있는 한 같은 보기 목록을 쓰고, 그 안에서 몇 번째(①~⑤)인지가
# 실제 정답 번호가 된다.

CANDIDATE = 4  # ★원문제 정답 (④ 4)

PARAMS = dict(
    p=1,    # 원래 함수 y=sqrt(x-p)+a 의 x축 이동 상수
    q=4,    # 목표 함수 y=sqrt(x-q) 의 x축 이동 상수
    c=-1,   # y축 방향 평행이동량
)

# 이 문제유형이 강제하는 고정 보기창: 1부터 5까지의 연속 정수.
CHOICES_WINDOW = (1, 2, 3, 4, 5)


def value(prm):
    """평행이동 후 항등식이 되는 조건을 sympy 로 실제로 풀어 a+b 값을 구한다."""
    p, q, c = prm['p'], prm['q'], prm['c']
    a, b = sp.symbols('a b', real=True)
    # 평행이동 결과 y = sqrt(x-b-p) + (a+c) 가 목표 y = sqrt(x-q) 와 항등이 되는 조건:
    #   근호 내부 계수 비교: -b - p + q = 0
    #   상수항 비교         : a + c = 0
    eqs = [sp.Eq(-b - p + q, 0), sp.Eq(a + c, 0)]
    sol = sp.solve(eqs, [a, b], dict=True)
    if not sol:
        raise ValueError(f"평행이동 조건을 만족하는 a,b 가 없음: p={p}, q={q}, c={c}")
    s = sol[0]
    return sp.nsimplify(s[a] + s[b])


def choices(prm):
    """이 문제유형이 강제하는 고정 보기: 1부터 5까지의 연속 정수."""
    return CHOICES_WINDOW


def solve(prm):
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        # 값이 1~5 범위를 벗어나면 이 문제유형(보기가 1,2,3,4,5)으로 성립하지 않음
        raise ValueError(f"값 {v}이(가) 보기 범위 {ch}를 벗어남 — 문제로 성립하지 않음")
    return ch.index(v) + 1  # 1-based 보기 번호 (①=1, ..., ⑤=5)


def statement(prm):
    p, q, c = prm['p'], prm['q'], prm['c']
    return (
        f"함수 y=\\sqrt{{x-{p}}}+a의 그래프를 x축의 방향으로 b만큼, "
        f"y축의 방향으로 {c}만큼 평행이동하면 함수 y=\\sqrt{{x-{q}}}의 "
        f"그래프와 일치한다. a+b의 값은? (단, a, b는 상수이다.)"
    )


# 원문제 보기가 정확히 ①1 ②2 ③3 ④4 ⑤5 인지 고정 검증
assert choices(PARAMS) == (1, 2, 3, 4, 5)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
