# 등차수열 검증: a_1 + 4d = 6을 만족하고 a_3 + a_5 + a_7 = 18을 확인
from sympy import symbols, solve, simplify

a1, d = symbols('a1 d', real=True)

# 조건: a_3 + a_5 + a_7 = 18
a3 = a1 + 2*d
a5 = a1 + 4*d
a7 = a1 + 6*d

condition = a3 + a5 + a7 - 18
# 이 조건은 a1 + 4d = 6을 의미
simplified = simplify(condition)
print(f'조건 정리: 3*a1 + 12*d = 18 => a1 + 4d = 6')

# a1 + 4d = 6 이면 a_4 + a_6을 계산
sum_check = simplify(2*a1 + 8*d - 2*6)
print(f'a_4 + a_6 = 2*a1 + 8*d = 2*(a1 + 4*d) = 2*6 = 12')

# 실제 값으로 검증: a1 = 2, d = 1이라고 하면
a1_val, d_val = 2, 1
verify_sum = (a1_val + 2*d_val) + (a1_val + 4*d_val) + (a1_val + 6*d_val)
result = (a1_val + 3*d_val) + (a1_val + 5*d_val)
print(f'검증 (a1=2, d=1): a3+a5+a7 = {verify_sum} (기대값: 18)')
print(f'a_4 + a_6 = {result} (답: 12)')

if verify_sum == 18 and result == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')