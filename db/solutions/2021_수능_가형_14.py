#!/usr/bin/env python3
"""가형_14 역검산 — 자기유사 도형 무한등비급수.
직사각형 AB₁C₁D₁ (AB₁=2, AD₁=4). E₁=AD₁의 3:1 내분점. 내부 점 F₁: F₁E₁=F₁C₁, ∠E₁F₁C₁=π/2.
색칠=사각형 E₁F₁C₁D₁(넓이 a₁). 재귀 직사각형 AB₂C₂D₂(B₂∈AB₁, D₂∈AE₁, C₂∈E₁F₁) → 닮음비 k.
lim S_n = a₁/(1-k²). 좌표부터 전부 재계산해 441/115(보기③)인지 확인."""
import sympy as sp

# 좌표: A 좌상, AB₁=2(아래로), AD₁=4(오른쪽). A=(0,2),B₁=(0,0),C₁=(4,0),D₁=(4,2)
A = (sp.Integer(0), sp.Integer(2)); B1 = (sp.Integer(0), sp.Integer(0))
C1 = (sp.Integer(4), sp.Integer(0)); D1 = (sp.Integer(4), sp.Integer(2))

# E₁: 선분 AD₁을 3:1 내분 = A + 3/4·(D₁−A)
E1 = (A[0] + sp.Rational(3, 4) * (D1[0] - A[0]), A[1] + sp.Rational(3, 4) * (D1[1] - A[1]))  # (3,2)

# F₁: E₁C₁ 위 직각이등변 꼭짓점(∠E₁F₁C₁=π/2, F₁E₁=F₁C₁) = 중점 ± (E₁C₁의 수직벡터)/2, 내부 선택
M = ((E1[0] + C1[0]) / 2, (E1[1] + C1[1]) / 2)
d = (C1[0] - E1[0], C1[1] - E1[1])           # E₁→C₁ = (1,-2)
perp = (d[1], -d[0])                          # 수직 = (-2,-1), |perp|=|d|
cand = [(M[0] + perp[0] * sp.Rational(1, 2), M[1] + perp[1] * sp.Rational(1, 2)),
        (M[0] - perp[0] * sp.Rational(1, 2), M[1] - perp[1] * sp.Rational(1, 2))]
F1 = next(p for p in cand if 0 < p[0] < 4 and 0 < p[1] < 2)   # 직사각형 내부

# 조건 확인: 직각 + 등변
v1 = (E1[0] - F1[0], E1[1] - F1[1]); v2 = (C1[0] - F1[0], C1[1] - F1[1])
assert v1[0] * v2[0] + v1[1] * v2[1] == 0, '∠E1F1C1 ≠ 90°'
assert v1[0]**2 + v1[1]**2 == v2[0]**2 + v2[1]**2, 'F1E1 ≠ F1C1'

# a₁ = 사각형 E₁F₁C₁D₁ 넓이 (신발끈)
def shoelace(pts):
    s = sp.Integer(0)
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return sp.Abs(s) / 2
a1 = shoelace([E1, F1, C1, D1])              # 9/4

# 닮음비 k: 새 직사각형 AB₂C₂D₂ (A 공유, B₂∈AB₁, D₂∈AD₁ 방향) → C₂=(4k, 2−2k). C₂∈선분 E₁F₁.
k, t = sp.symbols('k t', positive=True)
C2 = (4 * k, 2 - 2 * k)                       # A + k·(B₁−A) + k·(D₁−A)
P = (E1[0] + t * (F1[0] - E1[0]), E1[1] + t * (F1[1] - E1[1]))   # E₁+t(F₁−E₁)
sol = sp.solve([sp.Eq(C2[0], P[0]), sp.Eq(C2[1], P[1])], [k, t], dict=True)[0]
kval = sol[k]                                # 9/14
r = kval**2                                  # 81/196

limS = sp.nsimplify(a1) / (1 - r)
limS = sp.simplify(limS)
print('VERIFY_PASS' if limS == sp.Rational(441, 115) else f'VERIFY_FAIL(a1={a1}, k={kval}, limS={limS})')
