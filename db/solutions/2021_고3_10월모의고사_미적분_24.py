# 조건을 만족하는 구체적 수열: a_1 = 5, a_n = 4n (n >= 2)
# 검증: sum((a_n - 4n)/n) = (5-4)/1 + 0 + 0 + ... = 1 ✓

# 극한값 검증
n = 100000
a_n = 4 * n if n != 1 else 5
limit_approx = (5*n + a_n) / (3*n - 1)

if abs(limit_approx - 3) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')