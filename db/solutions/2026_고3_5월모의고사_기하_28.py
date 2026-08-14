# 점 F(p·a, q·a)(a>0)을 초점으로 하고 준선이 x=-d·a인 포물선 C1,
# 점 F를 초점으로 하고 준선이 y=-d·a인 포물선 C2 라 하자.
# 두 포물선이 만나는 두 점을 A,B(BF<AF)라 할 때 OA=OA_target 이면 AF-BF는?
#
# ── 구조(파라미터로 재유도) ─────────────────────────────────────────────
# C1: (x-p a)^2+(y-q a)^2 = (x+d a)^2   ← 초점거리=준선까지 거리(둘 다 제곱해도 등가, 부호 문제 없음)
# C2: (x-p a)^2+(y-q a)^2 = (y+d a)^2
# 두 식은 a 에 대해 동차(homogeneous)이므로 a=1 로 두고 실교점 (x0,y0) 를 구하면
# 실제 교점은 (a·x0, a·y0) — a=1 에서 이미 두 실근이 항상 나온다(문제가 성립하도록
# p,q,d 가 주어졌으므로). 두 실교점 중 초점거리(FD=|점-F|)가 큰 쪽이 A, 작은 쪽이 B.
# OA = a·OA0(A의 a=1 기준 원점거리) = OA_target 로 a 를 정하고,
# AF-BF = a·(FD_A0 - FD_B0) 를 계산한다(FD 도 a 에 대해 동차라 같은 배율).
from sympy import symbols, Eq, solve as _solve, sqrt, simplify, Rational, nsimplify

CANDIDATE = 3 * sqrt(2)

# 문제가 준 수치
PARAMS = dict(
    p=3,            # F = (p·a, q·a) 의 x 계수
    q=4,            # F = (p·a, q·a) 의 y 계수
    d=5,            # 두 준선의 계수 (C1: x=-d·a, C2: y=-d·a, 동일값)
    OA_target=6,    # 주어진 조건: OA 의 길이
)


def solve(prm):
    p = nsimplify(prm['p'])
    q = nsimplify(prm['q'])
    d = nsimplify(prm['d'])
    OA_t = nsimplify(prm['OA_target'])

    x, y = symbols('x y', real=True)
    eq1 = Eq((x - p) ** 2 + (y - q) ** 2, (x + d) ** 2)   # C1 (a=1 기준)
    eq2 = Eq((x - p) ** 2 + (y - q) ** 2, (y + d) ** 2)   # C2 (a=1 기준)
    sols = _solve([eq1, eq2], [x, y], dict=True)

    pts = []
    for s in sols:
        xv, yv = simplify(s[x]), simplify(s[y])
        if xv.is_real and yv.is_real:
            pts.append((xv, yv))
    if len(pts) != 2:
        raise ValueError(f'실교점이 정확히 2개가 아님: {len(pts)}개')

    pairs = []
    for xv, yv in pts:
        fd = simplify(sqrt((xv - p) ** 2 + (yv - q) ** 2))
        pairs.append((xv, yv, fd))
    pairs.sort(key=lambda t: t[2])          # 초점거리 오름차순: [0]=B, [1]=A
    xB, yB, FDB = pairs[0]
    xA, yA, FDA = pairs[1]

    OA0 = simplify(sqrt(xA ** 2 + yA ** 2))  # a=1 기준 OA
    if OA0 == 0:
        raise ValueError('OA0=0, OA 조건으로 a 를 정할 수 없음')

    a_val = OA_t / OA0
    return simplify(a_val * (FDA - FDB))


def statement(prm):
    """같은 유형의 새 문제 문장."""
    p, q, d, OA_t = prm['p'], prm['q'], prm['d'], prm['OA_target']
    return (
        f"점 F({p}a, {q}a)(a>0)을 초점으로 하고 준선이 x=-{d}a인 포물선을 C₁, "
        f"점 F를 초점으로 하고 준선이 y=-{d}a인 포물선을 C₂라 하자. "
        f"두 포물선 C₁, C₂가 만나는 두 점을 A, B(BF<AF)라 할 때, OA={OA_t}이다. "
        f"AF-BF의 값은? (단, O는 원점이다.)"
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
