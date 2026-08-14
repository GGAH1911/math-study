from sympy import symbols, Eq, Rational, nsimplify
from sympy import solve as sp_solve

CANDIDATE = 4  # ★원문제 정답(보기 번호이자 값 4). 절대 바꾸지 않는다.

# ------------------------------------------------------------------
# 문제의 수학 구조
#   명제 'x - c = 0 이면  x^2 + (p*a) x + (q*a) = 0 이다' 가 참
#   ⟺ x = c 를 방정식에 대입했을 때 등식이 성립
#   c^2 + p*a*c + q*a = 0  →  a = -c^2 / (p*c + q)   (단 p*c+q ≠ 0)
#
#   원문제(x-2=0 이면 x^2-ax+a=0)는 c=2, p=-1, q=1 인 특수한 경우.
#   보기는 anchor 에서 시작하는 5개의 연속한 정수(원문제는 1,2,3,4,5).
# ------------------------------------------------------------------
PARAMS = dict(
    c=2,       # 명제의 조건 'x - c = 0' 에서의 근 c  (원문제 c=2)
    p=-1,      # x항 계수를 이루는 a의 배수 (원문제: -a → p=-1)
    q=1,       # 상수항을 이루는 a의 배수 (원문제: +a → q=1)
    anchor=1,  # 보기 ①의 값 (보기가 anchor, anchor+1, ..., anchor+4)
)

# c, q 를 바꾸면 실제로 답(보기 번호)이 달라짐을 보여주는 조합들.
# (c, q 는 c-q 조합에 따라 정수해가 나오는지가 갈리므로 서로 묶여 있어
#  VARIANTS 로 성립하는 조합만 제시한다.)
VARIANTS = [
    dict(c=2, p=-1, q=1, anchor=1),   # 원문제: a=4 → 보기 ④
    dict(c=2, p=-1, q=0, anchor=1),   # q만 변경: a=2 → 보기 ②
    dict(c=3, p=-1, q=0, anchor=1),   # c만 다시 변경: a=3 → 보기 ③
]


def value(prm):
    """조건을 만족시키는 상수 a의 값을 sympy로 실제 계산."""
    x, a = symbols('x a', real=True)
    c, p, q = prm['c'], prm['p'], prm['q']

    expr = x**2 + p * a * x + q * a          # x^2 + p*a*x + q*a
    eq = Eq(expr.subs(x, c), 0)               # x=c 대입 → a에 대한 방정식

    denom = p * c + q
    if denom == 0:
        # a의 계수가 0 → a가 유일하게 정해지지 않거나(항등식) 해가 없음
        raise ValueError("이 조합에서는 a가 유일하게 결정되지 않습니다.")

    sol = sp_solve(eq, a)
    if not sol:
        raise ValueError("a에 대한 해가 존재하지 않습니다.")

    a_val = nsimplify(sol[0])
    return a_val


def choices(prm):
    """보기 목록: anchor에서 시작하는 5개의 연속한 정수 (원문제: 1~5)."""
    anchor = prm['anchor']
    return tuple(range(anchor, anchor + 5))


def solve_fn(prm):
    """value(prm)이 choices(prm) 중 몇 번째(①~⑤)인지를 답으로 반환."""
    v = value(prm)
    ch = choices(prm)

    if not v.is_integer:
        raise ValueError(f"값 {v}이 정수가 아니어서 보기와 대응되지 않습니다.")

    v_int = int(v)
    if v_int not in ch:
        raise ValueError(f"값 {v_int}이 보기 {ch} 범위 밖입니다.")

    return ch.index(v_int) + 1  # 1번(①)부터 시작하는 보기 번호


def solve(prm):
    return solve_fn(prm)


def _fmt_a_term(coef, has_x):
    """p*a 또는 q*a 항을 'ax' / '2a' / '-3ax' 같은 문자열로 포맷."""
    coef = Rational(coef)
    if coef == 0:
        return None
    sign = '+' if coef > 0 else '-'
    mag = abs(coef)
    mag_str = '' if mag == 1 else str(mag)
    var = 'x' if has_x else ''
    return sign, f"{mag_str}a{var}"


def statement(prm):
    c, p, q, anchor = prm['c'], prm['p'], prm['q'], prm['anchor']

    eq_str = "x^2"
    for coef, has_x in [(p, True), (q, False)]:
        term = _fmt_a_term(coef, has_x)
        if term is None:
            continue
        sign, s = term
        eq_str += f" {sign} {s}"
    eq_str += " = 0"

    ch = choices(prm)
    circled = ['①', '②', '③', '④', '⑤']
    options = ' '.join(f"{circled[i]} {ch[i]}" for i in range(5))

    return (
        "실수 x에 대하여 명제\n"
        f"  'x-{c}=0이면 {eq_str}이다.'\n"
        "가 참일 때, 상수 a의 값은? [2점]\n"
        f"  {options}"
    )


if __name__ == '__main__':
    # 원문제 재현 검증
    print(statement(PARAMS))
    print('value(PARAMS) =', value(PARAMS))
    print('solve(PARAMS) =', solve(PARAMS))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')

    # 파라미터가 실제로 답을 바꾸는지 확인
    for v in VARIANTS:
        print(v, '->', solve(v))

    assert choices(PARAMS) == (1, 2, 3, 4, 5)
    assert solve(VARIANTS[0]) == 4
    assert solve(VARIANTS[1]) == 2
    assert solve(VARIANTS[2]) == 3
    assert solve(VARIANTS[1]) != solve(VARIANTS[0])
    assert solve(VARIANTS[2]) != solve(VARIANTS[0])
