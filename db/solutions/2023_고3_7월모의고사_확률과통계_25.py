from fractions import Fraction

# 계산된 답
a = Fraction(1, 6)
b = Fraction(1, 3)

# 확률분포 확인
prob_sum = a + (a + b) + b
if prob_sum != 1:
    print('VERIFY_FAIL')
else:
    # E(X^2) 계산
    E_X2 = 1**2 * a + 2**2 * (a + b) + 3**2 * b
    # 조건 검증
    if E_X2 == a + 5:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')