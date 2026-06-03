import sympy as sp
import numpy as np
from sympy import symbols, limit, oo, simplify

n = symbols('n', integer=True, positive=True)

# 정의한 수열
a_n = 3 / (n**2 + 1)
b_n = -11 / (4*n**2 + 1)

# 조건 1 검증
cond1 = limit((n**2 + 1) * a_n, n, oo)
print(f'Condition 1: (n²+1)aₙ → {cond1}', 'PASS' if cond1 == 3 else 'FAIL')

# 조건 2 검증
cond2 = limit((4*n**2 + 1) * (a_n + b_n), n, oo)
print(f'Condition 2: (4n²+1)(aₙ+bₙ) → {cond2}', 'PASS' if cond2 == 1 else 'FAIL')

# 구하는 극한값
result = limit((2*n**2 + 1) * (a_n + 2*b_n), n, oo)
print(f'Target: (2n²+1)(aₙ+2bₙ) → {result}')

if result == -5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')