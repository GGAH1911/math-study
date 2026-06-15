from sympy import symbols, expand, simplify, solve

x = symbols('x')

# 주어진 등식: x(x+1)(x+2) = (x+1)(x-1)P(x) + ax + b
# a=3, b=3으로 결정됨
a, b = 3, 3

# P(x) = x + 3으로 결정됨
P = lambda t: t + 3

# 검증: 등식이 모든 x에서 성립하는가?
lhs = x * (x + 1) * (x + 2)
rhs = (x + 1) * (x - 1) * P(x) + a * x + b

verify = expand(lhs - rhs)

if verify == 0:
    # a - b 계산
    result = P(a - b)
    print(result)
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')