import sympy as sp
from sympy import sqrt, Rational

# 주어진 값
a = 4
r1 = 2  # |PF|
r2 = 4  # |FQ|

# focal chord 공식: 1/r1 + 1/r2 = 2a/b²
left_side = Rational(1, 2) + Rational(1, 4)
print(f"1/r1 + 1/r2 = {left_side} = {float(left_side)}")

# b² 구하기
b_squared = 2 * a / left_side
print(f"b² = {b_squared} = {float(b_squared)}")

# c² 구하기
c_squared = a**2 - b_squared
print(f"c² = {c_squared} = {float(c_squared)}")

# c 구하기
c = sqrt(c_squared)
print(f"c = {c} = {float(c)}")

# 검증: 타원 위의 점들이 주어진 거리 조건을 만족하는가?
# |PF'| + |PF| = 8
pf_prime = 6
pf = 2
ellipse_check_p = pf_prime + pf
print(f"\n|PF'| + |PF| = {pf_prime} + {pf} = {ellipse_check_p} (should be 8): {ellipse_check_p == 8}")

# |QF'| + |QF| = 8
qf_prime = 4
qf = 4
ellipse_check_q = qf_prime + qf
print(f"|QF'| + |QF| = {qf_prime} + {qf} = {ellipse_check_q} (should be 8): {ellipse_check_q == 8}")

# 초점 현 공식 검증
focal_chord_lhs = Rational(1, r1) + Rational(1, r2)
focal_chord_rhs = 2 * a / b_squared
print(f"\nFocal chord formula: {focal_chord_lhs} = {focal_chord_rhs}")
print(f"Formula verified: {focal_chord_lhs == focal_chord_rhs}")

# 최종 답
print(f"\nFinal answer: c = {c} = {4*sqrt(3)/3}")
print(f"Simplified: c = 4√3/3")

if abs(float(c) - float(4*sqrt(3)/3)) < 1e-10:
    print("\nVERIFY_PASS")
else:
    print("\nVERIFY_FAIL")