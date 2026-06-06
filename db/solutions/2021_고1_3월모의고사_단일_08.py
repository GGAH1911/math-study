from sympy import *

# 원래 식 계산
result = 5**3 * 6**4
print(f'5^3 × 6^4 = {result}')

# 자릿수 계산
num_digits = len(str(result))
print(f'자릿수: {num_digits}')

# 검증: 162000이 6자리 수인가?
if num_digits == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')