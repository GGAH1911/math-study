import sympy as sp
import numpy as np

# 변수 정의
x = sp.Symbol('x', real=True)
a_val = 1

# 원래 함수: y = 2^(-x+a) + a
def f(x_val, a):
    return 2**(-x_val + a) + a

# a=1일 때, 함수는 f(x) = 2^(-x+1) + 1
result = f(1, a_val)

# 역함수의 그래프가 (a+1, 1)을 지나려면
# 원래 함수가 (1, a+1)을 지나야 함
expected = a_val + 1

if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')