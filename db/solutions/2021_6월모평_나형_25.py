import sympy as sp
r = 2
a1 = 1
# 등비수열 항
a4 = a1 * (r ** 3)
a7 = a1 * (r ** 6)
# 합
S3 = a1 * (1 - r**3) / (1 - r)
S6 = a1 * (1 - r**6) / (1 - r)
ratio = S6 / S3
condition = 2 * a4 - 7
if abs(ratio - condition) < 1e-10 and a7 == 64:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')