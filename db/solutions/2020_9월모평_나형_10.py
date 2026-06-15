import sympy as sp
import numpy as np

# 부등식 검증
# sqrt(9n^2 + 4) < sqrt(na_n) < 3n + 2
# 양변 제곱: 9n^2 + 4 < na_n < (3n+2)^2 = 9n^2 + 12n + 4

n = sp.Symbol('n', positive=True, integer=True)

# a_n의 범위
left_bound = (9*n**2 + 4) / n
right_bound = (9*n**2 + 12*n + 4) / n

# a_n/n의 범위
left_ratio = left_bound / n
right_ratio = right_bound / n

# 정리
left_simplified = sp.simplify(left_ratio)
right_simplified = sp.simplify(right_ratio)

# 극한 계산
limit_left = sp.limit(left_simplified, n, sp.oo)
limit_right = sp.limit(right_simplified, n, sp.oo)

# 답 검증
if limit_left == 9 and limit_right == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')