import sympy as sp

CANDIDATE = 18  # ★절대 바꾸지 않음 (원문제 정답)

# ── 문제의 수학 구조 ──────────────────────────────────────────────
# 쌍곡선 x²/a² - y²/b² = 1 (초점 F(c,0), F'(-c,0), c=√(a²+b²)) 위,
# 제1사분면의 점 P에 대해 삼각형 PF'F의 내접원 반지름이 r일 때 OQ² 구하기.
#   a : 쌍곡선의 실반축 (원문제: 9=a² → a=3)
#   b : 쌍곡선의 허반축 (원문제: 16=b² → b=4)
#   r : 삼각형 PF'F에 내접하는 원의 반지름 (원문제: 3)
PARAMS = dict(a=3, b=4, r=3)


def solve(prm):
    a_ = sp.nsimplify(prm['a'])
    b_ = sp.nsimplify(prm['b'])
    r_ = sp.nsimplify(prm['r'])
    if a_ <= 0 or b_ <= 0 or r_ <= 0:
        raise ValueError('a, b, r 은 모두 양수여야 함')

    c_ = sp.sqrt(a_**2 + b_**2)      # 초점까지 거리
    e_ = c_ / a_                     # 이심률

    x0, y0 = sp.symbols('x0 y0', real=True)

    # (1) 오른쪽 가지 위의 점 P=(x0,y0) 에서 초점 F 까지 거리(초점반지름 공식)
    PF = e_*x0 - a_
    # (2) 쌍곡선 방정식
    eq_hyper = sp.Eq(x0**2/a_**2 - y0**2/b_**2, 1)
    # (3) 내접원 반지름 = 넓이/반둘레 = (c*y0) / (|PF|+a+c) = r
    eq_incircle = sp.Eq(r_*(PF + a_ + c_), c_*y0)

    y0_sol = sp.solve(eq_incircle, y0)
    if not y0_sol:
        raise ValueError('내접원 조건을 만족하는 y0을 구할 수 없음')
    y0_expr = y0_sol[0]

    x0_candidates = sp.solve(sp.Eq(x0**2/a_**2 - y0_expr**2/b_**2, 1), x0)

    sols = []
    for xv in x0_candidates:
        if not xv.is_real:
            continue
        yv = sp.simplify(y0_expr.subs(x0, xv))
        # 제1사분면(오른쪽 가지, x0>a, y0>0) 조건
        if xv > a_ and yv.is_real and yv > 0:
            sols.append((xv, yv))
    if not sols:
        raise ValueError('제1사분면 조건을 만족하는 점 P가 존재하지 않음(파라미터 조합이 성립하지 않음)')

    xv, yv = sols[0]

    F = (c_, sp.Integer(0))
    Fp = (-c_, sp.Integer(0))
    dPF = sp.sqrt((xv - c_)**2 + yv**2)     # |PF|
    dPFp = sp.sqrt((xv + c_)**2 + yv**2)    # |PF'|
    dFFp = 2*c_                             # |FF'|
    perim = dPF + dPFp + dFFp

    # 검산: 넓이/반둘레가 실제로 r 인지 확인
    area = c_ * yv
    if sp.simplify(area/(perim/2) - r_) != 0:
        raise ValueError('내접원 반지름 조건이 성립하지 않음')

    # 내접원의 중심(내심) 공식: 각 꼭짓점에 대변 길이를 가중치로 준 평균
    Qx = sp.simplify((dFFp*xv + dPF*Fp[0] + dPFp*F[0]) / perim)
    Qy = sp.simplify((dFFp*yv + dPF*Fp[1] + dPFp*F[1]) / perim)

    return sp.nsimplify(sp.simplify(Qx**2 + Qy**2))


def statement(prm):
    a_, b_, r_ = prm['a'], prm['b'], prm['r']
    return (
        f"두 점 F, F'을 초점으로 하는 쌍곡선 x²/{a_**2} - y²/{b_**2} = 1의 "
        f"제1사분면 위의 점을 P라 하자. 삼각형 PF'F에 내접하는 원의 반지름의 길이가 "
        f"{r_}일 때, 이 원의 중심을 Q라 하자. 원점 O에 대하여 OQ²의 값을 구하시오. "
        f"(단, 점 F의 x좌표는 양수이다.)"
    )


# a, r 을 함께 바꾸되 각각이 답을 실제로 움직인다는 것을 보여주는 조합들.
# (b는 위 기하 구조상 답에 영향이 없음이 자연스러운 결과이지만, 실제 풀이 과정에서는
#  초점 c=√(a²+b²) 계산과 P의 존재(제1사분면 조건) 판정에 쓰인다.)
VARIANTS = [
    dict(a=3, b=4, r=3),   # 원문제 → 18
    dict(a=3, b=4, r=2),   # r만 변경 → 13
    dict(a=3, b=4, r=1),   # r만 변경 → 10
    dict(a=4, b=4, r=3),   # a만 변경 → 25
    dict(a=5, b=4, r=3),   # a만 변경 → 34
]

if __name__ == '__main__':
    print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
