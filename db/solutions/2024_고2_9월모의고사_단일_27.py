from fractions import Fraction
from math import gcd
from sympy import Rational, simplify

CANDIDATE = 271

# ==================== 문제 조건 인코딩 ====================
# 평행사변형 ABCD: 둘레=20, cos(∠ABC)=1/4
# 삼각형ABC 외접원 넓이 = (32/3)π
# AB < AD 조건: a < b 설정

# [1] cos(∠ABC) = 1/4에서 sin(∠ABC) 계산
cos_ABC = Rational(1, 4)
sin_ABC_squared = 1 - cos_ABC**2
assert sin_ABC_squared == Rational(15, 16), "sin²(∠ABC) 계산 오류"

# [2] 삼각형ABC 외접원 반지름 제약
# 넓이 = πR² = (32/3)π => R² = 32/3
R_ABC_squared = Rational(32, 3)

# [3] 사인 법칙으로 AC 길이
# AC = 2R·sin(∠ABC) => AC² = 4R²·sin²(∠ABC)
AC_squared = 4 * R_ABC_squared * sin_ABC_squared
AC_squared = simplify(AC_squared)
assert AC_squared == 40, f"AC² 계산 오류: {AC_squared} != 40"

# [4] a, b 결정 (a=AB, b=AD=BC)
# 둘레 조건: 2(a+b) = 20 => a+b = 10
# 코사인 법칙: AC² = a² + b² - 2ab·cos(∠ABC)
# 40 = a² + b² - ab/2
# a² + b² = (a+b)² - 2ab = 100 - 2ab 대입:
# 40 = 100 - 2ab - ab/2 = 100 - 5ab/2
# => ab = 24

ab_product = 24
a_plus_b_sum = 10

# t² - 10t + 24 = 0 => (t-4)(t-6) = 0
# a < b 조건에서: a = 4, b = 6
a = 4
b = 6

assert a + b == a_plus_b_sum, "a+b 조건 위반"
assert a * b == ab_product, "ab 조건 위반"
assert a < b, "a < b 조건 위반"

AC_verify = a**2 + b**2 - a*b*Rational(1, 2)
assert AC_verify == 40, f"코사인 법칙 검증 오류: {AC_verify} != 40"

# [5] 삼각형ABD 외접원 계산
# 평행사변형에서 ∠DAB = 180° - ∠ABC
# sin(∠DAB) = sin(∠ABC), cos(∠DAB) = -cos(∠ABC)

sin_DAB_squared = sin_ABC_squared  # = 15/16
cos_DAB = -cos_ABC  # = -1/4

# 코사인 법칙: BD² = a² + b² - 2ab·cos(∠DAB)
BD_squared = a**2 + b**2 - 2*a*b*cos_DAB
BD_squared = simplify(BD_squared)
assert BD_squared == 64, f"BD² 계산 오류: {BD_squared} != 64"

# [6] 삼각형ABD 외접원 반지름
# 사인 법칙: 2R_ABD = BD / sin(∠DAB)
# R_ABD² = BD² / (4·sin²(∠DAB))

R_ABD_squared = BD_squared / (4 * sin_DAB_squared)
R_ABD_squared = simplify(R_ABD_squared)
assert R_ABD_squared == Rational(256, 15), f"R_ABD² 계산 오류: {R_ABD_squared} != 256/15"

# [7] 외접원 넓이에서 p, q 추출
# 외접원 넓이 = π·R² = (256/15)π = (q/p)π
# => q = 256, p = 15

q = 256
p = 15

assert gcd(p, q) == 1, f"p, q 서로소 조건 위반: gcd({p}, {q}) != 1"

# [8] 최종 답 계산
answer = p + q

# ==================== 검증 ====================
if answer == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")