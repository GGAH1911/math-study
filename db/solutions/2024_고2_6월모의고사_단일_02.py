import math

# 원래 문제식
value1 = math.log(24, 3)
value2 = math.log(3/8, 3)
result = value1 + value2

# 로그 합 성질 검증
product = 24 * (3/8)
result_combined = math.log(product, 3)

print(f'log_3(24) = {value1}')
print(f'log_3(3/8) = {value2}')
print(f'합: {result}')
print(f'log_3(24 * 3/8) = log_3(9) = {result_combined}')
print(f'3^2 = 9, log_3(9) = 2')

if abs(result - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')