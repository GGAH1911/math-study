from sympy import *

A = Matrix([0, 2, 2*sqrt(3)])
B = Matrix([0, 4, 0])
C = Matrix([-2, 0, 0])
D = Matrix([2, 0, 0])
H = Matrix([0, 0, 0])

# 주어진 조건 검증
assert simplify((A-B).norm() - 4) == 0
assert simplify((C-D).norm() - 4) == 0
assert simplify((B-C).norm() - 2*sqrt(5)) == 0
assert simplify((B-D).norm() - 2*sqrt(5)) == 0
assert simplify((A-H).norm() - 4) == 0
assert (H-A).dot(D-C) == 0  # AH ⊥ CD

# 평면 ABH ⊥ 평면 BCD
n_ABH = (A-H).cross(B-H)
n_BCD = Matrix([0,0,1])
assert simplify(n_ABH.dot(n_BCD)) == 0

# G = 무게중심
G = (A + B + H) / 3

# 구 S 반지름: 평면 ACD(-sqrt(3)y+z=0)까지 거리
r = simplify(Abs(-sqrt(3)*G[1] + G[2]) / 2)
assert simplify(r - Rational(2,3)*sqrt(3)) == 0

# 선분 AG를 지름으로 하는 구
M = (A + G) / 2
GM = simplify((G - M).norm())
R = simplify((A - G).norm() / 2)
assert simplify(R - r) == 0
assert simplify(GM - r) == 0

# 교원 T 반지름
rho = simplify(sqrt(r**2 - (GM/2)**2))
assert simplify(rho - 1) == 0

# 샘플 점 P = (1, 2, sqrt(3))이 T 위의 점인지 검증
P = Matrix([1, 2, sqrt(3)])
assert simplify((P-G).norm() - r) == 0  # P ∈ 구 S
assert simplify((A-P).dot(G-P)) == 0   # ∠APG = 90°

# 정사영 각도: 평면 z=√3 vs 평면 ABC
AB_v = B - A; AC_v = C - A
n_ABC = AB_v.cross(AC_v)
n_ABC_u = n_ABC / simplify(n_ABC.norm())
n_T = Matrix([0, 0, 1])
cos_alpha = simplify(Abs(n_T.dot(n_ABC_u)))
assert simplify(cos_alpha - Rational(1,4)) == 0

# 정사영 넓이
area = simplify(pi * rho**2 * cos_alpha)
if simplify(area - pi/4) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL:', area)
