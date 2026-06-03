import numpy as np
from sympy import symbols, limit, oo, simplify

n = symbols('n', integer=True, positive=True)
expr = (2 * 3**(n+1) + 5) / (3**n + 2**(n+1))

# 직접 극한 계산
result = limit(expr, n, oo)
print(f'극한값: {result}')

# 수치적 검증
for test_n in [10, 20, 50, 100]:
    numerator = 2 * (3**(test_n+1)) + 5
    denominator = 3**test_n + 2**(test_n+1)
    value = numerator / denominator
    print(f'n={test_n}: {value}')

if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')