import numpy as np
from sympy import symbols, solve, simplify

n = 8

# 첫 번째 부등식: x^2 >= 4n^2
# x <= -2n or x >= 2n

# 두 번째 부등식: x^2 - nx - 6n^2 <= 0
# (x - 3n)(x + 2n) <= 0
# -2n <= x <= 3n

# 연립부등식의 해 영역
lower_bound = -2*n  # x = -2n
upper_bound = 3*n   # x = 3n
middle_bound = 2*n  # x >= 2n

# 정수 개수 확인
count = 0
integers = []

# x = -2n
integers.append(-2*n)
count += 1

# 2n <= x <= 3n 구간의 정수
for x in range(2*n, 3*n + 1):
    # 첫 번째 조건 확인: x^2 >= 4n^2
    if x**2 >= 4*n**2:
        # 두 번째 조건 확인: x^2 - nx - 6n^2 <= 0
        if x**2 - n*x - 6*n**2 <= 0:
            integers.append(x)
            count += 1

if count == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')