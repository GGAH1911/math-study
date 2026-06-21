"""2022 예시 미적분 26 — 무한등비급수 넓이.
직사각형 OA1B1C1 (OA1=√3, OC1=1). B1C1 위 D1: B1D1=2·C1D1.
부채꼴 B1D1E1(중심 B1, 반지름 B1D1=2√3/3) + 부채꼴 C1C2D1(중심 C1, 반지름 C1D1=√3/3) = 색칠.
같은 방법 반복 → lim S_n.
★haiku 오답(③, r=2/3 가정)을 정정: 실제 닮음비 r=(3-√3)/3.
"""
import sympy as sp

r3 = sp.sqrt(3)
O = sp.Point(0, 0); A1 = sp.Point(0, r3); B1 = sp.Point(1, r3); C1 = sp.Point(1, 0)

# C1D1 = √3/3, B1D1 = 2√3/3 (B1D1 = 2·C1D1, 합 = √3)
C1D1 = r3/3; B1D1 = 2*r3/3
D1 = sp.Point(1, C1D1)                       # B1C1(x=1) 위, C1에서 √3/3
E1 = sp.Point(0, 2*r3/3)                     # 원(B1, 2√3/3) ∩ OA1(x=0)
C2 = sp.Point(1 - r3/3, 0)                   # 원(C1, √3/3) ∩ OC1(y=0)

# 반지름 검증
assert sp.simplify(B1.distance(D1) - B1D1) == 0
assert sp.simplify(B1.distance(E1) - B1D1) == 0
assert sp.simplify(C1.distance(D1) - C1D1) == 0
assert sp.simplify(C1.distance(C2) - C1D1) == 0

def central_angle(c, p, q):
    v1 = sp.Matrix([p.x - c.x, p.y - c.y]); v2 = sp.Matrix([q.x - c.x, q.y - c.y])
    return sp.acos(sp.simplify(v1.dot(v2) / (v1.norm() * v2.norm())))

th_B = sp.simplify(central_angle(B1, D1, E1))   # π/3
th_C = sp.simplify(central_angle(C1, C2, D1))   # π/2
assert th_B == sp.pi/3 and th_C == sp.pi/2, (th_B, th_C)

S_B = sp.Rational(1, 2) * B1D1**2 * th_B        # 2π/9
S_C = sp.Rational(1, 2) * C1D1**2 * th_C        # π/12
S1 = sp.simplify(S_B + S_C)                     # 11π/36

# 닮음비: 새 직사각형 OA2B2C2. C2가 가로변 위 → OC2 = 1-√3/3. 세로 OA2는 B2가 호 D1E1 위라는 조건.
# (OC2-1)^2 + (OA2-√3)^2 = (2√3/3)^2  →  OA2 = √3-1
OA2 = r3 - 1
B2 = sp.Point(C2.x, OA2)
assert sp.simplify(B1.distance(B2) - B1D1) == 0          # B2가 호 위
r = sp.simplify(C2.x / C1.x)                              # 가로비 (3-√3)/3
assert sp.simplify(OA2/r3 - r) == 0                       # 세로비 = 가로비 → 닮음
ratio2 = sp.simplify(r**2)                                # (4-2√3)/3

S = sp.simplify(S1 / (1 - ratio2))                        # 무한등비급수 합
expected = sp.simplify((1 + 2*r3)/12 * sp.pi)            # ⑤

print("S1 =", S1)
print("닮음비 r =", r, "  r^2 =", ratio2, "  1-r^2 =", sp.simplify(1-ratio2))
print("S = lim S_n =", S)
print("정답 ⑤ (1+2√3)/12·π =", expected)
if sp.simplify(S - expected) == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")
