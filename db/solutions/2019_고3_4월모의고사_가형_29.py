import sympy as sp

CANDIDATE = 11  # ★원문제 정답, 절대 바꾸지 않음

# 문제의 수학 구조
#  - 원 C1: 중심 (r1, 0), 반지름 r1  -> y축에 원점 O에서 접함
#  - 원 C2: 중심 (-r2, 0), 반지름 r2 -> y축에 원점 O에서 접함
#  - P(0, a) 에서 각 원에 그은 (y축이 아닌) 접선의 접점을 Q, R
#  - tan(∠RPQ) = tan_p / tan_q 로 주어질 때 (a-(r1+r2))^2 를 구한다.
# 파라미터로 뽑은 것: 두 원의 반지름 r1, r2, 그리고 tan θ 의 분자/분모 tan_p, tan_q.
# (r1, r2, tan_p, tan_q 모두 답을 바꾸는 실질 파라미터이다.)
PARAMS = dict(r1=1, r2=2, tan_p=4, tan_q=3)


def _tangent_point(a, r, sign):
    """중심 (sign*r, 0), 반지름 r 인 원(원점 접, y축 접)에서
    P(0,a) 로부터 그은 y축이 아닌 접선의 접점을 반환한다."""
    x = sp.symbols('x')
    # 접선 기울기 (판별식=0 으로부터 유도됨: r^2 + 2*a*m*(sign*r) ... )
    if sign > 0:
        m = (r**2 - a**2) / (2 * a * r)
    else:
        m = (a**2 - r**2) / (2 * a * r)
    circ = sp.expand((x - sign * r) ** 2 + (m * x + a) ** 2 - r ** 2)
    A = circ.coeff(x, 2)
    B = circ.coeff(x, 1)
    xt = sp.simplify(-B / (2 * A))
    yt = sp.simplify(m * xt + a)
    return xt, yt


def solve(prm):
    r1, r2 = sp.Integer(prm['r1']), sp.Integer(prm['r2'])
    p, q = sp.Integer(prm['tan_p']), sp.Integer(prm['tan_q'])

    a = sp.symbols('a', positive=True)

    xQ, yQ = _tangent_point(a, r1, +1)   # 원 C1 접점 Q
    xR, yR = _tangent_point(a, r2, -1)   # 원 C2 접점 R

    PQx, PQy = xQ, yQ - a
    PRx, PRy = xR, yR - a

    cross = PQx * PRy - PQy * PRx   # |PQ x PR| = |PQ||PR| sin theta 에 비례
    dot = PQx * PRx + PQy * PRy      # PQ . PR = |PQ||PR| cos theta 에 비례

    # tan^2(theta) = (p/q)^2 를 만족하는 a 를 구함 (부호 모호성 제거를 위해 제곱)
    eq = sp.expand(cross ** 2 * q ** 2 - dot ** 2 * p ** 2)
    sols = sp.solve(sp.Eq(eq, 0), a)

    real_pos = [s for s in sols if s.is_real and s > 0]
    if not real_pos:
        raise ValueError("실수 양의 해가 존재하지 않습니다 (문제가 성립하지 않음)")

    # 문제의 조건(a > sqrt(2) 등)은 여러 실근 중 기하학적으로 맞는 것을
    # 골라내는 역할을 한다 — 이는 항상 가장 큰 양의 실근이다.
    a_val = max(real_pos, key=lambda s: float(s))

    value = sp.simplify((a_val - (r1 + r2)) ** 2)
    if not value.is_number:
        raise ValueError("답이 수치로 확정되지 않습니다")
    value = sp.nsimplify(value)
    if value.is_Integer:
        return int(value)
    return value


def statement(prm):
    r1, r2 = prm['r1'], prm['r2']
    p, q = prm['tan_p'], prm['tan_q']
    return (
        f"그림과 같이 중심이 점 A({r1}, 0)이고 반지름의 길이가 {r1}인 원 C_1과 "
        f"중심이 점 B({-r2}, 0)이고 반지름의 길이가 {r2}인 원 C_2가 있다. "
        f"y축 위의 점 P(0, a)(a > √2)에서 원 C_1에 그은 접선 중 y축이 아닌 직선이 "
        f"원 C_1과 접하는 점을 Q, 원 C_2에 그은 접선 중 y축이 아닌 직선이 원 C_2와 "
        f"접하는 점을 R라 하고 ∠RPQ = θ라 하자.\n"
        f"tan θ = {p}/{q}일 때, (a-({r1}+{r2}))^2의 값을 구하시오."
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
