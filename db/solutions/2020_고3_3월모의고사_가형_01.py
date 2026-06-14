from math import isclose

# 원래 식 계산: 8^(4/3) × 2^(-2)
result = (8 ** (4/3)) * (2 ** (-2))
expected_answer = 4

# 부동소수점 오차 범위 내에서 비교
if isclose(result, expected_answer, rel_tol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')