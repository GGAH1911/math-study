import numpy as np
from fractions import Fraction
import sympy as sp

# 기호 계산
sqrt2 = sp.sqrt(2)

# 좌표
A = sp.Matrix([sp.Rational(16,3), sp.Rational(32,3)*sqrt2])
F = sp.Matrix([24, 0])
D = sp.Matrix([sp.Rational(61,3), sp.Rational(32,3)*sqrt2])
K = sp.Matrix([sp.Rational(3377,351), sp.Rational(2884,351)*sqrt2])

# 각 FKD의 탄젠트
KF = F - K
KD = D - K

# 2D 외적 (스칼라)
cross = KF[0]*KD[1] - KF[1]*KD[0]

# 내적
dot = KF[0]*KD[0] + KF[1]*KD[1]

# 탄젠트
tan_angle = sp.simplify(cross / dot)

# 형태 확인: q*sqrt(2)/p
coeff = sp.simplify(tan_angle / sqrt2)

if sp.simplify(tan_angle - (13*sqrt2/12)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')