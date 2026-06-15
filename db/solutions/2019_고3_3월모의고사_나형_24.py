CANDIDATE = 33

import sympy as sp

# A, B를 미지수로 정의
A, B = sp.symbols('A B')

# 주어진 조건을 방정식으로 표현
eq1 = sp.Eq(A + 2*B, 9)        # lim(a_n + 2*b_n) = 9
eq2 = sp.Eq(2*A + B, 90)       # lim(2*a_n + b_n) = 90

# 연립방정식 풀이
solution = sp.solve([eq1, eq2], [A, B])
A_val = solution[A]
B_val = solution[B]

# 구하는 값: A + B
result = A_val + B_val

# CANDIDATE 검증
if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')