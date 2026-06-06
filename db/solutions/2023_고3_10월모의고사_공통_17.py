# 미분 규칙 검증
# g(x) = (x+2)f(x)
# g'(x) = f(x) + (x+2)f'(x)
# x=3에서: g'(3) = f(3) + 5*f'(3)

f_3 = 2  # f(3) = 2
f_prime_3 = 4  # f'(3) = 4

g_prime_3 = f_3 + 5 * f_prime_3

if g_prime_3 == 22:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')