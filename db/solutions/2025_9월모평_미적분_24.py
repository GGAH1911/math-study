import math

# 원래 문제의 조건 검증
# f'(x) = 1/x + 4e^(2x), f(1) = 2e^2 + 1
# 적분 결과: f(x) = ln(x) + 2e^(2x) + C, C=1

def f(x):
    return math.log(x) + 2 * math.exp(2 * x) + 1

def f_prime(x):
    return 1/x + 4 * math.exp(2 * x)

# 검증 1: f(1) == 2e^2 + 1
cond1 = abs(f(1) - (2 * math.exp(2) + 1)) < 1e-10

# 검증 2: f'(1) == 1 + 4e^2 (도함수 일치)
import numpy as np
x0 = 1.0
numerical_deriv = (f(x0 + 1e-7) - f(x0 - 1e-7)) / (2e-7)
cond2 = abs(numerical_deriv - f_prime(x0)) < 1e-5

# 검증 3: f(e) == 2e^(2e) + 2
e = math.e
fe = f(e)
expected = 2 * math.exp(2 * e) + 2
cond3 = abs(fe - expected) < 1e-6

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'f(1)={f(1)}, expected={2*math.exp(2)+1}, cond1={cond1}')
    print(f'f_prime check cond2={cond2}')
    print(f'f(e)={fe}, expected={expected}, cond3={cond3}')
