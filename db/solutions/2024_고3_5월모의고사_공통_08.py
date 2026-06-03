import numpy as np
from fractions import Fraction

# 내 답
a_ans = Fraction(2)
b_ans = Fraction(1, 3)
ans_sum = a_ans + b_ans  # 7/3

a = float(a_ans)
b = float(b_ans)

# 원래 함수
def f(x):
    return a * np.cos(b * x)

# 조건1: 주기 6π 검증 (f(x+6π)=f(x))
xs = np.linspace(-10, 10, 2001)
period_ok = np.allclose(f(xs + 6*np.pi), f(xs), atol=1e-9)

# 조건2: [π, 4π]에서 최댓값 1
xs2 = np.linspace(np.pi, 4*np.pi, 200001)
max_val = np.max(f(xs2))
max_ok = abs(max_val - 1.0) < 1e-6

# a+b = 7/3 확인
sum_ok = ans_sum == Fraction(7, 3)

if period_ok and max_ok and sum_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
