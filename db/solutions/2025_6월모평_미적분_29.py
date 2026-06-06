import math
from scipy.optimize import fsolve

# 답: 55에 해당하는 p+q = 11/6
p_plus_q = 11/6

# 주어진 조건에서 p = 7/3, q = -1/2
p = 7/3
q = -1/2

# a = 1/3 - (1/2)ln(2)
a = 1/3 - 0.5 * math.log(2)
b = 1
c = 1

# 원래 함수들
def f(x):
    return (1/3)*x**3 - x**2 + math.log(1 + x**2) + a

def f_prime(x):
    return x**2 - 2*x + 2*x/(1 + x**2)

# 조건 1: 연속성 f(b) = -f(b-c)
cond1_left = f(b)
cond1_right = -f(b - c)

# 조건 2: 미분가능성 f'(b) = -f'(b-c)
cond2_left = f_prime(b)
cond2_right = -f_prime(b - c)

# 조건 3: a + b + c = p + q*ln(2)
sum_abc = a + b + c
expected = p + q * math.log(2)

# 검증
if abs(cond1_left - cond1_right) < 1e-10 and abs(cond2_left - cond2_right) < 1e-10 and abs(sum_abc - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')