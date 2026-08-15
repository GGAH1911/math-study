"""
2019 고3 7월모의고사 가형 19번 파라미터화 솔버

[문제 구조]
직육면체 ABCD-EFGH: 밑면 ABCD는 정사각형(한 변 a, 미지수), 높이 AE = h.
  A(0,0,0), B(a,0,0), C(a,a,0), D(0,a,0), E(0,0,h), F(a,0,h), G(a,a,h), H(0,a,h)

BC 위의 점 P=(a,t,0), EF 위의 점 Q=(s,0,h) 에 대해, P를 밑면 EFGH(z=h) 위로
정사영한 점 P'=(a,t,h) 와 H, Q 가 이루는 삼각형(=삼각형 PHQ의 정사영)이
한 변의 길이 L 인 정삼각형이 되도록 a,s,t 가 결정된다:
    a^2+(a-t)^2 = L^2   (P'H)
    s^2+a^2     = L^2   (HQ)
    (a-s)^2+t^2 = L^2   (QP')
→ a,s,t 는 모두 L에 비례하는 값으로 유일하게 정해진다(비율 t/a, s/a 는 L과 무관한 상수).

삼각형 EQH(=E(0,0,h),Q(s,0,h),H(0,a,h))는 밑면 z=h 위에 놓이므로 넓이 = a*s/2.
이를 실제 3차원 평면 PHQ 위로 정사영한 넓이가 문제의 값이며,
θ 를 평면 PHQ 와 밑면(z=h) 사이의 각이라 하면 정사영 넓이 = (a*s/2)*cosθ 이고,
cosθ 는 평면 PHQ의 법선벡터 n 의 z성분을 이용해 cosθ = |n_z| / |n| 로 구한다.

이 값은 L 이 정해지면 h(=높이)와 결합하여 유일하게 정해지는데(둘 다 답에 실제로
영향을 준다 — h 만 바꿔도, L 만 바꿔도 정사영 넓이가 달라짐을 아래에서 직접 확인함),
객관식 보기가 항상 "공차 1/3 인 등차수열 5개(1/3,2/3,1,4/3,5/3)"로 고정되어 나오는
문제 유형이라, 아무 L,h 조합이나 넣으면 값이 그 보기 범위를 벗어나 "문제로 성립하지
않을" 수 있다(규칙 6에 따라 그 경우 예외를 던진다). L,h 가 서로 결합되어 있어(비율
h/L 을 원문제와 같게 유지해야 값이 보기 범위 안의 "깔끔한" 값이 됨) 자유롭게 한쪽만
흔들 수 없는 전형적인 결합 파라미터 문제이므로, 성립하는 (L,h) 조합을 VARIANTS 로
제시한다(규칙 5).
"""
import sympy as sp

CANDIDATE = 4  # 원문제 정답 보기 번호(④, 값 4/3) — 절대 바꾸지 않음

PARAMS = dict(L=4, h=sp.sqrt(15))


def _geometry(L, h):
    """정사영 정삼각형 조건으로 a,s,t 를 구하고, 삼각형 EQH 의
    평면 PHQ 위로의 정사영 넓이(값 V)를 반환한다."""
    a, s, t = sp.symbols('a s t', positive=True)
    eqs = [
        sp.Eq(a**2 + (a - t)**2, L**2),   # 정사영 삼각형 변 P'H = L
        sp.Eq(s**2 + a**2, L**2),          # 정사영 삼각형 변 HQ  = L
        sp.Eq((a - s)**2 + t**2, L**2),    # 정사영 삼각형 변 QP' = L
    ]
    sols = sp.solve(eqs, [a, s, t], dict=True)
    if not sols:
        raise ValueError('정사영 정삼각형 조건을 만족하는 a,s,t 해가 없습니다')
    so = sols[0]
    A, S, T = so[a], so[s], so[t]

    P = sp.Matrix([A, T, 0])
    H = sp.Matrix([0, A, h])
    Q = sp.Matrix([S, 0, h])
    n = (H - P).cross(Q - P)
    magn = sp.sqrt(n.dot(n))
    if sp.simplify(magn) == 0:
        raise ValueError('P, H, Q 가 한 평면(직선)을 이루지 않아 평면 PHQ가 정의되지 않습니다')
    cos_theta = sp.simplify(sp.Abs(n[2]) / magn)
    area_EQH = sp.simplify(A * S / 2)
    return sp.simplify(area_EQH * cos_theta)


