"""2019 고3 7월모의고사 가형 26번 — 파라미터화 솔버.

[원문제] 미분가능한 f(x) 가 f(1)=0 이고, 0이 아닌 모든 실수 x 에 대해
  (x f'(x) - f(x)) / x^2 = x e^x
를 만족할 때 f(3)·f(-3) 의 값.

[수학 구조]
  좌변은 (f(x)/x)' 의 quotient-rule 전개와 같다:
      (f/x)' = (x f' - f) / x^2
  따라서 조건은 (f/x)' = g(x) 꼴의 1계 미분방정식이고
      f(x)/x = ∫ g(x) dx + C
  로 적분해 풀 수 있다. 원문제는 g(x) = x e^x (계수 c=1, 지수계수 k=1),
  경계조건은 f(a)=0 (a=1), 구하는 값은 f(p)·f(q) (p=3, q=-3).

  파라미터로 뽑은 것:
    k : g(x)=c·x·e^{k x} 의 지수 계수 (k≠0)
    c : g(x) 의 배율 상수
    a : 경계조건 f(a)=0 을 주는 점 (a≠0)
    p, q : f(p)·f(q) 를 구할 때의 평가점 두 개
  다섯 값 모두 답에 실제로 영향을 준다(아래 VERIFY 및 게이트로 확인).
"""
import sympy as sp

CANDIDATE = 72  # ★원문제 정답 — 절대 변경 금지

PARAMS = dict(k=1, c=1, a=1, p=3, q=-3)


def solve(prm):
    """조건 (x f'(x)-f(x))/x^2 = c·x·e^{kx}, f(a)=0 로부터 f(p)·f(q) 를 구한다."""
    k = sp.nsimplify(prm['k'])
    c = sp.nsimplify(prm['c'])
    a = sp.nsimplify(prm['a'])
    p = sp.nsimplify(prm['p'])
    q = sp.nsimplify(prm['q'])
    if k == 0 or a == 0:
        raise ValueError("k, a 는 0이 될 수 없습니다 (지수계수/경계점).")

    x, C = sp.symbols('x C')
    g = c * x * sp.exp(k * x)              # (f/x)' = g(x)
    h = sp.integrate(g, x) + C             # f/x = ∫g dx + C
    f_expr = x * h

    Csol = sp.solve(sp.Eq(f_expr.subs(x, a), 0), C)
    if not Csol:
        raise ValueError("경계조건 f(a)=0 을 만족하는 C가 없습니다.")
    f_expr = f_expr.subs(C, Csol[0])

    val = sp.simplify(f_expr.subs(x, p) * f_expr.subs(x, q))
    if not val.is_number or val.has(sp.zoo, sp.nan, sp.oo):
        raise ValueError(f"유효한 수치 답이 아닙니다: {val}")
    return val


def statement(prm):
    return (
        "실수 전체의 집합에서 미분가능한 함수 f(x)가 다음 조건을 만족시킨다.\n"
        f"(가) f({prm['a']})=0\n"
        "(나) 0이 아닌 모든 실수 x에 대하여\n"
        f"  (xf'(x)-f(x))/x^2 = {prm['c']}·x·e^{{{prm['k']}x}} 이다.\n"
        f"f({prm['p']}) × f({prm['q']})의 값을 구하시오."
    )


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
