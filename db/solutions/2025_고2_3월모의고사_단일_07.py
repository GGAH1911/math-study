import sympy as sp
a, b = sp.symbols('a b', real=True)
eq1 = a - b - 2
eq2 = a**3 - b**3 - 32
ab_value = 4

# 주어진 조건을 만족하는 a, b 구하기
from sympy import solve
solutions = solve([eq1, eq2], [a, b])
print(f'Solutions: {solutions}')

# 각 해에 대해 ab 확인
for sol in solutions:
    a_val, b_val = sol
    ab_check = a_val * b_val
    eq1_check = a_val - b_val
    eq2_check = a_val**3 - b_val**3
    print(f'a={a_val}, b={b_val}, ab={ab_check}, a-b={eq1_check}, a³-b³={eq2_check}')
    if sp.simplify(ab_check - 4) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')