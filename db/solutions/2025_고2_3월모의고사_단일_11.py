import numpy as np

# z^2 + 4*conj(z) = 0의 해: z = 2 ± 2√3*i
z = 2 + 2j*np.sqrt(3)
z_conj = 2 - 2j*np.sqrt(3)

# 방정식 검증
eq_check = z**2 + 4*z_conj

# z*conj(z) 계산
result = z * z_conj

# 검증
if np.isclose(eq_check, 0) and np.isclose(result, 16):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')