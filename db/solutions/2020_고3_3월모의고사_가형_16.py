from scipy.integrate import quad
import numpy as np

C = 1/8
f = lambda x: x**3 - 4*C*x

# f(1) > 0 검증
assert f(1) > 0, 'f(1) must be > 0'

# 적분 검증
def integrand(t):
    return abs(f(t))

integral, _ = quad(integrand, 0, 1)
assert np.isclose(integral, C), f'Integral {integral} != C {C}'

# 답 계산
answer = f(2)
assert np.isclose(answer, 7), f'f(2) = {answer} != 7'

print('VERIFY_PASS')