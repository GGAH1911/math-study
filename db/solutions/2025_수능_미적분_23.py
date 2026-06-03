import sympy as sp
import numpy as np

# 변수 정의
x = sp.Symbol('x')

# 원래 문제의 함수
f = 3*x**2 / sp.sin(x)**2

# 극한 계산
limit_result = sp.limit(f, x, 0)

print(f'극한값: {limit_result}')
if limit_result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')