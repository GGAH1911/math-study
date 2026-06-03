import math
from sympy import *

# 원래 문제의 식
result = math.sin(math.radians(30)) * math.tan(math.radians(60))

# 정답 값
answer_value = sqrt(3) / 2

# 검증
if abs(result - float(answer_value)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')