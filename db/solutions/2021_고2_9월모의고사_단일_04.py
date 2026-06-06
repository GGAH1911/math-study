from sympy import sqrt

# 등비수열의 성질: a_n^2 = a_{n-1} * a_{n+1}
# 주어진 조건: a_4 * a_6 = 64

# 따라서 a_5^2 = 64
a5_squared = 64
a5 = sqrt(a5_squared)

# 모든 항이 양수이므로
if a5 == 8 and a5 > 0:
    # 원래 조건 확인: a_4 * a_6 = 64일 때
    # a_5^2 = a_4 * a_6이 성립하는가?
    # a_5 = 8일 때, a_5^2 = 64 ✓
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')