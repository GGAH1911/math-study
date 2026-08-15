import sympy as sp

# ── 문제 구조 ──────────────────────────────────────────────────────
# 실수 전체에서 연속인 f(x) 가
#   ∫_a^x f(t) dt = (x + a + c) * e^{k x}     ... (★)
# 를 만족시킬 때 f(a) 의 값은? (단, a 는 상수, 보기는 e^1 ~ e^5)
#
# 원문제는 c=-4, k=1 인 경우: (x+a-4)e^x
#
# 풀이(일반화):
#   (★) 양변을 x 로 미분 → f(x) = e^{kx}[1 + k(x+a+c)]
#   (★) 에 x=a 대입하면 좌변 ∫_a^a f(t)dt = 0 이므로
#       0 = (2a+c) e^{ka}  →  e^{ka}>0 이므로  a = -c/2
#   f(a) = e^{ka}[1 + k(2a+c)] = e^{ka}   ( 2a+c=0 이므로 대괄호 안이 1 )
#   즉 f(a) = e^n,  n = k*a = -k*c/2
#
# 보기는 문제 형식상 e^1, e^2, e^3, e^4, e^5 (지수 1~5) 로 고정되어 있고,
# 정답은 그 중 n 번째(=지수가 n인 것) 이다. c, k 를 바꾸면 n 이 달라져
# 서로 다른 보기가 정답이 되거나(파라미터가 실제로 답을 바꿈), n 이 1~5
# 범위의 정수를 벗어나면 더 이상 이 보기 형식의 문제가 성립하지 않으므로
# 예외를 던진다.

CANDIDATE = 2  # 원문제 정답: ② e^2

PARAMS = dict(
    c=-4,  # (x + a + c) 의 상수항 c
    k=1,   # e^{kx} 의 계수 k  (원문제는 e^x 이므로 k=1)
)


def _exponent(prm):
    """f(a) = e^n 의 지수 n = -k*c/2 를 sympy 로 계산한다."""
    c = sp.nsimplify(prm['c'])
    k = sp.nsimplify(prm['k'])
    a = sp.together(-c / sp.Integer(2))       # 2a+c=0 의 해
    n = sp.simplify(k * a)                    # f(a)=e^{ka} 의 지수
    return n


def value(prm):
    """f(a) 의 실제 값 (수식)."""
    return sp.exp(_exponent(prm))


def choices(prm):
    """객관식 보기: e^1, e^2, e^3, e^4, e^5 (문제 형식이 고정하는 지수 범위)."""
    return [sp.exp(i) for i in range(1, 6)]


# 유도한 보기가 원문제의 보기(① e ② e^2 ③ e^3 ④ e^4 ⑤ e^5)와 같은지 고정
assert choices(PARAMS) == [sp.exp(1), sp.exp(2), sp.exp(3), sp.exp(4), sp.exp(5)]
assert sp.simplify(value(PARAMS) - sp.exp(2)) == 0


def solve(prm):
    """value(prm) 이 choices(prm) 중 몇 번째인지(1-based) 반환."""
    n = _exponent(prm)
    if not n.is_integer:
        raise ValueError(f'지수 n={n} 이 정수가 아니어서 보기(e^1~e^5)와 대응되지 않습니다')
    n_int = int(n)
    if n_int < 1 or n_int > 5:
        raise ValueError(f'지수 n={n_int} 이 보기 범위(1~5) 밖이라 문제가 성립하지 않습니다')
    return n_int


def statement(prm):
    c = prm['c']
    k = prm['k']
    cterm = f'{c:+d}' if c != 0 else ''
    kx = 'x' if k == 1 else f'{k}x'
    body = f'(x + a {cterm})'.replace('  ', ' ').replace('a )', 'a)')
    return (
        '실수 전체의 집합에서 연속인 함수 f(x)가\n'
        f'  \\int_{{a}}^{{x}} f(t)\\,dt = {body} e^{{{kx}}}\n'
        '을 만족시킬 때, f(a)의 값은? (단, a는 상수이다.)\n'
        '① e ② e^2 ③ e^3 ④ e^4 ⑤ e^5'
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
