import math
from math import sin, pi

# 원래 방정식: 2sin²x + 3sin(x) - 2 = 0
# 모든 해
solutions = [pi/6, 5*pi/6]

# 각 해를 원래 방정식에 대입
all_valid = True
for x in solutions:
    result = 2 * sin(x)**2 + 3 * sin(x) - 2
    if abs(result) > 1e-10:
        all_valid = False
        print(f'x={x}: {result}')

# 합 검증
sum_of_solutions = sum(solutions)
expected_sum = pi

if all_valid and abs(sum_of_solutions - expected_sum) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')