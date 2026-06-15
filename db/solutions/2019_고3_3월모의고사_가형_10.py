import math
from sympy import log, symbols, solve, simplify

x = symbols('x', real=True)

# 우변이 3인 경우 검증
ineq_lhs = log(x**2 - 1, 3) + log(3, 3)
ineq_3 = log(x**2 - 1, 3) + 1 - 3

# 부등식 풀기
# log_3(x^2-1) <= 2
# x^2 - 1 <= 9
# x^2 <= 10

bound = math.sqrt(10)

# 정의역 체크 및 정수 찾기
integers = []
for xi in range(-10, 11):
    # 정의역 체크
    if xi**2 - 1 > 0:
        # 부등식 체크: log_3(x^2-1) <= 2
        log_val = math.log(xi**2 - 1) / math.log(3)
        if log_val <= 2 + 1e-10:  # 수치 오차 감안
            integers.append(xi)

print(f'VERIFY_PASS' if len(integers) == 4 and integers == [-3, -2, 2, 3] else 'VERIFY_FAIL')