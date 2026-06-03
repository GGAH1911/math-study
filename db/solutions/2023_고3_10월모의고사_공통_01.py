from sympy import sqrt, simplify, N
import math

# 원래 식
expr = 2**sqrt(2) * (1/2)**(sqrt(2)-1)

# 숫자값으로 계산
result = N(expr)
print(f'계산값: {result}')

# 답이 2인지 확인
if abs(float(result) - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')