"""2019 고3 10월모의고사 가형 29번 — 파라미터화 솔버.

원문제: 좌표공간의 세 점 A(-1,0,6), B(2,-√3,0), C(3,0,0)에 대하여
두 점 P, Q가 |AP|=2, |CQ|=2√3, BC·CQ=6 을 만족시킨다. |PQ|의 최댓값을 구하시오. (답 12)

[수학 구조]
  - P는 중심 A, 반지름 rAP 인 구 위의 점 → {P : |AP|=rAP}.
  - Q는 중심 C, 반지름 rCQ 인 구 위의 점이면서, 동시에 BC·CQ = k 라는
    평면 조건(법선벡터 BC, 상수 k)을 만족 → 구와 평면의 교선인 "원" 위의 점.
    · 축방향 거리 d = k / |BC|  (BC 방향 단위벡터 ub = BC/|BC| 사용 시
      cosθ = k/(|BC|·rCQ), d = rCQ·cosθ)
    · 원의 중심 Oc = C + d·ub, 반지름 rc = rCQ·√(1-cosθ²)  (|d|≤rCQ 이어야 실원)
  - max|PQ| = rAP + max|AQ| (Q가 원 위를 움직일 때 A에서 가장 먼 점을 잡음)
    · AO = A - Oc, 축방향 성분 h = AO·ub, 평면내 성분 ρ = √(|AO|²-h²)
    · max|AQ| = √(h² + (ρ+rc)²)

  ⇒ 답을 실제로 좌우하는 파라미터: rAP(=|AP|), rCQ(=|CQ|), k(=BC·CQ),
    그리고 세 점 A,B,C의 좌표. 이 중 rAP, rCQ, k 세 개를 PARAMS 로 노출한다.
"""
import sympy as sp


def _fmt(v):
    """sympy 수를 문제 문장에 쓸 LaTeX 문자열로 변환."""
    v = sp.nsimplify(v)
    return sp.latex(v)


def _fmt_point(name, coords):
    return f"{name}({', '.join(_fmt(c) for c in coords)})"


PARAMS = dict(
    A=(-1, 0, 6),
    B=(2, -sp.sqrt(3), 0),
    C=(3, 0, 0),
    rAP=2,              # |AP|
    rCQ=2 * sp.sqrt(3),  # |CQ|
    k=6,                # BC·CQ
)

CANDIDATE = 12  # ★원문제 정답, 절대 변경 금지


def solve(prm):
    A = sp.Matrix([sp.nsimplify(x) for x in prm['A']])
    B = sp.Matrix([sp.nsimplify(x) for x in prm['B']])
    C = sp.Matrix([sp.nsimplify(x) for x in prm['C']])
    rAP = sp.nsimplify(prm['rAP'])
    rCQ = sp.nsimplify(prm['rCQ'])
    k = sp.nsimplify(prm['k'])

    BC = C - B
    BCnorm = sp.sqrt(BC.dot(BC))
    if BCnorm == 0:
        raise ValueError("B와 C가 같은 점이라 BC 방향을 정의할 수 없습니다.")
    ub = BC / BCnorm

    # BC·CQ = |BC||CQ|cosθ = k  →  cosθ = k / (|BC|rCQ)
    cos = k / (BCnorm * rCQ)
    cos = sp.simplify(cos)
    if sp.simplify(cos**2 - 1) > 0:
        # cos 값이 [-1,1] 범위를 벗어나면 구와 평면이 만나지 않는다 (조건 모순)
        raise ValueError("주어진 조건으로는 구와 평면이 만나지 않아 Q가 존재하지 않습니다.")

    d = rCQ * cos                       # C에서 원의 중심까지 축방향 거리
    Oc = C + d * ub                     # 원의 중심
    rc = rCQ * sp.sqrt(1 - cos**2)      # 원의 반지름

    AO = A - Oc
    h = AO.dot(ub)                      # 축방향(평면 법선방향) 성분
    rho_sq = sp.simplify(AO.dot(AO) - h**2)
    if sp.simplify(rho_sq) < 0:
        raise ValueError("계산 중 음수 제곱근이 발생했습니다 (파라미터 불일치).")
    rho = sp.sqrt(rho_sq)               # 평면 내 성분(투영점-원중심 거리)

    max_AQ = sp.sqrt(h**2 + (rho + rc)**2)
    ans = sp.simplify(rAP + max_AQ)
    ans = sp.nsimplify(sp.radsimp(sp.simplify(ans)))
    if not ans.is_number:
        raise ValueError("답이 수치로 정리되지 않았습니다.")
    return sp.simplify(ans)


def statement(prm):
    A, B, C = prm['A'], prm['B'], prm['C']
    rAP, rCQ, k = prm['rAP'], prm['rCQ'], prm['k']
    return (
        f"좌표공간의 세 점 {_fmt_point('A', A)}, {_fmt_point('B', B)}, "
        f"{_fmt_point('C', C)}에 대하여 두 점 P, Q가\n"
        f"|AP|={_fmt(rAP)}, |CQ|={_fmt(rCQ)}, BC·CQ={_fmt(k)}\n"
        f"을 만족시킨다. |PQ|의 최댓값을 구하시오."
    )


if __name__ == '__main__':
    result = solve(PARAMS)
    print(statement(PARAMS))
    print('solve(PARAMS) =', result)
    print('VERIFY_PASS' if result == CANDIDATE else 'VERIFY_FAIL')
