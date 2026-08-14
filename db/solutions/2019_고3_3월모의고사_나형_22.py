"""2019 고3 3월모의고사 나형 22번 — 파라미터화 솔버.

원문제: a = 9^11 일 때, 1/log_a(3) 의 값을 구하시오. (답 22)

[수학 구조]
  1/log_a(target) = log_target(a)   (로그의 밑 변환)
  a = base^n,  base = target^k  (즉 a = target^(k*n))
  => log_target(a) = k*n

  원문제는 target=3, k=2 (9 = 3^2), n=11 인 경우로,
    1/log_a(3) = log_3(a) = log_3(3^(2*11)) = 2*11 = 22

파라미터로 뽑은 수학 구조:
  - target : 로그의 밑이자 최종 지수를 만들어내는 '씨앗' 소수/정수 (원래 3)
  - k      : a의 밑(base)이 target의 몇 제곱인지 (원래 9=3^2 이므로 k=2)
  - n      : base를 다시 몇 제곱한 것이 a인지 (원래 11)
  답 = k*n 이므로 k, n 을 각각 바꾸면 답이 실제로 달라진다 (target은 구조상
  필요하지만 곱 k*n 자체는 target 값과 무관하므로 답을 바꾸는 핵심 파라미터는 k, n).
"""
import sympy as sp


PARAMS = dict(target=3, k=2, n=11)


def solve(prm):
    target = prm['target']
    k = prm['k']
    n = prm['n']

    if not (isinstance(target, int) and target > 1):
        raise ValueError("target 은 2 이상의 정수여야 합니다.")
    if not (isinstance(k, int) and k > 0):
        raise ValueError("k 는 양의 정수여야 합니다.")
    if not (isinstance(n, int) and n > 0):
        raise ValueError("n 은 양의 정수여야 합니다.")

    base = sp.Integer(target) ** k      # a의 밑, 예: 9 = 3^2
    a = base ** n                       # a = base^n, 예: 9^11

    # 1/log_a(target) = x  <=>  target^x = a  를 방정식으로 실제로 풀어 x 를 구한다.
    x = sp.symbols('x', positive=True)
    sol = sp.solve(sp.Eq(sp.Integer(target) ** x, a), x)

    if len(sol) != 1:
        raise ValueError(f"해가 유일하지 않습니다: {sol}")

    val = sp.simplify(sol[0])
    if not val.is_Integer:
        raise ValueError(f"정수해가 아닙니다: {val}")

    return int(val)


def statement(prm):
    target = prm['target']
    k = prm['k']
    n = prm['n']
    base_val = int(sp.Integer(target) ** k)
    return (
        f"a = {base_val}^{{{n}}} 일 때, "
        f"\\dfrac{{1}}{{\\log_{{a}} {target}}}의 값을 구하시오."
    )


CANDIDATE = 22

assert solve(PARAMS) == CANDIDATE, solve(PARAMS)

# k, n 각각이 실제로 답을 바꾸는지 확인 (장식 파라미터가 아님을 보장)
assert solve(dict(target=3, k=3, n=11)) != CANDIDATE   # k 변경 -> 답 변경 (3*11=33)
assert solve(dict(target=3, k=2, n=7)) != CANDIDATE    # n 변경 -> 답 변경 (2*7=14)
assert solve(dict(target=2, k=2, n=11)) == CANDIDATE   # target만 바뀌어도 구조상 답은 k*n 그대로

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
