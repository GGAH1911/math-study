import math
from sympy import *

# 답 검증
a = Rational(4) ** (Rational(1, 3))  # a = 4^(1/3)
k = Rational(1, 4)

# 각 점의 좌표
x_A = 1 - log(4, a)
x_B = 0
x_C = 1 - log(k, a)
x_D = 1 - log(k, 4)

# 평행사변형 조건: x_D - x_A = x_C - x_B
cond1 = simplify(x_D - x_A - (x_C - x_B))

# 넓이 조건
area = abs(x_B - x_A) * abs(4 - k)
area_simplified = simplify(area)

# 4ak 계산
result = 4 * a * k
result_simplified = simplify(result)

# 검증
if simplify(cond1) == 0 and simplify(area_simplified - Rational(15, 2)) == 0 and simplify(result_simplified - 2**(Rational(2, 3))) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')