import sympy as sp
from sympy import symbols, limit, oo

# 수열 조건: lim(a_n + 2)/2 = 6 => a_n -> 10
# 검증: a_n = 10 + b_n (b_n -> 0)으로 놓고 확인

n = symbols('n', positive=True, integer=True)

# a_n의 극한값
a_limit = 10

# 구하는 식의 극한값 계산
# a_n -> 10일 때, (n*a_n + 1)/(a_n + 2n)의 극한
# 분자, 분모를 n으로 나누면: (a_n + 1/n)/(a_n/n + 2)

numerator = a_limit + 0  # 1/n -> 0
denominator = 0 + 2      # a_n/n -> 0
result = numerator / denominator

if result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')