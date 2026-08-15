"""2019 고3 4월모의고사 나형 30번 — 파라미터화 솔버.

원문제: f(x)=ax+b, g(x)=1/(ax+b-2)+3.
  (가) x>0 일 때 1<g(x)<3
  (나) y=f(x) 와 y=1/(x-2)+3 의 교점이 제4사분면 위에 있지 않다.
  영역 R={(a,b)} 에서 a²+b² 의 최댓값 M, 100M 의 값 (답 306)

수학 구조 파라미터화:
  g(x)=1/(ax+b-c)+d  는 "쌍곡선 y=1/(x-c)+d 에 f(x) 를 대입한 것"이다 — 조건 (나)의
  쌍곡선과 (가)의 쌍곡선이 같은 c(수직 점근선), d(수평 점근선) 로 묶여 있다.
    c : 쌍곡선의 수직 점근선 x 좌표         (원문제 2)
    d : 쌍곡선의 수평 점근선 y 좌표          (원문제 3)
    k : (가)의 상한 hi=d, 하한 lo=d-k 를 정하는 폭 (원문제 1<g<3 은 k=2)
    mult : "이 M의 값을 구하시오" 앞에 곱해지는 배수  (원문제 100)

  풀이 구조(모두 sympy 로 계산):
    (가) x>0, lo<g(x)<hi(=d) ⟺ a<0, b ≤ c-1/k =: bmax   (t=ax+b-c 의 상한 분석)
    쌍곡선이 y=0 을 지나는 점(코너) x0 = c-1/d 를 sympy.solve 로 구한다.
    최댓점은 b=bmax, 직선이 코너 (x0,0) 을 지나는 경우 → sympy.solve 로 a 결정.
    M=a²+b², 답 = mult*M. 이때 (나) 가 실제로 지켜지는지(교점이 Q4에 없는지)
    ax²+Bx+C=0 의 실근을 sympy.solve 로 구해 검증한다.
"""
import sympy as sp

CANDIDATE = 306

# 문제를 정하는 값들: c(수직 점근선), d(수평 점근선), k((가)의 폭), mult(구하는 배수)
PARAMS = dict(c=2, d=3, k=2, mult=100)


def solve(prm):
    c = sp.Rational(prm['c'])
    d = sp.Rational(prm['d'])
    k = sp.Rational(prm['k'])
    mult = sp.Rational(prm['mult'])
    if k <= 0 or d == 0:
        raise ValueError('k>0, d≠0 이어야 (가)의 폭·점근선이 정의된다')

    x = sp.symbols('x', real=True)
    a, b = sp.symbols('a b', real=True)

    # (가) x>0, d-k < g(x) < d ⟺ a<0, b<=bmax  (t=ax+b-c 를 x>0에서 분석해 나오는 상한)
    bmax = c - 1 / k

    # 쌍곡선 y=1/(x-c)+d 가 y=0 을 지나는 코너점 — 제4사분면 진입 경계
    corner = [s for s in sp.solve(sp.Eq(1 / (x - c) + d, 0), x) if s.is_real]
    if not corner:
        raise ValueError('쌍곡선이 x축과 만나지 않아 (나)의 경계 코너가 없다')
    x0 = corner[0]
    if x0 == 0:
        raise ValueError('코너점이 원점 — 퇴화된 조합')

    # 최댓점: b=bmax, 직선이 코너 (x0,0) 을 통과 (a*x0+b=0) 하는 순간이 a²+b² 최댓값
    b_val = bmax
    a_val = sp.solve(sp.Eq(a * x0 + b_val, 0), a)[0]
    if not (a_val < 0):
        raise ValueError('a<0 조건이 깨짐 — 이 파라미터 조합은 문제로 성립하지 않는다')
    if x0 <= 0:
        raise ValueError('코너점이 x<=0 — (나)의 제4사분면 구조가 성립하지 않는다')

    # (나) 검증: (a_val*x+b_val - d)(x-c) = 1 의 실근이 실제로 제4사분면(x>0,y<0)에 없는지 확인
    B = b_val - d - a_val * c
    C = -c * (b_val - d) - 1
    roots = sp.solve(sp.Eq(a_val * x ** 2 + B * x + C, 0), x)
    for r in roots:
        if r.is_real and sp.simplify(r - c) != 0:
            y = a_val * r + b_val
            if r > 0 and y < 0:
                raise ValueError('최댓점 후보에서 (나) 위배 — 코너-접촉 가정이 이 조합엔 안 맞음')

    M = a_val ** 2 + b_val ** 2
    return sp.nsimplify(mult * M)


def statement(prm):
    c, d, k, mult = prm['c'], prm['d'], prm['k'], prm['mult']
    lo, hi = d - k, d
    return (
        f"두 실수 a, b에 대하여 두 함수\n"
        f"  f(x)=ax+b,\n"
        f"  g(x)=1/(ax+b-{c})+{d}\n"
        f"이 다음 조건을 만족시키도록 하는 두 실수 a, b의 순서쌍 (a, b)를 좌표평면에\n"
        f"나타낸 영역을 R라 하자.\n"
        f"(가) x > 0일 때, {lo} < g(x) < {hi}\n"
        f"(나) 두 함수 y = f(x)와 y = 1/(x-{c})+{d}의 그래프의 교점이 제4사분면 위에는\n"
        f"있지 않다.\n"
        f"영역 R에 속하는 점 (a, b)에 대하여 a^2+b^2의 최댓값을 M이라 할 때, {mult}M의\n"
        f"값을 구하시오. (단, a ≠ 0)"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
