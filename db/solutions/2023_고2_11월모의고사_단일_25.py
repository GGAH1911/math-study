from sympy import symbols, solve, simplify
from math import log

CANDIDATE = 8

# 원래 문제: log_2(x) - 3 = log_x(16)을 만족하는 모든 x의 곱
#
# 풀이 과정:
# t = log_2(x)로 치환하면
# log_x(16) = 4/t (∵ log_x(16) = log_x(2^4) = 4/log_2(x) = 4/t)
# 
# 방정식이 t - 3 = 4/t로 변환됨
# t^2 - 3t - 4 = 0
# (t - 4)(t + 1) = 0
# t = 4 또는 t = -1

# Step 1: t에 대한 이차방정식 풀기
t = symbols('t', real=True)
t_equation = t**2 - 3*t - 4
t_roots = solve(t_equation, t)

# Step 2: x = 2^t로 변환
x_roots = [2**root for root in t_roots]

# Step 3: 각 해를 원래 방정식에 대입해 검증
def verify_in_original_equation(x_val):
    """원래 방정식: log_2(x) - 3 = log_x(16)"""
    x_numeric = float(x_val)
    
    # 정의역 체크 (x > 0, x ≠ 1)
    if x_numeric <= 0 or x_numeric == 1:
        return False
    
    # 좌변: log_2(x) - 3
    lhs = log(x_numeric, 2) - 3
    
    # 우변: log_x(16)
    rhs = log(16, x_numeric)
    
    # 부동소수점 오차 범위 내에서 같은지 확인
    return abs(lhs - rhs) < 1e-9

# Step 4: 모든 해가 원래 방정식을 만족하는지 확인
all_valid = all(verify_in_original_equation(x_val) for x_val in x_roots)

# Step 5: 모든 해의 곱 계산
product = 1
for x_val in x_roots:
    product *= x_val
product = simplify(product)

# Step 6: CANDIDATE와 비교
if all_valid and abs(float(product) - CANDIDATE) < 1e-9:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")