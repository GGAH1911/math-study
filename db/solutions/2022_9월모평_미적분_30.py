import numpy as np
from scipy.optimize import fsolve

# f(x) = 9x^3 - 9x^2 + 3
def f(x):
    return 9*x**3 - 9*x**2 + 3

def f_prime(x):
    return 27*x**2 - 18*x

# 검증 1: f'(0) = 0
assert abs(f_prime(0)) < 1e-10, 'f\'(0) != 0'

# 검증 2: f(0)은 정수
assert abs(f(0) - 3) < 1e-10, 'f(0) != 3'

# 검증 3: 극댓값 × 극솟값 = 5
f_max = f(0)
f_min = f(2/3)
assert abs(f_max * f_min - 5) < 1e-10, 'product != 5'

# 검증 4: f(1) = f(0) (연속성)
assert abs(f(1) - f(0)) < 1e-10, 'f(1) != f(0)'

# 검증 5: 조건 (가) - lim_{x->0} sin(pi*f(x))/x = 0
# f'(0) = 0이므로 극한 = pi*cos(pi*f(0))*f'(0) = 0
assert abs(f_prime(0)) < 1e-10

# 검증 6: 적분값
from scipy.integrate import quad

# int_0^1 f(u) du
int_f, _ = quad(f, 0, 1)
assert abs(int_f - 9/4) < 1e-10

# int_0^1 u*f(u) du  
int_uf = lambda x: x * f(x)
int_uf_val, _ = quad(int_uf, 0, 1)
assert abs(int_uf_val - 21/20) < 1e-10

# int_0^5 x*g(x) dx = 5*int_0^1 u*f(u) + 10*int_0^1 f(u)
integral_result = 5 * int_uf_val + 10 * int_f
assert abs(integral_result - 111/4) < 1e-10

# p=4, q=111이 서로소인지 확인
import math
assert math.gcd(4, 111) == 1

print('VERIFY_PASS')