# 포물선 y^2=4px (초점 F(p,0), 준선 x=-p). cos∠PFF'=c 인 제1사분면 점 P.
# R = PF' 의 중점. 초점 O, F' 이고 R 을 지나는 쌍곡선. 선분 PF' 과 쌍곡선의 R 아닌 교점 Q.
# ★도형 전체가 p 에 비례하므로 p=1 로 풀어 둘레를 구한 뒤 p0 = L/(둘레) 로 되돌린다.
#   길이는 p, 넓이는 p^2 에 비례하므로 S = S1 * p0^2.
# ★쌍곡선 교점은 근호를 제곱해 t 에 대한 **1차식**이 되므로 정확·즉시 풀린다:
#   |X| = g + t·|PF'|  →  p^2 + 2t(F'·(P-F')) = g^2 + 2 g t |PF'|
#   부호 g = +gapR 이면 t=1/2 (=R), g = -gapR 이면 그 외의 교점 Q.
CANDIDATE = 216
import sympy as sp

# 문제가 준 수치만: cos∠PFF' = cos_num/cos_den, 삼각형 QOR 의 둘레, 구하는 거듭제곱 S^power
PARAMS = dict(cos_num=1, cos_den=5, perimeter=14, power=2)


def solve(prm=PARAMS):
    c = sp.Rational(prm['cos_num'], prm['cos_den'])      # cos∠PFF'
    L = sp.nsimplify(prm['perimeter'])                   # 삼각형 QOR 의 둘레
    n = sp.nsimplify(prm['power'])                       # S^n 을 답한다
    s = sp.sqrt(1 - c**2)                                # sin∠PFF' (P 는 제1사분면 → +)

    # --- p=1 로 두고 도형을 확정한다 (모든 길이는 p 에 비례) ---
    F, F2, O = sp.Matrix([1, 0]), sp.Matrix([-1, 0]), sp.Matrix([0, 0])
    # FP 의 단위벡터는 FF'(=(-1,0)) 과 각 ∠PFF' 를 이룬다 → u = (-c, s)
    r = sp.Rational(2, 1) / (1 + c)                      # 초점거리 PF = x_P + 1 에서 r(1+c)=2
    P = F + r * sp.Matrix([-c, s])
    P = sp.Matrix([sp.simplify(P[0]), sp.simplify(P[1])])
    assert sp.simplify(P[1]**2 - 4 * P[0]) == 0          # 포물선 y^2=4x 위 확인

    R = (P + F2) / 2                                     # PF' 의 중점
    d = lambda A, B: sp.sqrt(sp.simplify((A - B).dot(A - B)))
    gapR = sp.simplify(d(R, O) - d(R, F2))               # R 의 부호 있는 초점거리 차 (= ±2a)

    D = P - F2
    L1 = sp.simplify(sp.sqrt(D.dot(D)))                  # |PF'|
    dot = sp.simplify(F2.dot(D))

    def t_of(g):                                         # d(X,O) - d(X,F') = g 인 X=F'+tD 의 t
        return sp.simplify((g**2 - 1) / (2 * (dot - g * L1)))

    tQ = t_of(-gapR)                                     # R(t=1/2) 아닌 다른 가지의 교점
    if sp.simplify(tQ - sp.Rational(1, 2)) == 0:         # 축퇴 방어
        tQ = t_of(gapR)
    Q = F2 + tQ * D
    Q = sp.Matrix([sp.simplify(Q[0]), sp.simplify(Q[1])])

    per1 = sp.simplify(d(Q, O) + d(O, R) + d(R, Q))      # p=1 일 때 삼각형 QOR 의 둘레
    p0 = sp.simplify(L / per1)                           # 둘레가 L 이 되는 실제 p
    S1 = sp.Rational(1, 2) * sp.Abs(P[0] * R[1] - P[1] * R[0])   # p=1 일 때 삼각형 PRO 넓이
    return sp.simplify((S1 * p0**2) ** n)


def statement(prm=PARAMS):
    c = sp.Rational(prm['cos_num'], prm['cos_den'])
    return (f"초점이 F(p,0)(p>0)이고 준선이 x=-p인 포물선이 있다. 점 F'(-p,0)에 대하여 "
            f"cos(∠PFF')={sp.latex(c)}을 만족시키는 이 포물선 위의 점 중 제1사분면에 있는 점을 P라 하고, "
            f"선분 PF'의 중점을 R이라 하자. 두 점 O, F'을 초점으로 하고 점 R을 지나는 쌍곡선에 대하여 "
            f"선분 PF'과 쌍곡선이 만나는 점 중 R이 아닌 점을 Q라 하자. 삼각형 QOR의 둘레의 길이가 "
            f"{prm['perimeter']}일 때, 삼각형 PRO의 넓이를 S라 하자. S^{prm['power']}의 값을 구하시오. "
            f"(단, O는 원점이다.)")


print('VERIFY_PASS' if sp.simplify(solve(PARAMS) - CANDIDATE) == 0 else 'VERIFY_FAIL')
