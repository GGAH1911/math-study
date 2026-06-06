from sympy import *

CANDIDATE = 2

# 문제 조건 1: FD = 2
# 기하학적 분석에서 FD = cotα·cscα = cosα/sin²α
# 따라서: cosα/sin²α = 2
# ⟹ cosα = 2sin²α = 2(1 - cos²α)
# ⟹ cosα = 2 - 2cos²α
# ⟹ 2cos²α + cosα - 2 = 0

cos_alpha = symbols('cos_alpha', real=True)
condition_equation = 2*cos_alpha**2 + cos_alpha - 2

# 방정식의 해
solutions = solve(condition_equation, cos_alpha)
# [(-1 - sqrt(17))/4, (-1 + sqrt(17))/4]

# 기하학적으로 유효한 해: 0 < cosα < 1
# cosα = (-1 + √17)/4
cos_alpha_value = (-1 + sqrt(17))/4

# 문제 조건 2: AE = (a + b√17)/2
# 기하학적 분석에서 E는 AC의 중점이고 AE = 2cosα
# 따라서 AE = 2·(-1 + √17)/4 = (-1 + √17)/2

AE_value = 2 * cos_alpha_value
AE_simplified = simplify(AE_value)
# = (-1 + √17)/2

# 조건 3: AE = (a + b√17)/2 형태에서 a, b 추출
# (-1 + √17)/2 = (a + b√17)/2
# 양변이 같으려면: a + b√17 = -1 + √17
# 계수 비교: a = -1, b = 1

a_value = -1
b_value = 1

# 최종 계산: a² + b²
computed_result = a_value**2 + b_value**2
# = 1 + 1 = 2

# 검증: 원래 조건으로부터 계산한 값이 CANDIDATE와 일치하는가
if computed_result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')