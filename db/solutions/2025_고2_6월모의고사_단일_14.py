from sympy import log, sqrt, simplify, Rational
import math

# 주어진 x좌표들
log_val = log(Rational(3, 2), 2)
x_A = Rational(1, 2) * log_val
x_B = Rational(5, 2) * log_val

# 곡선 y=2^x에서 y좌표
y_A = 2 ** x_A
y_B = 2 ** x_B

# 중점 M
x_M = (x_A + x_B) / 2
y_M = (y_A + y_B) / 2

# 점 N (M을 지나는 수직선이 y=2^x와 만나는 점)
y_N = 2 ** x_M

# MN의 길이
MN_length = abs(y_N - y_M)
MN_simplified = simplify(MN_length)

# 답과 비교
expected_answer = sqrt(6) / 16
expected_simplified = simplify(expected_answer)

if simplify(MN_simplified - expected_simplified) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')