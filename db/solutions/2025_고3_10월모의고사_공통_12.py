import numpy as np
from sympy import symbols, solve, simplify

n_val = symbols('n', integer=True, positive=True)
a_val = symbols('a', integer=True)

# 원래 방정식: 3a^2 + 2na - 8n^2 = 0
def verify_equation(n, a):
    return 3*a**2 + 2*n*a - 8*n**2

# 각 선택지 검증
total_M = 0
total_m = 0

for n in range(1, 31):
    # 가능한 a_n 값들
    a_candidates = []
    
    # a_n = 4n/3
    if n % 3 == 0:
        a_candidates.append(4*n // 3)
    
    # a_n = -2n
    a_candidates.append(-2*n)
    
    # 각 후보가 원래 방정식을 만족하는지 확인
    for a in a_candidates:
        result = verify_equation(n, a)
        assert result == 0, f'n={n}, a={a} failed equation check'
    
    # 최댓값: 3의 배수일 때만 4n/3 선택
    if n % 3 == 0:
        total_M += 4*n // 3
    else:
        total_M += -2*n
    
    # 최솟값: 항상 -2n 선택
    total_m += -2*n

M = total_M
m = total_m
result = M - m

if result == 550:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')