"""2019 고3 4월모의고사 가형 26번 — 파라미터 솔버 (수동 작성).
문제: P(-2,k), 포물선 y²=8x(초점 F), 위의 점 Q. PQ=QF=10, 양수 k. (답 8)
구조: y²=8x → 4p=8, p=2, 초점 (2,0), 준선 x=-2 (P가 준선 위!).
      QF=초점거리=x_Q-(-2)=x_Q+2=10 → x_Q=8, y_Q=√(8·8)=8(양수).
      PQ=10이고 P가 준선 위 → P는 Q에서 준선에 내린 수선의 발 → k=y_Q=8.
재생산: (4p, dist) 파라미터화.
"""
import sympy as sp


def solve(four_p=8, dist=10):
    p = sp.Rational(four_p, 4)              # 초점 (p,0), 준선 x=-p
    xQ = dist - p                           # QF = x_Q + p = dist
    yQ = sp.sqrt(four_p * xQ)               # 포물선 위, 양수
    # P=(-p,k), PQ=dist: (xQ+p)²+(yQ-k)²=dist² → (yQ-k)²=0 → k=yQ
    assert (xQ + p) ** 2 == dist ** 2
    return yQ


CANDIDATE = 8
assert solve() == CANDIDATE, solve()
print('VERIFY_PASS')
