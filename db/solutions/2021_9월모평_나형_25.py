import math
from sympy import *

CANDIDATE = 41

# 주어진 조건
AB = 6
AC = 10
AD = 6  # AB = AD
BD = sqrt(15)
DC = AC - AD  # D는 AC 위의 점
assert DC == 4

# 삼각형 ABD에서 코사인 법칙으로 cos(∠BAD) 구하기
# BD² = AB² + AD² - 2·AB·AD·cos(∠BAD)
cos_BAD = (AB**2 + AD**2 - BD**2) / (2 * AB * AD)
cos_BAD_simplified = simplify(cos_BAD)
assert cos_BAD_simplified == Rational(19, 24)

# 삼각형 ABC에서 코사인 법칙으로 BC² 구하기
# BC² = AB² + AC² - 2·AB·AC·cos(∠BAC)
# ∠BAC = ∠BAD이므로
BC_squared = AB**2 + AC**2 - 2 * AB * AC * cos_BAD_simplified
BC_squared_simplified = simplify(BC_squared)

if BC_squared_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: {CANDIDATE}, Got: {BC_squared_simplified}')