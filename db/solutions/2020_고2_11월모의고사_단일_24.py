CANDIDATE = 12

import sympy as sp
from sympy import symbols, solve, simplify

a = symbols('a', real=True)

# 주어진 조건: 4^a = 4/9
condition = 4**a - 4/9

# 조건을 만족하는 a 구하기
a_value = solve(condition, a)

if a_value:
    a_val = a_value[0]
    
    # 2^(3-a) 계산
    result = 2**(3 - a_val)
    result_simplified = simplify(result)
    result_float = float(result_simplified)
    
    # 후보값과 비교
    if abs(result_float - CANDIDATE) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')