from sympy import symbols, Eq, solve
a1 = 7
d = 3
# 일반항 a_n = a1 + (n-1)*d, n=7
n = 7
a7 = a1 + (n-1)*d
CANDIDATE = 25
if a7 == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')