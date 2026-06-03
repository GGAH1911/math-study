from fractions import Fraction

a = Fraction(1, 6)
b = Fraction(7, 3)

# 첫 번째 식: ax + 2y - b = 0에 (2, 1) 대입
eq1_result = a * 2 + 2 * 1 - b

# 두 번째 식: 2ax + by - 3 = 0에 (2, 1) 대입
eq2_result = 2 * a * 2 + b * 1 - 3

if eq1_result == 0 and eq2_result == 0:
    answer = a + b
    if answer == Fraction(5, 2):
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')