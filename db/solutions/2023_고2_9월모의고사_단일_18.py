from fractions import Fraction

p = Fraction(3)
q = Fraction(2)

# 두 곡선이 (4,2)에서 만나는지 확인 (log2 계산)
import math
cond1 = math.isclose(math.log2(4), 2)
cond2 = math.isclose(math.log2(4 - p) + q, 2)

# 각 점 x좌표
xA = Fraction(1)
xB = p + Fraction(1, 4)  # 2^(-2) = 1/4
xC = Fraction(8)
xD = p + Fraction(2)     # 2^(3-2) = 2

CD = xC - xD
BA = xB - xA

diff = CD - BA

if cond1 and cond2 and diff == Fraction(3, 4) and p + q == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')