import sympy as sp
from sympy import sqrt, symbols, summation, simplify

# 변수 설정
p = 2
n = symbols('n', integer=True, positive=True)

# a_n = p * (sqrt(3))^(n-1)
# b_n = p * (-sqrt(3))^(n-1)

# a_3 = p * (sqrt(3))^2
a_3 = p * (sqrt(3))**2

# b_3 = p * (-sqrt(3))^2
b_3 = p * ((-sqrt(3))**2)

# a_3 + b_3 계산
result = simplify(a_3 + b_3)

# 합 검증
a_sum = p * (sqrt(3)**8 - 1) / (sqrt(3) - 1)
b_sum = p * ((-sqrt(3))**8 - 1) / ((-sqrt(3)) - 1)
total_sum = simplify(a_sum + b_sum)

# 조건 확인
if result == 12 and simplify(total_sum - 160) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')