"""2019 고3 4월모의고사 나형 25번 — 파라미터화 솔버.

문제: 수열 {a_n} 에 대하여 Σ_{k=1}^{n} a_k = S 일 때 Σ_{k=1}^{n}(k + a_k) 의 값을 구하시오.

수학 구조:
  Σ_{k=1}^{n}(k + a_k) = Σ_{k=1}^{n} k + Σ_{k=1}^{n} a_k = n(n+1)/2 + S

파라미터로 뽑은 것:
  n : 시그마의 상한 (합의 개수) — 1부터 n까지 정수합 Σk 를 결정
  S : 주어진 조건 Σ a_k 의 값

두 값 모두 답(n(n+1)/2 + S)에 그대로 더해지는 항이므로, 각각을 바꾸면 답이 실제로 달라진다.
(n 은 삼각수 항을 통해, S 는 상수항을 통해 — 서로 독립적으로 답에 기여)
"""
import sympy as sp


def solve(prm):
    n = prm['n']
    S = prm['sum_a']
    k = sp.symbols('k', integer=True, positive=True)
    # Σ_{k=1}^{n} k 를 실제로 sympy 합산으로 계산
    triangular = sp.summation(k, (k, 1, n))
    return sp.nsimplify(triangular + S)


def statement(prm):
    n = prm['n']
    S = prm['sum_a']
    return (
        f"수열 {{a_n}}에 대하여 \\sum_{{k=1}}^{{{n}}} a_k = {S}일 때, "
        f"\\sum_{{k=1}}^{{{n}}} (k+a_k)의 값을 구하시오."
    )


CANDIDATE = 85
PARAMS = dict(n=10, sum_a=30)

assert solve(PARAMS) == CANDIDATE, solve(PARAMS)
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
