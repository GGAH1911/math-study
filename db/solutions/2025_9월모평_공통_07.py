# 연속성 조건 검증
from sympy import symbols, solve, simplify

a = symbols('a', real=True)

# x=4에서 연속 조건: (4-a)^2 = 4
continuity_eq = (4 - a)**2 - 4

# a의 값들 구하기
a_values = solve(continuity_eq, a)
a_values = sorted([float(val) for val in a_values])

# 각 a에 대해 연속성 확인
for a_val in a_values:
    left_limit = (4 - a_val)**2
    right_limit = 2*4 - 4
    assert abs(left_limit - right_limit) < 1e-10

# 곱 계산
product = 1
for a_val in a_values:
    product *= a_val

product = int(round(product))

if product == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')