import sympy as sp
from sympy import log, symbols, solve, Abs

CANDIDATE = 26

x = symbols('x', real=True)

# 부등식 조건
inequality = log(x**2 - 7*x, 2) - log(x + 5, 2) <= 1

# 정의역 조건
domain1 = x**2 - 7*x > 0  # x < 0 or x > 7
domain2 = x + 5 > 0  # x > -5

# 정의역: (-5, 0) or (7, ∞)
valid_integers = []
for test_x in range(-10, 20):
    if test_x > -5 and test_x < 0:
        valid_integers.append(test_x)
    elif test_x > 7:
        valid_integers.append(test_x)

# 각 정수에서 부등식 확인
solutions = []
for test_x in valid_integers:
    try:
        val1 = (test_x**2 - 7*test_x)
        val2 = (test_x + 5)
        if val1 > 0 and val2 > 0:
            lhs = float(log(val1, 2) - log(val2, 2))
            if lhs <= 1 + 1e-9:
                solutions.append(test_x)
    except:
        pass

computed_sum = sum(solutions)

if computed_sum == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')