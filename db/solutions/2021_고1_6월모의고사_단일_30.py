import cmath
import numpy as np

# omega = e^(2πi/3)
omega = cmath.exp(2j * cmath.pi / 3)

# 검증할 n 값들
test_cases = [18, 20]

for n in test_cases:
    # (1+ω)(1+ω²)...(1+ωⁿ) 계산
    product = 1.0 + 0j
    for k in range(1, n+1):
        product *= (1 + omega**k)
    
    # 64와 같은지 확인
    result = abs(product - 64.0) < 1e-9 and abs(product.imag) < 1e-9
    print(f'n={n}: product = {product:.10f}, equals 64? {result}')

# 최종 답 검증
if abs(product - 64.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')