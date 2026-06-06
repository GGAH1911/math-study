import numpy as np
from sympy import Rational, sqrt, simplify

# 모집단 정보
mu = 20
sigma = 5
n = 16

# 표본평균의 기댓값
E_X = mu

# 표본평균의 표준편차
sigma_X = sigma / np.sqrt(n)

# E(X) + sigma(X) 계산
result = E_X + sigma_X

# 답값 확인
answer_exact = Rational(85, 4)
answer_decimal = float(answer_exact)

if abs(result - answer_decimal) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')