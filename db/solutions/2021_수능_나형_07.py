from sympy import symbols, solve, simplify
import math

x = symbols('x', real=True)

# 원래 부등식: (1/9)^x < 3^(21-4x)
# 이를 지수 형태로: 3^(-2x) < 3^(21-4x)
# 로그를 취하면: -2x < 21 - 4x
# 정리하면: 2x < 21 즉, x < 10.5

# 자연수 x의 개수 확인
count = 0
for natural_x in range(1, 20):  # 충분한 범위 확인
    lhs = (1/9)**natural_x
    rhs = 3**(21 - 4*natural_x)
    if lhs < rhs:
        count += 1
    else:
        break

if count == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')