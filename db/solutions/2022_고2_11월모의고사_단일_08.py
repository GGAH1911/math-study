import sympy as sp
import numpy as np

# 답: a = 1/8
a = sp.Rational(1, 8)

# 함수 정의
def f(x, a_val):
    return sp.log(3*x + 1, a_val) + 2

# x=5에서 함수값 계산
x_min = 5
f_min = f(x_min, a)
print(f'f(5) = {f_min}')
print(f'f(5) simplified = {sp.simplify(f_min)}')

# 최솟값이 2/3인지 확인
expected_min = sp.Rational(2, 3)
if sp.simplify(f_min - expected_min) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')