import sympy as sp
import numpy as np

# 변수 정의
x = sp.Symbol('x', real=True)

# 원래 방정식: cos²x - 1 = 2sin(x)
eq = sp.cos(x)**2 - 1 - 2*sp.sin(x)

# 구한 해들
solutions = [sp.pi, 2*sp.pi]

# 각 해를 원래 방정식에 대입하여 검증
all_valid = True
for sol in solutions:
    result = eq.subs(x, sol)
    result_simplified = sp.simplify(result)
    if result_simplified != 0:
        all_valid = False
        print(f'x = {sol}: {result_simplified} (FAIL)')

if all_valid:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')