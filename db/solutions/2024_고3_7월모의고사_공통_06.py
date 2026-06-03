from sympy import symbols, Eq, solve, Rational

a1, r = symbols('a1 r', positive=True, real=True)

# 조건 1: (a3 + a4)/(a1 + a2) = 4
cond1 = Eq((a1*r**2 + a1*r**3)/(a1 + a1*r), 4)

# 조건 2: a2 * a4 = 1
cond2 = Eq(a1*r * a1*r**3, 1)

# 연립방정식 풀기
sol = solve([cond1, cond2], [a1, r])

# 양수 해만 선택
for solution in sol:
    a1_val, r_val = solution
    if a1_val > 0 and r_val > 0:
        a1_num = a1_val
        r_num = r_val
        break

# a6, a7 계산
a6 = a1_num * r_num**5
a7 = a1_num * r_num**6
result = a6 + a7

# 검증
check_cond1 = (a1_num * r_num**2 + a1_num * r_num**3) / (a1_num + a1_num * r_num)
check_cond2 = a1_num * r_num * a1_num * r_num**3

if abs(check_cond1 - 4) < 1e-10 and abs(check_cond2 - 1) < 1e-10 and result == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')