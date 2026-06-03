import numpy as np

# 원래 방정식 x^3 + x^2 + x - 3 = 0의 근
coeffs = [1, 1, 1, -3]
roots = np.roots(coeffs)

# 허근 분리
complex_roots = sorted([r for r in roots if abs(r.imag) > 1e-10], key=lambda x: x.imag)
alpha, beta = complex_roots[0], complex_roots[1]

# 원래 방정식에서 만족: alpha^2 + 2*alpha + 3 = 0, beta^2 + 2*beta + 3 = 0
check1 = abs((alpha**2 + 2*alpha + 3)) < 1e-10
check2 = abs((beta**2 + 2*beta + 3)) < 1e-10

# 계산: (alpha^2 + 2*alpha + 6) = -3 + 6 = 3
term1 = alpha**2 + 2*alpha + 6
term2 = beta**2 + 2*beta + 8
result = term1 * term2

if check1 and check2 and abs(result.real - 15) < 1e-9 and abs(result.imag) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')