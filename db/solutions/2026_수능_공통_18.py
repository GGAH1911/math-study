import math
from sympy import sqrt, simplify, Rational

# 주어진 조건
AB = 5
AC = 6
cos_BAC = Rational(-3, 5)

# sin(∠BAC) 계산
sin_BAC_squared = 1 - cos_BAC**2
sin_BAC = sqrt(sin_BAC_squared)

# 삼각형 넓이 공식
area = Rational(1, 2) * AB * AC * sin_BAC
area_simplified = simplify(area)

# 정답 확인
if area_simplified == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')