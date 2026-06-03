from sympy import symbols, limit, oo, simplify, solve, Eq
from sympy import Rational

x = symbols('x', positive=True, real=True)
n = symbols('n', integer=True, positive=True)

# 각 구간에서 f(x) 정의
def f_value(x_val):
    if 0 < x_val < 2:
        return x_val / 4
    elif x_val == 2:
        return 1
    else:  # x > 2
        return x_val

# 각 영역에서 방정식 검증
x1 = Rational(12, 7)
x2 = 2
x3 = 3

# 검증
test1 = abs(f_value(float(x1)) - (2*float(x1) - 3)) < 1e-10
test2 = abs(f_value(x2) - (2*x2 - 3)) < 1e-10
test3 = abs(f_value(x3) - (2*x3 - 3)) < 1e-10

# 합 계산
total_sum = x1 + x2 + x3
expected = Rational(47, 7)

if test1 and test2 and test3 and total_sum == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')