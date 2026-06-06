from sympy import *
import numpy as np

# 정의
x = symbols('x', real=True)
ln2 = log(2)

# 적분 구간
a = log(Rational(1, 2))  # ln(1/2) = -ln(2)
b = ln2  # ln(2)

# 피적분함수
f = exp(2*x)

# 정적분 계산
result = integrate(f, (x, a, b))
result_simplified = simplify(result)

# 답 (15/8)
answer = Rational(15, 8)

# 검증
if result_simplified == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: {answer}, Got: {result_simplified}')