"""2026 고3 7월 미적분 30번 — 역함수 조건(단조·f'(k)=0)과 교점 x좌표의 합 (파라미터화 솔버)

문제 꼴:
    a>0, b>0 이고 모든 실수 x 에 대하여
        (f(x))^3 + f(x) = a/(x^2 + C) - b·x - c·b          (원문제 C=12, c=16/3)
    (나) f 의 역함수가 존재하고 f'(k)=0 인 실수 k 가 존재한다.
    곡선 y=f(x) 와 직선 y=-b·x 의 교점의 x좌표의 합이 k+s 일 때 (원문제 s=8),
    a×b = q/p 의 p+q 를 구하라.

수학 구조 (전부 PARAMS 에서 재유도한다)
  · g(y)=y^3+y 는 순증가 → f 의 증감은 우변의 증감과 같다.
  · 역함수 존재 + f'(k)=0  ⇔  우변' = -2ax/(x^2+C)^2 - b 가 항상 0 이하이고 x=k 에서만 0
      ⇔ b = max_x( -2ax/(x^2+C)^2 ) 이고 그 최대점이 k.
      최대점은 x = -√(C/3) 이므로  k = -√(C/3),  ρ := a/b = 8C^2 / (9√(C/3)).
      (C=12 → k=-2, ρ=64)
  · 교점: g(f(x))=g(-bx)  ⇔  a/(x^2+C) - c·b + b^3 x^3 = 0.
      양변에 (x^2+C) 를 곱하고 b 로 나누면 (a=ρb, t:=b^2)
          Q(x) = t·x^5 + C·t·x^3 - c·x^2 + E = 0,        E := ρ - c·C
      Q'(x) = x(5t x^3 + 3Ct x - 2c) 이고 괄호는 순증가라 임계점이 x=0 과 x1>0 뿐이다.
      → Q 의 실근은 **1개 또는 3개**(5개는 불가능).
        ① 실근 1개면 그 근이 곧 '교점 x좌표의 합' → x = S := k+s 가 Q 의 근 (t 에 대한 1차식).
           원문제처럼 E=0 이면 Q = x^2(t x^3 + Ct x - c) 라 근이 {0(중근), R} 이고 합이 R=S 이므로
           이 경우도 같은 식이 성립한다.
        ② 실근 3개면 5차식의 근의 합이 0 이므로 비실근 켤레쌍의 합은 -S
           → Q 가 (x^2 + S x + q) 를 인수로 가진다 (q 에 대한 3차식으로 t 가 결정된다).
  · 후보 t 마다 **실제로 서로 다른 실근의 합이 S 인지 다시 정확히 확인**한 뒤
    a×b = ρ·t 를 기약분수 q/p 로 만들어 p+q 를 돌려준다.
"""
CANDIDATE = 59
import sympy as sp

# 문제가 준 수치
PARAMS = dict(
    denom_const=12,   # a/(x^2+12) 의 12
    const_num=16,     # 우변 상수항 16b/3 의 분자
    const_den=3,      # 우변 상수항 16b/3 의 분모
    sum_offset=8,     # 교점 x좌표의 합 'k+8' 의 8
)

X = sp.Symbol('X', real=True)


def _setup(prm):
    """PARAMS → (C, c, S, E, ρ). k 와 ρ 는 (나) 조건에서 유도되는 값이라 여기서 계산한다."""
    C = sp.Integer(prm['denom_const'])
    c = sp.Rational(prm['const_num'], prm['const_den'])
    s = sp.Integer(prm['sum_offset'])
    if C <= 0 or c <= 0:
        raise ValueError('C>0, c>0 이어야 문제가 성립한다')
    x = sp.Symbol('x', real=True)
    a = sp.Symbol('a', positive=True)
    slope = -2 * a * x / (x ** 2 + C) ** 2               # 우변 도함수에서 -b 를 뺀 부분
    crit = [r for r in sp.solve(sp.diff(slope, x), x) if r.is_real]
    if not crit:
        raise ValueError('최대점이 없다')
    k = min(crit)                                        # 음수 임계점이 최댓값을 준다
    rho = sp.simplify(a / slope.subs(x, k))              # ρ = a/b
    S = sp.nsimplify(k + s)                              # 교점 x좌표의 합
    E = sp.simplify(rho - c * C)
    return C, c, S, E, rho


