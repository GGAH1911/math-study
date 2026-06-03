import math
from sympy import sqrt, simplify, N

# 원래 문제의 식
base = 2**sqrt(3) * 4
exponent = sqrt(3) - 2
original_expr = base ** exponent

# 수치 계산
result = N(original_expr)

# 정답이 1/2인지 확인
answer = 0.5
if abs(result - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')