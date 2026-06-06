from fractions import Fraction

# 원래 문제의 조건
# 1. y = ax + b는 y = -2/3 * x와 평행 → a = -2/3
a = Fraction(-2, 3)

# 2. y = ax + b의 x절편이 3 → x=3일 때 y=0
# 0 = a*3 + b
b = -a * 3

# 검증: x절편이 3인지 확인
x_intercept = -b / a
if x_intercept == 3:
    result = a + b
    if result == Fraction(4, 3):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')