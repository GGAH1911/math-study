import sympy as sp

x = sp.symbols('x')

CANDIDATE = 340  # ★원문제 정답, 절대 변경 금지

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 이차함수 f(x)=x^2+bx, 삼차함수 g(x)=x^3+px^2+qx (최고차항 계수 1)
#   (가) f(0)=g(0)  ⇒  두 함수의 상수항은 0
#   (나) lim_{x→0} f(x)/x = L1   ⇒  f(x) = x^2 + L1*x
#        lim_{x→a} g(x)/(x-a) = 0 ⇒  x=a 가 g의 이중근, g(0)=0과 결합해
#                                    g(x) = x(x-a)^2
#   (다) ∫_0^a {g(x)-f(x)} dx = T  ⇒  a에 대한 4차방정식
#        12T = a^4 - 4a^3 - 6*L1*a^2   (양수 a에 대해 유일해를 가짐)
#   구하는 값: M * ∫_0^a |f(x)-g(x)| dx
#
# 파라미터로 뽑아낸 것: L1 (조건 (나)의 첫 번째 극한값, 원문제는 0),
#                      T  (조건 (다)의 적분값, 원문제는 36),
#                      M  (마지막에 곱하는 계수, 원문제는 3)
# 세 값 모두 답을 실제로 바꾼다 (아래 자체 검증에서 확인).
PARAMS = dict(L1=0, T=36, M=3)


def _find_a(L1, T):
    """조건 (다)로부터 나오는 4차방정식의 유일한 양의 실근 a를 구한다."""
    a = sp.symbols('a')
    poly = a**4 - 4*a**3 - 6*L1*a**2 - 12*T
    roots = sp.Poly(poly, a).real_roots()
    pos_roots = [r for r in roots if sp.N(r) > 0]
    if len(pos_roots) != 1:
        raise ValueError(f"조건을 만족하는 양수 a가 유일하지 않습니다: {pos_roots}")
    return pos_roots[0]


def value(prm):
    """M * ∫_0^a |f(x)-g(x)| dx 를 sympy로 실제 계산해서 돌려준다."""
    L1 = sp.Rational(prm['L1'])
    T = sp.Rational(prm['T'])
    M = sp.Rational(prm['M'])

    a_val = _find_a(L1, T)

    # f(x)-g(x) = -x^3+(2a+1)x^2-(a^2-L1)x = -x*(x-r1)*(x-r2)
    h = -x**3 + (2*a_val + 1)*x**2 - (a_val**2 - L1)*x
    disc = 4*a_val + 1 + 4*L1

    pts = [sp.Integer(0), a_val]
    if sp.N(disc) >= 0:
        sqrt_disc = sp.sqrt(disc)
        r1 = ((2*a_val + 1) - sqrt_disc) / 2
        r2 = ((2*a_val + 1) + sqrt_disc) / 2
        for r in (r1, r2):
            if sp.N(0) < sp.N(r) < sp.N(a_val):
                pts.append(r)
    pts = sorted(set(pts), key=lambda v: sp.N(v))

    total = sp.Integer(0)
    for lo, hi in zip(pts, pts[1:]):
        mid = (lo + hi) / 2
        sign = 1 if sp.N(h.subs(x, mid)) >= 0 else -1
        total += sign * sp.integrate(h, (x, lo, hi))

    result = sp.simplify(M * total)
    if result.has(sp.CRootOf):
        result = sp.N(result, 15)  # 닫힌 형태가 지저분하면 수치로 정리
    else:
        result = sp.nsimplify(result)
    return result


def solve(prm):
    return value(prm)


def statement(prm):
    L1, T, M = prm['L1'], prm['T'], prm['M']
    return (
        "양수 a에 대하여 최고차항의 계수가 1인 이차함수 f(x)와 "
        "최고차항의 계수가 1인 삼차함수 g(x)가 다음 조건을 만족시킨다.\n"
        "(가) f(0)=g(0)\n"
        f"(나) lim_{{x→0}} f(x)/x = {L1}, lim_{{x→a}} g(x)/(x-a) = 0\n"
        f"(다) ∫_0^a {{g(x)-f(x)}} dx = {T}\n"
        f"{M} ∫_0^a |f(x)-g(x)| dx의 값을 구하시오."
    )


if __name__ == '__main__':
    ans = solve(PARAMS)
    print('solve(PARAMS) =', ans)
    print('VERIFY_PASS' if ans == CANDIDATE else 'VERIFY_FAIL')

    # 파라미터별로 답이 실제로 달라지는지 자체 확인
    variants = [
        dict(L1=1, T=36, M=3),
        dict(L1=0, T=10, M=3),
        dict(L1=0, T=36, M=5),
    ]
    base = solve(PARAMS)
    for v in variants:
        r = solve(v)
        print(v, '->', r, '(달라짐)' if r != base else '(동일 - 문제!)')
