# AB 를 지름으로 하는 구 S. C,D 는 S 위, A,B,C,D 는 평면 α 위, AD=BC(=a), CD<AB.
# 지름에 대한 원주각이 직각이므로 α∩S 는 AB 를 지름으로 하는 원이고 ∠ADB=∠ACB=π/2 → BD=AC=√(AB²-a²).
# (가) P 의 α 정사영이 선분 BD 위 · (나) 평면 PAD 와 α 의 예각의 탄젠트제곱이 TAN2
# → 평면 PAB 와 평면 PBC 의 예각 θ 에 대해 cos²θ = q/p (기약), 답 = p+q.
CANDIDATE = 52
import sympy as sp

# 문제가 준 수치만 담는다 (BD·AC·CD 등은 solve 가 유도한다).
PARAMS = dict(
    AB_COEF=10,   # AB = AB_COEF * √AB_RAD  (원문제: 10√5)
    AB_RAD=5,
    AD=10,        # AD = BC
    TAN2=1,       # 조건 (나) 의 예각의 tan² (π/4 → 1, π/3 → 3, π/6 → 1/3)
)


def _geom(prm):
    """조건 → 좌표 (A,B,C,D,P) 를 실제로 구성한다."""
    a = sp.nsimplify(prm['AD'])
    c = sp.nsimplify(prm['AB_COEF']) * sp.sqrt(sp.nsimplify(prm['AB_RAD']))   # AB
    T2 = sp.nsimplify(prm['TAN2'])
    if not (sp.simplify(c**2 - 2*a**2) > 0 and T2 > 0):
        return None                      # CD>0 (C≠D, 같은 쪽) 이 깨지면 문제가 성립하지 않는다
    d = sp.sqrt(sp.simplify(c**2 - a**2))                 # ∠ADB=π/2 → BD = AC

    # α 를 xy평면으로: A 를 원점, AB 를 x축. D,C 는 AB 를 지름으로 하는 원 위 (같은 반평면).
    A = sp.Matrix([0, 0, 0])
    B = sp.Matrix([c, 0, 0])
    D = sp.Matrix([a**2/c, a*d/c, 0])                     # AD=a, ∠ADB=π/2
    C = sp.Matrix([c - a**2/c, a*d/c, 0])                 # BC=a, ∠ACB=π/2, CD<AB
    O = (A + B)/2
    R = c/2
    for X, want in ((D, a), (C, d)):                      # AD=a, AC=d 확인
        assert sp.simplify(sp.sqrt((X - A).dot(X - A)) - want) == 0
    assert sp.simplify(sp.sqrt((C - B).dot(C - B)) - a) == 0
    assert sp.simplify(sp.sqrt((C - D).dot(C - D)) - (c - 2*a**2/c)) == 0
    for X in (C, D):
        assert sp.simplify(sp.sqrt((X - O).dot(X - O)) - R) == 0    # 구 위

    # (가) 정사영 F 는 선분 BD 위: F = B + t(D-B), 0<t<1
    t = sp.Symbol('t', real=True)
    F = B + t*(D - B)
    # (나) 평면 PAD 와 α 가 이루는 각: 교선이 AD 이므로 F 에서 직선 AD 까지 거리 h 에 대해 tan²=z²/h²
    u = (D - A)/a
    w = F - A
    h2 = sp.simplify(w.dot(w) - w.dot(u)**2)
    z2 = sp.simplify(T2*h2)
    # P 가 구 위: |F-O|² + z² = R²
    roots = sp.solve(sp.Eq(sp.simplify((F - O).dot(F - O)) + z2, R**2), t)
    cand = [sp.nsimplify(r) for r in roots if r.is_real and 0 < r < 1
            and sp.simplify(z2.subs(t, r)) > 0]
    if not cand:
        return None
    tv = cand[0]
    P = sp.Matrix([F[0].subs(t, tv), F[1].subs(t, tv), sp.sqrt(sp.simplify(z2.subs(t, tv)))])
    return A, B, C, D, P


def solve(prm):
    """조건 → p+q (cos²θ = q/p, 기약)."""
    g = _geom(prm)
    if g is None:
        return None
    A, B, C, D, P = g
    n1 = (A - P).cross(B - P)                 # 평면 PAB 의 법선
    n2 = (B - P).cross(C - P)                 # 평면 PBC 의 법선
    cos2 = sp.nsimplify(sp.radsimp(sp.simplify(n1.dot(n2)**2/(n1.dot(n1)*n2.dot(n2)))))
    q, p = sp.fraction(sp.cancel(cos2))
    q, p = sp.Integer(q), sp.Integer(p)
    assert sp.gcd(p, q) == 1 and p > 0 and q > 0
    return int(p + q)


def statement(prm):
    """같은 유형의 새 문제 문장."""
    rad = sp.nsimplify(prm['AB_RAD'])
    ab = f"{prm['AB_COEF']}" if rad == 1 else f"{prm['AB_COEF']}\\sqrt{{{rad}}}"
    T2 = sp.nsimplify(prm['TAN2'])
    ang = {sp.Integer(1): '\\frac{\\pi}{4}', sp.Integer(3): '\\frac{\\pi}{3}',
           sp.Rational(1, 3): '\\frac{\\pi}{6}'}.get(T2, f'\\arctan\\sqrt{{{T2}}}')
    return (f"공간에 \\overline{{AB}}={ab} 인 선분 AB 를 지름으로 하는 구 S 가 있다. "
            f"구 S 위의 두 점 C, D 에 대하여 네 점 A, B, C, D 는 평면 α 위에 있고, "
            f"\\overline{{AD}}=\\overline{{BC}}={prm['AD']} 이다. 구 S 위의 점 P 가 다음 조건을 만족시킨다. "
            f"(가) 점 P 의 평면 α 위로의 정사영은 선분 BD 위에 있다. "
            f"(나) 평면 PAD 와 평면 α 가 이루는 예각의 크기는 {ang} 이다. "
            f"평면 PAB 와 평면 PBC 가 이루는 예각의 크기를 θ 라 할 때 cos^2θ=\\frac{{q}}{{p}} 이다. "
            f"p+q 의 값을 구하시오. (단, \\overline{{CD}}<\\overline{{AB}} 이고 p 와 q 는 서로소인 자연수이다.)")


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
