import sympy as sp
from sympy import symbols, ln, exp, integrate, diff

# 우리의 답: 31
answer = 31

# 역검증: 주어진 조건이 만족되는지 확인
# f(1) = 4*ln(2)이므로 e^f(1) = 16
e_f_1 = 16
e_f_2 = 25

# 조건 1: 2*e^f(2) - e^f(1) = 34
check1 = 2*e_f_2 - e_f_1
print(f'조건 1 검증: 2*e^f(2) - e^f(1) = {check1}, 기댓값 = 34, 통과: {check1 == 34}')

# 조건 2: [x^2*e^f(x)]_1^2 - 2*∫xe^f(x)dx = 4*e^f(2) - e^f(1) - 2*∫xe^f(x)dx
# ∫xg(x)dx = ∫xe^f(x)dx + 4*e^f(2) - e^f(1) - 2*∫xe^f(x)dx
# 53 = -∫xe^f(x)dx + 100 - 16
# ∫xe^f(x)dx = 31
integral_check = -answer + 4*e_f_2 - e_f_1
print(f'조건 2로부터: -∫xe^f(x)dx + 100 - 16 = {integral_check}, 기댓값 = 53, 통과: {integral_check == 53}')

if check1 == 34 and integral_check == 53:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')