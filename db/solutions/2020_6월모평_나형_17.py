from sympy import Rational, sqrt, solve, symbols

# 2020 6월모평 나형 17 (자기닮음 등비급수): lim S_n?  (보기 ②=125/12)
# 정사각형 변 4: A1(0,0),B1(4,0),C1(4,4),D1(0,4), E1=mid(C1D1)=(2,4).
# F1,G1 on y=0, x=2 대칭(반너비 3s), 높이 4, E1F1=5s: sqrt((3s)^2+16)=5s → s=1.
CANDIDATE = Rational(125, 12)
s = symbols('s', positive=True)
s0 = solve(sqrt((3 * s)**2 + 4**2) - 5 * s, s)[0]      # s = 1
A1, B1, C1, D1, E1 = (0, 0), (4, 0), (4, 4), (0, 4), (2, 4)
F1, G1 = (2 - 3 * s0, 0), (2 + 3 * s0, 0)
def inter_vert(P, Q, xv):                               # 선분 PQ ∩ 수직선 x=xv
    t = (xv - P[0]) / (Q[0] - P[0])
    return (xv, P[1] + t * (Q[1] - P[1]))
P1 = inter_vert(E1, F1, 0)                              # D1A1 (x=0) 와 E1F1
Q1 = inter_vert(G1, E1, 4)                              # B1C1 (x=4) 와 G1E1
def area(pts):
    A = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
        A += x1 * y2 - x2 * y1
    return abs(A) / 2
S1 = (area([E1, D1, P1]) + area([P1, F1, A1])
      + area([Q1, B1, G1]) + area([E1, Q1, C1]))        # R1 색칠 넓이 = 20/3
b, h = G1[0] - F1[0], E1[1]                              # 삼각형 E1F1G1: 밑변 6, 높이 4
side = b * h / (b + h)                                   # 내접 정사각형 변 = 12/5
ratio = (side / 4)**2                                    # 면적 닮음비 = 9/25
lim = S1 / (1 - ratio)
print('VERIFY_PASS' if lim == CANDIDATE else 'VERIFY_FAIL')
