# 주어진 조건
f_1 = 2
f_prime_1 = 4

# g'(x) = f(x) + (x+1)f'(x) 의 미분법
# x=1 에서:
g_prime_1 = f_1 + (1 + 1) * f_prime_1

# 답 검증
expected = 10
if g_prime_1 == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')