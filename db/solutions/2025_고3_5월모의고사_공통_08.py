import numpy as np
from sympy import symbols, Abs, solve

x = symbols('x', integer=True)
ineq = 2**Abs(x) + 64/(2**Abs(x)) - 20

# 정수 해 찾기
solutions = []
for val in range(-10, 11):
    result = float(2**abs(val) + 64/(2**abs(val)))
    if result <= 20.0001:  # 부동소수점 오차 허용
        solutions.append(val)

print('Solutions:', solutions)
print('Count:', len(solutions))

# 검증
for sol in solutions:
    check = 2**abs(sol) + 64/(2**abs(sol))
    print(f'x={sol}: 2^{abs(sol)} + 64/2^{abs(sol)} = {check}')

if len(solutions) == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')