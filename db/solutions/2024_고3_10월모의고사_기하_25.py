import sympy as sp
from sympy import sqrt, symbols, solve, Eq

# 벡터의 내적을 변수로 설정
a_mag_sq = 2  # |a|^2 = 2
a_dot_b = symbols('a_dot_b', real=True)
b_mag_sq = symbols('b_mag_sq', real=True, positive=True)

# 조건 1: |2a + b|^2 = 13
eq1 = Eq(4*a_mag_sq + 4*a_dot_b + b_mag_sq, 13)

# 조건 2: |a - b|^2 = 1
eq2 = Eq(a_mag_sq - 2*a_dot_b + b_mag_sq, 1)

# 연립방정식 풀이
sol = solve([eq1, eq2], [a_dot_b, b_mag_sq])
a_dot_b_val = sol[a_dot_b]
b_mag_sq_val = sol[b_mag_sq]

# |a + b|^2 계산
a_plus_b_sq = a_mag_sq + 2*a_dot_b_val + b_mag_sq_val
a_plus_b = sqrt(a_plus_b_sq)

# 검증: 구한 값이 답이 맞는지 확인
assert a_dot_b_val == 1, f'a·b should be 1, got {a_dot_b_val}'
assert b_mag_sq_val == 1, f'|b|^2 should be 1, got {b_mag_sq_val}'
assert a_plus_b_sq == 5, f'|a+b|^2 should be 5, got {a_plus_b_sq}'
assert a_plus_b == sqrt(5), f'|a+b| should be sqrt(5), got {a_plus_b}'

print('VERIFY_PASS')