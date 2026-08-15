"""2019 고3 4월모의고사 나형 24번 — 파라미터화 솔버.

원문제: (ax+1)^6 의 전개식에서 x의 계수와 x^3의 계수가 같을 때,
        양수 a에 대하여 20a^2의 값을 구하시오. (정답 6)

수학 구조:
  (ax+1)^n 의 전개식에서 x^p의 계수 = C(n,p) a^p,
                          x^q의 계수 = C(n,q) a^q  (p<q).
  두 계수가 같다는 조건 C(n,p) a^p = C(n,q) a^q 을 양수 a에 대해 풀면
  a^(q-p) = C(n,p)/C(n,q) → a 를 구하고, 마지막으로 mult*a^2 를 구한다.

파라미터화:
  n    : 이항식의 지수 (원문제 6)
  p, q : 비교하는 두 항의 차수 (원문제 x의 계수 ↔ p=1, x^3의 계수 ↔ q=3)
  mult : 최종적으로 구하는 식 mult*a^2 의 계수 (원문제 20)
"""
import sympy as sp


def value(prm):
    """조건을 만족하는 양수 a 를 구한다."""
    n, p, q = prm['n'], prm['p'], prm['q']
    a = sp.symbols('a', positive=True)
    x = sp.symbols('x')
    e = sp.expand((a * x + 1) ** n)
    cp = e.coeff(x, p)
    cq = e.coeff(x, q)
    sols = [s for s in sp.solve(sp.Eq(cp, cq), a) if s.is_real and s > 0]
    if not sols:
        raise ValueError(f'조건을 만족하는 양수 a가 없음: n={n}, p={p}, q={q}')
    return sols[0]


def solve(prm):
    a = value(prm)
    return prm['mult'] * a ** 2


def statement(prm):
    n, p, q, mult = prm['n'], prm['p'], prm['q'], prm['mult']
    return (f"다항식 (ax+1)^{n}의 전개식에서 x^{p}의 계수와 x^{q}의 계수가 같을 때, "
            f"양수 a에 대하여 {mult}a^2의 값을 구하시오.")


CANDIDATE = 6
PARAMS = dict(n=6, p=1, q=3, mult=20)

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
