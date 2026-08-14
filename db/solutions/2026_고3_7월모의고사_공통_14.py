"""2026 고3 7월모의고사 공통 14 — 파라미터화 솔버.

문제 구조(파라미터: 두 변 AB, AC 와 외접원 반지름 R, ∠B 가 둔각):
  ① 사인법칙  sin B = AC/(2R),  sin C = AB/(2R)   (∠B 둔각 → cos B < 0)
  ② 좌표 배치 B(0,0), C(a,0), A(AB·cos B, AB·sin B),  a = BC = 2R·sin A
  ③ M, N 은 AB, AC 의 중점 → 원 C1(중심 M, 반지름 AB/2)·C2(중심 N, 반지름 AC/2) 는
     각각 AB, AC 를 지름으로 하는 원. 두 교점은 중심선 MN 에 대해 대칭이므로
     D = (직선 MN 에 대한 A 의 대칭점)  (= 실제로 BC 위, A 에서 내린 수선의 발)
  ④ MH = 점 M 과 직선 DN 사이의 거리
solve 는 이렇게 얻은 MH 를 보기 값들과 대조해 **보기 번호**를 돌려준다.
(보기 중 어느 것과도 맞지 않거나 삼각형이 존재하지 않으면 0)
"""
import sympy as sp

CANDIDATE = 4

PARAMS = dict(
    AB=sp.Integer(4),                       # 선분 AB 의 길이
    AC=sp.Integer(8),                       # 선분 AC 의 길이
    R=16 * sp.sqrt(15) / 15,                # 삼각형 ABC 의 외접원의 반지름
    B_obtuse=True,                          # ∠CBA > π/2
    choices=[5 * sp.sqrt(15) / 16,          # ①
             11 * sp.sqrt(15) / 32,         # ②
             5 * sp.sqrt(5) / 8,            # ③
             3 * sp.sqrt(15) / 8,           # ④
             3 * sp.sqrt(5) / 4],           # ⑤
)


def mh_length(prm):
    """조건 → 선분 MH 의 길이(정확값). 삼각형이 만들어지지 않으면 None."""
    AB, AC, R = (sp.nsimplify(prm['AB']), sp.nsimplify(prm['AC']), sp.nsimplify(prm['R']))
    sinB, sinC = sp.simplify(AC / (2 * R)), sp.simplify(AB / (2 * R))
    if sp.N(sinB) > 1 or sp.N(sinC) > 1 or sp.N(sinB) <= 0 or sp.N(sinC) <= 0:
        return None                          # 외접원이 두 변을 감당 못 함 = 그런 삼각형 없음
    cosB = sp.sqrt(1 - sinB ** 2)
    if prm.get('B_obtuse', True):
        cosB = -cosB                         # ∠CBA > π/2
    cosC = sp.sqrt(1 - sinC ** 2)            # ∠B 가 둔각이면 ∠C 는 예각
    sinA = sp.simplify(sinB * cosC + cosB * sinC)      # sin A = sin(B + C)
    if sp.N(sinA) <= 0:
        return None                          # 내각의 합 조건 위배
    a = sp.simplify(2 * R * sinA)                       # BC (사인법칙)

    A = sp.Matrix([sp.simplify(AB * cosB), sp.simplify(AB * sinB)])
    Bv = sp.Matrix([0, 0])
    Cv = sp.Matrix([a, 0])
    M = sp.simplify((A + Bv) / 2)            # 선분 AB 의 중점
    N = sp.simplify((A + Cv) / 2)            # 선분 AC 의 중점

    # 두 원의 교점 A, D 는 중심선 MN 에 대해 대칭 → D 는 직선 MN 에 대한 A 의 대칭점
    d = N - M
    t = sp.simplify((A - M).dot(d) / d.dot(d))
    D = sp.simplify(2 * (M + t * d) - A)

    # 점 M 에서 직선 DN 까지의 거리
    e = N - D
    cross = (M[0] - D[0]) * e[1] - (M[1] - D[1]) * e[0]
    return sp.simplify(sp.Abs(cross) / sp.sqrt(e.dot(e)))


def solve(prm):
    """보기 번호(1-5)를 계산해서 돌려준다. 맞는 보기가 없으면 0."""
    v = mh_length(prm)
    if v is None:
        return 0
    for i, ch in enumerate(prm['choices'], 1):
        if sp.simplify(sp.nsimplify(ch) - v) == 0:
            return i
    return 0


def statement(prm):
    """같은 유형의 새 문제 문장."""
    mark = '①②③④⑤'
    opts = ' '.join(f'{mark[i]}{sp.latex(sp.nsimplify(c))}' for i, c in enumerate(prm['choices']))
    rel = '>' if prm.get('B_obtuse', True) else '<'
    return (f"그림과 같이 \\overline{{AB}}={sp.latex(sp.nsimplify(prm['AB']))}, "
            f"\\overline{{AC}}={sp.latex(sp.nsimplify(prm['AC']))}, "
            f"∠CBA{rel}\\frac{{π}}{{2}}인 삼각형 ABC의 외접원의 반지름의 길이가 "
            f"{sp.latex(sp.nsimplify(prm['R']))}이다. 선분 AB의 중점을 M, 선분 AC의 중점을 N이라 할 때, "
            "두 점 M, N을 각각 중심으로 하고 점 A를 지나는 두 원 C_{1}, C_{2}가 있다. "
            "두 원 C_{1}, C_{2}가 만나는 점 중 A가 아닌 점을 D라 하고, "
            "점 M에서 선분 DN에 내린 수선의 발을 H라 하자. 선분 MH의 길이는?\n" + opts)


print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else f'VERIFY_FAIL: {solve(PARAMS)} != {CANDIDATE}')