def value(prm):
    """삼각형 EQH 의 평면 PHQ 위로의 정사영 넓이(수학적 값)."""
    return sp.nsimplify(_geometry(prm['L'], prm['h']))


def choices(prm):
    """이 문제 유형이 강제하는 고정 보기: 공차 1/3 인 등차수열 5개
    (①1/3 ②2/3 ③1 ④4/3 ⑤5/3). 문항 형태가 강제하는 고정 창(window)이라
    prm 값과 무관하다(2019_고3_10월모의고사_가형_01.py 의 {1..5} 방식과 동일 패턴)."""
    return (sp.Rational(1, 3), sp.Rational(2, 3), sp.Integer(1),
            sp.Rational(4, 3), sp.Rational(5, 3))


def solve(prm):
    """값이 보기 중 몇 번째(1-based)인지 반환 — 객관식 정답 번호.
    값이 고정 보기 범위를 벗어나면 이 유형의 문제로 성립하지 않으므로 예외를 던진다."""
    v = value(prm)
    ch = choices(prm)
    if v not in ch:
        raise ValueError(f'값 {v} 이(가) 보기 범위 {ch} 를 벗어남 — 문제로 성립하지 않음')
    return ch.index(v) + 1


def statement(prm):
    L, h = prm['L'], prm['h']
    return (
        f"그림과 같이 \\overline{{AB}}=\\overline{{AD}} 이고 \\overline{{AE}}={sp.latex(h)} 인 "
        f"직육면체 ABCD-EFGH가 있다. 선분 BC 위의 점 P와 선분 EF 위의 점 Q에 대하여 "
        f"삼각형 PHQ의 평면 EFGH 위로의 정사영은 한 변의 길이가 {L}인 정삼각형이다. "
        f"삼각형 EQH 의 평면 PHQ 위로의 정사영의 넓이는?"
    )


# L,h 는 결합 파라미터: 비율 h/L 을 원문제와 같게(=sqrt(15)/4) 유지한 채 L 만
# 바꾸면 정사영 넓이가 L^2 에 비례해 바뀌고(도형의 닮음), 그중 아래 조합들은
# 값이 고정 보기 범위 안의 "깔끔한" 값으로 떨어져 문제로 성립한다.
# → ①1/3 ②2/3 ③1 ④4/3(=원문제) ⑤5/3 를 각각 재현하며, 서로 다른 정답 번호를 낸다.
_r0 = sp.sqrt(15) / 4  # 원문제의 높이/변 비율 h/L
VARIANTS = [
    dict(L=2, h=sp.simplify(2 * _r0)),                    # 값 1/3  → ①
    dict(L=2 * sp.sqrt(2), h=sp.simplify(2 * sp.sqrt(2) * _r0)),  # 값 2/3  → ②
    dict(L=2 * sp.sqrt(3), h=sp.simplify(2 * sp.sqrt(3) * _r0)),  # 값 1    → ③
    dict(L=2 * sp.sqrt(5), h=sp.simplify(2 * sp.sqrt(5) * _r0)),  # 값 5/3  → ⑤
]

# 원문제 보기와 유도된 보기가 일치하는지 고정
assert choices(PARAMS) == (sp.Rational(1, 3), sp.Rational(2, 3), sp.Integer(1),
                            sp.Rational(4, 3), sp.Rational(5, 3))

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
