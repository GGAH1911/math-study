from sympy import *

a1, a2, a3 = Integer(3), Integer(0), 3*sqrt(3)
b1, b2, b3 = Integer(0), 2*sqrt(6), 2*sqrt(3)

# 구 위에 있는지
assert simplify(a1**2 + a2**2 + a3**2 - 36) == 0, 'A not on sphere'
assert simplify(b1**2 + b2**2 + b3**2 - 36) == 0, 'B not on sphere'

# a3 양수, 6 아님
assert a3 > 0 and simplify(a3 - 6) != 0

# 조건 (가): C = 2/3 A, B_z = C_z
c3 = Rational(2,3)*a3
assert simplify(b3 - c3) == 0, '(가) failed'

# BC가 xy평면과 평행 (BC 방향벡터 z성분 0)
assert simplify(c3 - b3) == 0

# 조건 (나): |AB| = 6
AB2 = (b1-a1)**2 + (b2-a2)**2 + (b3-a3)**2
assert simplify(AB2 - 36) == 0, '(나) |AB|=6 failed'

# 정사영 직각삼각형: O에서 직각
dot = a1*b1 + a2*b2
assert simplify(dot) == 0, 'orthogonality in projection failed'

# 법선벡터
OA = Matrix([a1, a2, a3])
OB = Matrix([b1, b2, b3])
n = OA.cross(OB)

# cos theta
cos_theta = Abs(n[2]) / n.norm()
cos_theta_s = simplify(cos_theta)

expected = sqrt(2)/3
if simplify(cos_theta_s - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('Got:', cos_theta_s)
