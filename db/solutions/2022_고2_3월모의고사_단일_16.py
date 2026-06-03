import numpy as np
from numpy.polynomial import Polynomial

# k = -2일 때 방정식 x^3 - x^2 - kx + k = 0
k = -2
coeffs = [k, -k, -1, 1]  # k - kx - x^2 + x^3 형태
roots = np.roots([1, -1, -k, k])  # x^3 - x^2 - kx + k

# 근 확인
print('Roots:', roots)

# 실수인 근 찾기
real_roots = [r.real for r in roots if abs(r.imag) < 1e-10]
imaginary_roots = [r for r in roots if abs(r.imag) >= 1e-10]

print('Real roots:', real_roots)
print('Imaginary roots:', imaginary_roots)

# 조건에 맞게 할당
alpha = imaginary_roots[0]  # ia
beta = 1  # 실수
gamma = imaginary_roots[1]  # -ia

# 조건 검증
alpha_squared = alpha**2
minus_2_beta = -2*beta
print(f'alpha^2 = {alpha_squared}')
print(f'-2*beta = {minus_2_beta}')
print(f'alpha^2 == -2*beta: {np.isclose(alpha_squared, minus_2_beta)}')

# 답 계산
result = beta**2 + gamma**2
print(f'beta^2 + gamma^2 = {result}')
print(f'Real part: {result.real}')
print(f'Imaginary part (should be ~0): {result.imag}')

if np.isclose(result.real, -1) and abs(result.imag) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')