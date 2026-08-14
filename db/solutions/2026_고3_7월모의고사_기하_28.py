"""2026 고3 7월모의고사 기하 28번 — 평면벡터 내적 조건 + 원 위 점의 내적 최대·최소.

유형 구조(파라미터를 바꾸면 같은 유형의 새 문제가 된다):
  직사각형 ABCD (|AB|=AB, |AD|=AD) 를 B 를 원점으로 놓는다 → A(0,AB), B(0,0), C(AD,0), D(AD,AB).
  (나) BQ→ = (cBA*BA→ + cAD*AD→)/den  로 내부의 점 Q 가 고정된다.
  (가) PA→·PQ→ = |PQ→|^2  ⟺  PQ→·QA→ = 0  즉 QP ⊥ QA — 선분 CD 위의 P 가 고정된다.
  (AR→+QR→)·(PR→+QR→) = 0  ⟺  (R-M1)·(R-M2) = 0 (M1=(A+Q)/2, M2=(P+Q)/2)
    → R 은 M1M2 를 지름으로 하는 원 위를 움직인다.
  BR→·QP→ 는 R 이 그 원 위를 돌 때 (중심)·QP ± r|QP| 사이를 훑으므로
    M+m = 2*(O-B)·QP→ (반지름 항은 상쇄된다).
"""
import sympy as sp

CANDIDATE = 5

PARAMS = dict(
    AB=6,                              # 직사각형의 세로 |AB| (A와 B를 잇는 변)
    AD=8,                              # 직사각형의 가로 |AD|
    cBA=2,                             # 조건 (나): BQ→ = (cBA*BA→ + cAD*AD→)/den
    cAD=3,
    den=10,
    choices=[sp.Rational(226, 5), sp.Rational(236, 5), sp.Rational(246, 5),
             sp.Rational(256, 5), sp.Rational(266, 5)],   # 5지선다 보기 값
)


def configure(prm):
    """조건 (가)·(나)로 결정되는 점들을 좌표로 계산한다.

    문항이 성립하지 않으면(P 가 선분 CD 를 벗어나거나 Q 가 직사각형 내부가 아니면) None.
    """
    h, w = sp.nsimplify(prm['AB']), sp.nsimplify(prm['AD'])
    if h <= 0 or w <= 0:
        return None
    A = sp.Matrix([0, h])
    B = sp.Matrix([0, 0])
    C = sp.Matrix([w, 0])
    D = sp.Matrix([w, h])

    # 조건 (나): Q 의 위치벡터
    BA, AD = A - B, D - A
    Q = B + (sp.nsimplify(prm['cBA']) * BA + sp.nsimplify(prm['cAD']) * AD) / sp.nsimplify(prm['den'])
    if not (0 < Q[0] < w and 0 < Q[1] < h):
        return None                                  # Q 가 직사각형 내부가 아니면 문항 미성립

    # 조건 (가): P=(w,p) 는 선분 CD 위. PA→·PQ→=|PQ→|^2 ⟺ PQ→·QA→=0
    t = sp.Symbol('p', real=True)
    P = sp.Matrix([w, t])
    sol = sp.solve(sp.Eq((Q - P).dot(A - Q), 0), t)
    if len(sol) != 1:
        return None
    pv = sp.nsimplify(sol[0])
    if not pv.is_real or not (0 <= pv <= h):
        return None                                  # P 가 선분 CD 위에 없으면 문항 미성립
    P = sp.Matrix([w, pv])

    # 검산: 원래 형태 PA→·PQ→ = |PQ→|^2
    assert sp.simplify((A - P).dot(Q - P) - (Q - P).dot(Q - P)) == 0
    return dict(A=A, B=B, C=C, D=D, P=P, Q=Q)


def extreme_values(prm):
    """BR→·QP→ 의 최댓값 M, 최솟값 m 을 구한다 (R 은 지름 M1M2 인 원 위)."""
    g = configure(prm)
    if g is None:
        return None
    A, B, P, Q = g['A'], g['B'], g['P'], g['Q']
    M1 = (A + Q) / 2                                  # AR→+QR→ = 2(R-M1)
    M2 = (P + Q) / 2                                  # PR→+QR→ = 2(R-M2)
    O = (M1 + M2) / 2                                 # 원의 중심
    r = sp.sqrt((M2 - M1).dot(M2 - M1)) / 2           # 반지름
    QP = P - Q
    base = (O - B).dot(QP)
    span = r * sp.sqrt(QP.dot(QP))
    return sp.simplify(base + span), sp.simplify(base - span)


def sum_value(prm):
    """M+m 의 값(보기와 대조할 값)."""
    mm = extreme_values(prm)
    return None if mm is None else sp.nsimplify(sp.simplify(mm[0] + mm[1]))


def solve(prm):
    """조건 → 정답 보기 번호. 계산값이 보기에 없으면 0(문항 미성립)."""
    v = sum_value(prm)
    if v is None:
        return sp.Integer(0)
    for i, c in enumerate(prm['choices'], 1):
        if sp.simplify(sp.nsimplify(c) - v) == 0:
            return i
    return sp.Integer(0)


def make_choices(prm, step=2, shift=4):
    """계산값을 포함하는 등차 보기 5개(유사문제 생성용). 기본은 정답이 ⑤에 오도록."""
    v = sum_value(prm)
    return None if v is None else [sp.nsimplify(v) + step * (k - shift) for k in range(5)]


def statement(prm):
    marks = ['①', '②', '③', '④', '⑤']
    opts = ' '.join(f'{m} {sp.latex(sp.nsimplify(c))}' for m, c in zip(marks, prm['choices']))
    coef = lambda k: '' if prm[k] == 1 else str(prm[k])
    return (
        f"좌표평면에 |AB|={prm['AB']}, |AD|={prm['AD']}인 직사각형 ABCD가 있다. "
        "선분 CD 위의 한 점 P와 직사각형 ABCD 내부의 한 점 Q가 다음 조건을 만족시킨다.\n"
        "(가) PA→·PQ→ = |PQ→|^2\n"
        f"(나) BQ→ = ({coef('cBA')}BA→ + {coef('cAD')}AD→)/{prm['den']}\n"
        "(AR→+QR→)·(PR→+QR→)=0을 만족시키는 점 R에 대하여 "
        "BR→·QP→의 최댓값을 M, 최솟값을 m이라 할 때, M+m의 값은? [4점]\n" + opts
    )


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
