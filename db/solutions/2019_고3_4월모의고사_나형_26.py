"""2019 고3 4월모의고사 나형 26번 — 파라미터화 솔버.

원문제: 두 상수 a, b에 대하여
  lim_{x→∞} a x^2/(x^2-1) = 2,   lim_{x→1} a(x-1)/(x^2-1) = b
일 때, a+b의 값을 구하시오. (답 3)

★수학 구조 분석
  분모 x^2-1 = (x-1)(x+1) 은 사실 "근 k=1 을 갖는 이차식 x^2-k^2" 의 특수한 경우다.
  - 첫 번째 극한: lim_{x→∞} a x^2/(x^2-k^2) = a  (최고차항 비율) → 이 값을 c1 로 두면 a = c1.
  - 두 번째 극한: a(x-k)/(x^2-k^2) = a(x-k)/((x-k)(x+k)) = a/(x+k) 이므로
    lim_{x→k} = a/(2k) = b.
  따라서 a+b = c1 + c1/(2k).

파라미터로 뽑은 것:
  c1 : 첫 번째 극한의 목표값 (원문제 2)
  k  : 분모가 근으로 갖는 값 (원문제 1) — 두 번째 극한을 계산하는 점이자 분모 x^2-k^2 를 결정
  둘 다 답 a+b = c1 + c1/(2k) 에 실제로 관여한다(장식 아님).
"""
import sympy as sp


def value(prm):
    """조건을 그대로 sympy 로 풀어 a, b, a+b 를 구한다."""
    x, a = sp.symbols('x a')
    c1 = sp.nsimplify(prm['c1'])
    k = sp.nsimplify(prm['k'])
    if k == 0:
        raise ValueError('k=0 이면 두 번째 극한의 분모가 0이 되어 문제가 성립하지 않는다')

    # 첫 번째 조건: lim_{x→∞} a x^2/(x^2-k^2) = c1
    first_limit = sp.limit(a * x ** 2 / (x ** 2 - k ** 2), x, sp.oo)
    a_sols = sp.solve(sp.Eq(first_limit, c1), a)
    if not a_sols:
        raise ValueError('a에 대한 해가 존재하지 않는다')
    a_val = a_sols[0]

    # 두 번째 조건: lim_{x→k} a(x-k)/(x^2-k^2) = b
    second_expr = a_val * (x - k) / (x ** 2 - k ** 2)
    b_val = sp.limit(second_expr, x, k)
    if b_val.has(sp.zoo, sp.nan, sp.oo):
        raise ValueError('두 번째 극한이 발산하여 b를 정할 수 없다')

    return a_val, b_val


def solve(prm):
    a_val, b_val = value(prm)
    return sp.nsimplify(a_val + b_val)


def statement(prm):
    c1 = prm['c1']
    k = prm['k']
    k2 = sp.nsimplify(k) ** 2
    return (
        "두 상수 a, b에 대하여\n"
        f"  lim_(x→∞) a·x^2/(x^2-{k2}) = {c1},  "
        f"lim_(x→{k}) a·(x-{k})/(x^2-{k2}) = b\n"
        "일 때, a+b의 값을 구하시오."
    )


CANDIDATE = 3
PARAMS = dict(c1=2, k=1)

# 결합 파라미터가 아니어도 되지만, 서로 다른 답을 내는 예시 조합을 남겨 재생성력을 보여준다.
VARIANTS = [
    dict(c1=2, k=1),   # 원문제: a=2, b=1 → 3
    dict(c1=4, k=2),   # a=4, b=1 → 5
    dict(c1=6, k=3),   # a=6, b=1 → 7
]

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
