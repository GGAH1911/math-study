# 원래 문제 조건 검증
m = 11
n = 115

# 조건 1: m × n = 1265
product_check = (m * n == 1265)

# 조건 2: m은 두 자리 자연수
two_digit_check = (10 <= m <= 99)

# 조건 3: n은 세 자리 자연수
three_digit_check = (100 <= n <= 999)

if product_check and two_digit_check and three_digit_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')