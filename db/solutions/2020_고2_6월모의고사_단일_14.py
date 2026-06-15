import math
from sympy import *

# 변수 정의
a, b = symbols('a b', real=True, positive=True)

# 조건 1: b = 3 + a
eq1 = Eq(b, 3 + a)

# 조건 2: 12 = 2b + a
eq2 = Eq(12, 2*b + a)

# 연립방정식 풀기
sol = solve([eq1, eq2], [a, b])
print(f'a = {sol[a]}, b = {sol[b]}')

a_val = sol[a]
b_val = sol[b]

# 역함수 검증
# f^{-1}(x) = log_3(x + a)
def f_inv(x, a):
    return math.log(x + a) / math.log(3)

# 점 1 검증: (3, log_3 b)
point1_y_from_inv = f_inv(3, a_val)
point1_y_expected = math.log(b_val) / math.log(3)
check1 = abs(point1_y_from_inv - point1_y_expected) < 1e-10

# 점 2 검증: (2b, log_3 12)
point2_y_from_inv = f_inv(2*b_val, a_val)
point2_y_expected = math.log(12) / math.log(3)
check2 = abs(point2_y_from_inv - point2_y_expected) < 1e-10

result = a_val + b_val
print(f'a + b = {result}')
print(f'Point 1 check: {check1}')
print(f'Point 2 check: {check2}')

if check1 and check2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')