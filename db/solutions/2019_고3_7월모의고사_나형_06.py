import sympy as sp

# ─────────────────────────────────────────────────────────────────────────
# 문제 구조
#   f(x) = m*x + k          (x < c)
#          x^2 + b*x + a    (x >= c)
#   가 실수 전체에서 연속일 때 a 를 구한다.
#   연속 조건: x=c 에서 좌극한(m*c+k) = 우변 값(c^2+b*c+a).
#
# 파라미터:
#   m, k : x<c 구간 일차식 계수/상수 (원문제: x+1 → m=1, k=1)
#   c    : 구간이 갈리는 경계점     (원문제: 2)
#   b    : x>=c 구간 이차식의 일차항 계수 (원문제: -4x → b=-4)
# 이 넷을 바꾸면 연속조건 방정식 자체가 달라지므로 a(정답)도 달라진다.
#
# 보기(선택지)는 "정답" 하나만이 아니라, 이 문제를 풀 때 흔히 나올 수 있는
# 오답 패턴 4가지를 같은 파라미터로부터 sympy 로 각각 계산해 만든다.
#   f1: 좌극한 부호를 통째로 잘못 씀        (-m*c-k = 우변)
#   f2: 이차항(c^2+b*c)을 깜빡하고 a=좌극한 이라 오해
#   f3: 경계점을 c 대신 c-1 로 잘못 대입
#   f4: 정답에서 단순 계산 실수로 +2
# 오답 공식도 파라미터에 따라 값이 달라지므로, 파라미터를 바꾸면 정답이
# 보기 중 몇 번째에 놓이는지(선택지 번호)까지 실제로 바뀐다.
# ─────────────────────────────────────────────────────────────────────────

CANDIDATE = 4        # ★원문제 정답(선택지 번호, ④) — 절대 바꾸지 않음

PARAMS = dict(m=1, k=1, c=2, b=-4)


def value(prm):
    """연속조건 방정식을 sympy 로 풀어 a 의 실제 값을 구한다."""
    m, k, c, b = prm['m'], prm['k'], prm['c'], prm['b']
    a = sp.symbols('a')
    left = m * c + k                      # x -> c^- 에서의 좌극한
    right = c ** 2 + b * c + a            # f(c) (x>=c 구간의 값)
    sols = sp.solve(sp.Eq(left, right), a)
    if not sols:
        raise ValueError('연속이 되도록 하는 a가 존재하지 않는다')
    return sols[0]


def _wrong1(prm):
    """오답1: 좌극한의 부호를 통째로 잘못 적용."""
    m, k, c, b = prm['m'], prm['k'], prm['c'], prm['b']
    a = sp.symbols('a')
    left = -(m * c + k)
    right = c ** 2 + b * c + a
    sols = sp.solve(sp.Eq(left, right), a)
    if not sols:
        raise ValueError('오답1 계산 불가')
    return sols[0]


def _wrong2(prm):
    """오답2: 이차항(c^2+b*c)을 빼먹고 a = 좌극한 이라 오해."""
    m, k, c = prm['m'], prm['k'], prm['c']
    return m * c + k


def _wrong3(prm):
    """오답3: 경계점을 c 대신 c-1 로 잘못 대입해서 연속조건을 세움."""
    m, k, c, b = prm['m'], prm['k'], prm['c'], prm['b']
    a = sp.symbols('a')
    c1 = c - 1
    left = m * c1 + k
    right = c1 ** 2 + b * c1 + a
    sols = sp.solve(sp.Eq(left, right), a)
    if not sols:
        raise ValueError('오답3 계산 불가')
    return sols[0]


def _wrong4(prm):
    """오답4: 정답에서 단순 계산 실수로 +2."""
    return value(prm) + 2


def choices(prm):
    """값 + 4가지 오답 패턴을 오름차순으로 정렬해 5지선다 보기를 만든다."""
    vals = [value(prm), _wrong1(prm), _wrong2(prm), _wrong3(prm), _wrong4(prm)]
    for v in vals:
        if not getattr(sp.nsimplify(v), 'is_number', False) or sp.nsimplify(v).has(sp.zoo, sp.nan, sp.oo):
            raise ValueError('보기 계산 중 유효하지 않은 값 발생')
    return sorted(vals, key=lambda v: sp.N(v))


# 원문제 보기(① 1 ② 3 ③ 5 ④ 7 ⑤ 9)와 일치하는지 고정
assert choices(PARAMS) == [1, 3, 5, 7, 9]


def solve(prm):
    """정답 값이 보기 중 몇 번째(1~5)인지 반환한다."""
    opts = choices(prm)
    v = value(prm)
    return opts.index(v) + 1


def statement(prm):
    m, k, c, b = prm['m'], prm['k'], prm['c'], prm['b']
    lin = f"{m}x + {k}" if m != 1 else f"x + {k}"
    quad_b = f"+ {b}x" if b >= 0 else f"- {abs(b)}x"
    opts = choices(prm)
    opt_marks = ['①', '②', '③', '④', '⑤']
    opt_str = ' '.join(f"{mk} {v}" for mk, v in zip(opt_marks, opts))
    return (
        f"함수 f(x) = {lin} (x < {c}), x^2 {quad_b} + a (x >= {c}) 가 "
        f"실수 전체의 집합에서 연속일 때, 상수 a의 값은?\n{opt_str}"
    )


if __name__ == '__main__':
    print(statement(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
