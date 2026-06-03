from math import comb

# (x^5 + 1/x^2)^6 의 전개에서 x^2의 계수
# 일반항: C(6,k) * (x^5)^(6-k) * (1/x^2)^k = C(6,k) * x^(30-7k)
# x^2 항: 30 - 7k = 2 => k = 4

k = 4
exponent = 30 - 7*k
coefficient = comb(6, k)

if exponent == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')