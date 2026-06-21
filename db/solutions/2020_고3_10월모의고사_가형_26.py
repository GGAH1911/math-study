import sympy as sp
from sympy import sqrt, limit, oo

CANDIDATE = 5

n = sp.Symbol('n', positive=True, integer=True)

# 거리 계산
PC_n = 3/n
OB_n = sqrt(n**2 + 9)
OA_n = n

# 극한 계산
numerator = PC_n
denominator = OB_n - OA_n

limit_value = limit(numerator / denominator, n, oo)

# 극한값이 2/3인지 확인
expected = sp.Rational(2, 3)

if limit_value == expected:
    p = 3
    q = 2
    result = p + q
    if result == CANDIDATE:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')