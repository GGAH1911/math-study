import math
from sympy import symbols, solve, log, simplify
x = symbols('x')

# 정의역 확인 함수
def check_domain(val):
    return val**2 - 7*val > 0 and val + 5 > 0

# 부등식 확인 함수
def check_inequality(val):
    if not check_domain(val):
        return False
    lhs = math.log2(val**2 - 7*val) - math.log2(val + 5)
    return lhs <= 1.0000001  # 수치 오차 고려

# 정수해 찾기
integer_solutions = []
for i in range(-10, 30):
    if check_domain(i) and check_inequality(i):
        integer_solutions.append(i)

total_sum = sum(integer_solutions)
if total_sum == 26:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')