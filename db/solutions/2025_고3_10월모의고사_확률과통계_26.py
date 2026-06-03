import numpy as np

# 답: σ = 5/4
sigma = 5/4
a = 0.245

# 첫 번째 조건 검증 (n=100)
n1 = 100
margin_1 = 1.96 * (sigma / np.sqrt(n1))
if not np.isclose(margin_1, a):
    print('VERIFY_FAIL')
    exit()

# 두 번째 조건 검증 (n=25)
n2 = 25
margin_2 = 1.96 * (sigma / np.sqrt(n2))
expected_margin_2 = a + 0.245
if not np.isclose(margin_2, expected_margin_2):
    print('VERIFY_FAIL')
    exit()

print('VERIFY_PASS')