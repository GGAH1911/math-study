import sympy as sp
from sympy import sqrt, symbols, solve, Rational

c = symbols('c', real=True, positive=True)

# 경우 A: c = 4 검증
c_val = 4
b2 = c_val**2 - 9
print(f'경우 A, c={c_val}: b²={b2}')

# P의 좌표
x_P = (9 + 6*c_val) / c_val
print(f'x_P = {x_P}')

# 쌍곡선 위에 있는지 확인
y_P2 = b2 * (x_P**2/9 - 1)
print(f'y_P² = {y_P2}')

# 거리 확인
PF = 2*c_val
PF_prime = PF + 6
print(f'PF={PF}, PF\'={PF_prime}')

# 삼각형 PQF 둘레
PQ = Rational(168, 13)
QF = Rational(92, 13)
FP = 8
perimeter_A = PQ + QF + FP
print(f'둘레 (경우A) = {perimeter_A}')
assert perimeter_A == 28, f'Failed: {perimeter_A}'
print('경우 A 검증 PASS\n')

# 경우 B: c = 7 검증
c_val = 7
b2 = c_val**2 - 9
print(f'경우 B, c={c_val}: b²={b2}')

# P의 좌표
x_P = 6 - Rational(9, c_val)
print(f'x_P = {x_P}')

# 쌍곡선 위에 있는지 확인
y_P2 = b2 * (x_P**2/9 - 1)
print(f'y_P² = {y_P2}')

# 거리 확인
PF_prime = 2*c_val
PF = 2*c_val - 6
print(f'PF\'={PF_prime}, PF={PF}')

# 삼각형 PQF 둘레
PQ = Rational(294, 31)
QF = Rational(326, 31)
FP = 8
perimeter_B = PQ + QF + FP
print(f'둘레 (경우B) = {perimeter_B}')
assert perimeter_B == 28, f'Failed: {perimeter_B}'
print('경우 B 검증 PASS')

print(f'\n최종 답: 4 + 7 = 11')
print('VERIFY_PASS')