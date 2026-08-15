"""
2번 문제: lim_{x->0} (x^3+2x)/(e^{3x}-1) 의 값 (객관식, 정답 ③=2/3 → 보기번호 3)

파라미터화 구조
---------------
분자 = a*x^n + b*x   (n>=2 인 항 a*x^n 은 x->0 극한에서 소멸 — 실제 답을 정하는 건 b, c)
분모 = e^{c*x} - 1
극한값 value = b/c  (sympy 로 실제 로피탈/극한 계산)

보기(선택지) 구조
-----------------
원문제의 다섯 보기 1/3, 1/2, 2/3, 5/6, 1 은 분모 D=6, 분자 r..r+4 (r=2) 인
등차수열 (r+i)/D, i=0..4 이다. 정답 위치(1-based)는 value 가 이 격자에서 몇 번째
칸에 있는지로 정해진다: value == (r+k)/D 를 만족하는 k 를 찾아 idx=k+1.

D, r 은 "보기를 만드는 격자"를 결정하는 독립적 설계 파라미터이고, b, c 는 값 자체를
결정한다. b, c, r 을 흔들면 value 가 격자 위 다른 칸에 놓여 정답 번호(solve 결과)가
실제로 바뀐다 (a, n, D 는 이 문제에서는 답을 안 바꾸는 장식/구조 파라미터).
"""
from sympy import symbols, limit, exp, Rational, simplify

CANDIDATE = 3  # ★원문제 정답(보기 번호) — 절대 바꾸지 않음

PARAMS = dict(
    a=1,   # 분자의 소멸항 계수 (a*x^n) — 극한값엔 영향 없음(장식)
    n=3,   # 분자의 소멸항 차수 (n>=2) — 극한값엔 영향 없음(장식)
    b=2,   # 분자의 1차항 계수 (x^3+2x 의 "2")
    c=3,   # 분모 e^{c x}-1 의 계수 (e^{3x} 의 "3")
    r=2,   # 보기 격자의 시작 분자값 (r, r+1, ..., r+4)/D
    D=6,   # 보기 격자의 공통분모
)


def value(prm):
    """sympy 로 실제 극한을 계산한다 (로피탈/테일러와 동치)."""
    x = symbols('x')
    expr = (prm['a'] * x**prm['n'] + prm['b'] * x) / (exp(prm['c'] * x) - 1)
    return limit(expr, x, 0)


def choices(prm):
    """value 가 놓일 수 있는 등차수열 격자 (r+i)/D, i=0..4 — 원문제 보기를 재현한다."""
    r, D = prm['r'], prm['D']
    return [Rational(r + i, D) for i in range(5)]


def solve(prm):
    """value 가 choices 격자에서 몇 번째(1-based)인지를 찾아 보기 번호를 반환.
    격자 위에 놓이지 않으면(성립하지 않는 조합) 예외를 던진다."""
    v = value(prm)
    opts = choices(prm)
    for i, o in enumerate(opts, start=1):
        if simplify(o - v) == 0:
            return i
    raise ValueError(f'value={v} 가 choices={opts} 격자 위에 없음 — 성립하지 않는 조합')


def statement(prm):
    a, n, b, c = prm['a'], prm['n'], prm['b'], prm['c']
    num = (f"x^{n}" if a == 1 else f"{a}x^{n}") + (f"+{b}x" if b >= 0 else f"{b}x")
    opts = choices(prm)
    labels = ['①', '②', '③', '④', '⑤']
    opt_str = '  '.join(f'{lab} {o}' for lab, o in zip(labels, opts))
    return (
        f"lim_{{x->0}} ({num})/(e^{{{c}x}}-1) 의 값은?\n" + opt_str
    )


# 원문제 보기(1/3, 1/2, 2/3, 5/6, 1) 재현 확인
assert choices(PARAMS) == [Rational(1, 3), Rational(1, 2), Rational(2, 3), Rational(5, 6), 1]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
