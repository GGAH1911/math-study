from sympy import symbols, Eq, solve

a1, d = symbols('a1 d')

# 조건: a2 = 3, a4 = 9
eq1 = Eq(a1 + d, 3)
eq2 = Eq(a1 + 3*d, 9)

# 연립방정식 풀기
solution = solve([eq1, eq2], [a1, d])
d_value = solution[d]

# 검증
a1_value = solution[a1]
a2 = a1_value + d_value
a4 = a1_value + 3*d_value

if a2 == 3 and a4 == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')