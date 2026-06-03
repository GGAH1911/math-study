from fractions import Fraction

# 구한 답: a_1 = 24, r = -1/2
a1 = 24
r = Fraction(-1, 2)

# 조건 1: sum(a_k, k=1..20) + sum(a_2k, k=1..10) = 0
sum1 = sum(a1 * (r ** (k-1)) for k in range(1, 21))
sum2 = sum(a1 * (r ** (2*k-1)) for k in range(1, 11))
cond1 = sum1 + sum2

# 조건 2: a_3 + a_4 = 3
a3 = a1 * (r ** 2)
a4 = a1 * (r ** 3)
cond2 = a3 + a4

if abs(float(cond1)) < 1e-10 and abs(float(cond2) - 3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')