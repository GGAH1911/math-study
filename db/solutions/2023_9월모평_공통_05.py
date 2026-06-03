from sympy import symbols, Eq, solve

# 등차수열: a_n = a_1 + (n-1)d
a1, d = symbols('a1 d')

# 조건 1: a_1 = 2*a_5
cond1 = Eq(a1, 2*(a1 + 4*d))

# 조건 2: a_8 + a_12 = -6
cond2 = Eq((a1 + 7*d) + (a1 + 11*d), -6)

# 연립방정식 풀기
sol = solve([cond1, cond2], [a1, d])

# 풀이 결과
a1_val = sol[a1]
d_val = sol[d]
a2 = a1_val + d_val

# 검증
verify1 = a1_val == 2*(a1_val + 4*d_val)
verify2 = (a1_val + 7*d_val) + (a1_val + 11*d_val) == -6

if verify1 and verify2 and a2 == 21:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')