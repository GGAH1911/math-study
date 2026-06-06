import math

# 검증: α = 1/4, β = 1/2, x_1 = 256
alpha = 0.25
beta = 0.5
x_1 = 256

# 점 A가 세 조건을 만족하는지 확인
y_1_log = math.log(x_1) / math.log(4)  # log_4(x_1)
y_1_power = alpha * (x_1 ** beta)      # α*x_1^β

print(f'log_4(256) = {y_1_log}')
print(f'(1/4)*sqrt(256) = {y_1_power}')
print(f'Match: {abs(y_1_log - y_1_power) < 1e-10}')

if abs(y_1_log - y_1_power) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')