import sympy as sp
from sympy import sqrt, Rational

# 점들의 좌표
A = (Rational(9,4), Rational(5,4)*sqrt(7))
B = (0, 0)
C = (6, 0)
D = (2, 0)
E = (Rational(20,11), Rational(-10,11)*sqrt(7))

# 외접원 검증
center = (3, sqrt(7)/7)
R_sq = Rational(64,7)

# A, B, C가 외접원 위에 있는지 확인
dist_A = (A[0] - center[0])**2 + (A[1] - center[1])**2
dist_B = (B[0] - center[0])**2 + (B[1] - center[1])**2
dist_E = (E[0] - center[0])**2 + (E[1] - center[1])**2

assert sp.simplify(dist_A - R_sq) == 0, "A not on circle"
assert sp.simplify(dist_B - R_sq) == 0, "B not on circle"
assert sp.simplify(dist_E - R_sq) == 0, "E not on circle"

# D에서 CE로의 수선의 발 F
F = (Rational(527,176), Rational(-115,176)*sqrt(7))

# DF가 CE에 수직인지 확인
DF = (F[0] - D[0], F[1] - D[1])
CE = (E[0] - C[0], E[1] - C[1])
dot_product = DF[0]*CE[0] + DF[1]*CE[1]
assert sp.simplify(dot_product) == 0, "DF not perpendicular to CE"

# FC의 길이
FC_sq = (C[0] - F[0])**2 + (C[1] - F[1])**2
FC_sq_simplified = sp.simplify(FC_sq)
assert FC_sq_simplified == Rational(529, 44), f"FC^2 should be 529/44, got {FC_sq_simplified}"

FC = sp.sqrt(Rational(529, 44))
FC_simplified = sp.simplify(FC)
assert FC_simplified == Rational(23,22)*sqrt(11), f"FC should be 23*sqrt(11)/22, got {FC_simplified}"

print('VERIFY_PASS')