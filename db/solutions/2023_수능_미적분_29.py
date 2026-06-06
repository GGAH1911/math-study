import sympy as sp
from scipy.optimize import fsolve
import numpy as np

# 원래 함수 f(x) = e^(2x) + e^x - 6
# 조건 확인: a=1, b=1, c=-6

# 조건 (가): lim(x->-inf) (f(x)+6)/e^x = 1
# f(x) + 6 = e^(2x) + e^x
# (f(x) + 6)/e^x = e^x + 1 -> 1 as x -> -inf ✓

# 조건 (나): f(ln 2) = e^(2ln2) + e^(ln2) - 6 = 4 + 2 - 6 = 0 ✓

def f(x):
    return np.exp(2*x) + np.exp(x) - 6

def g(x):
    return np.log((-1 + np.sqrt(25 + 4*x)) / 2)

# g(0) = ln(2), g(14) = ln(4) = 2*ln(2)
g0 = g(0)
g14 = g(14)

# 역함수 적분: integral_0^14 g(x)dx = 14*g(14) - 0*g(0) - integral_{g(0)}^{g(14)} f(x)dx
# = 28*ln(2) - integral_{ln 2}^{2*ln 2} (e^(2x) + e^x - 6)dx

ln2 = np.log(2)
ln4 = np.log(4)

# 부정적분: [e^(2x)/2 + e^x - 6x]
F_upper = np.exp(2*ln4)/2 + np.exp(ln4) - 6*ln4
F_lower = np.exp(2*ln2)/2 + np.exp(ln2) - 6*ln2

integral_f = F_upper - F_lower
integral_g = 14*ln4 - integral_f

# p + q*ln(2) = -8 + 34*ln(2)에 대해 검증
p_expected = -8
q_expected = 34
integral_expected = p_expected + q_expected*ln2

if abs(integral_g - integral_expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Computed: {integral_g}, Expected: {integral_expected}')