"""
[원문제] 실수 a에 대한 조건
  '어떤 실수 x에 대하여 (x-1)^2+ax ≠ x^2+1이다.'
  의 부정이 참인 명제가 되도록 하는 a의 값은? (① 1 ② 2 ③ 3 ④ 4 ⑤ 5)

[수학 구조]
  원 명제를 (x-b)^2 + a x ≠ x^2 + c 로 일반화한다.
  부정 '모든 실수 x에 대하여 (x-b)^2+ax = x^2+c' 가 참이려면, 좌변-우변을
  x 에 대해 전개했을 때 x^1, x^0 계수가 모두 0 이어야 한다.
    (x-b)^2+ax-(x^2+c) = (a-2b) x + (b^2-c)
  x^1 계수=0  ->  a = 2b               (이 문제의 진짜 답을 만드는 손잡이: b)
  x^0 계수=0  ->  b^2 = c              (b,c 가 성립하려면 반드시 묶여야 하는 조건)
  즉 b 하나가 곧 a=2b 를 결정하고, c 는 b^2 으로 종속된다 — 전형적인 '결합 파라미터'
  구조이므로 VARIANTS 로 (b,c) 의 유효한 조합을 여러 개 제시한다.

  보기(선택지)는 원문제에서 1,2,3,4,5 로, 정답 a=2 가 두 번째 자리에 온다. 이를
  일반화하면 선택지는 [b, b+1, b+2, b+3, b+4] (즉 a/2 = b 에서 시작하는 연속된
  5개 정수) 이고, 정답 a=2b 는 이 목록에서 (b+1) 번째 자리에 온다 — b 를 바꾸면
  정답의 '번호'(보기 몇 번인지)도 함께 바뀐다.
"""
from sympy import symbols, expand, Eq, solve as sp_solve, simplify, Integer

CANDIDATE = 2        # ★원문제의 정답: ② (보기 번호). 절대 바꾸지 않는다.

# 문제를 정하는 값: (x-b)^2 + a x ≠ x^2 + c  (원문제는 b=1, c=1)
PARAMS = dict(b=1, c=1)


def value(prm):
    """일반화한 조건에서 a 의 값을 sympy 로 실제로 구한다."""
    b, c = prm['b'], prm['c']
    x, a = symbols('x a')
    lhs = (x - b) ** 2 + a * x
    rhs = x ** 2 + c
    diff = expand(lhs - rhs)                       # (a-2b) x + (b^2-c)
    coeff_x1 = diff.coeff(x, 1)
    coeff_x0 = diff.coeff(x, 0)

    a_sol = sp_solve(Eq(coeff_x1, 0), a)            # x^1 계수=0 을 a 에 대해 풀기
    if not a_sol:
        raise ValueError('x 계수가 a 를 포함하지 않음 — a 를 결정할 수 없다')
    a_val = a_sol[0]

    if simplify(coeff_x0) != 0:                     # x^0 계수는 a 와 무관 — b,c 만의 조건
        raise ValueError(f'b^2={b**2} != c={c} — 이 (b,c) 로는 부정이 참이 되는 a가 존재하지 않음')

    return simplify(a_val)


def choices(prm):
    """보기 목록: 값에서 유도 — a=2b 이므로 a/2 = b 에서 시작하는 연속 정수 5개."""
    v = value(prm)
    b = v / Integer(2)
    if not b.is_integer:
        raise ValueError('a 가 짝수가 아니어서 정수 보기 목록을 만들 수 없음')
    b = int(b)
    return [b + i for i in range(5)]


def solve(prm):
    """조건 -> 보기 번호(1-based)."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'정답 {v} 이 보기 목록 {ch} 범위를 벗어남')
    return ch.index(v) + 1


def statement(prm):
    b, c = prm['b'], prm['c']
    ch = choices(prm)
    marks = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{m}{v}' for m, v in zip(marks, ch))
    return (
        f"실수 a에 대한 조건 '어떤 실수 x에 대하여 (x-{b})^2+ax \\ne x^2+{c}이다.'"
        f" 의 부정이 참인 명제가 되도록 하는 a의 값은? {opts}"
    )


# 원문제 보기가 그대로 재현되는지 고정
assert choices(PARAMS) == [1, 2, 3, 4, 5]

# b 가 서로 다른, 유효한(c=b^2) 조합들 — 정답 '번호'가 서로 달라진다
VARIANTS = [
    dict(b=1, c=1),   # a=2  -> 보기 ②
    dict(b=2, c=4),   # a=4  -> 보기 ③
    dict(b=3, c=9),   # a=6  -> 보기 ④
    dict(b=4, c=16),  # a=8  -> 보기 ⑤
]

if __name__ == '__main__':
    print(statement(PARAMS))
    print('solve(PARAMS) =', solve(PARAMS))
    for v in VARIANTS:
        print(v, '->', solve(v))
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