def _poly(t, C, c, E):
    return sp.Poly(sp.expand(t * X ** 5 + C * t * X ** 3 - c * X ** 2 + E), X)


def _sum_is(t, C, c, E, S):
    """t=b^2 일 때 Q 의 서로 다른 실근의 합이 정말 S 인지 확인 (계수가 유리수면 정확히)."""
    if not (t.is_real and t > 0):
        return False
    P = _poly(t, C, c, E)
    if all(co.is_rational for co in P.all_coeffs()):
        rts = set(P.real_roots())
        return bool(rts) and sp.simplify(sum(rts) - S) == 0
    tiny = sp.Float('1e-20')
    uniq = []
    for r in P.nroots(n=40, maxsteps=300):
        if abs(sp.im(r)) > tiny:
            continue
        rr = sp.re(r)
        if not any(abs(rr - u) < tiny for u in uniq):
            uniq.append(rr)
    return bool(uniq) and abs(sum(uniq) - S) < sp.Float('1e-15')


def _candidates(C, c, S, E, rho):
    """조건을 만족할 수 있는 t=b^2 후보들 (①실근 1개 꼴, ②실근 3개 꼴)."""
    out = []
    den = S ** 3 * (S ** 2 + C)
    if S != 0 and den != 0:                              # ① x=S 자체가 Q 의 근
        out.append(sp.nsimplify(sp.simplify((c * S ** 2 - E) / den)))
    if S != 0 and rho.is_rational:                       # ② Q 가 x^2+Sx+q 를 인수로
        q = sp.Symbol('q', real=True)
        v = C + S ** 2 - q                               # 3차 인수 x^3 - Sx^2 + vx + w
        w = -q * v / S                                   # x^1 계수 일치
        D = sp.expand(w + S * v - q * S)                 # = -c/t   (x^2 계수 일치)
        eq = sp.Poly(sp.expand(-c * q * w - E * D), q)   # x^0 계수(qw=E/t)와의 양립 조건
        if eq.degree() > 0:
            for r in eq.real_roots():
                d = D.subs(q, r)
                if d == 0:
                    continue
                out.append(sp.nsimplify(sp.simplify(-c / d)))
    return out


def solve(prm=None):
    """조건 → 답: a×b 를 기약분수 q/p 로 만들었을 때의 p+q."""
    prm = PARAMS if prm is None else prm
    C, c, S, E, rho = _setup(prm)
    for t in _candidates(C, c, S, E, rho):
        if not _sum_is(t, C, c, E, S):
            continue
        ab = sp.nsimplify(sp.radsimp(rho * t))           # a×b = (a/b)·b^2 = ρ t
        if not ab.is_rational or ab <= 0:
            continue                                     # q/p (자연수 비) 꼴이 아니면 문제가 성립 안 함
        q, p = sp.fraction(sp.Rational(ab))              # 기약분수
        return int(p + q)
    raise ValueError('이 수치 조합에서는 조건을 만족하는 b>0 (a×b=q/p) 가 없다')


def statement(prm=None):
    """같은 유형의 새 문제 문장 (유사문제 재생성용)."""
    prm = PARAMS if prm is None else prm
    C = sp.Integer(prm['denom_const'])
    c = sp.Rational(prm['const_num'], prm['const_den'])
    cs = f'\\frac{{{c.p}b}}{{{c.q}}}' if c.q != 1 else f'{c.p}b'
    return (
        'a>0, b>0 인 두 상수 a, b 에 대하여 실수 전체의 집합에서 미분가능한 함수 f(x) 가 '
        '다음 조건을 만족시킨다.\n'
        f'  (가) 모든 실수 x 에 대하여 (f(x))^3+f(x)=\\frac{{a}}{{x^2+{C}}}-bx-{cs} 이다.\n'
        '  (나) 함수 f(x) 의 역함수가 존재하고, f′(k)=0 인 실수 k 가 존재한다.\n'
        f'곡선 y=f(x) 와 직선 y=-bx 가 만나는 서로 다른 모든 점의 x좌표의 합이 k+{prm["sum_offset"]} 일 때 '
        'a×b=\\frac{q}{p} 이다. p+q 의 값을 구하시오. (단, p 와 q 는 서로소인 자연수이다.) [4점]'
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
