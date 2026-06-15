import numpy as np
from scipy import integrate

# 두 함수 정의
def f1(x):
    return np.sin(x) * np.log(x)

def f2(x):
    return np.cos(x) / x

def integrand(x):
    return f1(x) - f2(x)

# 수치 적분으로 검증
result, error = integrate.quad(integrand, np.pi/2, np.pi)
expected = np.log(np.pi)

print(f'수치 적분 결과: {result}')
print(f'예상값 ln(π): {expected}')
print(f'차이: {abs(result - expected)}')

if abs(result - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')