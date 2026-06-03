import numpy as np
from math import tan, pi

a = 2
b = 4

# A(3, -2)가 함수 위에 있는지 확인
y_A = a * tan((pi/4) * 3)
assert abs(y_A - (-2)) < 1e-10, f'A 검증 실패: {y_A}'

# A'(9, -2+b)가 함수 위에 있는지 확인
y_A_prime = a * tan((pi/4) * 9)
expected_y_A_prime = -2 + b
assert abs(y_A_prime - expected_y_A_prime) < 1e-10, f'A\' 검증 실패: {y_A_prime} vs {expected_y_A_prime}'

print('VERIFY_PASS')