import numpy as np
from scipy import integrate

CANDIDATE = 340

# h(x) = sqrt(2x) + 1
def h(x):
    return np.sqrt(2*x) + 1

# 단면의 넓이 A(x) = h(x)^2
def A(x):
    return h(x)**2

# 부피 계산
V_numerical, _ = integrate.quad(A, 0, 2)

# 해석적 계산
# V = ∫(2x + 2√(2x) + 1)dx from 0 to 2
# = [x^2 + (2/3)(2x)^(3/2) + x] from 0 to 2
at_2 = 4 + (2/3)*(4)**(3/2) + 2
V_analytical = at_2

result_30V = 30 * V_analytical

if abs(result_30V - CANDIDATE) < 0.01:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')