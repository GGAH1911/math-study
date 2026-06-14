from sympy import log, simplify, nsimplify

CANDIDATE = 2

# 원래 식 계산
result = log(54, 3) + log(1/36, 9)

# 수치로 확인
numerical_result = float(result.evalf())

if abs(numerical_result - CANDIDATE) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')