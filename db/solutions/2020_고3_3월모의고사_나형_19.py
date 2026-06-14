import sympy as sp
from sympy import sqrt, cos, sin, acos, atan2, N

# 외접원 반지름
R = 3*sqrt(5)

# 변 AB = c = 10
c = 10

# 정현법칙: c/sin(C) = 2R
sin_C = c / (2*R)
print(f'sin C = {sin_C} = {N(sin_C)}')

# cos C 계산
cos_C_squared = 1 - sin_C**2
cos_C = sqrt(cos_C_squared)
print(f'cos C = {cos_C} = {N(cos_C)}')

# ab 구하기
# 조건: a^2 + b^2 - ab*cos(C) = (4*ab)/3
# 코사인 법칙: a^2 + b^2 = c^2 + 2*ab*cos(C)
# 따라서: c^2 + 2*ab*cos(C) - ab*cos(C) = (4*ab)/3
# c^2 + ab*cos(C) = (4*ab)/3
# 100 + ab*(2/3) = (4*ab)/3
# 100 = (4*ab)/3 - (2*ab)/3 = (2*ab)/3
# ab = 150

ab = sp.symbols('ab', positive=True)
eq = 100 + ab*cos_C - 4*ab/3
solution = sp.solve(eq, ab)
print(f'ab = {solution}')

# 검증: a = b인 경우 (대칭)
if solution:
    ab_val = solution[0]
    print(f'ab = {ab_val}')
    
    # 조건 확인
    # a = b = sqrt(ab_val)인 경우
    a_val = sqrt(ab_val)
    b_val = sqrt(ab_val)
    
    # 코사인 법칙 확인: c^2 = a^2 + b^2 - 2ab*cos(C)
    c_check_sq = a_val**2 + b_val**2 - 2*a_val*b_val*cos_C
    print(f'c^2 check: {c_check_sq} = {N(c_check_sq)} (should be 100)')
    
    # 주어진 조건 확인
    condition = (a_val**2 + b_val**2 - a_val*b_val*cos_C) / (a_val*b_val)
    print(f'Condition check: {condition} = {N(condition)} (should be 4/3)')
    
    if abs(N(condition - 4/3)) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')