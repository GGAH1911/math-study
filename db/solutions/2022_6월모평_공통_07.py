import numpy as np

# 등차수열 매개변수
a1 = 2
d = 2

# 각 항 계산
a6 = a1 + 5*d
S3 = sum(a1 + i*d for i in range(3))
S2 = sum(a1 + i*d for i in range(2))

# 조건 확인: a_6 = 2(S_3 - S_2)
cond_lhs = a6
cond_rhs = 2 * (S3 - S2)

if abs(cond_lhs - cond_rhs) < 1e-9:
    # S_10 계산
    S10 = sum(a1 + i*d for i in range(10))
    if S10 == 110:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')