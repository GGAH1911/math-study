import numpy as np
from sympy import *

# a = sqrt(3), b = 1/6
a = sqrt(3)
b = Rational(1, 6)

# 점 (2, 3) 검증
x1 = 2
y1_expected = 3
y1_actual = a * tan(b * pi * x1)
y1_actual_simplified = simplify(y1_actual)
print(f'Point (2,3): Expected={y1_expected}, Actual={float(y1_actual_simplified)}')
assert abs(float(y1_actual_simplified) - 3.0) < 1e-10, f'Point (2,3) failed: {y1_actual_simplified}'

# 점 (8, 3) 검증
x2 = 8
y2_expected = 3
y2_actual = a * tan(b * pi * x2)
y2_actual_simplified = simplify(y2_actual)
print(f'Point (8,3): Expected={y2_expected}, Actual={float(y2_actual_simplified)}')
assert abs(float(y2_actual_simplified) - 3.0) < 1e-10, f'Point (8,3) failed: {y2_actual_simplified}'

# a^2 * b 계산
answer = a**2 * b
answer_simplified = simplify(answer)
print(f'a^2 * b = {answer_simplified}')
assert answer_simplified == Rational(1, 2), f'Answer verification failed: {answer_simplified}'

print('VERIFY_PASS')