"""2019 고3 4월모의고사 가형 26번 — 파라미터화 솔버.

문제 구조:
  포물선 y^2 = (four_p)x, 초점 F(p,0), 준선 x=-p  (four_p = 4p)
  점 P(-p, k) : P의 x좌표가 "우연히" 준선과 같다는 것이 이 문제의 핵심 트릭.
  Q는 포물선 위의 점, PQ = QF = dist (두 거리가 같은 공통 값).

  포물선의 초점-준선 성질: QF = x_Q + p  →  x_Q = dist - p.
  Q가 포물선 위 → y_Q = sqrt(four_p * x_Q)  (양수 값 선택).

  P가 준선 위에 있으므로, Q에서 준선까지의 거리(=QF)는 PQ의 하한이고,
  등호(PQ = QF)는 P가 Q에서 준선에 내린 수선의 발일 때만 성립한다.
  즉 PQ = QF 라는 조건이 곧 k = y_Q 를 강제한다 — 이것이 답을 만드는 기하 논증.

파라미터로 뽑은 것:
  four_p : 포물선 계수(=4p). 바뀌면 초점·준선·x_Q·y_Q 모두 바뀌어 답이 바뀐다.
  dist   : 공통 거리 PQ=QF. 바뀌면 x_Q, y_Q(=답)가 바뀐다.
두 파라미터가 서로 얽혀 있진 않고(전제: dist > p, four_p > 0) 각각 답을 실제로 바꾼다.
"""
import sympy as sp


def solve(prm):
    four_p = sp.nsimplify(prm['four_p'])   # 포물선 y^2 = four_p * x 의 계수 (=4p)
    dist = sp.nsimplify(prm['dist'])       # PQ = QF = dist

    if four_p <= 0:
        raise ValueError('four_p 는 양수여야 포물선이 오른쪽으로 열린다')

    p = four_p / 4                          # 초점 F(p,0), 준선 x=-p
    xQ = dist - p                           # QF = x_Q + p = dist (초점-준선 성질)
    if xQ < 0:
        raise ValueError('x_Q < 0 이면 포물선 위에 그런 점 Q가 존재하지 않는다')

    yQ = sp.sqrt(four_p * xQ)               # Q가 포물선 위, y_Q>0 (편의상 위쪽 점 선택)

    # P(-p, k)는 준선 위의 점 → Q에서 준선까지 거리 = QF = x_Q + p.
    # 이는 항상 PQ의 하한이며, PQ = QF(등호) 는 PQ가 준선에 수직(수평 방향)일 때,
    # 즉 P가 Q에서 준선에 내린 수선의 발일 때만 성립한다 → k = y_Q.
    if sp.simplify((xQ + p) - dist) != 0:
        raise ValueError('QF = dist 조건이 깨졌다')

    return sp.nsimplify(yQ)


def statement(prm):
    four_p = prm['four_p']
    dist = prm['dist']
    p = sp.Rational(four_p, 4)
    return (
        f"좌표평면에서 점 P(-{p}, k)와 초점이 F인 포물선 y^2 = {four_p}x "
        f"위의 점 Q에 대하여 \\overline{{PQ}}=\\overline{{QF}}={dist}일 때, "
        f"양수 k의 값을 구하시오."
    )


PARAMS = dict(four_p=8, dist=10)
CANDIDATE = 8

print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
