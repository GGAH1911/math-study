import sympy as sp

# 문제에서 구한 R(x) = -5x + 16
a, b = -5, 16

# R(x)의 정의
def R(x):
    return a * x + b

# 조건 (가) 검증: P(2) + P(3) = 7
P2 = R(2)  # 2a + b
P3 = R(3)  # 3a + b
condition_a = P2 + P3
print(f'조건 (가): P(2) + P(3) = {P2} + {P3} = {condition_a}')
assert condition_a == 7, f'조건 (가) 실패: {condition_a} != 7'

# 조건 (나) 검증: R(1) - R(2) = 5
R1 = R(1)
R2 = R(2)
condition_b = R1 - R2
print(f'조건 (나): R(1) - R(2) = {R1} - {R2} = {condition_b}')
assert condition_b == 5, f'조건 (나) 실패: {condition_b} != 5'

print(f'\n최종 답: R(1) = {R1}')
print('VERIFY_PASS')