from sympy import symbols, Eq, solve

# 변수 정의
A, B = symbols('A B', real=True)

# 주어진 조건
eq1 = Eq(A, 2*B - 10)
eq2 = Eq(3*A + B, 33)

# 연립방정식 풀이
solution = solve([eq1, eq2], [A, B])
B_value = solution[B]

# 답 검증
A_value = 2*B_value - 10
check = 3*A_value + B_value

if check == 33 and B_value == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')