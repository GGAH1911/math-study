# 원래 식에서 a=7, b=11 검증
a, b = 7, 11
# (3+ai)(2-i) 계산
left_real = 3*2 - a*(-1)  # 실수부: 3*2 + ai*(-i) = 6 + a
left_imag = 3*(-1) + a*2  # 허수부: 3*(-i) + ai*2 = -3 + 2a
right_real, right_imag = 13, b
if left_real == right_real and left_imag == right_imag:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')