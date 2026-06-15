import sympy as sp
import numpy as np
from sympy import symbols, exp, integrate, diff, solve, simplify

# 변수 정의
x, t, a = symbols('x t a', real=True)

# Step 1: 원래 방정식의 양변을 x로 미분해서 f(x) 구하기
# d/dx[∫_a^x f(t)dt] = d/dx[(x+a-4)e^x]
# 좌변: f(x) (FTC)
# 우변을 미분
rhs = (x + a - 4) * exp(x)
f_x = diff(rhs, x)  # (x+a-3)e^x

# Step 2: x=a를 원래 방정식에 대입하여 a 구하기
# ∫_a^a f(t)dt = 0 = (2a-4)e^a
# 따라서 2a-4=0 → a=2
a_val = 2

# Step 3: a=2일 때 f(x) 계산
f_x_specific = f_x.subs(a, a_val)  # (x-1)e^x

# Step 4: f(a) = f(2) 계산
f_a = f_x_specific.subs(x, a_val)
print(f'f(a) = f(2) = {f_a}')
print(f'Simplified: {simplify(f_a)}')

# 검증: 원래 적분방정식이 만족되는지 확인
# ∫_2^x (t-1)e^t dt = (x-2)e^x인지 확인
integrand = (t - 1) * exp(t)
integral_result = integrate(integrand, (t, a_val, x))
rhs_check = (x + a_val - 4) * exp(x)
integral_simplified = simplify(integral_result)
rhs_simplified = simplify(rhs_check)

if simplify(integral_simplified - rhs_simplified) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')