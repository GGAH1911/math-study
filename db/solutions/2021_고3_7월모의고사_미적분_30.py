import numpy as np
from scipy.integrate import quad

# 조건: a=9, b=1
a, b = 9, 1

# f(x) = ax^2 + b
def f(x):
    return a*x**2 + b

# 적분 계산: ∫₀⁹ e^x(9x²+1)dx
def integrand(x):
    return np.exp(x) * f(x)

result, _ = quad(integrand, 0, a)

# 예상값: me^a - 19 with m=586
expected = 586 * np.exp(a) - 19

print(f'적분값: {result}')
print(f'예상값(m=586): {expected}')
print(f'오차: {abs(result - expected)}')

if abs(result - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')