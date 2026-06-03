import math

# 중복조합 계산
def comb(n, r):
    if n < r or r < 0:
        return 0
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

n = 8
lhs = comb(n + 1, 2)  # _nH_2 = _{n+1}C_2
rhs = comb(9, 2)

if lhs == rhs == 36:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')