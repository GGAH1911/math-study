import numpy as np

# 삼차방정식 x^3 + x^2 - 2 = 0 의 근
roots = np.roots([1, 1, 0, -2])

# 허근 찾기
complex_roots = [r for r in roots if abs(np.imag(r)) > 1e-10]

if len(complex_roots) > 0:
    root = complex_roots[0]
    a = np.real(root)
    b = np.imag(root)
    
    # 원래 방정식에 대입하여 검증
    result = root**3 + root**2 - 2
    
    if abs(result) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')