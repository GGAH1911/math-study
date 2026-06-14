from scipy.integrate import quad
import numpy as np

# 조건 검증
# s(a) = -8, s(c) = -6
# integral_0_a v(t)dt = -8
# integral_0_b v(t)dt = -3
# integral_b_c v(t)dt = -3
# integral_a_b v(t)dt = 5

# 일관성 검증
integral_0_a = -8
integral_a_b = 5
integral_0_b = integral_0_a + integral_a_b
assert integral_0_b == -3, f'Expected integral_0_b = -3, got {integral_0_b}'

integral_b_c = -3
integral_0_c = integral_0_b + integral_b_c
assert integral_0_c == -6, f'Expected integral_0_c = -6, got {integral_0_c}'

# 주어진 조건 확인
assert integral_0_b == integral_b_c, 'Condition not satisfied'

# t=a부터 t=b까지 거리
distance = abs(integral_a_b)
assert distance == 5, f'Expected distance = 5, got {distance}'

print('VERIFY_PASS')